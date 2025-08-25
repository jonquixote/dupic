import openai
import requests
import json
import logging
from typing import Dict, Any, Optional
from src.models import db, AIProviderConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Making API call to {provider_name} for {call_type} with model {model}")
        
        if provider_name not in self.supported_providers:
            error_msg = f"Unsupported provider: {provider_name}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        try:
            result = self.supported_providers[provider_name](config, call_type, data, model)
            if "error" in result:
                logger.error(f"API call to {provider_name} failed: {result['error']}")
            else:
                logger.info(f"API call to {provider_name} successful")
            return result
        except Exception as e:
            error_msg = f"API call failed: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _call_openai(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to OpenAI."""
        try:
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
                import io
                audio_file = io.BytesIO(data)
                audio_file.name = "audio.wav"  # Give it a name for the API
                
                response = client.audio.transcriptions.create(
                    model=model,
                    file=audio_file
                )
                return {
                    "success": True,
                    "transcription": response.text
                }
            
            elif call_type == "vision_to_text":
                # For vision, data should be {"image": bytes, "prompt": str}
                import base64
                # Convert image bytes to base64
                image_data = base64.b64encode(data["image"]).decode("utf-8")
                prompt = data.get("prompt", "Describe this image in detail.")
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    }
                                }
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
        except Exception as e:
            return {"error": f"OpenAI API call failed: {str(e)}"}
    
    def _call_google(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Google AI (Gemini)."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=config.api_key)
            
            if call_type == "text":
                gemini_model = genai.GenerativeModel(model)
                response = gemini_model.generate_content(data)
                return {
                    "success": True,
                    "content": response.text,
                    "usage": {
                        "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                        "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                        "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                    } if response.usage_metadata else {}
                }
            
            elif call_type == "speech_to_text":
                # Gemini doesn't have a direct speech-to-text API
                # We would need to use a separate service for this
                return {"error": "Speech-to-text not directly supported by Google Gemini. Use a separate transcription service."}
            
            elif call_type == "vision_to_text":
                # For vision, data should be {"image": bytes, "prompt": str}
                gemini_model = genai.GenerativeModel(model)
                import io
                from PIL import Image
                
                # Convert bytes to PIL Image
                image = Image.open(io.BytesIO(data["image"]))
                prompt = data.get("prompt", "Describe this image in detail.")
                
                response = gemini_model.generate_content([prompt, image])
                return {
                    "success": True,
                    "description": response.text,
                    "usage": {
                        "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                        "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                        "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                    } if response.usage_metadata else {}
                }
            
            return {"error": f"Unsupported call type: {call_type}"}
        except Exception as e:
            return {"error": f"Google AI API call failed: {str(e)}"}
    
    def _call_anthropic(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Anthropic (Claude)."""
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=config.api_key)
            
            if call_type == "text":
                response = client.messages.create(
                    model=model,
                    max_tokens=1000,
                    messages=[{"role": "user", "content": data}]
                )
                return {
                    "success": True,
                    "content": response.content[0].text,
                    "usage": {
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    }
                }
            
            elif call_type == "speech_to_text":
                # Anthropic doesn't have a direct speech-to-text API
                # We would need to use a separate service for this
                return {"error": "Speech-to-text not directly supported by Anthropic. Use a separate transcription service."}
            
            elif call_type == "vision_to_text":
                # For vision, data should be {"image": bytes, "prompt": str}
                import base64
                # Convert image bytes to base64
                image_data = base64.b64encode(data["image"]).decode("utf-8")
                prompt = data.get("prompt", "Describe this image in detail.")
                
                response = client.messages.create(
                    model=model,
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": image_data,
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": prompt,
                                },
                            ],
                        }
                    ],
                )
                return {
                    "success": True,
                    "description": response.content[0].text,
                    "usage": {
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    }
                }
            
            return {"error": f"Unsupported call type: {call_type}"}
        except Exception as e:
            return {"error": f"Anthropic API call failed: {str(e)}"}
    
    def _call_azure(self, config: AIProviderConfig, call_type: str, data: Any, model: str) -> Dict[str, Any]:
        """Make API call to Azure OpenAI."""
        try:
            from openai import AzureOpenAI
            import os
            
            # For Azure, we need to extract the endpoint from the API key or config
            # The config might need to store additional Azure-specific information
            # For now, we'll assume it's in environment variables
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
            
            if not azure_endpoint:
                return {"error": "Azure OpenAI endpoint not configured. Set AZURE_OPENAI_ENDPOINT environment variable."}
            
            client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=config.api_key,
                api_version=api_version
            )
            
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
                # Azure OpenAI doesn't have a direct speech-to-text API
                # We would need to use Azure Speech Service for this
                return {"error": "Speech-to-text not directly supported by Azure OpenAI. Use Azure Speech Service."}
            
            elif call_type == "vision_to_text":
                # For vision, data should be {"image": bytes, "prompt": str}
                import base64
                # Convert image bytes to base64
                image_data = base64.b64encode(data["image"]).decode("utf-8")
                prompt = data.get("prompt", "Describe this image in detail.")
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_data}"
                                    }
                                }
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
        except Exception as e:
            return {"error": f"Azure OpenAI API call failed: {str(e)}"}
    
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
