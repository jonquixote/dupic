import json
import asyncio
from src.models import CharacterProfile, Trend
from typing import Dict, List, Optional
from src.ai_providers import ai_manager, AIProvider

class ContentGenerator:
    """Service for generating AI-powered social media content"""
    
    def __init__(self, provider: AIProvider, model: str):
        """
        Initialize the ContentGenerator with a specific AI provider and model.

        :param provider: The AIProvider enum member (e.g., AIProvider.OPENAI).
        :param model: The name of the model to use for generation (e.g., "gpt-4o-mini").
        """
        self.provider = provider
        self.model = model
        self.ai_manager = ai_manager
    
    async def generate_content(self, 
                        trend: Trend, 
                        character: CharacterProfile, 
                        content_type: str = 'post',
                        platform: str = 'twitter',
                        additional_context: str = '') -> Dict:
        """Generate content based on trend, character profile, and specifications"""
        
        # Build the prompt
        prompt = self._build_content_prompt(trend, character, content_type, platform, additional_context)
        
        try:
            # Determine the litellm model string
            model_string = f"{self.provider.value}/{self.model}" if self.provider != AIProvider.OPENAI else self.model

            response = await self.ai_manager.generate_text(
                model_name=model_string,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response['content'].strip()
            
            # Parse the response and format it
            return self._format_generated_content(content, content_type, platform)
            
        except Exception as e:
            return {
                'error': f'Failed to generate content with {self.provider.value}/{self.model}: {str(e)}',
                'content': '',
                'hashtags': [],
                'call_to_action': ''
            }
    
    async def generate_multiple_variations(self,
                                   trend: Trend,
                                   character: CharacterProfile,
                                   content_type: str = 'post',
                                   platform: str = 'twitter',
                                   count: int = 3) -> List[Dict]:
        """Generate multiple content variations concurrently"""
        
        tasks = []
        for i in range(count):
            # Add variation context to make each generation unique
            variation_context = f"Variation {i+1}: Create a unique approach to this content."
            tasks.append(
                self.generate_content(trend, character, content_type, platform, variation_context)
            )
        
        variations = await asyncio.gather(*tasks)
        return variations
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for content generation"""
        return """You are an expert social media content creator and strategist. Your job is to create engaging, platform-appropriate content that aligns with current trends and the user's character profile.

Guidelines:
- Create content that is authentic and matches the specified tone
- Include relevant hashtags (3-8 hashtags)
- Add a clear call-to-action when appropriate
- Ensure content is optimized for the specified platform
- Keep content within platform character limits
- Make content engaging and likely to drive interaction

Format your response as JSON with the following structure:
{
    "content": "The main content text",
    "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"],
    "call_to_action": "Specific call to action",
    "platform_notes": "Any platform-specific considerations"
}"""
    
    def _build_content_prompt(self,
                            trend: Trend,
                            character: CharacterProfile,
                            content_type: str,
                            platform: str,
                            additional_context: str) -> str:
        """Build the content generation prompt"""
        
        # Parse character keywords and platforms
        try:
            character_keywords = json.loads(character.keywords) if character.keywords else []
            character_platforms = json.loads(character.preferred_platforms) if character.preferred_platforms else []
        except (json.JSONDecodeError, TypeError):
            character_keywords = []
            character_platforms = []
        
        # Parse trend hashtags
        try:
            trend_hashtags = json.loads(trend.hashtags) if trend.hashtags else []
        except (json.JSONDecodeError, TypeError):
            trend_hashtags = []
        
        prompt = f"""Create a {content_type} for {platform} based on the following:

TRENDING TOPIC:
- Keyword: {trend.keyword}
- Platform: {trend.platform}
- Category: {trend.category}
- Engagement Score: {trend.engagement_score}/10
- Sentiment: {trend.sentiment}
- Related Hashtags: {', '.join(trend_hashtags)}

CHARACTER PROFILE:
- Name: {character.name}
- Description: {character.description}
- Tone: {character.tone}
- Target Audience: {character.target_audience}
- Content Style: {character.content_style}
- Keywords: {', '.join(character_keywords)}
- Preferred Platforms: {', '.join(character_platforms)}

CONTENT SPECIFICATIONS:
- Content Type: {content_type}
- Target Platform: {platform}
- Character Limit: {self._get_character_limit(platform, content_type)}

{additional_context}

Create engaging content that:
1. Incorporates the trending topic naturally
2. Matches the character's tone and style
3. Appeals to the target audience
4. Is optimized for {platform}
5. Includes relevant hashtags
6. Has a clear call-to-action

