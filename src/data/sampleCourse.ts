import { Course } from '@/types/course';

export const sampleCourse: Course = {
  id: 'developer-productivity-ai',
  title: 'Developer Productivity Using Artificial Intelligence',
  description: 'Acquire the knowledge to design, build, and deploy generative AI agents and multi-agent systems in the context of your company.',
  weeks: [
    {
      id: 'week-1',
      title: 'Week 1: AI Development Fundamentals',
      description: 'Establish foundational concepts and tools for building AI-powered applications, progressing from basic LLM integration to production-ready monitoring.',
      lessons: [
        {
          id: 'lesson-1-1',
          title: 'LLM Fundamentals & Intuition',
          duration: '80 min',
          videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
          videoId: 'dQw4w9WgXcQ',
          content: `# LLM Fundamentals & Intuition

**Instructor:** John Cody Sokol (Head of Developer Relations & Strategy, Lockheed Martin)  
**Date:** May 20, 2024  
**Duration:** 80.2 minutes

## Course Introduction & Objectives

Welcome to Developer Productivity Using Artificial Intelligence! This course will help you acquire the knowledge to design, build, and deploy generative AI agents and multi-agent systems in the context of your company.

### Primary Learning Objectives
- Design, build, and deploy generative AI agents and multi-agent systems
- Increase individual developer productivity through AI assistance
- Build internal applications that leverage AI for your company
- Master the four-phase curriculum: Foundation → RAG → Tool Integration → Production

### Four-Phase Curriculum Structure

**Phase 1: Foundation** - LLM overview, LangChain, and LangSmith basics
**Phase 2: Retrieval Systems** - Retrieval Augmented Generation (RAG) to mitigate hallucination
**Phase 3: Tool Integration** - Chaining together different tools within an LLM
**Phase 4: Production Systems** - Agents, multi-agent systems, and AWS deployment

## Understanding LLMs

LLMs are fundamentally **next token predictors** enhanced by complex statistical analysis and probabilistic methods. They're not perfect - they're statistical models of the relationship between text and probability.

### Historical Context
LLMs are not the first generative text methods. Back in 2018-2019, people were using LSTMs and other methods. Transformers began taking off around 2016-2017. We've come an incredible distance in just 8 years.

## Markov Chain Foundation

To understand LLMs, we start with Markov chains - a simpler concept that shares the same core principle.

### What is a Markov Chain?
A Markov chain calculates the probability of the next word based on what word follows another word. For any sequence of words, you can predict what the full sequence will be starting from those words.

### Connection to LLMs
- **Markov chains:** Use random choice for next token
- **LLMs:** Use probabilistic methods based on context windows
- **Context window:** Instead of just one token, LLMs analyze entire context to determine the most probable next token

## Practical AI Integration

One of the most immediate applications is documentation generation. Using tools like Copilot or Gemini, you can:
- Add docstrings to functions in seconds
- Generate comprehensive documentation
- Customize the style and format through prompt engineering

### Prompt Engineering Speed
Creating effective prompts is fast and iterative:
1. **First attempt:** "Can you document this function?"
2. **Result analysis:** Review the output
3. **Refinement:** "I want you to modify the function with DocStrings"

This demonstrates the rapid iteration possible with generative AI for practical development tasks.`,
          codeExamples: [
            {
              id: 'code-1-1-1',
              title: 'Simple Markov Chain Implementation',
              language: 'python',
              code: `import random
from collections import defaultdict

class MarkovChain:
    def __init__(self, text):
        self.words = text.split()
        self.word_pairs = defaultdict(list)
        
        # Create word pairs
        for i in range(len(self.words) - 1):
            current_word = self.words[i]
            next_word = self.words[i + 1]
            self.word_pairs[current_word].append(next_word)
    
    def generate_text(self, start_word, max_length=100):
        if start_word not in self.word_pairs:
            return "Start word not found in training data"
        
        result = [start_word]
        current_word = start_word
        
        for _ in range(max_length - 1):
            if current_word not in self.word_pairs:
                break
            next_word = random.choice(self.word_pairs[current_word])
            result.append(next_word)
            current_word = next_word
        
        return ' '.join(result)

# Example usage with simple text
text = "This is a test. This is only a test."
chain = MarkovChain(text)
generated = chain.generate_text("This", 50)
print(generated)`
            },
            {
              id: 'code-1-1-2',
              title: 'AI-Powered Documentation Generation',
              language: 'python',
              code: `def undocumented_function(data, threshold):
    filtered = []
    for item in data:
        if item > threshold:
            filtered.append(item * 2)
    return filtered

# After AI documentation generation:

def process_data_with_threshold(data, threshold):
    """
    Process a list of numerical data by filtering and transforming values.
    
    Args:
        data (list): List of numerical values to process
        threshold (float): Minimum value threshold for inclusion
    
    Returns:
        list: Filtered and doubled values above the threshold
    
    Example:
        >>> process_data_with_threshold([1, 3, 5, 7], 3)
        [6, 10, 14]
    """
    filtered = []
    for item in data:
        if item > threshold:
            filtered.append(item * 2)
    return filtered`
            },
            {
              id: 'code-1-1-3',
              title: 'Basic LLM Integration Setup',
              language: 'python',
              code: `# Environment setup for LLM integration
import os
from langchain.llms import OpenAI

# Set up API key (never hardcode in production!)
api_key = os.getenv('OPENAI_API_KEY')

# Initialize LLM
llm = OpenAI(api_key=api_key)

# Simple prompt example
prompt = """As a technical support specialist, provide clear and concise 
instructions for the following problem:

User Problem: My code is running but the AI responses seem inconsistent.

Please provide a helpful response."""

# Generate response
response = llm.predict(prompt)
print(response)`
            }
          ],
          checklist: [
            {
              id: 'check-1-1-1',
              text: 'Understand LLMs as "next token predictors"',
              completed: false
            },
            {
              id: 'check-1-1-2', 
              text: 'Implement a basic Markov chain for text generation',
              completed: false
            },
            {
              id: 'check-1-1-3',
              text: 'Set up LangChain development environment',
              completed: false
            },
            {
              id: 'check-1-1-4',
              text: 'Create effective prompts using context and role assignment',
              completed: false
            },
            {
              id: 'check-1-1-5',
              text: 'Use AI for practical documentation generation',
              completed: false
            },
            {
              id: 'check-1-1-6',
              text: 'Understand the four-phase curriculum progression',
              completed: false
            }
          ],
          timestamps: [
            {
              time: '0:00',
              label: 'Course Introduction',
              description: 'Overview of course objectives and learning outcomes'
            },
            {
              time: '8:08',
              label: 'Four-Phase Curriculum',
              description: 'Foundation → RAG → Tool Integration → Production Systems'
            },
            {
              time: '17:19',
              label: 'LLM Reality Check',
              description: 'Understanding LLMs as statistical models, not magic'
            },
            {
              time: '20:20',
              label: 'Markov Chain Foundation',
              description: 'Building intuition for next-token prediction'
            },
            {
              time: '21:31',
              label: 'Hands-On Markov Demo',
              description: 'Implementing and testing a simple Markov chain'
            },
            {
              time: '26:25',
              label: 'Connection to Modern LLMs',
              description: 'How context windows improve upon Markov chains'
            },
            {
              time: '29:03',
              label: 'Prompt Engineering Basics',
              description: 'Zero-shot, one-shot, and few-shot prompting techniques'
            },
            {
              time: '39:22',
              label: 'Practical AI Integration',
              description: 'Using AI for documentation generation and code improvement'
            }
          ]
        },
        {
          id: 'lesson-1-2',
          title: 'Understanding Data in AI',
          duration: '15 min',
          videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
          videoId: 'dQw4w9WgXcQ',
          content: `# Understanding Data in AI

Data is the fuel that powers artificial intelligence. In this lesson, we'll explore different types of data, how to work with them, and best practices for data preparation.

## Types of Data in AI

### Structured Data
Data that follows a predefined format, like spreadsheets or databases.

### Unstructured Data  
Text, images, audio, and video that don't follow a specific structure.

### Time Series Data
Data points collected or recorded at specific time intervals.

## Data Quality Matters

The quality of your data directly impacts the performance of your AI models. Poor data leads to poor results, regardless of how sophisticated your algorithms are.

## Data Preprocessing Pipeline

A systematic approach to cleaning and preparing your data for machine learning models.`,
          codeExamples: [
            {
              id: 'code-1-2-1',
              title: 'Loading and Exploring Data',
              language: 'python',
              code: `import pandas as pd
import numpy as np

# Load a CSV file
df = pd.read_csv('sample_data.csv')

# Explore the data
print("Dataset shape:", df.shape)
print("\\nFirst 5 rows:")
print(df.head())

print("\\nData types:")
print(df.dtypes)

print("\\nSummary statistics:")
print(df.describe())`
            }
          ],
          checklist: [
            {
              id: 'check-1-2-1',
              text: 'Understand the difference between structured and unstructured data',
              completed: false
            },
            {
              id: 'check-1-2-2',
              text: 'Load a dataset using pandas',
              completed: false
            },
            {
              id: 'check-1-2-3',
              text: 'Perform basic data exploration',
              completed: false
            }
          ],
          timestamps: [
            {
              time: '0:00',
              label: 'Data Types Overview',
              description: 'Understanding different types of data in AI'
            },
            {
              time: '3:45',
              label: 'Data Quality',
              description: 'Why data quality is crucial for AI success'
            },
            {
              time: '8:20',
              label: 'Pandas Basics',
              description: 'Using pandas for data manipulation'
            }
          ]
        }
      ]
    },
    {
      id: 'week-2',
      title: 'Week 2: Machine Learning Fundamentals',
      description: 'Dive into core machine learning concepts and build your first predictive models.',
      lessons: [
        {
          id: 'lesson-2-1',
          title: 'Supervised vs Unsupervised Learning',
          duration: '18 min',
          videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
          videoId: 'dQw4w9WgXcQ',
          content: `# Supervised vs Unsupervised Learning

Understanding the fundamental paradigms of machine learning is crucial for choosing the right approach for your problem.

## Supervised Learning

In supervised learning, we have input-output pairs. The algorithm learns from examples where we know the correct answer.

### Common Applications:
- Image classification
- Spam email detection  
- Price prediction
- Medical diagnosis

## Unsupervised Learning

Here, we only have input data without corresponding output labels. The algorithm finds hidden patterns in the data.

### Common Applications:
- Customer segmentation
- Anomaly detection
- Data compression
- Recommendation systems`,
          codeExamples: [
            {
              id: 'code-2-1-1',
              title: 'Supervised Learning Example - Classification',
              language: 'python',
              code: `from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the iris dataset
iris = load_iris()
X, y = iris.data, iris.target

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create and train the model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")`
            }
          ],
          checklist: [
            {
              id: 'check-2-1-1',
              text: 'Understand the difference between supervised and unsupervised learning',
              completed: false
            },
            {
              id: 'check-2-1-2',
              text: 'Implement a supervised learning classifier',
              completed: false
            },
            {
              id: 'check-2-1-3',
              text: 'Evaluate model performance using appropriate metrics',
              completed: false
            }
          ],
          timestamps: [
            {
              time: '0:00',
              label: 'Learning Paradigms',
              description: 'Introduction to supervised and unsupervised learning'
            },
            {
              time: '5:30',
              label: 'Supervised Examples',
              description: 'Real-world applications of supervised learning'
            },
            {
              time: '12:00',
              label: 'Hands-on Implementation',
              description: 'Building your first classifier'
            }
          ]
        }
      ]
    }
  ]
};