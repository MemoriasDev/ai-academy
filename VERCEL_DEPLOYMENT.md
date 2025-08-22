# AI Academy - Vercel Deployment Guide

## Prerequisites
- GitHub account with access to `MemoriasDev/ai-academy` repository
- Vercel account (free tier is sufficient)
- Supabase project with videos already uploaded

## Step-by-Step Deployment Instructions

### 1. Connect to Vercel

1. Go to [https://vercel.com/new](https://vercel.com/new)
2. Click **"Import Git Repository"**
3. If not connected, click **"Add GitHub Account"** and authorize Vercel
4. Search for `ai-academy` or select from `MemoriasDev/ai-academy`
5. Click **"Import"**

### 2. Configure Project Settings

**Project Name:**
- Keep as `ai-academy` or customize (e.g., `ai-academy-course`)
- This will become your subdomain: `ai-academy.vercel.app`

**Framework Preset:**
- Vercel should auto-detect **Vite**
- If not, manually select: `Vite`

**Root Directory:**
- Leave as `./` (repository root)

**Build Settings (should auto-populate):**
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

### 3. Add Environment Variables

Click **"Environment Variables"** and add these two required variables:

| Variable Name | Value | Description |
|--------------|-------|-------------|
| `VITE_SUPABASE_URL` | `https://your-project-ref.supabase.co` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Your Supabase anon/public key |

**⚠️ IMPORTANT:** 
- Only add variables with `VITE_` prefix (these are safe for client-side)
- NEVER add `SUPABASE_SERVICE_ROLE_KEY` to Vercel (security risk)
- Get these values from your `.env.local` file or Supabase dashboard

### 4. Deploy

1. Click **"Deploy"** button
2. Wait 1-3 minutes for build and deployment
3. Watch the build logs for any errors

**Expected Build Output:**
```
[09:23:45.123] Cloning github.com/MemoriasDev/ai-academy (Branch: main)
[09:23:46.456] Installing dependencies...
[09:23:58.789] Building application...
[09:24:12.345] Build completed
[09:24:13.456] Uploading static files...
[09:24:15.789] Deployment ready
```

### 5. Post-Deployment Verification

Once deployed, verify:

1. **Visit your URL**: `https://[your-project-name].vercel.app`
2. **Test Authentication**:
   - Click "Sign In"
   - Create account or use existing credentials
   - Verify login works
3. **Test Video Playback**:
   - Navigate to any lesson
   - Confirm videos load from Supabase storage
   - Check timestamp navigation works
4. **Test Progress Tracking**:
   - Mark checklist items
   - Verify progress saves (localStorage)
   - Refresh page to confirm persistence

## Common Issues & Solutions

### Build Fails

**Error: "Module not found"**
```bash
Solution: Check package.json dependencies are committed
```

**Error: "Environment variables not defined"**
```bash
Solution: Verify VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set
```

### Videos Not Loading

**403 Forbidden Error:**
- Check Supabase RLS policies for `course-videos` bucket
- Ensure bucket is public or has proper auth policies

**404 Not Found:**
- Verify video files exist in Supabase storage
- Check video paths match those in `courseData.ts`

### Authentication Issues

**"Invalid API key":**
- Double-check `VITE_SUPABASE_ANON_KEY` is correct (get from your Supabase dashboard)
- Ensure no extra spaces or quotes in environment variable

**Login not persisting:**
- Check browser allows cookies/localStorage
- Verify Supabase auth settings

## Custom Domain Setup (Optional)

1. Go to **Settings → Domains** in Vercel dashboard
2. Add your custom domain (e.g., `course.yourdomain.com`)
3. Update DNS records as instructed by Vercel
4. SSL certificate auto-provisions

## Environment Management

### Development vs Production

Vercel automatically sets `NODE_ENV=production`. The app handles this via:
- Production: Uses Vercel environment variables
- Development: Uses local `.env.local` file

### Updating Environment Variables

1. Go to **Settings → Environment Variables**
2. Edit variable values
3. Click **Save**
4. **IMPORTANT**: Redeploy for changes to take effect
   - Go to **Deployments** tab
   - Click **...** menu on latest deployment
   - Select **Redeploy**

## Monitoring & Analytics

### Vercel Dashboard Provides:
- Deployment history
- Build logs
- Function logs (if using API routes)
- Performance metrics
- Error tracking

### Recommended: Enable Speed Insights
1. Go to **Analytics** tab
2. Enable **Speed Insights** (free tier available)
3. Monitor Core Web Vitals

## Continuous Deployment

**Automatic Deployments:**
- Every push to `main` branch triggers deployment
- Pull requests create preview deployments

**Preview Deployments:**
- Each PR gets unique URL for testing
- Comments added to GitHub PR with preview link

## Security Checklist

✅ **Before Deploying:**
- [ ] Only `VITE_` prefixed env vars in Vercel
- [ ] No service role keys exposed
- [ ] Supabase RLS policies configured
- [ ] No sensitive data in repository

✅ **After Deploying:**
- [ ] Test authentication flow
- [ ] Verify video access controls
- [ ] Check browser console for errors
- [ ] Confirm no API keys exposed in source

## Rollback Procedure

If issues occur after deployment:

1. Go to **Deployments** tab
2. Find last working deployment
3. Click **...** → **Promote to Production**
4. Previous version instantly restored

## Support Resources

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Status**: [vercel-status.com](https://www.vercel-status.com)
- **Supabase Dashboard**: [app.supabase.com](https://app.supabase.com)
- **Repository**: [github.com/MemoriasDev/ai-academy](https://github.com/MemoriasDev/ai-academy)

## Next Steps After Deployment

1. **Test Everything**: Full user journey from signup to lesson completion
2. **Set Up Monitoring**: Enable Vercel Analytics
3. **Configure Alerts**: Set up uptime monitoring
4. **Document Issues**: Keep notes on any deployment quirks
5. **Plan Improvements**: Review `progress_tracking_status.md` for roadmap

---

**Deployment Checklist Summary:**
- [ ] Import repository to Vercel
- [ ] Add environment variables (get from your Supabase dashboard)
- [ ] Deploy application
- [ ] Verify authentication works
- [ ] Test video playback
- [ ] Check progress tracking
- [ ] Share URL with team

**Estimated Time**: 5-10 minutes for initial deployment