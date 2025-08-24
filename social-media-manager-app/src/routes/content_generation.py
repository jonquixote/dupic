from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # allow type checkers to see Flask symbols without requiring the package at runtime
    # Use a string import style to avoid static linters complaining in some setups
    from flask import Blueprint, request, jsonify  # type: ignore[import]

try:
    from flask import Blueprint, request, jsonify  # type: ignore[import]
except Exception:
    # Minimal runtime stubs to allow editors/tests to import this module when Flask
    # isn't installed. Real Flask should be used at runtime in production.
    class _DummyBlueprint:
        def __init__(self, name, import_name):
            self.name = name
            self.import_name = import_name

        def route(self, rule, methods=None):
            def decorator(f):
                return f
            return decorator

    Blueprint = _DummyBlueprint

    class _DummyRequest:
        @staticmethod
        def get_json():
            return None

    request = _DummyRequest()

    def jsonify(obj):
        # return a simple serializable representation for tests/editing
        import json

        return json.dumps(obj)

from src.services.content_generator import ContentGenerator
from src.models import Trend, CharacterProfile
from src.ai_providers import AIProvider
import asyncio

content_generation_bp = Blueprint("content_generation", __name__)

@content_generation_bp.route("/content/generate", methods=["POST"])
def generate_content_route():
    """Generate content based on a trend and character profile."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    trend_id = data.get("trend_id")
    character_id = data.get("character_id")
    provider_name = data.get("provider")
    model_name = data.get("model")
    content_type = data.get("content_type", "post")
    platform = data.get("platform", "twitter")
    additional_context = data.get("additional_context", "")

    if not all([trend_id, character_id, provider_name, model_name]):
        return jsonify({"error": "trend_id, character_id, provider, and model are required"}), 400

    try:
        provider = AIProvider(provider_name)
    except ValueError:
        return jsonify({"error": f"Invalid AI provider: {provider_name}"}), 400

    trend = Trend.query.get(trend_id)
    if not trend:
        return jsonify({"error": f"Trend with id {trend_id} not found"}), 404
    
    character = CharacterProfile.query.get(character_id)
    if not character:
        return jsonify({"error": f"CharacterProfile with id {character_id} not found"}), 404

    content_generator = ContentGenerator(provider=provider, model=model_name)
    
    # Run the async function in a new event loop
    result = asyncio.run(content_generator.generate_content(
        trend=trend,
        character=character,
        content_type=content_type,
        platform=platform,
        additional_context=additional_context
    ))

    return jsonify(result)
