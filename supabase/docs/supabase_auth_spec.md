# Technical Specification: Module Mind MVP Authentication System

## 1. System Architecture

### 1.1 High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                         Client (React)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   App.tsx   │──│  AuthProvider │──│  ProtectedRoute  │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
│         │                 │                    │            │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │  AuthModal  │  │   useAuth    │  │  CourseLayout    │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Supabase Backend                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Auth Service│  │  PostgreSQL  │  │  Storage Service │  │
│  │  (JWT)       │  │  (Profiles)  │  │  (Videos)        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Component Dependencies
```typescript
// Dependency tree
App.tsx
├── AuthProvider (wraps entire app)
│   ├── Supabase Client
│   └── Auth State Management
├── Router
│   ├── ProtectedRoute (HOC)
│   │   ├── AuthModal (conditionally rendered)
│   │   └── Protected Content (CourseLayout, etc.)
│   └── Public Routes (if any)
```

## 2. Database Schema Updates

### 2.1 SQL Migrations for MVP
```sql
-- Simplify RLS policies for MVP (all authenticated users have access)

-- Verify bucket exists before applying policies
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM storage.buckets WHERE id = 'course-videos'
  ) THEN
    RAISE EXCEPTION 'Bucket course-videos does not exist. Please create it first.';
  END IF;
END $$;

-- Drop existing complex policies
DROP POLICY IF EXISTS "Authenticated users can access cohort_2 videos" ON storage.objects;

-- Create simplified policy for MVP (with explicit bucket path scoping)
CREATE POLICY "Authenticated users can access all videos"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'course-videos'
  AND auth.role() = 'authenticated'
  AND (storage.foldername(name))[1] = 'course-videos'
);

-- Ensure profiles trigger exists and works
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, created_at, updated_at)
  VALUES (
    new.id, 
    new.email, 
    COALESCE(new.raw_user_meta_data->>'full_name', ''),
    NOW(),
    NOW()
  )
  ON CONFLICT (id) DO UPDATE
  SET 
    email = EXCLUDED.email,
    updated_at = NOW();
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Ensure trigger is attached
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## 3. Component Specifications

### 3.1 AuthProvider Enhancement
```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { User, Session, AuthError } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';
import { useNavigate } from 'react-router-dom';

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

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<AuthError | null>(null);
  const navigate = useNavigate();

  // Initialize and check session
  const checkSession = useCallback(async () => {
    try {
      setLoading(true);
      const { data: { session }, error } = await supabase.auth.getSession();
      
      if (error) throw error;
      
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

  // Set up auth listener
  useEffect(() => {
    // Initial session check
    checkSession();

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        console.log('Auth event:', event);
        
        setSession(session);
        setUser(session?.user ?? null);
        
        // Handle different auth events
        switch (event) {
          case 'SIGNED_IN':
            // Redirect to stored URL or default
            const redirectUrl = sessionStorage.getItem('redirectUrl') || '/';
            sessionStorage.removeItem('redirectUrl');
            navigate(redirectUrl);
            break;
          case 'SIGNED_OUT':
            setUser(null);
            setSession(null);
            break;
          case 'TOKEN_REFRESHED':
            console.log('Token refreshed successfully');
            break;
          case 'USER_UPDATED':
            setUser(session?.user ?? null);
            break;
        }
        
        setLoading(false);
      }
    );

    return () => {
      subscription.unsubscribe();
    };
  }, [navigate, checkSession]);

  // Sign in with email/password
  const signIn = async (email: string, password: string) => {
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

      return { error: null };
    } finally {
      setLoading(false);
    }
  };

  // Sign up with email/password
  const signUp = async (
    email: string, 
    password: string, 
    metadata?: { full_name?: string }
  ) => {
    try {
      setError(null);
      setLoading(true);
      
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: metadata,
          emailRedirectTo: window.location.origin,
        },
      });

      if (error) {
        setError(error);
        return { error };
      }

      // Auto sign in after signup (MVP)
      if (data.user && !data.session) {
        // If email confirmation is disabled, sign in immediately
        return signIn(email, password);
      }

      return { error: null };
    } finally {
      setLoading(false);
    }
  };

  // Sign out
  const signOut = async () => {
    try {
      setLoading(true);
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      
      // Clear any app-specific storage
      localStorage.removeItem('lastAccessedLesson');
      sessionStorage.clear();
      
      navigate('/');
    } catch (err) {
      console.error('Sign out error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => setError(null);

  const value: AuthContextType = {
    user,
    session,
    loading,
    error,
    signIn,
    signUp,
    signOut,
    clearError,
    isAuthenticated: !!user,
    checkSession,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### 3.2 AuthModal Component
```typescript
// src/components/auth/AuthModal.tsx
import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';

interface AuthModalProps {
  isOpen: boolean;
  onClose?: () => void; // Optional, as it shouldn't close without auth
}

export function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const { signIn, signUp, loading, error, clearError, isAuthenticated } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [localError, setLocalError] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState('signin');

  // Close modal when authenticated
  useEffect(() => {
    if (isAuthenticated && onClose) {
      onClose();
    }
  }, [isAuthenticated, onClose]);

  // Clear errors when switching tabs
  useEffect(() => {
    clearError();
    setLocalError('');
  }, [activeTab, clearError]);

  const validateForm = (isSignUp: boolean = false): boolean => {
    if (!email || !email.includes('@')) {
      setLocalError('Please enter a valid email address');
      return false;
    }
    if (!password || password.length < 6) {
      setLocalError('Password must be at least 6 characters');
      return false;
    }
    if (isSignUp && !fullName) {
      setLocalError('Please enter your name');
      return false;
    }
    return true;
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setIsSubmitting(true);
    setLocalError('');
    
    const { error } = await signIn(email, password);
    
    if (error) {
      if (error.message.includes('Invalid login credentials')) {
        setLocalError('Invalid email or password');
      } else {
        setLocalError(error.message);
      }
    }
    
    setIsSubmitting(false);
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm(true)) return;

    setIsSubmitting(true);
    setLocalError('');
    
    const { error } = await signUp(email, password, { full_name: fullName });
    
    if (error) {
      if (error.message.includes('already registered')) {
        setLocalError('An account with this email already exists');
      } else {
        setLocalError(error.message);
      }
    }
    
    setIsSubmitting(false);
  };

  const displayError = localError || error?.message;

  return (
    <Dialog open={isOpen} onOpenChange={() => {
      // Security: Modal must not be dismissible without authentication
      // This empty handler prevents escape key and backdrop click from closing
    }}>
      <DialogContent 
        className="sm:max-w-[425px]" 
        onPointerDownOutside={(e) => e.preventDefault()}
        onEscapeKeyDown={(e) => e.preventDefault()}
      >
        <DialogHeader>
          <DialogTitle>Welcome to Module Mind</DialogTitle>
          <DialogDescription>
            Sign in to access your AI/LLM course content
          </DialogDescription>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="signin">Sign In</TabsTrigger>
            <TabsTrigger value="signup">Sign Up</TabsTrigger>
          </TabsList>

          <TabsContent value="signin" className="space-y-4">
            <form onSubmit={handleSignIn} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signin-email">Email</Label>
                <Input
                  id="signin-email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isSubmitting}
                  required
                  autoComplete="email"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="signin-password">Password</Label>
                <Input
                  id="signin-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isSubmitting}
                  required
                  autoComplete="current-password"
                />
              </div>

              {displayError && (
                <Alert variant="destructive">
                  <AlertDescription>{displayError}</AlertDescription>
                </Alert>
              )}

              <Button 
                type="submit" 
                className="w-full" 
                disabled={isSubmitting || loading}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Signing in...
                  </>
                ) : (
                  'Sign In'
                )}
              </Button>
            </form>
          </TabsContent>

          <TabsContent value="signup" className="space-y-4">
            <form onSubmit={handleSignUp} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signup-name">Full Name</Label>
                <Input
                  id="signup-name"
                  type="text"
                  placeholder="John Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  disabled={isSubmitting}
                  required
                  autoComplete="name"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="signup-email">Email</Label>
                <Input
                  id="signup-email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isSubmitting}
                  required
                  autoComplete="email"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="signup-password">Password</Label>
                <Input
                  id="signup-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={isSubmitting}
                  required
                  minLength={6}
                  autoComplete="new-password"
                />
                <p className="text-xs text-muted-foreground">
                  Minimum 6 characters
                </p>
              </div>

              {displayError && (
                <Alert variant="destructive">
                  <AlertDescription>{displayError}</AlertDescription>
                </Alert>
              )}

              <Button 
                type="submit" 
                className="w-full" 
                disabled={isSubmitting || loading}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Creating account...
                  </>
                ) : (
                  'Sign Up'
                )}
              </Button>

              <p className="text-xs text-center text-muted-foreground">
                By signing up, you'll get immediate access to all course content
              </p>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
```

### 3.3 ProtectedRoute Component
```typescript
// src/components/auth/ProtectedRoute.tsx
import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useLocation } from 'react-router-dom';
import { AuthModal } from './AuthModal';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, loading, checkSession } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const location = useLocation();

  useEffect(() => {
    // Store the attempted URL for post-login redirect
    // NOTE: Using sessionStorage means redirect is lost on browser close
    // TODO: Consider localStorage + TTL if deep-link persistence becomes critical
    if (!isAuthenticated && !loading) {
      sessionStorage.setItem('redirectUrl', location.pathname);
      setShowAuthModal(true);
    } else if (isAuthenticated) {
      setShowAuthModal(false);
    }
  }, [isAuthenticated, loading, location]);

  // Initial loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Not authenticated - show modal
  if (!isAuthenticated) {
    return (
      <>
        <div className="min-h-screen flex items-center justify-center bg-background">
          <div className="text-center p-8">
            <h1 className="text-2xl font-bold mb-4">Authentication Required</h1>
            <p className="text-muted-foreground mb-6">
              Please sign in to access course content
            </p>
            <button
              onClick={() => setShowAuthModal(true)}
              className="text-primary hover:underline"
            >
              Sign in to continue
            </button>
          </div>
        </div>
        <AuthModal 
          isOpen={showAuthModal} 
          onClose={() => {
            // Only close if authenticated
            if (isAuthenticated) {
              setShowAuthModal(false);
            }
          }}
        />
      </>
    );
  }

  // Authenticated - render protected content
  return <>{children}</>;
}
```

### 3.4 App.tsx Updates
```typescript
// src/App.tsx
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/contexts/AuthContext";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Protected route - all course content */}
            <Route 
              path="/" 
              element={
                <ProtectedRoute>
                  <Index />
                </ProtectedRoute>
              } 
            />
            
            {/* Public routes (if any in future) */}
            {/* <Route path="/about" element={<About />} /> */}
            
            {/* Catch-all */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
```

### 3.5 VideoPlayerSecure Updates
```typescript
// src/components/course/VideoPlayerSecure.tsx (update the useEffect)
useEffect(() => {
  async function getVideoUrl() {
    // Simplified check - just need authentication, not specific course access
    if (!user) {
      setError('Please log in to view videos');
      return;
    }

    if (!videoPath) {
      if (videoUrl) {
        setSecureVideoUrl(videoUrl);
      }
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Generate signed URL - RLS now checks auth only
      const { data, error: urlError } = await supabase.storage
        .from('course-videos')
        .createSignedUrl(videoPath, 900); // 15 minutes

      if (urlError) {
        setError('Failed to load video');
        console.error('Error generating signed URL:', urlError);
        return;
      }

      setSecureVideoUrl(data.signedUrl);
      urlExpiryRef.current = new Date(Date.now() + 900 * 1000);
    } catch (err) {
      setError('An error occurred loading the video');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  getVideoUrl();

  // Auto-refresh logic remains the same
  const refreshInterval = setInterval(() => {
    if (urlExpiryRef.current && new Date() > new Date(urlExpiryRef.current.getTime() - 60000)) {
      getVideoUrl();
    }
  }, 60000);

  return () => clearInterval(refreshInterval);
}, [videoPath, videoUrl, user]);
```

## 4. Implementation Phases

### Phase 1: Core Authentication Setup (2-3 hours)
1. **Update Supabase Configuration**
   ```bash
   # Run SQL migrations for simplified RLS
   # Execute in Supabase SQL Editor
   ```

2. **Enhance AuthContext**
   - Copy enhanced AuthContext code
   - Test auth state management
   - Verify session persistence

3. **Create AuthModal Component**
   - Implement modal with tabs
   - Add form validation
   - Test login/signup flows

### Phase 2: Route Protection (2-3 hours)
1. **Create ProtectedRoute Component**
   - Implement auth checking
   - Add loading states
   - Handle modal display

2. **Update App.tsx**
   - Wrap routes with ProtectedRoute
   - Move AuthProvider inside BrowserRouter
   - Test protection on all routes

3. **Test Redirect Flow**
   - Verify URL preservation
   - Test post-login redirect
   - Handle edge cases

### Phase 3: Video Integration (1-2 hours)
1. **Update VideoPlayerSecure**
   - Remove course_access checks
   - Simplify to auth-only
   - Test video playback

2. **Update RLS Policies**
   - Run simplified SQL policies
   - Test video access
   - Verify signed URL generation

### Phase 4: Polish & Error Handling (2-3 hours)
1. **Error Handling**
   - Implement retry logic
   - Add network error handling
   - User-friendly error messages

2. **Loading States**
   - Add skeletons for loading
   - Smooth transitions
   - Progress indicators

3. **Mobile Responsiveness**
   - Test modal on mobile
   - Ensure touch-friendly
   - Keyboard navigation

4. **Cross-browser Testing**
   - Test on Chrome, Firefox, Safari
   - Verify session persistence
   - Check video playback

## 5. Error Handling Specifications

### 5.1 Network Errors
```typescript
// In AuthContext
const handleNetworkError = (error: any) => {
  if (!navigator.onLine) {
    return 'No internet connection. Please check your network.';
  }
  if (error.message.includes('NetworkError')) {
    return 'Network error. Please try again.';
  }
  if (error.message.includes('timeout')) {
    return 'Request timed out. Please try again.';
  }
  return error.message;
};
```

### 5.2 Auth Errors
```typescript
const AUTH_ERROR_MESSAGES = {
  'Invalid login credentials': 'Incorrect email or password',
  'User already registered': 'An account with this email already exists',
  'Email not confirmed': 'Please check your email to confirm your account',
  'Password should be at least 6 characters': 'Password must be at least 6 characters',
  'Invalid email': 'Please enter a valid email address',
};
```

### 5.3 Token Expiry Handling
```typescript
// In AuthContext
useEffect(() => {
  // Set up token refresh interval
  const refreshInterval = setInterval(async () => {
    if (session?.expires_at) {
      const expiresAt = new Date(session.expires_at * 1000);
      const now = new Date();
      const timeUntilExpiry = expiresAt.getTime() - now.getTime();
      
      // Refresh if less than 5 minutes until expiry
      if (timeUntilExpiry < 5 * 60 * 1000) {
        const { data, error } = await supabase.auth.refreshSession();
        if (error) {
          console.error('Token refresh failed:', error);
          // Force re-authentication
          await signOut();
        }
      }
    }
  }, 60000); // Check every minute

  return () => clearInterval(refreshInterval);
}, [session]);
```

## 6. Testing Specifications

### 6.1 Unit Tests
```typescript
// src/__tests__/auth/AuthContext.test.tsx
describe('AuthContext', () => {
  it('should sign in user successfully');
  it('should sign up new user and auto-login');
  it('should handle invalid credentials');
  it('should persist session on refresh');
  it('should clear session on logout');
  it('should auto-refresh tokens');
});
```

### 6.2 Integration Tests
```typescript
// src/__tests__/auth/ProtectedRoute.test.tsx
describe('ProtectedRoute', () => {
  it('should show auth modal when not authenticated');
  it('should render children when authenticated');
  it('should redirect to original URL after login');
  it('should handle loading states');
});
```

### 6.3 E2E Tests
```typescript
// e2e/auth.spec.ts
describe('Authentication Flow', () => {
  it('should complete full signup flow');
  it('should login and access course');
  it('should maintain session across page refresh');
  it('should handle logout correctly');
  it('should play videos after authentication');
});
```

## 7. Performance Optimizations

### 7.1 Code Splitting
```typescript
// Lazy load heavy components
const CourseLayout = lazy(() => import('@/components/course/CourseLayout'));
const VideoPlayerSecure = lazy(() => import('@/components/course/VideoPlayerSecure'));
```

### 7.2 Session Caching
```typescript
// Cache session check results
const SESSION_CACHE_KEY = 'module_mind_session_cache';
const SESSION_CACHE_TTL = 5 * 60 * 1000; // 5 minutes

const getCachedSession = () => {
  const cached = localStorage.getItem(SESSION_CACHE_KEY);
  if (cached) {
    const { session, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < SESSION_CACHE_TTL) {
      return session;
    }
  }
  return null;
};
```

## 8. Security Considerations

### 8.1 Content Security Policy
```html
<!-- In index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://*.supabase.co; 
               connect-src 'self' https://*.supabase.co;
               img-src 'self' data: https:;
               style-src 'self' 'unsafe-inline';">
```

### 8.2 Environment Variables
```typescript
// Validate environment variables on app start
const validateEnv = () => {
  const required = ['VITE_SUPABASE_URL', 'VITE_SUPABASE_ANON_KEY'];
  const missing = required.filter(key => !import.meta.env[key]);
  
  if (missing.length > 0) {
    throw new Error(`Missing environment variables: ${missing.join(', ')}`);
  }
};
```

## 9. Deployment Checklist

### 9.1 Pre-deployment
- [ ] Run SQL migrations in production Supabase
- [ ] Set environment variables in hosting platform
- [ ] Enable HTTPS only
- [ ] Configure CORS if needed
- [ ] Test auth flow in staging

### 9.2 Post-deployment
- [ ] Verify auth modal appears
- [ ] Test signup flow
- [ ] Test login flow
- [ ] Verify video playback
- [ ] Check session persistence
- [ ] Monitor error rates

## 10. Future Enhancements Path

### 10.1 Phase 2 Features
- Email verification toggle
- Password reset flow
- Remember me checkbox
- Social login (Google, GitHub)

### 10.2 Phase 3 Features
- Course access management
- Payment integration
- Admin panel
- User profiles page
- Progress tracking

## 11. File Structure

```
src/
├── components/
│   ├── auth/
│   │   ├── AuthModal.tsx         # Modal-based login/signup
│   │   └── ProtectedRoute.tsx    # Route protection HOC
│   └── course/
│       └── VideoPlayerSecure.tsx # Updated for MVP auth
├── contexts/
│   └── AuthContext.tsx           # Enhanced auth state management
├── lib/
│   └── supabase.ts              # Existing Supabase client
└── App.tsx                      # Updated with route protection
```

## 12. API Reference

### 12.1 AuthContext API
```typescript
interface AuthContextType {
  // State
  user: User | null;
  session: Session | null;
  loading: boolean;
  error: AuthError | null;
  isAuthenticated: boolean;
  
  // Actions
  signIn(email: string, password: string): Promise<{ error: AuthError | null }>;
  signUp(email: string, password: string, metadata?: object): Promise<{ error: AuthError | null }>;
  signOut(): Promise<void>;
  clearError(): void;
  checkSession(): Promise<void>;
}
```

### 12.2 Component Props
```typescript
// AuthModal
interface AuthModalProps {
  isOpen: boolean;
  onClose?: () => void;
}

// ProtectedRoute
interface ProtectedRouteProps {
  children: React.ReactNode;
}
```

## 13. Migration Guide

### 13.1 From Current State to MVP Auth
1. **Database Changes**
   - Run SQL migrations to simplify RLS policies
   - Verify profiles trigger is working

2. **Component Updates**
   - Replace AuthContext with enhanced version
   - Create auth components folder
   - Add AuthModal and ProtectedRoute
   - Update App.tsx routing

3. **Video Player Updates**
   - Remove course_access checks
   - Simplify to auth-only verification

4. **Testing**
   - Test signup flow (auto-access)
   - Test login flow
   - Verify video playback
   - Check session persistence

### 13.2 Rollback Plan
If issues arise:
1. Revert RLS policies to original
2. Remove ProtectedRoute wrapper
3. Restore original AuthContext
4. Keep AuthModal for future use

This specification provides a complete implementation guide for the MVP authentication system, with clear phases, detailed component specifications, and comprehensive error handling strategies.