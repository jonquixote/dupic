import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, Users, Heart, Share, ArrowUpRight, Sparkles, Zap, Brain, Activity } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

const mockEngagementData = [
  { name: 'Mon', engagement: 4000, reach: 2400 },
  { name: 'Tue', engagement: 3000, reach: 1398 },
  { name: 'Wed', engagement: 2000, reach: 9800 },
  { name: 'Thu', engagement: 2780, reach: 3908 },
  { name: 'Fri', engagement: 1890, reach: 4800 },
  { name: 'Sat', engagement: 2390, reach: 3800 },
  { name: 'Sun', engagement: 3490, reach: 4300 },
]

const mockTrendingTopics = [
  { keyword: 'AI Revolution', platform: 'twitter', engagement: 9.8, growth: '+15%', color: 'neon-blue' },
  { keyword: 'Sustainable Living', platform: 'instagram', engagement: 9.4, growth: '+12%', color: 'neon-green' },
  { keyword: 'Remote Work', platform: 'linkedin', engagement: 8.7, growth: '+8%', color: 'neon-purple' },
  { keyword: 'Digital Art', platform: 'tiktok', engagement: 8.2, growth: '+22%', color: 'neon-pink' },
  { keyword: 'Crypto News', platform: 'twitter', engagement: 7.9, growth: '+5%', color: 'neon-orange' },
]

export function Dashboard() {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setTrends(mockTrendingTopics)
      setLoading(false)
    }, 1000)
  }, [])

  const stats = [
    {
      title: 'Total Followers',
      value: '12.5K',
      change: '+2.5%',
      icon: Users,
      color: 'neon-glow-blue',
      bgGradient: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      title: 'Engagement Rate',
      value: '8.2%',
      change: '+1.2%',
      icon: Heart,
      color: 'neon-glow-pink',
      bgGradient: 'from-pink-500/20 to-rose-500/20'
    },
    {
      title: 'Reach',
      value: '45.2K',
      change: '+5.8%',
      icon: TrendingUp,
      color: 'neon-glow-green',
      bgGradient: 'from-green-500/20 to-emerald-500/20'
    },
    {
      title: 'Shares',
      value: '1.8K',
      change: '+12.3%',
      icon: Share,
      color: 'neon-glow-purple',
      bgGradient: 'from-purple-500/20 to-violet-500/20'
    }
  ]

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold holographic-text">Neural Dashboard</h1>
          <p className="text-gray-400 text-lg">Welcome back! Here's what's happening in your digital realm.</p>
        </div>
        <Button className="btn-futuristic group">
          <Sparkles className="mr-2 h-5 w-5 group-hover:animate-spin" />
          Generate Content
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className={`futuristic-card p-6 ${stat.color} group cursor-pointer`}>
            <div className="flex items-center justify-between">
              <div className="space-y-2">
                <p className="text-sm font-medium text-gray-300 uppercase tracking-wide">{stat.title}</p>
                <p className="text-3xl font-bold text-white font-mono">{stat.value}</p>
                <div className="flex items-center space-x-1">
                  <ArrowUpRight className="h-4 w-4 text-green-400" />
                  <span className="text-sm text-green-400 font-semibold">{stat.change}</span>
                </div>
              </div>
              <div className={`p-4 rounded-xl bg-gradient-to-br ${stat.bgGradient} group-hover:scale-110 transition-transform duration-300`}>
                <stat.icon className="h-8 w-8 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Trending Topics */}
        <div className="futuristic-card p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-bold text-white mb-2">Trending Neural Patterns</h3>
              <p className="text-gray-400">Top viral content opportunities detected</p>
            </div>
            <div className="status-indicator">
              <div className="status-dot status-online"></div>
              <span className="text-sm text-gray-300">Live Analysis</span>
            </div>
          </div>
          
          <div className="space-y-4">
            {loading ? (
              <div className="space-y-4">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-4 bg-gray-700/50 rounded w-3/4 mb-2"></div>
                    <div className="h-3 bg-gray-700/30 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : (
              trends.map((trend, index) => (
                <div key={index} className="glass p-4 rounded-lg border border-gray-700/50 hover:border-gray-600/50 transition-all duration-300 group">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-semibold text-white group-hover:text-blue-300 transition-colors">{trend.keyword}</h4>
                        <Badge variant="outline" className="text-xs border-gray-600 text-gray-300">
                          {trend.platform}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-6">
                        <div className="flex items-center space-x-2">
                          <Activity className="h-4 w-4 text-blue-400" />
                          <span className="text-sm text-gray-300 font-mono">
                            {trend.engagement}/10
                          </span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <TrendingUp className="h-4 w-4 text-green-400" />
                          <span className="text-sm text-green-400 font-semibold font-mono">
                            {trend.growth}
                          </span>
                        </div>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm" className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <Brain className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Performance Chart */}
        <div className="futuristic-card p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-xl font-bold text-white mb-2">Neural Activity</h3>
              <p className="text-gray-400">Engagement patterns over the last 7 days</p>
            </div>
            <div className="status-indicator">
              <div className="status-dot status-processing"></div>
              <span className="text-sm text-gray-300">Processing</span>
            </div>
          </div>
          
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockEngagementData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey="name" 
                stroke="rgba(255,255,255,0.5)"
                fontSize={12}
                fontFamily="monospace"
              />
              <YAxis 
                stroke="rgba(255,255,255,0.5)"
                fontSize={12}
                fontFamily="monospace"
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: '1px solid rgba(0, 212, 255, 0.3)',
                  borderRadius: '8px',
                  color: 'white'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="engagement" 
                stroke="#00d4ff" 
                strokeWidth={3}
                name="Engagement"
                dot={{ fill: '#00d4ff', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#00d4ff', strokeWidth: 2 }}
              />
              <Line 
                type="monotone" 
                dataKey="reach" 
                stroke="#00ff88" 
                strokeWidth={3}
                name="Reach"
                dot={{ fill: '#00ff88', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#00ff88', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="futuristic-card p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-xl font-bold text-white mb-2">Neural Commands</h3>
            <p className="text-gray-400">Execute your content strategy protocols</p>
          </div>
          <Zap className="h-6 w-6 text-yellow-400 animate-pulse" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Button className="btn-futuristic h-24 flex-col space-y-3 group">
            <TrendingUp className="h-8 w-8 group-hover:scale-110 transition-transform" />
            <span className="font-semibold">Analyze Trends</span>
          </Button>
          <Button className="btn-futuristic h-24 flex-col space-y-3 group">
            <Sparkles className="h-8 w-8 group-hover:scale-110 transition-transform" />
            <span className="font-semibold">Generate Content</span>
          </Button>
          <Button className="btn-futuristic h-24 flex-col space-y-3 group">
            <Users className="h-8 w-8 group-hover:scale-110 transition-transform" />
            <span className="font-semibold">View Analytics</span>
          </Button>
        </div>
      </div>
    </div>
  )
}
