import { Zap } from 'lucide-react';

export function Logo() {
  return (
    <div className="flex items-center space-x-2">
      <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
        <Zap className="h-5 w-5 text-primary-foreground" />
      </div>
      <span className="font-semibold text-lg text-foreground">AI Academy</span>
    </div>
  );
}