#!/usr/bin/env python3
"""
Fix Pass Script - Normalize times, de-densify, and rewrite weak summaries
"""
import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple

# Configuration
COURSE_JSON_PATH = "src/content/course.json"
BACKUPS_DIR = "src/content/.backups"
MIN_SEP_S = 8
LABEL_WORDS_MIN = 2
LABEL_WORDS_MAX = 5
DESC_WORDS_MIN = 5
DESC_WORDS_MAX = 15

# Patterns
TIME_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)(?:\s+\(.+\))?$")
DURATION_CLEAN_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)$")
GENERIC_LABELS = {"overview", "discussion", "recap", "intro", "general", "introduction", "review"}

def normalize_time(time_str: str) -> Tuple[str, bool]:
    """
    Normalize time to H:MM:SS format.
    Returns (normalized_time, was_changed)
    """
    # Remove any trailing text first
    clean = time_str.strip().split('(')[0].strip()
    
    # Parse the time
    match = DURATION_CLEAN_RE.match(clean)
    if not match:
        # Try to extract just numbers
        parts = clean.split(':')
        if len(parts) == 2:
            try:
                minutes = int(parts[0])
                seconds = int(parts[1])
                hours = minutes // 60
                minutes = minutes % 60
                normalized = f"{hours}:{minutes:02d}:{seconds:02d}"
                return normalized, True
            except ValueError:
                return time_str, False
        return time_str, False
    
    h = int(match.group(1) or 0)
    m = int(match.group(2))
    s = int(match.group(3))
    
    # Handle minutes >= 60
    if m >= 60:
        h += m // 60
        m = m % 60
    
    normalized = f"{h}:{m:02d}:{s:02d}"
    return normalized, normalized != clean

def to_seconds(time_str: str) -> Optional[int]:
    """Convert H:MM:SS to seconds."""
    normalized, _ = normalize_time(time_str)
    parts = normalized.split(':')
    if len(parts) == 3:
        try:
            h, m, s = map(int, parts)
            return h * 3600 + m * 60 + s
        except ValueError:
            return None
    return None

def extract_words(text: str) -> List[str]:
    """Extract words from text."""
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def word_count(text: str) -> int:
    """Count words in text."""
    return len(extract_words(text))

def is_weak_label(label: str) -> bool:
    """Check if label is weak/generic."""
    if not label:
        return True
    wc = word_count(label)
    if wc < LABEL_WORDS_MIN or wc > LABEL_WORDS_MAX:
        return True
    words = set(extract_words(label))
    # Too generic if only generic words
    if words.issubset(GENERIC_LABELS):
        return True
    return False

def is_weak_description(desc: str, label: str) -> bool:
    """Check if description is weak."""
    if not desc:
        return True
    wc = word_count(desc)
    if wc < DESC_WORDS_MIN or wc > DESC_WORDS_MAX:
        return True
    # Check for too much repetition
    label_words = set(extract_words(label))
    desc_words = set(extract_words(desc))
    if label_words and desc_words:
        overlap = len(label_words & desc_words) / len(desc_words)
        if overlap > 0.7:
            return True
    return False

def rewrite_label(old_label: str, context: str) -> str:
    """
    Rewrite a weak label based on context.
    This is a simple heuristic - in production, use AI.
    """
    # Extract key technical terms from context
    words = extract_words(context.lower())
    
    # Look for specific patterns
    if any(w in words for w in ['configure', 'config', 'setup', 'setting']):
        if 'database' in words or 'pinecone' in words:
            return "Configure Database"
        elif 'api' in words:
            return "API Setup"
        elif 'environment' in words or 'env' in words:
            return "Environment Setup"
    
    if any(w in words for w in ['implement', 'build', 'create']):
        if 'function' in words:
            return "Implement Function"
        elif 'class' in words:
            return "Build Class"
        elif 'pipeline' in words:
            return "Create Pipeline"
    
    if 'test' in words or 'testing' in words:
        return "Testing Process"
    
    if 'deploy' in words or 'deployment' in words:
        return "Deployment Steps"
    
    # Fallback: try to extract most meaningful 2-3 words
    tech_terms = [w for w in words if len(w) > 4 and w not in GENERIC_LABELS]
    if len(tech_terms) >= 2:
        return ' '.join(tech_terms[:3]).title()
    
    # Last resort
    return "Key Concepts"

