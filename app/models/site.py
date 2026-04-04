from app.extensions import db

class SiteSetting(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f'<SiteSetting {self.key}>'