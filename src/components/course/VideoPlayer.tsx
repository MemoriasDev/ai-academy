import { useState, useRef, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface VideoPlayerProps {
  videoUrl: string;
  videoId: string;
  title: string;
  duration: string;
  onTimeUpdate?: (time: number) => void;
  onPlayStateChange?: (isPlaying: boolean) => void;
}

export function VideoPlayer({ 
  videoUrl, 
  videoId, 
  title, 
  duration, 
  onTimeUpdate,
  onPlayStateChange 
}: VideoPlayerProps) {
  const [currentTime, setCurrentTime] = useState('0:00');
  const videoRef = useRef<HTMLVideoElement>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

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
    
    video.addEventListener('timeupdate', updateTimeDisplay);
    video.addEventListener('play', handlePlayPause);
    video.addEventListener('pause', handlePlayPause);
    
    return () => {
      video.removeEventListener('timeupdate', updateTimeDisplay);
      video.removeEventListener('play', handlePlayPause);
      video.removeEventListener('pause', handlePlayPause);
    };
  }, [videoUrl, onTimeUpdate, onPlayStateChange]);

  // Public method to seek to a specific time (used by Timeline)
  useEffect(() => {
    // Expose seek method on window for Timeline to use
    (window as any).seekVideo = (timeInSeconds: number) => {
      if (videoRef.current) {
        videoRef.current.currentTime = timeInSeconds;
      }
    };
    
    return () => {
      delete (window as any).seekVideo;
    };
  }, []);

  // Check if the video URL is a local file or relative path
  const isLocalFile = videoUrl.startsWith('file://') || videoUrl.startsWith('/');
  const videoSrc = videoUrl.startsWith('file://') ? videoUrl.replace('file://', '') : videoUrl;

  return (
    <Card>
      <CardContent className="p-0">
        <div className="relative">
          <div className="aspect-video bg-muted rounded-lg overflow-hidden">
            {isLocalFile ? (
              <video
                ref={videoRef}
                src={videoSrc}
                controls
                className="w-full h-full"
                title={title}
              >
                Your browser does not support the video tag.
              </video>
            ) : (
              <iframe
                ref={iframeRef}
                src={videoUrl}
                title={title}
                className="w-full h-full"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            )}
          </div>
          <div className="absolute bottom-4 left-4 flex items-center space-x-2">
            <Badge variant="secondary" className="bg-background/80 backdrop-blur">
              {duration}
            </Badge>
            <Badge variant="secondary" className="bg-background/80 backdrop-blur">
              {currentTime}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}