def rewrite_description(old_desc: str, label: str, context: str) -> str:
    """
    Rewrite a weak description based on label and context.
    This is a simple heuristic - in production, use AI.
    """
    words = extract_words(context.lower())
    
    # Generate based on label
    label_lower = label.lower()
    
    if 'setup' in label_lower or 'configure' in label_lower:
        return "Set up required components and configuration parameters"
    
    if 'implement' in label_lower or 'build' in label_lower:
        return "Build core functionality with error handling"
    
    if 'test' in label_lower:
        return "Validate implementation with comprehensive test cases"
    
    if 'deploy' in label_lower:
        return "Deploy to production environment with monitoring"
    
    # Look for action words in context
    action_words = ['create', 'build', 'implement', 'configure', 'set', 'deploy', 'test', 'validate']
    found_actions = [w for w in action_words if w in words]
    
    if found_actions:
        return f"Learn to {found_actions[0]} and apply best practices"
    
    # Fallback
    return "Understand key concepts and practical applications"

def process_lesson(lesson: Dict[str, Any], dry_run: bool = True) -> Dict[str, Any]:
    """Process a single lesson."""
    result = {
        "lesson_id": lesson.get("id", ""),
        "duration_changed": False,
        "normalized_times": [],
        "removed_dense_pairs": [],
        "rewritten": [],
        "notes": []
    }
    
    # 1. Normalize duration
    duration = lesson.get("duration", "")
    if duration:
        normalized_duration, changed = normalize_time(duration)
        if changed:
            result["duration_changed"] = True
            result["normalized_times"].append(f"{duration} -> {normalized_duration}")
            if not dry_run:
                lesson["duration"] = normalized_duration
    
    # 2. Process timestamps
    timestamps = lesson.get("timestamps", [])
    content = lesson.get("content", "")
    
    # Normalize timestamp times
    for ts in timestamps:
        time_str = ts.get("time", "")
        normalized_time, changed = normalize_time(time_str)
        if changed:
            result["normalized_times"].append(f"{time_str} -> {normalized_time}")
            if not dry_run:
                ts["time"] = normalized_time
    
    # 3. De-densify timestamps
    if len(timestamps) > 1:
        times_with_index = []
        for i, ts in enumerate(timestamps):
            time_s = to_seconds(ts.get("time", ""))
            if time_s is not None:
                times_with_index.append((time_s, i, ts))
        
        # Sort by time
        times_with_index.sort(key=lambda x: x[0])
        
        # Find dense pairs
        to_remove = set()
        for i in range(1, len(times_with_index)):
            prev_s, prev_idx, prev_ts = times_with_index[i-1]
            curr_s, curr_idx, curr_ts = times_with_index[i]
            
            if prev_idx not in to_remove and (curr_s - prev_s) < MIN_SEP_S:
                # Decide which to keep
                prev_desc = prev_ts.get("description", "")
                curr_desc = curr_ts.get("description", "")
                
                # Keep the one with longer description, or earlier if equal
                if len(curr_desc) > len(prev_desc):
                    to_remove.add(prev_idx)
                    result["removed_dense_pairs"].append(
                        f"{prev_ts.get('time', '')}→{curr_ts.get('time', '')}"
                    )
                else:
                    to_remove.add(curr_idx)
                    result["removed_dense_pairs"].append(
                        f"{prev_ts.get('time', '')}→{curr_ts.get('time', '')}"
                    )
        
        # Remove dense timestamps
        if to_remove and not dry_run:
            lesson["timestamps"] = [
                ts for i, ts in enumerate(timestamps) if i not in to_remove
            ]
            timestamps = lesson["timestamps"]
    
    # 4. Rewrite weak summaries
    for ts in timestamps:
        time_str = ts.get("time", "")
        label = ts.get("label", "")
        desc = ts.get("description", "")
        
        changes = {}
        
        if is_weak_label(label):
            new_label = rewrite_label(label, content[:500])  # Use first 500 chars as context
            changes["old_label"] = label
            changes["new_label"] = new_label
            if not dry_run:
                ts["label"] = new_label
        
        if is_weak_description(desc, label):
            new_desc = rewrite_description(desc, label, content[:500])
            # Ensure it meets word count
            if word_count(new_desc) > DESC_WORDS_MAX:
                words = new_desc.split()[:DESC_WORDS_MAX]
                new_desc = ' '.join(words)
            changes["old_desc"] = desc
            changes["new_desc"] = new_desc
            if not dry_run:
                ts["description"] = new_desc
        
        if changes:
            changes["time"] = time_str
            result["rewritten"].append(changes)
    
    return result

