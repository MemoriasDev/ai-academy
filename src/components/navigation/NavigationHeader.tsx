import { Play } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Logo } from './Logo';
import { CourseDropdown } from './CourseDropdown';
import { CohortDropdown } from './CohortDropdown';
import { UserProfile } from './UserProfile';
import { BreadcrumbBar } from './BreadcrumbBar';
import { Course, Week, Lesson } from '@/types/course';
import { loadProgress } from '@/lib/progressStorage';

interface NavigationHeaderProps {
  course: Course;
  currentWeek?: Week;
  currentLesson?: Lesson;
  onCourseSelect?: (course: Course) => void;
  onCohortSelect?: (cohort: string) => void;
  onResumeClick?: () => void;
  onNavigate?: (type: 'home' | 'course' | 'week', id?: string) => void;
}

export function NavigationHeader({ 
  course, 
  currentWeek, 
  currentLesson,
  onCourseSelect,
  onCohortSelect,
  onResumeClick,
  onNavigate
}: NavigationHeaderProps) {
  const progress = loadProgress(course.id);
  const hasProgress = progress.completedLessons.length > 0;

  return (
    <div className="bg-background border-b border-border">
      {/* Main Header */}
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-6">
          <Logo />
          <div className="flex items-center space-x-4">
            <CourseDropdown 
              currentCourse={course}
              onCourseSelect={onCourseSelect}
            />
            <CohortDropdown 
              onCohortSelect={onCohortSelect}
            />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {hasProgress && onResumeClick && (
            <Button 
              variant="outline" 
              onClick={onResumeClick}
              className="flex items-center space-x-2"
            >
              <Play className="h-4 w-4" />
              <span>Continue Learning</span>
            </Button>
          )}
          <UserProfile />
        </div>
      </div>

      {/* Breadcrumb Bar */}
      <BreadcrumbBar 
        course={course}
        currentWeek={currentWeek}
        currentLesson={currentLesson}
        onNavigate={onNavigate}
      />
    </div>
  );
}