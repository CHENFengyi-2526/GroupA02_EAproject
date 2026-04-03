from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User, UserProfile, UserActivityLog
from app.models.tutorial import Tutorial, Lesson
from app.models.community import Question, Answer, Comment
from app.models.resource import Resource, Category, ResourceTag

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(func):
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

@bp.route('/')
@login_required
@admin_required
def dashboard():

    user_count = User.query.count()
    tutorial_count = Tutorial.query.count()
    question_count = Question.query.count()
    resource_count = Resource.query.count()
    return render_template('admin/dashboard.html',
                         user_count=user_count,
                         tutorial_count=tutorial_count,
                         question_count=question_count,
                         resource_count=resource_count)


@bp.route('/users')
@login_required
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/user/<int:id>/toggle_admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'danger')
        return redirect(url_for('admin.list_users'))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'User {user.username} admin status updated.', 'success')
    return redirect(url_for('admin.list_users'))

@bp.route('/user/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin.list_users'))
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted.', 'success')
    return redirect(url_for('admin.list_users'))


@bp.route('/tutorials')
@login_required
@admin_required
def list_tutorials():
    tutorials = Tutorial.query.all()
    return render_template('admin/tutorials.html', tutorials=tutorials)

@bp.route('/tutorial/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tutorial(id):
    tutorial = Tutorial.query.get_or_404(id)
    db.session.delete(tutorial)
    db.session.commit()
    flash('Tutorial deleted.', 'success')
    return redirect(url_for('admin.list_tutorials'))


@bp.route('/questions')
@login_required
@admin_required
def list_questions():
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)

@bp.route('/question/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted.', 'success')
    return redirect(url_for('admin.list_questions'))


@bp.route('/resources')
@login_required
@admin_required
def list_resources():
    resources = Resource.query.all()
    return render_template('admin/resources.html', resources=resources)

@bp.route('/resource/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    flash('Resource deleted.', 'success')
    return redirect(url_for('admin.list_resources'))