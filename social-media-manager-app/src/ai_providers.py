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

# Global instance
ai_manager = AIProviderManager()
