from flask import Blueprint, jsonify, request
from src.services.trend_analyzer import TrendAnalyzer
from src.models import Trend, db
import json
from datetime import datetime, timedelta

trends_bp = Blueprint("trends", __name__)
trend_analyzer = TrendAnalyzer()

@trends_bp.route("/trends", methods=["GET"])
def get_trends():
    """Get a list of stored trends, with optional filtering."""
    platform = request.args.get('platform')
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Trend.query
    if platform:
        query = query.filter_by(platform=platform)
    if category:
        query = query.filter_by(category=category)
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Trend.created_at >= start_dt)
        except ValueError:
            pass  # Invalid date format, ignore filter
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Trend.created_at <= end_dt)
        except ValueError:
            pass  # Invalid date format, ignore filter
        
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
    """Get top trends with optional limit and filters."""
    limit = request.args.get('limit', default=10, type=int)
    platform = request.args.get('platform')
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Trend.query
    if platform:
        query = query.filter_by(platform=platform)
    if category:
        query = query.filter_by(category=category)
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Trend.created_at >= start_dt)
        except ValueError:
            pass  # Invalid date format, ignore filter
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Trend.created_at <= end_dt)
        except ValueError:
            pass  # Invalid date format, ignore filter
        
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

@trends_bp.route("/trends/visualization/platform-distribution", methods=["GET"])
def get_platform_distribution():
    """Get trend distribution by platform for visualization."""
    # Get date filters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        Trend.platform,
        db.func.count(Trend.id).label('count'),
        db.func.avg(Trend.engagement_score).label('avg_engagement')
    ).group_by(Trend.platform)
    
    # Apply date filters
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Trend.created_at >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Trend.created_at <= end_dt)
        except ValueError:
            pass
    
    results = query.all()
    
    return jsonify([{
        'platform': result.platform,
        'count': result.count,
        'avg_engagement': float(result.avg_engagement) if result.avg_engagement else 0.0
    } for result in results])

@trends_bp.route("/trends/visualization/category-distribution", methods=["GET"])
def get_category_distribution():
    """Get trend distribution by category for visualization."""
    # Get filters
    platform = request.args.get('platform')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        Trend.category,
        db.func.count(Trend.id).label('count'),
        db.func.avg(Trend.engagement_score).label('avg_engagement')
    ).group_by(Trend.category)
    
    # Apply filters
    if platform:
        query = query.filter(Trend.platform == platform)
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Trend.created_at >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Trend.created_at <= end_dt)
        except ValueError:
            pass
    
    results = query.all()
    
    return jsonify([{
        'category': result.category,
        'count': result.count,
        'avg_engagement': float(result.avg_engagement) if result.avg_engagement else 0.0
    } for result in results])

@trends_bp.route("/trends/visualization/sentiment-distribution", methods=["GET"])
def get_sentiment_distribution():
    """Get trend distribution by sentiment for visualization."""
    # Get filters
    platform = request.args.get('platform')
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        Trend.sentiment,
        db.func.count(Trend.id).label('count')
    ).group_by(Trend.sentiment)
    
    # Apply filters
    if platform:
        query = query.filter(Trend.platform == platform)
    if category:
        query = query.filter(Trend.category == category)
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(Trend.created_at >= start_dt)
        except ValueError:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(Trend.created_at <= end_dt)
        except ValueError:
            pass
    
    results = query.all()
    
    return jsonify([{
        'sentiment': result.sentiment,
        'count': result.count
    } for result in results])

@trends_bp.route("/trends/visualization/engagement-over-time", methods=["GET"])
def get_engagement_over_time():
    """Get engagement scores over time for visualization."""
    # Get filters
    platform = request.args.get('platform')
    category = request.args.get('category')
    days = request.args.get('days', default=30, type=int)
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    query = db.session.query(
        Trend.created_at,
        Trend.engagement_score
    ).filter(Trend.created_at >= start_date)
    
    # Apply filters
    if platform:
        query = query.filter(Trend.platform == platform)
    if category:
        query = query.filter(Trend.category == category)
    
    results = query.order_by(Trend.created_at).all()
    
    return jsonify([{
        'date': result.created_at.isoformat(),
        'engagement_score': result.engagement_score
    } for result in results])