"""
AI Providers Integration Module
Supports multiple AI API providers including Groq, Cerebras, OpenRouter, and others
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import openai
from groq import Groq
import google.generativeai as genai

class AIProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"
    CEREBRAS = "cerebras"
    OPENROUTER = "openrouter"
    GEMINI = "gemini"

@dataclass
class AIModel:
    name: str
    provider: AIProvider
    capabilities: List[str]  # e.g., ["text", "image", "audio", "video"]
    max_tokens: int
    cost_per_token: float = 0.0

class AIProviderManager:
    """Manages multiple AI providers and their models"""
    
    def __init__(self):
        self.providers = {}
        self.models = {}
        self._initialize_providers()
        self._load_models()
    
    def _initialize_providers(self):
        """Initialize all AI providers with their API keys"""
        
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            self.providers[AIProvider.OPENAI] = openai.OpenAI(
                api_key=os.getenv('OPENAI_API_KEY')
            )
        
        # Groq
        if os.getenv('GROQ_API_KEY'):
            self.providers[AIProvider.GROQ] = Groq(
                api_key=os.getenv('GROQ_API_KEY')
            )
        
        # Gemini
        if os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            self.providers[AIProvider.GEMINI] = genai
        
        # Cerebras (using OpenAI-compatible API)
        if os.getenv('CEREBRAS_API_KEY'):
            self.providers[AIProvider.CEREBRAS] = openai.OpenAI(
                api_key=os.getenv('CEREBRAS_API_KEY'),
                base_url="https://api.cerebras.ai/v1"
            )
        
        # OpenRouter
        if os.getenv('OPENROUTER_API_KEY'):
            self.providers[AIProvider.OPENROUTER] = openai.OpenAI(
                api_key=os.getenv('OPENROUTER_API_KEY'),
                base_url="https://openrouter.ai/api/v1"
            )
    
    def _load_models(self):
        """Load available models for each provider"""
        
        # OpenAI Models
        self.models[AIProvider.OPENAI] = [
            AIModel("gpt-4o", AIProvider.OPENAI, ["text", "image"], 128000),
            AIModel("gpt-4o-mini", AIProvider.OPENAI, ["text", "image"], 128000),
            AIModel("gpt-3.5-turbo", AIProvider.OPENAI, ["text"], 16385),
            AIModel("whisper-1", AIProvider.OPENAI, ["audio"], 25000000),  # 25MB file limit
            AIModel("dall-e-3", AIProvider.OPENAI, ["image_generation"], 4000),
        ]
        
        # Groq Models (including Whisper, Scout, Maverick)
        self.models[AIProvider.GROQ] = [
            AIModel("llama-3.1-405b-reasoning", AIProvider.GROQ, ["text"], 131072),
            AIModel("llama-3.1-70b-versatile", AIProvider.GROQ, ["text"], 131072),
            AIModel("llama-3.1-8b-instant", AIProvider.GROQ, ["text"], 131072),
            AIModel("mixtral-8x7b-32768", AIProvider.GROQ, ["text"], 32768),
            AIModel("gemma2-9b-it", AIProvider.GROQ, ["text"], 8192),
            AIModel("whisper-large-v3", AIProvider.GROQ, ["audio"], 25000000),
            AIModel("llama-3.2-90b-vision-preview", AIProvider.GROQ, ["text", "image"], 131072),
            AIModel("llama-3.2-11b-vision-preview", AIProvider.GROQ, ["text", "image"], 131072),
        ]
        
        # Cerebras Models
        self.models[AIProvider.CEREBRAS] = [
            AIModel("llama3.1-8b", AIProvider.CEREBRAS, ["text"], 128000),
            AIModel("llama3.1-70b", AIProvider.CEREBRAS, ["text"], 128000),
        ]
        
        # OpenRouter Models
        self.models[AIProvider.OPENROUTER] = [
            AIModel("anthropic/claude-3.5-sonnet", AIProvider.OPENROUTER, ["text"], 200000),
            AIModel("meta-llama/llama-3.1-405b-instruct", AIProvider.OPENROUTER, ["text"], 131072),
            AIModel("google/gemini-pro-1.5", AIProvider.OPENROUTER, ["text", "image"], 2000000),
            AIModel("openai/gpt-4o", AIProvider.OPENROUTER, ["text", "image"], 128000),
        ]
        
        # Gemini Models
        self.models[AIProvider.GEMINI] = [
            AIModel("gemini-1.5-pro", AIProvider.GEMINI, ["text", "image", "video"], 2000000),
            AIModel("gemini-1.5-flash", AIProvider.GEMINI, ["text", "image", "video"], 1000000),
            AIModel("gemini-pro", AIProvider.GEMINI, ["text"], 32768),
        ]
    
    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_models_for_provider(self, provider: AIProvider) -> List[AIModel]:
        """Get available models for a specific provider"""
        return self.models.get(provider, [])
    
    def get_model(self, provider: AIProvider, model_name: str) -> Optional[AIModel]:
        """Get specific model information"""
        models = self.models.get(provider, [])
        for model in models:
            if model.name == model_name:
                return model
        return None
    
    async def generate_text(self, provider: AIProvider, model_name: str, 
                          messages: List[Dict], **kwargs) -> Dict[str, Any]:
        """Generate text using specified provider and model"""
        
        if provider not in self.providers:
            raise ValueError(f"Provider {provider.value} not available")
        
        try:
            if provider == AIProvider.OPENAI:
                response = self.providers[provider].chat.completions.create(
                    model=model_name,
                    messages=messages,
                    **kwargs
                )
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.dict() if response.usage else {},
                    "model": response.model
                }
            
            elif provider == AIProvider.GROQ:
                response = self.providers[provider].chat.completions.create(
                    model=model_name,
                    messages=messages,
                    **kwargs
                )
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.dict() if response.usage else {},
                    "model": response.model
                }
            
            elif provider == AIProvider.CEREBRAS or provider == AIProvider.OPENROUTER:
                response = self.providers[provider].chat.completions.create(
                    model=model_name,
                    messages=messages,
                    **kwargs
                )
                return {
                    "content": response.choices[0].message.content,
                    "usage": response.usage.dict() if response.usage else {},
                    "model": response.model
                }
            
            elif provider == AIProvider.GEMINI:
                model = genai.GenerativeModel(model_name)
                # Convert messages to Gemini format
                prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
                response = model.generate_content(prompt)
                return {
                    "content": response.text,
                    "usage": {},
                    "model": model_name
                }
            
        except Exception as e:
            raise Exception(f"Error generating text with {provider.value}: {str(e)}")
    
    async def transcribe_audio(self, provider: AIProvider, audio_file_path: str, 
                             model_name: str = None) -> Dict[str, Any]:
        """Transcribe audio using specified provider"""
        
        if provider == AIProvider.OPENAI:
            model_name = model_name or "whisper-1"
            with open(audio_file_path, "rb") as audio_file:
                response = self.providers[provider].audio.transcriptions.create(
                    model=model_name,
                    file=audio_file
                )
            return {"text": response.text}
        
        elif provider == AIProvider.GROQ:
            model_name = model_name or "whisper-large-v3"
            with open(audio_file_path, "rb") as audio_file:
                response = self.providers[provider].audio.transcriptions.create(
                    model=model_name,
                    file=audio_file
                )
            return {"text": response.text}
        
        else:
            raise ValueError(f"Audio transcription not supported for {provider.value}")
    
    async def analyze_image(self, provider: AIProvider, model_name: str, 
                          image_path: str, prompt: str) -> Dict[str, Any]:
        """Analyze image using vision models"""
        
        if provider == AIProvider.OPENAI:
            import base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = self.providers[provider].chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ]
            )
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else {},
                "model": response.model
            }
        
        elif provider == AIProvider.GROQ:
            import base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            response = self.providers[provider].chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ]
            )
            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if response.usage else {},
                "model": response.model
            }
        
        elif provider == AIProvider.GEMINI:
            from PIL import Image
            img = Image.open(image_path)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content([prompt, img])
            return {
                "content": response.text,
                "usage": {},
                "model": model_name
            }
        
        else:
            raise ValueError(f"Image analysis not supported for {provider.value}")
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers"""
        status = {}
        for provider in AIProvider:
            status[provider.value] = {
                "available": provider in self.providers,
                "models_count": len(self.models.get(provider, [])),
                "capabilities": []
            }
            
            if provider in self.models:
                capabilities = set()
                for model in self.models[provider]:
                    capabilities.update(model.capabilities)
                status[provider.value]["capabilities"] = list(capabilities)
        
        return status

# Global instance
ai_manager = AIProviderManager()

