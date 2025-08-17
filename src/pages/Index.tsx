import { useState, useEffect } from 'react';
import { CourseLayout } from '@/components/course/CourseLayout';
import { NavigationHeader } from '@/components/navigation/NavigationHeader';
import { courseData } from '@/data/courseData';
import { Course, Week, Lesson } from '@/types/course';
import { getLastAccessedLesson, updateLastAccessedLesson } from '@/lib/progressStorage';

const Index = () => {
  const [currentLesson, setCurrentLesson] = useState<Lesson | null>(null);
  const [currentWeek, setCurrentWeek] = useState<Week | null>(null);

  useEffect(() => {
    // Try to resume from last accessed lesson
    const { lessonId } = getLastAccessedLesson(courseData.id);
    
    if (lessonId) {
      // Find the lesson and week
      for (const week of courseData.weeks) {
        const lesson = week.lessons.find(l => l.id === lessonId);
        if (lesson) {
          setCurrentLesson(lesson);
          setCurrentWeek(week);
          return;
        }
      }
    }
    
    // Default to first lesson if no progress
    if (courseData.weeks.length > 0 && courseData.weeks[0].lessons.length > 0) {
      const firstWeek = courseData.weeks[0];
      const firstLesson = firstWeek.lessons[0];
      setCurrentWeek(firstWeek);
      setCurrentLesson(firstLesson);
    }
  }, []);

  const handleResumeClick = () => {
    const { lessonId, timestamp } = getLastAccessedLesson(courseData.id);
    
    if (lessonId) {
      // Find and navigate to the lesson
      for (const week of courseData.weeks) {
        const lesson = week.lessons.find(l => l.id === lessonId);
        if (lesson) {
          setCurrentLesson(lesson);
          setCurrentWeek(week);
          // In a real implementation, we'd also seek to the timestamp
          break;
        }
      }
    }
  };

  const handleLessonChange = (lesson: Lesson, week: Week) => {
    setCurrentLesson(lesson);
    setCurrentWeek(week);
    updateLastAccessedLesson(courseData.id, lesson.id);
  };

  return (
    <div className="min-h-screen bg-background">
      <NavigationHeader
        course={courseData}
        currentWeek={currentWeek || undefined}
        currentLesson={currentLesson || undefined}
        onResumeClick={handleResumeClick}
      />
      <CourseLayout 
        course={courseData}
        initialLesson={currentLesson}
        initialWeek={currentWeek}
        onLessonChange={handleLessonChange}
      />
    </div>
  );
};

export default Index;
