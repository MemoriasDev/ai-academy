#!/usr/bin/env python3
"""
Enhanced Fix Pass Script - Comprehensive timestamp fixes and intelligent rewrites
"""
import json
import re
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime

# Configuration
MIN_SEPARATION_S = 15  # Minimum 15 seconds between timestamps
MAX_GAP_PERCENT = 0.25  # Max 25% of video without coverage
LABEL_WORDS_MIN = 2
LABEL_WORDS_MAX = 5
DESC_WORDS_MIN = 5
DESC_WORDS_MAX = 15

# Generic terms to avoid in labels (unless with specific context)
GENERIC_TERMS = {
    "overview", "introduction", "discussion", "recap", "general", 
    "review", "summary", "basics", "fundamentals", "concepts"
}

# Technical keywords for better rewrites
TECH_KEYWORDS = {
    "llm": ["LLM", "language model", "AI model", "GPT"],
    "rag": ["RAG", "retrieval", "augmented", "vector", "embedding"],
    "agent": ["agent", "autonomous", "tool", "workflow"],
    "api": ["API", "endpoint", "REST", "request", "response"],
    "database": ["database", "DB", "SQL", "vector store", "index"],
    "deploy": ["deploy", "production", "hosting", "server"],
    "test": ["test", "validate", "QA", "unit test", "integration"],
    "config": ["config", "setup", "environment", "settings"],
    "chain": ["chain", "pipeline", "workflow", "sequence"],
    "prompt": ["prompt", "template", "instruction", "context"]
}

def normalize_time(time_str: str) -> str:
    """Normalize time to H:MM:SS format."""
    # Remove any trailing text in parentheses
    clean = re.sub(r'\s*\([^)]+\)', '', time_str.strip())
    
    # Parse time components
    parts = clean.split(':')
    if len(parts) == 2:
        # MM:SS format
        minutes = int(parts[0])
        seconds = int(parts[1])
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    elif len(parts) == 3:
        # H:MM:SS format - normalize
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        # Handle overflow
        minutes += seconds // 60
        seconds = seconds % 60
        hours += minutes // 60
        minutes = minutes % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return time_str  # Return as-is if can't parse

def time_to_seconds(time_str: str) -> int:
    """Convert H:MM:SS to seconds."""
    normalized = normalize_time(time_str)
    parts = normalized.split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0

