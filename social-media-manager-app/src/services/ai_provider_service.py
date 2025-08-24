import openai
import requests
import json
from typing import Dict, Any, Optional
from src.models import db, AIProviderConfig

class AIProviderService:
    """Service for managing AI provider configurations and API calls."""
    
    def __init__(self):
        self.supported_providers = {
            "openai": self._call_openai,
            "google": self._call_google,
            "anthropic": self._call_anthropic,
            "azure": self._call_azure
        }
    
    def get_user_default_config(self, user_id: int, provider_type: str = None) -> Optional[AIProviderConfig]:
        """Get the default AI provider configuration for a user."""
        query = AIProviderConfig.query.filter_by(user_id=user_id, is_default=True)
        if provider_type:
            query = query.filter_by(provider_name=provider_type)
        return query.first()
    
    def get_admin_default_config(self, provider_type: str = None) -> Optional[AIProviderConfig]:
        """Get the admin default AI provider configuration."""
        # Admin user_id is assumed to be 1 or a special admin user
        return self.get_user_default_config(user_id=1, provider_type=provider_type)
    
    def call_text_generation(self, user_id: int, prompt: str, model: str = None, provider: str = None) -> Dict[str, Any]:
        """Generate text using the user's configured AI provider."""
        config = self._get_config_for_user(user_id, provider)
        if not config:
            return {"error": "No AI provider configuration found"}
        
        model = model or config.default_model_text
        if not model:
            return {"error": "No text generation model configured"}
        
        return self._make_api_call(config, "text", prompt, model)
    
    def call_speech_to_text(self, user_id: int, audio_data: bytes, model: str = None, provider: str = None) -> Dict[str, Any]:
        """Transcribe audio using the user's configured AI provider."""
        config = self._get_config_for_user(user_id, provider)
        if not config:
            return {"error": "No AI provider configuration found"}
        
        model = model or config.default_model_speech_to_text
        if not model:
            return {"error": "No speech-to-text model configured"}
        
        return self._make_api_call(config, "speech_to_text", audio_data, model)
    
    def call_vision_to_text(self, user_id: int, image_data: bytes, prompt: str = "", model: str = None, provider: str = None) -> Dict[str, Any]:
        """Analyze image using the user's configured AI provider."""
        config = self._get_config_for_user(user_id, provider)
        if not config:
            return {"error": "No AI provider configuration found"}
        
        model = model or config.default_model_vision_to_text
        if not model:
            return {"error": "No vision-to-text model configured"}
        
        return self._make_api_call(config, "vision_to_text", {"image": image_data, "prompt": prompt}, model)
    
    def _get_config_for_user(self, user_id: int, provider: str = None) -> Optional[AIProviderConfig]:
        """Get AI config for user, falling back to admin config if needed."""
        config = self.get_user_default_config(user_id, provider)
        if not config:
            config = self.get_admin_default_config(provider)
        return config
    
    def _make_api_call(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to the configured provider."""
        provider_name = config.provider_name.lower()
        if provider_name not in self.supported_providers:
            return {"error": f"Unsupported provider: {provider_name}"}
        
        try:
            return self.supported_providers[provider_name](config, call_type, data, model)
        except Exception as e:
            return {"error": f"API call failed: {str(e)}"}
    
    def _call_openai(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to OpenAI."""
        client = openai.OpenAI(api_key=config.api_key)
        
        if call_type == "text":
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": data}],
                max_tokens=1000
            )
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None
            }
        
        elif call_type == "speech_to_text":
            # For speech-to-text, data should be audio bytes
            response = client.audio.transcriptions.create(
                model=model,
                file=data
            )
            return {
                "success": True,
                "transcription": response.text
            }
        
        elif call_type == "vision_to_text":
            # For vision, data should be {"image": bytes, "prompt": str}
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": data.get("prompt", "Describe this image in detail.")},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{data['image']}"}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            return {
                "success": True,
                "description": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else None
            }
        
        return {"error": f"Unsupported call type: {call_type}"}
    
    def _call_google(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Google AI (Gemini)."""
        # Placeholder for Google AI implementation
        # This would require the Google AI SDK
        return {"error": "Google AI integration not yet implemented"}
    
    def _call_anthropic(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Anthropic (Claude)."""
        # Placeholder for Anthropic implementation
        # This would require the Anthropic SDK
        return {"error": "Anthropic integration not yet implemented"}
    
    def _call_azure(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Azure OpenAI."""
        # Placeholder for Azure OpenAI implementation
        return {"error": "Azure OpenAI integration not yet implemented"}
    
    def test_configuration(self, config: AIProviderConfig) -> Dict[str, Any]:
        """Test an AI provider configuration."""
        try:
            result = self._make_api_call(config, "text", "Hello, this is a test.", config.default_model_text)
            if result.get("success"):
                return {"success": True, "message": "Configuration test successful"}
            else:
                return {"success": False, "error": result.get("error", "Unknown error")}
        except Exception as e:
            return {"success": False, "error": f"Test failed: {str(e)}"}
