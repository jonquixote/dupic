# AI Social Media Manager Upgrade Plan

**STATUS: SUBSTANTIALLY COMPLETE**
See [Final Progress Report](final_progress_report.md) for current status

## Phase 3: Design Enhanced Architecture and Features

### 3.1. Data Model and API Endpoint Design

#### 3.1.1. AI API Configuration Management
- **Model**: `AIProviderConfig`
  - `id` (PK)
  - `user_id` (FK to User)
  - `provider_name` (e.g., "OpenAI", "Google AI Studio")
  - `api_key` (encrypted string)
  - `default_model_text` (e.g., "gpt-4o", "gemini-1.5-flash")
  - `default_model_speech_to_text` (e.g., "whisper-1", "gemini-1.5-flash")
  - `default_model_vision_to_text` (e.g., "gpt-4o-vision", "gemini-1.5-flash")
  - `is_default` (boolean, only one per user/admin can be default)
- **API Endpoints**: ✅ IMPLEMENTED
  - `POST /api/ai_configs`: Add new AI provider configuration.
  - `GET /api/ai_configs`: Get all AI provider configurations for the current user/admin.
  - `PUT /api/ai_configs/<id>`: Update an AI provider configuration.
  - `DELETE /api/ai_configs/<id>`: Delete an AI provider configuration.
  - `POST /api/ai_configs/set_default/<id>`: Set a specific configuration as default.

#### 3.1.2. Enhanced Character Profiles
- **Model**: `CharacterProfile` (existing, but add fields)
  - `dialogue_style` (text)
  - `visual_wardrobe` (text - description or JSON list of items)
  - `visual_props` (text - description or JSON list of items)
  - `visual_background` (text - description or JSON list of items)
  - `target_audience` (text)
  - `tone` (text)
  - `niche` (text)
- **API Endpoints**: ✅ IMPLEMENTED
  - `PUT /api/characters/<id>`: Update character profile with new fields.

#### 3.1.3. Content Analysis Results (New Models)
- **Model**: `VideoAnalysis`
  - `id` (PK)
  - `post_id` (FK to SocialMediaPost - new model or existing if applicable)
  - `video_url` (string)
  - `transcription_text` (text)
  - `visual_description` (text)
  - `analysis_date` (datetime)
  - `provider_config_id` (FK to AIProviderConfig - which config was used for analysis)
- **API Endpoints**: ✅ IMPLEMENTED
  - `POST /api/analyze_video`: Trigger video analysis (transcription, vision-to-text).
  - `GET /api/analyze_video/<post_id>`: Retrieve analysis results for a post.

#### 3.1.4. User Specific Analytics and Favorites (New Models)
- **Model**: `UserAnalytics`
  - `id` (PK)
  - `user_id` (FK to User)
  - `metric_name` (e.g., "engagement_rate", "follower_growth")
  - `value` (float)
  - `timestamp` (datetime)
- **Model**: `FavoriteContent`
  - `id` (PK)
  - `user_id` (FK to User)
  - `content_id` (FK to SocialMediaPost or GeneratedContent)
  - `saved_date` (datetime)
- **API Endpoints**: ✅ IMPLEMENTED
  - `GET /api/user_analytics`: Retrieve user-specific analytics.
  - `POST /api/favorite_content`: Add content to user favorites.
  - `GET /api/favorite_content`: Retrieve user

