from flask import Blueprint, jsonify, request
from src.models import db, FavoriteContent, User
from datetime import datetime

favorite_content_bp = Blueprint('favorite_content', __name__)

@favorite_content_bp.route('/favorite_content', methods=['GET'])
def get_favorite_content():
    """Get user's favorite content"""
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    favorites = FavoriteContent.query.filter(
        FavoriteContent.user_id == user_id
    ).order_by(FavoriteContent.saved_date.desc()).all()
    
    return jsonify([{
        'id': favorite.id,
        'user_id': favorite.user_id,
        'content_id': favorite.content_id,
        'saved_date': favorite.saved_date.isoformat()
    } for favorite in favorites])

@favorite_content_bp.route('/favorite_content', methods=['POST'])
def add_favorite_content():
    """Add content to user's favorites"""
    data = request.json
    
    required_fields = ['user_id', 'content_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if already favorited
    existing = FavoriteContent.query.filter(
        FavoriteContent.user_id == data['user_id'],
        FavoriteContent.content_id == data['content_id']
    ).first()
    
    if existing:
        return jsonify({'message': 'Content already in favorites'}), 200
    
    favorite = FavoriteContent(
        user_id=data['user_id'],
        content_id=data['content_id']
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({
        'id': favorite.id,
        'user_id': favorite.user_id,
        'content_id': favorite.content_id,
        'saved_date': favorite.saved_date.isoformat()
    }), 201

@favorite_content_bp.route('/favorite_content/<int:favorite_id>', methods=['DELETE'])
def remove_favorite_content(favorite_id):
    """Remove content from user's favorites"""
    favorite = FavoriteContent.query.get_or_404(favorite_id)
    db.session.delete(favorite)
    db.session.commit()
    return '', 204

@favorite_content_bp.route('/favorite_content/check', methods=['GET'])
def check_favorite_content():
    """Check if content is in user's favorites"""
    user_id = request.args.get('user_id', type=int)
    content_id = request.args.get('content_id')
    
    if not user_id or not content_id:
        return jsonify({'error': 'user_id and content_id are required'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    favorite = FavoriteContent.query.filter(
        FavoriteContent.user_id == user_id,
        FavoriteContent.content_id == content_id
    ).first()
    
    return jsonify({
        'is_favorite': favorite is not None
    })