import { ChevronDown, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

interface CohortDropdownProps {
  currentCohort?: string;
  cohorts?: string[];
  onCohortSelect?: (cohort: string) => void;
}

export function CohortDropdown({ currentCohort = "Cohort 2", cohorts, onCohortSelect }: CohortDropdownProps) {
  const availableCohorts = cohorts || ["Cohort 2"];

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="flex items-center space-x-2 h-9 px-3">
          <Users className="h-4 w-4" />
          <span className="font-medium">{currentCohort}</span>
          <ChevronDown className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start" className="w-40 bg-background border border-border">
        {availableCohorts.map((cohort) => (
          <DropdownMenuItem
            key={cohort}
            onClick={() => onCohortSelect?.(cohort)}
            className="flex items-center space-x-2 cursor-pointer"
          >
            <Users className="h-4 w-4" />
            <span>{cohort}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}