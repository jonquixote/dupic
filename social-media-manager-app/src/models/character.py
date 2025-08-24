from src.models import db
from datetime import datetime
import json

class CharacterProfile(db.Model):
    __tablename__ = 'character_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    tone = db.Column(db.String(50))
    target_audience = db.Column(db.String(100))
    content_style = db.Column(db.String(100))
    preferred_platforms = db.Column(db.Text)  # Stored as JSON string
    keywords = db.Column(db.Text)  # Stored as JSON string
    dialogue_style = db.Column(db.Text)
    visual_wardrobe = db.Column(db.Text)
    visual_props = db.Column(db.Text)
    visual_background = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'tone': self.tone,
            'target_audience': self.target_audience,
            'content_style': self.content_style,
            'preferred_platforms': json.loads(self.preferred_platforms) if self.preferred_platforms else [],
            'keywords': json.loads(self.keywords) if self.keywords else [],
            'dialogue_style': self.dialogue_style,
            'visual_wardrobe': self.visual_wardrobe,
            'visual_props': self.visual_props,
            'visual_background': self.visual_background,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
