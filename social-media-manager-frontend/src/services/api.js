const API_BASE_URL = 'https://5000-i540tybl1fxpgt1rl4jex-81b4f8a2.manusvm.computer/api'

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'API request failed')
      }
      
      return data
    } catch (error) {
      console.error('API request error:', error)
      throw error
    }
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

  // Content Generation API
  async generateContent(contentData) {
    return this.request('/content/generate', {
      method: 'POST',
      body: JSON.stringify(contentData),
    })
  }

  async generateContentVariations(contentData) {
    return this.request('/content/generate/variations', {
      method: 'POST',
      body: JSON.stringify(contentData),
    })
  }

  async generateHashtags(hashtagData) {
    return this.request('/content/hashtags', {
      method: 'POST',
      body: JSON.stringify(hashtagData),
    })
  }

  async optimizeContent(optimizeData) {
    return this.request('/content/optimize', {
      method: 'POST',
      body: JSON.stringify(optimizeData),
    })
  }

  async getContentTemplates() {
    return this.request('/content/templates')
  }

  async analyzeContent(analyzeData) {
    return this.request('/content/analyze', {
      method: 'POST',
      body: JSON.stringify(analyzeData),
    })
  }

  // Users API
  async getUsers() {
    return this.request('/users')
  }

  async createUser(userData) {
    return this.request('/users', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async getUser(userId) {
    return this.request(`/users/${userId}`)
  }

  async updateUser(userId, userData) {
    return this.request(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    })
  }

  async deleteUser(userId) {
    return this.request(`/users/${userId}`, {
      method: 'DELETE',
    })
  }
}

export const apiService = new ApiService()
export default apiService

