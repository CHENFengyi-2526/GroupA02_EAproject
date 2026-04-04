from app.extensions import db
from datetime import datetime

class ResourceCategory(db.Model):
   
    __tablename__ = 'resource_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    icon = db.Column(db.String(50))
    
    resources = db.relationship('Resource', backref='category', lazy='dynamic')


class Resource(db.Model):

    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)  # 'ebook', 'video', 'sample', 'tool'
    download_url = db.Column(db.String(500))
    external_link = db.Column(db.String(500))
    file_size = db.Column(db.String(50))
    download_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('resource_categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tags = db.relationship('ResourceTag', secondary='resource_tag_association', backref='resources')


class ResourceTag(db.Model):
    
    __tablename__ = 'resource_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)



resource_tag_association = db.Table('resource_tag_association',
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('resource_tags.id'))
)


class ResourceDownload(db.Model):
    
    __tablename__ = 'resource_downloads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))