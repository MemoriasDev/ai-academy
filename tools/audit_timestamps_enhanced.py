#!/usr/bin/env python3
"""
Enhanced Course Timestamp Audit Script
Generates JSON report, Markdown log, and NDJSON log
"""
import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path

# Configuration
COURSE_JSON_PATH = "src/content/course.json"
MAX_GAP_S = 900  # 15 minutes
MIN_SEP_S = 8    # seconds
LOG_PATH = "audits/course_timestamp_audit.md"
NDJSON_PATH = "audits/course_timestamp_audit.ndjson"

# Patterns
TIME_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)(?:\s+\(.+\))?$")
DURATION_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)$")  # Strict H:MM:SS
GENERIC_LABELS = {"overview", "discussion", "recap", "intro", "general", "introduction", "review"}

def to_seconds(time_str: str) -> Optional[int]:
    """Convert H:MM:SS or MM:SS to seconds."""
    match = TIME_RE.match(time_str.strip())
    if not match:
        return None
    h = int(match.group(1) or 0)
    m = int(match.group(2))
    s = int(match.group(3))
    return h * 3600 + m * 60 + s

def is_clean_duration(duration_str: str) -> bool:
    """Check if duration is clean H:MM:SS format without extra text."""
    return bool(DURATION_RE.match(duration_str.strip()))

def extract_words(text: str) -> List[str]:
    """Extract words from text."""
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

def word_count(text: str) -> int:
    """Count words in text."""
    return len(extract_words(text))

def check_label_quality(label: str) -> bool:
    """Check if label meets quality standards."""
    if not label:
        return False
    wc = word_count(label)
    if wc < 2 or wc > 5:
        return False
    words = set(extract_words(label))
    # Allow generic terms only if accompanied by specific terms
    if len(words) == 1 and words.issubset(GENERIC_LABELS):
        return False
    return True

def check_description_quality(desc: str, label: str) -> bool:
    """Check if description meets quality standards."""
    if not desc:
        return False
    wc = word_count(desc)
    if wc < 5 or wc > 15:
        return False
    # Check for repetition
    label_words = set(extract_words(label))
    desc_words = set(extract_words(desc))
    if label_words and desc_words:
        overlap = len(label_words & desc_words) / len(desc_words)
        if overlap > 0.7:  # Too much repetition
            return False
    return True

def audit_lesson(lesson: Dict[str, Any]) -> Dict[str, Any]:
    """Audit a single lesson."""
    lesson_id = lesson.get("id", "")
    title = lesson.get("title", "")
    duration_str = lesson.get("duration", "")
    timestamps = lesson.get("timestamps", [])
    
    # Duration check
    duration_ok = is_clean_duration(duration_str)
    duration_s = to_seconds(duration_str) if duration_ok else None
    
    # Initialize issue trackers
    issues = {
        "format": [],
        "out_of_range": [],
        "non_monotonic": [],
        "density": [],
        "coverage_gaps": []
    }
    
    summary_issues = {
        "vague_labels": [],
        "weak_descriptions": []
    }
    
    # Process timestamps
    times_s = []
    for i, ts in enumerate(timestamps):
        time_str = ts.get("time", "")
        time_s = to_seconds(time_str)
        
        if time_s is None:
            issues["format"].append(time_str)
            continue
            
        times_s.append((time_s, time_str, ts))
        
        # Range check
        if duration_s and (time_s < 0 or time_s > duration_s):
            issues["out_of_range"].append(time_str)
        
        # Label and description quality
        label = ts.get("label", "")
        desc = ts.get("description", "")
        
        if not check_label_quality(label):
            summary_issues["vague_labels"].append(time_str)
        
        if not check_description_quality(desc, label):
            summary_issues["weak_descriptions"].append(time_str)
    
    # Order check
    for i in range(1, len(times_s)):
        if times_s[i][0] < times_s[i-1][0]:
            issues["non_monotonic"].append(times_s[i][1])
    
    # Density check
    for i in range(1, len(times_s)):
        gap = times_s[i][0] - times_s[i-1][0]
        if gap < MIN_SEP_S:
            issues["density"].append(f"{times_s[i-1][1]}→{times_s[i][1]}")
    
    # Coverage check
    if len(times_s) > 1:
        for i in range(1, len(times_s)):
            gap = times_s[i][0] - times_s[i-1][0]
            if gap > MAX_GAP_S:
                issues["coverage_gaps"].append({
                    "start": times_s[i-1][1],
                    "end": times_s[i][1],
                    "length_s": gap
                })
    
    # Determine acceptance
    timestamps_pass = (
        duration_ok and
        len(issues["format"]) == 0 and
        len(issues["out_of_range"]) == 0 and
        len(issues["non_monotonic"]) == 0 and
        len(issues["density"]) == 0 and
        len(issues["coverage_gaps"]) == 0
    )
    
    summaries_pass = (
        len(summary_issues["vague_labels"]) == 0 and
        len(summary_issues["weak_descriptions"]) == 0
    )
    
    # Determine actions
    actions = []
    if not duration_ok:
        actions.append("fix_duration")
    if issues["out_of_range"]:
        actions.append("fix_range")
    if issues["non_monotonic"]:
        actions.append("fix_order")
    if issues["coverage_gaps"]:
        actions.append("fix_coverage")
    if issues["density"]:
        actions.append("fix_density")
    if not summaries_pass:
        actions.append("rewrite_summaries")
    
    return {
        "lesson_id": lesson_id,
        "title": title,
        "duration_ok": duration_ok,
        "timestamp_issues": issues,
        "summary_issues": summary_issues,
        "acceptance": {
            "timestamps_pass": timestamps_pass,
            "summaries_pass": summaries_pass,
            "overall": "pass" if (timestamps_pass and summaries_pass) else "needs_fixes"
        },
        "actions": actions
    }

