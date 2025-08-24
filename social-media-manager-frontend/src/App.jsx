import { useState } from 'react'
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
import { VideoAnalysis } from '@/components/VideoAnalysis'
import './App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <Router>
      <div className="flex h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white overflow-hidden">
        {/* Animated background particles */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-4 -left-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-8 -right-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse animation-delay-4000"></div>
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
                <Route path="/ai-config" element={<AIConfigurations />} />
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

