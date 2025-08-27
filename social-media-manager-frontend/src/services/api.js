const API_BASE_URL = 'http://localhost:5000/api'

class ApiService {
  getAuthHeader() {
    // Use session-based auth instead of token-based
    return {}
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      credentials: 'include', // Include cookies/sessions
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        // Try to parse error message if present
        try {
          const errorData = await response.json()
          throw new Error(errorData.error || 'API request failed')
        } catch {
          throw new Error(`API request failed with status: ${response.status}`)
        }
      }
      
      // Only try to parse JSON if there's content and it's JSON
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json') && response.status !== 204) {
        return await response.json()
      }
      
      // Return null for empty responses (like DELETE requests)
      return null
    } catch (error) {
      console.error('API request error:', error)
      throw error
    }
  }

  // Auth API
  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
  }

  async logout() {
    return this.request('/auth/logout', {
      method: 'POST',
    })
  }

  async getAuthStatus() {
    return this.request('/auth/status')
  }

  async getProfile() {
    return this.request('/auth/profile')
  }

  async updateProfile(profileData) {
    return this.request('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    })
  }

  async getApiKeys() {
    return this.request('/auth/api-keys')
  }

  async addApiKey(apiKeyData) {
    return this.request('/auth/api-keys', {
      method: 'POST',
      body: JSON.stringify(apiKeyData),
    })
  }

  async getApiKey(keyId) {
    return this.request(`/auth/api-keys/${keyId}`)
  }

  async updateApiKey(keyId, apiKeyData) {
    return this.request(`/auth/api-keys/${keyId}`, {
      method: 'PUT',
      body: JSON.stringify(apiKeyData),
    })
  }

  async removeApiKey(keyId) {
    return this.request(`/auth/api-keys/${keyId}`, {
      method: 'DELETE',
    })
  }

  async setDefaultProvider(providerData) {
    return this.request('/auth/default-provider', {
      method: 'POST',
      body: JSON.stringify(providerData),
    })
  }

  async changePassword(passwordData) {
    return this.request('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify(passwordData),
    })
  }

  // Trends API
  async getTrends(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends${queryString ? `?${queryString}` : ''}`)
  }

  async getTopTrends(limit = 10) {
    return this.request(`/trends/top?limit=${limit}`)
  }

  async refreshTrends() {
    return this.request('/trends/refresh', { method: 'POST' })
  }

  async getTrendingHashtags(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends/hashtags${queryString ? `?${queryString}` : ''}`)
  }

  // Content Generation API
  async generateContent(contentData) {
    return this.request('/content/generate', {
      method: 'POST',
      body: JSON.stringify(contentData),
    })
  }

  async transcribeAudio(formData) {
    // For file uploads, we don't want to JSON stringify
    return this.request('/ai/transcribe', {
      method: 'POST',
      body: formData,
      headers: {
        // Remove Content-Type to let browser set it with boundary for multipart/form-data
      },
    })
  }

  async analyzeImage(formData) {
    // For file uploads, we don't want to JSON stringify
    return this.request('/ai/analyze-image', {
      method: 'POST',
      body: formData,
      headers: {
        // Remove Content-Type to let browser set it with boundary for multipart/form-data
      },
    })
  }

  // Video Analysis API
  async analyzeVideo(videoData) {
    return this.request('/analyze_video', {
      method: 'POST',
      body: JSON.stringify(videoData),
    })
  }

  async getVideoAnalysis(postId) {
    return this.request(`/analyze_video/${postId}`)
  }

  async getVideoAnalyses(userId) {
    return this.request(`/video_analyses?user_id=${userId}`)
  }

  async analyzeTrendingVideos(data = {}) {
    return this.request('/analyze_trending', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Analytics API
  async getAnalyticsSummary(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/analytics/summary${queryString ? `?${queryString}` : ''}`)
  }

  async getOptimalPostingTimes(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/analytics/posting-times${queryString ? `?${queryString}` : ''}`)
  }

  async getUserAnalytics() {
    return this.request('/user_analytics')
  }

  async getUserAnalyticsSummary() {
    return this.request('/user_analytics/summary')
  }

  // Visualization API
  async getPlatformDistribution(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends/visualization/platform-distribution${queryString ? `?${queryString}` : ''}`)
  }

  async getCategoryDistribution(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends/visualization/category-distribution${queryString ? `?${queryString}` : ''}`)
  }

  async getSentimentDistribution(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends/visualization/sentiment-distribution${queryString ? `?${queryString}` : ''}`)
  }

  async getEngagementOverTime(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/trends/visualization/engagement-over-time${queryString ? `?${queryString}` : ''}`)
  }

  // Content Optimization API
  async optimizeContent(contentData) {
    return this.request('/content/optimize', {
      method: 'POST',
      body: JSON.stringify(contentData),
    })
  }

  // AI Configurations API
  async getAiConfigs() {
    return this.request('/ai_configs')
  }

  async createAiConfig(configData) {
    return this.request('/ai_configs', {
      method: 'POST',
      body: JSON.stringify(configData),
    })
  }

  async updateAiConfig(configId, configData) {
    return this.request(`/ai_configs/${configId}`, {
      method: 'PUT',
      body: JSON.stringify(configData),
    })
  }

  async deleteAiConfig(configId) {
    return this.request(`/ai_configs/${configId}`, {
      method: 'DELETE',
    })
  }

  async testAiConfig(configId) {
    return this.request(`/ai_configs/${configId}/test`, {
      method: 'POST',
    })
  }

  // Favorite Content API
  async getFavoriteContent() {
    return this.request('/favorite_content')
  }

  async addFavoriteContent(contentData) {
    return this.request('/favorite_content', {
      method: 'POST',
      body: JSON.stringify(contentData),
    })
  }

  async removeFavoriteContent(favoriteId) {
    return this.request(`/favorite_content/${favoriteId}`, {
      method: 'DELETE',
    })
  }

  async checkFavoriteContent(contentId) {
    return this.request(`/favorite_content/check?content_id=${contentId}`)
  }

  // Providers API
  async getProviders() {
    return this.request('/ai_providers')
  }

  async getProviderModels(provider) {
    // This would require implementing a specific endpoint
    // For now, we can get models from the providers list
    const providers = await this.getProviders()
    const providerInfo = providers.find(p => p.name === provider)
    return providerInfo ? providerInfo.models : []
  }

  async testProvider(configId) {
    return this.request(`/ai_configs/${configId}/test`, {
      method: 'POST'
    })
  }

  // Characters API
  async getCharacters(userId) {
    return this.request(`/characters?user_id=${userId}`)
  }

  async createCharacter(characterData) {
    return this.request('/characters', {
      method: 'POST',
      body: JSON.stringify(characterData),
    })
  }

  async updateCharacter(characterId, characterData) {
    return this.request(`/characters/${characterId}`, {
      method: 'PUT',
      body: JSON.stringify(characterData),
    })
  }

  async deleteCharacter(characterId) {
    return this.request(`/characters/${characterId}`, {
      method: 'DELETE',
    })
  }

  async getCharacterTemplates() {
    return this.request('/characters/templates')
  }

  // Content Templates API
  async getContentTemplates() {
    return this.request('/content/templates')
  }
}

export const apiService = new ApiService()
export default apiService

