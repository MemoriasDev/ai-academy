-- MVP Authentication RLS Policies
-- Simplifies access control: all authenticated users can access course content

-- Verify bucket exists before applying policies
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM storage.buckets WHERE id = 'course-videos'
  ) THEN
    RAISE EXCEPTION 'Bucket course-videos does not exist. Please create it first.';
  END IF;
END $$;

-- Drop existing complex policies if they exist
DROP POLICY IF EXISTS "Authenticated users can access cohort_2 videos" ON storage.objects;
DROP POLICY IF EXISTS "Users can access their course videos" ON storage.objects;

-- Create simplified policy for MVP (with explicit bucket path scoping)
CREATE POLICY "Authenticated users can access all videos"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'course-videos'
  AND auth.role() = 'authenticated'
  AND (storage.foldername(name))[1] = 'course-videos'
);

-- Ensure profiles table has proper RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing profiles policies if they exist
DROP POLICY IF EXISTS "Users can read own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;

-- Create profiles policies
CREATE POLICY "Users can read own profile"
ON public.profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
ON public.profiles FOR UPDATE
USING (auth.uid() = id);

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

-- Note: To rollback these changes, run 001_mvp_auth_policies_revert.sql