import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, User, Sparkles, Palette, MessageSquare, Camera } from 'lucide-react'
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

export function CharacterProfiles() {
  const [characters, setCharacters] = useState([])
  const [templates, setTemplates] = useState([])
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    tone: '',
    target_audience: '',
    content_style: '',
    dialogue_style: '',
    visual_wardrobe: '',
    visual_props: '',
    visual_background: '',
    preferred_platforms: [],
    keywords: []
  })

  useEffect(() => {
    fetchCharacters()
    fetchTemplates()
  }, [])

  const fetchCharacters = async () => {
    try {
      // Mock data for now - replace with actual API call
      setCharacters([
        {
          id: 1,
          name: "Tech Innovator",
          description: "Cutting-edge technology content creator",
          tone: "informative",
          target_audience: "Tech professionals, developers",
          content_style: "Technical, educational",
          dialogue_style: "Clear, precise, jargon-friendly",
          visual_wardrobe: "Smart casual, tech-branded apparel",
          visual_props: "Gadgets, computer setups, VR headsets",
          visual_background: "Futuristic lab, minimalist workspace",
          preferred_platforms: ["twitter", "linkedin"],
          keywords: ["AI", "technology", "innovation"]
        }
      ])
    } catch (error) {
      console.error('Error fetching characters:', error)
    }
  }

  const fetchTemplates = async () => {
    try {
      // Mock templates - replace with actual API call
      setTemplates([
        {
          name: "Professional Brand",
          description: "Corporate and business-focused content creator",
          tone: "professional",
          target_audience: "Business professionals, entrepreneurs",
          content_style: "Informative, authoritative, data-driven"
        },
        {
          name: "Lifestyle Influencer",
          description: "Casual and relatable lifestyle content creator",
          tone: "casual",
          target_audience: "Young adults, lifestyle enthusiasts",
          content_style: "Personal, authentic, visually appealing"
        }
      ])
    } catch (error) {
      console.error('Error fetching templates:', error)
    }
  }

  const handleCreateCharacter = async () => {
    try {
      // Mock API call - replace with actual implementation
      const newCharacter = {
        id: Date.now(),
        ...formData,
        user_id: 1 // Mock user ID
      }
      setCharacters([...characters, newCharacter])
      setIsCreateDialogOpen(false)
      resetForm()
    } catch (error) {
      console.error('Error creating character:', error)
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      tone: '',
      target_audience: '',
      content_style: '',
      dialogue_style: '',
      visual_wardrobe: '',
      visual_props: '',
      visual_background: '',
      preferred_platforms: [],
      keywords: []
    })
    setSelectedTemplate(null)
  }

  const applyTemplate = (template) => {
    setFormData({
      ...formData,
      ...template,
      preferred_platforms: template.preferred_platforms || [],
      keywords: template.keywords || []
    })
    setSelectedTemplate(template)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="heading-2050 text-3xl">Character Profiles</h1>
          <p className="text-gray-400">Create and manage AI personas for content generation</p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="btn-primary-2050 flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Create Character</span>
            </Button>
          </DialogTrigger>
          <DialogContent className="glass-dark border-white/20 text-white max-w-2xl max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle className="text-gradient-blue">Create New Character Profile</DialogTitle>
              <DialogDescription className="text-gray-400">
                Define a unique AI persona for content generation
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-6 py-4">
              {/* Template Selection */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Choose Template (Optional)</label>
                <div className="grid grid-cols-2 gap-2">
                  {templates.map((template, index) => (
                    <button
                      key={index}
                      onClick={() => applyTemplate(template)}
                      className={`p-3 rounded-lg border text-left transition-all ${
                        selectedTemplate?.name === template.name
                          ? 'border-blue-500 bg-blue-500/20'
                          : 'border-white/20 hover:border-blue-500/50 hover:bg-white/5'
                      }`}
                    >
                      <div className="font-medium text-sm">{template.name}</div>
                      <div className="text-xs text-gray-400 mt-1">{template.description}</div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Basic Information */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Character Name</label>
                  <Input
                    className="input-2050"
                    placeholder="e.g., Tech Innovator"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Tone</label>
                  <Select value={formData.tone} onValueChange={(value) => setFormData({...formData, tone: value})}>
                    <SelectTrigger className="input-2050">
                      <SelectValue placeholder="Select tone" />
                    </SelectTrigger>
                    <SelectContent className="glass-dark border-white/20 text-white">
                      <SelectItem value="professional">Professional</SelectItem>
                      <SelectItem value="casual">Casual</SelectItem>
                      <SelectItem value="humorous">Humorous</SelectItem>
                      <SelectItem value="informative">Informative</SelectItem>
                      <SelectItem value="inspiring">Inspiring</SelectItem>
                      <SelectItem value="motivational">Motivational</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Description</label>
                <Textarea
                  className="input-2050 min-h-[80px]"
                  placeholder="Describe this character's personality and purpose..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>

              {/* Audience & Style */}
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Target Audience</label>
                  <Input
                    className="input-2050"
                    placeholder="e.g., Tech professionals, developers"
                    value={formData.target_audience}
                    onChange={(e) => setFormData({...formData, target_audience: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-300">Content Style</label>
                  <Input
                    className="input-2050"
                    placeholder="e.g., Technical, educational, engaging"
                    value={formData.content_style}
                    onChange={(e) => setFormData({...formData, content_style: e.target.value})}
                  />
                </div>
              </div>

              {/* Dialogue Style */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 flex items-center space-x-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>Dialogue Style</span>
                </label>
                <Textarea
                  className="input-2050"
                  placeholder="How does this character speak? e.g., Clear, precise, uses technical jargon appropriately..."
                  value={formData.dialogue_style}
                  onChange={(e) => setFormData({...formData, dialogue_style: e.target.value})}
                />
              </div>

              {/* Visual Elements */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gradient-purple flex items-center space-x-2">
                  <Camera className="h-5 w-5" />
                  <span>Visual Identity</span>
                </h3>
                
                <div className="grid grid-cols-1 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Wardrobe Style</label>
                    <Input
                      className="input-2050"
                      placeholder="e.g., Smart casual, tech-branded apparel, professional accessories"
                      value={formData.visual_wardrobe}
                      onChange={(e) => setFormData({...formData, visual_wardrobe: e.target.value})}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Props & Accessories</label>
                    <Input
                      className="input-2050"
                      placeholder="e.g., Gadgets, computer setups, VR headsets, books"
                      value={formData.visual_props}
                      onChange={(e) => setFormData({...formData, visual_props: e.target.value})}
                    />
                  </div>
                  
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Background Settings</label>
                    <Input
                      className="input-2050"
                      placeholder="e.g., Futuristic lab, minimalist workspace, modern office"
                      value={formData.visual_background}
                      onChange={(e) => setFormData({...formData, visual_background: e.target.value})}
                    />
                  </div>
                </div>
              </div>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)} className="btn-secondary-2050">
                Cancel
              </Button>
              <Button onClick={handleCreateCharacter} className="btn-primary-2050">
                Create Character
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Character Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {characters.map((character) => (
          <div key={character.id} className="card-2050 p-6 space-y-4 hover:scale-105 transition-transform">
            {/* Character Avatar */}
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                <User className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">{character.name}</h3>
                <p className="text-sm text-gray-400 capitalize">{character.tone} tone</p>
              </div>
            </div>

            {/* Character Description */}
            <p className="text-gray-300 text-sm line-clamp-3">{character.description}</p>

            {/* Character Stats */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-400">Target Audience</span>
                <span className="text-blue-400">{character.target_audience}</span>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-400">Content Style</span>
                <span className="text-purple-400">{character.content_style}</span>
              </div>
            </div>

            {/* Visual Elements Preview */}
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Palette className="h-4 w-4 text-gray-400" />
                <span className="text-xs text-gray-400">Visual Style</span>
              </div>
              <div className="text-xs text-gray-300">
                <div>👔 {character.visual_wardrobe}</div>
                <div>🎯 {character.visual_props}</div>
                <div>🏢 {character.visual_background}</div>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-white/10">
              <div className="flex items-center space-x-2">
                <Button size="sm" className="btn-secondary-2050 p-2">
                  <Edit className="h-4 w-4" />
                </Button>
                <Button size="sm" className="btn-secondary-2050 p-2 hover:bg-red-500/20 hover:text-red-400">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
              <Button size="sm" className="btn-primary-2050 flex items-center space-x-1">
                <Sparkles className="h-4 w-4" />
                <span>Generate</span>
              </Button>
            </div>
          </div>
        ))}

        {/* Empty State */}
        {characters.length === 0 && (
          <div className="col-span-full">
            <div className="card-2050 p-12 text-center">
              <User className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-300 mb-2">No Characters Yet</h3>
              <p className="text-gray-400 mb-6">Create your first AI character profile to start generating personalized content</p>
              <Button onClick={() => setIsCreateDialogOpen(true)} className="btn-primary-2050">
                Create Your First Character
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

