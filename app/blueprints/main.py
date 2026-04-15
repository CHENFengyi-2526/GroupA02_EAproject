from flask import render_template,Blueprint,make_response, request, url_for, flash, redirect
from app.models.tutorial import Tutorial
from app.models.resource import Resource
from flask_login import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    latest_tutorials = Tutorial.query.filter_by(is_published=True).order_by(Tutorial.created_at.desc()).limit(5).all()
    featured_resources = Resource.query.filter_by(is_featured=True).order_by(Resource.created_at.desc()).limit(5).all()
    return render_template('index.html.j2', latest_tutorials=latest_tutorials, featured_resources=featured_resources)

@bp.route('/user/<username>')
@login_required
def user_profile(username):
    from app.models.user import User
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html.j2', user=user)

@bp.route('/set-language/<lang>')
def set_language(lang):
    if lang not in ['en', 'zh', 'ja', 'ko']:
        flash('Invalid language', 'danger')
        return redirect(request.referrer or url_for('main.index'))
    
    resp = make_response(redirect(request.referrer or url_for('main.index')))
    resp.set_cookie('preferred_language', lang, max_age=30*24*3600) 
    flash(f'Language preference set to {lang}', 'success')
    return resp

@bp.route('/show-cookie')
def show_cookie():
    lang = request.cookies.get('preferred_language', 'not set')
    return f'Your preferred language is: {lang}'