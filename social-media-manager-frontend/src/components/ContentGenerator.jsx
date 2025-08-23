import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Sparkles, Copy, RefreshCw, User, Settings, Wand2 } from 'lucide-react'
import { toast } from 'sonner'
import { apiService } from '@/services/api'

export function ContentGenerator() {
  const [trends, setTrends] = useState([])
  const [characters, setCharacters] = useState([])
  const [selectedTrend, setSelectedTrend] = useState('')
  const [selectedCharacter, setSelectedCharacter] = useState('')
  const [selectedPlatform, setSelectedPlatform] = useState('')
  const [contentType, setContentType] = useState('')
  const [additionalContext, setAdditionalContext] = useState('')
  const [generatedContent, setGeneratedContent] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchTrends()
    fetchCharacters()
  }, [])

  const fetchTrends = async () => {
    try {
      const data = await apiService.getTopTrends(10)
      setTrends(data)
    } catch (error) {
      console.error('Error fetching trends:', error)
      setTrends(mockTrends)
    }
  }

  const fetchCharacters = async () => {
    try {
      // For demo, we'll use mock data since we need a user_id
      // In a real app, you'd get the current user's ID from auth context
      const data = await apiService.getCharacters(2) // Using test user ID
      setCharacters(data.length > 0 ? data : mockCharacters)
    } catch (error) {
      console.error('Error fetching characters:', error)
      setCharacters(mockCharacters)
    }
  }

  const generateContent = async () => {
    if (!selectedTrend || !selectedCharacter) {
      toast.error('Please select both a trend and character profile')
      return
    }

    setLoading(true)
    try {
      const contentData = {
        trend_id: parseInt(selectedTrend),
        character_id: parseInt(selectedCharacter),
        content_type: contentType || 'post',
        platform: selectedPlatform || 'twitter',
        additional_context: additionalContext
      }

      const result = await apiService.generateContent(contentData)
      setGeneratedContent([result])
      toast.success('Content generated successfully!')
    } catch (error) {
      console.error('Error generating content:', error)
      toast.error('Failed to generate content: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }

  const mockTrends = [
    { id: 1, keyword: 'AI Revolution', platform: 'twitter', engagement_score: 9.8 },
    { id: 2, keyword: 'Sustainable Living', platform: 'instagram', engagement_score: 9.4 },
    { id: 3, keyword: 'Remote Work', platform: 'linkedin', engagement_score: 8.7 }
  ]

  const mockCharacters = [
    { id: 1, name: 'Professional Brand', tone: 'professional', description: 'Corporate and business-focused' },
    { id: 2, name: 'Lifestyle Influencer', tone: 'casual', description: 'Casual and relatable lifestyle content' },
    { id: 3, name: 'Tech Enthusiast', tone: 'informative', description: 'Technology and innovation focused' }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Content Generator</h1>
          <p className="text-gray-600">Create AI-powered content based on trending topics and your brand voice</p>
        </div>
        <Button onClick={generateContent} disabled={loading}>
          {loading ? (
            <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <Sparkles className="mr-2 h-4 w-4" />
          )}
          Generate Content
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Panel */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="mr-2 h-5 w-5" />
                Content Settings
              </CardTitle>
              <CardDescription>Configure your content generation parameters</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  Select Trending Topic
                </label>
                <Select value={selectedTrend} onValueChange={setSelectedTrend}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a trending topic..." />
                  </SelectTrigger>
                  <SelectContent>
                    {trends.map((trend) => (
                      <SelectItem key={trend.id} value={trend.id.toString()}>
                        <div className="flex items-center justify-between w-full">
                          <span>{trend.keyword}</span>
                          <Badge variant="secondary" className="ml-2">
                            {trend.platform}
                          </Badge>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  Character Profile
                </label>
                <Select value={selectedCharacter} onValueChange={setSelectedCharacter}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose your brand voice..." />
                  </SelectTrigger>
                  <SelectContent>
                    {characters.map((character) => (
                      <SelectItem key={character.id} value={character.id.toString()}>
                        <div>
                          <div className="font-medium">{character.name}</div>
                          <div className="text-sm text-gray-500">{character.description}</div>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Platform
                  </label>
                  <Select value={selectedPlatform} onValueChange={setSelectedPlatform}>
                    <SelectTrigger>
                      <SelectValue placeholder="Platform" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="twitter">Twitter</SelectItem>
                      <SelectItem value="instagram">Instagram</SelectItem>
                      <SelectItem value="tiktok">TikTok</SelectItem>
                      <SelectItem value="facebook">Facebook</SelectItem>
                      <SelectItem value="linkedin">LinkedIn</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700 mb-2 block">
                    Content Type
                  </label>
                  <Select value={contentType} onValueChange={setContentType}>
                    <SelectTrigger>
                      <SelectValue placeholder="Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="post">Post</SelectItem>
                      <SelectItem value="story">Story</SelectItem>
                      <SelectItem value="reel">Reel</SelectItem>
                      <SelectItem value="video">Video</SelectItem>
                      <SelectItem value="thread">Thread</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 block">
                  Additional Context (Optional)
                </label>
                <Textarea
                  placeholder="Add any specific requirements, tone adjustments, or context..."
                  value={additionalContext}
                  onChange={(e) => setAdditionalContext(e.target.value)}
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>

          {/* Character Profiles Management */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="mr-2 h-5 w-5" />
                Character Profiles
              </CardTitle>
              <CardDescription>Manage your brand voices and content styles</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {characters.map((character) => (
                  <div key={character.id} className="p-3 border rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium">{character.name}</h4>
                        <p className="text-sm text-gray-600">{character.description}</p>
                        <Badge variant="outline" className="mt-1">
                          {character.tone}
                        </Badge>
                      </div>
                      <Button variant="ghost" size="sm">
                        Edit
                      </Button>
                    </div>
                  </div>
                ))}
                <Button variant="outline" className="w-full">
                  + Add New Profile
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Output Panel */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Wand2 className="mr-2 h-5 w-5" />
                Generated Content
              </CardTitle>
              <CardDescription>AI-generated content ready for your social media</CardDescription>
            </CardHeader>
            <CardContent>
              {generatedContent.length === 0 ? (
                <div className="text-center py-12">
                  <Sparkles className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No content generated yet</h3>
                  <p className="text-gray-600 mb-4">
                    Select a trending topic and character profile, then click "Generate Content" to get started.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {generatedContent.map((content, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <Badge variant="secondary">Generated Content</Badge>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(content.content)}
                        >
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                      
                      <div className="space-y-3">
                        <div>
                          <h4 className="text-sm font-medium text-gray-700 mb-1">Content:</h4>
                          <p className="text-gray-900 whitespace-pre-wrap">{content.content}</p>
                        </div>
                        
                        {content.hashtags && content.hashtags.length > 0 && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-1">Hashtags:</h4>
                            <div className="flex flex-wrap gap-1">
                              {content.hashtags.map((hashtag, i) => (
                                <Badge key={i} variant="outline" className="text-xs">
                                  {hashtag}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        )}
                        
                        {content.call_to_action && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-1">Call to Action:</h4>
                            <p className="text-gray-900">{content.call_to_action}</p>
                          </div>
                        )}
                        
                        {content.platform_notes && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-1">Platform Notes:</h4>
                            <p className="text-gray-600 text-sm">{content.platform_notes}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Content Templates */}
          <Card>
            <CardHeader>
              <CardTitle>Content Templates</CardTitle>
              <CardDescription>Quick templates for different content types</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 gap-3">
                <Button variant="outline" className="justify-start h-auto p-4">
                  <div className="text-left">
                    <div className="font-medium">Question Post</div>
                    <div className="text-sm text-gray-600">Engage audience with questions</div>
                  </div>
                </Button>
                <Button variant="outline" className="justify-start h-auto p-4">
                  <div className="text-left">
                    <div className="font-medium">How-To Guide</div>
                    <div className="text-sm text-gray-600">Educational step-by-step content</div>
                  </div>
                </Button>
                <Button variant="outline" className="justify-start h-auto p-4">
                  <div className="text-left">
                    <div className="font-medium">Behind the Scenes</div>
                    <div className="text-sm text-gray-600">Personal and authentic content</div>
                  </div>
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

