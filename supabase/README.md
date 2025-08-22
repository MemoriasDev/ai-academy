# Supabase Backend Configuration

Database migrations, authentication policies, and serverless functions for the AI Academy learning platform.

## 📖 What it does
Provides the complete backend infrastructure for user authentication, video storage, and data persistence. Includes Row Level Security (RLS) policies for content protection and edge functions for video URL generation.

## 🛠️ Built with
- **Database**: PostgreSQL with Supabase extensions
- **Authentication**: Supabase Auth with JWT tokens
- **Storage**: Supabase Storage with signed URLs
- **Edge Functions**: Deno runtime for serverless video processing
- **Security**: Row Level Security (RLS) policies
- **Migrations**: SQL migration files for version control

## 🚀 Status
**In Production** - Live database supporting authenticated users with secure video streaming and 15-minute signed URL expiration.

## 🌐 Demo
- **Auth Flow**: Sign up/sign in through the main platform
- **Video Access**: Protected video streaming with automatic URL refresh
- **Security**: Try accessing content without authentication (blocked by RLS)

## 📁 Structure

### Migrations (`migrations/`)
Database schema and security policy management:

- **`001_mvp_auth_policies.sql`** - Initial authentication and authorization setup
- **`001_mvp_auth_policies_revert.sql`** - Rollback script for auth policies  
- **`002_fix_storage_policy.sql`** - Storage bucket security improvements

### Functions (`functions/`)
Serverless edge functions for backend logic:

- **`get-video-url/index.ts`** - Generates signed URLs for secure video access

### Documentation (`docs/`)
Implementation guides and specifications:

- **`supabase_auth_spec.md`** - Authentication system specification
- **`supabase_auth_prd.md`** - Production authentication requirements
- **`supabase_auth_prd.mdx`** - MDX version for documentation sites

## 🔐 Security Features

### Row Level Security (RLS)
- **User Isolation**: Users can only access their own data
- **Content Protection**: Videos require valid authentication
- **Automatic Enforcement**: Database-level security (not just app-level)

### Video Storage Security
- **Signed URLs**: 15-minute expiration for video access
- **Authentication Required**: No direct file access without login
- **Bucket Policies**: Granular permissions for different content types

### Authentication Policies
- **JWT Validation**: Automatic token verification
- **Session Management**: Secure session handling with auto-refresh
- **Multi-device Support**: Consistent auth across devices

## 🚀 Quick Start

### Local Development Setup
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize local development
supabase init

# Start local Supabase stack
supabase start

# Apply migrations
supabase db reset
```

### Production Deployment
```bash
# Link to production project
supabase link --project-ref your-project-ref

# Deploy migrations
supabase db push

# Deploy edge functions
supabase functions deploy get-video-url
```

## 📊 Database Schema

### Tables
- **User Management**: Handled by Supabase Auth (built-in)
- **Progress Tracking**: (Future) User lesson progress and completion status
- **Course Content**: (Future) Dynamic course content management

### Storage Buckets
- **`course-videos`**: Protected video content with RLS policies
- **`public-assets`**: Public images and static content

## 🔧 Edge Functions

### get-video-url
**Purpose**: Generate secure video URLs with expiration
**Input**: Video path and user authentication
**Output**: Signed URL valid for 15 minutes
**Security**: Validates user authentication before URL generation

```typescript
// Example usage
const { data, error } = await supabase.functions.invoke('get-video-url', {
  body: { videoPath: 'cohort_2/week_01/lesson1.mp4' }
})
```

## 📋 Environment Variables

### Required for Functions
```env
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Security Notes
- **Service Role Key**: Only for server-side operations, never client-side
- **Anon Key**: Safe for client-side use when RLS is enabled
- **URL**: Public project URL, safe to expose

## 🔄 Migration Management

### Best Practices
1. **Always backup** before running migrations in production
2. **Test migrations** in local environment first
3. **Use rollback scripts** for reversible changes
4. **Version control** all migration files

### Running Migrations
```bash
# Local development
supabase db reset

# Production (careful!)
supabase db push --dry-run  # Test first
supabase db push           # Apply changes
```

## 🤝 Contributing

### Adding New Migrations
1. Create numbered migration file in `migrations/`
2. Include both forward and rollback operations
3. Test thoroughly in local environment
4. Document any breaking changes

### Edge Function Development
1. Create function in `functions/` directory
2. Include TypeScript types and error handling
3. Test with local Supabase stack
4. Document function parameters and responses

## 📞 Support

- **Supabase Docs**: [supabase.com/docs](https://supabase.com/docs)
- **Local Issues**: Check `supabase status` for local stack health
- **Production Issues**: Monitor Supabase dashboard for errors
- **Function Logs**: View in Supabase dashboard under Functions tab
