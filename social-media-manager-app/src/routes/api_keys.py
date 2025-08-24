from flask import Blueprint, request, jsonify
from src.models import db
from src.models.api_key import ApiKey

api_keys_bp = Blueprint("api_keys", __name__)

@api_keys_bp.route("/api_keys", methods=["GET"])
def get_api_keys():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    api_keys = ApiKey.query.filter_by(user_id=user_id).all()
    return jsonify([api_key.to_dict(mask_key=True) for api_key in api_keys])

@api_keys_bp.route("/api_keys", methods=["POST"])
def create_api_key():
    data = request.get_json()
    user_id = data.get("user_id")
    service = data.get("service")
    key = data.get("key")

    if not all([user_id, service, key]):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if a key for this service already exists
    existing_key = ApiKey.query.filter_by(user_id=user_id, service=service).first()
    if existing_key:
        return jsonify({"error": f"API key for {service} already exists"}), 409

    new_api_key = ApiKey(user_id=user_id, service=service, key=key)
    db.session.add(new_api_key)
    db.session.commit()

    return jsonify(new_api_key.to_dict()), 201

@api_keys_bp.route("/api_keys/<int:api_key_id>", methods=["PUT"])
def update_api_key(api_key_id):
    api_key = ApiKey.query.get_or_404(api_key_id)
    data = request.get_json()
    api_key.key = data.get("key", api_key.key)
    db.session.commit()
    return jsonify(api_key.to_dict(mask_key=True))

@api_keys_bp.route("/api_keys/<int:api_key_id>", methods=["DELETE"])
def delete_api_key(api_key_id):
    api_key = ApiKey.query.get_or_404(api_key_id)
    db.session.delete(api_key)
    db.session.commit()
    return jsonify({"message": "API key deleted successfully"}), 200