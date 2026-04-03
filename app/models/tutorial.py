from app.extensions import db
from datetime import datetime

class Tutorial(db.Model):
    __tablename__ = 'tutorials'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref='tutorials')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tutorial_id = db.Column(db.Integer, db.ForeignKey('tutorials.id'))
    order = db.Column(db.Integer, default=0)
    tutorial = db.relationship('Tutorial', backref='lessons')

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    user = db.relationship('User')
    lesson = db.relationship('Lesson')