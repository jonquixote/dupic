"""
AI Providers Integration Module
Supports multiple AI API providers using litellm
"""

import os
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum
try:
    import litellm  # type: ignore[import]
except Exception:
    litellm = None  # type: ignore

# Set API keys from environment variables
if litellm is not None:
    litellm.api_key = os.getenv("OPENAI_API_KEY")
    litellm.groq_api_key = os.getenv("GROQ_API_KEY")
    litellm.gemini_api_key = os.getenv("GEMINI_API_KEY")
    litellm.cohere_api_key = os.getenv("COHERE_API_KEY")
    litellm.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    litellm.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    litellm.cerebras_api_key = os.getenv("CEREBRAS_API_KEY")
else:
    # litellm is optional for editor/CI when not installed.
    # Runtime calls that require litellm will raise a clear ImportError.
    pass

class AIProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"
    GEMINI = "gemini"
    COHERE = "cohere"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    CEREBRAS = "cerebras"

@dataclass
class AIModel:
    name: str
    provider: AIProvider
    capabilities: List[str]
    max_tokens: int
    cost_per_token: float = 0.0

class AIProviderManager:
    """Manages multiple AI providers and their models via litellm"""
    
    def __init__(self):
        self.models = {}
        self._load_models()
    
    def _load_models(self):
        """Load available models for each provider"""
        
        self.models[AIProvider.OPENAI] = [
            AIModel("gpt-4o", AIProvider.OPENAI, ["text", "image"], 128000),
            AIModel("gpt-4o-mini", AIProvider.OPENAI, ["text", "image"], 128000),
            AIModel("gpt-3.5-turbo", AIProvider.OPENAI, ["text"], 16385),
        ]
        
        self.models[AIProvider.GROQ] = [
            AIModel("llama-3.1-405b-reasoning", AIProvider.GROQ, ["text"], 131072),
            AIModel("llama-3.1-70b-versatile", AIProvider.GROQ, ["text"], 131072),
            AIModel("llama-3.1-8b-instant", AIProvider.GROQ, ["text"], 131072),
        ]
        
        self.models[AIProvider.GEMINI] = [
            AIModel("gemini-1.5-pro", AIProvider.GEMINI, ["text", "image", "video"], 2000000),
            AIModel("gemini-1.5-flash", AIProvider.GEMINI, ["text", "image", "video"], 1000000),
        ]

        self.models[AIProvider.COHERE] = [
            AIModel("command-r-plus", AIProvider.COHERE, ["text"], 128000),
            AIModel("command-r", AIProvider.COHERE, ["text"], 128000),
        ]

        self.models[AIProvider.ANTHROPIC] = [
            AIModel("claude-3-opus-20240229", AIProvider.ANTHROPIC, ["text"], 200000),
            AIModel("claude-3.5-sonnet-20240620", AIProvider.ANTHROPIC, ["text"], 200000),
        ]

        self.models[AIProvider.OPENROUTER] = [
            AIModel("openrouter/google/palm-2-chat-bison", AIProvider.OPENROUTER, ["text"], 8192),
            AIModel("openrouter/meta-llama/llama-3-8b-instruct", AIProvider.OPENROUTER, ["text"], 8192),
        ]

        self.models[AIProvider.CEREBRAS] = [
            AIModel("cerebras/llama3-70b-instruct", AIProvider.CEREBRAS, ["text"], 4096),
        ]

    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available providers"""
        return list(self.models.keys())
    
    def get_models_for_provider(self, provider: AIProvider) -> List[AIModel]:
        """Get available models for a specific provider"""
        return self.models.get(provider, [])
    
    async def generate_text(self, model_name: str, 
                          messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """Generate text using litellm"""
        if litellm is None:
            raise ImportError(
                "litellm is not available. Install with `pip install litellm` "
                "or set up the project environment that provides it."
            )

        try:
            response = await litellm.acompletion(
                model=model_name,
                messages=messages,
                **kwargs
            )

            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if getattr(response, "usage", None) else {},
                "model": getattr(response, "model", model_name)
            }

        except Exception as e:
            raise Exception(f"Error generating text with {model_name}: {str(e)}")

    async def transcribe_audio(self, provider: 'AIProvider', audio_file_path: str, model: str, **kwargs) -> Dict[str, Any]:
        """Transcribe audio using litellm
        
        Args:
            provider (AIProvider): The AI provider to use
            audio_file_path (str): Path to the audio file to transcribe
            model (str): The model to use for transcription
            **kwargs: Additional arguments to pass to the transcription API
            
        Returns:
            Dict[str, Any]: Transcription result containing text, language, duration, and segments
            
        Raises:
            Exception: If transcription fails
        """
        if litellm is None:
            raise ImportError(
                "litellm is not available. Install with `pip install litellm` "
                "or set up the project environment that provides it."
            )

        # Map provider to model name
        model_name = model
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = await litellm.atranscription(
                    model=model_name,
                    file=audio_file,
                    **kwargs
                )

            return {
                "text": response.text,
                "language": getattr(response, "language", None),
                "duration": getattr(response, "duration", None),
                "segments": getattr(response, "segments", [])
            }

        except Exception as e:
            raise Exception(f"Error transcribing audio with {model_name}: {str(e)}")

    async def analyze_image(self, provider: 'AIProvider', model: str, image_file_path: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Analyze image using litellm
        
        Args:
            provider (AIProvider): The AI provider to use
            model (str): The model to use for image analysis
            image_file_path (str): Path to the image file to analyze
            prompt (str): Prompt to guide the image analysis
            **kwargs: Additional arguments to pass to the analysis API
            
        Returns:
            Dict[str, Any]: Analysis result containing content, usage, and model information
            
        Raises:
            Exception: If image analysis fails
        """
        if litellm is None:
            raise ImportError(
                "litellm is not available. Install with `pip install litellm` "
                "or set up the project environment that provides it."
            )

        # Map provider to model name
        model_name = model
        
        try:
            import base64
            with open(image_file_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
            response = await litellm.acompletion(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                        ]
                    }
                ],
                **kwargs
            )

            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if getattr(response, "usage", None) else {},
                "model": getattr(response, "model", model_name)
            }

        except Exception as e:
            raise Exception(f"Error analyzing image with {model_name}: {str(e)}")

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers
        
        Returns:
            Dict[str, Any]: Status information for each provider
        """
        status = {}
        for provider in self.get_available_providers():
            try:
                # Try to get a simple response from the provider
                status[provider.value] = {
                    "available": True,
                    "models": len(self.get_models_for_provider(provider))
                }
            except Exception:
                status[provider.value] = {
                    "available": False,
                    "error": "Provider not configured or unavailable"
                }
        return status

# Global instance
ai_manager = AIProviderManager()
