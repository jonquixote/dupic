import { Link, useLocation } from 'react-router-dom'
import { 
  BarChart3, 
  TrendingUp, 
  PenTool, 
  Settings, 
  Home,
  Zap
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Trends', href: '/trends', icon: TrendingUp },
  { name: 'Content Generator', href: '/content', icon: PenTool },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export function Sidebar({ isOpen }) {
  const location = useLocation()

  return (
    <div className={cn(
      "bg-white shadow-lg transition-all duration-300 ease-in-out",
      isOpen ? "w-64" : "w-16"
    )}>
      <div className="flex items-center justify-center h-16 px-4 border-b">
        <div className="flex items-center space-x-2">
          <Zap className="h-8 w-8 text-blue-600" />
          {isOpen && (
            <span className="text-xl font-bold text-gray-900">
              AI Social Manager
            </span>
          )}
        </div>
      </div>
      
      <nav className="mt-8">
        <div className="px-2 space-y-1">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors",
                  isActive
                    ? "bg-blue-100 text-blue-900"
                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                )}
              >
                <item.icon
                  className={cn(
                    "mr-3 h-5 w-5 flex-shrink-0",
                    isActive ? "text-blue-500" : "text-gray-400 group-hover:text-gray-500"
                  )}
                />
                {isOpen && item.name}
              </Link>
            )
          })}
        </div>
      </nav>
    </div>
  )
}