def seconds_to_time(seconds: int) -> str:
    """Convert seconds to H:MM:SS format."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}"

def extract_keywords_from_content(content: str, title: str) -> List[str]:
    """Extract relevant keywords from lesson content and title."""
    keywords = []
    
    # Extract from title
    title_words = re.findall(r'\b[A-Z][a-z]+|\b[A-Z]+\b|\b\w+', title)
    keywords.extend([w.lower() for w in title_words if len(w) > 3])
    
    # Look for technical terms in content
    content_lower = content.lower()
    for category, terms in TECH_KEYWORDS.items():
        for term in terms:
            if term.lower() in content_lower:
                keywords.append(term.lower())
    
    # Find section headers (## or ###)
    headers = re.findall(r'^#{2,3}\s+(.+)$', content, re.MULTILINE)
    for header in headers[:5]:  # Use first 5 headers
        header_words = re.findall(r'\b\w+\b', header)
        keywords.extend([w.lower() for w in header_words if len(w) > 3])
    
    return list(set(keywords))  # Remove duplicates

def generate_smart_label(timestamp_idx: int, lesson_title: str, keywords: List[str], 
                         existing_labels: List[str]) -> str:
    """Generate a smart, specific label based on context."""
    # Try to find relevant technical keywords
    relevant_tech = [k for k in keywords if k not in GENERIC_TERMS]
    
    # Common patterns based on position in video
    if timestamp_idx == 0:
        if "introduction" not in existing_labels:
            return "Course Introduction"
    elif timestamp_idx == 1:
        if any(k in relevant_tech for k in ["setup", "config", "environment"]):
            return "Environment Setup"
    
    # Use technical keywords
    if "api" in relevant_tech:
        if "build" in relevant_tech:
            return "Build API"
        elif "test" in relevant_tech:
            return "Test API"
        else:
            return "API Configuration"
    
    if "rag" in relevant_tech:
        if "implement" in relevant_tech:
            return "Implement RAG"
        elif "vector" in relevant_tech:
            return "Vector Storage"
        else:
            return "RAG Pipeline"
    
    if "agent" in relevant_tech:
        if "multi" in relevant_tech:
            return "Multi-Agent System"
        elif "tool" in relevant_tech:
            return "Agent Tools"
        else:
            return "Agent Architecture"
    
    if "deploy" in relevant_tech:
        return "Production Deployment"
    
    if "test" in relevant_tech:
        return "Testing Strategy"
    
    # Fallback to position-based
    position_labels = [
        "Core Concepts", "Implementation Details", "Practical Example",
        "Code Walkthrough", "Best Practices", "Common Patterns",
        "Advanced Topics", "Troubleshooting", "Performance Tips",
        "Security Considerations", "Integration Points", "Next Steps"
    ]
    
    # Find unused label
    for label in position_labels:
        if label not in existing_labels:
            return label
    
    return f"Section {timestamp_idx + 1}"

def generate_smart_description(label: str, lesson_title: str, keywords: List[str]) -> str:
    """Generate a smart description that adds value beyond the label."""
    # Map labels to contextual descriptions
    label_lower = label.lower()
    
    # Extract main topic from lesson title
    title_keywords = [w for w in keywords if len(w) > 4][:2]
    topic = " and ".join(title_keywords) if title_keywords else "concepts"
    
    descriptions = {
        "course introduction": f"Overview of {topic} and learning objectives",
        "environment setup": f"Configure development tools for {topic}",
        "core concepts": f"Fundamental principles of {topic} explained",
        "implementation details": f"Step-by-step coding of {topic} features",
        "practical example": f"Real-world application of {topic} techniques",
        "code walkthrough": f"Line-by-line explanation of {topic} implementation",
        "best practices": f"Industry standards for {topic} development",
        "api configuration": f"Set up endpoints and authentication for {topic}",
        "rag pipeline": "Build retrieval and generation components",
        "vector storage": "Configure embeddings and similarity search",
        "agent architecture": "Design autonomous decision-making systems",
        "multi-agent system": "Coordinate multiple AI agents effectively",
        "production deployment": f"Deploy {topic} to cloud infrastructure",
        "testing strategy": f"Validate {topic} with comprehensive tests",
        "performance tips": f"Optimize {topic} for speed and efficiency",
        "troubleshooting": f"Debug common {topic} implementation issues",
        "next steps": f"Advanced topics and further {topic} resources"
    }
    
    # Try to find a matching description
    for key, desc in descriptions.items():
        if key in label_lower:
            return desc[:DESC_WORDS_MAX * 6]  # Rough character limit
    
    # Generate based on keywords
    if "build" in label_lower or "create" in label_lower:
        return f"Build functional {topic} with error handling"
    elif "test" in label_lower:
        return f"Validate {topic} functionality and edge cases"
    elif "deploy" in label_lower:
        return f"Deploy {topic} to production environment"
    elif "configure" in label_lower or "setup" in label_lower:
        return f"Configure {topic} parameters and dependencies"
    else:
        return f"Learn {topic} implementation techniques"

def fix_lesson_timestamps(lesson: Dict[str, Any], audit_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix all timestamp issues for a lesson."""
    lesson_id = lesson.get("id", "")
    title = lesson.get("title", "")
    duration_str = lesson.get("duration", "")
    content = lesson.get("content", "")[:2000]  # Use first 2000 chars for context
    timestamps = lesson.get("timestamps", [])
    
    # Track changes
    changes = []
    
    # 1. Fix duration format
    original_duration = duration_str
    duration_str = normalize_time(duration_str)
    duration_seconds = time_to_seconds(duration_str)
    if original_duration != duration_str:
        changes.append(f"Fixed duration format: {original_duration} -> {duration_str}")
    
    # 2. Normalize all timestamp times
    for ts in timestamps:
        original_time = ts.get("time", "")
        ts["time"] = normalize_time(original_time)
        if original_time != ts["time"]:
            changes.append(f"Normalized time: {original_time} -> {ts['time']}")
    
    # 3. Fix out-of-range timestamps
    timestamps = [ts for ts in timestamps if time_to_seconds(ts["time"]) < duration_seconds]
    
    # 4. Sort by time (fix order)
    timestamps.sort(key=lambda x: time_to_seconds(x["time"]))
    
    # 5. Fix density (merge too-close timestamps)
    merged_timestamps = []
    i = 0
    while i < len(timestamps):
        current = timestamps[i]
        current_seconds = time_to_seconds(current["time"])
        
        # Look for timestamps too close
        j = i + 1
        while j < len(timestamps) and time_to_seconds(timestamps[j]["time"]) - current_seconds < MIN_SEPARATION_S:
            # Merge descriptions
            current["description"] = current["description"] + "; " + timestamps[j]["description"]
            changes.append(f"Merged close timestamps: {current['time']} and {timestamps[j]['time']}")
            j += 1
        
        merged_timestamps.append(current)
        i = j
    
    timestamps = merged_timestamps
    
    # 6. Check coverage gaps
    if len(timestamps) > 1:
        max_gap = duration_seconds * MAX_GAP_PERCENT
        gaps_to_fill = []
        
        for i in range(1, len(timestamps)):
            prev_seconds = time_to_seconds(timestamps[i-1]["time"])
            curr_seconds = time_to_seconds(timestamps[i]["time"])
            gap = curr_seconds - prev_seconds
            
            if gap > max_gap:
                # Insert timestamp in the middle of the gap
                mid_point = prev_seconds + gap // 2
                gaps_to_fill.append({
                    "time": seconds_to_time(mid_point),
                    "label": "TO_REVIEW",
                    "description": "Section needs manual review for content"
                })
                changes.append(f"Added coverage timestamp at {seconds_to_time(mid_point)}")
        
        timestamps.extend(gaps_to_fill)
        timestamps.sort(key=lambda x: time_to_seconds(x["time"]))
    
    # 7. Extract keywords for smart rewrites
    keywords = extract_keywords_from_content(content, title)
    existing_labels = []
    
    # 8. Rewrite weak labels and descriptions
    for i, ts in enumerate(timestamps):
        original_label = ts.get("label", "")
        original_desc = ts.get("description", "")
        
        # Check if label needs rewriting
        label_words = original_label.split()
        is_generic = any(term in original_label.lower() for term in GENERIC_TERMS)
        needs_label_rewrite = (
            len(label_words) < LABEL_WORDS_MIN or 
            len(label_words) > LABEL_WORDS_MAX or
            is_generic or
            original_label in existing_labels or
            original_label == "TO_REVIEW"
        )
        
        if needs_label_rewrite and original_label != "TO_REVIEW":
            new_label = generate_smart_label(i, title, keywords, existing_labels)
            ts["label"] = new_label
            changes.append(f"Rewrote label at {ts['time']}: '{original_label}' -> '{new_label}'")
        
        existing_labels.append(ts["label"])
        
        # Check if description needs rewriting
        desc_words = original_desc.split()
        needs_desc_rewrite = (
            len(desc_words) < DESC_WORDS_MIN or
            len(desc_words) > DESC_WORDS_MAX or
            original_desc.lower() == original_label.lower() or
            "overview" in original_desc.lower() and len(desc_words) < 8
        )
        
        if needs_desc_rewrite:
            new_desc = generate_smart_description(ts["label"], title, keywords)
            ts["description"] = new_desc
            changes.append(f"Rewrote description at {ts['time']}: '{original_desc}' -> '{new_desc}'")
    
    # Flag if manual review needed
    if any(ts["label"] == "TO_REVIEW" for ts in timestamps):
        changes.append("Manual Review Required - coverage gaps filled with TO_REVIEW")
    
    return {
        "lesson_id": lesson_id,
        "original_timestamps": lesson.get("timestamps", []),
        "updated_timestamps": timestamps,
        "changes_summary": changes
    }

