# AI Social Media Manager - Frontend Documentation

## Overview

The AI Social Media Manager frontend is a React application built with modern UI components and cyberpunk-inspired styling. It provides a comprehensive dashboard for managing AI-powered social media content creation, trend analysis, and performance analytics.

## Navigation Structure

The application uses a sidebar navigation with the following primary pages:

1. **Dashboard** - Overview of key metrics and quick actions
2. **Trends** - Trend analysis and visualization tools
3. **Content Generator** - AI-powered content creation interface
4. **Character Profiles** - Management of AI personas for content generation
5. **Video Analysis** - Tools for analyzing video content
6. **Analytics** - Detailed performance metrics and insights
7. **AI Configuration** - Management of AI provider settings and API keys
8. **Settings** - General application configuration

## Page-by-Page Analysis

### 1. Dashboard (`/`)

#### Elements:
- **Header Section**
  - Page title: "Neural Dashboard"
  - Subtitle: "Welcome back! Here's what's happening in your digital realm."
  - "Generate Content" button with Sparkles icon

- **Stats Cards** (4 cards in a grid)
  - Total Followers card (Users icon)
  - Engagement Rate card (Heart icon)
  - Reach card (TrendingUp icon)
  - Shares card (Share icon)

- **Trending Topics Section**
  - Section title: "Trending Neural Patterns"
  - Status indicator: "Live Analysis"
  - List of trending topics with engagement scores and growth rates

- **Performance Chart**
  - Section title: "Neural Activity"
  - Status indicator: "Processing"
  - Line chart showing engagement and reach over 7 days

- **Quick Actions Section**
  - Section title: "Neural Commands"
  - "Analyze Trends" button (TrendingUp icon)
  - "Generate Content" button (Sparkles icon)
  - "View Analytics" button (Users icon)

### 2. Trends (`/trends`)

#### Elements:
- **Header Section**
  - Page title: "Trend Analysis"
  - Subtitle: "Discover viral content opportunities across social platforms"
  - "Refresh Trends" button with RefreshCw icon

- **Filters Section**
  - Search input with Search icon
  - Platform selector (All Platforms, Twitter, Instagram, TikTok, Facebook)
  - Category selector (All Categories, Technology, Lifestyle, Business, Entertainment, Sports, News)

- **Tabs Navigation**
  - "Trending Topics" tab
  - "Platform Analytics" tab
  - "AI Insights" tab

- **Trending Topics Tab Content**
  - Grid of trend cards showing:
    - Keyword
    - Platform badge
    - Category badge
    - Engagement score
    - Volume count
    - Growth rate with directional indicator
    - Sentiment badge

- **Platform Analytics Tab Content**
  - Bar chart: "Trends by Platform"
  - Pie chart: "Platform Distribution"

- **AI Insights Tab Content**
  - "Opportunity Alert" recommendation card
  - "Growth Trend" recommendation card
  - "Platform Insight" recommendation card

### 3. Content Generator (`/content`)

#### Elements:
- **Header Section**
  - Page title: "Content Generator"
  - Subtitle: "Create AI-powered content based on trending topics and your brand voice"
  - "Generate Content" button with Sparkles/RefreshCw icon

- **Input Panel** (Left side)
  - **Content Settings Card**
    - "Select Trending Topic" dropdown
    - "Character Profile" dropdown
    - Platform selector (Twitter, Instagram, TikTok, Facebook, LinkedIn)
    - Content Type selector (Post, Story, Reel, Video, Thread)
    - "Additional Context" textarea

  - **Character Profiles Management Card**
    - "Character Profiles" title with User icon
    - List of character profiles with Edit buttons
    - "Add New Profile" button

- **Output Panel** (Right side)
  - **Generated Content Card**
    - "Generated Content" title with Wand2 icon
    - Empty state with Sparkles icon when no content
    - Generated content display with:
      - Content text
      - Hashtags list
      - Call to action
      - Platform notes
    - Copy to clipboard button

  - **Content Templates Card**
    - "Content Templates" title
    - "Question Post" template button
    - "How-To Guide" template button
    - "Behind the Scenes" template button

### 4. Character Profiles (`/characters`)

#### Elements:
- **Header Section**
  - Page title: "Character Profiles"
  - Subtitle: "Create and manage AI personas for content generation"
  - "Create Character" button with Plus icon

