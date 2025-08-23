import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, Users, Heart, Share, ArrowUpRight, Sparkles } from 'lucide-react'
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
  { keyword: 'AI Revolution', platform: 'twitter', engagement: 9.8, growth: '+15%' },
  { keyword: 'Sustainable Living', platform: 'instagram', engagement: 9.4, growth: '+12%' },
  { keyword: 'Remote Work', platform: 'linkedin', engagement: 8.7, growth: '+8%' },
  { keyword: 'Digital Art', platform: 'tiktok', engagement: 8.2, growth: '+22%' },
  { keyword: 'Crypto News', platform: 'twitter', engagement: 7.9, growth: '+5%' },
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
      color: 'text-blue-600'
    },
    {
      title: 'Engagement Rate',
      value: '8.2%',
      change: '+1.2%',
      icon: Heart,
      color: 'text-pink-600'
    },
    {
      title: 'Reach',
      value: '45.2K',
      change: '+5.8%',
      icon: TrendingUp,
      color: 'text-green-600'
    },
    {
      title: 'Shares',
      value: '1.8K',
      change: '+12.3%',
      icon: Share,
      color: 'text-purple-600'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's what's happening with your social media.</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700">
          <Sparkles className="mr-2 h-4 w-4" />
          Generate Content
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                  <p className="text-sm text-green-600 flex items-center mt-1">
                    <ArrowUpRight className="h-3 w-3 mr-1" />
                    {stat.change}
                  </p>
                </div>
                <div className={`p-3 rounded-full bg-gray-100 ${stat.color}`}>
                  <stat.icon className="h-6 w-6" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trending Topics */}
        <Card>
          <CardHeader>
            <CardTitle>Trending Topics</CardTitle>
            <CardDescription>Top viral content opportunities right now</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {loading ? (
                <div className="space-y-3">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="animate-pulse">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  ))}
                </div>
              ) : (
                trends.map((trend, index) => (
                  <div key={index} className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h4 className="font-medium text-gray-900">{trend.keyword}</h4>
                        <Badge variant="secondary" className="text-xs">
                          {trend.platform}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-4 mt-1">
                        <span className="text-sm text-gray-600">
                          Engagement: {trend.engagement}/10
                        </span>
                        <span className="text-sm text-green-600 font-medium">
                          {trend.growth}
                        </span>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm">
                      <TrendingUp className="h-4 w-4" />
                    </Button>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        {/* Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Weekly Performance</CardTitle>
            <CardDescription>Engagement and reach over the last 7 days</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockEngagementData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="engagement" 
                  stroke="#3B82F6" 
                  strokeWidth={2}
                  name="Engagement"
                />
                <Line 
                  type="monotone" 
                  dataKey="reach" 
                  stroke="#10B981" 
                  strokeWidth={2}
                  name="Reach"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Get started with your content strategy</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <TrendingUp className="h-6 w-6" />
              <span>Analyze Trends</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Sparkles className="h-6 w-6" />
              <span>Generate Content</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Users className="h-6 w-6" />
              <span>View Analytics</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

