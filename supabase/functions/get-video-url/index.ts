import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Create Supabase client with user's auth token
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { 
        global: { 
          headers: { Authorization: req.headers.get('Authorization')! } 
        } 
      }
    )

    // Verify user is authenticated
    const { data: { user }, error: userError } = await supabaseClient.auth.getUser()
    if (userError || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized - Please log in' }),
        { 
          status: 401, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    // Check if user has course access
    const { data: access, error: accessError } = await supabaseClient
      .from('course_access')
      .select('*')
      .eq('user_id', user.id)
      .eq('course_id', 'cohort_2')
      .gte('expires_at', new Date().toISOString())
      .single()

    if (accessError || !access) {
      // Check if expires_at is null (permanent access)
      const { data: permanentAccess } = await supabaseClient
        .from('course_access')
        .select('*')
        .eq('user_id', user.id)
        .eq('course_id', 'cohort_2')
        .is('expires_at', null)
        .single()

      if (!permanentAccess) {
        return new Response(
          JSON.stringify({ error: 'No access to this course. Please contact admin.' }),
          { 
            status: 403, 
            headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
          }
        )
      }
    }

    // Get video path from request body
    const { videoPath } = await req.json()
    
    if (!videoPath) {
      return new Response(
        JSON.stringify({ error: 'Video path is required' }),
        { 
          status: 400, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    // Use service role to generate signed URL
    const supabaseServiceClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )
    
    // Generate signed URL (valid for 2 hours)
    const { data, error } = await supabaseServiceClient.storage
      .from('course-videos')
      .createSignedUrl(videoPath, 7200)

    if (error) {
      console.error('Error creating signed URL:', error)
      return new Response(
        JSON.stringify({ error: 'Failed to generate video URL' }),
        { 
          status: 500, 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
        }
      )
    }

    // Log access for analytics (optional)
    await supabaseClient
      .from('video_access_logs')
      .insert({
        user_id: user.id,
        video_path: videoPath,
        accessed_at: new Date().toISOString()
      })
      .select()
      .single()
      .catch(() => {}) // Ignore logging errors

    return new Response(
      JSON.stringify({ 
        url: data.signedUrl,
        expires_in: 7200 
      }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    )
  } catch (error) {
    console.error('Edge function error:', error)
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' } 
      }
    )
  }
})