def main(dry_run=False):
    """Main processing function."""
    # Create backup first if not dry run
    if not dry_run:
        from datetime import datetime
        import shutil
        backup_dir = Path("src/content/.backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"course_backup_{timestamp}.json"
        shutil.copy2("src/content/course.json", backup_path)
        print(f"Created backup: {backup_path}")
    
    # Load course data
    with open("src/content/course.json", 'r') as f:
        course_data = json.load(f)
    
    # Load audit report
    with open("audits/course_timestamp_audit_report.json", 'r') as f:
        audit_report = json.load(f)
    
    # Process all lessons
    all_results = []
    
    for week in course_data.get("weeks", []):
        for lesson in week.get("lessons", []):
            lesson_id = lesson.get("id", "")
            
            # Find corresponding audit data
            audit_data = next(
                (l for l in audit_report.get("lessons", []) if l.get("lesson_id") == lesson_id),
                {}
            )
            
            # Fix the lesson
            result = fix_lesson_timestamps(lesson, audit_data)
            
            # Apply changes if not dry run
            if not dry_run:
                # Update duration
                if result["changes_summary"]:
                    # Update timestamps in the actual lesson
                    lesson["timestamps"] = result["updated_timestamps"]
                    # Update duration if it was changed
                    for change in result["changes_summary"]:
                        if "Fixed duration format:" in change:
                            new_duration = change.split(" -> ")[1]
                            lesson["duration"] = new_duration
                            break
            
            all_results.append(result)
            
            # Print progress
            print(f"Processed {lesson_id}: {len(result['changes_summary'])} changes")
    
    # Save updated course.json if not dry run
    if not dry_run:
        with open("src/content/course.json", 'w') as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)
        print("\n✅ Applied all changes to src/content/course.json")
    
    # Create output report
    output = {
        "generated": datetime.now().isoformat(),
        "dry_run": dry_run,
        "total_lessons": len(all_results),
        "lessons_with_changes": sum(1 for r in all_results if r["changes_summary"]),
        "results": all_results
    }
    
    # Write to file
    output_path = f"audits/fix_pass_{'dry_run' if dry_run else 'applied'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'Dry run' if dry_run else 'Fix'} complete. Results written to: {output_path}")
    
    # Summary statistics
    total_changes = sum(len(r["changes_summary"]) for r in all_results)
    manual_review = sum(1 for r in all_results if "Manual Review Required" in str(r["changes_summary"]))
    
    print(f"\nSummary:")
    print(f"- Total lessons processed: {len(all_results)}")
    print(f"- Lessons with changes: {output['lessons_with_changes']}")
    print(f"- Total changes made: {total_changes}")
    print(f"- Lessons needing manual review: {manual_review}")
    
    return output

if __name__ == "__main__":
    import sys
    # Check for --apply flag to run actual fix
    if "--apply" in sys.argv:
        print("🚀 Running ACTUAL FIX (not a dry run)...")
        main(dry_run=False)
    else:
        print("🔍 Running DRY RUN (use --apply to make actual changes)...")
        main(dry_run=True)