import { useState, useEffect } from 'react';
import { Check, Copy, Code } from 'lucide-react';
// TODO: Re-enable when section checklists are implemented
// import { CheckSquare, Square, ListChecks } from 'lucide-react';
// import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { Lesson, Progress, ContentSection as ContentSectionType } from '@/types/course';
import { 
  loadProgress
  // TODO: Re-enable when section checklists are implemented
  // toggleChecklistItem, 
  // isChecklistItemCompleted,
  // markLessonComplete 
} from '@/lib/progressStorage';
import { ContentSection } from './content/ContentSection';

interface SynchronizedContentProps {
  lesson: Lesson;
  courseId: string;
  currentTime: number;
  contentSections: ContentSectionType[];
}

export function SynchronizedContent({ 
  lesson, 
  courseId, 
  currentTime, 
  contentSections 
}: SynchronizedContentProps) {
  const [progress, setProgress] = useState<Progress>(() => loadProgress(courseId));
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [activeSection, setActiveSection] = useState<ContentSectionType | null>(null);
  const { toast } = useToast();

  useEffect(() => {
    setProgress(loadProgress(courseId));
  }, [courseId]);

  useEffect(() => {
    // Find the current section based on current time
    const currentSection = contentSections.find(section => 
      currentTime >= section.startTime && currentTime < section.endTime
    );
    
    if (currentSection && currentSection.id !== activeSection?.id) {
      setActiveSection(currentSection);
    }
  }, [currentTime, contentSections, activeSection]);

  // TODO: Re-enable and modify when section checklists are implemented
  // const handleChecklistToggle = (itemId: string) => {
  //   toggleChecklistItem(courseId, lesson.id, itemId);
  //   const newProgress = loadProgress(courseId);
  //   setProgress(newProgress);

  //   // Check if all checklist items are completed
  //   const allCompleted = lesson.checklist.every(item => 
  //     isChecklistItemCompleted(newProgress, lesson.id, item.id)
  //   );

  //   if (allCompleted && !newProgress.completedLessons.includes(lesson.id)) {
  //     markLessonComplete(courseId, lesson.id);
  //     setProgress(loadProgress(courseId));
  //     toast({
  //       title: "Lesson completed! 🎉",
  //       description: "Great job finishing all the requirements.",
  //     });
  //   }
  // };

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

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!activeSection) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <Card className="text-center">
          <CardContent className="p-12">
            <div className="space-y-4">
              <h2 className="text-2xl font-semibold">Ready to Begin</h2>
              <p className="text-muted-foreground">
                Start the video to see synchronized lesson content that updates as you watch.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 animate-fade-in">
      {/* Section Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-3xl font-bold">{activeSection.title}</h1>
          <Badge variant="secondary" className="text-sm">
            {formatTime(activeSection.startTime)} - {formatTime(activeSection.endTime)}
          </Badge>
        </div>
        
        {progress.completedLessons.includes(lesson.id) && (
          <div className="flex items-center space-x-2 text-success">
            <Check className="h-5 w-5" />
            <span className="font-medium">Lesson completed</span>
          </div>
        )}
      </div>


      {/* Key Concepts - Enhanced Content Section 
          TODO: Add keyPoints to course.json for full functionality */}
      <ContentSection
        title="Key Concepts"
        content={activeSection.content}
        keyPoints={activeSection.keyPoints || []}
        learningObjectives={activeSection.learningObjectives}
        isActive={true}
        className="mb-6 animate-fade-in"
      />

      {/* Code Examples */}
      {activeSection.codeExamples.length > 0 && (
        <Card className="mb-6">
          <CardHeader className="pb-4">
            <CardTitle className="text-xl flex items-center">
              <Code className="h-5 w-5 mr-2 text-accent" />
              Try It Yourself
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {activeSection.codeExamples.map((example) => (
                <div key={example.id} className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold">{example.title}</h4>
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
                  <pre className="overflow-x-auto">
                    <code>{example.code}</code>
                  </pre>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Section Checklist - TODO: Enable when checklistItems are added to course.json */}
      {/* {activeSection.checklistItems && activeSection.checklistItems.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-xl flex items-center">
              <ListChecks className="h-5 w-5 mr-2 text-success" />
              Section Checklist
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              Complete these items for this section
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {activeSection.checklistItems.map((itemText, index) => {
                // Create a unique ID for section-specific checklist items
                const itemId = `${activeSection.id}-${index}`;
                const isCompleted = isChecklistItemCompleted(progress, lesson.id, itemId);
                return (
                  <div
                    key={itemId}
                    className="flex items-center space-x-3 p-3 rounded-lg hover:bg-secondary/30 transition-colors cursor-pointer"
                    onClick={() => handleChecklistToggle(itemId)}
                  >
                    {isCompleted ? (
                      <CheckSquare className="h-5 w-5 text-success flex-shrink-0" />
                    ) : (
                      <Square className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                    )}
                    <span className={cn(
                      "flex-1",
                      isCompleted ? 'line-through text-muted-foreground' : ''
                    )}>
                      {itemText}
                    </span>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )} */}
    </div>
  );
}