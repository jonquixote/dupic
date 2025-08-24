import React, { useState, useEffect } from 'react';
import '../styles/2050-theme.css';

const AIConfig = () => {
  const [providers, setProviders] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState('openai');
  const [models, setModels] = useState([]);

  useEffect(() => {
    fetchProviders();
  }, []);

  useEffect(() => {
    if (selectedProvider) {
      fetchModels(selectedProvider);
    }
  }, [selectedProvider]);

  const fetchProviders = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/providers');
      const data = await response.json();
      if (data.success) {
        setProviders(data.providers);
      }
    } catch (error) {
      console.error('Error fetching providers:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchModels = async (provider) => {
    try {
      const response = await fetch(`http://localhost:5000/api/providers/${provider}/models`);
      const data = await response.json();
      if (data.success) {
        setModels(data.models);
      }
    } catch (error) {
      console.error('Error fetching models:', error);
    }
  };

  const getProviderIcon = (provider) => {
    const icons = {
      openai: '🤖',
      groq: '⚡',
      gemini: '💎',
      cerebras: '🧠',
      openrouter: '🌐'
    };
    return icons[provider] || '🔧';
  };

  const getProviderColor = (provider) => {
    const colors = {
      openai: 'from-green-400 to-blue-500',
      groq: 'from-yellow-400 to-orange-500',
      gemini: 'from-purple-400 to-pink-500',
      cerebras: 'from-red-400 to-pink-500',
      openrouter: 'from-blue-400 to-cyan-500'
    };
    return colors[provider] || 'from-gray-400 to-gray-600';
  };

  if (loading) {
    return (
      <div className="ai-config-container">
        <div className="loading-spinner">
          <div className="holographic-text">Loading AI Providers...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="ai-config-container">
      <div className="page-header">
        <h1 className="holographic-text">AI Configurations</h1>
        <p className="subtitle">Manage your AI provider settings and API keys</p>
        <button className="btn-primary neon-button">
          <span>+ Add Provider</span>
        </button>
      </div>

      <div className="providers-grid">
        {Object.entries(providers).map(([providerName, providerData]) => (
          <div 
            key={providerName}
            className={`provider-card glassmorphism ${selectedProvider === providerName ? 'selected' : ''}`}
            onClick={() => setSelectedProvider(providerName)}
          >
            <div className="provider-header">
              <div className="provider-icon">
                {getProviderIcon(providerName)}
              </div>
              <div className="provider-info">
                <h3 className="provider-name">{providerName.toUpperCase()}</h3>
                <div className={`status-badge ${providerData.available ? 'online' : 'offline'}`}>
                  {providerData.available ? 'Online' : 'Offline'}
                </div>
              </div>
            </div>

            <div className="provider-stats">
              <div className="stat-item">
                <span className="stat-label">Models</span>
                <span className="stat-value neon-text">{providerData.models_count}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Capabilities</span>
                <div className="capabilities-list">
                  {providerData.capabilities.map((capability, index) => (
                    <span key={index} className="capability-tag">
                      {capability}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="provider-actions">
              <button className="btn-secondary">Configure</button>
              <button className="btn-outline">Test</button>
            </div>
          </div>
        ))}
      </div>

      {selectedProvider && (
        <div className="models-section glassmorphism">
          <h2 className="section-title">Available Models - {selectedProvider.toUpperCase()}</h2>
          <div className="models-grid">
            {models.map((model, index) => (
              <div key={index} className="model-card">
                <div className="model-header">
                  <h4 className="model-name">{model.name}</h4>
                  <div className="model-tokens">
                    {model.max_tokens.toLocaleString()} tokens
                  </div>
                </div>
                <div className="model-capabilities">
                  {model.capabilities.map((capability, capIndex) => (
                    <span key={capIndex} className="capability-badge">
                      {capability}
                    </span>
                  ))}
                </div>
                <div className="model-actions">
                  <button className="btn-sm btn-primary">Select</button>
                  <button className="btn-sm btn-outline">Test</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="api-keys-section glassmorphism">
        <h2 className="section-title">API Keys Management</h2>
        <div className="api-keys-grid">
          {Object.entries(providers).map(([providerName, providerData]) => (
            <div key={providerName} className="api-key-item">
              <div className="api-key-header">
                <span className="provider-icon">{getProviderIcon(providerName)}</span>
                <span className="provider-name">{providerName.toUpperCase()}</span>
                <div className={`status-indicator ${providerData.available ? 'active' : 'inactive'}`}></div>
              </div>
              <div className="api-key-input">
                <input 
                  type="password" 
                  placeholder="Enter API key..."
                  className="input-field"
                  defaultValue={providerData.available ? '****-****-****-1234' : ''}
                />
                <button className="btn-sm btn-primary">Update</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="system-status glassmorphism">
        <h2 className="section-title">System Status</h2>
        <div className="status-grid">
          <div className="status-item">
            <div className="status-label">AI System</div>
            <div className="status-value online">Online</div>
          </div>
          <div className="status-item">
            <div className="status-label">Database</div>
            <div className="status-value online">Connected</div>
          </div>
          <div className="status-item">
            <div className="status-label">ML Services</div>
            <div className="status-value online">Initialized</div>
          </div>
          <div className="status-item">
            <div className="status-label">Performance</div>
            <div className="status-value">85%</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIConfig;

