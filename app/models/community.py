from app.extensions import db
from datetime import datetime

class DiscussionPost(db.Model):
    
    __tablename__ = 'discussion_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), default='general')  # general, help, showcase
    view_count = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    is_closed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    comments = db.relationship('PostComment', backref='post', lazy='dynamic', cascade='all, delete-orphan')


class PostComment(db.Model):
    
    __tablename__ = 'post_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('discussion_posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    like_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    parent_id = db.Column(db.Integer, db.ForeignKey('post_comments.id'))  # 支持嵌套回复
    replies = db.relationship('PostComment', backref=db.backref('parent', remote_side=[id]))


class PostLike(db.Model):
    
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('discussion_posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id'),)