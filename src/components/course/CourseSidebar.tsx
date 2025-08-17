import { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight, Play, CheckCircle2, Circle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Course, Week, Lesson, Progress } from '@/types/course';
import { loadProgress, getWeekProgress, getLessonProgress } from '@/lib/progressStorage';

interface CourseSidebarProps {
  course: Course;
  currentLessonId?: string;
  onLessonSelect: (lesson: Lesson, week: Week) => void;
}

export function CourseSidebar({ course, currentLessonId, onLessonSelect }: CourseSidebarProps) {
  const [expandedWeeks, setExpandedWeeks] = useState<Set<string>>(new Set(['week-1']));
  const [progress, setProgress] = useState<Progress>(() => loadProgress(course.id));

  useEffect(() => {
    setProgress(loadProgress(course.id));
  }, [course.id]);

  const toggleWeek = (weekId: string) => {
    const newExpanded = new Set(expandedWeeks);
    if (newExpanded.has(weekId)) {
      newExpanded.delete(weekId);
    } else {
      newExpanded.add(weekId);
    }
    setExpandedWeeks(newExpanded);
  };

  const isLessonCompleted = (lessonId: string) => {
    return progress.completedLessons.includes(lessonId);
  };

  return (
    <div className="w-80 bg-card border-r border-border flex flex-col">
      <div className="p-6 border-b border-border">
        <h1 className="text-xl font-semibold text-foreground mb-2">{course.title}</h1>
        <p className="text-sm text-muted-foreground">{course.description}</p>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-4 space-y-2">
          {course.weeks.map((week) => {
            const isExpanded = expandedWeeks.has(week.id);
            const weekProgressValue = getWeekProgress(progress, week.lessons.map(l => l.id));
            const completedLessons = week.lessons.filter(l => isLessonCompleted(l.id)).length;
            
            return (
              <div key={week.id} className="space-y-1">
                <Button
                  variant="ghost"
                  className="w-full justify-between p-3 h-auto text-left hover:bg-secondary"
                  onClick={() => toggleWeek(week.id)}
                >
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center space-x-2">
                      {isExpanded ? (
                        <ChevronDown className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      )}
                      <div>
                        <div className="font-medium text-sm">{week.title}</div>
                        <div className="text-xs text-muted-foreground">
                          {completedLessons}/{week.lessons.length} lessons completed
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-8 h-8 rounded-full border-2 border-border bg-background flex items-center justify-center">
                      {weekProgressValue === 1 ? (
                        <CheckCircle2 className="h-4 w-4 text-success" />
                      ) : (
                        <div 
                          className="w-3 h-3 rounded-full bg-primary" 
                          style={{ 
                            background: `conic-gradient(hsl(var(--primary)) ${weekProgressValue * 360}deg, hsl(var(--border)) 0deg)`
                          }}
                        />
                      )}
                    </div>
                  </div>
                </Button>

                {isExpanded && (
                  <div className="ml-4 space-y-1 slide-in">
                    {week.lessons.map((lesson) => {
                      const isActive = currentLessonId === lesson.id;
                      const isCompleted = isLessonCompleted(lesson.id);

                      return (
                        <Button
                          key={lesson.id}
                          variant="ghost"
                          className={cn(
                            "w-full justify-start p-3 h-auto text-left hover:bg-secondary/50",
                            isActive && "bg-primary/10 border border-primary/20"
                          )}
                          onClick={() => onLessonSelect(lesson, week)}
                        >
                          <div className="flex items-center space-x-3 w-full">
                            <div className="flex-shrink-0">
                              {isCompleted ? (
                                <CheckCircle2 className="h-4 w-4 text-success" />
                              ) : isActive ? (
                                <Play className="h-4 w-4 text-primary" />
                              ) : (
                                <Circle className="h-4 w-4 text-muted-foreground" />
                              )}
                            </div>
                            <div className="min-w-0 flex-1">
                              <div className="text-sm font-medium truncate">
                                {lesson.title}
                              </div>
                              <div className="text-xs text-muted-foreground">
                                {lesson.duration}
                              </div>
                            </div>
                          </div>
                        </Button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}