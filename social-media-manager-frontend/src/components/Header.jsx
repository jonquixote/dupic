import { useState } from 'react'
import { Menu, Search, Bell, User, Zap, Settings } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

export function Header({ onMenuClick }) {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <header className="glass-dark border-b border-white/10 relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-cyan-500/10 animate-shimmer"></div>
      
      <div className="relative z-10 flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-6">
          <Button
            variant="ghost"
            size="sm"
            onClick={onMenuClick}
            className="btn-secondary-2050 p-2 hover:glow-blue"
          >
            <Menu className="h-5 w-5" />
          </Button>
          
          <div className="relative w-96">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-blue-400" />
            <Input
              type="text"
              placeholder="Search trends, content, analytics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-2050 pl-10 pr-4 py-2 w-full text-white placeholder-gray-400"
            />
          </div>

          {/* AI Status Indicator */}
          <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-green-500/20 border border-green-500/30">
            <Zap className="h-4 w-4 text-green-400 animate-pulse" />
            <span className="text-xs font-medium text-green-400">AI Active</span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Notifications with glow effect */}
          <Button variant="ghost" size="sm" className="btn-secondary-2050 p-2 relative">
            <Bell className="h-5 w-5" />
            <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full animate-pulse"></span>
          </Button>

          {/* Settings */}
          <Button variant="ghost" size="sm" className="btn-secondary-2050 p-2">
            <Settings className="h-5 w-5" />
          </Button>

          {/* User Profile Dropdown */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="btn-secondary-2050 p-2 relative">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
                <div className="absolute -bottom-1 -right-1 h-3 w-3 bg-green-500 rounded-full border-2 border-gray-900"></div>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56 glass-dark border-white/20 text-white">
              <DropdownMenuLabel className="text-gradient-blue">My Account</DropdownMenuLabel>
              <DropdownMenuSeparator className="bg-white/20" />
              <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                <User className="mr-2 h-4 w-4" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                <Settings className="mr-2 h-4 w-4" />
                Settings
              </DropdownMenuItem>
              <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                <Zap className="mr-2 h-4 w-4" />
                AI Configuration
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-white/20" />
              <DropdownMenuItem className="hover:bg-red-500/20 focus:bg-red-500/20 text-red-400">
                Log out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  )
}

