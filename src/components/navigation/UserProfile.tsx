/**
 * @description 
 * User profile dropdown component that displays user information and actions.
 * Integrates with the authentication system to show real user data and
 * handle logout operations.
 * 
 * Key features:
 * - Displays user avatar with initials fallback
 * - Shows user name and email from auth context
 * - Handles logout with auth context integration
 * - Placeholder actions for profile and settings (future features)
 * 
 * @dependencies
 * - @/contexts/AuthContext: User data and logout functionality
 * - @/components/ui/*: Shadcn UI components
 * - lucide-react: Icons for menu items
 * 
 * @notes
 * - Profile and Settings clicks are placeholders for future features
 * - Avatar shows initials if no image URL is available
 * - Logout clears session and redirects to home
 */

import { User, Settings, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';

interface UserProfileProps {
  onProfileClick?: () => void;
  onSettingsClick?: () => void;
}

/**
 * UserProfile component - Displays user menu with profile info and actions
 * @param onProfileClick - Optional handler for profile click (future feature)
 * @param onSettingsClick - Optional handler for settings click (future feature)
 */
export function UserProfile({ 
  onProfileClick,
  onSettingsClick,
}: UserProfileProps) {
  const { user, signOut } = useAuth();
  const { toast } = useToast();
  
  // Get user data from auth context
  const userName = user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'User';
  const userEmail = user?.email || '';
  const avatarUrl = user?.user_metadata?.avatar_url;
  
  // Generate initials for avatar fallback
  const initials = userName
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2); // Max 2 characters for initials

  /**
   * Handle logout action
   */
  const handleLogout = async () => {
    try {
      await signOut();
      toast({
        title: "Signed out",
        description: "You have been successfully signed out.",
      });
    } catch (error) {
      console.error('Logout error:', error);
      toast({
        title: "Error",
        description: "Failed to sign out. Please try again.",
        variant: "destructive",
      });
    }
  };

  /**
   * Handle profile click - placeholder for future feature
   */
  const handleProfileClick = () => {
    if (onProfileClick) {
      onProfileClick();
    } else {
      toast({
        title: "Coming soon",
        description: "Profile management will be available in a future update.",
      });
    }
  };

  /**
   * Handle settings click - placeholder for future feature
   */
  const handleSettingsClick = () => {
    if (onSettingsClick) {
      onSettingsClick();
    } else {
      toast({
        title: "Coming soon",
        description: "Settings will be available in a future update.",
      });
    }
  };

  // Don't render if no user (shouldn't happen with ProtectedRoute, but defensive)
  if (!user) {
    return null;
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button 
          variant="ghost" 
          className="h-9 w-9 rounded-full p-0 hover:ring-2 hover:ring-primary hover:ring-offset-2 transition-all"
          aria-label="User menu"
        >
          <Avatar className="h-8 w-8">
            <AvatarImage src={avatarUrl} alt={userName} />
            <AvatarFallback className="bg-primary text-primary-foreground text-sm font-medium">
              {initials}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56 bg-background border border-border">
        {/* User info header */}
        <div className="flex items-center space-x-2 p-2">
          <Avatar className="h-8 w-8">
            <AvatarImage src={avatarUrl} alt={userName} />
            <AvatarFallback className="bg-primary text-primary-foreground text-sm font-medium">
              {initials}
            </AvatarFallback>
          </Avatar>
          <div className="flex flex-col space-y-1 overflow-hidden">
            <div className="text-sm font-medium text-foreground truncate">{userName}</div>
            <div className="text-xs text-muted-foreground truncate">{userEmail}</div>
          </div>
        </div>
        
        <DropdownMenuSeparator />
        
        {/* Profile action - placeholder for future */}
        <DropdownMenuItem 
          onClick={handleProfileClick} 
          className="cursor-pointer hover:bg-accent"
        >
          <User className="mr-2 h-4 w-4" />
          <span>Profile</span>
        </DropdownMenuItem>
        
        {/* Settings action - placeholder for future */}
        <DropdownMenuItem 
          onClick={handleSettingsClick} 
          className="cursor-pointer hover:bg-accent"
        >
          <Settings className="mr-2 h-4 w-4" />
          <span>Settings</span>
        </DropdownMenuItem>
        
        <DropdownMenuSeparator />
        
        {/* Logout action */}
        <DropdownMenuItem 
          onClick={handleLogout} 
          className="cursor-pointer hover:bg-accent text-destructive focus:text-destructive"
        >
          <LogOut className="mr-2 h-4 w-4" />
          <span>Log out</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}