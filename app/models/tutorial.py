from app.extensions import db
from datetime import datetime

class TutorialCategory(db.Model):
    
    __tablename__ = 'tutorial_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    
    tutorials = db.relationship('Tutorial', backref='category', lazy='dynamic')


class Tutorial(db.Model):
    
    __tablename__ = 'tutorials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    summary = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    estimated_minutes = db.Column(db.Integer, default=10)
    is_published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('tutorial_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    steps = db.relationship('TutorialStep', backref='tutorial', lazy='dynamic', cascade='all, delete-orphan')


class TutorialStep(db.Model):
    
    __tablename__ = 'tutorial_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorials.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    code_snippet = db.Column(db.Text)  
    image_url = db.Column(db.String(500))
    
    __table_args__ = (db.UniqueConstraint('tutorial_id', 'step_number'),)


class UserTutorialProgress(db.Model):
    
    __tablename__ = 'user_tutorial_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorials.id'), nullable=False)
    completed_steps = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'tutorial_id'),)