def write_markdown_log(report: Dict[str, Any], log_path: str):
    """Write human-readable markdown log."""
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(log_path, 'w') as f:
        f.write("# Course Timestamp Audit (read-only)\n")
        f.write(f"- Course: {COURSE_JSON_PATH}\n")
        f.write(f"- max_gap_s: {MAX_GAP_S} | min_sep_s: {MIN_SEP_S}\n")
        f.write(f"- Generated: {datetime.now().isoformat()}Z\n\n")
        
        f.write("## Summary\n")
        f.write(f"- Weeks: {report['summary']['weeks']}\n")
        f.write(f"- Lessons: {report['summary']['lessons']}\n")
        f.write(f"- Issues total: {report['summary']['issues_total']}\n\n")
        
        f.write("## Lessons\n")
        for lesson in report['lessons']:
            f.write(f"### {lesson['week_id']} / {lesson['lesson_id']} — {lesson['title']}\n")
            
            # Duration status
            duration_status = "OK" if lesson['duration_ok'] else "Needs fix"
            f.write(f"- Duration: {duration_status}\n")
            
            # Timestamp issues
            order_status = "OK" if not lesson['timestamp_issues']['non_monotonic'] else "Broken"
            coverage_status = "OK" if not lesson['timestamp_issues']['coverage_gaps'] else f"Gaps: {len(lesson['timestamp_issues']['coverage_gaps'])}"
            density_status = "OK" if not lesson['timestamp_issues']['density'] else f"Too dense ({len(lesson['timestamp_issues']['density'])})"
            f.write(f"- Order: {order_status} | Coverage: {coverage_status} | Density: {density_status}\n")
            
            # Summary quality
            label_quality = "OK" if not lesson['summary_issues']['vague_labels'] else "Weak"
            desc_quality = "OK" if not lesson['summary_issues']['weak_descriptions'] else "Weak"
            f.write(f"- Label Quality: {label_quality} | Description Quality: {desc_quality}\n")
            
            # Example problem
            example = ""
            if lesson['timestamp_issues']['format']:
                example = f"Bad format: {lesson['timestamp_issues']['format'][0]}"
            elif lesson['timestamp_issues']['out_of_range']:
                example = f"Out of range: {lesson['timestamp_issues']['out_of_range'][0]}"
            elif lesson['timestamp_issues']['non_monotonic']:
                example = f"Order broken: {lesson['timestamp_issues']['non_monotonic'][0]}"
            elif lesson['timestamp_issues']['density']:
                example = f"Too dense: {lesson['timestamp_issues']['density'][0]}"
            elif lesson['summary_issues']['vague_labels']:
                example = f"Vague label: {lesson['summary_issues']['vague_labels'][0]}"
            elif lesson['summary_issues']['weak_descriptions']:
                example = f"Weak description: {lesson['summary_issues']['weak_descriptions'][0]}"
            
            if example:
                f.write(f"- Example: {example}\n")
            
            if lesson['actions']:
                f.write(f"- Suggested actions: {', '.join(lesson['actions'])}\n")
            
            f.write("\n")

def write_ndjson_log(report: Dict[str, Any], ndjson_path: str):
    """Write NDJSON log for programmatic consumption."""
    Path(ndjson_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(ndjson_path, 'w') as f:
        # Write summary line
        f.write(json.dumps({
            "type": "summary",
            "timestamp": datetime.now().isoformat(),
            "config": {
                "course_json_path": COURSE_JSON_PATH,
                "max_gap_s": MAX_GAP_S,
                "min_sep_s": MIN_SEP_S
            },
            "summary": report['summary']
        }) + '\n')
        
        # Write lesson lines
        for lesson in report['lessons']:
            f.write(json.dumps({
                "type": "lesson",
                "week_id": lesson['week_id'],
                "lesson_id": lesson['lesson_id'],
                "title": lesson['title'],
                "acceptance": lesson['acceptance'],
                "issues": {
                    "timestamp": lesson['timestamp_issues'],
                    "summary": lesson['summary_issues']
                },
                "actions": lesson['actions']
            }) + '\n')

def main():
    """Main audit function."""
    # Load course data
    with open(COURSE_JSON_PATH, 'r') as f:
        course_data = json.load(f)
    
    # Initialize report
    report = {
        "status": "ok",
        "summary": {
            "weeks": 0,
            "lessons": 0,
            "issues_total": 0
        },
        "lessons": []
    }
    
    # Process each week and lesson
    weeks = course_data.get("weeks", [])
    report["summary"]["weeks"] = len(weeks)
    
    for week in weeks:
        week_id = week.get("id", "")
        lessons = week.get("lessons", [])
        
        for lesson in lessons:
            report["summary"]["lessons"] += 1
            
            # Audit the lesson
            audit_result = audit_lesson(lesson)
            audit_result["week_id"] = week_id
            
            # Track issues
            if audit_result["acceptance"]["overall"] != "pass":
                report["summary"]["issues_total"] += 1
            
            report["lessons"].append(audit_result)
    
    # Write logs
    write_markdown_log(report, LOG_PATH)
    write_ndjson_log(report, NDJSON_PATH)
    
    # Output JSON report to stdout
    print(json.dumps(report, indent=2))
    
    return report

if __name__ == "__main__":
    main()