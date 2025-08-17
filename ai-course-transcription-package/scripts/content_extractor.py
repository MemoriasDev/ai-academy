#!/usr/bin/env python3
"""
Content extraction system for analyzing transcripts and extracting
core programming principles, instructions, and learning materials.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LearningPrinciple:
    """Represents an extracted learning principle."""
    title: str
    description: str
    category: str  # e.g., "algorithms", "data_structures", "design_patterns"
    keywords: List[str]
    timestamp_start: float
    timestamp_end: float
    context: str
    difficulty_level: str  # "beginner", "intermediate", "advanced"
    code_examples: List[str] = None

@dataclass
class InstructionSegment:
    """Represents a step-by-step instruction segment."""
    step_number: int
    instruction: str
    timestamp_start: float
    timestamp_end: float
    action_type: str  # "explanation", "demonstration", "exercise", "review"
    related_concepts: List[str]
    code_snippets: List[str] = None

@dataclass
class ClassSession:
    """Represents analysis of a complete class session."""
    cohort: str
    week: str
    session_number: int
    title: str
    duration: float
    principles: List[LearningPrinciple]
    instructions: List[InstructionSegment]
    key_topics: List[str]
    summary: str
    difficulty_progression: List[str]

class ContentExtractor:
    """Extract structured learning content from transcripts."""
    
    def __init__(self):
        self.programming_keywords = self._load_programming_keywords()
        self.instruction_patterns = self._compile_instruction_patterns()
        self.concept_categories = self._define_concept_categories()
    
    def _load_programming_keywords(self) -> Dict[str, List[str]]:
        """Load comprehensive programming keywords by category."""
        return {
            "data_structures": [
                "array", "list", "dictionary", "hash table", "tree", "graph",
                "stack", "queue", "heap", "linked list", "set", "tuple"
            ],
            "algorithms": [
                "sort", "search", "recursion", "iteration", "binary search",
                "merge sort", "quick sort", "depth first", "breadth first",
                "dynamic programming", "greedy", "divide and conquer"
            ],
            "concepts": [
                "variable", "function", "class", "object", "method", "property",
                "inheritance", "polymorphism", "encapsulation", "abstraction",
                "interface", "module", "package", "import"
            ],
            "control_flow": [
                "if", "else", "elif", "for", "while", "loop", "break", "continue",
                "return", "yield", "exception", "try", "catch", "finally"
            ],
            "paradigms": [
                "object oriented", "functional", "procedural", "declarative",
                "imperative", "reactive", "asynchronous", "concurrent"
            ],
            "tools": [
                "debugger", "testing", "unit test", "integration test",
                "git", "version control", "ide", "compiler", "interpreter"
            ]
        }
    
    def _compile_instruction_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns to identify instructional content."""
        patterns = [
            r"(?i)(?:first|next|then|now|step \d+)",  # Sequential indicators
            r"(?i)(?:let's|we're going to|we'll|we need to)",  # Action indicators
            r"(?i)(?:here's how|this is how|the way to)",  # Explanation indicators
            r"(?i)(?:notice that|observe|see how|look at)",  # Observation indicators
            r"(?i)(?:remember|important|key point|crucial)",  # Emphasis indicators
            r"(?i)(?:example|for instance|let me show you)",  # Example indicators
            r"(?i)(?:exercise|practice|try this|homework)",  # Practice indicators
        ]
        return [re.compile(pattern) for pattern in patterns]
    
    def _define_concept_categories(self) -> Dict[str, List[str]]:
        """Define how to categorize programming concepts."""
        return {
            "fundamentals": ["variables", "data types", "operators", "syntax"],
            "control_structures": ["conditionals", "loops", "functions"],
            "data_structures": ["arrays", "objects", "collections"],
            "algorithms": ["sorting", "searching", "optimization"],
            "object_oriented": ["classes", "inheritance", "polymorphism"],
            "functional": ["pure functions", "immutability", "higher order"],
            "system_design": ["architecture", "patterns", "scalability"],
            "tools_and_practices": ["debugging", "testing", "version control"]
        }
    
    def parse_transcript_file(self, transcript_path: str) -> Dict:
        """Parse a transcript file and extract structured content."""
        transcript_path = Path(transcript_path)
        
        with open(transcript_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata from header
        metadata = self._extract_metadata_from_header(content)
        
        # Parse timestamped segments
        segments = self._parse_timestamped_segments(content)
        
        return {
            'metadata': metadata,
            'segments': segments,
            'content': content
        }
    
    def _extract_metadata_from_header(self, content: str) -> Dict:
        """Extract metadata from transcript header."""
        metadata = {}
        
        # Look for metadata patterns
        patterns = {
            'source_file': r'\*\*Source File:\*\* (.+)',
            'duration': r'\*\*Duration:\*\* ([\d.]+) seconds',
            'language': r'\*\*Language:\*\* (\w+)',
            'model': r'\*\*Model:\*\* (\w+)',
            'segments': r'\*\*Segments:\*\* (\d+)',
            'file_hash': r'\*\*File Hash:\*\* ([a-f0-9]+)'
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                metadata[key] = match.group(1)
        
        return metadata
    
    def _parse_timestamped_segments(self, content: str) -> List[Dict]:
        """Parse timestamped segments from transcript."""
        segments = []
        
        # Pattern to match timestamped segments
        segment_pattern = r'\*\*\[([\d.]+)s → ([\d.]+)s\]\*\* (.+?)(?=\n\n|\n\*\*\[|$)'
        
        for match in re.finditer(segment_pattern, content, re.DOTALL):
            start_time = float(match.group(1))
            end_time = float(match.group(2))
            text = match.group(3).strip()
            
            segments.append({
                'start': start_time,
                'end': end_time,
                'duration': end_time - start_time,
                'text': text
            })
        
        return segments
    
    def extract_learning_principles(self, segments: List[Dict]) -> List[LearningPrinciple]:
        """Extract learning principles from transcript segments."""
        principles = []
        
        for i, segment in enumerate(segments):
            text = segment['text'].lower()
            
            # Check for programming concepts
            for category, keywords in self.programming_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        # Look for explanatory context around the keyword
                        context_segments = segments[max(0, i-2):min(len(segments), i+3)]
                        context = " ".join([s['text'] for s in context_segments])
                        
                        # Determine if this is a substantial explanation
                        if len(segment['text']) > 50 and any(
                            word in text for word in ['because', 'since', 'reason', 'why', 'how']
                        ):
                            principle = LearningPrinciple(
                                title=f"{keyword.title()} Concept",
                                description=segment['text'][:200] + "..." if len(segment['text']) > 200 else segment['text'],
                                category=category,
                                keywords=[keyword],
                                timestamp_start=segment['start'],
                                timestamp_end=segment['end'],
                                context=context[:300] + "..." if len(context) > 300 else context,
                                difficulty_level=self._assess_difficulty(segment['text']),
                                code_examples=self._extract_code_examples(segment['text'])
                            )
                            principles.append(principle)
        
        return self._deduplicate_principles(principles)
    
    def extract_instruction_segments(self, segments: List[Dict]) -> List[InstructionSegment]:
        """Extract step-by-step instruction segments."""
        instructions = []
        step_counter = 1
        
        for segment in segments:
            text = segment['text']
            
            # Check if segment contains instructional content
            is_instruction = any(pattern.search(text) for pattern in self.instruction_patterns)
            
            if is_instruction and len(text) > 30:
                action_type = self._classify_action_type(text)
                related_concepts = self._identify_related_concepts(text)
                
                instruction = InstructionSegment(
                    step_number=step_counter,
                    instruction=text,
                    timestamp_start=segment['start'],
                    timestamp_end=segment['end'],
                    action_type=action_type,
                    related_concepts=related_concepts,
                    code_snippets=self._extract_code_snippets(text)
                )
                
                instructions.append(instruction)
                step_counter += 1
        
        return instructions
    
    def _assess_difficulty(self, text: str) -> str:
        """Assess the difficulty level of content."""
        text_lower = text.lower()
        
        beginner_indicators = ['basic', 'simple', 'introduction', 'first', 'start']
        advanced_indicators = ['complex', 'advanced', 'sophisticated', 'optimization']
        
        if any(indicator in text_lower for indicator in advanced_indicators):
            return "advanced"
        elif any(indicator in text_lower for indicator in beginner_indicators):
            return "beginner"
        else:
            return "intermediate"
    
    def _classify_action_type(self, text: str) -> str:
        """Classify the type of instructional action."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['explain', 'because', 'reason', 'why']):
            return "explanation"
        elif any(word in text_lower for word in ['show', 'demonstrate', 'example']):
            return "demonstration"
        elif any(word in text_lower for word in ['try', 'exercise', 'practice']):
            return "exercise"
        elif any(word in text_lower for word in ['review', 'recap', 'summary']):
            return "review"
        else:
            return "instruction"
    
    def _identify_related_concepts(self, text: str) -> List[str]:
        """Identify programming concepts mentioned in text."""
        concepts = []
        text_lower = text.lower()
        
        for category, keywords in self.programming_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    concepts.append(keyword)
        
        return list(set(concepts))  # Remove duplicates
    
    def _extract_code_examples(self, text: str) -> List[str]:
        """Extract code-like content from text."""
        # Simple patterns for code detection
        code_patterns = [
            r'`([^`]+)`',  # Inline code
            r'```[\s\S]*?```',  # Code blocks
            r'\b\w+\([^)]*\)',  # Function calls
            r'\b\w+\.\w+',  # Method calls
        ]
        
        code_examples = []
        for pattern in code_patterns:
            matches = re.findall(pattern, text)
            code_examples.extend(matches)
        
        return code_examples
    
    def _extract_code_snippets(self, text: str) -> List[str]:
        """Extract code snippets from instructional text."""
        return self._extract_code_examples(text)  # Same implementation for now
    
    def _deduplicate_principles(self, principles: List[LearningPrinciple]) -> List[LearningPrinciple]:
        """Remove duplicate principles based on similarity."""
        unique_principles = []
        seen_titles = set()
        
        for principle in principles:
            if principle.title not in seen_titles:
                unique_principles.append(principle)
                seen_titles.add(principle.title)
        
        return unique_principles
    
    def analyze_class_session(self, transcript_path: str) -> ClassSession:
        """Perform complete analysis of a class session transcript."""
        # Parse transcript
        parsed = self.parse_transcript_file(transcript_path)
        
        # Extract content
        principles = self.extract_learning_principles(parsed['segments'])
        instructions = self.extract_instruction_segments(parsed['segments'])
        
        # Derive metadata from file path
        path_parts = Path(transcript_path).parts
        cohort = next((part for part in path_parts if 'cohort' in part), 'unknown')
        week = next((part for part in path_parts if 'week' in part), 'unknown')
        
        # Generate summary
        key_topics = list(set([p.category for p in principles]))
        difficulty_levels = [p.difficulty_level for p in principles]
        
        session = ClassSession(
            cohort=cohort,
            week=week,
            session_number=1,  # Could be derived from filename
            title=f"{cohort.replace('_', ' ').title()} - {week.replace('_', ' ').title()}",
            duration=float(parsed['metadata'].get('duration', 0)),
            principles=principles,
            instructions=instructions,
            key_topics=key_topics,
            summary=self._generate_session_summary(principles, instructions),
            difficulty_progression=difficulty_levels
        )
        
        return session
    
    def _generate_session_summary(self, principles: List[LearningPrinciple], 
                                instructions: List[InstructionSegment]) -> str:
        """Generate a concise summary of the session."""
        if not principles and not instructions:
            return "No significant content extracted."
        
        concept_counts = defaultdict(int)
        for principle in principles:
            concept_counts[principle.category] += 1
        
        main_topics = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        topic_list = [f"{topic} ({count} concepts)" for topic, count in main_topics]
        
        summary = f"Session covered {len(principles)} key principles across {len(concept_counts)} categories. "
        summary += f"Main focus areas: {', '.join(topic_list)}. "
        summary += f"Included {len(instructions)} instructional segments."
        
        return summary
    
    def save_analysis_report(self, session: ClassSession, output_path: str):
        """Save comprehensive analysis report."""
        report = {
            'session_info': {
                'cohort': session.cohort,
                'week': session.week,
                'title': session.title,
                'duration': session.duration,
                'summary': session.summary
            },
            'learning_principles': [asdict(p) for p in session.principles],
            'instruction_segments': [asdict(i) for i in session.instructions],
            'key_topics': session.key_topics,
            'difficulty_progression': session.difficulty_progression,
            'statistics': {
                'total_principles': len(session.principles),
                'total_instructions': len(session.instructions),
                'unique_categories': len(set(p.category for p in session.principles)),
                'avg_segment_duration': sum(i.timestamp_end - i.timestamp_start for i in session.instructions) / len(session.instructions) if session.instructions else 0
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Analysis report saved: {output_path}")

def main():
    """Test content extraction on existing transcripts."""
    extractor = ContentExtractor()
    
    # Find transcript files
    transcripts_dir = Path("../cohorts")
    transcript_files = list(transcripts_dir.rglob("*_transcript.txt"))
    
    if not transcript_files:
        print("No transcript files found. Run batch transcription first.")
        return
    
    # Analyze first transcript as test
    test_file = transcript_files[0]
    print(f"Analyzing: {test_file}")
    
    try:
        session = extractor.analyze_class_session(str(test_file))
        
        # Save analysis
        output_path = test_file.parent / f"{test_file.stem}_analysis.json"
        extractor.save_analysis_report(session, str(output_path))
        
        print(f"✅ Analysis complete!")
        print(f"📊 Found {len(session.principles)} principles, {len(session.instructions)} instructions")
        print(f"🎯 Key topics: {', '.join(session.key_topics)}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    main()
