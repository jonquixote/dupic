from datetime import datetime
from src.models import db

class Trend(db.Model):
    __tablename__ = 'trend'
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
    __tablename__ = 'content_recommendation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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

class VideoAnalysis(db.Model):
    __tablename__ = 'video_analysis'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    video_url = db.Column(db.String(500), nullable=False)
    transcription_text = db.Column(db.Text)
    visual_description = db.Column(db.Text)
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    provider_config_id = db.Column(db.Integer, db.ForeignKey('ai_provider_configs.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    metric_name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class FavoriteContent(db.Model):
    __tablename__ = 'favorite_content'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_id = db.Column(db.String(255), nullable=False)
    saved_date = db.Column(db.DateTime, default=datetime.utcnow)
