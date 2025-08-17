import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ContentBlock {
  type: 'heading' | 'paragraph' | 'list' | 'emphasis' | 'section';
  level?: number;
  content: string;
  items?: string[];
  children?: ContentBlock[];
}

interface RichContentProps {
  content: string;
  className?: string;
}

export const RichContent: React.FC<RichContentProps> = ({ content, className }) => {
  const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set());
  const [copiedStates, setCopiedStates] = useState<Record<string, boolean>>({});

  const parseContent = (text: string): ContentBlock[] => {
    const blocks: ContentBlock[] = [];
    const lines = text.split('\n').filter(line => line.trim());
    
    let currentSection: ContentBlock | null = null;
    
    for (const line of lines) {
      const trimmed = line.trim();
      
      // Headings
      if (trimmed.match(/^#{1,3}\s/)) {
        if (currentSection) blocks.push(currentSection);
        const level = trimmed.match(/^(#{1,3})/)?.[1].length || 1;
        const headingText = trimmed.replace(/^#{1,3}\s+/, '');
        
        currentSection = {
          type: 'section',
          content: headingText,
          level,
          children: []
        };
      }
      // Bold text
      else if (trimmed.match(/^\*\*(.+)\*\*:/)) {
        const content = trimmed.replace(/^\*\*(.+)\*\*:\s*/, '$1');
        const block: ContentBlock = { type: 'emphasis', content };
        if (currentSection) {
          currentSection.children = currentSection.children || [];
          currentSection.children.push(block);
        } else {
          blocks.push(block);
        }
      }
      // List items
      else if (trimmed.match(/^[-*]\s/)) {
        const content = trimmed.replace(/^[-*]\s+/, '');
        const block: ContentBlock = { type: 'list', content, items: [content] };
        if (currentSection) {
          currentSection.children = currentSection.children || [];
          currentSection.children.push(block);
        } else {
          blocks.push(block);
        }
      }
      // Regular paragraphs
      else if (trimmed) {
        const block: ContentBlock = { type: 'paragraph', content: trimmed };
        if (currentSection) {
          currentSection.children = currentSection.children || [];
          currentSection.children.push(block);
        } else {
          blocks.push(block);
        }
      }
    }
    
    if (currentSection) blocks.push(currentSection);
    return blocks;
  };

  const toggleSection = (index: number) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSections(newExpanded);
  };

  const copyToClipboard = async (text: string, id: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedStates(prev => ({ ...prev, [id]: true }));
      setTimeout(() => {
        setCopiedStates(prev => ({ ...prev, [id]: false }));
      }, 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const renderBlock = (block: ContentBlock, index: number): React.ReactNode => {
    switch (block.type) {
      case 'section':
        const isExpanded = expandedSections.has(index);
        const hasChildren = block.children && block.children.length > 0;
        
        return (
          <div key={index} className="mb-6 last:mb-0">
            <Button
              variant="ghost"
              onClick={() => hasChildren && toggleSection(index)}
              className={cn(
                "w-full justify-start p-0 h-auto hover:bg-transparent",
                block.level === 1 && "text-2xl font-bold",
                block.level === 2 && "text-xl font-semibold", 
                block.level === 3 && "text-lg font-medium"
              )}
            >
              <div className="flex items-center w-full">
                {hasChildren && (
                  <div className="mr-2">
                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4 text-muted-foreground" />
                    ) : (
                      <ChevronRight className="h-4 w-4 text-muted-foreground" />
                    )}
                  </div>
                )}
                <span className="text-left text-foreground">{block.content}</span>
              </div>
            </Button>
            
            {hasChildren && (isExpanded || !hasChildren) && (
              <div className="mt-3 ml-6 space-y-3 animate-accordion-down">
                {block.children!.map((child, childIndex) => renderBlock(child, childIndex))}
              </div>
            )}
          </div>
        );
      
      case 'emphasis':
        return (
          <div key={index} className="mb-3">
            <strong className="font-semibold text-accent">{block.content}</strong>
          </div>
        );
        
      case 'paragraph':
        return (
          <p key={index} className="mb-3 text-foreground leading-relaxed">
            {block.content.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold">$1</strong>')
              .replace(/\*(.+?)\*/g, '<em class="italic text-muted-foreground">$1</em>')
              .split(/(<strong class="[^"]*">.*?<\/strong>|<em class="[^"]*">.*?<\/em>)/)
              .map((part, i) => {
                if (part.includes('<strong')) {
                  const text = part.replace(/<[^>]*>/g, '');
                  return <strong key={i} className="font-semibold">{text}</strong>;
                } else if (part.includes('<em')) {
                  const text = part.replace(/<[^>]*>/g, '');
                  return <em key={i} className="italic text-muted-foreground">{text}</em>;
                }
                return part;
              })}
          </p>
        );
        
      case 'list':
        return (
          <ul key={index} className="mb-3 space-y-1">
            <li className="flex items-start space-x-3">
              <div className="w-1.5 h-1.5 bg-primary rounded-full mt-2.5 flex-shrink-0" />
              <span className="text-foreground leading-relaxed">{block.content}</span>
            </li>
          </ul>
        );
        
      default:
        return null;
    }
  };

  const blocks = parseContent(content);

  return (
    <div className={cn("rich-content space-y-4", className)}>
      {blocks.map((block, index) => renderBlock(block, index))}
    </div>
  );
};