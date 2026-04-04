from flask import render_template,Blueprint
from app.models.tutorial import Tutorial
from app.models.resource import Resource

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    latest_tutorials = Tutorial.query.filter_by(is_published=True).order_by(Tutorial.created_at.desc()).limit(5).all()
    featured_resources = Resource.query.filter_by(is_featured=True).order_by(Resource.created_at.desc()).limit(5).all()
    return render_template('index.html.j2', latest_tutorials=latest_tutorials, featured_resources=featured_resources)