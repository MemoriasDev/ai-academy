/**
 * @description 
 * Enhanced AuthContext with comprehensive session management for Module Mind.
 * Handles authentication state, session persistence, automatic token refresh,
 * and redirect URL preservation for post-login navigation.
 * 
 * Key features:
 * - Automatic session restoration on app load
 * - Token refresh before expiry (5 minutes before)
 * - Redirect URL preservation for protected routes
 * - Cross-tab session synchronization via Supabase
 * - Comprehensive error handling and user feedback
 * 
 * @dependencies
 * - @supabase/supabase-js: Authentication and session management
 * - react-router-dom: Navigation after auth events
 * - @/lib/supabase: Configured Supabase client
 * 
 * @notes
 * - Sessions persist for 7 days (Supabase default with refresh tokens)
 * - Access tokens are short-lived (1 hour) and auto-refresh
 * - Redirect URLs use sessionStorage (lost on browser close)
 * - For MVP, all authenticated users have course access (no RBAC)
 */

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { User, Session, AuthError } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';
import { useNavigate } from 'react-router-dom';

/**
 * Complete AuthContext type definition with all auth operations
 */
interface AuthContextType {
  // State
  user: User | null;
  session: Session | null;
  loading: boolean;
  error: AuthError | null;
  
  // Actions
  signIn: (email: string, password: string) => Promise<{ error: AuthError | null }>;
  signUp: (email: string, password: string, metadata?: { full_name?: string }) => Promise<{ error: AuthError | null }>;
  signOut: () => Promise<void>;
  clearError: () => void;
  
  // Utilities
  isAuthenticated: boolean;
  checkSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * AuthProvider component that wraps the app and provides auth state
 * Must be placed INSIDE BrowserRouter to use useNavigate hook
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<AuthError | null>(null);
  const navigate = useNavigate();

