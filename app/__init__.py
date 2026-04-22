from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from app.extensions import db, login_manager, bootstrap



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate = Migrate(app, db)
    

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.tutorials import bp as tutorials_bp
    app.register_blueprint(tutorials_bp, url_prefix='/tutorials')
    
    from app.blueprints.resources import bp as resources_bp
    app.register_blueprint(resources_bp, url_prefix='/resources')
    
    from app.blueprints.community import bp as community_bp
    app.register_blueprint(community_bp, url_prefix='/community')
    
    from app.blueprints.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    
    with app.app_context():
        from app.models.user import User, Role
        from app.models.tutorial import Tutorial, Category, Tag
        from app.models.resource import Resource, ResourceCategory, Download
        from app.models.community import DiscussionPost, PostComment, PostLike

        db.create_all()

        import os
        dump_file = os.path.join(os.path.dirname(__file__), '..', 'instance', 'database_dump.sql')
        
        if os.path.exists(dump_file):
            try:
                with open(dump_file, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                
                for statement in sql_script.split(';'):
                    if statement.strip():
                        db.session.execute(statement)
                
                db.session.commit()
                print("✅ 測試資料已成功匯入到資料庫！")
                

            except Exception as e:
                print(f"⚠️ 匯入測試資料時發生錯誤: {e}")
        else:
            print("ℹ️ 沒有找到 database_dump.sql，跳過資料匯入。")

    return app