Respond in JSON format only."""
        
        return prompt
    
    def _get_character_limit(self, platform: str, content_type: str) -> str:
        """Get character limits for different platforms and content types"""
        limits = {
            'twitter': {
                'post': '280 characters',
                'thread': '280 characters per tweet'
            },
            'instagram': {
                'post': '2,200 characters',
                'story': '2,200 characters',
                'reel': '2,200 characters'
            },
            'tiktok': {
                'video': '4,000 characters',
                'story': '150 characters'
            },
            'facebook': {
                'post': '63,206 characters (but aim for 40-80 characters for best engagement)',
                'story': '2,200 characters'
            },
            'linkedin': {
                'post': '3,000 characters',
                'article': '125,000 characters'
            }
        }
        
        return limits.get(platform, {}).get(content_type, '280 characters')
    
    def _format_generated_content(self, content: str, content_type: str, platform: str) -> Dict:
        """Format the generated content response"""
        try:
            # Try to parse as JSON first
            parsed_content = json.loads(content)
            return {
                'content': parsed_content.get('content', ''),
                'hashtags': parsed_content.get('hashtags', []),
                'call_to_action': parsed_content.get('call_to_action', ''),
                'platform_notes': parsed_content.get('platform_notes', ''),
                'content_type': content_type,
                'platform': platform
            }
        except json.JSONDecodeError:
            # If not valid JSON, treat as plain text
            lines = content.split('\n')
            main_content = lines[0] if lines else content
            
            # Extract hashtags from content
            hashtags = [word for word in main_content.split() if word.startswith('#')]
            
            # Remove hashtags from main content for cleaner presentation
            clean_content = ' '.join([word for word in main_content.split() if not word.startswith('#')])
            
            return {
                'content': clean_content,
                'hashtags': hashtags,
                'call_to_action': '',
                'platform_notes': '',
                'content_type': content_type,
                'platform': platform
            }
    
    async def generate_hashtags(self, trend: Trend, character: CharacterProfile, count: int = 8) -> List[str]:
        """Generate relevant hashtags for a trend and character"""
        
        prompt = f"""Generate {count} relevant hashtags for a social media post about "{trend.keyword}" 
        in the {trend.category} category, targeting {character.target_audience} with a {character.tone} tone.
        
        Return only the hashtags, one per line, starting with #."""
        
        try:
            # Determine the litellm model string
            model_string = f"{self.provider.value}/{self.model}" if self.provider != AIProvider.OPENAI else self.model
            
            response = await self.ai_manager.generate_text(
                model_name=model_string,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            hashtags = [line.strip() for line in response['content'].strip().split('\n') 
                       if line.strip().startswith('#')]
            
            return hashtags[:count]
            
        except Exception as e:
            # Fallback to basic hashtag generation
            return [
                f"#{trend.keyword.replace(' ', '').lower()}",
                f"#{trend.category}",
                f"#{character.tone}",
                "#trending",
                "#viral"
            ]
    
    def optimize_for_platform(self, content: str, platform: str) -> str:
        """Optimize content for specific platform requirements"""
        platform_optimizations = {
            'twitter': self._optimize_for_twitter,
            'instagram': self._optimize_for_instagram,
            'tiktok': self._optimize_for_tiktok,
            'facebook': self._optimize_for_facebook,
            'linkedin': self._optimize_for_linkedin
        }
        
        optimizer = platform_optimizations.get(platform, lambda x: x)
        return optimizer(content)
    
    def _optimize_for_twitter(self, content: str) -> str:
        """Optimize content for Twitter"""
        if len(content) > 280:
            # Truncate and add ellipsis
            return content[:277] + "..."
        return content
    
    def _optimize_for_instagram(self, content: str) -> str:
        """Optimize content for Instagram"""
        # Instagram allows longer content, but first 125 characters are most important
        return content
    
    def _optimize_for_tiktok(self, content: str) -> str:
        """Optimize content for TikTok"""
        # TikTok content should be engaging and trend-focused
        return content
    
    def _optimize_for_facebook(self, content: str) -> str:
        """Optimize content for Facebook"""
        # Facebook favors shorter posts for better engagement
        if len(content) > 80:
            return content[:77] + "..."
        return content
    
    def _optimize_for_linkedin(self, content: str) -> str:
        """Optimize content for LinkedIn"""
        # LinkedIn content should be professional and value-driven
        return content
