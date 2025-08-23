import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { BarChart3, TrendingUp, Users, Heart, Share, Calendar, Download } from 'lucide-react'
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
  Area
} from 'recharts'

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

const mockEngagementData = [
  { date: '2024-01-01', engagement: 4000, reach: 2400, likes: 1200, shares: 800 },
  { date: '2024-01-02', engagement: 3000, reach: 1398, likes: 900, shares: 600 },
  { date: '2024-01-03', engagement: 2000, reach: 9800, likes: 1500, shares: 1200 },
  { date: '2024-01-04', engagement: 2780, reach: 3908, likes: 1100, shares: 900 },
  { date: '2024-01-05', engagement: 1890, reach: 4800, likes: 800, shares: 700 },
  { date: '2024-01-06', engagement: 2390, reach: 3800, likes: 1000, shares: 850 },
  { date: '2024-01-07', engagement: 3490, reach: 4300, likes: 1400, shares: 1100 },
]

const mockPlatformData = [
  { platform: 'Instagram', posts: 45, engagement: 8.2, reach: 12500 },
  { platform: 'Twitter', posts: 32, engagement: 6.8, reach: 8900 },
  { platform: 'TikTok', posts: 28, engagement: 12.4, reach: 15600 },
  { platform: 'Facebook', posts: 20, engagement: 4.2, reach: 6700 },
  { platform: 'LinkedIn', posts: 15, engagement: 5.8, reach: 4200 },
]

const mockContentPerformance = [
  { title: 'AI Revolution in 2024', platform: 'Twitter', engagement: 9.8, likes: 1200, shares: 450 },
  { title: 'Sustainable Living Tips', platform: 'Instagram', engagement: 9.4, likes: 2100, shares: 680 },
  { title: 'Remote Work Setup', platform: 'LinkedIn', engagement: 8.7, likes: 890, shares: 320 },
  { title: 'Tech Trends Video', platform: 'TikTok', engagement: 12.1, likes: 3400, shares: 1200 },
  { title: 'Digital Art Tutorial', platform: 'Instagram', engagement: 8.2, likes: 1800, shares: 540 },
]

export function Analytics() {
  const [timeRange, setTimeRange] = useState('7d')
  const [selectedPlatform, setSelectedPlatform] = useState('all')

  const stats = [
    {
      title: 'Total Engagement',
      value: '24.8K',
      change: '+12.5%',
      icon: Heart,
      color: 'text-pink-600'
    },
    {
      title: 'Reach',
      value: '156.2K',
      change: '+8.3%',
      icon: TrendingUp,
      color: 'text-green-600'
    },
    {
      title: 'Followers',
      value: '12.5K',
      change: '+2.1%',
      icon: Users,
      color: 'text-blue-600'
    },
    {
      title: 'Shares',
      value: '3.2K',
      change: '+15.7%',
      icon: Share,
      color: 'text-purple-600'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-600">Track your social media performance and insights</p>
        </div>
        <div className="flex items-center space-x-4">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 3 months</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
        </div>
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
                    <TrendingUp className="h-3 w-3 mr-1" />
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

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="platforms">Platforms</TabsTrigger>
          <TabsTrigger value="content">Content Performance</TabsTrigger>
          <TabsTrigger value="audience">Audience Insights</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Engagement Over Time</CardTitle>
                <CardDescription>Daily engagement metrics for the selected period</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={mockEngagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area 
                      type="monotone" 
                      dataKey="engagement" 
                      stroke="#3B82F6" 
                      fill="#3B82F6" 
                      fillOpacity={0.3}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Reach vs Engagement</CardTitle>
                <CardDescription>Comparison of reach and engagement metrics</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={mockEngagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="reach" 
                      stroke="#10B981" 
                      strokeWidth={2}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="engagement" 
                      stroke="#3B82F6" 
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Engagement Breakdown</CardTitle>
              <CardDescription>Detailed breakdown of likes, shares, and comments</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={mockEngagementData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="likes" fill="#3B82F6" name="Likes" />
                  <Bar dataKey="shares" fill="#10B981" name="Shares" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="platforms" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Platform Performance</CardTitle>
                <CardDescription>Engagement rates across different platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={mockPlatformData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="engagement" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Reach Distribution</CardTitle>
                <CardDescription>Total reach across platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={mockPlatformData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ platform, reach }) => `${platform}: ${reach}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="reach"
                    >
                      {mockPlatformData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Platform Comparison</CardTitle>
              <CardDescription>Detailed metrics for each platform</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockPlatformData.map((platform, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <div className={`w-4 h-4 rounded-full`} style={{ backgroundColor: COLORS[index] }}></div>
                      <div>
                        <h4 className="font-medium">{platform.platform}</h4>
                        <p className="text-sm text-gray-600">{platform.posts} posts</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{platform.engagement}% engagement</div>
                      <div className="text-sm text-gray-600">{platform.reach.toLocaleString()} reach</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="content" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Top Performing Content</CardTitle>
              <CardDescription>Your best performing posts across all platforms</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockContentPerformance.map((content, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{content.title}</h4>
                      <div className="flex items-center space-x-4 mt-1">
                        <Badge variant="secondary">{content.platform}</Badge>
                        <span className="text-sm text-gray-600">
                          {content.engagement}% engagement
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-medium">{content.likes.toLocaleString()} likes</div>
                      <div className="text-sm text-gray-600">{content.shares} shares</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="audience" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Audience Demographics</CardTitle>
                <CardDescription>Age and gender breakdown of your audience</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">18-24</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: '35%' }}></div>
                      </div>
                      <span className="text-sm text-gray-600">35%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">25-34</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: '45%' }}></div>
                      </div>
                      <span className="text-sm text-gray-600">45%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">35-44</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: '15%' }}></div>
                      </div>
                      <span className="text-sm text-gray-600">15%</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">45+</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: '5%' }}></div>
                      </div>
                      <span className="text-sm text-gray-600">5%</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Best Posting Times</CardTitle>
                <CardDescription>Optimal times for maximum engagement</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <div>
                      <div className="font-medium">Monday - Friday</div>
                      <div className="text-sm text-gray-600">9:00 AM - 11:00 AM</div>
                    </div>
                    <Badge variant="default">Best</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <div>
                      <div className="font-medium">Tuesday - Thursday</div>
                      <div className="text-sm text-gray-600">2:00 PM - 4:00 PM</div>
                    </div>
                    <Badge variant="secondary">Good</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-amber-50 rounded-lg">
                    <div>
                      <div className="font-medium">Weekend</div>
                      <div className="text-sm text-gray-600">10:00 AM - 12:00 PM</div>
                    </div>
                    <Badge variant="outline">Average</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

