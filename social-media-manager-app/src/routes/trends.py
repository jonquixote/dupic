from flask import Blueprint, jsonify, request
from src.services.trend_analyzer import TrendAnalyzer
from src.models import Trend, db
import json

trends_bp = Blueprint("trends", __name__)
trend_analyzer = TrendAnalyzer()

@trends_bp.route("/trends", methods=["GET"])
def get_trends():
    """Get a list of stored trends, with optional filtering."""
    platform = request.args.get('platform')
    category = request.args.get('category')
    
    query = Trend.query
    if platform:
        query = query.filter_by(platform=platform)
    if category:
        query = query.filter_by(category=category)
        
    trends = query.order_by(Trend.engagement_score.desc()).limit(100).all()
    return jsonify([{
        'id': trend.id,
        'keyword': trend.keyword,
        'platform': trend.platform,
        'engagement_score': trend.engagement_score,
        'volume': trend.volume,
        'growth_rate': trend.growth_rate,
        'sentiment': trend.sentiment,
        'category': trend.category,
        'hashtags': json.loads(trend.hashtags) if trend.hashtags else [],
        'created_at': trend.created_at.isoformat() if trend.created_at else None,
        'updated_at': trend.updated_at.isoformat() if trend.updated_at else None,
    } for trend in trends])

@trends_bp.route("/trends/top", methods=["GET"])
def get_top_trends():
    """Get top trends with optional limit."""
    limit = request.args.get('limit', default=10, type=int)
    platform = request.args.get('platform')
    
    query = Trend.query
    if platform:
        query = query.filter_by(platform=platform)
        
    trends = query.order_by(Trend.engagement_score.desc()).limit(limit).all()
    return jsonify([{
        'id': trend.id,
        'keyword': trend.keyword,
        'platform': trend.platform,
        'engagement_score': trend.engagement_score,
        'volume': trend.volume,
        'growth_rate': trend.growth_rate,
        'sentiment': trend.sentiment,
        'category': trend.category,
        'hashtags': json.loads(trend.hashtags) if trend.hashtags else [],
        'created_at': trend.created_at.isoformat() if trend.created_at else None,
        'updated_at': trend.updated_at.isoformat() if trend.updated_at else None,
    } for trend in trends])

@trends_bp.route("/trends/refresh", methods=["POST"])
def refresh_trends():
    """Trigger a new trend analysis and storage task."""
    new_trends = trend_analyzer.fetch_and_analyze_trends()
    return jsonify({
        "message": "Trend analysis completed.",
        "new_trends_count": len(new_trends)
    })

@trends_bp.route("/trends/analyze", methods=["POST"])
def analyze_trends():
    """Trigger a new trend analysis and storage task."""
    new_trends = trend_analyzer.fetch_and_analyze_trends()
    return jsonify({
        "message": "Trend analysis completed.",
        "new_trends_count": len(new_trends)
    })