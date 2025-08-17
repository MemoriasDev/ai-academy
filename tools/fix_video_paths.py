#!/usr/bin/env python3
"""
Fix video paths in course.json by removing the cohort_2/ prefix
since videos are stored directly in the bucket root
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

def fix_video_paths():
    # Paths
    course_file = Path('/Users/bda/module-mind/module-mind/src/content/course.json')
    
    # Create backup
    backup_file = course_file.parent / f'course_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    shutil.copy2(course_file, backup_file)
    print(f"Created backup: {backup_file}")
    
    # Load course data
    with open(course_file, 'r') as f:
        course_data = json.load(f)
    
    # Track changes
    changes_made = 0
    
    # Fix videoPath in all lessons
    for week in course_data.get('weeks', []):
        for lesson in week.get('lessons', []):
            if 'videoPath' in lesson:
                old_path = lesson['videoPath']
                # Remove cohort_2/ prefix if present
                if old_path.startswith('cohort_2/'):
                    new_path = old_path.replace('cohort_2/', '')
                    lesson['videoPath'] = new_path
                    changes_made += 1
                    print(f"Updated: {old_path} -> {new_path}")
    
    # Save updated course data
    with open(course_file, 'w') as f:
        json.dump(course_data, f, indent=2)
    
    print(f"\n✅ Fixed {changes_made} video paths")
    print(f"Backup saved as: {backup_file}")
    return changes_made

if __name__ == '__main__':
    fix_video_paths()