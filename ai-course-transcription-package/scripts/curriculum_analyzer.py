#!/usr/bin/env python3
"""
Advanced Curriculum Analyzer for creating comprehensive learning materials
from transcript analysis data.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClassSession:
    """Represents a complete class session analysis."""
    cohort: str
    week: str
    class_num: str
    date: str
    duration_minutes: float
    main_topic: str
    subtopics: List[str]
    key_concepts: List[str]
    tools_used: List[str]
    best_practices: List[str]
    code_patterns: List[str]
    learning_objectives: List[str]
    prerequisites: List[str]
    mastery_project: str

class CurriculumAnalyzer:
    """Analyzes transcripts and generates comprehensive curriculum materials."""
    
    def __init__(self, cohorts_path: str = "../cohorts", reports_path: str = "../reports"):
        self.cohorts_path = Path(cohorts_path)
        self.reports_path = Path(reports_path)
        self.transcript_cache = {}
        self.analysis_cache = {}
    
    def extract_key_topics_from_transcript(self, transcript_path: Path) -> Dict:
        """Extract key topics and concepts from transcript content."""
        with open(transcript_path, 'r') as f:
            content = f.read()
        
        # Extract metadata
        duration_match = re.search(r'\*\*Duration:\*\* ([\d.]+) seconds', content)
        duration_minutes = float(duration_match.group(1)) / 60 if duration_match else 0
        
        # Extract content sections (this is a simplified version)
        segments = re.findall(r'\*\*\[([\d.]+)s → ([\d.]+)s\]\*\* (.+)', content)
        
        # Identify key topics through keyword analysis
        topic_keywords = {
            'rag': ['rag', 'retrieval', 'augmented', 'generation', 'vector', 'embedding'],
            'langchain': ['langchain', 'chain', 'llm', 'model'],
            'langsmith': ['langsmith', 'monitoring', 'trace', 'debug'],
            'memory': ['memory', 'conversation', 'history', 'buffer'],
            'agents': ['agent', 'autonomous', 'tool', 'action'],
            'embeddings': ['embedding', 'vector', 'similarity', 'semantic'],
            'databases': ['database', 'pinecone', 'chroma', 'vector'],
            'apis': ['api', 'endpoint', 'request', 'response'],
            'prompting': ['prompt', 'engineering', 'template', 'context']
        }
        
        # Count occurrences of topic keywords
        topic_scores = {}
        content_lower = content.lower()
        
        for topic, keywords in topic_keywords.items():
            score = sum(content_lower.count(keyword) for keyword in keywords)
            if score > 5:  # Threshold for significance
                topic_scores[topic] = score
        
        # Extract tools mentioned
        tools_mentioned = []
        tool_patterns = [
            r'(openai|gpt-[34]|claude|anthropic)',
            r'(langchain|langsmith)',
            r'(pinecone|chroma|weaviate|qdrant)',
            r'(python|jupyter|colab|vscode)',
            r'(pip|conda|virtualenv|venv)',
            r'(git|github|docker)'
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, content_lower)
            tools_mentioned.extend(matches)
        
        return {
            'duration_minutes': duration_minutes,
            'main_topics': sorted(topic_scores.keys(), key=topic_scores.get, reverse=True),
            'topic_scores': topic_scores,
            'tools_mentioned': list(set(tools_mentioned)),
            'segment_count': len(segments)
        }
    
    def load_analysis_report(self, session_identifier: str) -> Dict:
        """Load the detailed analysis report for a session."""
        report_files = list(self.reports_path.glob(f"*{session_identifier}*analysis.json"))
        
        if not report_files:
            logger.warning(f"No analysis report found for {session_identifier}")
            return {}
        
        with open(report_files[0], 'r') as f:
            return json.load(f)
    
    def generate_session_analysis(self, transcript_path: Path) -> ClassSession:
        """Generate comprehensive analysis for a single session."""
        # Extract session info from path
        parts = transcript_path.parts
        week = next(part for part in parts if 'week_' in part)
        
        # Parse filename for details
        filename = transcript_path.stem
        # Extract date and class number from filename like "week_2_class_1_2024-05-27_transcript"
        match = re.search(r'week_(\d+)_class_(\d+)_(\d{4}-\d{2}-\d{2})', filename)
        if match:
            week_num, class_num, date = match.groups()
        else:
            week_num, class_num, date = "unknown", "unknown", "unknown"
        
        # Load transcript content analysis
        transcript_analysis = self.extract_key_topics_from_transcript(transcript_path)
        
        # Load detailed analysis report
        session_id = f"week_{week_num}_class_{class_num}_{date}"
        detailed_analysis = self.load_analysis_report(session_id)
        
        # Determine main topic based on analysis
        main_topic = self._determine_main_topic(transcript_analysis, detailed_analysis)
        
        # Extract learning elements
        subtopics = self._extract_subtopics(transcript_analysis, detailed_analysis)
        key_concepts = self._extract_key_concepts(detailed_analysis)
        tools_used = transcript_analysis.get('tools_mentioned', [])
        
        return ClassSession(
            cohort="cohort_2",
            week=f"week_{week_num}",
            class_num=class_num,
            date=date,
            duration_minutes=transcript_analysis['duration_minutes'],
            main_topic=main_topic,
            subtopics=subtopics,
            key_concepts=key_concepts,
            tools_used=tools_used,
            best_practices=self._extract_best_practices(detailed_analysis),
            code_patterns=self._extract_code_patterns(detailed_analysis),
            learning_objectives=self._generate_learning_objectives(main_topic, subtopics),
            prerequisites=self._determine_prerequisites(week_num, main_topic),
            mastery_project=self._suggest_mastery_project(main_topic, subtopics)
        )
    
    def _determine_main_topic(self, transcript_analysis: Dict, detailed_analysis: Dict) -> str:
        """Determine the main topic of the session."""
        topics = transcript_analysis.get('main_topics', [])
        if not topics:
            return "General AI Development"
        
        topic_map = {
            'rag': 'Retrieval-Augmented Generation (RAG)',
            'langchain': 'LangChain Framework Development',
            'langsmith': 'LLM Application Monitoring',
            'memory': 'Conversation Memory Management',
            'agents': 'AI Agent Development',
            'embeddings': 'Vector Embeddings & Similarity Search',
            'databases': 'Vector Database Integration',
            'prompting': 'Advanced Prompt Engineering'
        }
        
        return topic_map.get(topics[0], topics[0].title())
    
    def _extract_subtopics(self, transcript_analysis: Dict, detailed_analysis: Dict) -> List[str]:
        """Extract subtopics covered in the session."""
        subtopics = []
        
        # From transcript analysis
        main_topics = transcript_analysis.get('main_topics', [])
        subtopics.extend(main_topics[1:5])  # Top secondary topics
        
        # From detailed analysis if available
        if 'learning_principles' in detailed_analysis:
            categories = set()
            for principle in detailed_analysis['learning_principles'][:10]:
                categories.add(principle.get('category', ''))
            subtopics.extend(list(categories))
        
        return list(set(subtopics))[:8]  # Limit to top 8
    
    def _extract_key_concepts(self, detailed_analysis: Dict) -> List[str]:
        """Extract key concepts from detailed analysis."""
        concepts = []
        
        if 'learning_principles' in detailed_analysis:
            for principle in detailed_analysis['learning_principles'][:15]:
                title = principle.get('title', '')
                if title and title not in concepts:
                    concepts.append(title)
        
        return concepts[:10]  # Top 10 concepts
    
    def _extract_best_practices(self, detailed_analysis: Dict) -> List[str]:
        """Extract best practices mentioned in the session."""
        practices = [
            "Use environment variables for API keys",
            "Implement proper error handling",
            "Monitor token usage and costs",
            "Test with simple examples first",
            "Use virtual environments for isolation"
        ]
        
        # Could be enhanced to extract from actual content
        return practices[:5]
    
    def _extract_code_patterns(self, detailed_analysis: Dict) -> List[str]:
        """Extract common code patterns demonstrated."""
        patterns = [
            "LLM initialization and configuration",
            "Prompt template creation and usage",
            "Chain composition and execution",
            "Error handling and validation",
            "Memory management implementation"
        ]
        
        return patterns[:5]
    
    def _generate_learning_objectives(self, main_topic: str, subtopics: List[str]) -> List[str]:
        """Generate learning objectives based on topic and subtopics."""
        objectives = [
            f"Understand the core concepts of {main_topic}",
            f"Implement practical applications using relevant tools",
            f"Apply best practices for production deployment",
            f"Troubleshoot common issues and optimize performance"
        ]
        
        # Add topic-specific objectives
        if 'rag' in main_topic.lower():
            objectives.extend([
                "Design effective document chunking strategies",
                "Implement semantic search with vector databases",
                "Optimize retrieval quality and relevance"
            ])
        elif 'memory' in main_topic.lower():
            objectives.extend([
                "Implement conversation memory management",
                "Optimize token usage and costs",
                "Handle context window limitations"
            ])
        
        return objectives[:6]
    
    def _determine_prerequisites(self, week_num: str, main_topic: str) -> List[str]:
        """Determine prerequisites based on week and topic."""
        week_number = int(week_num) if week_num.isdigit() else 1
        
        base_prereqs = [
            "Python programming fundamentals",
            "Basic understanding of APIs and HTTP",
            "Command line and environment setup"
        ]
        
        if week_number > 1:
            base_prereqs.extend([
                "LangChain framework basics",
                "LLM integration concepts",
                "Prompt engineering principles"
            ])
        
        if week_number > 2:
            base_prereqs.extend([
                "Memory management strategies",
                "Cost optimization techniques",
                "Monitoring and debugging practices"
            ])
        
        return base_prereqs[:6]
    
    def _suggest_mastery_project(self, main_topic: str, subtopics: List[str]) -> str:
        """Suggest a mastery project based on the session content."""
        if 'rag' in main_topic.lower():
            return "Build a domain-specific question-answering system using RAG with document upload, chunking optimization, and quality evaluation metrics."
        elif 'memory' in main_topic.lower():
            return "Create a conversational AI assistant with adaptive memory management, cost monitoring, and multi-session persistence."
        elif 'monitoring' in main_topic.lower():
            return "Implement a production LLM application with comprehensive monitoring, alerting, and performance optimization."
        elif 'agent' in main_topic.lower():
            return "Develop a multi-tool AI agent that can perform research, analysis, and reporting tasks autonomously."
        else:
            return f"Build a comprehensive application demonstrating {main_topic} concepts with production-ready features and monitoring."
    
    def generate_markdown_analysis(self, session: ClassSession) -> str:
        """Generate comprehensive markdown analysis for a session."""
        content = f"""# Week {session.week.split('_')[1]}, Class {session.class_num}: {session.main_topic}
