import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Search, Filter, RefreshCw, TrendingUp, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { apiService } from '@/services/api'
import { toast } from 'sonner'

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

export function TrendsPage() {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [selectedCategory, setSelectedCategory] = useState('all')

  useEffect(() => {
    fetchTrends()
  }, [])

  const fetchTrends = async () => {
    setLoading(true)
    try {
      const data = await apiService.getTrends()
      setTrends(data)
      toast.success('Trends loaded successfully!')
    } catch (error) {
      console.error('Error fetching trends:', error)
      toast.error('Failed to load trends')
      // Fallback to mock data
      setTrends(mockTrends)
    } finally {
      setLoading(false)
    }
  }

  const refreshTrends = async () => {
    setLoading(true)
    try {
      const data = await apiService.refreshTrends()
      setTrends(data.trends || [])
      toast.success('Trends refreshed successfully!')
    } catch (error) {
      console.error('Error refreshing trends:', error)
      toast.error('Failed to refresh trends')
    } finally {
      setLoading(false)
    }
  }

  const filteredTrends = trends.filter(trend => {
    const matchesSearch = trend.keyword.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesPlatform = selectedPlatform === 'all' || trend.platform === selectedPlatform
    const matchesCategory = selectedCategory === 'all' || trend.category === selectedCategory
    return matchesSearch && matchesPlatform && matchesCategory
  })

  const platformData = trends.reduce((acc, trend) => {
    acc[trend.platform] = (acc[trend.platform] || 0) + 1
    return acc
  }, {})

  const chartData = Object.entries(platformData).map(([platform, count]) => ({
    platform,
    count
  }))

  const pieData = Object.entries(platformData).map(([platform, count]) => ({
    name: platform,
    value: count
  }))

  const mockTrends = [
    {
      id: 1,
      keyword: 'AI Revolution',
      platform: 'twitter',
      category: 'technology',
      engagement_score: 9.8,
      volume: 45000,
      growth_rate: 15.2,
      sentiment: 'positive'
    },
    {
      id: 2,
      keyword: 'Sustainable Living',
      platform: 'instagram',
      category: 'lifestyle',
      engagement_score: 9.4,
      volume: 32000,
      growth_rate: 12.8,
      sentiment: 'positive'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Trend Analysis</h1>
          <p className="text-gray-600">Discover viral content opportunities across social platforms</p>
        </div>
        <Button onClick={refreshTrends} disabled={loading}>
          <RefreshCw className={`mr-2 h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh Trends
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search trends..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Platform" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Platforms</SelectItem>
                <SelectItem value="twitter">Twitter</SelectItem>
                <SelectItem value="instagram">Instagram</SelectItem>
                <SelectItem value="tiktok">TikTok</SelectItem>
                <SelectItem value="facebook">Facebook</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-full md:w-48">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="technology">Technology</SelectItem>
                <SelectItem value="lifestyle">Lifestyle</SelectItem>
                <SelectItem value="business">Business</SelectItem>
                <SelectItem value="entertainment">Entertainment</SelectItem>
                <SelectItem value="sports">Sports</SelectItem>
                <SelectItem value="news">News</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="trends" className="space-y-6">
        <TabsList>
          <TabsTrigger value="trends">Trending Topics</TabsTrigger>
          <TabsTrigger value="analytics">Platform Analytics</TabsTrigger>
          <TabsTrigger value="insights">AI Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="trends" className="space-y-6">
          {/* Trends Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {loading ? (
              [...Array(6)].map((_, i) => (
                <Card key={i} className="animate-pulse">
                  <CardContent className="p-6">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                  </CardContent>
                </Card>
              ))
            ) : (
              filteredTrends.slice(0, 12).map((trend) => (
                <Card key={trend.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-2">{trend.keyword}</h3>
                        <div className="flex items-center space-x-2 mb-3">
                          <Badge variant="secondary">{trend.platform}</Badge>
                          <Badge variant="outline">{trend.category}</Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">
                          {trend.engagement_score?.toFixed(1) || 'N/A'}
                        </div>
                        <div className="text-xs text-gray-500">Engagement</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Volume:</span>
                        <span className="font-medium">{trend.volume?.toLocaleString() || 'N/A'}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Growth:</span>
                        <span className={`font-medium flex items-center ${
                          (trend.growth_rate || 0) > 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {(trend.growth_rate || 0) > 0 ? (
                            <ArrowUpRight className="h-3 w-3 mr-1" />
                          ) : (
                            <ArrowDownRight className="h-3 w-3 mr-1" />
                          )}
                          {trend.growth_rate?.toFixed(1) || '0'}%
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Sentiment:</span>
                        <Badge 
                          variant={
                            trend.sentiment === 'positive' ? 'default' : 
                            trend.sentiment === 'negative' ? 'destructive' : 'secondary'
                          }
                          className="text-xs"
                        >
                          {trend.sentiment || 'neutral'}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Trends by Platform</CardTitle>
                <CardDescription>Distribution of trending topics across platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Platform Distribution</CardTitle>
                <CardDescription>Percentage breakdown of trending content</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>AI-Powered Insights</CardTitle>
              <CardDescription>Smart recommendations based on trending data</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <h4 className="font-medium text-blue-900 mb-2">🚀 Opportunity Alert</h4>
                  <p className="text-blue-800 text-sm">
                    "AI Revolution" is trending with 15% growth. Consider creating content about AI tools, 
                    automation, or future predictions to capitalize on this trend.
                  </p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                  <h4 className="font-medium text-green-900 mb-2">📈 Growth Trend</h4>
                  <p className="text-green-800 text-sm">
                    Sustainable living content is performing well across Instagram and TikTok. 
                    Focus on eco-friendly tips, zero-waste lifestyle, or green technology.
                  </p>
                </div>
                <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
                  <h4 className="font-medium text-amber-900 mb-2">⚠️ Platform Insight</h4>
                  <p className="text-amber-800 text-sm">
                    Twitter shows higher engagement for tech and business content, while Instagram 
                    performs better for lifestyle and visual content.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

