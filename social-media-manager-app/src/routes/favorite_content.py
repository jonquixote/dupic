from flask import Blueprint, jsonify, request
from src.models import db, FavoriteContent

favorite_content_bp = Blueprint("favorite_content", __name__)

@favorite_content_bp.route("/favorite_content", methods=["POST"])
def add_favorite_content():
    data = request.json
    user_id = data.get("user_id")
    content_id = data.get("content_id")

    if not all([user_id, content_id]):
        return jsonify({"error": "Missing required fields"}), 400

    new_favorite = FavoriteContent(
        user_id=user_id,
        content_id=content_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Content added to favorites successfully"}), 201

@favorite_content_bp.route("/favorite_content", methods=["GET"])
def get_favorite_content():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    favorites = FavoriteContent.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": f.id,
            "user_id": f.user_id,
            "content_id": f.content_id,
            "saved_date": f.saved_date.isoformat()
        } for f in favorites
    ]), 200
