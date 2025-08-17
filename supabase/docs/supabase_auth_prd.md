# Module Mind MVP Authentication System

## Project Description
Implement a minimal viable authentication system for Module Mind that protects all course content behind a modal-based login/signup flow, using Supabase Authentication with JWT session management and following security best practices. All authenticated users automatically have course access in MVP.

## Target Audience
Students accessing the AI/LLM course content who need a frictionless authentication experience

## Desired Features

### Authentication Modal
- [ ] Modal-based auth guard
    - [ ] Intercepts all course page access
    - [ ] Cannot be dismissed without authentication
    - [ ] Centered modal with backdrop
- [ ] Login functionality
    - [ ] Email/password authentication
    - [ ] Clear error messaging
    - [ ] Loading states during authentication
- [ ] Sign up functionality
    - [ ] Email/password registration
    - [ ] No email verification required (MVP)
    - [ ] Automatic profile creation
    - [ ] Immediate course access upon signup

### Session Management
- [ ] JWT-based authentication (Supabase default)
    - [ ] Secure httpOnly cookies for refresh tokens
    - [ ] Short-lived access tokens (1 hour)
    - [ ] Automatic token refresh
- [ ] Session persistence
    - [ ] Sessions persist for 7 days
    - [ ] Persist across browser closes
    - [ ] Automatic re-authentication with refresh token
- [ ] Session security
    - [ ] Secure token storage (localStorage for access, httpOnly cookie for refresh)
    - [ ] Clear tokens on logout
    - [ ] Handle expired sessions gracefully

### Database Integration
- [ ] User profiles table
    - [ ] Auto-create profile on signup (via trigger)
    - [ ] Store user ID, email, created_at
    - [ ] Foundation for future features (progress tracking, preferences)
- [ ] Course access (MVP simplified)
    - [ ] ALL authenticated users have access to cohort_2
    - [ ] No course_access table checks in MVP
    - [ ] Prepared for future payment/enrollment system

### Route Protection
- [ ] Auth guard implementation
    - [ ] React Context for auth state
    - [ ] Protected route wrapper component
    - [ ] Check authentication before rendering
- [ ] Protected routes
    - [ ] All course content requires auth
    - [ ] Modal shows on unauthenticated access
    - [ ] Maintain requested URL for post-login redirect

### User Flow
- [ ] Authentication flow
    - [ ] User visits course → auth check → modal if needed
    - [ ] Successful login → redirect to requested content
    - [ ] Successful signup → automatic login → redirect to course
- [ ] State management
    - [ ] Global auth context with user state
    - [ ] Loading states during auth checks
    - [ ] Sync auth state across tabs (Supabase handles)

### Video Access (Already Configured)
- [ ] Authenticated video streaming
    - [ ] Videos check auth.uid() exists (not course_access)
    - [ ] Generate signed URLs for authenticated users
    - [ ] 15-minute expiry with auto-refresh

## Design Requests
- [ ] Modal interface
    - [ ] Clean, minimal design matching existing UI
    - [ ] Tab switching between login/signup
    - [ ] Form validation feedback
    - [ ] Responsive on mobile
- [ ] User feedback
    - [ ] Loading spinners during auth
    - [ ] Toast notifications for success/errors
    - [ ] Clear password requirements (min 6 characters)
    - [ ] Helpful error messages

## Technical Implementation Details
- [ ] Supabase configuration
    - [ ] Use existing profiles table with trigger
    - [ ] Simplify RLS policies for MVP (authenticated = access)
    - [ ] Keep course_access table for future use
- [ ] State management
    - [ ] AuthContext at app root
    - [ ] useAuth hook for components
    - [ ] Automatic token refresh handling
- [ ] Security considerations
    - [ ] No sensitive data in localStorage
    - [ ] HTTPS only in production
    - [ ] Rate limiting on auth endpoints (Supabase handles)

## Implementation Phases

### Phase 1: Core Authentication
1. Update Supabase RLS policies for MVP access
2. Create AuthModal component
3. Implement AuthContext with Supabase client
4. Add protected route wrapper

### Phase 2: User Flow
1. Integrate modal with route protection
2. Handle login/signup flows
3. Implement redirect after authentication
4. Add loading states

### Phase 3: Video Integration
1. Update video player auth checks
2. Simplify to authenticated-only access
3. Test signed URL generation
4. Verify auto-refresh functionality

### Phase 4: Polish & Testing
1. Error handling and user feedback
2. Mobile responsiveness
3. Cross-browser testing
4. Session persistence verification

## Success Criteria
- [ ] Users cannot access course content without authentication
- [ ] Signup process takes less than 30 seconds
- [ ] Login persists across browser sessions
- [ ] Videos play immediately after authentication
- [ ] No email verification friction in signup
- [ ] Clear error messages guide users

## Future Considerations
- Email verification for production
- Payment integration for course access
- Social login providers (Google, GitHub)
- Two-factor authentication
- Admin panel for user management
- Course enrollment management
- Progress tracking per user
- User preferences and settings

## Technical Stack
- **Frontend**: React with TypeScript
- **Authentication**: Supabase Auth
- **Database**: PostgreSQL via Supabase
- **Session Management**: JWT with refresh tokens
- **State Management**: React Context API
- **UI Components**: Existing shadcn/ui components
- **Routing**: React Router with protected routes

## Database Schema (Existing)

### Tables
- `auth.users` - Supabase managed auth table
- `public.profiles` - User profiles with app-specific data
- `public.course_access` - Course enrollment (future use)

### RLS Policies for MVP
- Profiles: Users can read/update their own profile
- Storage: Authenticated users can access course videos
- Course access: Simplified to auth check only (MVP)

## API Endpoints (Supabase Managed)
- `POST /auth/v1/signup` - User registration
- `POST /auth/v1/token?grant_type=password` - User login
- `POST /auth/v1/token?grant_type=refresh_token` - Token refresh
- `POST /auth/v1/logout` - User logout
- `GET /auth/v1/user` - Get current user

## Environment Variables Required
```env
VITE_SUPABASE_URL=your-project-url
VITE_SUPABASE_ANON_KEY=your-anon-key
```

## Risks and Mitigations
- **Risk**: Users sharing accounts
  - **Mitigation**: Monitor concurrent sessions (future)
- **Risk**: Brute force attacks
  - **Mitigation**: Supabase rate limiting
- **Risk**: Token theft
  - **Mitigation**: Short-lived access tokens, secure storage
- **Risk**: Users losing access
  - **Mitigation**: Clear password reset flow (Phase 2)

## Dependencies
- @supabase/supabase-js (already installed)
- React Router (already installed)
- Existing UI components (already built)

## Estimated Timeline
- Phase 1: 2-3 hours
- Phase 2: 2-3 hours
- Phase 3: 1-2 hours
- Phase 4: 2-3 hours
- **Total**: 7-11 hours of development

## Definition of Done
- [ ] All authenticated users can access course content
- [ ] Unauthenticated users see login modal
- [ ] Sessions persist for 7 days
- [ ] Videos play with authentication
- [ ] Mobile responsive design
- [ ] Error handling implemented
- [ ] Basic documentation provided