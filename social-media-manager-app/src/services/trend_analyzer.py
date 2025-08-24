import json
import random
from datetime import datetime, timedelta
from src.models import Trend, ContentRecommendation, CharacterProfile, db, User

class TrendAnalyzer:
    """Service for analyzing social media trends and generating content recommendations"""
    
    def __init__(self):
        self.platforms = ['twitter', 'instagram', 'tiktok', 'facebook']
        self.categories = ['technology', 'entertainment', 'lifestyle', 'business', 'sports', 'news']
    
    def fetch_and_analyze_trends(self):
        """Fetch trends from various sources and analyze them"""
        new_trends = []
        
        # Since we don't have access to real APIs in this demo, we'll simulate trend data
        # In a real implementation, this would call actual social media APIs
        
        simulated_trends = self._generate_simulated_trends()
        
        for trend_data in simulated_trends:
            # Check if trend already exists
            existing_trend = Trend.query.filter_by(
                keyword=trend_data['keyword'],
                platform=trend_data['platform']
            ).first()
            
            if existing_trend:
                # Update existing trend
                existing_trend.engagement_score = trend_data['engagement_score']
                existing_trend.volume = trend_data['volume']
                existing_trend.growth_rate = trend_data['growth_rate']
                existing_trend.updated_at = datetime.utcnow()
                new_trends.append(existing_trend)
            else:
                # Create new trend
                trend = Trend(
                    keyword=trend_data['keyword'],
                    platform=trend_data['platform'],
                    engagement_score=trend_data['engagement_score'],
                    volume=trend_data['volume'],
                    growth_rate=trend_data['growth_rate'],
                    sentiment=trend_data['sentiment'],
                    category=trend_data['category'],
                    hashtags=json.dumps(trend_data['hashtags'])
                )
                db.session.add(trend)
                new_trends.append(trend)
        
        db.session.commit()
        return new_trends
    
    def _generate_simulated_trends(self):
        """Generate simulated trend data for demonstration purposes"""
        trending_keywords = [
            'AI Revolution', 'Sustainable Living', 'Remote Work', 'Digital Art', 'Crypto News',
            'Fitness Journey', 'Mental Health', 'Climate Change', 'Space Exploration', 'Food Trends',
            'Gaming Updates', 'Fashion Week', 'Travel Tips', 'Tech Innovation', 'Music Festival',
            'Movie Reviews', 'Book Recommendations', 'Startup Life', 'Photography Tips', 'Cooking Hacks'
        ]
        
        trends = []
        
        for _ in range(50):  # Generate 50 random trends
            keyword = random.choice(trending_keywords)
            platform = random.choice(self.platforms)
            category = random.choice(self.categories)
            
            # Generate realistic metrics
            engagement_score = round(random.uniform(0.1, 10.0), 2)
            volume = random.randint(100, 100000)
            growth_rate = round(random.uniform(-50.0, 200.0), 2)
            sentiment = random.choice(['positive', 'negative', 'neutral'])
            
            # Generate related hashtags
            hashtags = [
                f"#{keyword.replace(' ', '').lower()}",
                f"#{category}",
                f"#{platform}trending",
                f"#viral{random.randint(1, 100)}"
            ]
            
            trends.append({
                'keyword': keyword,
                'platform': platform,
                'engagement_score': engagement_score,
                'volume': volume,
                'growth_rate': growth_rate,
                'sentiment': sentiment,
                'category': category,
                'hashtags': hashtags
            })
        
        return trends
    
    def generate_recommendations(self, user_id):
        """Generate content recommendations for a specific user"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Get user's character profiles
        character_profiles = CharacterProfile.query.filter_by(user_id=user_id).all()
        
        # Get top trending topics
        top_trends = Trend.query.order_by(
            Trend.engagement_score.desc()
        ).limit(20).all()
        
        recommendations = []
        
        for trend in top_trends:
            for character in character_profiles:
                # Check if trend matches character's interests
                if self._is_trend_relevant(trend, character):
                    recommendation = self._create_recommendation(user_id, trend, character)
                    recommendations.append(recommendation)
        
        # If no character profiles, create generic recommendations
        if not character_profiles and top_trends:
            for trend in top_trends[:5]:
                recommendation = self._create_generic_recommendation(user_id, trend)
                recommendations.append(recommendation)
        
        db.session.commit()
        return recommendations
    
    def _is_trend_relevant(self, trend, character):
        """Check if a trend is relevant to a character profile"""
        # Parse character keywords
        try:
            character_keywords = json.loads(character.keywords) if character.keywords else []
        except (json.JSONDecodeError, TypeError):
            character_keywords = []
        
        # Parse character platforms
        try:
            character_platforms = json.loads(character.preferred_platforms) if character.preferred_platforms else []
        except (json.JSONDecodeError, TypeError):
            character_platforms = []
        
        # Check platform match
        if character_platforms and trend.platform not in character_platforms:
            return False
        
        # Check keyword relevance
        trend_keywords = trend.keyword.lower().split()
        for keyword in character_keywords:
            if keyword.lower() in trend.keyword.lower():
                return True
        
        # Check category relevance
        if character.content_style and character.content_style.lower() in trend.category.lower():
            return True
        
        return random.random() > 0.7  # 30% chance for serendipitous recommendations
    
    def _create_recommendation(self, user_id, trend, character):
        """Create a content recommendation based on trend and character"""
        # Determine content type based on platform and character
        content_types = {
            'twitter': ['post', 'thread'],
            'instagram': ['post', 'story', 'reel'],
            'tiktok': ['video', 'story'],
            'facebook': ['post', 'story']
        }
        
        content_type = random.choice(content_types.get(trend.platform, ['post']))
        
        # Calculate confidence score
        confidence_score = min(trend.engagement_score / 10.0, 1.0)
        
        # Generate hashtag suggestions
        hashtag_suggestions = self._generate_hashtag_suggestions(trend, character)
        
        # Generate content suggestions
        content_suggestions = self._generate_content_suggestions(trend, character, content_type)
        
        # Calculate optimal posting time (simulate based on platform)
        recommended_time = self._calculate_optimal_time(trend.platform)
        
        recommendation = ContentRecommendation(
            user_id=user_id,
            trend_id=trend.id,
            content_type=content_type,
            recommended_time=recommended_time,
            confidence_score=confidence_score,
            hashtag_suggestions=json.dumps(hashtag_suggestions),
            content_suggestions=json.dumps(content_suggestions)
        )
        
        db.session.add(recommendation)
        return recommendation
    
    def _create_generic_recommendation(self, user_id, trend):
        """Create a generic recommendation without character profile"""
        content_types = ['post', 'story']
        content_type = random.choice(content_types)
        
        confidence_score = min(trend.engagement_score / 10.0, 1.0)
        
        hashtag_suggestions = json.loads(trend.hashtags) if trend.hashtags else []
        content_suggestions = [
            f"Share your thoughts on {trend.keyword}",
            f"What's your take on the {trend.keyword} trend?",
            f"Join the conversation about {trend.keyword}"
        ]
        
        recommended_time = self._calculate_optimal_time(trend.platform)
        
        recommendation = ContentRecommendation(
            user_id=user_id,
            trend_id=trend.id,
            content_type=content_type,
            recommended_time=recommended_time,
            confidence_score=confidence_score,
            hashtag_suggestions=json.dumps(hashtag_suggestions),
            content_suggestions=json.dumps(content_suggestions)
        )
        
        db.session.add(recommendation)
        return recommendation
    
    def _generate_hashtag_suggestions(self, trend, character):
        """Generate hashtag suggestions based on trend and character"""
        hashtags = []
        
        # Add trend hashtags
        try:
            trend_hashtags = json.loads(trend.hashtags) if trend.hashtags else []
            hashtags.extend(trend_hashtags)
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Add character-specific hashtags
        try:
            character_keywords = json.loads(character.keywords) if character.keywords else []
            for keyword in character_keywords:
                hashtags.append(f"#{keyword.replace(' ', '').lower()}")
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Add platform-specific hashtags
        platform_hashtags = {
            'twitter': ['#TwitterTrends', '#Viral'],
            'instagram': ['#InstaGood', '#Trending'],
            'tiktok': ['#ForYou', '#Viral'],
            'facebook': ['#Trending', '#Social']
        }
        
        hashtags.extend(platform_hashtags.get(trend.platform, []))
        
        return list(set(hashtags))[:10]  # Remove duplicates and limit to 10
    
    def _generate_content_suggestions(self, trend, character, content_type):
        """Generate content suggestions based on trend, character, and content type"""
        suggestions = []
        
        tone_templates = {
            'professional': [
                f"Industry insights on {trend.keyword}: What this means for businesses",
                f"Professional perspective on the {trend.keyword} trend",
                f"How {trend.keyword} is reshaping our industry"
            ],
            'casual': [
                f"Just discovered {trend.keyword} and I'm obsessed! 😍",
                f"Anyone else following the {trend.keyword} trend?",
                f"My take on {trend.keyword} - what do you think?"
            ],
            'humorous': [
                f"When everyone's talking about {trend.keyword} but you're still confused 😂",
                f"Me trying to understand the {trend.keyword} hype",
                f"Plot twist: {trend.keyword} is actually..."
            ],
            'educational': [
                f"Everything you need to know about {trend.keyword}",
                f"Breaking down the {trend.keyword} phenomenon",
                f"5 key facts about {trend.keyword} you should know"
            ]
        }
        
        tone = character.tone if character.tone in tone_templates else 'casual'
        suggestions.extend(tone_templates[tone])
        
        # Add content type specific suggestions
        if content_type == 'video':
            suggestions.extend([
                f"Behind the scenes: My experience with {trend.keyword}",
                f"Quick tutorial on {trend.keyword}",
                f"Reacting to the {trend.keyword} trend"
            ])
        elif content_type == 'story':
            suggestions.extend([
                f"Quick thoughts on {trend.keyword}",
                f"Poll: What's your opinion on {trend.keyword}?",
                f"Swipe up to learn more about {trend.keyword}"
            ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _calculate_optimal_time(self, platform):
        """Calculate optimal posting time based on platform"""
        # Simulate optimal posting times based on general best practices
        optimal_times = {
            'twitter': [9, 12, 15, 18],  # 9am, 12pm, 3pm, 6pm
            'instagram': [11, 13, 17, 19],  # 11am, 1pm, 5pm, 7pm
            'tiktok': [6, 10, 19, 21],  # 6am, 10am, 7pm, 9pm
            'facebook': [9, 13, 15]  # 9am, 1pm, 3pm
        }
        
        hours = optimal_times.get(platform, [12, 15, 18])
        optimal_hour = random.choice(hours)
        
        # Calculate next occurrence of this hour
        now = datetime.utcnow()
        recommended_time = now.replace(hour=optimal_hour, minute=0, second=0, microsecond=0)
        
        # If the time has passed today, schedule for tomorrow
        if recommended_time <= now:
            recommended_time += timedelta(days=1)
        
        return recommended_time