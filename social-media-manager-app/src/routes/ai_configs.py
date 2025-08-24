from flask import Blueprint, jsonify, request
from src.models import db, AIProviderConfig
from src.services.ai_provider_service import AIProviderService

ai_configs_bp = Blueprint("ai_configs", __name__)
ai_service = AIProviderService()

@ai_configs_bp.route("/ai_configs", methods=["POST"])
def add_ai_config():
    data = request.json
    user_id = data.get("user_id")
    provider_name = data.get("provider_name")
    api_key = data.get("api_key")
    default_model_text = data.get("default_model_text")
    default_model_speech_to_text = data.get("default_model_speech_to_text")
    default_model_vision_to_text = data.get("default_model_vision_to_text")
    is_default = data.get("is_default", False)

    if not all([user_id, provider_name, api_key]):
        return jsonify({"error": "Missing required fields"}), 400

    if is_default:
        # Set all other configs for this user to not default
        AIProviderConfig.query.filter_by(user_id=user_id).update({"is_default": False})

    new_config = AIProviderConfig(
        user_id=user_id,
        provider_name=provider_name,
        api_key=api_key,
        default_model_text=default_model_text,
        default_model_speech_to_text=default_model_speech_to_text,
        default_model_vision_to_text=default_model_vision_to_text,
        is_default=is_default
    )
    db.session.add(new_config)
    db.session.commit()
    return jsonify({"message": "AI Provider config added successfully", "id": new_config.id}), 201

@ai_configs_bp.route("/ai_configs", methods=["GET"])
def get_ai_configs():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    configs = AIProviderConfig.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "id": config.id,
            "user_id": config.user_id,
            "provider_name": config.provider_name,
            "api_key": "***" + config.api_key[-4:] if len(config.api_key) > 4 else "***",  # Mask API key
            "default_model_text": config.default_model_text,
            "default_model_speech_to_text": config.default_model_speech_to_text,
            "default_model_vision_to_text": config.default_model_vision_to_text,
            "is_default": config.is_default
        } for config in configs
    ]), 200

@ai_configs_bp.route("/ai_configs/<int:config_id>", methods=["PUT"])
def update_ai_config(config_id):
    data = request.json
    config = AIProviderConfig.query.get_or_404(config_id)

    if "provider_name" in data: config.provider_name = data["provider_name"]
    if "api_key" in data: config.api_key = data["api_key"]
    if "default_model_text" in data: config.default_model_text = data["default_model_text"]
    if "default_model_speech_to_text" in data: config.default_model_speech_to_text = data["default_model_speech_to_text"]
    if "default_model_vision_to_text" in data: config.default_model_vision_to_text = data["default_model_vision_to_text"]
    if "is_default" in data:
        if data["is_default"]:
            # Set all other configs for this user to not default
            AIProviderConfig.query.filter_by(user_id=config.user_id).update({"is_default": False})
        config.is_default = data["is_default"]

    db.session.commit()
    return jsonify({"message": "AI Provider config updated successfully"}), 200

@ai_configs_bp.route("/ai_configs/<int:config_id>", methods=["DELETE"])
def delete_ai_config(config_id):
    config = AIProviderConfig.query.get_or_404(config_id)
    db.session.delete(config)
    db.session.commit()
    return jsonify({"message": "AI Provider config deleted successfully"}), 204

@ai_configs_bp.route("/ai_configs/set_default/<int:config_id>", methods=["POST"])
def set_default_ai_config(config_id):
    config = AIProviderConfig.query.get_or_404(config_id)
    AIProviderConfig.query.filter_by(user_id=config.user_id).update({"is_default": False})
    config.is_default = True
    db.session.commit()
    return jsonify({"message": "AI Provider config set as default"}), 200

@ai_configs_bp.route("/ai_configs/<int:config_id>/test", methods=["POST"])
def test_ai_config(config_id):
    config = AIProviderConfig.query.get_or_404(config_id)
    result = ai_service.test_configuration(config)
    return jsonify(result), 200 if result.get("success") else 400
