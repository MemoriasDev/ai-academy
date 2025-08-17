import { useState, useRef, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { supabase } from '@/lib/supabase';
import { useAuth } from '@/contexts/AuthContext';

interface VideoPlayerSecureProps {
  videoPath?: string; // New: Supabase storage path
  videoUrl?: string;  // Fallback: local URL
  videoId: string;
  title: string;
  duration: string;
  onTimeUpdate?: (time: number) => void;
  onPlayStateChange?: (isPlaying: boolean) => void;
}

export function VideoPlayerSecure({ 
  videoPath,
  videoUrl, 
  videoId, 
  title, 
  duration, 
  onTimeUpdate,
  onPlayStateChange 
}: VideoPlayerSecureProps) {
  const [currentTime, setCurrentTime] = useState('0:00');
  const [secureVideoUrl, setSecureVideoUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSeeking, setIsSeeking] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const { user } = useAuth();
  const urlExpiryRef = useRef<Date | null>(null);

  // Generate signed URL for video
  useEffect(() => {
    async function getVideoUrl() {
      // If no videoPath, fall back to local videoUrl
      if (!videoPath) {
        if (videoUrl) {
          setSecureVideoUrl(videoUrl);
        }
        return;
      }

      // MVP: Simplified check - just need authentication, not specific course access
      if (!user) {
        setError('Please log in to view videos');
        return;
      }

      setLoading(true);
      setError(null);

      try {
        console.log('Attempting to generate signed URL for:', videoPath);
        console.log('User authenticated:', !!user);
        
        // Generate signed URL - RLS now checks auth only (not course_access)
        const { data, error: urlError } = await supabase.storage
          .from('course-videos')
          .createSignedUrl(videoPath, 900); // 15 minutes

        if (urlError) {
          // More detailed error logging
          console.error('Error generating signed URL:', urlError);
          console.error('Video path:', videoPath);
          console.error('Error details:', urlError.message, urlError.name);
          
          // Check specific error types
          if (urlError.message?.includes('Object not found')) {
            setError(`Video not found in storage: ${videoPath}`);
          } else if (urlError.message?.includes('not authorized')) {
            setError('Not authorized to access videos. Please try logging out and back in.');
          } else {
            setError('Failed to load video. Please try refreshing the page.');
          }
          return;
        }

        setSecureVideoUrl(data.signedUrl);
        // Track when URL expires for auto-refresh
        urlExpiryRef.current = new Date(Date.now() + 900 * 1000);
      } catch (err) {
        setError('An error occurred loading the video. Please try refreshing the page.');
        console.error('Video loading error:', err);
      } finally {
        setLoading(false);
      }
    }

    getVideoUrl();

    // Auto-refresh URL before it expires (at 14 minutes)
    const refreshInterval = setInterval(() => {
      if (urlExpiryRef.current && new Date() > new Date(urlExpiryRef.current.getTime() - 60000)) {
        console.log('Refreshing video URL before expiry...');
        getVideoUrl();
      }
    }, 60000); // Check every minute

    return () => clearInterval(refreshInterval);
  }, [videoPath, videoUrl, user]);

  // Update current time display and notify parent as video plays
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    
    const updateTimeDisplay = () => {
      const minutes = Math.floor(video.currentTime / 60);
      const seconds = Math.floor(video.currentTime % 60);
      setCurrentTime(`${minutes}:${seconds.toString().padStart(2, '0')}`);
      onTimeUpdate?.(video.currentTime);
    };
    
    const handlePlayPause = () => {
      onPlayStateChange?.(!video.paused);
    };

    const handleError = (e: Event) => {
      const video = e.currentTarget as HTMLVideoElement;
      if (video.error?.code === 4) { // MEDIA_ERR_SRC_NOT_SUPPORTED
        // URL might have expired, try refreshing
        getVideoUrl();
      }
    };
    
    video.addEventListener('timeupdate', updateTimeDisplay);
    video.addEventListener('play', handlePlayPause);
    video.addEventListener('pause', handlePlayPause);
    video.addEventListener('error', handleError);
    
    return () => {
      video.removeEventListener('timeupdate', updateTimeDisplay);
      video.removeEventListener('play', handlePlayPause);
      video.removeEventListener('pause', handlePlayPause);
      video.removeEventListener('error', handleError);
    };
  }, [onTimeUpdate, onPlayStateChange]);

  // Handle seeking to a specific time from external components
  const seekToTime = (seconds: number) => {
    if (videoRef.current && videoRef.current.readyState >= 2) {
      // Show seeking indicator
      setIsSeeking(true);
      
      // Perform the seek
      videoRef.current.currentTime = seconds;
      
      // Play the video if it was paused
      if (videoRef.current.paused) {
        videoRef.current.play().catch(e => {
          console.warn('Auto-play after seek failed:', e);
        });
      }
      
      // Hide seeking indicator after a short delay
      setTimeout(() => setIsSeeking(false), 500);
      
      console.log(`Video seeked to ${seconds} seconds`);
    } else {
      console.warn('Video not ready for seeking, current readyState:', videoRef.current?.readyState);
    }
  };

  // Expose the seek function to be called by Timeline/CourseLayout
  useEffect(() => {
    if (window) {
      // Use seekVideo name to match what CourseLayout expects
      (window as any).seekVideo = seekToTime;
      // Also keep seekToTime for backward compatibility
      (window as any).seekToTime = seekToTime;
    }
    
    // Cleanup on unmount
    return () => {
      if (window) {
        delete (window as any).seekVideo;
        delete (window as any).seekToTime;
      }
    };
  }, []);

  if (loading) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center h-[480px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading video...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center h-[480px]">
          <div className="text-center">
            <p className="text-red-600 mb-2">{error}</p>
            {error.includes('log in') && (
              <p className="text-sm text-gray-600">
                Please log in to access course videos
              </p>
            )}
            {error.includes('access') && (
              <p className="text-sm text-gray-600">
                Please contact the course administrator for access
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  // Check if this is a YouTube URL
  const isYouTube = secureVideoUrl?.includes('youtube.com') || secureVideoUrl?.includes('youtu.be');
  
  if (isYouTube) {
    // Extract YouTube video ID
    let youtubeId = '';
    if (secureVideoUrl?.includes('youtube.com')) {
      youtubeId = secureVideoUrl.split('v=')[1]?.split('&')[0] || '';
    } else if (secureVideoUrl?.includes('youtu.be')) {
      youtubeId = secureVideoUrl.split('/').pop() || '';
    }
    
    return (
      <Card className="w-full">
        <CardContent className="p-0">
          <div className="relative">
            <iframe
              ref={iframeRef}
              src={`https://www.youtube.com/embed/${youtubeId}?enablejsapi=1`}
              className="w-full aspect-video"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
            <div className="absolute top-4 right-4 flex gap-2">
              <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm">
                {currentTime} / {duration}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }
  
  // Local or Supabase video file
  return (
    <Card className="w-full">
      <CardContent className="p-0">
        <div className="relative">
          {/* Seeking indicator overlay */}
          {isSeeking && secureVideoUrl && (
            <div className="absolute inset-0 z-10 flex items-center justify-center bg-black/30 pointer-events-none">
              <div className="bg-background/90 backdrop-blur-sm rounded-lg px-4 py-2">
                <p className="text-sm font-medium">Jumping to timestamp...</p>
              </div>
            </div>
          )}
          
          {secureVideoUrl ? (
            <video
              ref={videoRef}
              src={secureVideoUrl}
              controls
              className="w-full aspect-video bg-black"
              controlsList="nodownload"
              preload="metadata"
            >
              Your browser does not support the video tag.
            </video>
          ) : (
            <div className="w-full aspect-video bg-gray-100 flex items-center justify-center">
              <p className="text-gray-500">No video available</p>
            </div>
          )}
          <div className="absolute top-4 right-4 flex gap-2">
            <Badge variant="secondary" className="bg-background/80 backdrop-blur-sm">
              {currentTime} / {duration}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}