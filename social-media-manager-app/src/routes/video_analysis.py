from flask import Blueprint, jsonify, request
from src.models import db, VideoAnalysis
from src.services.content_analysis_service import ContentAnalysisService

video_analysis_bp = Blueprint("video_analysis", __name__)
analysis_service = ContentAnalysisService()

@video_analysis_bp.route("/analyze_video", methods=["POST"])
def analyze_video():
    data = request.json
    user_id = data.get("user_id")
    video_url = data.get("video_url")
    post_id = data.get("post_id")

    if not all([user_id, video_url]):
        return jsonify({"error": "Missing required fields: user_id, video_url"}), 400

    result = analysis_service.analyze_video_url(user_id, video_url, post_id)
    
    if result.get("success"):
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@video_analysis_bp.route("/analyze_video/<int:post_id>", methods=["GET"])
def get_video_analysis(post_id):
    analysis = VideoAnalysis.query.filter_by(post_id=post_id).first_or_404()
    return jsonify({
        "id": analysis.id,
        "post_id": analysis.post_id,
        "video_url": analysis.video_url,
        "transcription_text": analysis.transcription_text,
        "visual_description": analysis.visual_description,
        "analysis_date": analysis.analysis_date.isoformat(),
        "provider_config_id": analysis.provider_config_id
    }), 200

@video_analysis_bp.route("/analyze_trending", methods=["POST"])
def analyze_trending_content():
    data = request.json
    user_id = data.get("user_id")
    trending_items = data.get("trending_items", [])

    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    result = analysis_service.analyze_trending_content(user_id, trending_items)
    return jsonify(result), 200

@video_analysis_bp.route("/content_insights", methods=["POST"])
def get_content_insights():
    data = request.json
    user_id = data.get("user_id")
    content_text = data.get("content_text")

    if not all([user_id, content_text]):
        return jsonify({"error": "Missing required fields: user_id, content_text"}), 400

    result = analysis_service.get_content_insights(user_id, content_text)
    return jsonify(result), 200

@video_analysis_bp.route("/content_variations", methods=["POST"])
def generate_content_variations():
    data = request.json
    user_id = data.get("user_id")
    original_content = data.get("original_content")
    character_profile = data.get("character_profile", {})
    count = data.get("count", 3)

    if not all([user_id, original_content]):
        return jsonify({"error": "Missing required fields: user_id, original_content"}), 400

    result = analysis_service.generate_content_variations(user_id, original_content, character_profile, count)
    return jsonify(result), 200

@video_analysis_bp.route("/optimal_posting_time", methods=["POST"])
def get_optimal_posting_time():
    data = request.json
    user_id = data.get("user_id")
    platform = data.get("platform")
    content_type = data.get("content_type", "text")

    if not all([user_id, platform]):
        return jsonify({"error": "Missing required fields: user_id, platform"}), 400

    result = analysis_service.suggest_optimal_posting_time(user_id, platform, content_type)
    return jsonify(result), 200
