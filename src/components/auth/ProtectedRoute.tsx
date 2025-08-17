/**
 * @description 
 * Higher Order Component (HOC) that wraps protected content and enforces authentication.
 * Displays the AuthModal when users are not authenticated and preserves the
 * requested URL for post-login redirection.
 * 
 * Key features:
 * - Automatic auth check on mount and route changes
 * - Loading state while checking authentication
 * - Preserves requested URL in sessionStorage for redirect
 * - Shows AuthModal for unauthenticated users
 * - Renders children only when authenticated
 * 
 * @dependencies
 * - @/contexts/AuthContext: Authentication state and operations
 * - @/components/auth/AuthModal: Modal for login/signup
 * - react-router-dom: Location tracking for redirects
 * - lucide-react: Loading spinner icon
 * 
 * @notes
 * - Redirect URLs stored in sessionStorage (lost on browser close)
 * - TODO: Consider localStorage + TTL if deep-link persistence becomes critical
 * - Loading state prevents content flash during auth check
 * - Modal auto-opens for unauthenticated users
 */

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useLocation } from 'react-router-dom';
import { AuthModal } from './AuthModal';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

/**
 * ProtectedRoute component - Enforces authentication for wrapped content
 * @param children - Content to protect behind authentication
 */
export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading, checkSession } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const location = useLocation();

  /**
   * Check authentication status and manage modal display
   */
  useEffect(() => {
    // Store the attempted URL for post-login redirect
    // NOTE: Using sessionStorage means redirect is lost on browser close
    // TODO: Consider localStorage + TTL if deep-link persistence becomes critical
    if (!isAuthenticated && !loading) {
      // Save current path for redirect after login
      sessionStorage.setItem('redirectUrl', location.pathname);
      setShowAuthModal(true);
    } else if (isAuthenticated) {
      // Hide modal if user is authenticated
      setShowAuthModal(false);
    }
  }, [isAuthenticated, loading, location]);

  /**
   * Refresh session when location changes (optional enhancement)
   * This ensures fresh auth state on navigation
   */
  useEffect(() => {
    // Only check session if not already loading
    if (!loading) {
      checkSession();
    }
  }, [location.pathname]); // Re-check on route change

  /**
   * Render loading state while checking authentication
   * This prevents content flash and provides better UX
   */
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  /**
   * Not authenticated - show modal with backdrop
   * The backdrop content provides context while modal is open
   */
  if (!isAuthenticated) {
    return (
      <>
        {/* Background content while modal is open */}
        <div className="min-h-screen flex items-center justify-center bg-background">
          <div className="text-center p-8 max-w-md">
            <h1 className="text-2xl font-bold mb-4">Authentication Required</h1>
            <p className="text-muted-foreground mb-6">
              Please sign in to access Module Mind course content. 
              All authenticated users get immediate access to the full curriculum.
            </p>
            {/* This button is mostly for accessibility/screen readers since modal auto-opens */}
            <button
              onClick={() => setShowAuthModal(true)}
              className="text-primary hover:underline focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded"
              aria-label="Open sign in modal"
            >
              Click here to sign in
            </button>
          </div>
        </div>
        
        {/* Auth modal - cannot be dismissed without authentication */}
        <AuthModal 
          isOpen={showAuthModal} 
          onClose={() => {
            // Only close if authenticated
            // This callback is called by AuthModal when auth succeeds
            if (isAuthenticated) {
              setShowAuthModal(false);
            }
          }}
        />
      </>
    );
  }

  /**
   * Authenticated - render protected content
   * At this point, user has valid session and can access content
   */
  return <>{children}</>;
}