  /**
   * Check and restore session from Supabase
   * Called on mount and can be called manually to refresh session
   */
  const checkSession = useCallback(async () => {
    try {
      setLoading(true);
      const { data: { session }, error } = await supabase.auth.getSession();
      
      if (error) {
        console.error('Session check error:', error);
        throw error;
      }
      
      setSession(session);
      setUser(session?.user ?? null);
    } catch (err) {
      console.error('Session check failed:', err);
      setSession(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Set up auth state listener and token refresh
   */
  useEffect(() => {
    // Initial session check
    checkSession();

    // Listen for auth state changes (login, logout, token refresh, etc.)
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        // Auth event handled
        
        // Update local state
        setSession(session);
        setUser(session?.user ?? null);
        
        // Handle different auth events
        switch (event) {
          case 'SIGNED_IN':
            // Clear any previous errors
            setError(null);
            
            // Check for stored redirect URL (from ProtectedRoute)
            const redirectUrl = sessionStorage.getItem('redirectUrl');
            if (redirectUrl) {
              sessionStorage.removeItem('redirectUrl');
              // Use navigate to redirect to the originally requested page
              navigate(redirectUrl);
            } else {
              // Default redirect to home
              navigate('/');
            }
            break;
            
          case 'SIGNED_OUT':
            // Clear user data
            setUser(null);
            setSession(null);
            // Clear any app-specific storage
            localStorage.removeItem('lastAccessedLesson');
            sessionStorage.clear();
            break;
            
          case 'TOKEN_REFRESHED':
            // Token was successfully refreshed
            // Token refreshed successfully
            break;
            
          case 'USER_UPDATED':
            // User metadata was updated
            setUser(session?.user ?? null);
            break;
            
          case 'PASSWORD_RECOVERY':
            // User clicked password recovery link
            // Password recovery initiated
            break;
        }
        
        setLoading(false);
      }
    );

    // Set up automatic token refresh check
    // Check every minute if token needs refreshing
    const refreshInterval = setInterval(async () => {
      if (session?.expires_at) {
        const expiresAt = new Date(session.expires_at * 1000);
        const now = new Date();
        const timeUntilExpiry = expiresAt.getTime() - now.getTime();
        
        // Refresh if less than 5 minutes until expiry
        if (timeUntilExpiry < 5 * 60 * 1000 && timeUntilExpiry > 0) {
          // Refreshing token proactively
          const { data, error } = await supabase.auth.refreshSession();
          
          if (error) {
            console.error('Token refresh failed:', error);
            // Force re-authentication if refresh fails
            setError(error);
            await signOut();
          } else if (data.session) {
            setSession(data.session);
            setUser(data.session.user);
          }
        }
      }
    }, 60000); // Check every minute

    // Cleanup
    return () => {
      subscription.unsubscribe();
      clearInterval(refreshInterval);
    };
  }, [navigate, checkSession, session?.expires_at]);

  /**
   * Sign in with email and password
   * Returns error object for UI handling
   */
  const signIn = async (email: string, password: string): Promise<{ error: AuthError | null }> => {
    try {
      setError(null);
      setLoading(true);
      
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        setError(error);
        return { error };
      }

      // Session update will be handled by onAuthStateChange listener
      return { error: null };
    } catch (err) {
      const authError = err as AuthError;
      setError(authError);
      return { error: authError };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Sign up with email, password, and optional metadata
   * For MVP, auto-signs in after signup (no email verification required)
   */
  const signUp = async (
    email: string, 
    password: string, 
    metadata?: { full_name?: string }
  ): Promise<{ error: AuthError | null }> => {
    try {
      setError(null);
      setLoading(true);
      
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: metadata,
          // For MVP, we're not requiring email confirmation
          // In production, you might want to set emailRedirectTo
          emailRedirectTo: window.location.origin,
        },
      });

      if (error) {
        setError(error);
        return { error };
      }

      // For MVP with email confirmation disabled, 
      // user is automatically signed in after signup
      if (data.user && !data.session) {
        // If no session returned, try to sign in automatically
        // This happens when email confirmation is required but we want to bypass for MVP
        // No session returned from signup, attempting auto-signin
        
        // Wait a brief moment for the user to be fully created
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Attempt to sign in with the credentials
        const signInResult = await signIn(email, password);
        
        // If sign in fails, it might be because email confirmation is required
        if (signInResult.error) {
          // Auto-signin failed, email confirmation may be required
          // Return success anyway since user was created
          // Show a message about email confirmation
          return { 
            error: {
              message: 'Account created! Please check your email to confirm your account, then sign in.',
              status: 200
            } as any
          };
        }
        
        return signInResult;
      }
      
      // If we got both user and session, everything worked!
      if (data.user && data.session) {
        // Signup successful with immediate session
      }

      return { error: null };
    } catch (err) {
      const authError = err as AuthError;
      setError(authError);
      return { error: authError };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Sign out the current user
   * Clears all auth state and app-specific storage
   */
  const signOut = async (): Promise<void> => {
    try {
      setLoading(true);
      const { error } = await supabase.auth.signOut();
      
      if (error) {
        console.error('Sign out error:', error);
        throw error;
      }
      
      // Clear all auth state
      setUser(null);
      setSession(null);
      setError(null);
      
      // Clear any app-specific storage
      localStorage.removeItem('lastAccessedLesson');
      sessionStorage.clear();
      
      // Navigate to home page
      navigate('/');
    } catch (err) {
      console.error('Sign out error:', err);
      // Even if sign out fails, clear local state
      setUser(null);
      setSession(null);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Clear any auth errors
   * Used by UI components to clear error state
   */
  const clearError = () => setError(null);

  /**
   * Computed property for authentication status
   */
  const isAuthenticated = !!user;

  const value: AuthContextType = {
    // State
    user,
    session,
    loading,
    error,
    
    // Actions
    signIn,
    signUp,
    signOut,
    clearError,
    
    // Utilities
    isAuthenticated,
    checkSession,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

/**
 * Hook to use auth context in components
 * Must be used within AuthProvider
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};