from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.tutorial import Tutorial, Lesson, UserProgress
from app.forms import TutorialForm, LessonForm

bp = Blueprint('tutorials', __name__)


@bp.route('/')
def list_tutorials():
    tutorials = Tutorial.query.all()
    return render_template('tutorials/list.html', tutorials=tutorials)


@bp.route('/<int:id>')
def view_tutorial(id):
    tutorial = Tutorial.query.get_or_404(id)
    return render_template('tutorials/detail.html', tutorial=tutorial)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_tutorial():
    if not current_user.is_admin:
        abort(403)
    form = TutorialForm()
    if form.validate_on_submit():
        tutorial = Tutorial(title=form.title.data, description=form.description.data, created_by=current_user.id)
        db.session.add(tutorial)
        db.session.commit()
        flash('Tutorial created.', 'success')
        return redirect(url_for('tutorials.view_tutorial', id=tutorial.id))
    return render_template('tutorials/edit.html', form=form, title='New Tutorial')


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tutorial(id):
    if not current_user.is_admin:
        abort(403)
    tutorial = Tutorial.query.get_or_404(id)
    form = TutorialForm(obj=tutorial)
    if form.validate_on_submit():
        tutorial.title = form.title.data
        tutorial.description = form.description.data
        db.session.commit()
        flash('Tutorial updated.', 'success')
        return redirect(url_for('tutorials.view_tutorial', id=tutorial.id))
    return render_template('tutorials/edit.html', form=form, title='Edit Tutorial')


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_tutorial(id):
    if not current_user.is_admin:
        abort(403)
    tutorial = Tutorial.query.get_or_404(id)
    db.session.delete(tutorial)
    db.session.commit()
    flash('Tutorial deleted.', 'success')
    return redirect(url_for('tutorials.list_tutorials'))

