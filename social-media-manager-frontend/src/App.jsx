import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Sidebar } from '@/components/Sidebar'
import { Header } from '@/components/Header'
import { Dashboard } from '@/components/Dashboard'
import { TrendsPage } from '@/components/TrendsPage'
import { ContentGenerator } from '@/components/ContentGenerator'
import { Analytics } from '@/components/Analytics'
import { Settings } from '@/components/Settings'
import { CharacterProfiles } from '@/components/CharacterProfiles'
import { AIConfigurations } from '@/components/AIConfigurations'
import AIConfig from '@/components/AIConfig'
import { VideoAnalysis } from '@/components/VideoAnalysis'
import './styles/App.css'
import './styles/2050-theme.css'

// Floating particles component
const FloatingParticles = () => {
  const [particles, setParticles] = useState([])

  useEffect(() => {
    const generateParticles = () => {
      const newParticles = []
      for (let i = 0; i < 50; i++) {
        newParticles.push({
          id: i,
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          delay: Math.random() * 6
        })
      }
      setParticles(newParticles)
    }

    generateParticles()
    window.addEventListener('resize', generateParticles)
    return () => window.removeEventListener('resize', generateParticles)
  }, [])

  return (
    <div className="floating-particles">
      {particles.map(particle => (
        <div
          key={particle.id}
          className="particle"
          style={{
            left: `${particle.x}px`,
            top: `${particle.y}px`,
            animationDelay: `${particle.delay}s`
          }}
        />
      ))}
    </div>
  )
}

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="flex h-screen text-white overflow-hidden relative" style={{ background: 'var(--primary-bg)' }}>
        {/* Cyberpunk Grid Background */}
        <div className="fixed inset-0 cyber-grid opacity-30 pointer-events-none"></div>
        
        {/* Floating Particles */}
        <FloatingParticles />
        
        {/* Scan Lines Effect */}
        <div className="fixed inset-0 scan-lines pointer-events-none opacity-20"></div>
        
        {/* Enhanced Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-4 -left-4 w-96 h-96 rounded-full mix-blend-multiply filter blur-3xl opacity-20 gradient-animated"></div>
          <div className="absolute -bottom-8 -right-4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-pulse" style={{ animationDelay: '2s' }}></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-pulse" style={{ animationDelay: '4s' }}></div>
          <div className="absolute top-1/4 right-1/4 w-72 h-72 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-15 animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <Sidebar isOpen={sidebarOpen} />
        <div className="flex-1 flex flex-col overflow-hidden relative z-10">
          <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
          <main className="flex-1 overflow-x-hidden overflow-y-auto p-6 backdrop-blur-sm">
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/trends" element={<TrendsPage />} />
                <Route path="/content" element={<ContentGenerator />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/characters" element={<CharacterProfiles />} />
                <Route path="/ai-config" element={<AIConfig />} />
                <Route path="/video-analysis" element={<VideoAnalysis />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
