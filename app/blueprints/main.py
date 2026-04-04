from flask import Blueprint, render_template, current_app
from flask import make_response, session
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():

    resp = make_response(render_template('index.html'))

    visit_count = int(request.cookies.get('visit_count', 0)) + 1
    resp.set_cookie('visit_count', str(visit_count), max_age=60*60*24*365)

    if 'language' not in session:
        session['language'] = 'en'
    return resp