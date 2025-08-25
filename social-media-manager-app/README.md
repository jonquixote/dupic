# AI Social Media Manager

A next-generation AI-powered social media management platform with multi-AI provider integration and advanced analytics.

## Features Implemented

- Multi-AI provider support (OpenAI, Google AI, Anthropic, Azure OpenAI)
- Content generation with variations and hashtag suggestions
- Trend analysis with real Twitter integration
- Video analysis with transcription and visual description
- Character profile management
- User analytics and favorites tracking

## Prerequisites

- Python 3.10+
- Node.js 16+
- Virtual environment (recommended)

## Backend Setup

1. Navigate to the backend directory:
   ```
   cd social-media-manager-app
   ```

2. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```
   # AI API Keys (add your own keys)
   OPENAI_API_KEY=your_openai_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_VERSION=your_azure_api_version
   
   # Social Media API Keys
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here
   ```

5. Run the application:
   ```
   python app.py
   ```

The backend will be available at `http://localhost:5000`

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd social-media-manager-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### Core Endpoints
- `GET /api/health` - System health check
- `GET /api/providers` - Available AI providers

### Content Generation
- `POST /api/content/generate` - Generate content
- `POST /api/content/generate/variations` - Generate content variations
- `POST /api/content/hashtags` - Generate hashtags
- `POST /api/content/optimize` - Optimize content

### Trend Analysis
- `GET /api/trends` - Get stored trends
- `GET /api/trends/top` - Get top trends
- `POST /api/trends/refresh` - Refresh trends
- `POST /api/trends/analyze` - Analyze new trends

### Character Profiles
- `GET /api/characters` - Get character profiles
- `POST /api/characters` - Create character profile
- `PUT /api/characters/<id>` - Update character profile
- `DELETE /api/characters/<id>` - Delete character profile
- `GET /api/characters/templates` - Get character templates

### Video Analysis
- `POST /api/analyze_video` - Analyze video from URL
- `GET /api/analyze_video/<post_id>` - Get video analysis results

### User Analytics
- `GET /api/user_analytics` - Get user analytics
- `POST /api/user_analytics` - Create user analytic record
- `GET /api/user_analytics/summary` - Get analytics summary

### Favorites
- `GET /api/favorite_content` - Get user favorites
- `POST /api/favorite_content` - Add to favorites
- `DELETE /api/favorite_content/<id>` - Remove from favorites

## Development Progress

This project has completed all Priority 1 and Priority 2 tasks, with partial completion of Priority 3 tasks. See `tasks.md` for detailed progress tracking and `completion_summary.md` for a comprehensive overview.