from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes import main, auth, tutorials, community, resources
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(tutorials.bp, url_prefix='/tutorials')
    app.register_blueprint(community.bp, url_prefix='/community')
    app.register_blueprint(resources.bp, url_prefix='/resources')

    return app