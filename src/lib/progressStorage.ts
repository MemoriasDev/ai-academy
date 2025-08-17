import { Progress } from '@/types/course';

const PROGRESS_KEY = 'course_progress';

export const saveProgress = (progress: Progress): void => {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  } catch (error) {
    console.error('Failed to save progress:', error);
  }
};

export const loadProgress = (courseId: string): Progress => {
  try {
    const saved = localStorage.getItem(PROGRESS_KEY);
    if (saved) {
      const progress = JSON.parse(saved) as Progress;
      if (progress.courseId === courseId) {
        return progress;
      }
    }
  } catch (error) {
    console.error('Failed to load progress:', error);
  }
  
  return {
    courseId,
    completedLessons: [],
    checklistProgress: {},
    lastAccessedLesson: undefined,
    lastVideoTimestamp: 0,
    navigationHistory: []
  };
};

export const markLessonComplete = (courseId: string, lessonId: string): void => {
  const progress = loadProgress(courseId);
  if (!progress.completedLessons.includes(lessonId)) {
    progress.completedLessons.push(lessonId);
    saveProgress(progress);
  }
};

export const toggleChecklistItem = (courseId: string, lessonId: string, itemId: string): void => {
  const progress = loadProgress(courseId);
  if (!progress.checklistProgress[lessonId]) {
    progress.checklistProgress[lessonId] = [];
  }
  
  const completed = progress.checklistProgress[lessonId];
  const index = completed.indexOf(itemId);
  
  if (index >= 0) {
    completed.splice(index, 1);
  } else {
    completed.push(itemId);
  }
  
  saveProgress(progress);
};

export const isChecklistItemCompleted = (progress: Progress, lessonId: string, itemId: string): boolean => {
  return progress.checklistProgress[lessonId]?.includes(itemId) || false;
};

export const getLessonProgress = (progress: Progress, lessonId: string): number => {
  const totalItems = 1; // The lesson itself
  const completedItems = progress.completedLessons.includes(lessonId) ? 1 : 0;
  return completedItems / totalItems;
};

export const getWeekProgress = (progress: Progress, lessonIds: string[]): number => {
  if (lessonIds.length === 0) return 0;
  const completed = lessonIds.filter(id => progress.completedLessons.includes(id)).length;
  return completed / lessonIds.length;
};

export const updateLastAccessedLesson = (courseId: string, lessonId: string, timestamp?: number): void => {
  const progress = loadProgress(courseId);
  progress.lastAccessedLesson = lessonId;
  if (timestamp !== undefined) {
    progress.lastVideoTimestamp = timestamp;
  }
  
  // Update navigation history
  if (!progress.navigationHistory) {
    progress.navigationHistory = [];
  }
  
  const existingIndex = progress.navigationHistory.indexOf(lessonId);
  if (existingIndex >= 0) {
    progress.navigationHistory.splice(existingIndex, 1);
  }
  progress.navigationHistory.unshift(lessonId);
  
  // Keep only last 10 items
  if (progress.navigationHistory.length > 10) {
    progress.navigationHistory = progress.navigationHistory.slice(0, 10);
  }
  
  saveProgress(progress);
};

export const getLastAccessedLesson = (courseId: string): { lessonId?: string; timestamp?: number } => {
  const progress = loadProgress(courseId);
  return {
    lessonId: progress.lastAccessedLesson,
    timestamp: progress.lastVideoTimestamp
  };
};