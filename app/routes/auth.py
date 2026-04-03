from flask import Blueprint, render_template, redirect, url_for, flash, request, session, make_response
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db
from app.models.user import User, UserProfile
from app.forms import LoginForm, RegistrationForm
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            resp = make_response(redirect(url_for('main.index')))
            resp.set_cookie('theme', 'light', max_age=60*60*24*30)
            flash(f'Welcome back, {user.username}!', 'success')
            return resp
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))