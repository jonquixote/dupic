from flask import Blueprint, jsonify, request
from src.models import db, UserAnalytics

user_analytics_bp = Blueprint("user_analytics", __name__)

@user_analytics_bp.route("/user_analytics", methods=["POST"])
def add_user_analytics():
    data = request.json
    user_id = data.get("user_id")
    metric_name = data.get("metric_name")
    value = data.get("value")

    if not all([user_id, metric_name, value]):
        return jsonify({"error": "Missing required fields"}), 400

    new_analytics = UserAnalytics(
        user_id=user_id,
        metric_name=metric_name,
        value=value
    )
    db.session.add(new_analytics)
    db.session.commit()
    return jsonify({"message": "User analytics added successfully"}), 201

@user_analytics_bp.route("/user_analytics", methods=["GET"])
def get_user_analytics():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    analytics = UserAnalytics.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "metric_name": a.metric_name,
            "value": a.value,
            "timestamp": a.timestamp.isoformat()
        } for a in analytics
    ]), 200
