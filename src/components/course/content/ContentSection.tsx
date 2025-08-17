import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Lightbulb, BookOpen, Target } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import { RichContent } from './RichContent';
import { cn } from '@/lib/utils';

interface ContentSectionProps {
  title: string;
  content: string;
  keyPoints: string[];
  learningObjectives: string[];
  isActive?: boolean;
  className?: string;
}

export const ContentSection: React.FC<ContentSectionProps> = ({
  title,
  content,
  keyPoints,
  learningObjectives,
  isActive = true,
  className
}) => {
  // Only expand sections that have content
  const initialExpanded = new Set(['content']);
  if (learningObjectives && learningObjectives.length > 0) {
    initialExpanded.add('objectives');
  }
  if (keyPoints && keyPoints.length > 0) {
    initialExpanded.add('keypoints');
  }
  const [expandedSections, setExpandedSections] = useState<Set<string>>(initialExpanded);

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  return (
    <div className={cn("content-section space-y-4", className)}>
      {/* Learning Objectives - TODO: Add learningObjectives to course.json */}
      {learningObjectives && learningObjectives.length > 0 && (
        <Card className="border-l-4 border-l-primary bg-primary/5">
          <CardHeader className="pb-3">
            <Button
              variant="ghost"
              onClick={() => toggleSection('objectives')}
              className="w-full justify-between p-0 h-auto hover:bg-transparent"
            >
              <CardTitle className="text-lg flex items-center">
                <Target className="h-5 w-5 mr-2 text-primary" />
                Learning Objectives
              </CardTitle>
              {expandedSections.has('objectives') ? (
                <ChevronUp className="h-4 w-4 text-muted-foreground" />
              ) : (
                <ChevronDown className="h-4 w-4 text-muted-foreground" />
              )}
            </Button>
          </CardHeader>
          {expandedSections.has('objectives') && (
            <CardContent className="pt-0">
              <ul className="space-y-3">
                {learningObjectives.map((objective, index) => (
                  <li key={index} className="flex items-start space-x-3 animate-fade-in">
                    <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                    <span className="text-foreground leading-relaxed">{objective}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          )}
        </Card>
      )}

      {/* Main Content */}
      <Card className="border-l-4 border-l-accent">
        <CardHeader className="pb-3">
          <Button
            variant="ghost"
            onClick={() => toggleSection('content')}
            className="w-full justify-between p-0 h-auto hover:bg-transparent"
          >
            <CardTitle className="text-xl flex items-center">
              <BookOpen className="h-5 w-5 mr-2 text-accent" />
              Key Concepts
              {isActive && <Badge variant="secondary" className="ml-2">Active</Badge>}
            </CardTitle>
            {expandedSections.has('content') ? (
              <ChevronUp className="h-4 w-4 text-muted-foreground" />
            ) : (
              <ChevronDown className="h-4 w-4 text-muted-foreground" />
            )}
          </Button>
        </CardHeader>
        {expandedSections.has('content') && (
          <CardContent className="pt-0">
            <div className="prose-enhanced max-w-none">
              <RichContent content={content} />
            </div>
          </CardContent>
        )}
      </Card>

      {/* Key Points Summary - TODO: Add keyPoints to course.json */}
      {keyPoints && keyPoints.length > 0 && (
        <Card className="border-l-4 border-l-warning bg-warning/5">
          <CardHeader className="pb-3">
            <Button
              variant="ghost"
              onClick={() => toggleSection('keypoints')}
              className="w-full justify-between p-0 h-auto hover:bg-transparent"
            >
              <CardTitle className="text-lg flex items-center">
                <Lightbulb className="h-5 w-5 mr-2 text-warning" />
                Key Points Summary
              </CardTitle>
              {expandedSections.has('keypoints') ? (
                <ChevronUp className="h-4 w-4 text-muted-foreground" />
              ) : (
                <ChevronDown className="h-4 w-4 text-muted-foreground" />
              )}
            </Button>
          </CardHeader>
          {expandedSections.has('keypoints') && (
            <CardContent className="pt-0">
              <div className="grid gap-3">
                {keyPoints.map((point, index) => (
                  <div 
                    key={index} 
                    className="flex items-start space-x-3 p-3 bg-background rounded-lg border border-warning/20 animate-fade-in"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="w-6 h-6 bg-warning/20 rounded-full flex items-center justify-center flex-shrink-0">
                      <span className="text-xs font-semibold text-warning">{index + 1}</span>
                    </div>
                    <span className="text-foreground leading-relaxed">{point}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          )}
        </Card>
      )}
    </div>
  );
};