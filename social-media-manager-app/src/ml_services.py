"""
ML Services Module
Provides machine learning capabilities for trend analysis, sentiment analysis,
content optimization, and predictive analytics
"""

import os
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import uuid

# ML Libraries
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Optional imports
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("OpenCV not available, visual analysis will be limited")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL not available, image processing will be limited")

try:
    import torch
    from transformers import pipeline, AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available, using fallback NLP models")

from .database import db_manager, TrendingContent, MLAnalysis, Platform, ContentType

@dataclass
class TrendPrediction:
    hashtag: str
    platform: Platform
    predicted_engagement: float
    confidence_score: float
    trend_direction: str  # "rising", "stable", "declining"
    time_to_peak: int  # hours
    recommended_actions: List[str]

@dataclass
class ContentOptimization:
    content_id: str
    current_score: float
    optimized_score: float
    improvements: List[Dict[str, Any]]
    recommended_hashtags: List[str]
    best_posting_time: str
    target_audience: Dict[str, Any]

class MLServicesManager:
    """Manages all ML services for social media analytics"""
    
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.scalers = {}
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models and pipelines"""
        try:
            if TRANSFORMERS_AVAILABLE:
                # Use simpler models that work with current PyTorch version
                print("Using fallback models due to PyTorch version compatibility")
                self._setup_fallback_models()
            else:
                print("Using fallback ML models due to missing dependencies")
                self._setup_fallback_models()
                
        except Exception as e:
            print(f"Error initializing ML models: {e}")
            self._setup_fallback_models()
    
    def _setup_fallback_models(self):
        """Setup fallback models if main models fail to load"""
        print("Setting up fallback ML models")
        self.models = {
            'sentiment': None,
            'text_classifier': None,
            'feature_extractor': None
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text content"""
        try:
            if self.models['sentiment']:
                results = self.models['sentiment'](text)
                
                # Convert to standardized format
                sentiment_scores = {}
                for result in results[0]:
                    label = result['label'].lower()
                    if 'positive' in label:
                        sentiment_scores['positive'] = result['score']
                    elif 'negative' in label:
                        sentiment_scores['negative'] = result['score']
                    else:
                        sentiment_scores['neutral'] = result['score']
                
                # Determine overall sentiment
                max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
                
                return {
                    'overall_sentiment': max_sentiment[0],
                    'confidence': max_sentiment[1],
                    'scores': sentiment_scores,
                    'analysis_timestamp': datetime.utcnow().isoformat()
                }
            else:
                # Fallback: simple keyword-based sentiment
                positive_words = ['good', 'great', 'amazing', 'awesome', 'love', 'excellent']
                negative_words = ['bad', 'terrible', 'awful', 'hate', 'horrible', 'worst']
                
                text_lower = text.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    sentiment = 'positive'
                    confidence = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
                elif negative_count > positive_count:
                    sentiment = 'negative'
                    confidence = min(0.8, 0.5 + (negative_count - positive_count) * 0.1)
                else:
                    sentiment = 'neutral'
                    confidence = 0.6
                
                return {
                    'overall_sentiment': sentiment,
                    'confidence': confidence,
                    'scores': {sentiment: confidence},
                    'analysis_timestamp': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'scores': {'neutral': 0.5},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def extract_topics(self, texts: List[str], num_topics: int = 5) -> List[Dict[str, Any]]:
        """Extract topics from a collection of texts using clustering"""
        try:
            if not texts:
                return []
            
            # Vectorize texts
            tfidf_matrix = self.vectorizers['tfidf'].fit_transform(texts)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=min(num_topics, len(texts)), random_state=42)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)
            
            # Extract top terms for each cluster
            feature_names = self.vectorizers['tfidf'].get_feature_names_out()
            topics = []
            
            for i in range(kmeans.n_clusters):
                # Get top terms for this cluster
                cluster_center = kmeans.cluster_centers_[i]
                top_indices = cluster_center.argsort()[-10:][::-1]
                top_terms = [feature_names[idx] for idx in top_indices]
                
                # Count documents in this cluster
                doc_count = np.sum(cluster_labels == i)
                
                topics.append({
                    'topic_id': i,
                    'top_terms': top_terms,
                    'document_count': int(doc_count),
                    'weight': float(doc_count / len(texts))
                })
            
            return sorted(topics, key=lambda x: x['weight'], reverse=True)
            
        except Exception as e:
            print(f"Error in topic extraction: {e}")
            return []
    
    def predict_engagement(self, content_features: Dict[str, Any], 
                          historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict engagement for content based on features and historical data"""
        try:
            if not historical_data:
                return {
                    'predicted_engagement': 0.5,
                    'confidence': 0.3,
                    'factors': ['insufficient_data']
                }
            
            # Prepare training data
            df = pd.DataFrame(historical_data)
            
            # Feature engineering
            features = []
            targets = []
            
            for _, row in df.iterrows():
                feature_vector = [
                    len(row.get('hashtags', [])),
                    len(row.get('description', '')),
                    row.get('sentiment_score', 0.5),
                    len(row.get('mentions', [])),
                    row.get('hour_of_day', 12),
                    row.get('day_of_week', 3)
                ]
                features.append(feature_vector)
                targets.append(row.get('engagement_score', 0))
            
            if len(features) < 5:  # Need minimum data for training
                return {
                    'predicted_engagement': np.mean(targets) if targets else 0.5,
                    'confidence': 0.4,
                    'factors': ['limited_data']
                }
            
            # Train model
            X = np.array(features)
            y = np.array(targets)
            
            # Scale features
            X_scaled = self.scalers['standard'].fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            confidence = max(0.3, min(0.9, r2))
            
            # Prepare current content features
            current_features = [
                len(content_features.get('hashtags', [])),
                len(content_features.get('description', '')),
                content_features.get('sentiment_score', 0.5),
                len(content_features.get('mentions', [])),
                content_features.get('hour_of_day', 12),
                content_features.get('day_of_week', 3)
            ]
            
            current_features_scaled = self.scalers['standard'].transform([current_features])
            predicted_engagement = model.predict(current_features_scaled)[0]
            
            # Get feature importance
            feature_names = ['hashtags_count', 'description_length', 'sentiment_score',
                           'mentions_count', 'hour_of_day', 'day_of_week']
            importance_scores = model.feature_importances_
            
            important_factors = [
                feature_names[i] for i in np.argsort(importance_scores)[-3:][::-1]
            ]
            
            return {
                'predicted_engagement': float(max(0, min(1, predicted_engagement))),
                'confidence': float(confidence),
                'factors': important_factors,
                'model_performance': {
                    'r2_score': float(r2),
                    'training_samples': len(X_train)
                }
            }
            
        except Exception as e:
            print(f"Error in engagement prediction: {e}")
            return {
                'predicted_engagement': 0.5,
                'confidence': 0.3,
                'factors': ['prediction_error']
            }
    
    def analyze_visual_content(self, image_path: str) -> Dict[str, Any]:
        """Analyze visual content using computer vision"""
        try:
            if not CV2_AVAILABLE:
                return {
                    'error': 'OpenCV not available',
                    'message': 'Visual analysis requires opencv-python package'
                }
            
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return {'error': 'Could not load image'}
            
            # Basic image analysis
            height, width, channels = image.shape
            
            # Color analysis
            mean_color = np.mean(image, axis=(0, 1))
            dominant_color = mean_color.astype(int).tolist()
            
            # Brightness analysis
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            # Contrast analysis
            contrast = np.std(gray)
            
            # Edge detection for complexity
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            
            # Color distribution
            hist_b = cv2.calcHist([image], [0], None, [256], [0, 256])
            hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
            hist_r = cv2.calcHist([image], [2], None, [256], [0, 256])
            
            color_variance = {
                'blue': float(np.var(hist_b)),
                'green': float(np.var(hist_g)),
                'red': float(np.var(hist_r))
            }
            
            return {
                'dimensions': {'width': width, 'height': height},
                'dominant_color': dominant_color,
                'brightness': float(brightness),
                'contrast': float(contrast),
                'edge_density': float(edge_density),
                'color_variance': color_variance,
                'aspect_ratio': float(width / height),
                'complexity_score': float(edge_density * contrast / 1000),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"Error in visual content analysis: {e}")
            return {'error': str(e)}
    
    def generate_content_recommendations(self, user_id: str, 
                                       platform: Platform) -> List[Dict[str, Any]]:
        """Generate personalized content recommendations"""
        try:
            # Get user's historical content
            user_content = db_manager.get_user_content(user_id, platform)
            
            # Get trending content for the platform
            trending_content = db_manager.get_trending_content(platform, limit=100)
            
            if not trending_content:
                return []
            
            # Analyze user's successful content
            user_successful_content = [
                content for content in user_content 
                if content.optimization_score > 0.7
            ]
            
            recommendations = []
            
            # Extract patterns from successful content
            if user_successful_content:
                successful_hashtags = []
                successful_topics = []
                
                for content in user_successful_content:
                    # Extract hashtags and topics from successful content
                    # This would be enhanced with actual content analysis
                    pass
            
            # Generate recommendations based on trending content
            for trend in trending_content[:10]:
                # Calculate relevance score
                relevance_score = self._calculate_content_relevance(
                    trend, user_successful_content
                )
                
                if relevance_score > 0.5:
                    recommendation = {
                        'content_id': trend.id,
                        'title': trend.title,
                        'platform': trend.platform.value,
                        'engagement_score': trend.engagement_score,
                        'relevance_score': relevance_score,
                        'hashtags': trend.hashtags[:5],
                        'topics': trend.topics[:3],
                        'recommended_action': self._generate_action_recommendation(trend),
                        'estimated_performance': self._estimate_performance(
                            trend, user_successful_content
                        )
                    }
                    recommendations.append(recommendation)
            
            # Sort by relevance and estimated performance
            recommendations.sort(
                key=lambda x: x['relevance_score'] * x['estimated_performance'],
                reverse=True
            )
            
            return recommendations[:5]
            
        except Exception as e:
            print(f"Error generating content recommendations: {e}")
            return []
    
    def _calculate_content_relevance(self, trending_content: TrendingContent,
                                   user_content: List) -> float:
        """Calculate relevance score between trending content and user's content"""
        try:
            if not user_content:
                return 0.6  # Default relevance for new users
            
            # Simple relevance calculation based on hashtags and topics
            user_hashtags = set()
            user_topics = set()
            
            for content in user_content:
                # This would be enhanced with actual hashtag/topic extraction
                pass
            
            # Calculate hashtag overlap
            trending_hashtags = set(trending_content.hashtags)
            hashtag_overlap = len(trending_hashtags.intersection(user_hashtags))
            hashtag_score = hashtag_overlap / max(len(trending_hashtags), 1)
            
            # Calculate topic overlap
            trending_topics = set(trending_content.topics)
            topic_overlap = len(trending_topics.intersection(user_topics))
            topic_score = topic_overlap / max(len(trending_topics), 1)
            
            # Combine scores
            relevance_score = (hashtag_score * 0.4 + topic_score * 0.6)
            
            return min(1.0, max(0.1, relevance_score))
            
        except Exception as e:
            print(f"Error calculating content relevance: {e}")
            return 0.5
    
    def _generate_action_recommendation(self, trending_content: TrendingContent) -> str:
        """Generate action recommendation based on trending content"""
        actions = [
            "Create similar content with your unique perspective",
            "Join the conversation with relevant hashtags",
            "Share your opinion on this trending topic",
            "Create a response or reaction video",
            "Adapt this trend to your niche"
        ]
        
        # Simple selection based on content type
        if trending_content.content_type == ContentType.VIDEO:
            return "Create a response or reaction video"
        elif trending_content.engagement_score > 0.8:
            return "Join the conversation with relevant hashtags"
        else:
            return "Create similar content with your unique perspective"
    
    def _estimate_performance(self, trending_content: TrendingContent,
                            user_content: List) -> float:
        """Estimate performance if user creates similar content"""
        try:
            if not user_content:
                return 0.6  # Default estimate for new users
            
            # Calculate average performance of user's content
            avg_user_performance = np.mean([
                content.optimization_score for content in user_content
            ])
            
            # Adjust based on trending content engagement
            trend_factor = min(1.2, trending_content.engagement_score)
            
            estimated_performance = avg_user_performance * trend_factor
            
            return min(1.0, max(0.1, estimated_performance))
            
        except Exception as e:
            print(f"Error estimating performance: {e}")
            return 0.5
    
    def analyze_optimal_posting_times(self, user_id: str, 
                                    platform: Platform) -> Dict[str, Any]:
        """Analyze optimal posting times based on historical data"""
        try:
            # Get user's content and trending content
            user_content = db_manager.get_user_content(user_id, platform)
            trending_content = db_manager.get_trending_content(platform, hours_back=168)  # 1 week
            
            # Analyze posting times vs engagement
            hourly_engagement = {}
            daily_engagement = {}
            
            all_content = user_content + trending_content
            
            for content in all_content:
                hour = content.created_at.hour
                day = content.created_at.weekday()
                
                if hour not in hourly_engagement:
                    hourly_engagement[hour] = []
                if day not in daily_engagement:
                    daily_engagement[day] = []
                
                engagement = getattr(content, 'engagement_score', 
                                   getattr(content, 'optimization_score', 0.5))
                
                hourly_engagement[hour].append(engagement)
                daily_engagement[day].append(engagement)
            
            # Calculate average engagement by hour and day
            best_hours = []
            for hour, engagements in hourly_engagement.items():
                avg_engagement = np.mean(engagements)
                best_hours.append({
                    'hour': hour,
                    'avg_engagement': avg_engagement,
                    'sample_size': len(engagements)
                })
            
            best_days = []
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
            for day, engagements in daily_engagement.items():
                avg_engagement = np.mean(engagements)
                best_days.append({
                    'day': day_names[day],
                    'day_number': day,
                    'avg_engagement': avg_engagement,
                    'sample_size': len(engagements)
                })
            
            # Sort by engagement
            best_hours.sort(key=lambda x: x['avg_engagement'], reverse=True)
            best_days.sort(key=lambda x: x['avg_engagement'], reverse=True)
            
            return {
                'best_hours': best_hours[:5],
                'best_days': best_days[:3],
                'recommended_posting_time': {
                    'hour': best_hours[0]['hour'] if best_hours else 12,
                    'day': best_days[0]['day'] if best_days else 'Tuesday'
                },
                'analysis_period': '7 days',
                'total_samples': len(all_content)
            }
            
        except Exception as e:
            print(f"Error analyzing optimal posting times: {e}")
            return {
                'best_hours': [{'hour': 12, 'avg_engagement': 0.6}],
                'best_days': [{'day': 'Tuesday', 'avg_engagement': 0.6}],
                'recommended_posting_time': {'hour': 12, 'day': 'Tuesday'}
            }

# Global instance
ml_services = MLServicesManager()

