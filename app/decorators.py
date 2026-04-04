from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Requires administrator rights', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def login_required_with_message(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function