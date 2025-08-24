import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Heart, 
  Share, 
  Download, 
  Eye, 
  MessageSquare,
  Target,
  Zap,
  Brain,
  Activity,
  Calendar
} from 'lucide-react'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  AreaChart,
  Area,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts'

const COLORS = ['#00d4ff', '#8b5cf6', '#00ff88', '#ff6b35', '#ff006e', '#ffd700']

const mockEngagementData = [
  { date: '2024-08-16', engagement: 4200, reach: 12400, likes: 1800, shares: 420, comments: 180, views: 8500 },
  { date: '2024-08-17', engagement: 3800, reach: 11200, likes: 1650, shares: 380, comments: 165, views: 7800 },
  { date: '2024-08-18', engagement: 5200, reach: 15800, likes: 2200, shares: 580, comments: 220, views: 11200 },
  { date: '2024-08-19', engagement: 4800, reach: 14200, likes: 2000, shares: 520, comments: 200, views: 10400 },
  { date: '2024-08-20', engagement: 6200, reach: 18500, likes: 2600, shares: 680, comments: 280, views: 13800 },
  { date: '2024-08-21', engagement: 5800, reach: 17200, likes: 2400, shares: 620, comments: 260, views: 12800 },
  { date: '2024-08-22', engagement: 7200, reach: 21500, likes: 3000, shares: 780, comments: 320, views: 16200 },
]

const mockPlatformData = [
  { platform: 'TikTok', posts: 45, engagement: 12.8, reach: 25600, color: '#00d4ff' },
  { platform: 'Instagram', posts: 38, engagement: 9.4, reach: 18900, color: '#8b5cf6' },
  { platform: 'YouTube', posts: 12, engagement: 15.2, reach: 32400, color: '#00ff88' },
  { platform: 'Twitter', posts: 52, engagement: 6.8, reach: 14200, color: '#ff6b35' },
  { platform: 'LinkedIn', posts: 18, engagement: 8.2, reach: 9800, color: '#ff006e' },
]

const mockContentPerformance = [
  { 
    title: 'AI-Powered Content Creation Tips', 
    platform: 'TikTok', 
    engagement: 15.8, 
    likes: 3400, 
    shares: 890, 
    views: 28500,
    aiScore: 92,
    trendingScore: 88
  },
  { 
    title: 'Future of Social Media Marketing', 
    platform: 'YouTube', 
    engagement: 18.2, 
    likes: 2800, 
    shares: 650, 
    views: 45200,
    aiScore: 89,
    trendingScore: 95
  },
  { 
    title: '2050 UI Design Trends', 
    platform: 'Instagram', 
    engagement: 12.4, 
    likes: 2100, 
    shares: 420, 
    views: 18700,
    aiScore: 85,
    trendingScore: 82
  },
  { 
    title: 'Productivity Hacks with AI', 
    platform: 'LinkedIn', 
    engagement: 14.6, 
    likes: 1800, 
    shares: 380, 
    views: 12400,
    aiScore: 91,
    trendingScore: 78
  },
]

const mockAIInsights = [
  { metric: 'Content Quality', score: 88, target: 90 },
  { metric: 'Trend Alignment', score: 92, target: 85 },
  { metric: 'Audience Match', score: 85, target: 88 },
  { metric: 'Engagement Prediction', score: 91, target: 90 },
  { metric: 'Viral Potential', score: 78, target: 80 },
  { metric: 'Brand Consistency', score: 94, target: 90 },
]

