import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # ==================== Cloud SQL for MySQL ====================
    INSTANCE_CONNECTION_NAME = os.environ.get('INSTANCE_CONNECTION_NAME')
    DB_USER = os.environ.get('DB_USER', 'root')           
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME', 'eadb')           

    if INSTANCE_CONNECTION_NAME:
        # 使用 Cloud SQL Proxy (TCP 3306)
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@127.0.0.1:3306/{DB_NAME}"
    else:

        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_DURATION = 3600
    POSTS_PER_PAGE = 10