import { ChevronRight, Home } from 'lucide-react';
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { Course, Week, Lesson } from '@/types/course';

interface BreadcrumbBarProps {
  course: Course;
  currentWeek?: Week;
  currentLesson?: Lesson;
  onNavigate?: (type: 'home' | 'course' | 'week', id?: string) => void;
}

export function BreadcrumbBar({ course, currentWeek, currentLesson, onNavigate }: BreadcrumbBarProps) {
  return (
    <div className="bg-muted/30 border-b border-border px-6 py-3">
      <Breadcrumb>
        <BreadcrumbList>
          <BreadcrumbItem>
            <BreadcrumbLink 
              href="#" 
              onClick={(e) => {
                e.preventDefault();
                onNavigate?.('home');
              }}
              className="flex items-center space-x-1"
            >
              <Home className="h-4 w-4" />
              <span>Home</span>
            </BreadcrumbLink>
          </BreadcrumbItem>
          
          <BreadcrumbSeparator>
            <ChevronRight className="h-4 w-4" />
          </BreadcrumbSeparator>
          
          <BreadcrumbItem>
            <BreadcrumbLink 
              href="#" 
              onClick={(e) => {
                e.preventDefault();
                onNavigate?.('course', course.id);
              }}
            >
              AI Development
            </BreadcrumbLink>
          </BreadcrumbItem>
          
          {currentWeek && (
            <>
              <BreadcrumbSeparator>
                <ChevronRight className="h-4 w-4" />
              </BreadcrumbSeparator>
              <BreadcrumbItem>
                <BreadcrumbLink 
                  href="#" 
                  onClick={(e) => {
                    e.preventDefault();
                    onNavigate?.('week', currentWeek.id);
                  }}
                >
                  Cohort 2
                </BreadcrumbLink>
              </BreadcrumbItem>
            </>
          )}
          
          {currentWeek && (
            <>
              <BreadcrumbSeparator>
                <ChevronRight className="h-4 w-4" />
              </BreadcrumbSeparator>
              <BreadcrumbItem>
                <BreadcrumbLink 
                  href="#" 
                  onClick={(e) => {
                    e.preventDefault();
                    onNavigate?.('week', currentWeek.id);
                  }}
                >
                  {currentWeek.title}
                </BreadcrumbLink>
              </BreadcrumbItem>
            </>
          )}
          
          {currentLesson && (
            <>
              <BreadcrumbSeparator>
                <ChevronRight className="h-4 w-4" />
              </BreadcrumbSeparator>
              <BreadcrumbItem>
                <BreadcrumbPage>{currentLesson.title}</BreadcrumbPage>
              </BreadcrumbItem>
            </>
          )}
        </BreadcrumbList>
      </Breadcrumb>
    </div>
  );
}