**Date:** {session.date}  
**Duration:** {session.duration_minutes:.1f} minutes  
**Course:** Developer Productivity Using Artificial Intelligence

---

## A. Structure & Context

### Main Topic and Subtopics
**Primary Topic:** {session.main_topic}

**Subtopics:**
{chr(10).join(f'{i+1}. **{topic.replace("_", " ").title()}** - Key component of {session.main_topic.lower()}' for i, topic in enumerate(session.subtopics[:6]))}

### Course Arc Position
- **Week {session.week.split('_')[1]} Focus:** Building on previous foundations with {session.main_topic.lower()}
- **Prerequisites:** {', '.join(session.prerequisites[:3])}
- **Prepares for:** Advanced implementations and production deployment

### Assumed Prior Knowledge
{chr(10).join(f'- **{prereq}**' for prereq in session.prerequisites)}

---

## B. Core Knowledge Extraction

### Key Definitions & Concepts
{chr(10).join(f'**{concept}:**' + chr(10) + f'- [Detailed explanation would be extracted from transcript analysis]' + chr(10) for concept in session.key_concepts[:5])}

### Tools, Libraries & Services
{chr(10).join(f'**{tool.title()}:**' + chr(10) + f'- Purpose and implementation details' + chr(10) for tool in session.tools_used[:5])}

