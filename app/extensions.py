from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
mail = Mail()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(int(user_id))