import { useState, useEffect } from 'react';
import { Check, Copy, CheckSquare, Square } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { Lesson, Progress, ChecklistItem } from '@/types/course';
import { 
  loadProgress, 
  saveProgress, 
  toggleChecklistItem, 
  isChecklistItemCompleted,
  markLessonComplete 
} from '@/lib/progressStorage';

interface LessonContentProps {
  lesson: Lesson;
  courseId: string;
}

export function LessonContent({ lesson, courseId }: LessonContentProps) {
  const [progress, setProgress] = useState<Progress>(() => loadProgress(courseId));
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    setProgress(loadProgress(courseId));
  }, [courseId]);

  const handleChecklistToggle = (itemId: string) => {
    toggleChecklistItem(courseId, lesson.id, itemId);
    const newProgress = loadProgress(courseId);
    setProgress(newProgress);

    // Check if all checklist items are completed
    const allCompleted = lesson.checklist.every(item => 
      isChecklistItemCompleted(newProgress, lesson.id, item.id)
    );

    if (allCompleted && !newProgress.completedLessons.includes(lesson.id)) {
      markLessonComplete(courseId, lesson.id);
      setProgress(loadProgress(courseId));
      toast({
        title: "Lesson completed! 🎉",
        description: "Great job finishing all the requirements.",
      });
    }
  };

  const copyToClipboard = async (code: string, exampleId: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(exampleId);
      setTimeout(() => setCopiedCode(null), 2000);
      toast({
        title: "Code copied!",
        description: "The code has been copied to your clipboard.",
      });
    } catch (err) {
      toast({
        title: "Failed to copy",
        description: "Could not copy code to clipboard.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Lesson Header */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">{lesson.title}</h1>
          <Badge variant="secondary" className="text-sm">
            {lesson.duration}
          </Badge>
        </div>
        
        {progress.completedLessons.includes(lesson.id) && (
          <div className="flex items-center space-x-2 text-success">
            <Check className="h-5 w-5" />
            <span className="font-medium">Lesson completed</span>
          </div>
        )}
      </div>

      {/* Lesson Content */}
      <div className="prose max-w-none">
        <div 
          className="lesson-content text-foreground"
          dangerouslySetInnerHTML={{ 
            __html: lesson.content.replace(/\n/g, '<br/>').replace(/^# (.+)/gm, '<h1>$1</h1>').replace(/^## (.+)/gm, '<h2>$1</h2>').replace(/^### (.+)/gm, '<h3>$1</h3>')
          }} 
        />
      </div>

      {/* Code Examples */}
      {lesson.codeExamples && lesson.codeExamples.length > 0 && (
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold">Code Examples</h2>
          {lesson.codeExamples.map((example) => (
            <Card key={example.id}>
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{example.title}</CardTitle>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline">{example.language}</Badge>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => copyToClipboard(example.code, example.id)}
                      className="text-xs"
                    >
                      {copiedCode === example.id ? (
                        <Check className="h-3 w-3 mr-1" />
                      ) : (
                        <Copy className="h-3 w-3 mr-1" />
                      )}
                      {copiedCode === example.id ? 'Copied!' : 'Copy'}
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <pre className="overflow-x-auto">
                  <code>{example.code}</code>
                </pre>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Checklist */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">Lesson Checklist</CardTitle>
          <p className="text-sm text-muted-foreground">
            Complete all items to mark this lesson as finished
          </p>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {lesson.checklist.map((item) => {
              const isCompleted = isChecklistItemCompleted(progress, lesson.id, item.id);
              return (
                <div
                  key={item.id}
                  className="flex items-center space-x-3 p-3 rounded-lg hover:bg-secondary/30 transition-colors cursor-pointer"
                  onClick={() => handleChecklistToggle(item.id)}
                >
                  {isCompleted ? (
                    <CheckSquare className="h-5 w-5 text-success flex-shrink-0" />
                  ) : (
                    <Square className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                  )}
                  <span className={`flex-1 ${isCompleted ? 'line-through text-muted-foreground' : ''}`}>
                    {item.text}
                  </span>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}