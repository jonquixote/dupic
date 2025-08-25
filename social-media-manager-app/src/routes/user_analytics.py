from flask import Blueprint, jsonify, request
from src.models import db, UserAnalytics, User
from datetime import datetime, timedelta
import json

user_analytics_bp = Blueprint('user_analytics', __name__)

@user_analytics_bp.route('/user_analytics', methods=['GET'])
def get_user_analytics():
    """Get user analytics data"""
    user_id = request.args.get('user_id', type=int)
    metric_name = request.args.get('metric_name')
    days = request.args.get('days', default=30, type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Build query
    query = UserAnalytics.query.filter(
        UserAnalytics.user_id == user_id,
        UserAnalytics.timestamp >= start_date,
        UserAnalytics.timestamp <= end_date
    )
    
    if metric_name:
        query = query.filter(UserAnalytics.metric_name == metric_name)
    
    analytics = query.order_by(UserAnalytics.timestamp.desc()).all()
    
    # Format response
    result = []
    for analytic in analytics:
        try:
            value = json.loads(analytic.value)
        except (json.JSONDecodeError, TypeError):
            value = analytic.value
            
        result.append({
            'id': analytic.id,
            'user_id': analytic.user_id,
            'metric_name': analytic.metric_name,
            'value': value,
            'timestamp': analytic.timestamp.isoformat()
        })
    
    return jsonify(result)

@user_analytics_bp.route('/user_analytics/summary', methods=['GET'])
def get_user_analytics_summary():
    """Get a summary of user analytics"""
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get unique metric names for this user
    metrics = db.session.query(UserAnalytics.metric_name).filter(
        UserAnalytics.user_id == user_id
    ).distinct().all()
    
    # Get latest value for each metric
    summary = {}
    for (metric_name,) in metrics:
        latest = UserAnalytics.query.filter(
            UserAnalytics.user_id == user_id,
            UserAnalytics.metric_name == metric_name
        ).order_by(UserAnalytics.timestamp.desc()).first()
        
        if latest:
            try:
                value = json.loads(latest.value)
            except (json.JSONDecodeError, TypeError):
                value = latest.value
                
            summary[metric_name] = {
                'value': value,
                'timestamp': latest.timestamp.isoformat()
            }
    
    return jsonify(summary)

@user_analytics_bp.route('/user_analytics', methods=['POST'])
def create_user_analytic():
    """Create a new user analytic record"""
    data = request.json
    
    required_fields = ['user_id', 'metric_name', 'value']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Convert value to JSON string if it's not already a string
    if isinstance(data['value'], (dict, list)):
        value = json.dumps(data['value'])
    else:
        value = str(data['value'])
    
    analytic = UserAnalytics(
        user_id=data['user_id'],
        metric_name=data['metric_name'],
        value=value
    )
    
    db.session.add(analytic)
    db.session.commit()
    
    return jsonify({
        'id': analytic.id,
        'user_id': analytic.user_id,
        'metric_name': analytic.metric_name,
        'value': json.loads(analytic.value) if analytic.value.startswith('[') or analytic.value.startswith('{') else analytic.value,
        'timestamp': analytic.timestamp.isoformat()
    }), 201