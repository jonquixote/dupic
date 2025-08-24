import { Link, useLocation } from 'react-router-dom'
import { 
  BarChart3, 
  TrendingUp, 
  PenTool, 
  Settings, 
  Home,
  Zap,
  Users,
  Brain,
  Video,
  Sparkles
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Trends', href: '/trends', icon: TrendingUp },
  { name: 'Content Generator', href: '/content', icon: PenTool },
  { name: 'Character Profiles', href: '/characters', icon: Users },
  { name: 'Video Analysis', href: '/video-analysis', icon: Video },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'AI Configuration', href: '/ai-config', icon: Brain },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar({ isOpen }) {
  const location = useLocation()

  return (
    <div className={cn(
      "glass-dark border-r border-white/10 transition-all duration-300 ease-in-out relative overflow-hidden",
      isOpen ? "w-64" : "w-16"
    )}>
      {/* Animated sidebar glow */}
      <div className="absolute inset-y-0 right-0 w-px bg-gradient-to-b from-transparent via-blue-500/50 to-transparent"></div>
      
      {/* Logo Section */}
      <div className="flex items-center justify-center h-16 px-4 border-b border-white/10 relative">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Sparkles className="h-8 w-8 text-blue-400 animate-pulse" />
            <div className="absolute inset-0 h-8 w-8 bg-blue-400 rounded-full blur-md opacity-30 animate-pulse"></div>
          </div>
          {isOpen && (
            <div className="flex flex-col">
              <span className="text-lg font-bold text-gradient-blue">
                DUPIC
              </span>
              <span className="text-xs text-gray-400 -mt-1">
                AI Social Manager
              </span>
            </div>
          )}
        </div>
      </div>
      
      {/* Navigation */}
      <nav className="mt-8 px-2">
        <div className="space-y-2">
          {navigation.map((item, index) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all duration-300 relative overflow-hidden",
                  isActive
                    ? "bg-gradient-to-r from-blue-500/20 to-purple-500/20 text-white border border-blue-500/30 glow-blue"
                    : "text-gray-300 hover:bg-white/5 hover:text-white hover:border-white/20 border border-transparent"
                )}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Active indicator */}
                {isActive && (
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-blue-400 to-purple-400 rounded-r-full"></div>
                )}
                
                {/* Icon with glow effect */}
                <div className="relative">
                  <item.icon
                    className={cn(
                      "h-5 w-5 flex-shrink-0 transition-all duration-300",
                      isActive 
                        ? "text-blue-400" 
                        : "text-gray-400 group-hover:text-blue-400"
                    )}
                  />
                  {isActive && (
                    <div className="absolute inset-0 h-5 w-5 bg-blue-400 rounded-full blur-sm opacity-30"></div>
                  )}
                </div>
                
                {/* Navigation text */}
                {isOpen && (
                  <span className={cn(
                    "ml-3 transition-all duration-300",
                    isActive ? "text-white" : "group-hover:text-white"
                  )}>
                    {item.name}
                  </span>
                )}
                
                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/0 via-blue-500/5 to-purple-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </Link>
            )
          })}
        </div>
      </nav>

      {/* Bottom Section - AI Status */}
      {isOpen && (
        <div className="absolute bottom-4 left-2 right-2">
          <div className="card-2050 p-3">
            <div className="flex items-center space-x-2 mb-2">
              <Brain className="h-4 w-4 text-green-400 animate-pulse" />
              <span className="text-xs font-medium text-green-400">AI System</span>
            </div>
            <div className="text-xs text-gray-400 mb-2">Status: Online</div>
            <div className="w-full bg-gray-700 rounded-full h-1">
              <div className="bg-gradient-to-r from-green-400 to-blue-400 h-1 rounded-full animate-pulse" style={{width: '85%'}}></div>
            </div>
            <div className="text-xs text-gray-500 mt-1">Performance: 85%</div>
          </div>
        </div>
      )}
    </div>
  )
}

