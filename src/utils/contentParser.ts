import { Lesson, ContentSection, CodeExample } from '@/types/course';

// Convert time string (e.g., "5:30") to seconds
export function timeToSeconds(timeString: string): number {
  const parts = timeString.split(':').map(Number);
  if (parts.length === 2) {
    return parts[0] * 60 + parts[1];
  } else if (parts.length === 3) {
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }
  return 0;
}

// Parse lesson content into sections based on timestamps
export function parseContentIntoSections(lesson: Lesson): ContentSection[] {
  const sections: ContentSection[] = [];
  
  // Enhanced timestamps with start/end times
  const enhancedTimestamps = lesson.timestamps.map((timestamp, index) => ({
    ...timestamp,
    startTime: timeToSeconds(timestamp.time),
    endTime: index < lesson.timestamps.length - 1 
      ? timeToSeconds(lesson.timestamps[index + 1].time)
      : timeToSeconds(lesson.duration) || 3600 // Default to 60 minutes if no duration
  }));

  // Content mapping based on the actual lesson content
  const contentMapping: Record<string, {
    objectives: string[];
    keyPoints: string[];
    content: string;
    codeExamples: CodeExample[];
    checklist: string[];
  }> = {
    'Course Introduction': {
      objectives: [
        'Understand the course structure and objectives',
        'Learn about the four-phase curriculum progression',
        'Set expectations for AI-powered development'
      ],
      keyPoints: [
        'Course focuses on practical AI implementation',
        'Four phases: Foundation → RAG → Tools → Production',
        'Emphasis on increasing developer productivity'
      ],
      content: `# Course Introduction & Objectives

Welcome to Developer Productivity Using Artificial Intelligence! This course will help you acquire the knowledge to design, build, and deploy generative AI agents and multi-agent systems in the context of your company.

### Primary Learning Objectives
- Design, build, and deploy generative AI agents and multi-agent systems
- Increase individual developer productivity through AI assistance
- Build internal applications that leverage AI for your company
- Master the four-phase curriculum: Foundation → RAG → Tool Integration → Production`,
      codeExamples: [],
      checklist: [
        'Understand course objectives and structure',
        'Set up development environment',
        'Review prerequisite knowledge'
      ]
    },
    'Four-Phase Curriculum': {
      objectives: [
        'Understand the structured learning progression',
        'Identify key skills for each phase',
        'Plan your learning journey'
      ],
      keyPoints: [
        'Foundation phase covers LLM basics and LangChain',
        'RAG phase focuses on reducing hallucinations',
        'Tool integration enables complex workflows',
        'Production phase covers deployment and monitoring'
      ],
      content: `# Four-Phase Curriculum Structure

**Phase 1: Foundation** - LLM overview, LangChain, and LangSmith basics
**Phase 2: Retrieval Systems** - Retrieval Augmented Generation (RAG) to mitigate hallucination
**Phase 3: Tool Integration** - Chaining together different tools within an LLM
**Phase 4: Production Systems** - Agents, multi-agent systems, and AWS deployment

Each phase builds upon the previous, ensuring a solid foundation before advancing to more complex topics.`,
      codeExamples: [],
      checklist: [
        'Review each phase objectives',
        'Understand learning progression',
        'Identify personal learning goals'
      ]
    },
    'LLM Reality Check': {
      objectives: [
        'Understand LLMs as statistical models',
        'Set realistic expectations for AI capabilities',
        'Learn the fundamental nature of token prediction'
      ],
      keyPoints: [
        'LLMs are "next token predictors" with statistical analysis',
        'Not perfect - they are probabilistic models',
        'Understanding limitations is crucial for effective use'
      ],
      content: `# Understanding LLMs

LLMs are fundamentally **next token predictors** enhanced by complex statistical analysis and probabilistic methods. They're not perfect - they're statistical models of the relationship between text and probability.

### Historical Context
LLMs are not the first generative text methods. Back in 2018-2019, people were using LSTMs and other methods. Transformers began taking off around 2016-2017. We've come an incredible distance in just 8 years.`,
      codeExamples: [],
      checklist: [
        'Understand LLMs as statistical models',
        'Recognize the historical context of AI development',
        'Set realistic expectations for AI capabilities'
      ]
    },
    'Markov Chain Foundation': {
      objectives: [
        'Understand the fundamental concept of sequence prediction',
        'Learn how Markov chains relate to LLMs',
        'Build intuition for probabilistic text generation'
      ],
      keyPoints: [
        'Markov chains predict next word based on current word',
        'Foundation concept for understanding LLMs',
        'Probabilistic approach to text generation'
      ],
      content: `# Markov Chain Foundation

To understand LLMs, we start with Markov chains - a simpler concept that shares the same core principle.

### What is a Markov Chain?
A Markov chain calculates the probability of the next word based on what word follows another word. For any sequence of words, you can predict what the full sequence will be starting from those words.`,
      codeExamples: lesson.codeExamples.filter(code => code.id === 'code-1-1-1'),
      checklist: [
        'Understand Markov chain concept',
        'Implement basic Markov chain',
        'Test text generation with simple examples'
      ]
    },
    'Hands-On Markov Demo': {
      objectives: [
        'Implement a working Markov chain',
        'Experiment with different text inputs',
        'Understand probabilistic text generation'
      ],
      keyPoints: [
        'Simple implementation using word pairs',
        'Random selection from possible next words',
        'Foundation for understanding LLM improvements'
      ],
      content: `# Hands-On Markov Chain Implementation

Let's build a simple Markov chain to understand the core concept of next-token prediction. This implementation will show you how probabilistic text generation works at its most basic level.

The key insight is that by analyzing patterns in training text, we can predict likely next words and generate coherent sequences.`,
      codeExamples: lesson.codeExamples.filter(code => code.id === 'code-1-1-1'),
      checklist: [
        'Run the Markov chain implementation',
        'Experiment with different training texts',
        'Observe how training data affects output quality'
      ]
    },
    'Connection to Modern LLMs': {
      objectives: [
        'Understand how LLMs improve upon Markov chains',
        'Learn about context windows and their importance',
        'Connect simple concepts to modern AI'
      ],
      keyPoints: [
        'LLMs use context windows instead of single tokens',
        'Probabilistic methods are more sophisticated',
        'Same core principle with massive improvements'
      ],
      content: `# Connection to Modern LLMs

### Markov Chains vs LLMs
- **Markov chains:** Use random choice for next token
- **LLMs:** Use probabilistic methods based on context windows
- **Context window:** Instead of just one token, LLMs analyze entire context to determine the most probable next token

This evolution from simple word-pair analysis to sophisticated context understanding represents the core advancement in modern AI systems.`,
      codeExamples: lesson.codeExamples.filter(code => code.id === 'code-1-1-3'),
      checklist: [
        'Understand context window concept',
        'Compare Markov chains to modern LLMs',
        'Set up basic LLM integration'
      ]
    },
    'Prompt Engineering Basics': {
      objectives: [
        'Learn fundamental prompting techniques',
        'Understand zero-shot, one-shot, and few-shot prompting',
        'Practice effective prompt creation'
      ],
      keyPoints: [
        'Prompt engineering is fast and iterative',
        'Context and role assignment improve results',
        'Different techniques for different use cases'
      ],
      content: `# Prompt Engineering Basics

### Prompt Engineering Speed
Creating effective prompts is fast and iterative:
1. **First attempt:** "Can you document this function?"
2. **Result analysis:** Review the output
3. **Refinement:** "I want you to modify the function with DocStrings"

This demonstrates the rapid iteration possible with generative AI for practical development tasks.`,
      codeExamples: [],
      checklist: [
        'Practice basic prompting techniques',
        'Try different prompt variations',
        'Understand iterative refinement process'
      ]
    },
    'Practical AI Integration': {
      objectives: [
        'Apply AI to real development tasks',
        'Learn documentation generation techniques',
        'Practice AI-assisted coding workflows'
      ],
      keyPoints: [
        'Documentation generation is an immediate application',
        'AI can customize output style and format',
        'Rapid iteration enables quick improvements'
      ],
      content: `# Practical AI Integration

One of the most immediate applications is documentation generation. Using tools like Copilot or Gemini, you can:
- Add docstrings to functions in seconds
- Generate comprehensive documentation
- Customize the style and format through prompt engineering

This practical application demonstrates how AI can immediately increase developer productivity with minimal setup.`,
      codeExamples: lesson.codeExamples.filter(code => code.id === 'code-1-1-2'),
      checklist: [
        'Generate documentation for existing code',
        'Experiment with different documentation styles',
        'Practice AI-assisted development workflow'
      ]
    }
  };

  enhancedTimestamps.forEach((timestamp, index) => {
    const mappedContent = contentMapping[timestamp.label] || {
      objectives: ['Complete this section'],
      keyPoints: ['Key concepts from this section'],
      content: lesson.content,
      codeExamples: [],
      checklist: ['Review section content']
    };

    sections.push({
      id: `section-${index}`,
      title: timestamp.label,
      startTime: timestamp.startTime,
      endTime: timestamp.endTime,
      learningObjectives: mappedContent.objectives,
      keyPoints: mappedContent.keyPoints,
      content: mappedContent.content,
      codeExamples: mappedContent.codeExamples,
      checklistItems: mappedContent.checklist
    });
  });

  return sections;
}