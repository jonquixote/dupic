"""
Main Flask Application for AI-Powered Social Media Manager
Provides REST API endpoints for frontend integration
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import asyncio
import threading

# Load environment variables
load_dotenv()

# Import our modules
from src.ai_providers import ai_manager, AIProvider
from src.database import db_manager, TrendingContent, UserContent, MLAnalysis, Platform, ContentType
from src.ml_services import ml_services

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Enable CORS for all routes
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Global variables for demo data
demo_trending_data = []
demo_user_content = []

def initialize_demo_data():
    """Initialize demo data for testing"""
    global demo_trending_data, demo_user_content
    
    # Demo trending content
    demo_trending_data = [
        {
            'id': str(uuid.uuid4()),
            'platform': 'twitter',
            'content_type': 'text',
            'title': 'AI Revolution in 2025',
            'description': 'The latest developments in artificial intelligence are transforming social media',
            'url': 'https://example.com/ai-revolution',
            'engagement_score': 9.2,
            'view_count': 150000,
            'like_count': 12500,
            'share_count': 3200,
            'comment_count': 850,
            'hashtags': ['#AI', '#Technology', '#Innovation', '#Future'],
            'mentions': ['@techguru', '@aiexpert'],
            'created_at': datetime.utcnow() - timedelta(hours=2),
            'analyzed_at': datetime.utcnow(),
            'ai_analysis': {'sentiment': 'positive', 'topics': ['technology', 'innovation']},
            'sentiment_score': 0.85,
            'topics': ['artificial intelligence', 'technology', 'innovation']
        },
        {
            'id': str(uuid.uuid4()),
            'platform': 'instagram',
            'content_type': 'image',
            'title': 'Sustainable Living Tips',
            'description': 'Simple ways to reduce your carbon footprint and live more sustainably',
            'url': 'https://example.com/sustainable-living',
            'engagement_score': 8.7,
            'view_count': 85000,
            'like_count': 7200,
            'share_count': 1800,
            'comment_count': 420,
            'hashtags': ['#Sustainability', '#EcoFriendly', '#GreenLiving', '#Environment'],
            'mentions': ['@ecowarrior', '@greenliving'],
            'created_at': datetime.utcnow() - timedelta(hours=4),
            'analyzed_at': datetime.utcnow(),
            'ai_analysis': {'sentiment': 'positive', 'topics': ['environment', 'lifestyle']},
            'sentiment_score': 0.78,
            'topics': ['sustainability', 'environment', 'lifestyle']
        }
    ]
    
    # Demo user content
    demo_user_content = [
        {
            'id': str(uuid.uuid4()),
            'user_id': 'demo_user',
            'platform': 'twitter',
            'content_type': 'text',
            'title': 'My thoughts on AI',
            'description': 'Sharing my perspective on the future of artificial intelligence',
            'url': 'https://example.com/my-ai-thoughts',
            'performance_metrics': {
                'views': 5000,
                'likes': 250,
                'shares': 45,
                'comments': 32
            },
            'created_at': datetime.utcnow() - timedelta(days=1),
            'analyzed_at': datetime.utcnow(),
            'ai_suggestions': ['Use more trending hashtags', 'Post during peak hours'],
            'optimization_score': 0.72
        }
    ]

# Initialize demo data
initialize_demo_data()

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'AI Social Media Manager API is running',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/providers', methods=['GET'])
def get_providers():
    """Get available AI providers and their status"""
    try:
        providers_status = ai_manager.get_provider_status()
        return jsonify({
            'success': True,
            'providers': providers_status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/providers/<provider>/models', methods=['GET'])
def get_provider_models(provider):
    """Get available models for a specific provider"""
    try:
        provider_enum = AIProvider(provider)
        models = ai_manager.get_models_for_provider(provider_enum)
        
        models_data = []
        for model in models:
            models_data.append({
                'name': model.name,
                'capabilities': model.capabilities,
                'max_tokens': model.max_tokens,
                'cost_per_token': model.cost_per_token
            })
        
        return jsonify({
            'success': True,
            'provider': provider,
            'models': models_data
        })
    except ValueError:
        return jsonify({
            'success': False,
            'error': f'Invalid provider: {provider}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/generate', methods=['POST'])
def generate_content():
    """Generate content using AI providers"""
    try:
        data = request.get_json()
        
        provider = AIProvider(data.get('provider', 'openai'))
        model = data.get('model', 'gpt-3.5-turbo')
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({
                'success': False,
                'error': 'Messages are required'
            }), 400
        
        # Generate content asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            ai_manager.generate_text(provider, model, messages)
        )
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trends', methods=['GET'])
def get_trends():
    """Get trending content"""
    try:
        platform = request.args.get('platform')
        content_type = request.args.get('content_type')
        limit = int(request.args.get('limit', 50))
        hours_back = int(request.args.get('hours_back', 24))
        
        # Convert string parameters to enums if provided
        platform_enum = Platform(platform) if platform else None
        content_type_enum = ContentType(content_type) if content_type else None
        
        # For demo, return demo data
        trends = demo_trending_data[:limit]
        
        # Apply filters
        if platform:
            trends = [t for t in trends if t['platform'] == platform]
        if content_type:
            trends = [t for t in trends if t['content_type'] == content_type]
        
        # Convert datetime objects to ISO strings for JSON serialization
        for trend in trends:
            trend['created_at'] = trend['created_at'].isoformat()
            trend['analyzed_at'] = trend['analyzed_at'].isoformat()
        
        return jsonify({
            'success': True,
            'trends': trends,
            'total': len(trends)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trends/hashtags', methods=['GET'])
def get_trending_hashtags():
    """Get trending hashtags"""
    try:
        platform = request.args.get('platform')
        hours_back = int(request.args.get('hours_back', 24))
        limit = int(request.args.get('limit', 20))
        
        # For demo, return mock hashtag data
        trending_hashtags = [
            {'hashtag': '#AI', 'count': 1250, 'avg_engagement': 8.5, 'total_views': 150000},
            {'hashtag': '#Technology', 'count': 980, 'avg_engagement': 7.8, 'total_views': 120000},
            {'hashtag': '#Innovation', 'count': 750, 'avg_engagement': 7.2, 'total_views': 95000},
            {'hashtag': '#Sustainability', 'count': 650, 'avg_engagement': 8.1, 'total_views': 85000},
            {'hashtag': '#Future', 'count': 580, 'avg_engagement': 6.9, 'total_views': 72000}
        ]
        
        return jsonify({
            'success': True,
            'hashtags': trending_hashtags[:limit]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/content/analyze', methods=['POST'])
def analyze_content():
    """Analyze content using ML services"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text content is required'
            }), 400
        
        # Perform sentiment analysis
        sentiment_result = ml_services.analyze_sentiment(text)
        
        # Extract topics (using single text in a list)
        topics_result = ml_services.extract_topics([text], num_topics=3)
        
        return jsonify({
            'success': True,
            'analysis': {
                'sentiment': sentiment_result,
                'topics': topics_result,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/content/recommendations', methods=['GET'])
def get_content_recommendations():
    """Get personalized content recommendations"""
    try:
        user_id = request.args.get('user_id', 'demo_user')
        platform = request.args.get('platform', 'twitter')
        
        platform_enum = Platform(platform)
        
        recommendations = ml_services.generate_content_recommendations(user_id, platform_enum)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    try:
        user_id = request.args.get('user_id', 'demo_user')
        hours_back = int(request.args.get('hours_back', 24))
        
        # For demo, return mock analytics data
        summary = {
            'total_trending_content': len(demo_trending_data),
            'total_user_content': len(demo_user_content),
            'total_ml_analyses': 15,
            'avg_engagement_score': 8.2,
            'top_platforms': [
                {'platform': 'twitter', 'count': 45},
                {'platform': 'instagram', 'count': 32},
                {'platform': 'tiktok', 'count': 28}
            ],
            'content_type_distribution': {
                'text': 60,
                'image': 25,
                'video': 15
            },
            'sentiment_distribution': {
                'positive': 65,
                'neutral': 25,
                'negative': 10
            }
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/posting-times', methods=['GET'])
def get_optimal_posting_times():
    """Get optimal posting times analysis"""
    try:
        user_id = request.args.get('user_id', 'demo_user')
        platform = request.args.get('platform', 'twitter')
        
        platform_enum = Platform(platform)
        
        posting_times = ml_services.analyze_optimal_posting_times(user_id, platform_enum)
        
        return jsonify({
            'success': True,
            'posting_times': posting_times
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio using AI providers"""
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Audio file is required'
            }), 400
        
        audio_file = request.files['audio']
        provider = request.form.get('provider', 'groq')
        model = request.form.get('model', 'whisper-large-v3')
        
        # Save uploaded file temporarily
        temp_path = f'/tmp/{uuid.uuid4()}.wav'
        audio_file.save(temp_path)
        
        try:
            provider_enum = AIProvider(provider)
            
            # Transcribe audio asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                ai_manager.transcribe_audio(provider_enum, temp_path, model)
            )
            
            return jsonify({
                'success': True,
                'transcription': result
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze image using AI providers"""
    try:
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Image file is required'
            }), 400
        
        image_file = request.files['image']
        provider = request.form.get('provider', 'openai')
        model = request.form.get('model', 'gpt-4o')
        prompt = request.form.get('prompt', 'Describe this image in detail.')
        
        # Save uploaded file temporarily
        temp_path = f'/tmp/{uuid.uuid4()}.jpg'
        image_file.save(temp_path)
        
        try:
            provider_enum = AIProvider(provider)
            
            # Analyze image asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = loop.run_until_complete(
                ai_manager.analyze_image(provider_enum, model, temp_path, prompt)
            )
            
            # Also perform computer vision analysis
            cv_analysis = ml_services.analyze_visual_content(temp_path)
            
            return jsonify({
                'success': True,
                'ai_analysis': result,
                'cv_analysis': cv_analysis
            })
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Comprehensive health check"""
    try:
        health_status = {
            'api': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'providers': ai_manager.get_provider_status(),
            'database': 'connected' if db_manager.client else 'fallback',
            'ml_services': 'initialized'
        }
        
        return jsonify({
            'success': True,
            'health': health_status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

@app.route('/api/trends/visualization/platform-distribution', methods=['GET'])
def get_platform_distribution():
    """Get trend distribution by platform for visualization."""
    try:
        # Get date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # For demo, return mock data
        platform_distribution = [
            {'platform': 'twitter', 'count': 45, 'avg_engagement': 7.2},
            {'platform': 'instagram', 'count': 32, 'avg_engagement': 8.1},
            {'platform': 'tiktok', 'count': 28, 'avg_engagement': 9.5},
            {'platform': 'facebook', 'count': 19, 'avg_engagement': 6.8}
        ]
        
        return jsonify({
            'success': True,
            'data': platform_distribution
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trends/visualization/category-distribution', methods=['GET'])
def get_category_distribution():
    """Get trend distribution by category for visualization."""
    try:
        # Get filters
        platform = request.args.get('platform')
        
        # For demo, return mock data
        category_distribution = [
            {'category': 'technology', 'count': 35, 'avg_engagement': 8.2},
            {'category': 'entertainment', 'count': 28, 'avg_engagement': 7.9},
            {'category': 'lifestyle', 'count': 22, 'avg_engagement': 8.5},
            {'category': 'business', 'count': 18, 'avg_engagement': 7.1},
            {'category': 'sports', 'count': 15, 'avg_engagement': 7.8}
        ]
        
        return jsonify({
            'success': True,
            'data': category_distribution
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trends/visualization/sentiment-distribution', methods=['GET'])
def get_sentiment_distribution():
    """Get trend distribution by sentiment for visualization."""
    try:
        # Get filters
        platform = request.args.get('platform')
        category = request.args.get('category')
        
        # For demo, return mock data
        sentiment_distribution = [
            {'sentiment': 'positive', 'count': 65},
            {'sentiment': 'neutral', 'count': 25},
            {'sentiment': 'negative', 'count': 10}
        ]
        
        return jsonify({
            'success': True,
            'data': sentiment_distribution
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trends/visualization/engagement-over-time', methods=['GET'])
def get_engagement_over_time():
    """Get engagement scores over time for visualization."""
    try:
        # Get filters
        platform = request.args.get('platform')
        category = request.args.get('category')
        days = request.args.get('days', default=30, type=int)
        
        # For demo, return mock data
        # Generate mock data for the last 30 days
        import random
        from datetime import datetime, timedelta
        
        engagement_data = []
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days-i)
            engagement_score = random.uniform(6.0, 9.5)  # Random engagement score between 6.0 and 9.5
            engagement_data.append({
                'date': date.isoformat(),
                'engagement_score': round(engagement_score, 2)
            })
        
        return jsonify({
            'success': True,
            'data': engagement_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting AI Social Media Manager API on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

