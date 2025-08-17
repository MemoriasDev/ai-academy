export interface Lesson {
  id: string;
  title: string;
  duration: string;
  videoUrl: string;
  videoPath?: string; // Supabase storage path
  videoId: string;
  content: string;
  codeExamples?: CodeExample[];
  checklist: ChecklistItem[];
  timestamps: Timestamp[];
}

export interface CodeExample {
  id: string;
  title: string;
  language: string;
  code: string;
}

export interface ChecklistItem {
  id: string;
  text: string;
  completed: boolean;
}

export interface Timestamp {
  time: string;
  label: string;
  description: string;
  startTime?: number; // in seconds, calculated dynamically
  endTime?: number; // in seconds, calculated dynamically
}

export interface ContentSection {
  id: string;
  title: string;
  startTime: number;
  endTime: number;
  learningObjectives: string[];
  keyPoints: string[];
  content: string;
  codeExamples: CodeExample[];
  checklistItems: string[];
}

export interface Week {
  id: string;
  title: string;
  description: string;
  lessons: Lesson[];
}

export interface Course {
  id: string;
  title: string;
  description: string;
  weeks: Week[];
}

export interface Progress {
  courseId: string;
  completedLessons: string[];
  checklistProgress: Record<string, string[]>; // lessonId -> completed checklist item ids
  lastAccessedLesson?: string;
  lastVideoTimestamp?: number;
  navigationHistory?: string[];
}