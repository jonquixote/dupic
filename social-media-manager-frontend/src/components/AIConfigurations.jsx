import { useState, useEffect } from 'react'
import { Plus, Settings, Trash2, CheckCircle, XCircle, Brain, Key, Zap, AlertTriangle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
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
import { Switch } from '@/components/ui/switch'

const AI_PROVIDERS = [
  {
    id: 'openai',
    name: 'OpenAI',
    description: 'GPT models for text generation, DALL-E for images',
    models: {
      text: ['gpt-4', 'gpt-3.5-turbo'],
      speech_to_text: ['whisper-1'],
      vision_to_text: ['gpt-4-vision-preview']
    }
  },
  {
    id: 'google',
    name: 'Google AI',
    description: 'Gemini models for multimodal AI tasks',
    models: {
      text: ['gemini-pro', 'gemini-pro-vision'],
      speech_to_text: ['speech-to-text-v1'],
      vision_to_text: ['gemini-pro-vision']
    }
  },
  {
    id: 'anthropic',
    name: 'Anthropic',
    description: 'Claude models for advanced reasoning',
    models: {
      text: ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
      speech_to_text: [],
      vision_to_text: ['claude-3-opus', 'claude-3-sonnet']
    }
  },
  {
    id: 'azure',
    name: 'Azure OpenAI',
    description: 'Microsoft Azure hosted OpenAI models',
    models: {
      text: ['gpt-4', 'gpt-35-turbo'],
      speech_to_text: ['whisper'],
      vision_to_text: ['gpt-4-vision']
    }
  }
]

export function AIConfigurations() {
  const [configurations, setConfigurations] = useState([])
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false)
  const [testingConfig, setTestingConfig] = useState(null)
  const [formData, setFormData] = useState({
    provider_name: '',
    api_key: '',
    default_model_text: '',
    default_model_speech_to_text: '',
    default_model_vision_to_text: '',
    is_default: false
  })

  useEffect(() => {
    fetchConfigurations()
  }, [])

  const fetchConfigurations = async () => {
    try {
      // Mock data - replace with actual API call
      setConfigurations([
        {
          id: 1,
          provider_name: 'openai',
          api_key: '***sk-1234',
          default_model_text: 'gpt-4',
          default_model_speech_to_text: 'whisper-1',
          default_model_vision_to_text: 'gpt-4-vision-preview',
          is_default: true,
          status: 'active'
        }
      ])
    } catch (error) {
      console.error('Error fetching AI configurations:', error)
    }
  }

  const handleCreateConfiguration = async () => {
    try {
      // Mock API call - replace with actual implementation
      const newConfig = {
        id: Date.now(),
        ...formData,
        user_id: 1, // Mock user ID
        status: 'active'
      }
      setConfigurations([...configurations, newConfig])
      setIsCreateDialogOpen(false)
      resetForm()
    } catch (error) {
      console.error('Error creating AI configuration:', error)
    }
  }

  const testConfiguration = async (configId) => {
    setTestingConfig(configId)
    try {
      // Mock API call - replace with actual implementation
      await new Promise(resolve => setTimeout(resolve, 2000))
      // Update configuration status
      setConfigurations(configs => 
        configs.map(config => 
          config.id === configId 
            ? { ...config, status: 'active' }
            : config
        )
      )
    } catch (error) {
      console.error('Error testing configuration:', error)
      setConfigurations(configs => 
        configs.map(config => 
          config.id === configId 
            ? { ...config, status: 'error' }
            : config
        )
      )
    } finally {
      setTestingConfig(null)
    }
  }

  const setAsDefault = async (configId) => {
    try {
      // Mock API call - replace with actual implementation
      setConfigurations(configs => 
        configs.map(config => ({
          ...config,
          is_default: config.id === configId
        }))
      )
    } catch (error) {
      console.error('Error setting default configuration:', error)
    }
  }

  const deleteConfiguration = async (configId) => {
    try {
      // Mock API call - replace with actual implementation
      setConfigurations(configs => configs.filter(config => config.id !== configId))
    } catch (error) {
      console.error('Error deleting configuration:', error)
    }
  }

  const resetForm = () => {
    setFormData({
      provider_name: '',
      api_key: '',
      default_model_text: '',
      default_model_speech_to_text: '',
      default_model_vision_to_text: '',
      is_default: false
    })
  }

  const getProviderInfo = (providerId) => {
    return AI_PROVIDERS.find(p => p.id === providerId) || {}
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-4 w-4 text-green-400" />
      case 'error':
        return <XCircle className="h-4 w-4 text-red-400" />
      case 'testing':
        return <div className="h-4 w-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
      default:
        return <AlertTriangle className="h-4 w-4 text-yellow-400" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="heading-2050 text-3xl">AI Configurations</h1>
          <p className="text-gray-400">Manage your AI provider settings and API keys</p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button className="btn-primary-2050 flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Add Provider</span>
            </Button>
          </DialogTrigger>
          <DialogContent className="glass-dark border-white/20 text-white max-w-2xl">
            <DialogHeader>
              <DialogTitle className="text-gradient-blue">Add AI Provider Configuration</DialogTitle>
              <DialogDescription className="text-gray-400">
                Configure a new AI provider for content generation and analysis
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-6 py-4">
              {/* Provider Selection */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">AI Provider</label>
                <Select value={formData.provider_name} onValueChange={(value) => setFormData({...formData, provider_name: value})}>
                  <SelectTrigger className="input-2050">
                    <SelectValue placeholder="Select AI provider" />
                  </SelectTrigger>
                  <SelectContent className="glass-dark border-white/20 text-white">
                    {AI_PROVIDERS.map((provider) => (
                      <SelectItem key={provider.id} value={provider.id}>
                        <div className="flex items-center space-x-2">
                          <Brain className="h-4 w-4" />
                          <div>
                            <div className="font-medium">{provider.name}</div>
                            <div className="text-xs text-gray-400">{provider.description}</div>
                          </div>
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* API Key */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300 flex items-center space-x-2">
                  <Key className="h-4 w-4" />
                  <span>API Key</span>
                </label>
                <Input
                  type="password"
                  className="input-2050"
                  placeholder="Enter your API key"
                  value={formData.api_key}
                  onChange={(e) => setFormData({...formData, api_key: e.target.value})}
                />
                <p className="text-xs text-gray-500">Your API key will be encrypted and stored securely</p>
              </div>

              {/* Model Configuration */}
              {formData.provider_name && (
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gradient-purple">Default Models</h3>
                  
                  {/* Text Generation Model */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Text Generation Model</label>
                    <Select 
                      value={formData.default_model_text} 
                      onValueChange={(value) => setFormData({...formData, default_model_text: value})}
                    >
                      <SelectTrigger className="input-2050">
                        <SelectValue placeholder="Select text model" />
                      </SelectTrigger>
                      <SelectContent className="glass-dark border-white/20 text-white">
                        {getProviderInfo(formData.provider_name).models?.text?.map((model) => (
                          <SelectItem key={model} value={model}>{model}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Speech to Text Model */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Speech-to-Text Model</label>
                    <Select 
                      value={formData.default_model_speech_to_text} 
                      onValueChange={(value) => setFormData({...formData, default_model_speech_to_text: value})}
                    >
                      <SelectTrigger className="input-2050">
                        <SelectValue placeholder="Select speech-to-text model" />
                      </SelectTrigger>
                      <SelectContent className="glass-dark border-white/20 text-white">
                        {getProviderInfo(formData.provider_name).models?.speech_to_text?.map((model) => (
                          <SelectItem key={model} value={model}>{model}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Vision to Text Model */}
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Vision-to-Text Model</label>
                    <Select 
                      value={formData.default_model_vision_to_text} 
                      onValueChange={(value) => setFormData({...formData, default_model_vision_to_text: value})}
                    >
                      <SelectTrigger className="input-2050">
                        <SelectValue placeholder="Select vision model" />
                      </SelectTrigger>
                      <SelectContent className="glass-dark border-white/20 text-white">
                        {getProviderInfo(formData.provider_name).models?.vision_to_text?.map((model) => (
                          <SelectItem key={model} value={model}>{model}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}

              {/* Set as Default */}
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <label className="text-sm font-medium text-gray-300">Set as Default</label>
                  <p className="text-xs text-gray-500">Use this configuration as the default for all AI operations</p>
                </div>
                <Switch
                  checked={formData.is_default}
                  onCheckedChange={(checked) => setFormData({...formData, is_default: checked})}
                />
              </div>
            </div>

            <DialogFooter>
              <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)} className="btn-secondary-2050">
                Cancel
              </Button>
              <Button onClick={handleCreateConfiguration} className="btn-primary-2050">
                Add Configuration
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {/* Configurations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {configurations.map((config) => {
          const providerInfo = getProviderInfo(config.provider_name)
          const isDefault = config.is_default
          const isTesting = testingConfig === config.id

          return (
            <div key={config.id} className={`card-2050 p-6 space-y-4 ${isDefault ? 'border-blue-500/50 glow-blue' : ''}`}>
              {/* Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                    <Brain className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{providerInfo.name}</h3>
                    <p className="text-sm text-gray-400">{providerInfo.description}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  {getStatusIcon(isTesting ? 'testing' : config.status)}
                  {isDefault && (
                    <div className="px-2 py-1 rounded-full bg-blue-500/20 border border-blue-500/30">
                      <span className="text-xs font-medium text-blue-400">Default</span>
                    </div>
                  )}
                </div>
              </div>

              {/* API Key */}
              <div className="flex items-center justify-between py-2 px-3 rounded-lg bg-white/5">
                <div className="flex items-center space-x-2">
                  <Key className="h-4 w-4 text-gray-400" />
                  <span className="text-sm text-gray-300">API Key</span>
                </div>
                <span className="text-sm font-mono text-gray-400">{config.api_key}</span>
              </div>

              {/* Models */}
              <div className="space-y-2">
                <h4 className="text-sm font-medium text-gray-300">Configured Models</h4>
                <div className="grid grid-cols-1 gap-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Text Generation:</span>
                    <span className="text-blue-400">{config.default_model_text}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Speech-to-Text:</span>
                    <span className="text-purple-400">{config.default_model_speech_to_text}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Vision-to-Text:</span>
                    <span className="text-green-400">{config.default_model_vision_to_text}</span>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between pt-4 border-t border-white/10">
                <div className="flex items-center space-x-2">
                  <Button 
                    size="sm" 
                    className="btn-secondary-2050 p-2"
                    onClick={() => testConfiguration(config.id)}
                    disabled={isTesting}
                  >
                    <Zap className="h-4 w-4" />
                  </Button>
                  <Button size="sm" className="btn-secondary-2050 p-2">
                    <Settings className="h-4 w-4" />
                  </Button>
                  <Button 
                    size="sm" 
                    className="btn-secondary-2050 p-2 hover:bg-red-500/20 hover:text-red-400"
                    onClick={() => deleteConfiguration(config.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
                
                {!isDefault && (
                  <Button 
                    size="sm" 
                    className="btn-primary-2050"
                    onClick={() => setAsDefault(config.id)}
                  >
                    Set Default
                  </Button>
                )}
              </div>
            </div>
          )
        })}

        {/* Empty State */}
        {configurations.length === 0 && (
          <div className="col-span-full">
            <div className="card-2050 p-12 text-center">
              <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-300 mb-2">No AI Providers Configured</h3>
              <p className="text-gray-400 mb-6">Add your first AI provider to start using advanced content generation features</p>
              <Button onClick={() => setIsCreateDialogOpen(true)} className="btn-primary-2050">
                Add Your First Provider
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