export function Analytics() {
  const [timeRange, setTimeRange] = useState('7d')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [realTimeData, setRealTimeData] = useState({
    activeUsers: 1247,
    currentEngagement: 8.4,
    trendsDetected: 12,
    aiRecommendations: 5
  })

  useEffect(() => {
    // Simulate real-time data updates
    const interval = setInterval(() => {
      setRealTimeData(prev => ({
        activeUsers: prev.activeUsers + Math.floor(Math.random() * 20) - 10,
        currentEngagement: Math.max(0, prev.currentEngagement + (Math.random() - 0.5) * 0.5),
        trendsDetected: prev.trendsDetected + Math.floor(Math.random() * 3) - 1,
        aiRecommendations: Math.max(0, prev.aiRecommendations + Math.floor(Math.random() * 2) - 1)
      }))
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const stats = [
    {
      title: 'Total Engagement',
      value: '47.2K',
      change: '+18.4%',
      icon: Heart,
      color: 'text-pink-400',
      bgColor: 'bg-pink-500/20',
      trend: 'up'
    },
    {
      title: 'AI-Optimized Reach',
      value: '284.6K',
      change: '+24.7%',
      icon: Brain,
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/20',
      trend: 'up'
    },
    {
      title: 'Active Followers',
      value: realTimeData.activeUsers.toLocaleString(),
      change: '+12.3%',
      icon: Users,
      color: 'text-green-400',
      bgColor: 'bg-green-500/20',
      trend: 'up'
    },
    {
      title: 'Viral Content',
      value: '8',
      change: '+33.3%',
      icon: Zap,
      color: 'text-yellow-400',
      bgColor: 'bg-yellow-500/20',
      trend: 'up'
    }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="heading-2050 text-3xl">AI Analytics Dashboard</h1>
          <p className="text-gray-400">Advanced insights powered by artificial intelligence</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-green-500/20 border border-green-500/30">
            <Activity className="h-4 w-4 text-green-400 animate-pulse" />
            <span className="text-xs font-medium text-green-400">Live Data</span>
          </div>
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="input-2050 w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="glass-dark border-white/20 text-white">
              <SelectItem value="24h">Last 24 hours</SelectItem>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 3 months</SelectItem>
            </SelectContent>
          </Select>
          <Button className="btn-primary-2050 flex items-center space-x-2">
            <Download className="h-4 w-4" />
            <span>Export Report</span>
          </Button>
        </div>
      </div>

      {/* Real-time Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="card-2050 p-6 relative overflow-hidden">
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-400">{stat.title}</p>
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <div className="flex items-center space-x-1">
                  <TrendingUp className="h-3 w-3 text-green-400" />
                  <span className="text-sm text-green-400 font-medium">{stat.change}</span>
                </div>
              </div>
              <div className={`p-3 rounded-full ${stat.bgColor} ${stat.color} relative`}>
                <stat.icon className="h-6 w-6" />
                <div className="absolute inset-0 rounded-full bg-current opacity-20 animate-pulse"></div>
              </div>
            </div>
            
            {/* Animated background gradient */}
            <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-purple-500 to-cyan-500 opacity-30"></div>
          </div>
        ))}
      </div>

      {/* AI Insights Panel */}
      <div className="card-2050 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
              <Brain className="h-4 w-4 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gradient-blue">AI Performance Insights</h3>
              <p className="text-sm text-gray-400">Real-time AI analysis of your content performance</p>
            </div>
          </div>
          <div className="flex items-center space-x-4 text-sm">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
              <span className="text-gray-400">Current Engagement: </span>
              <span className="text-green-400 font-medium">{realTimeData.currentEngagement.toFixed(1)}%</span>
            </div>
            <div className="flex items-center space-x-2">
              <Target className="h-4 w-4 text-blue-400" />
              <span className="text-gray-400">Trends Detected: </span>
              <span className="text-blue-400 font-medium">{realTimeData.trendsDetected}</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          {mockAIInsights.map((insight, index) => (
            <div key={index} className="bg-white/5 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-300">{insight.metric}</span>
                <span className="text-xs text-gray-500">Target: {insight.target}</span>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-white">{insight.score}</span>
                  <span className={`text-xs ${insight.score >= insight.target ? 'text-green-400' : 'text-yellow-400'}`}>
                    {insight.score >= insight.target ? '✓ On Target' : '⚠ Below Target'}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${
                      insight.score >= insight.target 
                        ? 'bg-gradient-to-r from-green-400 to-blue-400' 
                        : 'bg-gradient-to-r from-yellow-400 to-orange-400'
                    }`}
                    style={{ width: `${Math.min(100, (insight.score / 100) * 100)}%` }}
                  ></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="glass-dark border-white/20">
          <TabsTrigger value="overview" className="data-[state=active]:bg-blue-500/20 data-[state=active]:text-blue-400">
            Overview
          </TabsTrigger>
          <TabsTrigger value="platforms" className="data-[state=active]:bg-purple-500/20 data-[state=active]:text-purple-400">
            Platforms
          </TabsTrigger>
          <TabsTrigger value="content" className="data-[state=active]:bg-green-500/20 data-[state=active]:text-green-400">
            Content AI
          </TabsTrigger>
          <TabsTrigger value="predictions" className="data-[state=active]:bg-yellow-500/20 data-[state=active]:text-yellow-400">
            AI Predictions
          </TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Engagement Trends</h3>
                <Eye className="h-5 w-5 text-blue-400" />
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={mockEngagementData}>
                  <defs>
                    <linearGradient id="engagementGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#00d4ff" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#00d4ff" stopOpacity={0.1}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="date" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                  <Area 
                    type="monotone" 
                    dataKey="engagement" 
                    stroke="#00d4ff" 
                    fill="url(#engagementGradient)"
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Multi-Metric Analysis</h3>
                <BarChart3 className="h-5 w-5 text-purple-400" />
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={mockEngagementData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="date" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                  <Line type="monotone" dataKey="reach" stroke="#00ff88" strokeWidth={2} name="Reach" />
                  <Line type="monotone" dataKey="engagement" stroke="#00d4ff" strokeWidth={2} name="Engagement" />
                  <Line type="monotone" dataKey="views" stroke="#8b5cf6" strokeWidth={2} name="Views" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card-2050 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-white">Engagement Breakdown</h3>
              <MessageSquare className="h-5 w-5 text-green-400" />
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockEngagementData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9CA3AF" />
                <YAxis stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '8px',
                    color: 'white'
                  }} 
                />
                <Bar dataKey="likes" fill="#00d4ff" name="Likes" />
                <Bar dataKey="shares" fill="#00ff88" name="Shares" />
                <Bar dataKey="comments" fill="#8b5cf6" name="Comments" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </TabsContent>

        <TabsContent value="platforms" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Platform Performance</h3>
                <TrendingUp className="h-5 w-5 text-blue-400" />
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={mockPlatformData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="platform" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                  <Bar dataKey="engagement" fill="#00d4ff" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Reach Distribution</h3>
                <Eye className="h-5 w-5 text-purple-400" />
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={mockPlatformData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ platform, reach }) => `${platform}: ${(reach/1000).toFixed(1)}K`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="reach"
                  >
                    {mockPlatformData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card-2050 p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Platform Comparison</h3>
            <div className="space-y-4">
              {mockPlatformData.map((platform, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: platform.color }}
                    ></div>
                    <div>
                      <h4 className="font-medium text-white">{platform.platform}</h4>
                      <p className="text-sm text-gray-400">{platform.posts} posts</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium text-white">{platform.engagement}% engagement</div>
                    <div className="text-sm text-gray-400">{(platform.reach/1000).toFixed(1)}K reach</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="content" className="space-y-6">
          <div className="card-2050 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <Brain className="h-6 w-6 text-green-400" />
                <h3 className="text-lg font-semibold text-white">AI-Powered Content Analysis</h3>
              </div>
              <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                AI Enhanced
              </Badge>
            </div>
            
            <div className="space-y-4">
              {mockContentPerformance.map((content, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10 hover:bg-white/10 transition-colors">
                  <div className="flex-1">
                    <h4 className="font-medium text-white mb-2">{content.title}</h4>
                    <div className="flex items-center space-x-4">
                      <Badge variant="secondary" className="bg-blue-500/20 text-blue-400 border-blue-500/30">
                        {content.platform}
                      </Badge>
                      <span className="text-sm text-gray-400">
                        {content.engagement}% engagement
                      </span>
                      <div className="flex items-center space-x-2">
                        <Brain className="h-3 w-3 text-green-400" />
                        <span className="text-xs text-green-400">AI Score: {content.aiScore}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <TrendingUp className="h-3 w-3 text-yellow-400" />
                        <span className="text-xs text-yellow-400">Trend: {content.trendingScore}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="font-medium text-white">{content.likes.toLocaleString()} likes</div>
                    <div className="text-sm text-gray-400">{content.views.toLocaleString()} views</div>
                    <div className="text-sm text-gray-400">{content.shares} shares</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Performance Radar</h3>
                <Target className="h-5 w-5 text-yellow-400" />
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={mockAIInsights}>
                  <PolarGrid stroke="#374151" />
                  <PolarAngleAxis dataKey="metric" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
                  <PolarRadiusAxis 
                    angle={90} 
                    domain={[0, 100]} 
                    tick={{ fill: '#9CA3AF', fontSize: 10 }}
                  />
                  <Radar
                    name="Current Score"
                    dataKey="score"
                    stroke="#00d4ff"
                    fill="#00d4ff"
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                  <Radar
                    name="Target"
                    dataKey="target"
                    stroke="#00ff88"
                    fill="transparent"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(26, 26, 26, 0.9)', 
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      borderRadius: '8px',
                      color: 'white'
                    }} 
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <div className="card-2050 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">AI Recommendations</h3>
                <Zap className="h-5 w-5 text-yellow-400 animate-pulse" />
              </div>
              <div className="space-y-4">
                <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Brain className="h-4 w-4 text-blue-400" />
                    <span className="text-sm font-medium text-blue-400">Content Optimization</span>
                  </div>
                  <p className="text-sm text-gray-300">
                    Your TikTok content performs 23% better with trending audio. Consider using popular sounds in your next 3 posts.
                  </p>
                </div>
                
                <div className="p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Calendar className="h-4 w-4 text-green-400" />
                    <span className="text-sm font-medium text-green-400">Optimal Timing</span>
                  </div>
                  <p className="text-sm text-gray-300">
                    Post on Instagram between 7-9 PM for 34% higher engagement based on your audience activity.
                  </p>
                </div>
                
                <div className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Target className="h-4 w-4 text-purple-400" />
                    <span className="text-sm font-medium text-purple-400">Trend Alert</span>
                  </div>
                  <p className="text-sm text-gray-300">
                    "AI productivity" is trending up 45%. Create content around this topic in the next 48 hours.
                  </p>
                </div>
                
                <div className="p-4 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                  <div className="flex items-center space-x-2 mb-2">
                    <Users className="h-4 w-4 text-yellow-400" />
                    <span className="text-sm font-medium text-yellow-400">Audience Insight</span>
                  </div>
                  <p className="text-sm text-gray-300">
                    Your audience engages 28% more with behind-the-scenes content. Show your creative process.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

