import { useState, useRef, useEffect } from 'react';
import { Play, Pause, SkipForward, SkipBack } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Timestamp } from '@/types/course';
import { cn } from '@/lib/utils';

interface TimelineProps {
  timestamps: Timestamp[];
  currentTime: number;
  duration: number;
  onTimeSeek: (time: number) => void;
  onSegmentClick: (timestamp: Timestamp) => void;
  isPlaying?: boolean;
}

export function Timeline({ 
  timestamps, 
  currentTime, 
  duration, 
  onTimeSeek, 
  onSegmentClick,
  isPlaying = false 
}: TimelineProps) {
  const [hoveredSegment, setHoveredSegment] = useState<string | null>(null);
  const [hoveredBox, setHoveredBox] = useState<string | null>(null);
  const timelineRef = useRef<HTMLDivElement>(null);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getSegmentColor = (index: number): string => {
    const colors = [
      'bg-blue-500',
      'bg-green-500', 
      'bg-purple-500',
      'bg-orange-500',
      'bg-pink-500',
      'bg-indigo-500',
      'bg-teal-500',
      'bg-red-500'
    ];
    return colors[index % colors.length];
  };

  const handleTimelineHover = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current) return;
    
    const rect = timelineRef.current.getBoundingClientRect();
    const hoverX = event.clientX - rect.left;
    const percentage = hoverX / rect.width;
    const targetTime = percentage * duration;
    
    // Find which segment this hover position corresponds to
    const hoveredTimestamp = timestamps.find(timestamp => 
      timestamp.startTime !== undefined && 
      timestamp.endTime !== undefined &&
      targetTime >= timestamp.startTime && 
      targetTime < timestamp.endTime
    );
    
    if (hoveredTimestamp) {
      setHoveredSegment(hoveredTimestamp.time);
    } else {
      setHoveredSegment(null);
    }
  };

  const getCurrentSegment = (): Timestamp | null => {
    return timestamps.find(timestamp => 
      timestamp.startTime !== undefined && 
      timestamp.endTime !== undefined &&
      currentTime >= timestamp.startTime && 
      currentTime < timestamp.endTime
    ) || null;
  };

  const handleTimelineClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!timelineRef.current) return;
    
    const rect = timelineRef.current.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const percentage = clickX / rect.width;
    const targetTime = percentage * duration;
    
    onTimeSeek(targetTime);
  };

  const currentSegment = getCurrentSegment();

  return (
    <div className="space-y-4">
      {/* Main Timeline Bar */}
      <div className="relative group">
        {/* Invisible hover zone for better UX */}
        <div 
          className="absolute -top-2 -bottom-2 left-0 right-0 z-10 cursor-pointer"
          onClick={handleTimelineClick}
          onMouseMove={handleTimelineHover}
          onMouseLeave={() => setHoveredSegment(null)}
        />
        
        <div 
          ref={timelineRef}
          className="h-1.5 bg-muted/50 rounded-full relative overflow-hidden group-hover:h-2 transition-all duration-300 ease-out"
        >
          {/* Segment Blocks */}
          {timestamps.map((timestamp, index) => {
            if (!timestamp.startTime || !timestamp.endTime) return null;
            const startPercentage = (timestamp.startTime / duration) * 100;
            const widthPercentage = ((timestamp.endTime - timestamp.startTime) / duration) * 100;
            const isActive = currentSegment?.time === timestamp.time;
            const isHovered = hoveredSegment === timestamp.time;
            
            return (
              <div
                key={timestamp.time}
                className={cn(
                  "absolute top-0 h-full transition-all duration-300 ease-out",
                  getSegmentColor(index),
                  isHovered && "brightness-110 scale-y-125",
                  isActive && "brightness-110"
                )}
                style={{
                  left: `${startPercentage}%`,
                  width: `${widthPercentage}%`
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onSegmentClick(timestamp);
                }}
              />
            );
          })}
          
          {/* Progress Indicator - Circular Dot */}
          <div 
            className="absolute top-1/2 w-3 h-3 bg-primary rounded-full shadow-lg z-20 transition-all duration-100 -translate-y-1/2 -translate-x-1/2"
            style={{ left: `${(currentTime / duration) * 100}%` }}
          />
        </div>

        {/* Enhanced Hover Tooltip */}
        {hoveredSegment && (
          <div className="absolute -top-20 left-0 right-0 z-30 pointer-events-none">
            {timestamps
              .filter(t => t.time === hoveredSegment && t.startTime !== undefined && t.endTime !== undefined)
              .map(timestamp => {
                const segmentMidpoint = ((timestamp.startTime! + timestamp.endTime!) / 2 / duration) * 100;
                return (
                  <div
                    key={timestamp.time}
                    className="absolute bg-popover text-popover-foreground p-3 rounded-lg shadow-xl border max-w-xs animate-fade-in"
                    style={{
                      left: `${segmentMidpoint}%`,
                      transform: 'translateX(-50%)'
                    }}
                  >
                    <div className="font-semibold text-sm">{timestamp.label}</div>
                    <div className="text-xs text-muted-foreground">
                      {formatTime(timestamp.startTime!)} - {formatTime(timestamp.endTime!)}
                    </div>
                    {timestamp.description && (
                      <div className="text-xs mt-1 opacity-90">{timestamp.description}</div>
                    )}
                  </div>
                );
              })
            }
          </div>
        )}
      </div>

      {/* Time Display and Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="text-sm font-mono">
            {formatTime(currentTime)} / {formatTime(duration)}
          </div>
          {currentSegment && (
            <div className="text-sm text-muted-foreground">
              Current: {currentSegment.label}
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const currentIndex = timestamps.findIndex(t => t.time === currentSegment?.time);
              if (currentIndex > 0) {
                onSegmentClick(timestamps[currentIndex - 1]);
              }
            }}
            disabled={!currentSegment || timestamps.findIndex(t => t.time === currentSegment.time) === 0}
          >
            <SkipBack className="h-4 w-4" />
          </Button>
          
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const currentIndex = timestamps.findIndex(t => t.time === currentSegment?.time);
              if (currentIndex < timestamps.length - 1) {
                onSegmentClick(timestamps[currentIndex + 1]);
              }
            }}
            disabled={!currentSegment || timestamps.findIndex(t => t.time === currentSegment.time) === timestamps.length - 1}
          >
            <SkipForward className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Segment List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2 relative">
        {timestamps.map((timestamp, index) => {
          const isActive = currentSegment?.time === timestamp.time;
          return (
            <Button
              key={timestamp.time}
              variant="outline"
              size="sm"
              className={cn(
                "justify-start text-left h-auto p-3 transition-all",
                isActive && "ring-2 ring-primary bg-primary/10"
              )}
              onClick={() => onSegmentClick(timestamp)}
              onMouseEnter={() => setHoveredBox(timestamp.time)}
              onMouseLeave={() => setHoveredBox(null)}
            >
              <div className={cn("w-3 h-3 rounded mr-3 flex-shrink-0", getSegmentColor(index))} />
              <div className="min-w-0 flex-1">
                <div className="font-medium truncate">{timestamp.label}</div>
                <div className="text-xs text-muted-foreground">
                  {timestamp.startTime ? formatTime(timestamp.startTime) : timestamp.time}
                </div>
              </div>
            </Button>
          );
        })}
        
        {/* Box Hover Tooltip */}
        {hoveredBox && (
          <div className="absolute -top-32 left-1/2 transform -translate-x-1/2 z-30 pointer-events-none">
            {timestamps
              .filter(t => t.time === hoveredBox && t.startTime !== undefined && t.endTime !== undefined)
              .map(timestamp => (
                <div
                  key={`box-${timestamp.time}`}
                  className="bg-popover text-popover-foreground p-3 rounded-lg shadow-lg border max-w-xs"
                >
                  <div className="font-semibold">{timestamp.label}</div>
                  <div className="text-sm text-muted-foreground">
                    {formatTime(timestamp.startTime!)} - {formatTime(timestamp.endTime!)}
                  </div>
                  <div className="text-sm mt-1">{timestamp.description}</div>
                </div>
              ))
            }
          </div>
        )}
      </div>
    </div>
  );
}