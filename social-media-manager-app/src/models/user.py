from datetime import datetime
from src.models import db


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    character_profiles = db.relationship('CharacterProfile', backref='user', lazy=True, cascade='all, delete-orphan')
    ai_configs = db.relationship('AIProviderConfig', backref='user', lazy=True, cascade='all, delete-orphan')
    video_analyses = db.relationship('VideoAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    user_analytics = db.relationship('UserAnalytics', backref='user', lazy=True, cascade='all, delete-orphan')
    favorite_content = db.relationship('FavoriteContent', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
