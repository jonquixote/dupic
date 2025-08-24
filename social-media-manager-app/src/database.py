"""
Database Module for Social Media Analytics
Handles storage and retrieval of trends, transcripts, visuals, and ML analysis results
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import numpy as np

class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class Platform(Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"

@dataclass
class TrendingContent:
    id: str
    platform: Platform
    content_type: ContentType
    title: str
    description: str
    url: str
    engagement_score: float
    view_count: int
    like_count: int
    share_count: int
    comment_count: int
    hashtags: List[str]
    mentions: List[str]
    created_at: datetime
    analyzed_at: datetime
    ai_analysis: Dict[str, Any]
    sentiment_score: float
    topics: List[str]
    visual_features: Dict[str, Any] = None
    audio_transcript: str = None

@dataclass
class UserContent:
    id: str
    user_id: str
    platform: Platform
    content_type: ContentType
    title: str
    description: str
    url: str
    performance_metrics: Dict[str, Any]
    created_at: datetime
    analyzed_at: datetime
    ai_suggestions: List[str]
    optimization_score: float

@dataclass
class MLAnalysis:
    id: str
    content_id: str
    analysis_type: str  # "trend_prediction", "sentiment_analysis", "content_optimization"
    model_used: str
    confidence_score: float
    results: Dict[str, Any]
    created_at: datetime

class DatabaseManager:
    """Manages database operations for social media analytics"""
    
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string or os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client.social_media_analytics
            
            # Create indexes for better performance
            self._create_indexes()
            print("Connected to MongoDB successfully")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            # Fallback to in-memory storage for development
            self._setup_fallback_storage()
    
    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        collections = {
            'trending_content': [
                ('platform', 1),
                ('content_type', 1),
                ('engagement_score', -1),
                ('created_at', -1),
                ('hashtags', 1),
                ('topics', 1)
            ],
            'user_content': [
                ('user_id', 1),
                ('platform', 1),
                ('created_at', -1),
                ('optimization_score', -1)
            ],
            'ml_analysis': [
                ('content_id', 1),
                ('analysis_type', 1),
                ('created_at', -1),
                ('confidence_score', -1)
            ]
        }
        
        for collection_name, indexes in collections.items():
            collection = self.db[collection_name]
            for index in indexes:
                collection.create_index([index])
    
    def _setup_fallback_storage(self):
        """Setup in-memory storage as fallback"""
        self.fallback_storage = {
            'trending_content': [],
            'user_content': [],
            'ml_analysis': []
        }
        print("Using fallback in-memory storage")
    
    def store_trending_content(self, content: TrendingContent) -> str:
        """Store trending content data"""
        try:
            if self.db:
                content_dict = asdict(content)
                content_dict['_id'] = content.id
                content_dict['platform'] = content.platform.value
                content_dict['content_type'] = content.content_type.value
                
                result = self.db.trending_content.insert_one(content_dict)
                return str(result.inserted_id)
            else:
                # Fallback storage
                self.fallback_storage['trending_content'].append(asdict(content))
                return content.id
        except Exception as e:
            print(f"Error storing trending content: {e}")
            return None
    
    def get_trending_content(self, platform: Platform = None, 
                           content_type: ContentType = None,
                           limit: int = 50, 
                           hours_back: int = 24) -> List[TrendingContent]:
        """Retrieve trending content with filters"""
        try:
            if self.db:
                query = {}
                if platform:
                    query['platform'] = platform.value
                if content_type:
                    query['content_type'] = content_type.value
                
                # Filter by time
                time_threshold = datetime.utcnow() - timedelta(hours=hours_back)
                query['created_at'] = {'$gte': time_threshold}
                
                cursor = self.db.trending_content.find(query).sort('engagement_score', -1).limit(limit)
                
                results = []
                for doc in cursor:
                    doc['platform'] = Platform(doc['platform'])
                    doc['content_type'] = ContentType(doc['content_type'])
                    results.append(TrendingContent(**doc))
                
                return results
            else:
                # Fallback storage
                return [TrendingContent(**item) for item in self.fallback_storage['trending_content'][:limit]]
        except Exception as e:
            print(f"Error retrieving trending content: {e}")
            return []
    
    def store_user_content(self, content: UserContent) -> str:
        """Store user content data"""
        try:
            if self.db:
                content_dict = asdict(content)
                content_dict['_id'] = content.id
                content_dict['platform'] = content.platform.value
                content_dict['content_type'] = content.content_type.value
                
                result = self.db.user_content.insert_one(content_dict)
                return str(result.inserted_id)
            else:
                # Fallback storage
                self.fallback_storage['user_content'].append(asdict(content))
                return content.id
        except Exception as e:
            print(f"Error storing user content: {e}")
            return None
    
    def get_user_content(self, user_id: str, platform: Platform = None, 
                        limit: int = 50) -> List[UserContent]:
        """Retrieve user content"""
        try:
            if self.db:
                query = {'user_id': user_id}
                if platform:
                    query['platform'] = platform.value
                
                cursor = self.db.user_content.find(query).sort('created_at', -1).limit(limit)
                
                results = []
                for doc in cursor:
                    doc['platform'] = Platform(doc['platform'])
                    doc['content_type'] = ContentType(doc['content_type'])
                    results.append(UserContent(**doc))
                
                return results
            else:
                # Fallback storage
                user_content = [item for item in self.fallback_storage['user_content'] 
                              if item['user_id'] == user_id]
                return [UserContent(**item) for item in user_content[:limit]]
        except Exception as e:
            print(f"Error retrieving user content: {e}")
            return []
    
    def store_ml_analysis(self, analysis: MLAnalysis) -> str:
        """Store ML analysis results"""
        try:
            if self.db:
                analysis_dict = asdict(analysis)
                analysis_dict['_id'] = analysis.id
                
                result = self.db.ml_analysis.insert_one(analysis_dict)
                return str(result.inserted_id)
            else:
                # Fallback storage
                self.fallback_storage['ml_analysis'].append(asdict(analysis))
                return analysis.id
        except Exception as e:
            print(f"Error storing ML analysis: {e}")
            return None
    
    def get_ml_analysis(self, content_id: str = None, 
                       analysis_type: str = None,
                       limit: int = 50) -> List[MLAnalysis]:
        """Retrieve ML analysis results"""
        try:
            if self.db:
                query = {}
                if content_id:
                    query['content_id'] = content_id
                if analysis_type:
                    query['analysis_type'] = analysis_type
                
                cursor = self.db.ml_analysis.find(query).sort('created_at', -1).limit(limit)
                
                results = []
                for doc in cursor:
                    results.append(MLAnalysis(**doc))
                
                return results
            else:
                # Fallback storage
                filtered_analysis = self.fallback_storage['ml_analysis']
                if content_id:
                    filtered_analysis = [item for item in filtered_analysis 
                                       if item['content_id'] == content_id]
                if analysis_type:
                    filtered_analysis = [item for item in filtered_analysis 
                                       if item['analysis_type'] == analysis_type]
                
                return [MLAnalysis(**item) for item in filtered_analysis[:limit]]
        except Exception as e:
            print(f"Error retrieving ML analysis: {e}")
            return []
    
    def get_trending_hashtags(self, platform: Platform = None, 
                            hours_back: int = 24, limit: int = 20) -> List[Dict[str, Any]]:
        """Get trending hashtags with engagement metrics"""
        try:
            if self.db:
                pipeline = []
                
                # Match stage
                match_stage = {}
                if platform:
                    match_stage['platform'] = platform.value
                
                time_threshold = datetime.utcnow() - timedelta(hours=hours_back)
                match_stage['created_at'] = {'$gte': time_threshold}
                
                if match_stage:
                    pipeline.append({'$match': match_stage})
                
                # Unwind hashtags
                pipeline.extend([
                    {'$unwind': '$hashtags'},
                    {'$group': {
                        '_id': '$hashtags',
                        'count': {'$sum': 1},
                        'avg_engagement': {'$avg': '$engagement_score'},
                        'total_views': {'$sum': '$view_count'},
                        'total_likes': {'$sum': '$like_count'}
                    }},
                    {'$sort': {'avg_engagement': -1}},
                    {'$limit': limit}
                ])
                
                results = list(self.db.trending_content.aggregate(pipeline))
                return [{'hashtag': item['_id'], **{k: v for k, v in item.items() if k != '_id'}} 
                       for item in results]
            else:
                # Fallback: simple hashtag counting
                hashtag_counts = {}
                for content in self.fallback_storage['trending_content']:
                    for hashtag in content.get('hashtags', []):
                        if hashtag not in hashtag_counts:
                            hashtag_counts[hashtag] = {'count': 0, 'avg_engagement': 0}
                        hashtag_counts[hashtag]['count'] += 1
                        hashtag_counts[hashtag]['avg_engagement'] += content.get('engagement_score', 0)
                
                # Calculate averages and sort
                for hashtag in hashtag_counts:
                    hashtag_counts[hashtag]['avg_engagement'] /= hashtag_counts[hashtag]['count']
                
                sorted_hashtags = sorted(hashtag_counts.items(), 
                                       key=lambda x: x[1]['avg_engagement'], reverse=True)
                
                return [{'hashtag': hashtag, **data} for hashtag, data in sorted_hashtags[:limit]]
        except Exception as e:
            print(f"Error getting trending hashtags: {e}")
            return []
    
    def get_analytics_summary(self, user_id: str = None, 
                            hours_back: int = 24) -> Dict[str, Any]:
        """Get analytics summary"""
        try:
            summary = {
                'total_trending_content': 0,
                'total_user_content': 0,
                'total_ml_analyses': 0,
                'avg_engagement_score': 0,
                'top_platforms': [],
                'content_type_distribution': {},
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
            }
            
            if self.db:
                # Get trending content stats
                time_threshold = datetime.utcnow() - timedelta(hours=hours_back)
                trending_count = self.db.trending_content.count_documents({
                    'created_at': {'$gte': time_threshold}
                })
                summary['total_trending_content'] = trending_count
                
                # Get average engagement
                pipeline = [
                    {'$match': {'created_at': {'$gte': time_threshold}}},
                    {'$group': {'_id': None, 'avg_engagement': {'$avg': '$engagement_score'}}}
                ]
                avg_result = list(self.db.trending_content.aggregate(pipeline))
                if avg_result:
                    summary['avg_engagement_score'] = avg_result[0]['avg_engagement']
                
                # Get platform distribution
                platform_pipeline = [
                    {'$match': {'created_at': {'$gte': time_threshold}}},
                    {'$group': {'_id': '$platform', 'count': {'$sum': 1}}},
                    {'$sort': {'count': -1}},
                    {'$limit': 5}
                ]
                platform_results = list(self.db.trending_content.aggregate(platform_pipeline))
                summary['top_platforms'] = [{'platform': item['_id'], 'count': item['count']} 
                                          for item in platform_results]
                
                # User content stats
                if user_id:
                    user_content_count = self.db.user_content.count_documents({'user_id': user_id})
                    summary['total_user_content'] = user_content_count
                
                # ML analysis stats
                ml_analysis_count = self.db.ml_analysis.count_documents({
                    'created_at': {'$gte': time_threshold}
                })
                summary['total_ml_analyses'] = ml_analysis_count
                
            else:
                # Fallback calculations
                summary['total_trending_content'] = len(self.fallback_storage['trending_content'])
                summary['total_user_content'] = len(self.fallback_storage['user_content'])
                summary['total_ml_analyses'] = len(self.fallback_storage['ml_analysis'])
            
            return summary
        except Exception as e:
            print(f"Error getting analytics summary: {e}")
            return {}
    
    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()

# Global instance
db_manager = DatabaseManager()

