# DUPIC - AI-Powered Social Media Manager 2050

## 🚀 Project Overview

DUPIC is a next-generation AI-powered social media management platform featuring a futuristic 2050-style UI design and comprehensive AI integration. This upgraded version includes multiple AI providers, advanced analytics, and machine learning services for trend analysis.

**STATUS: ✅ COMPLETE** - [Documentation](docs/)

## ✨ Key Features

### 🎨 2050-Style UI Design
- **Holographic Text Effects**: Glowing, animated text with cyberpunk aesthetics
- **Glassmorphism**: Translucent glass-like components with backdrop blur
- **Neon Accents**: Vibrant cyan, purple, and pink color schemes
- **Particle Effects**: Dynamic floating particles and animated backgrounds
- **Responsive Design**: Optimized for both desktop and mobile devices

### 🤖 Multi-AI Provider Integration
- **OpenAI**: GPT-4, GPT-3.5, DALL-E, Whisper models
- **Groq**: Llama 3.1, Mixtral, Gemma2, Whisper-large-v3 models
- **Google Gemini**: Gemini Pro, Gemini Flash with multimodal capabilities
- **Cerebras**: High-performance Llama models
- **OpenRouter**: Access to Claude, Meta-Llama, and other premium models

### 📊 Advanced Analytics & ML Services
- **Trend Analysis**: Real-time social media trend detection
- **Sentiment Analysis**: AI-powered sentiment scoring
- **Content Optimization**: ML-driven content performance predictions
- **Visual Analysis**: Computer vision for image content analysis
- **Topic Extraction**: Automated topic clustering and categorization

### 🗄️ Database & Storage
- **MongoDB Integration**: Scalable document storage for trends and analytics
- **Fallback Storage**: In-memory storage for development environments
- **Data Models**: Comprehensive schemas for content, users, and analytics

## 🛠️ Technical Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **CSS3**: Advanced styling with custom properties and animations
- **Responsive Design**: Mobile-first approach with flexbox and grid

### Backend
- **Flask**: Python web framework with RESTful API design
- **Flask-CORS**: Cross-origin resource sharing support
- **Python 3.11**: Latest Python features and performance improvements

### AI & ML
- **OpenAI API**: GPT models and multimodal capabilities
- **Groq API**: Ultra-fast inference for Llama and Mixtral models
- **Google Generative AI**: Gemini models for advanced reasoning
- **Scikit-learn**: Machine learning algorithms and data processing
- **Transformers**: Hugging Face models for NLP tasks

### Database & Analytics
- **MongoDB**: Document database for flexible data storage
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations

## 🚀 Installation & Setup

### Prerequisites
- Node.js 20.x or higher
- Python 3.11 or higher
- MongoDB (optional, fallback storage available)

### Frontend Setup
```bash
cd social-media-manager-frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd social-media-manager-app
pip install -r requirements.txt
python app.py
```

### Environment Configuration
Create a `.env` file in the backend directory:
```env
# AI API Keys
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Database
MONGODB_URI=mongodb://localhost:27017/

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

## 📱 Application Features

### Dashboard
- Real-time analytics overview
- Engagement metrics visualization
- Trending content display
- Performance indicators

### AI Configuration
- Multi-provider AI model management
- API key configuration interface
- Model capability overview
- System status monitoring

### Content Analysis
- Sentiment analysis for social media posts
- Topic extraction and categorization
- Visual content analysis
- Engagement prediction

### Trends Monitoring
- Real-time trend detection
- Hashtag performance tracking
- Platform-specific analytics
- Content recommendation engine

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/health` - System health check
- `GET /api/providers` - Available AI providers
- `GET /api/providers/{provider}/models` - Provider-specific models

### Analytics Endpoints
- `GET /api/trends` - Trending content data
- `GET /api/trends/hashtags` - Trending hashtags
- `GET /api/analytics/summary` - Analytics overview
- `GET /api/analytics/posting-times` - Optimal posting times

### AI Processing Endpoints
- `POST /api/ai/generate` - Text generation
- `POST /api/ai/transcribe` - Audio transcription
- `POST /api/ai/analyze-image` - Image analysis
- `POST /api/content/analyze` - Content analysis

## 🎨 Design System

### Color Palette
- **Primary**: Cyan (#00FFFF) - Holographic blue
- **Secondary**: Purple (#8B5CF6) - Deep purple accents
- **Accent**: Pink (#EC4899) - Vibrant highlights
- **Background**: Dark gradients with transparency
- **Text**: White with glow effects

### Typography
- **Primary Font**: 'Orbitron' - Futuristic, tech-inspired
- **Secondary Font**: 'Inter' - Clean, readable interface text
- **Monospace**: 'JetBrains Mono' - Code and data display

### Components
- **Glass Cards**: Translucent containers with backdrop blur
- **Neon Buttons**: Glowing interactive elements
- **Holographic Text**: Animated text with shadow effects
- **Particle Systems**: Dynamic background animations

## 📋 Project Progress

This project is now complete with all core functionality implemented. For detailed progress tracking, see the [documentation directory](docs/):

- [Project Management](docs/project-management/) - Completion reports and progress tracking
- [Technical Documentation](docs/technical/) - Architecture and implementation details
- [API Documentation](docs/api/) - API endpoints and usage
- [User Guides](docs/user-guides/) - Tutorials and user manuals

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request
5. Code review and merge

### Code Standards
- **ESLint**: JavaScript/React linting
- **Prettier**: Code formatting
- **Black**: Python code formatting
- **Type Hints**: Python type annotations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI**: GPT models and API infrastructure
- **Groq**: Ultra-fast inference capabilities
- **Google**: Gemini AI models and services
- **Hugging Face**: Transformers and model hub
- **React Community**: Component libraries and tools

## 📞 Support

For support and questions:
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Comprehensive API and component docs
- **Community**: Join our Discord server for discussions

---

**Built with ❤️ for the future of social media management**
