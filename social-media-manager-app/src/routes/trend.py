from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Trend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(50), nullable=False)  # twitter, instagram, tiktok, etc.
    engagement_score = db.Column(db.Float, default=0.0)
    volume = db.Column(db.Integer, default=0)
    growth_rate = db.Column(db.Float, default=0.0)
    sentiment = db.Column(db.String(20), default='neutral')  # positive, negative, neutral
    category = db.Column(db.String(100))
    hashtags = db.Column(db.Text)  # JSON string of related hashtags
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Trend {self.keyword} on {self.platform}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'platform': self.platform,
            'engagement_score': self.engagement_score,
            'volume': self.volume,
            'growth_rate': self.growth_rate,
            'sentiment': self.sentiment,
            'category': self.category,
            'hashtags': self.hashtags,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ContentRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trend_id = db.Column(db.Integer, db.ForeignKey('trend.id'), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # post, story, reel, video
    recommended_time = db.Column(db.DateTime)
    confidence_score = db.Column(db.Float, default=0.0)
    hashtag_suggestions = db.Column(db.Text)  # JSON string
    content_suggestions = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('recommendations', lazy=True))
    trend = db.relationship('Trend', backref=db.backref('recommendations', lazy=True))
    
    def __repr__(self):
        return f'<ContentRecommendation for User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'trend_id': self.trend_id,
            'content_type': self.content_type,
            'recommended_time': self.recommended_time.isoformat() if self.recommended_time else None,
            'confidence_score': self.confidence_score,
            'hashtag_suggestions': self.hashtag_suggestions,
            'content_suggestions': self.content_suggestions,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'trend': self.trend.to_dict() if self.trend else None
        }

class CharacterProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    tone = db.Column(db.String(50))  # professional, casual, humorous, etc.
    target_audience = db.Column(db.String(200))
    content_style = db.Column(db.String(100))
    preferred_platforms = db.Column(db.Text)  # JSON string of platforms
    keywords = db.Column(db.Text)  # JSON string of relevant keywords
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('character_profiles', lazy=True))
    
    def __repr__(self):
        return f'<CharacterProfile {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'tone': self.tone,
            'target_audience': self.target_audience,
            'content_style': self.content_style,
            'preferred_platforms': self.preferred_platforms,
            'keywords': self.keywords,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

