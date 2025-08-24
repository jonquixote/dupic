from typing import Dict, Any, List, Optional
from src.services.ai_provider_service import AIProviderService
from src.models.character import CharacterProfile

class EnhancedContentGenerator:
    """Enhanced content generation service with dialogue, visual suggestions, and comprehensive content creation."""
    
    def __init__(self):
        self.ai_service = AIProviderService()
    
    def generate_comprehensive_content(self, user_id: int, trend_data: Dict[str, Any], character_profile: CharacterProfile, platform: str) -> Dict[str, Any]:
        """Generate comprehensive content including text, dialogue, visual suggestions, and metadata."""
        
        # Build comprehensive prompt
        prompt = self._build_comprehensive_prompt(trend_data, character_profile, platform)
        
        # Generate content using AI
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if not result.get("success"):
            return result
        
        # Parse and structure the generated content
        try:
            import json
            content_data = json.loads(result["content"])
            
            # Enhance with additional suggestions
            content_data = self._enhance_content_data(content_data, character_profile, platform)
            
            return {
                "success": True,
                "content": content_data,
                "usage": result.get("usage")
            }
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "success": True,
                "content": {
                    "main_text": result["content"],
                    "platform": platform,
                    "character_name": character_profile.name
                }
            }
    
    def generate_dialogue_suggestions(self, user_id: int, context: str, character_profile: CharacterProfile, scenario: str = "general") -> Dict[str, Any]:
        """Generate dialogue suggestions based on character profile and context."""
        
        prompt = f"""
        Generate dialogue suggestions for a social media content creator with the following profile:
        
        Character: {character_profile.name}
        Tone: {character_profile.tone}
        Dialogue Style: {character_profile.dialogue_style}
        Target Audience: {character_profile.target_audience}
        Content Style: {character_profile.content_style}
        
        Context: {context}
        Scenario: {scenario}
        
        Generate 5 different dialogue options that this character would use, each with:
        1. The dialogue text
        2. The emotional tone
        3. When to use it (situation)
        4. Expected audience reaction
        
        Format as JSON array with objects containing: dialogue, tone, situation, expected_reaction
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                import json
                dialogues = json.loads(result["content"])
                return {"success": True, "dialogues": dialogues}
            except json.JSONDecodeError:
                return {"success": True, "dialogues": [{"dialogue": result["content"], "tone": "generated", "situation": "general", "expected_reaction": "engagement"}]}
        else:
            return result
    
    def generate_visual_suggestions(self, user_id: int, content_text: str, character_profile: CharacterProfile, platform: str) -> Dict[str, Any]:
        """Generate comprehensive visual suggestions including wardrobe, props, and background."""
        
        prompt = f"""
        Generate detailed visual suggestions for social media content based on:
        
        Content: "{content_text}"
        Character Profile:
        - Name: {character_profile.name}
        - Visual Wardrobe Style: {character_profile.visual_wardrobe}
        - Preferred Props: {character_profile.visual_props}
        - Background Preferences: {character_profile.visual_background}
        - Target Audience: {character_profile.target_audience}
        
        Platform: {platform}
        
        Provide detailed suggestions for:
        1. Wardrobe (specific clothing items, colors, style)
        2. Props (objects, accessories, tools)
        3. Background/Setting (location, lighting, mood)
        4. Camera angles and framing
        5. Color palette
        6. Lighting suggestions
        7. Overall visual mood/aesthetic
        
        Format as JSON with keys: wardrobe, props, background, camera_angles, color_palette, lighting, visual_mood
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                import json
                visual_suggestions = json.loads(result["content"])
                return {"success": True, "visual_suggestions": visual_suggestions}
            except json.JSONDecodeError:
                return {"success": True, "visual_suggestions": {"general": result["content"]}}
        else:
            return result
    
    def generate_hashtag_strategy(self, user_id: int, content_text: str, platform: str, target_audience: str) -> Dict[str, Any]:
        """Generate strategic hashtag recommendations."""
        
        prompt = f"""
        Create a comprehensive hashtag strategy for:
        
        Content: "{content_text}"
        Platform: {platform}
        Target Audience: {target_audience}
        
        Provide:
        1. Primary hashtags (3-5 most important, high-engagement)
        2. Secondary hashtags (5-8 supporting hashtags)
        3. Niche hashtags (3-5 specific to the content/audience)
        4. Trending hashtags (2-3 currently popular, if relevant)
        5. Branded hashtags (1-2 for brand building)
        6. Community hashtags (2-3 for community engagement)
        
        For each category, explain why these hashtags were chosen.
        
        Format as JSON with keys: primary, secondary, niche, trending, branded, community, explanations
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                import json
                hashtag_strategy = json.loads(result["content"])
                return {"success": True, "hashtag_strategy": hashtag_strategy}
            except json.JSONDecodeError:
                # Extract hashtags from text if JSON parsing fails
                import re
                hashtags = re.findall(r'#\w+', result["content"])
                return {"success": True, "hashtag_strategy": {"all": hashtags, "raw": result["content"]}}
        else:
            return result
    
    def generate_call_to_action_suggestions(self, user_id: int, content_text: str, platform: str, goal: str = "engagement") -> Dict[str, Any]:
        """Generate call-to-action suggestions based on content and goals."""
        
        prompt = f"""
        Generate call-to-action (CTA) suggestions for:
        
        Content: "{content_text}"
        Platform: {platform}
        Goal: {goal}
        
        Create 5 different CTA options:
        1. Engagement-focused (likes, comments, shares)
        2. Community-building (follow, join, connect)
        3. Action-oriented (visit, try, learn)
        4. Question-based (interactive, discussion)
        5. Value-driven (save, bookmark, share with friends)
        
        For each CTA, provide:
        - The CTA text
        - Why it works
        - Expected outcome
        - Best placement in content
        
        Format as JSON array with objects containing: cta_text, reason, expected_outcome, placement
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                import json
                cta_suggestions = json.loads(result["content"])
                return {"success": True, "cta_suggestions": cta_suggestions}
            except json.JSONDecodeError:
                return {"success": True, "cta_suggestions": [{"cta_text": result["content"], "reason": "AI generated", "expected_outcome": "engagement", "placement": "end"}]}
        else:
            return result
    
    def generate_content_series(self, user_id: int, topic: str, character_profile: CharacterProfile, platform: str, count: int = 5) -> Dict[str, Any]:
        """Generate a series of related content pieces."""
        
        prompt = f"""
        Create a content series of {count} related posts about: {topic}
        
        Character Profile:
        - Name: {character_profile.name}
        - Tone: {character_profile.tone}
        - Content Style: {character_profile.content_style}
        - Target Audience: {character_profile.target_audience}
        
        Platform: {platform}
        
        For each post in the series, provide:
        1. Post title/hook
        2. Main content text
        3. Key message
        4. Suggested hashtags (3-5)
        5. Call-to-action
        6. Visual suggestion
        7. Connection to other posts in series
        
        Ensure the series has a logical flow and builds engagement over time.
        
        Format as JSON array with objects containing: title, content, key_message, hashtags, cta, visual_suggestion, series_connection
        """
        
        result = self.ai_service.call_text_generation(user_id, prompt)
        
        if result.get("success"):
            try:
                import json
                content_series = json.loads(result["content"])
                return {"success": True, "content_series": content_series}
            except json.JSONDecodeError:
                return {"success": True, "content_series": [{"title": f"{topic} Series", "content": result["content"]}]}
        else:
            return result
    
    def _build_comprehensive_prompt(self, trend_data: Dict[str, Any], character_profile: CharacterProfile, platform: str) -> str:
        """Build a comprehensive prompt for content generation."""
        
        return f"""
        Create comprehensive social media content based on the following:
        
        TREND DATA:
        - Topic: {trend_data.get('topic', 'General')}
        - Platform: {trend_data.get('platform', platform)}
        - Engagement Score: {trend_data.get('engagement_score', 'N/A')}
        - Trend Type: {trend_data.get('type', 'General')}
        - Context: {trend_data.get('description', 'No additional context')}
        
        CHARACTER PROFILE:
        - Name: {character_profile.name}
        - Description: {character_profile.description}
        - Tone: {character_profile.tone}
        - Target Audience: {character_profile.target_audience}
        - Content Style: {character_profile.content_style}
        - Dialogue Style: {character_profile.dialogue_style}
        - Visual Wardrobe: {character_profile.visual_wardrobe}
        - Visual Props: {character_profile.visual_props}
        - Visual Background: {character_profile.visual_background}
        - Keywords: {', '.join(character_profile.keywords) if character_profile.keywords else 'None'}
        
        TARGET PLATFORM: {platform}
        
        Generate comprehensive content including:
        1. Main post text (optimized for {platform})
        2. Alternative hook/opening lines (3 options)
        3. Suggested dialogue/quotes (2-3 options)
        4. Hashtag strategy (primary, secondary, niche)
        5. Call-to-action suggestions (2-3 options)
        6. Visual suggestions (wardrobe, props, background, mood)
        7. Posting time recommendation
        8. Engagement prediction and strategy
        9. Content variations for A/B testing (2 alternatives)
        10. Cross-platform adaptation notes
        
        Format the response as JSON with these keys: main_text, hook_alternatives, dialogue_options, hashtag_strategy, cta_options, visual_suggestions, posting_time, engagement_strategy, content_variations, cross_platform_notes
        """
    
    def _enhance_content_data(self, content_data: Dict[str, Any], character_profile: CharacterProfile, platform: str) -> Dict[str, Any]:
        """Enhance generated content data with additional metadata and suggestions."""
        
        # Add character and platform metadata
        content_data["character_name"] = character_profile.name
        content_data["character_tone"] = character_profile.tone
        content_data["target_platform"] = platform
        content_data["generated_timestamp"] = __import__('datetime').datetime.now().isoformat()
        
        # Add platform-specific optimizations
        if platform.lower() == "instagram":
            content_data["platform_tips"] = [
                "Use high-quality visuals",
                "Include relevant hashtags (up to 30)",
                "Post during peak hours (11 AM - 1 PM, 7 PM - 9 PM)",
                "Use Stories for behind-the-scenes content"
            ]
        elif platform.lower() == "twitter":
            content_data["platform_tips"] = [
                "Keep text under 280 characters",
                "Use 1-2 relevant hashtags",
                "Include engaging visuals or GIFs",
                "Tweet during business hours for max engagement"
            ]
        elif platform.lower() == "tiktok":
            content_data["platform_tips"] = [
                "Focus on video content",
                "Use trending sounds and effects",
                "Hook viewers in first 3 seconds",
                "Post when your audience is most active"
            ]
        elif platform.lower() == "linkedin":
            content_data["platform_tips"] = [
                "Professional tone and content",
                "Share industry insights",
                "Use professional headshots",
                "Post during business hours on weekdays"
            ]
        
        return content_data

