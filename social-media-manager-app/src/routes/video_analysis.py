from flask import Blueprint, jsonify, request
from src.models import db, VideoAnalysis
from src.services.video_analyzer import VideoAnalyzer

video_analysis_bp = Blueprint("video_analysis", __name__)
video_analyzer = VideoAnalyzer()

@video_analysis_bp.route("/analyze_video", methods=["POST"])
def analyze_video():
    """Analyze a video from URL including transcription and visual description."""
    data = request.json
    user_id = data.get("user_id")
    video_url = data.get("video_url")
    post_id = data.get("post_id")

    if not all([user_id, video_url]):
        return jsonify({"error": "Missing required fields: user_id, video_url"}), 400

    result = video_analyzer.analyze_video_url(user_id, video_url, post_id)
    
    if result.get("success"):
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@video_analysis_bp.route("/analyze_video/<int:post_id>", methods=["GET"])
def get_video_analysis(post_id):
    """Get video analysis results by post ID."""
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

@video_analysis_bp.route("/video_analyses", methods=["GET"])
def get_video_analyses():
    """Get all video analyses for the current user."""
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    analyses = VideoAnalysis.query.filter_by(user_id=user_id).order_by(VideoAnalysis.analysis_date.desc()).all()
    
    return jsonify([{
        "id": analysis.id,
        "post_id": analysis.post_id,
        "video_url": analysis.video_url,
        "transcription_text": analysis.transcription_text,
        "visual_description": analysis.visual_description,
        "analysis_date": analysis.analysis_date.isoformat(),
        "provider_config_id": analysis.provider_config_id
    } for analysis in analyses]), 200

@video_analysis_bp.route("/analyze_trending", methods=["POST"])
def analyze_trending_content():
    """Analyze multiple trending content items."""
    data = request.json
    user_id = data.get("user_id")
    trending_items = data.get("trending_items", [])

    if not user_id:
        return jsonify({"error": "Missing required field: user_id"}), 400

    results = []
    for item in trending_items:
        if item.get("type") == "video" and item.get("url"):
            analysis = video_analyzer.analyze_video_url(user_id, item["url"], item.get("id"))
            results.append({
                "item_id": item.get("id"),
                "url": item["url"],
                "analysis": analysis
            })

    return jsonify({
        "success": True,
        "analyzed_count": len(results),
        "results": results
    }), 200
