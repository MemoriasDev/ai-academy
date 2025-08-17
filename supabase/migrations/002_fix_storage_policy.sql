-- Fix storage policy for video access
-- Remove the problematic foldername condition

-- Drop the existing policy
DROP POLICY IF EXISTS "Authenticated users can access all videos" ON storage.objects;

-- Create corrected policy - simpler condition
CREATE POLICY "Authenticated users can access all videos"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'course-videos'
  AND auth.role() = 'authenticated'
);