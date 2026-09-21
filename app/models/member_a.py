from app.extensions import db
from datetime import datetime


class ElderlyProfile(db.Model):
    __tablename__ = 'elderly_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    family_links = db.relationship('FamilyElderlyLink', backref='elderly_profile', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<ElderlyProfile {self.full_name}>'


class FamilyContact(db.Model):
    __tablename__ = 'family_contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    relationship = db.Column(db.String(50))
    is_emergency = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<FamilyContact {self.contact_name}>'


class UserDevice(db.Model):
    __tablename__ = 'user_devices'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_name = db.Column(db.String(120))
    device_type = db.Column(db.String(50))
    device_uuid = db.Column(db.String(120), unique=True)
    last_active = db.Column(db.DateTime)

    def __repr__(self):
        return f'<UserDevice {self.device_name}>'


class ConsentRecord(db.Model):
    __tablename__ = 'consent_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consent_type = db.Column(db.String(50))
    consent_status = db.Column(db.String(20), default='pending')
    signed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ConsentRecord {self.consent_type}>'


class FamilyElderlyLink(db.Model):
    __tablename__ = 'family_elderly_links'

    id = db.Column(db.Integer, primary_key=True)
    family_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    elderly_profile_id = db.Column(db.Integer, db.ForeignKey('elderly_profiles.id'), nullable=False)
    relationship = db.Column(db.String(50))
    linked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FamilyElderlyLink family={self.family_user_id} elderly={self.elderly_profile_id}>'


class AccessLog(db.Model):
    __tablename__ = 'access_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(80))
    ip_address = db.Column(db.String(60))
    accessed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AccessLog {self.action}>'


class UserSetting(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    notification_enabled = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(20), default='en')
    theme = db.Column(db.String(20), default='light')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserSetting user={self.user_id}>'