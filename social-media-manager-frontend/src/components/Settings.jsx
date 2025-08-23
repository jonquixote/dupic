import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { User, Bell, Shield, Palette, Zap, Plus, Trash2 } from 'lucide-react'
import { toast } from 'sonner'

export function Settings() {
  const [profile, setProfile] = useState({
    name: 'John Doe',
    email: 'john@example.com',
    bio: 'Content creator and social media enthusiast',
    timezone: 'UTC-8'
  })

  const [notifications, setNotifications] = useState({
    trendAlerts: true,
    contentReminders: true,
    analyticsReports: false,
    emailDigest: true
  })

  const [characters, setCharacters] = useState([
    {
      id: 1,
      name: 'Professional Brand',
      description: 'Corporate and business-focused content creator',
      tone: 'professional',
      targetAudience: 'Business professionals, entrepreneurs',
      contentStyle: 'Informative, authoritative, data-driven',
      platforms: ['linkedin', 'twitter'],
      keywords: ['business', 'leadership', 'strategy']
    },
    {
      id: 2,
      name: 'Lifestyle Influencer',
      description: 'Casual and relatable lifestyle content creator',
      tone: 'casual',
      targetAudience: 'Young adults, lifestyle enthusiasts',
      contentStyle: 'Personal, authentic, visually appealing',
      platforms: ['instagram', 'tiktok'],
      keywords: ['lifestyle', 'fashion', 'travel']
    }
  ])

  const [newCharacter, setNewCharacter] = useState({
    name: '',
    description: '',
    tone: '',
    targetAudience: '',
    contentStyle: '',
    platforms: [],
    keywords: []
  })

  const [showNewCharacterForm, setShowNewCharacterForm] = useState(false)

  const [apiKeys, setApiKeys] = useState({
    openai: '',
    twitter: '',
    instagram: '',
    tiktok: ''
  })

  const handleProfileUpdate = () => {
    toast.success('Profile updated successfully!')
  }

  const handleNotificationUpdate = () => {
    toast.success('Notification preferences updated!')
  }

  const handleAddCharacter = () => {
    if (!newCharacter.name || !newCharacter.tone) {
      toast.error('Please fill in required fields')
      return
    }

    const character = {
      id: Date.now(),
      ...newCharacter
    }

    setCharacters([...characters, character])
    setNewCharacter({
      name: '',
      description: '',
      tone: '',
      targetAudience: '',
      contentStyle: '',
      platforms: [],
      keywords: []
    })
    setShowNewCharacterForm(false)
    toast.success('Character profile created!')
  }

  const handleDeleteCharacter = (id) => {
    setCharacters(characters.filter(char => char.id !== id))
    toast.success('Character profile deleted!')
  }

  const handleApiKeyUpdate = () => {
    toast.success('API Keys updated successfully!')
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Manage your account, preferences, and character profiles</p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="characters">Character Profiles</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
          <TabsTrigger value="api-keys">API Keys</TabsTrigger>
        </TabsList>

        <TabsContent value="profile" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="mr-2 h-5 w-5" />
                Profile Information
              </CardTitle>
              <CardDescription>Update your personal information and preferences</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={profile.name}
                    onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email Address</Label>
                  <Input
                    id="email"
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  placeholder="Tell us about yourself..."
                  value={profile.bio}
                  onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                />
              </div>

              <div>
                <Label htmlFor="timezone">Timezone</Label>
                <Select value={profile.timezone} onValueChange={(value) => setProfile({ ...profile, timezone: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="UTC-8">Pacific Time (UTC-8)</SelectItem>
                    <SelectItem value="UTC-5">Eastern Time (UTC-5)</SelectItem>
                    <SelectItem value="UTC+0">GMT (UTC+0)</SelectItem>
                    <SelectItem value="UTC+1">Central European Time (UTC+1)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button onClick={handleProfileUpdate}>
                Update Profile
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="characters" className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Character Profiles</h2>
              <p className="text-gray-600">Manage your brand voices and content styles</p>
            </div>
            <Button onClick={() => setShowNewCharacterForm(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Add Character
            </Button>
          </div>

          {showNewCharacterForm && (
            <Card>
              <CardHeader>
                <CardTitle>Create New Character Profile</CardTitle>
                <CardDescription>Define a new brand voice for your content</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="char-name">Character Name *</Label>
                    <Input
                      id="char-name"
                      placeholder="e.g., Tech Enthusiast"
                      value={newCharacter.name}
                      onChange={(e) => setNewCharacter({ ...newCharacter, name: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="char-tone">Tone *</Label>
                    <Select value={newCharacter.tone} onValueChange={(value) => setNewCharacter({ ...newCharacter, tone: value })}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="professional">Professional</SelectItem>
                        <SelectItem value="casual">Casual</SelectItem>
                        <SelectItem value="humorous">Humorous</SelectItem>
                        <SelectItem value="educational">Educational</SelectItem>
                        <SelectItem value="inspirational">Inspirational</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div>
                  <Label htmlFor="char-description">Description</Label>
                  <Textarea
                    id="char-description"
                    placeholder="Describe this character's personality and style..."
                    value={newCharacter.description}
                    onChange={(e) => setNewCharacter({ ...newCharacter, description: e.target.value })}
                  />
                </div>

                <div>
                  <Label htmlFor="char-audience">Target Audience</Label>
                  <Input
                    id="char-audience"
                    placeholder="e.g., Young professionals, tech enthusiasts"
                    value={newCharacter.targetAudience}
                    onChange={(e) => setNewCharacter({ ...newCharacter, targetAudience: e.target.value })}
                  />
                </div>

                <div>
                  <Label htmlFor="char-style">Content Style</Label>
                  <Input
                    id="char-style"
                    placeholder="e.g., Informative, visual, data-driven"
                    value={newCharacter.contentStyle}
                    onChange={(e) => setNewCharacter({ ...newCharacter, contentStyle: e.target.value })}
                  />
                </div>

                <div className="flex space-x-4">
                  <Button onClick={handleAddCharacter}>
                    Create Character
                  </Button>
                  <Button variant="outline" onClick={() => setShowNewCharacterForm(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {characters.map((character) => (
              <Card key={character.id}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{character.name}</CardTitle>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteCharacter(character.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  <CardDescription>{character.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <Label className="text-sm font-medium">Tone</Label>
                    <Badge variant="secondary" className="ml-2">
                      {character.tone}
                    </Badge>
                  </div>
                  
                  <div>
                    <Label className="text-sm font-medium">Target Audience</Label>
                    <p className="text-sm text-gray-600 mt-1">{character.targetAudience}</p>
                  </div>
                  
                  <div>
                    <Label className="text-sm font-medium">Content Style</Label>
                    <p className="text-sm text-gray-600 mt-1">{character.contentStyle}</pР> 
                  </div>
                  
                  {character.platforms && character.platforms.length > 0 && (
                    <div>
                      <Label className="text-sm font-medium">Preferred Platforms</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {character.platforms.map((platform, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {platform}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {character.keywords && character.keywords.length > 0 && (
                    <div>
                      <Label className="text-sm font-medium">Keywords</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {character.keywords.map((keyword, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Bell className="mr-2 h-5 w-5" />
                Notification Preferences
              </CardTitle>
              <CardDescription>Choose what notifications you want to receive</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="trend-alerts">Trend Alerts</Label>
                  <p className="text-sm text-gray-600">Get notified when new viral trends are detected</p>
                </div>
                <Switch
                  id="trend-alerts"
                  checked={notifications.trendAlerts}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, trendAlerts: checked })}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="content-reminders">Content Reminders</Label>
                  <p className="text-sm text-gray-600">Reminders to post content at optimal times</p>
                </div>
                <Switch
                  id="content-reminders"
                  checked={notifications.contentReminders}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, contentReminders: checked })}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="analytics-reports">Analytics Reports</Label>
                  <p className="text-sm text-gray-600">Weekly performance reports and insights</p>
                </div>
                <Switch
                  id="analytics-reports"
                  checked={notifications.analyticsReports}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, analyticsReports: checked })}
                />
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <Label htmlFor="email-digest">Email Digest</Label>
                  <p className="text-sm text-gray-600">Daily summary of trends and recommendations</p>
                </div>
                <Switch
                  id="email-digest"
                  checked={notifications.emailDigest}
                  onCheckedChange={(checked) => setNotifications({ ...notifications, emailDigest: checked })}
                />
              </div>

              <Button onClick={handleNotificationUpdate}>
                Save Preferences
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="integrations" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="mr-2 h-5 w-5" />
                Social Media Integrations
              </CardTitle>
              <CardDescription>Connect your social media accounts for better insights</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center text-white font-bold">
                    T
                  </div>
                  <div>
                    <h4 className="font-medium">Twitter</h4>
                    <p className="text-sm text-gray-600">Connect your Twitter account</p>
                  </div>
                </div>
                <Button variant="outline">Connect</Button>
              </div>

              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex flex-col items-center justify-center text-white font-bold">
                    I
                  </div>
                  <div>
                    <h4 className="font-medium">Instagram</h4>
                    <p className="text-sm text-gray-600">Connect your Instagram account</p>
                  </div>
                </div>
                <Button variant="outline">Connect</Button>
              </div>

              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-content-center text-white font-bold">
                    T
                  </div>
                  <div>
                    <h4 className="font-medium">TikTok</h4>
                    <p className="text-sm text-gray-600">Connect your TikTok account</p>
                  </div>
                </div>
                <Button variant="outline">Connect</Button>
              </div>

              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
                    L
                  </div>
                  <div>
                    <h4 className="font-medium">LinkedIn</h4>
                    <p className="text-sm text-gray-600">Connect your LinkedIn account</p>
                  </div>
                </div>
                <Button variant="outline">Connect</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="billing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Subscription Plan</CardTitle>
              <CardDescription>Manage your subscription and billing information</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-blue-900">Pro Plan</h4>
                      <p className="text-blue-800 text-sm">$29/month • Unlimited content generation</p>
                    </div>
                    <Badge variant="default">Current Plan</Badge>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 border rounded-lg">
                    <h4 className="font-medium mb-2">Free Plan</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• 10 content generations/month</li>
                      <li>• Basic trend analysis</li>
                      <li>• 1 character profile</li>
                    </ul>
                    <Button variant="outline" className="w-full mt-3" disabled>
                      Current Plan
                    </Button>
                  </div>

                  <div className="p-4 border rounded-lg border-blue-200 bg-blue-50">
                    <h4 className="font-medium mb-2">Pro Plan</h4>
                    <ul className="text-sm text-gray-600 space-y-1">
                      <li>• Unlimited content generation</li>
                      <li>• Advanced analytics</li>
                      <li>• Unlimited character profiles</li>
                      <li>• Priority support</li>
                    </ul>
                    <Button className="w-full mt-3">
                      $29/month
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="api-keys" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Shield className="mr-2 h-5 w-5" />
                API Key Management
              </CardTitle>
              <CardDescription>Manage your API keys for various services</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="openai-key">OpenAI API Key</Label>
                <Input
                  id="openai-key"
                  type="password"
                  value={apiKeys.openai}
                  onChange={(e) => setApiKeys({ ...apiKeys, openai: e.target.value })}
                  placeholder="sk-..."
                />
              </div>
              <div>
                <Label htmlFor="twitter-key">Twitter API Key</Label>
                <Input
                  id="twitter-key"
                  type="password"
                  value={apiKeys.twitter}
                  onChange={(e) => setApiKeys({ ...apiKeys, twitter: e.target.value })}
                  placeholder="Enter your Twitter API key"
                />
              </div>
              <div>
                <Label htmlFor="instagram-key">Instagram API Key</Label>
                <Input
                  id="instagram-key"
                  type="password"
                  value={apiKeys.instagram}
                  onChange={(e) => setApiKeys({ ...apiKeys, instagram: e.target.value })}
                  placeholder="Enter your Instagram API key"
                />
              </div>
              <div>
                <Label htmlFor="tiktok-key">TikTok API Key</Label>
                <Input
                  id="tiktok-key"
                  type="password"
                  value={apiKeys.tiktok}
                  onChange={(e) => setApiKeys({ ...apiKeys, tiktok: e.target.value })}
                  placeholder="Enter your TikTok API key"
                />
              </div>
              <Button onClick={handleApiKeyUpdate}>
                Save API Keys
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

