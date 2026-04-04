from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from app.config import config

from .extensions import db, login_manager, bootstrap, admin, migrate

from .blueprints import auth, main, tutorials, community, resources

def app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    admin.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(tutorials.bp, url_prefix='/tutorials')
    app.register_blueprint(community.bp, url_prefix='/community')
    app.register_blueprint(resources.bp, url_prefix='/resources')
    
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app