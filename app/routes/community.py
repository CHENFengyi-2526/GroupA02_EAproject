from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.community import Question, Answer, Comment
from app.forms import QuestionForm, AnswerForm, CommentForm

bp = Blueprint('community', __name__)

@bp.route('/')
def questions():
    questions = Question.query.order_by(Question.created_at.desc()).all()
    return render_template('community/questions.html', questions=questions)

@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = QuestionForm()
    if form.validate_on_submit():
        q = Question(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(q)
        db.session.commit()
        flash('Question posted.', 'success')
        return redirect(url_for('community.question_detail', id=q.id))
    return render_template('community/ask.html', form=form)

@bp.route('/<int:id>')
def question_detail(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    return render_template('community/question_detail.html', question=question, form=form)

@bp.route('/<int:id>/answer', methods=['POST'])
@login_required
def answer(id):
    question = Question.query.get_or_404(id)
    form = AnswerForm()
    if form.validate_on_submit():
        ans = Answer(content=form.content.data, user_id=current_user.id, question_id=question.id)
        db.session.add(ans)
        db.session.commit()
        flash('Answer posted.', 'success')
    return redirect(url_for('community.question_detail', id=question.id))