- **Create Character Dialog**
  - "Create New Character Profile" title
  - Template selection (Professional Brand, Lifestyle Influencer)
  - Character Name input
  - Tone selector (Professional, Casual, Humorous, Informative, Inspiring, Motivational)
  - Description textarea
  - Target Audience input
  - Content Style input
  - Dialogue Style textarea
  - Visual Identity section with:
    - Wardrobe Style input
    - Props & Accessories input
    - Background Settings input
  - "Cancel" and "Create Character" buttons

- **Character Grid**
  - Character cards showing:
    - Avatar with User icon
    - Character name and tone
    - Description
    - Target audience and content style
    - Visual style preview
    - Edit and Delete buttons
    - "Generate" button with Sparkles icon

### 5. Video Analysis (`/video-analysis`)

*Note: This component was not provided in the files examined*

### 6. Analytics (`/analytics`)

#### Elements:
- **Header Section**
  - Page title: "AI Analytics Dashboard"
  - Subtitle: "Advanced insights powered by artificial intelligence"
  - "Live Data" indicator with Activity icon
  - Time range selector (Last 24 hours, Last 7 days, Last 30 days, Last 3 months)
  - "Export Report" button with Download icon

- **Real-time Stats** (4 cards in a grid)
  - Total Engagement card (Heart icon)
  - AI-Optimized Reach card (Brain icon)
  - Active Followers card (Users icon)
  - Viral Content card (Zap icon)

- **AI Insights Panel**
  - "AI Performance Insights" title with Brain icon
  - Real-time engagement and trend indicators
  - AI metrics with progress bars:
    - Content Quality
    - Trend Alignment
    - Audience Match
    - Engagement Prediction
    - Viral Potential
    - Brand Consistency

- **Tabs Navigation**
  - "Overview" tab
  - "Platforms" tab
  - "Content AI" tab
  - "AI Predictions" tab

- **Overview Tab Content**
  - Engagement Trends area chart
  - Multi-Metric Analysis line chart
  - Engagement Breakdown bar chart

- **Platforms Tab Content**
  - Platform Performance bar chart
  - Reach Distribution pie chart
  - Platform Comparison list

- **Content AI Tab Content**
  - "AI-Powered Content Analysis" title with Brain icon
  - Content performance list with:
    - Content title
    - Platform badge
    - Engagement percentage
    - AI Score
    - Trend Score
    - Metrics (likes, views, shares)

- **AI Predictions Tab Content**
  - Performance Radar chart
  - "AI Recommendations" section with:
    - Content Optimization recommendation
    - Optimal Timing recommendation
    - Trend Alert recommendation
    - Audience Insight recommendation

### 7. AI Configuration (`/ai-config`)

#### Elements:
- **Header Section**
  - Page title: "AI Configurations"
  - Subtitle: "Manage your AI provider settings and API keys"
  - "+ Add Provider" button

- **Providers Grid**
  - Provider cards showing:
    - Provider icon (🤖, ⚡, 💎, etc.)
    - Provider name
    - Status badge (Online/Offline)
    - Model count
    - Configure and Test buttons

- **Models Section**
  - "Available Models" title with provider name
  - Model cards showing:
    - Model name
    - Token count
    - Capabilities badges
    - Select and Test buttons

- **API Keys Management Section**
  - "API Keys Management" title
  - API key items showing:
    - Provider icon and name
    - Status indicator
    - API key input field (password type)
    - "Update" button

- **System Status Section**
  - "System Status" title
  - Status items:
    - AI System: Online
    - Database: Connected
    - ML Services: Initialized
    - Performance: 85%

### 8. Settings (`/settings`)

*Note: This component was not provided in the files examined*

## UI Components and Styling

The application uses a cyberpunk-inspired design system with:

- **Glassmorphism** effects (frosted glass appearance)
- **Neon accents** and glowing elements
- **Gradient backgrounds** and text effects
- **Animated particles** and scan lines
- **Responsive grid layouts** that adapt to different screen sizes
- **Dark theme** with blue/purple accent colors

## API Integration

The frontend communicates with the backend API through the `apiService` class which handles:

- Base URL configuration (`http://localhost:5000/api`)
- HTTP request management with error handling
- JSON serialization/deserialization
- Authentication headers (when implemented)

## Responsive Design

The application is designed to be responsive with:

- Mobile-first layout principles
- Flexible grid systems that adapt to screen size
- Collapsible sidebar navigation
- Responsive charts that resize with container
- Touch-friendly button sizes and spacing

## Performance Considerations

- Lazy loading of components where applicable
- Efficient state management with React hooks
- Optimized rendering with memoization
- Loading states and skeleton screens for async operations
- Error boundaries for graceful error handling