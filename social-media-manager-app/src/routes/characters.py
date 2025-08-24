from flask import Blueprint, jsonify, request
from src.models.character import CharacterProfile
from src.models import db
import json

characters_bp = Blueprint('characters', __name__)

@characters_bp.route('/characters', methods=['GET'])
def get_characters():
    """Get all character profiles for a user"""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    characters = CharacterProfile.query.filter(
        CharacterProfile.user_id == user_id
    ).order_by(CharacterProfile.created_at.desc()).all()
    
    return jsonify([character.to_dict() for character in characters])

@characters_bp.route('/characters', methods=['POST'])
def create_character():
    """Create a new character profile"""
    data = request.json
    
    required_fields = ['user_id', 'name', 'tone']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate platforms and keywords are valid JSON if provided
    preferred_platforms = data.get('preferred_platforms', '[]')
    keywords = data.get('keywords', '[]')
    
    try:
        if isinstance(preferred_platforms, list):
            preferred_platforms = json.dumps(preferred_platforms)
        if isinstance(keywords, list):
            keywords = json.dumps(keywords)
    except (TypeError, ValueError):
        return jsonify({'error': 'preferred_platforms and keywords must be valid JSON arrays'}), 400
    
    character = CharacterProfile(
        user_id=data['user_id'],
        name=data['name'],
        description=data.get('description', ''),
        tone=data['tone'],
        target_audience=data.get('target_audience', ''),
        content_style=data.get('content_style', ''),
        preferred_platforms=preferred_platforms,
        keywords=keywords
    )
    
    db.session.add(character)
    db.session.commit()
    
    return jsonify(character.to_dict()), 201

@characters_bp.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    """Get a specific character profile"""
    character = CharacterProfile.query.get_or_404(character_id)
    return jsonify(character.to_dict())

@characters_bp.route('/characters/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    """Update a character profile"""
    character = CharacterProfile.query.get_or_404(character_id)
    data = request.json
    
    # Update fields if provided
    if 'name' in data:
        character.name = data['name']
    if 'description' in data:
        character.description = data['description']
    if 'tone' in data:
        character.tone = data['tone']
    if 'target_audience' in data:
        character.target_audience = data['target_audience']
    if 'content_style' in data:
        character.content_style = data['content_style']
    
    # Handle JSON fields
    if 'preferred_platforms' in data:
        platforms = data['preferred_platforms']
        if isinstance(platforms, list):
            character.preferred_platforms = json.dumps(platforms)
        else:
            character.preferred_platforms = platforms
    
    if 'keywords' in data:
        keywords = data['keywords']
        if isinstance(keywords, list):
            character.keywords = json.dumps(keywords)
        else:
            character.keywords = keywords
    
    db.session.commit()
    return jsonify(character.to_dict())

@characters_bp.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    """Delete a character profile"""
    character = CharacterProfile.query.get_or_404(character_id)
    db.session.delete(character)
    db.session.commit()
    return '', 204

@characters_bp.route('/characters/templates', methods=['GET'])
def get_character_templates():
    """Get predefined character profile templates"""
    templates = [
        {
            'name': 'Professional Brand',
            'description': 'Corporate and business-focused content creator',
            'tone': 'professional',
            'target_audience': 'Business professionals, entrepreneurs, industry leaders',
            'content_style': 'Informative, authoritative, data-driven',
            'preferred_platforms': ['linkedin', 'twitter'],
            'keywords': ['business', 'leadership', 'strategy', 'innovation', 'growth']
        },
        {
            'name': 'Lifestyle Influencer',
            'description': 'Casual and relatable lifestyle content creator',
            'tone': 'casual',
            'target_audience': 'Young adults, lifestyle enthusiasts, trend followers',
            'content_style': 'Personal, authentic, visually appealing',
            'preferred_platforms': ['instagram', 'tiktok'],
            'keywords': ['lifestyle', 'fashion', 'travel', 'wellness', 'inspiration']
        },
        {
            'name': 'Tech Enthusiast',
            'description': 'Technology and innovation focused creator',
            'tone': 'informative',
            'target_audience': 'Tech professionals, developers, early adopters',
            'content_style': 'Technical, educational, cutting-edge',
            'preferred_platforms': ['twitter', 'linkedin', 'youtube'],
            'keywords': ['technology', 'AI', 'programming', 'innovation', 'startups']
        },
        {
            'name': 'Entertainment Creator',
            'description': 'Fun and engaging entertainment content',
            'tone': 'humorous',
            'target_audience': 'General audience, entertainment seekers, young demographics',
            'content_style': 'Entertaining, viral, trend-focused',
            'preferred_platforms': ['tiktok', 'instagram', 'twitter'],
            'keywords': ['entertainment', 'funny', 'viral', 'trending', 'memes']
        },
        {
            'name': 'Educational Creator',
            'description': 'Knowledge sharing and educational content',
            'tone': 'educational',
            'target_audience': 'Students, lifelong learners, professionals seeking growth',
            'content_style': 'Informative, structured, value-driven',
            'preferred_platforms': ['youtube', 'linkedin', 'twitter'],
            'keywords': ['education', 'learning', 'tips', 'tutorial', 'knowledge']
        }
    ]
    
    return jsonify(templates)
