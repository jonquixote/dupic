from flask import Blueprint, request, jsonify
from src.services.content_generator import ContentGenerator
from src.models import Trend, CharacterProfile

content_generation_bp = Blueprint("content_generation", __name__)
content_generator = ContentGenerator()

@content_generation_bp.route("/content/generate", methods=["POST"])
def generate_content_route():
    """Generate content based on a trend and character profile."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    trend_id = data.get("trend_id")
    character_id = data.get("character_id")
    content_type = data.get("content_type", "post")
    platform = data.get("platform", "twitter")
    additional_context = data.get("additional_context", "")

    if not trend_id or not character_id:
        return jsonify({"error": "trend_id and character_id are required"}), 400

    trend = Trend.query.get(trend_id)
    if not trend:
        return jsonify({"error": f"Trend with id {trend_id} not found"}), 404
    
    character = CharacterProfile.query.get(character_id)
    if not character:
        return jsonify({"error": f"CharacterProfile with id {character_id} not found"}), 404

    result = content_generator.generate_content(
        trend=trend,
        character=character,
        content_type=content_type,
        platform=platform,
        additional_context=additional_context
    )

    return jsonify(result)