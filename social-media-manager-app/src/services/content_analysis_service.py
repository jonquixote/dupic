import requests
import base64
import tempfile
import os
import json
import re
from typing import Dict, Any, Optional
from src.services.ai_provider_service import AIProviderService
from src.models import db, VideoAnalysis

class ContentAnalysisService:
    """Service for analyzing social media content including video transcription and visual analysis."""
    
    def __init__(self):
        self.ai_service = AIProviderService()
    
    def analyze_video_url(self, user_id: int, video_url: str, post_id: int = None) -> Dict[str, Any]:
        """Analyze a video from URL including transcription and visual description."""
        try:
            # Download video content (in a real implementation, you'd want to handle this more robustly)
            response = requests.get(video_url, timeout=30)
            if response.status_code != 200:
                return {"error": f"Failed to download video: {response.status_code}"}
            
            video_data = response.content
            
            # Extract audio for transcription
            audio_data = self._extract_audio_from_video(video_data)
            if audio_data:
                transcription_result = self.ai_service.call_speech_to_text(user_id, audio_data)
            else:
                transcription_result = {
                    "transcription": "Audio extraction from video is not implemented.",
                    "success": False
                }
            
            # Extract frames for visual analysis
            frame_data = self._extract_frame_from_video(video_data)
            if frame_data:
                visual_result = self.ai_service.call_vision_to_text(
                    user_id,
                    {"image": frame_data, "prompt": "Describe this video frame in detail, including objects, people, actions, setting, mood, and visual style."}
                )
            else:
                visual_result = {
                    "description": "Video frame extraction is not implemented.",
                    "success": False
                }
            
            # Get AI config used
            config = self.ai_service._get_config_for_user(user_id)
            
            # Save analysis results
            analysis = VideoAnalysis(
                post_id=post_id or 0,
                video_url=video_url,
                transcription_text=transcription_result.get("transcription", ""),
                visual_description=visual_result.get("description", ""),
                provider_config_id=config.id if config else None
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            return {
                "success": True,
                "analysis_id": analysis.id,
                "transcription": transcription_result.get("transcription", ""),
                "visual_description": visual_result.get("description", ""),
                "transcription_success": transcription_result.get("success", False),
                "visual_success": visual_result.get("success", False)
            }
            
        except Exception as e:
            return {"error": f"Video analysis failed: {str(e)}"}
    
    def analyze_trending_content(self, user_id: int, trending_items: list) -> Dict[str, Any]:
        """Analyze multiple trending content items."""
        results = []
        
        for item in trending_items:
            if item.get("type") == "video" and item.get("url"):
                analysis = self.analyze_video_url(user_id, item["url"], item.get("id"))
                results.append({
                    "item_id": item.get("id"),
                    "url": item["url"],
                    "analysis": analysis
                })
        
        return {
            "success": True,
            "analyzed_count": len(results),
            "results": results
        }
    
    def get_content_insights(self, user_id: int, content_text: str) -> Dict[str, Any]:
        """Get AI-powered insights about content performance and optimization."""
        prompt = f"""
        Analyze the following social media content and provide insights:
        
        Content: "{content_text}"
        
        Please provide:
        1. Sentiment analysis (positive, negative, neutral)
        2. Key themes and topics
        3. Engagement potential (high, medium, low) with reasoning
        4. Suggested improvements
        5. Optimal posting times recommendation
        6. Hashtag suggestions (5-10 relevant hashtags)
        7. Target audience insights
        
        Format your response as JSON with these keys: sentiment, themes, engagement_potential, improvements, posting_times, hashtags, target_audience
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                # Try to parse JSON response
                insights = json.loads(result["content"])
                return {"success": True, "insights": insights}
            except json.JSONDecodeError:
                # If not valid JSON, return raw content
                return {"success": True, "insights": {"raw_analysis": result["content"]}}
        else:
            return result
    
    def generate_content_variations(self, user_id: int, original_content: str, character_profile: dict, count: int = 3) -> Dict[str, Any]:
        """Generate variations of content for A/B testing."""
        prompt = f"""
        Create {count} variations of the following social media content, maintaining the same core message but with different approaches:
        
        Original Content: "{original_content}"
        
        Character Profile:
        - Name: {character_profile.get('name', 'Unknown')}
        - Tone: {character_profile.get('tone', 'neutral')}
        - Target Audience: {character_profile.get('target_audience', 'general')}
        - Content Style: {character_profile.get('content_style', 'standard')}
        
        For each variation, provide:
        1. The content text
        2. The approach used (e.g., "more emotional", "data-driven", "humorous")
        3. Expected audience reaction
        
        Format as JSON array with objects containing: content, approach, expected_reaction
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                variations = json.loads(result["content"])
                return {"success": True, "variations": variations}
            except json.JSONDecodeError:
                return {"success": True, "variations": [{"content": result["content"], "approach": "AI-generated", "expected_reaction": "Unknown"}]}
        else:
            return result
    
    def _extract_audio_from_video(self, video_data: bytes) -> Optional[bytes]:
        """Extract audio from video data. This is a placeholder implementation."""
        # In a real implementation, you would use a library like ffmpeg-python or moviepy.
        # This feature is currently not implemented to avoid heavy dependencies.
        return None
    
    def _extract_frame_from_video(self, video_data: bytes) -> Optional[str]:
        """Extract a frame from video data and return as base64. This is a placeholder implementation."""
        # In a real implementation, you would use a library like opencv-python or ffmpeg-python.
        # This feature is currently not implemented to avoid heavy dependencies.
        return None
    
    def extract_hashtags_from_content(self, content: str) -> list:
        """Extract hashtags from content text."""
        hashtags = re.findall(r'#\w+', content)
        return hashtags
    
    def suggest_optimal_posting_time(self, user_id: int, platform: str, content_type: str) -> Dict[str, Any]:
        """Suggest optimal posting times based on platform and content type."""
        # This would typically involve analyzing historical performance data
        # For now, we'll provide general recommendations
        
        recommendations = {
            "instagram": {
                "image": ["11:00 AM", "2:00 PM", "5:00 PM"],
                "video": ["6:00 PM", "7:00 PM", "8:00 PM"],
                "story": ["9:00 AM", "12:00 PM", "7:00 PM"]
            },
            "twitter": {
                "text": ["9:00 AM", "12:00 PM", "3:00 PM"],
                "image": ["12:00 PM", "3:00 PM", "6:00 PM"],
                "video": ["6:00 PM", "7:00 PM", "9:00 PM"]
            },
            "tiktok": {
                "video": ["6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM"]
            },
            "linkedin": {
                "text": ["8:00 AM", "12:00 PM", "5:00 PM"],
                "article": ["7:00 AM", "8:00 AM", "12:00 PM"]
            }
        }
        
        platform_lower = platform.lower()
        if platform_lower in recommendations:
            times = recommendations[platform_lower].get(content_type, recommendations[platform_lower].get("text", ["12:00 PM"]))
            return {
                "success": True,
                "platform": platform,
                "content_type": content_type,
                "recommended_times": times,
                "timezone": "Local time"
            }
        else:
            return {
                "success": False,
                "error": f"No recommendations available for platform: {platform}"
            }