def create_backup(course_path: str, backups_dir: str) -> str:
    """Create timestamped backup."""
    Path(backups_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backups_dir, f"course_backup_{timestamp}.json")
    shutil.copy2(course_path, backup_path)
    return backup_path

def write_logs(results: Dict[str, Any], log_path: Optional[str], ndjson_path: Optional[str], dry_run: bool):
    """Write markdown and NDJSON logs."""
    if log_path:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'w') as f:
            f.write(f"# Fix Pass ({'dry run' if dry_run else 'executed'})\n")
            f.write(f"- Course: {COURSE_JSON_PATH}\n")
            f.write(f"- min_sep_s: {MIN_SEP_S} | label {LABEL_WORDS_MIN}–{LABEL_WORDS_MAX} words | desc {DESC_WORDS_MIN}–{DESC_WORDS_MAX} words\n")
            f.write(f"- Generated: {datetime.now().isoformat()}Z\n\n")
            
            for lesson in results["lessons"]:
                if any([lesson["duration_changed"], lesson["normalized_times"], 
                       lesson["removed_dense_pairs"], lesson["rewritten"]]):
                    f.write(f"## {lesson['lesson_id']}\n")
                    
                    if lesson["duration_changed"]:
                        for norm in lesson["normalized_times"]:
                            if "duration" in norm.lower() or "->" in norm:
                                f.write(f"- Duration normalized: {norm}\n")
                    
                    if lesson["removed_dense_pairs"]:
                        for pair in lesson["removed_dense_pairs"]:
                            f.write(f"- De-densified: removed {pair}\n")
                    
                    if lesson["rewritten"]:
                        f.write("- Rewrites:\n")
                        for rw in lesson["rewritten"]:
                            f.write(f"  - {rw['time']}\n")
                            if "new_label" in rw:
                                f.write(f"    - Label: \"{rw.get('old_label', '')}\" -> \"{rw['new_label']}\"\n")
                            if "new_desc" in rw:
                                f.write(f"    - Desc: \"{rw.get('old_desc', '')}\" -> \"{rw['new_desc']}\"\n")
                    f.write("\n")
    
    if ndjson_path:
        Path(ndjson_path).parent.mkdir(parents=True, exist_ok=True)
        with open(ndjson_path, 'w') as f:
            # Summary line
            f.write(json.dumps({
                "type": "summary",
                "timestamp": datetime.now().isoformat(),
                "dry_run": dry_run,
                "stats": results["summary"]
            }) + "\n")
            
            # Detail lines
            for lesson in results["lessons"]:
                if lesson["normalized_times"]:
                    f.write(json.dumps({
                        "type": "normalization",
                        "lesson_id": lesson["lesson_id"],
                        "changes": lesson["normalized_times"]
                    }) + "\n")
                
                if lesson["removed_dense_pairs"]:
                    f.write(json.dumps({
                        "type": "de-densification",
                        "lesson_id": lesson["lesson_id"],
                        "removed": lesson["removed_dense_pairs"]
                    }) + "\n")
                
                if lesson["rewritten"]:
                    f.write(json.dumps({
                        "type": "rewrite",
                        "lesson_id": lesson["lesson_id"],
                        "changes": lesson["rewritten"]
                    }) + "\n")

