# app/blueprints/tutorials.py
from flask import render_template, redirect, url_for, flash, request, abort, session,Blueprint
from flask_login import login_required, current_user
from app.decorators import admin_required
from app.extensions import db
from app.models.tutorial import Tutorial, TutorialCategory, TutorialStep, UserTutorialProgress
from app.forms import TutorialForm, TutorialStepForm

bp = Blueprint('tutorials', __name__, url_prefix='/tutorials')

@bp.route('/')
def list():
    category_slug = request.args.get('category')
    if category_slug:
        category = TutorialCategory.query.filter_by(slug=category_slug).first_or_404()
        tutorials = Tutorial.query.filter_by(category_id=category.id, is_published=True).all()
    else:
        tutorials = Tutorial.query.filter_by(is_published=True).all()
    categories = TutorialCategory.query.order_by(TutorialCategory.sort_order).all()
    return render_template('tutorials_list.html.j2', tutorials=tutorials, categories=categories)


@bp.route('/<slug>')
def view(slug):
    tutorial = Tutorial.query.filter_by(slug=slug).first_or_404()
    if not tutorial.is_published and not (current_user.is_authenticated and current_user.is_admin()):
        abort(404)
    
    if not session.get(f'viewed_tutorial_{tutorial.id}'):
        tutorial.view_count += 1
        db.session.commit()
        session[f'viewed_tutorial_{tutorial.id}'] = True
    
    progress = None
    if current_user.is_authenticated:
        progress = UserTutorialProgress.query.filter_by(user_id=current_user.id, tutorial_id=tutorial.id).first()
    return render_template('tutorials/view.html', tutorial=tutorial, progress=progress)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = TutorialForm()
    if form.validate_on_submit():
        tutorial = Tutorial(
            title=form.title.data,
            slug=form.slug.data,
            summary=form.summary.data,
            content=form.content.data,
            difficulty=form.difficulty.data,
            estimated_minutes=form.estimated_minutes.data,
            is_published=form.is_published.data,
            category_id=form.category_id.data
        )
        db.session.add(tutorial)
        db.session.commit()
        flash('Tutorial created successfully', 'success')
        return redirect(url_for('tutorials.view', slug=tutorial.slug))
    return render_template('tutorials/create.html', form=form)

@bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(slug):
    tutorial = Tutorial.query.filter_by(slug=slug).first_or_404()
    form = TutorialForm(obj=tutorial)
    if form.validate_on_submit():
        tutorial.title = form.title.data
        tutorial.slug = form.slug.data
        tutorial.summary = form.summary.data
        tutorial.content = form.content.data
        tutorial.difficulty = form.difficulty.data
        tutorial.estimated_minutes = form.estimated_minutes.data
        tutorial.is_published = form.is_published.data
        tutorial.category_id = form.category_id.data
        db.session.commit()
        flash('Tutorial updated', 'success')
        return redirect(url_for('tutorials.view', slug=tutorial.slug))
    return render_template('tutorials/edit.html', form=form, tutorial=tutorial)

@bp.route('/<slug>/delete', methods=['POST'])
@login_required
@admin_required
def delete(slug):
    tutorial = Tutorial.query.filter_by(slug=slug).first_or_404()
    db.session.delete(tutorial)
    db.session.commit()
    flash('Tutorial deleted', 'success')
    return redirect(url_for('tutorials.list'))

@bp.route('/<slug>/step/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_step(slug):
    tutorial = Tutorial.query.filter_by(slug=slug).first_or_404()
    form = TutorialStepForm()
    if form.validate_on_submit():
        step = TutorialStep(
            tutorial_id=tutorial.id,
            step_number=form.step_number.data,
            title=form.title.data,
            content=form.content.data,
            code_snippet=form.code_snippet.data,
            image_url=form.image_url.data
        )
        db.session.add(step)
        db.session.commit()
        flash('Step added', 'success')
        return redirect(url_for('tutorials.view', slug=tutorial.slug))
    return render_template('tutorials/step_form.html', form=form, tutorial=tutorial)

@bp.route('/step/<int:step_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_step(step_id):
    step = TutorialStep.query.get_or_404(step_id)
    form = TutorialStepForm(obj=step)
    if form.validate_on_submit():
        step.step_number = form.step_number.data
        step.title = form.title.data
        step.content = form.content.data
        step.code_snippet = form.code_snippet.data
        step.image_url = form.image_url.data
        db.session.commit()
        flash('Steps updated', 'success')
        return redirect(url_for('tutorials.view', slug=step.tutorial.slug))
    return render_template('tutorials/step_form.html', form=form, tutorial=step.tutorial)

@bp.route('/step/<int:step_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_step(step_id):
    step = TutorialStep.query.get_or_404(step_id)
    tutorial_slug = step.tutorial.slug
    db.session.delete(step)
    db.session.commit()
    flash('Step deleted', 'success')
    return redirect(url_for('tutorials.view', slug=tutorial_slug))


@bp.route('/my-progress')
@login_required
def my_progress():
    progress_list = UserTutorialProgress.query.filter_by(user_id=current_user.id).all()
    return render_template('tutorials/my_progress.html', progress_list=progress_list)

@bp.route('/<slug>/update-progress', methods=['POST'])
@login_required
def update_progress(slug):
    tutorial = Tutorial.query.filter_by(slug=slug).first_or_404()
    completed = request.form.get('completed_steps', type=int, default=0)
    progress = UserTutorialProgress.query.filter_by(user_id=current_user.id, tutorial_id=tutorial.id).first()
    if not progress:
        progress = UserTutorialProgress(user_id=current_user.id, tutorial_id=tutorial.id)
        db.session.add(progress)
    progress.completed_steps = completed
    progress.is_completed = (completed >= len(tutorial.steps.all()))
    if progress.is_completed and not progress.completed_at:
        progress.completed_at = datetime.utcnow()
    db.session.commit()
    flash('Progress updated', 'success')
    return redirect(url_for('tutorials.view', slug=tutorial.slug))