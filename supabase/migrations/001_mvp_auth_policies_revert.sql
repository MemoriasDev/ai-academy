-- Revert script for MVP auth policies
-- Run this if you need to rollback the simplified auth policies

-- Remove simplified MVP policy
DROP POLICY IF EXISTS "Authenticated users can access all videos" ON storage.objects;

-- Restore original complex policies (example - adjust based on your original setup)
CREATE POLICY "Authenticated users can access cohort_2 videos"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'course-videos'
  AND auth.role() = 'authenticated'
  AND EXISTS (
    SELECT 1 FROM course_access
    WHERE user_id = auth.uid()
    AND course_id = 'cohort_2'
    AND (expires_at IS NULL OR expires_at > NOW())
  )
);

-- Note: This is a template. You should backup your original policies before applying MVP changes
-- and use those exact policies in this revert script.