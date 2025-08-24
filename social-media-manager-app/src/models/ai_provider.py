from src.models import db
from datetime import datetime

class AIProviderConfig(db.Model):
    __tablename__ = 'ai_provider_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider_name = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(200), nullable=False)
    default_model_text = db.Column(db.String(100))
    default_model_speech_to_text = db.Column(db.String(100))
    default_model_vision_to_text = db.Column(db.String(100))
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'provider_name': self.provider_name,
            'api_key': self.api_key[:10] + '***' if self.api_key else None,  # Mask API key
            'default_model_text': self.default_model_text,
            'default_model_speech_to_text': self.default_model_speech_to_text,
            'default_model_vision_to_text': self.default_model_vision_to_text,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
