/**
 * @description 
 * Modal-based authentication component for Module Mind.
 * Provides tabbed interface for login and signup with form validation,
 * loading states, and comprehensive error handling.
 * Cannot be dismissed without authentication for security.
 * 
 * Key features:
 * - Tabbed interface for seamless login/signup switching
 * - Real-time form validation with helpful error messages
 * - Loading states during authentication operations
 * - Auto-closes when user becomes authenticated
 * - Non-dismissible design (no escape/backdrop close)
 * - Responsive design for mobile devices
 * 
 * @dependencies
 * - @/contexts/AuthContext: Authentication operations
 * - @/components/ui/*: Shadcn UI components
 * - lucide-react: Icons for loading states
 * 
 * @notes
 * - Modal cannot be closed without authentication (security requirement)
 * - Passwords must be at least 6 characters (Supabase minimum)
 * - Email validation uses basic regex pattern
 * - For MVP, no email verification is required after signup
 */

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

/**
 * AuthModal component - Handles user authentication via modal interface
 * @param isOpen - Controls modal visibility
 * @param onClose - Optional callback when modal closes (only called when authenticated)
 */
export function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const { signIn, signUp, loading, error, clearError, isAuthenticated } = useAuth();
  
  // Form state for sign in
  const [signInEmail, setSignInEmail] = useState('');
  const [signInPassword, setSignInPassword] = useState('');
  
  // Form state for sign up
  const [signUpEmail, setSignUpEmail] = useState('');
  const [signUpPassword, setSignUpPassword] = useState('');
  const [fullName, setFullName] = useState('');
  
  // Local state
  const [localError, setLocalError] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState('signin');

  /**
   * Close modal when user becomes authenticated
   */
  useEffect(() => {
    if (isAuthenticated && onClose) {
      onClose();
    }
  }, [isAuthenticated, onClose]);

  /**
   * Clear errors when switching tabs
   */
  useEffect(() => {
    clearError();
    setLocalError('');
    // Don't clear form fields to improve UX if user accidentally switches tabs
  }, [activeTab, clearError]);

  /**
   * Validate email format
   */
  const isValidEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  /**
   * Validate form inputs
   * @param isSignUp - Whether validating signup form (requires name)
   */
  const validateForm = (isSignUp: boolean = false): boolean => {
    const email = isSignUp ? signUpEmail : signInEmail;
    const password = isSignUp ? signUpPassword : signInPassword;
    
    // Check email
    if (!email || !isValidEmail(email)) {
      setLocalError('Please enter a valid email address');
      return false;
    }
    
    // Check password
    if (!password || password.length < 6) {
      setLocalError('Password must be at least 6 characters');
      return false;
    }
    
    // Check name for signup
    if (isSignUp && !fullName.trim()) {
      setLocalError('Please enter your name');
      return false;
    }
    
    return true;
  };

  /**
   * Handle sign in form submission
   */
  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear previous errors
    setLocalError('');
    
    // Validate form
    if (!validateForm(false)) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      const { error } = await signIn(signInEmail, signInPassword);
      
      if (error) {
        // Provide user-friendly error messages
        if (error.message.includes('Invalid login credentials')) {
          setLocalError('Invalid email or password. Please try again.');
        } else if (error.message.includes('Email not confirmed')) {
          setLocalError('Please check your email to confirm your account.');
        } else if (error.message.includes('Network')) {
          setLocalError('Network error. Please check your connection and try again.');
        } else {
          setLocalError(error.message);
        }
      }
      // If successful, modal will close automatically via useEffect
    } catch (err) {
      setLocalError('An unexpected error occurred. Please try again.');
      console.error('Sign in error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Handle sign up form submission
   */
  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Clear previous errors
    setLocalError('');
    
    // Validate form
    if (!validateForm(true)) {
      return;
    }

    setIsSubmitting(true);
    
    try {
      const { error } = await signUp(signUpEmail, signUpPassword, { 
        full_name: fullName.trim() 
      });
      
      if (error) {
        // Provide user-friendly error messages
        if (error.message.includes('already registered')) {
          setLocalError('An account with this email already exists. Please sign in instead.');
        } else if (error.message.includes('Password')) {
          setLocalError('Password must be at least 6 characters.');
        } else if (error.message.includes('Network')) {
          setLocalError('Network error. Please check your connection and try again.');
        } else {
          setLocalError(error.message);
        }
      }
      // If successful, user is auto-signed in and modal will close
    } catch (err) {
      setLocalError('An unexpected error occurred. Please try again.');
      console.error('Sign up error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  /**
   * Get the error message to display
   * Prioritizes local error over context error
   */
  const displayError = localError || error?.message;

  return (
    <Dialog 
      open={isOpen} 
      onOpenChange={() => {
        // Security: Modal must not be dismissible without authentication
        // This empty handler prevents escape key and backdrop click from closing
      }}
    >
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

          {/* Sign In Tab */}
          <TabsContent value="signin" className="space-y-4 mt-4">
            <form onSubmit={handleSignIn} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signin-email">Email</Label>
                <Input
                  id="signin-email"
                  type="email"
                  placeholder="you@example.com"
                  value={signInEmail}
                  onChange={(e) => setSignInEmail(e.target.value)}
                  disabled={isSubmitting || loading}
                  required
                  autoComplete="email"
                  autoFocus
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="signin-password">Password</Label>
                <Input
                  id="signin-password"
                  type="password"
                  placeholder="••••••••"
                  value={signInPassword}
                  onChange={(e) => setSignInPassword(e.target.value)}
                  disabled={isSubmitting || loading}
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

              {/* Future: Add "Forgot password?" link here */}
              {/* <p className="text-xs text-center text-muted-foreground">
                <a href="#" className="hover:underline">Forgot your password?</a>
              </p> */}
            </form>
          </TabsContent>

          {/* Sign Up Tab */}
          <TabsContent value="signup" className="space-y-4 mt-4">
            <form onSubmit={handleSignUp} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="signup-name">Full Name</Label>
                <Input
                  id="signup-name"
                  type="text"
                  placeholder="John Doe"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  disabled={isSubmitting || loading}
                  required
                  autoComplete="name"
                  autoFocus
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="signup-email">Email</Label>
                <Input
                  id="signup-email"
                  type="email"
                  placeholder="you@example.com"
                  value={signUpEmail}
                  onChange={(e) => setSignUpEmail(e.target.value)}
                  disabled={isSubmitting || loading}
                  required
                  autoComplete="email"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="signup-password">Password</Label>
                <Input
                  id="signup-password"
                  type="password"
                  placeholder="••••••••"
                  value={signUpPassword}
                  onChange={(e) => setSignUpPassword(e.target.value)}
                  disabled={isSubmitting || loading}
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