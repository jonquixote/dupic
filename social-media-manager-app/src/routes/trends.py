from flask import Blueprint, jsonify, request
from src.models.trend import Trend, ContentRecommendation, db
from src.services.trend_analyzer import TrendAnalyzer
from datetime import datetime, timedelta
import json

trends_bp = Blueprint('trends', __name__)

@trends_bp.route('/trends', methods=['GET'])
def get_trends():
    """Get trending topics with optional filtering"""
    platform = request.args.get('platform')
    category = request.args.get('category')
    limit = request.args.get('limit', 20, type=int)
    
    query = Trend.query
    
    if platform:
        query = query.filter(Trend.platform == platform)
    if category:
        query = query.filter(Trend.category == category)
    
    trends = query.order_by(Trend.engagement_score.desc()).limit(limit).all()
    return jsonify([trend.to_dict() for trend in trends])

@trends_bp.route('/trends/refresh', methods=['POST'])
def refresh_trends():
    """Manually trigger trend data refresh"""
    try:
        analyzer = TrendAnalyzer()
        new_trends = analyzer.fetch_and_analyze_trends()
        
        return jsonify({
            'message': f'Successfully refreshed {len(new_trends)} trends',
            'trends': [trend.to_dict() for trend in new_trends]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trends_bp.route('/trends/top', methods=['GET'])
def get_top_trends():
    """Get top trending topics across all platforms"""
    limit = request.args.get('limit', 10, type=int)
    
    # Get trends from the last 24 hours
    since = datetime.utcnow() - timedelta(hours=24)
    trends = Trend.query.filter(
        Trend.created_at >= since
    ).order_by(
        Trend.engagement_score.desc()
    ).limit(limit).all()
    
    return jsonify([trend.to_dict() for trend in trends])

@trends_bp.route('/trends/platforms', methods=['GET'])
def get_platform_trends():
    """Get trending topics grouped by platform"""
    platforms = ['twitter', 'instagram', 'tiktok', 'facebook']
    result = {}
    
    for platform in platforms:
        trends = Trend.query.filter(
            Trend.platform == platform
        ).order_by(
            Trend.engagement_score.desc()
        ).limit(5).all()
        
        result[platform] = [trend.to_dict() for trend in trends]
    
    return jsonify(result)

@trends_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get content recommendations for a user"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    recommendations = ContentRecommendation.query.filter(
        ContentRecommendation.user_id == user_id
    ).order_by(
        ContentRecommendation.confidence_score.desc()
    ).limit(10).all()
    
    return jsonify([rec.to_dict() for rec in recommendations])

@trends_bp.route('/recommendations/generate', methods=['POST'])
def generate_recommendations():
    """Generate new content recommendations for a user"""
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    try:
        analyzer = TrendAnalyzer()
        recommendations = analyzer.generate_recommendations(user_id)
        
        return jsonify({
            'message': f'Generated {len(recommendations)} recommendations',
            'recommendations': [rec.to_dict() for rec in recommendations]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@trends_bp.route('/analytics/engagement', methods=['GET'])
def get_engagement_analytics():
    """Get engagement analytics for trends"""
    platform = request.args.get('platform')
    days = request.args.get('days', 7, type=int)
    
    since = datetime.utcnow() - timedelta(days=days)
    
    query = Trend.query.filter(Trend.created_at >= since)
    if platform:
        query = query.filter(Trend.platform == platform)
    
    trends = query.all()
    
    # Calculate analytics
    total_trends = len(trends)
    avg_engagement = sum(t.engagement_score for t in trends) / total_trends if total_trends > 0 else 0
    avg_volume = sum(t.volume for t in trends) / total_trends if total_trends > 0 else 0
    
    # Group by platform
    platform_stats = {}
    for trend in trends:
        if trend.platform not in platform_stats:
            platform_stats[trend.platform] = {
                'count': 0,
                'total_engagement': 0,
                'total_volume': 0
            }
        platform_stats[trend.platform]['count'] += 1
        platform_stats[trend.platform]['total_engagement'] += trend.engagement_score
        platform_stats[trend.platform]['total_volume'] += trend.volume
    
    # Calculate averages for each platform
    for platform, stats in platform_stats.items():
        stats['avg_engagement'] = stats['total_engagement'] / stats['count']
        stats['avg_volume'] = stats['total_volume'] / stats['count']
    
    return jsonify({
        'total_trends': total_trends,
        'avg_engagement': avg_engagement,
        'avg_volume': avg_volume,
        'platform_stats': platform_stats,
        'period_days': days
    })

@trends_bp.route('/search', methods=['GET'])
def search_trends():
    """Search trends by keyword"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400
    
    trends = Trend.query.filter(
        Trend.keyword.contains(query)
    ).order_by(
        Trend.engagement_score.desc()
    ).limit(20).all()
    
    return jsonify([trend.to_dict() for trend in trends])

