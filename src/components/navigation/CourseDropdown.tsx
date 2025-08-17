import { ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Course } from '@/types/course';

interface CourseDropdownProps {
  currentCourse: Course;
  courses?: Course[];
  onCourseSelect?: (course: Course) => void;
}

export function CourseDropdown({ currentCourse, courses, onCourseSelect }: CourseDropdownProps) {
  // For now, we'll just show the current course
  const availableCourses = courses || [currentCourse];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="flex items-center space-x-2 h-9 px-3">
          <span className="font-medium">{currentCourse.title}</span>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="w-80 bg-background border border-border">
        {availableCourses.map((course) => (
          <DropdownMenuItem
            key={course.id}
            onClick={() => onCourseSelect?.(course)}
            className="flex flex-col items-start space-y-1 p-3 cursor-pointer"
          >
            <div className="font-medium text-foreground">{course.title}</div>
            <div className="text-sm text-muted-foreground line-clamp-2">{course.description}</div>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}