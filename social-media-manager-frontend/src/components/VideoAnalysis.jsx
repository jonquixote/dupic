import { useState, useEffect } from 'react'
import { Play, Upload, Eye, MessageSquare, TrendingUp, Download, Search, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { toast } from 'sonner'
import { apiService } from '@/services/api'

export function VideoAnalysis() {
  const [analyses, setAnalyses] = useState([])
  const [isAnalyzeDialogOpen, setIsAnalyzeDialogOpen] = useState(false)
  const [analyzingVideo, setAnalyzingVideo] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterPlatform, setFilterPlatform] = useState('all')
  const [formData, setFormData] = useState({
    video_url: '',
    platform: 'tiktok'
  })
  const [viewingAnalysis, setViewingAnalysis] = useState(null)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)

  useEffect(() => {
    fetchAnalyses()
  }, [])

    const fetchAnalyses = async () => {
    try {
      // Get user ID from profile
      const profileResponse = await apiService.getProfile()
      const userId = profileResponse.user?.id || 1 // Fallback to 1 for demo
      
      // Call the backend API to fetch video analyses
      const results = await apiService.getVideoAnalyses(userId)
      
      // Ensure all required fields are present
      const normalizedResults = results.map(analysis => ({
        id: analysis.id,
        post_id: analysis.post_id,
        video_url: analysis.video_url || '',
        platform: analysis.platform || 'tiktok',
        transcription_text: analysis.transcription_text || analysis.transcription || 'Transcription not available',
        visual_description: analysis.visual_description || 'Visual description not available',
        analysis_date: analysis.analysis_date || new Date().toISOString(),
        engagement_score: analysis.engagement_score || 0,
        trending_elements: Array.isArray(analysis.trending_elements) ? analysis.trending_elements : [],
        sentiment: analysis.sentiment || 'neutral',
        duration: analysis.duration || '00:00:00',
        ...analysis // Include any other fields that might be present
      }))
      
      setAnalyses(normalizedResults)
    } catch (error) {
      console.error('Error fetching video analyses:', error)
      // Fallback to mock data
      setAnalyses([
        {
          id: 1,
          video_url: 'https://example.com/video1.mp4',
          platform: 'tiktok',
          transcription_text: "Hey everyone! Today I want to share with you this amazing productivity hack that has completely changed my workflow. It's all about using AI to automate your social media content creation...",
          visual_description: 'A young professional in casual attire sitting in a modern home office setup. The background features a clean, minimalist desk with a laptop, ring light, and some plants. The lighting is bright and natural, creating a warm, inviting atmosphere. The person is gesturing enthusiastically while speaking to the camera.',
          analysis_date: '2024-08-23T10:30:00Z',
          engagement_score: 85,
          trending_elements: ['productivity', 'AI automation', 'home office setup'],
          sentiment: 'positive',
          duration: '00:01:23'
        },
        {
          id: 2,
          video_url: 'https://example.com/video2.mp4',
          platform: 'instagram',
          transcription_text: 'Quick morning routine that keeps me energized all day! First, I start with meditation, then I have my green smoothie, and finally some light stretching...',
          visual_description: 'Bright, airy bedroom with natural lighting streaming through large windows. The creator is wearing comfortable workout clothes and demonstrates various morning routine activities. The aesthetic is clean and minimalist with white and beige tones.',
          analysis_date: '2024-08-23T09:15:00Z',
          engagement_score: 92,
          trending_elements: ['morning routine', 'wellness', 'self-care'],
          sentiment: 'positive',
          duration: '00:00:45'
        }
      ])
    }
  }

  const analyzeVideo = async () => {
    if (!formData.video_url) {
      toast.error('Please enter a video URL')
      return
    }

    setAnalyzingVideo(true)
    try {
      // Get user ID from profile
      const profileResponse = await apiService.getProfile()
      const userId = profileResponse.user?.id || 1 // Fallback to 1 for demo
      
      // Call the backend API for video analysis
      const result = await apiService.analyzeVideo({
        user_id: userId,
        video_url: formData.video_url,
        platform: formData.platform
      })
      
      // Check if the result is successful
      if (result && (result.success === true || !result.error)) {
        const newAnalysis = {
          id: result.analysis_id || result.id || Date.now(),
          post_id: result.post_id || null,
          video_url: formData.video_url,
          platform: formData.platform,
          transcription_text: result.transcription || result.transcription_text || 'Transcription not available',
          visual_description: result.visual_description || 'Visual description not available',
          analysis_date: result.analysis_date || new Date().toISOString(),
          engagement_score: result.engagement_score || 0,
          trending_elements: Array.isArray(result.trending_elements) ? result.trending_elements : [],
          sentiment: result.sentiment || 'neutral',
          duration: result.duration || '00:00:00'
        }
        
        setAnalyses([newAnalysis, ...analyses])
        setIsAnalyzeDialogOpen(false)
        resetForm()
        toast.success('Video analysis completed!')
      } else {
        // Handle error response
        const errorMessage = result?.error || 'Failed to analyze video'
        toast.error(`Video analysis failed: ${errorMessage}`)
      }
    } catch (error) {
      console.error('Error analyzing video:', error)
      toast.error('Failed to analyze video: ' + (error.message || 'Unknown error'))
    } finally {
      setAnalyzingVideo(false)
    }
  }

  const resetForm = () => {
    setFormData({
      video_url: '',
      platform: 'tiktok'
    })
  }

  const filteredAnalyses = analyses.filter(analysis => {
    const matchesSearch = (analysis.transcription_text && analysis.transcription_text.toLowerCase().includes(searchQuery.toLowerCase())) ||
                         (Array.isArray(analysis.trending_elements) && 
                          analysis.trending_elements.some(element => 
                            element && element.toLowerCase().includes(searchQuery.toLowerCase())
                          ))
    const matchesPlatform = filterPlatform === 'all' || analysis.platform === filterPlatform
    return matchesSearch && matchesPlatform
  })

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive': return 'text-green-400'
      case 'negative': return 'text-red-400'
      case 'neutral': return 'text-gray-400'
      default: return 'text-gray-400'
    }
  }

  const getEngagementColor = (score) => {
    if (score >= 80) return 'text-green-400'
    if (score >= 60) return 'text-yellow-400'
    return 'text-red-400'
  }

  const handleDownload = (analysis) => {
    // Create a blob with the analysis data
    const data = JSON.stringify(analysis, null, 2)
    const blob = new Blob([data], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    
    // Create a temporary link and trigger download
    const link = document.createElement('a')
    link.href = url
    link.download = `video-analysis-${analysis.id}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    // Clean up
    URL.revokeObjectURL(url)
    
    toast.success('Analysis downloaded successfully!')
  }

  const handleViewDetails = (analysis) => {
    setViewingAnalysis(analysis)
    setIsViewDialogOpen(true)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="heading-2050 text-3xl">Video Analysis</h1>
          <p className="text-gray-400">AI-powered video content analysis and insights</p>
        </div>
        
        <Dialog open={isAnalyzeDialogOpen} onOpenChange={setIsAnalyzeDialogOpen}>
          <DialogTrigger asChild>
            <Button className="btn-primary-2050 flex items-center space-x-2">
              <Upload className="h-4 w-4" />
              <span>Analyze Video</span>
            </Button>
          </DialogTrigger>
          <DialogContent className="glass-dark border-white/20 text-white max-w-lg">
            <DialogHeader>
              <DialogTitle className="text-gradient-blue">Analyze Video Content</DialogTitle>
              <DialogDescription className="text-gray-400">
                Provide a video URL for AI-powered transcription and visual analysis
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Video URL</label>
                <Input
                  className="input-2050"
                  placeholder="https://example.com/video.mp4"
                  value={formData.video_url}
                  onChange={(e) => setFormData({...formData, video_url: e.target.value})}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Platform</label>
                <Select value={formData.platform} onValueChange={(value) => setFormData({...formData, platform: value})}>
                  <SelectTrigger className="input-2050">
                    <SelectValue placeholder="Select platform" />
                  </SelectTrigger>
                  <SelectContent className="glass-dark border-white/20 text-white">
                    <SelectItem value="tiktok">TikTok</SelectItem>
                    <SelectItem value="instagram">Instagram</SelectItem>
                    <SelectItem value="youtube">YouTube</SelectItem>
                    <SelectItem value="twitter">Twitter</SelectItem>
                    <SelectItem value="linkedin">LinkedIn</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsAnalyzeDialogOpen(false)} className="btn-secondary-2050">
                Cancel
              </Button>
              <Button 
                onClick={analyzeVideo} 
                className="btn-primary-2050"
                disabled={analyzingVideo || !formData.video_url}
              >
                {analyzingVideo ? (
                  <div className="flex items-center space-x-2">
                    <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>Analyzing...</span>
                  </div>
                ) : (
                  'Analyze Video'
                )}
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            className="input-2050 pl-10"
            placeholder="Search analyses..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <Select value={filterPlatform} onValueChange={setFilterPlatform}>
          <SelectTrigger className="input-2050 w-40">
            <Filter className="h-4 w-4 mr-2" />
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="glass-dark border-white/20 text-white">
            <SelectItem value="all">All Platforms</SelectItem>
            <SelectItem value="tiktok">TikTok</SelectItem>
            <SelectItem value="instagram">Instagram</SelectItem>
            <SelectItem value="youtube">YouTube</SelectItem>
            <SelectItem value="twitter">Twitter</SelectItem>
            <SelectItem value="linkedin">LinkedIn</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Analysis Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {filteredAnalyses.map((analysis) => (
          <div key={analysis.id} className="card-2050 p-6 space-y-4">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
                  <Play className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-white capitalize">{analysis.platform}</span>
                    <span className="text-xs text-gray-400">•</span>
                    <span className="text-xs text-gray-400">{analysis.duration}</span>
                  </div>
                  <p className="text-xs text-gray-500">
                    {new Date(analysis.analysis_date).toLocaleDateString()}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <div className={`text-sm font-medium ${getEngagementColor(analysis.engagement_score)}`}>
                  {analysis.engagement_score}%
                </div>
                <TrendingUp className="h-4 w-4 text-blue-400" />
              </div>
            </div>

            {/* Transcription */}
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <MessageSquare className="h-4 w-4 text-blue-400" />
                <span className="text-sm font-medium text-gray-300">Transcription</span>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <p className="text-sm text-gray-300 line-clamp-3">
                  {analysis.transcription_text}
                </p>
              </div>
            </div>

            {/* Visual Description */}
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Eye className="h-4 w-4 text-purple-400" />
                <span className="text-sm font-medium text-gray-300">Visual Analysis</span>
              </div>
              <div className="bg-white/5 rounded-lg p-3">
                <p className="text-sm text-gray-300 line-clamp-3">
                  {analysis.visual_description}
                </p>
              </div>
            </div>

            {/* Trending Elements */}
            <div className="space-y-2">
              <span className="text-sm font-medium text-gray-300">Trending Elements</span>
              <div className="flex flex-wrap gap-2">
                {analysis.trending_elements.map((element, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-xs text-blue-400"
                  >
                    #{element}
                  </span>
                ))}
              </div>
            </div>

            {/* Sentiment & Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-white/10">
              <div className="flex items-center space-x-4">
                <div className="text-xs">
                  <span className="text-gray-400">Sentiment: </span>
                  <span className={`capitalize ${getSentimentColor(analysis.sentiment)}`}>
                    {analysis.sentiment}
                  </span>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Button 
                  size="sm" 
                  className="btn-secondary-2050 p-2"
                  onClick={() => handleDownload(analysis)}
                >
                  <Download className="h-4 w-4" />
                </Button>
                <Button 
                  size="sm" 
                  className="btn-primary-2050 text-xs px-3"
                  onClick={() => handleViewDetails(analysis)}
                >
                  View Details
                </Button>
              </div>
            </div>
          </div>
        ))}

        {/* Empty State */}
        {filteredAnalyses.length === 0 && (
          <div className="col-span-full">
            <div className="card-2050 p-12 text-center">
              <Play className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-300 mb-2">
                {analyses.length === 0 ? 'No Video Analyses Yet' : 'No Results Found'}
              </h3>
              <p className="text-gray-400 mb-6">
                {analyses.length === 0 
                  ? 'Analyze your first video to get AI-powered insights and transcriptions'
                  : 'Try adjusting your search or filter criteria'
                }
              </p>
              {analyses.length === 0 && (
                <Button onClick={() => setIsAnalyzeDialogOpen(true)} className="btn-primary-2050">
                  Analyze Your First Video
                </Button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* View Details Dialog */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="glass-dark border-white/20 text-white max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-gradient-blue">Video Analysis Details</DialogTitle>
            <DialogDescription className="text-gray-400">
              Detailed insights and analysis of your video content
            </DialogDescription>
          </DialogHeader>

          {viewingAnalysis && (
            <div className="space-y-6 py-4">
              {/* Video Info */}
              <div className="flex items-center justify-between p-4 bg-white/5 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
                    <Play className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="font-medium capitalize">{viewingAnalysis.platform}</div>
                    <div className="text-sm text-gray-400">{viewingAnalysis.duration}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-bold ${getEngagementColor(viewingAnalysis.engagement_score)}`}>
                    {viewingAnalysis.engagement_score}%
                  </div>
                  <div className="text-xs text-gray-400">Engagement</div>
                </div>
              </div>

              {/* Transcription */}
              <div>
                <h3 className="text-lg font-semibold mb-2 flex items-center">
                  <MessageSquare className="h-5 w-5 mr-2 text-blue-400" />
                  Full Transcription
                </h3>
                <div className="bg-white/5 rounded-lg p-4">
                  <p className="text-gray-300 whitespace-pre-wrap">
                    {viewingAnalysis.transcription_text}
                  </p>
                </div>
              </div>

              {/* Visual Analysis */}
              <div>
                <h3 className="text-lg font-semibold mb-2 flex items-center">
                  <Eye className="h-5 w-5 mr-2 text-purple-400" />
                  Visual Analysis
                </h3>
                <div className="bg-white/5 rounded-lg p-4">
                  <p className="text-gray-300">
                    {viewingAnalysis.visual_description}
                  </p>
                </div>
              </div>

              {/* Trending Elements */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Trending Elements</h3>
                <div className="flex flex-wrap gap-2">
                  {viewingAnalysis.trending_elements.map((element, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full bg-blue-500/20 border border-blue-500/30 text-sm text-blue-400"
                    >
                      #{element}
                    </span>
                  ))}
                </div>
              </div>

              {/* Sentiment */}
              <div>
                <h3 className="text-lg font-semibold mb-2">Sentiment Analysis</h3>
                <div className="flex items-center space-x-4 p-4 bg-white/5 rounded-lg">
                  <div className="text-center">
                    <div className={`text-2xl font-bold ${getSentimentColor(viewingAnalysis.sentiment)}`}>
                      {viewingAnalysis.sentiment}
                    </div>
                    <div className="text-xs text-gray-400">Overall Sentiment</div>
                  </div>
                  <div className="flex-1">
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          viewingAnalysis.sentiment === 'positive' ? 'bg-green-500' :
                          viewingAnalysis.sentiment === 'negative' ? 'bg-red-500' : 'bg-gray-500'
                        }`}
                        style={{ width: '100%' }}
                      ></div>
                    </div>
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                      <span>Negative</span>
                      <span>Neutral</span>
                      <span>Positive</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-3">
                <Button 
                  variant="outline" 
                  className="btn-secondary-2050"
                  onClick={() => handleDownload(viewingAnalysis)}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download Report
                </Button>
                <Button 
                  className="btn-primary-2050"
                  onClick={() => setIsViewDialogOpen(false)}
                >
                  Close
                </Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}