def main(
    course_json_path: str = COURSE_JSON_PATH,
    backups_dir: str = BACKUPS_DIR,
    selection: Optional[List[str]] = None,
    min_sep_s: int = MIN_SEP_S,
    dry_run: bool = True,
    log_path: Optional[str] = None,
    ndjson_path: Optional[str] = None,
    commit: bool = False,
    git_user_name: Optional[str] = None,
    git_user_email: Optional[str] = None
):
    """Main fix function."""
    # Load course
    with open(course_json_path, 'r') as f:
        course_data = json.load(f)
    
    # Initialize results
    results = {
        "status": "ok",
        "config": {
            "course_json_path": course_json_path,
            "min_sep_s": min_sep_s,
            "label_words": [LABEL_WORDS_MIN, LABEL_WORDS_MAX],
            "desc_words": [DESC_WORDS_MIN, DESC_WORDS_MAX],
            "dry_run": dry_run
        },
        "summary": {
            "weeks": 0,
            "lessons_considered": 0,
            "lessons_updated": 0,
            "durations_normalized": 0,
            "timestamps_normalized": 0,
            "timestamps_removed_for_density": 0,
            "summaries_rewritten": 0
        },
        "lessons": [],
        "backup_path": None,
        "commit": {
            "attempted": False,
            "executed": False,
            "message": None,
            "git_stdout": None,
            "git_stderr": None
        }
    }
    
    # Create backup if not dry run
    if not dry_run:
        results["backup_path"] = create_backup(course_json_path, backups_dir)
    
    # Process lessons
    weeks = course_data.get("weeks", [])
    results["summary"]["weeks"] = len(weeks)
    
    for week in weeks:
        week_id = week.get("id", "")
        lessons = week.get("lessons", [])
        
        for lesson in lessons:
            lesson_id = lesson.get("id", "")
            
            # Skip if selection specified and not included
            if selection and lesson_id not in selection:
                continue
            
            results["summary"]["lessons_considered"] += 1
            
            # Process the lesson
            lesson_result = process_lesson(lesson, dry_run)
            lesson_result["week_id"] = week_id
            
            # Update counters
            if lesson_result["duration_changed"]:
                results["summary"]["durations_normalized"] += 1
            
            if lesson_result["normalized_times"]:
                results["summary"]["timestamps_normalized"] += len(lesson_result["normalized_times"])
                if lesson_result["duration_changed"]:
                    results["summary"]["timestamps_normalized"] -= 1  # Don't double count duration
            
            if lesson_result["removed_dense_pairs"]:
                results["summary"]["timestamps_removed_for_density"] += len(lesson_result["removed_dense_pairs"])
            
            if lesson_result["rewritten"]:
                results["summary"]["summaries_rewritten"] += len(lesson_result["rewritten"])
            
            if any([lesson_result["duration_changed"], lesson_result["normalized_times"],
                   lesson_result["removed_dense_pairs"], lesson_result["rewritten"]]):
                results["summary"]["lessons_updated"] += 1
            
            results["lessons"].append(lesson_result)
    
    # Write course file if not dry run
    if not dry_run:
        with open(course_json_path, 'w') as f:
            json.dump(course_data, f, indent=2, ensure_ascii=False)
    
    # Write logs
    write_logs(results, log_path, ndjson_path, dry_run)
    
    # Git commit if requested and not dry run
    if commit and not dry_run:
        results["commit"]["attempted"] = True
        # Git operations would go here
        # For now, just note it wasn't executed
        results["commit"]["message"] = "chore(course): normalize durations, de-densify, rewrite weak summaries"
    
    return results

if __name__ == "__main__":
    # Run with provided parameters
    result = main(
        course_json_path="src/content/course.json",
        backups_dir="src/content/.backups",
        selection=None,  # Process all lessons
        min_sep_s=8,
        dry_run=True,  # DRY RUN FIRST
        log_path="audits/fix_pass_2025-08-15.md",
        ndjson_path="audits/fix_pass_2025-08-15.ndjson",
        commit=False
    )
    
    print(json.dumps(result, indent=2))