from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app.extensions import db
from app.forms import LoginForm, RegistrationForm
from app.models.user import User
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            
            
            session['theme'] = 'light'  
            flash('Login successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Username or password incorrect.', 'danger')
    
    return render_template('login.html.j2', title='login', form=form)

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
        
        
        response = redirect(url_for('auth.login'))
        response.set_cookie('preferred_language', 'zh-CN', max_age=30*24*3600)
        
        flash('Registration successful, please log in', 'success')
        return response
    
    return render_template('register.html.j2', title='register', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('main.index'))