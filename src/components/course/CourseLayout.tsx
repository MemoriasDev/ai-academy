import { useState, useEffect } from 'react';
import { CourseSidebar } from './CourseSidebar';
import { VideoPlayerSecure } from './VideoPlayerSecure';
import { Timeline } from './Timeline';
import { SynchronizedContent } from './SynchronizedContent';
import { Course, Lesson, Week, Timestamp } from '@/types/course';
import { Button } from '@/components/ui/button';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { parseContentIntoSections, timeToSeconds } from '@/utils/contentParser';
import { useAuth } from '@/contexts/AuthContext';

interface CourseLayoutProps {
  course: Course;
  initialLesson?: Lesson | null;
  initialWeek?: Week | null;
  onLessonChange?: (lesson: Lesson, week: Week) => void;
}

export function CourseLayout({ course, initialLesson, initialWeek, onLessonChange }: CourseLayoutProps) {
  const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null);
  const [currentWeek, setCurrentWeek] = useState<Week | null>(null);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [videoDuration, setVideoDuration] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Use initial lesson if provided, otherwise default to first lesson
    if (initialLesson && initialWeek) {
      setCurrentLesson(initialLesson);
      setCurrentWeek(initialWeek);
      setVideoDuration(timeToSeconds(initialLesson.duration) || 4800);
    } else if (course.weeks.length > 0 && course.weeks[0].lessons.length > 0) {
      const firstWeek = course.weeks[0];
      const firstLesson = firstWeek.lessons[0];
      setCurrentWeek(firstWeek);
      setCurrentLesson(firstLesson);
      setVideoDuration(timeToSeconds(firstLesson.duration) || 4800);
    }
  }, [course, initialLesson, initialWeek]);

  const handleLessonSelect = (lesson: Lesson, week: Week) => {
    setCurrentLesson(lesson);
    setCurrentWeek(week);
    setCurrentTime(0);
    setVideoDuration(timeToSeconds(lesson.duration) || 4800);
    onLessonChange?.(lesson, week);
  };

  const getCurrentLessonIndex = () => {
    if (!currentLesson || !currentWeek) return -1;
    return currentWeek.lessons.findIndex(l => l.id === currentLesson.id);
  };

  const getNextLesson = (): { lesson: Lesson; week: Week } | null => {
    if (!currentLesson || !currentWeek) return null;
    
    const currentIndex = getCurrentLessonIndex();
    const nextIndex = currentIndex + 1;
    
    if (nextIndex < currentWeek.lessons.length) {
      return { lesson: currentWeek.lessons[nextIndex], week: currentWeek };
    }
    
    // Look for next week
    const currentWeekIndex = course.weeks.findIndex(w => w.id === currentWeek.id);
    const nextWeekIndex = currentWeekIndex + 1;
    
    if (nextWeekIndex < course.weeks.length && course.weeks[nextWeekIndex].lessons.length > 0) {
      const nextWeek = course.weeks[nextWeekIndex];
      return { lesson: nextWeek.lessons[0], week: nextWeek };
    }
    
    return null;
  };

  const getPreviousLesson = (): { lesson: Lesson; week: Week } | null => {
    if (!currentLesson || !currentWeek) return null;
    
    const currentIndex = getCurrentLessonIndex();
    const prevIndex = currentIndex - 1;
    
    if (prevIndex >= 0) {
      return { lesson: currentWeek.lessons[prevIndex], week: currentWeek };
    }
    
    // Look for previous week
    const currentWeekIndex = course.weeks.findIndex(w => w.id === currentWeek.id);
    const prevWeekIndex = currentWeekIndex - 1;
    
    if (prevWeekIndex >= 0) {
      const prevWeek = course.weeks[prevWeekIndex];
      const lastLessonIndex = prevWeek.lessons.length - 1;
      if (lastLessonIndex >= 0) {
        return { lesson: prevWeek.lessons[lastLessonIndex], week: prevWeek };
      }
    }
    
    return null;
  };

  const handleTimeSeek = (time: number) => {
    setCurrentTime(time);
    // Control the video player through the exposed window method
    if ((window as any).seekVideo) {
      (window as any).seekVideo(time);
    } else {
      console.warn('seekVideo function not available, video player may not be ready');
    }
  };

  const handleSegmentClick = (timestamp: Timestamp) => {
    // Use startTime if available (already in seconds), otherwise convert from string
    const targetTime = timestamp.startTime !== undefined 
      ? timestamp.startTime 
      : timeToSeconds(timestamp.time);
    
    setCurrentTime(targetTime);
    
    // Control the video player through the exposed window method
    if ((window as any).seekVideo) {
      (window as any).seekVideo(targetTime);
      console.log(`Seeking to timestamp: ${timestamp.label} at ${targetTime}s`);
    } else {
      console.warn('seekVideo function not available, video player may not be ready');
    }
  };

  // Enhance timestamps with start/end times
  const enhancedTimestamps = currentLesson ? currentLesson.timestamps.map((timestamp, index) => ({
    ...timestamp,
    startTime: timeToSeconds(timestamp.time),
    endTime: index < currentLesson.timestamps.length - 1 
      ? timeToSeconds(currentLesson.timestamps[index + 1].time)
      : videoDuration
  })) : [];

  const contentSections = currentLesson ? parseContentIntoSections(currentLesson) : [];

  const navigateToNext = () => {
    const next = getNextLesson();
    if (next) {
      handleLessonSelect(next.lesson, next.week);
    }
  };

  const navigateToPrevious = () => {
    const prev = getPreviousLesson();
    if (prev) {
      handleLessonSelect(prev.lesson, prev.week);
    }
  };

  if (!currentLesson) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-2">Loading Course...</h1>
          <p className="text-muted-foreground">Please wait while we load your course content.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex bg-background">
      {/* Sidebar */}
      {!sidebarCollapsed && (
        <CourseSidebar
          course={course}
          currentLessonId={currentLesson.id}
          onLessonSelect={handleLessonSelect}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Video Player */}
        <div className="bg-card border-b border-border p-6">
          <VideoPlayerSecure
            videoPath={currentLesson.videoPath}
            videoUrl={currentLesson.videoUrl}
            videoId={currentLesson.videoId}
            title={currentLesson.title}
            duration={currentLesson.duration}
            onTimeUpdate={setCurrentTime}
            onPlayStateChange={setIsPlaying}
          />
        </div>

        {/* Interactive Timeline */}
        <div className="bg-card border-b border-border p-6">
          <Timeline
            timestamps={enhancedTimestamps}
            currentTime={currentTime}
            duration={videoDuration}
            onTimeSeek={handleTimeSeek}
            onSegmentClick={handleSegmentClick}
            isPlaying={isPlaying}
          />
        </div>

        {/* Synchronized Content */}
        <div className="flex-1">
          <ScrollArea className="h-full">
            <SynchronizedContent
              lesson={currentLesson}
              courseId={course.id}
              currentTime={currentTime}
              contentSections={contentSections}
            />
            
            {/* Navigation */}
            <div className="max-w-4xl mx-auto p-6">
              <div className="flex items-center justify-between pt-8 border-t border-border">
                <Button
                  variant="outline"
                  onClick={navigateToPrevious}
                  disabled={!getPreviousLesson()}
                  className="flex items-center space-x-2"
                >
                  <ChevronLeft className="h-4 w-4" />
                  <span>Previous Lesson</span>
                </Button>

                <div className="text-sm text-muted-foreground">
                  Lesson {getCurrentLessonIndex() + 1} of {currentWeek?.lessons.length || 0} in {currentWeek?.title}
                </div>

                <Button
                  onClick={navigateToNext}
                  disabled={!getNextLesson()}
                  className="flex items-center space-x-2"
                >
                  <span>Next Lesson</span>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </ScrollArea>
        </div>
      </div>
    </div>
  );
}