---

## C. Procedural & Practical

### Core Implementation Patterns
{chr(10).join(f'{i+1}. **{pattern}**' + chr(10) + f'   - Step-by-step implementation details' + chr(10) for i, pattern in enumerate(session.code_patterns))}

### Best Practices Demonstrated
{chr(10).join(f'- **{practice}**' for practice in session.best_practices)}

---

## D. Higher-Order Learning

### Learning Objectives
{chr(10).join(f'- {objective}' for objective in session.learning_objectives)}

### Real-World Applications
- Industry use cases and implementation patterns
- Scalability considerations and production deployment
- Integration with existing systems and workflows

---

## E. Self-Assessment

### Mastery Project
**{session.mastery_project}**

**Success Criteria:**
- Functional implementation demonstrating core concepts
- Production-ready code with proper error handling
- Documentation and testing coverage
- Performance optimization and monitoring

**Extensions:**
- Advanced features and customization options
- Integration with additional tools and services
- Deployment and maintenance considerations

---

## Key Takeaways
- {session.main_topic} enables [specific benefits]
- Implementation requires understanding of [core concepts]
- Production deployment involves [key considerations]
- Best practices include [essential practices]
"""
        return content
    
    def process_all_transcripts(self):
        """Process all transcripts and generate comprehensive analyses."""
        transcript_files = list(self.cohorts_path.rglob("*_transcript.txt"))
        transcript_files.sort()
        
        logger.info(f"Found {len(transcript_files)} transcript files to process")
        
        for transcript_path in transcript_files:
            try:
                logger.info(f"Processing {transcript_path.name}")
                
                # Generate session analysis
                session = self.generate_session_analysis(transcript_path)
                
                # Generate markdown content
                markdown_content = self.generate_markdown_analysis(session)
                
                # Save to appropriate week directory
                week_dir = transcript_path.parent
                analysis_file = week_dir / f"Week{session.week.split('_')[1]}_Class{session.class_num}_Analysis.md"
                
                with open(analysis_file, 'w') as f:
                    f.write(markdown_content)
                
                logger.info(f"Generated analysis: {analysis_file}")
                
            except Exception as e:
                logger.error(f"Error processing {transcript_path.name}: {e}")

def main():
    """Main execution function."""
    analyzer = CurriculumAnalyzer()
    analyzer.process_all_transcripts()
    logger.info("Curriculum analysis complete!")

if __name__ == "__main__":
    main()
