from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .api_key import ApiKey
from .ai_provider import AIProviderConfig
from .character import CharacterProfile
from .trend import Trend, ContentRecommendation, VideoAnalysis, UserAnalytics, FavoriteContent