#!/usr/bin/env python3
"""Apply Week 6 timestamp proposals to course.json"""

import json
import sys
from pathlib import Path
from datetime import datetime
import shutil

def apply_week6_timestamps(course_path, proposal_path, dry_run=False):
    """Apply the proposed timestamps to Week 6 lessons"""
    
    # Load the course data
    with open(course_path, 'r') as f:
        course_data = json.load(f)
    
    # Load the proposals
    with open(proposal_path, 'r') as f:
        proposals = json.load(f)
    
    # Create backup if not dry run
    if not dry_run:
        backup_path = course_path.replace('.json', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        shutil.copy2(course_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    changes_made = []
    
    # Process each week
    for week in course_data['weeks']:
        if week['id'] != 'week-6':
            continue
            
        for lesson in week['lessons']:
            lesson_id = lesson['id']
            
            # Check if we have a proposal for this lesson
            if lesson_id not in proposals:
                continue
            
            proposal = proposals[lesson_id]
            
            # Convert proposed timestamps to the course.json format
            new_timestamps = []
            for ts in proposal['proposed_timestamps']:
                new_timestamps.append({
                    "time": ts['time'],
                    "label": ts['label'],
                    "description": ts['description']
                })
            
            # Record the change
            old_count = len(lesson.get('timestamps', []))
            new_count = len(new_timestamps)
            
            changes_made.append({
                'lesson': f"{week['id']}/{lesson_id}",
                'title': lesson['title'],
                'old_timestamp_count': old_count,
                'new_timestamp_count': new_count
            })
            
            # Apply the change
            if not dry_run:
                lesson['timestamps'] = new_timestamps
                print(f"Updated {lesson_id}: {old_count} → {new_count} timestamps")
            else:
                print(f"[DRY RUN] Would update {lesson_id}: {old_count} → {new_count} timestamps")
    
    # Save the updated course data if not dry run
    if not dry_run:
        with open(course_path, 'w') as f:
            json.dump(course_data, f, indent=2)
        print(f"\nSuccessfully updated {course_path}")
    
    return changes_made

def main():
    """Main function"""
    # Check for dry run flag
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    course_path = 'src/content/course.json'
    proposal_path = 'week6_timestamps_proposal.json'
    
    # Check files exist
    if not Path(course_path).exists():
        print(f"Error: Course file not found: {course_path}")
        sys.exit(1)
    
    if not Path(proposal_path).exists():
        print(f"Error: Proposal file not found: {proposal_path}")
        sys.exit(1)
    
    # Apply the changes
    print(f"{'[DRY RUN] ' if dry_run else ''}Applying Week 6 timestamp proposals...")
    print(f"Course file: {course_path}")
    print(f"Proposal file: {proposal_path}")
    print()
    
    changes = apply_week6_timestamps(course_path, proposal_path, dry_run)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for change in changes:
        print(f"{change['lesson']}: {change['title']}")
        print(f"  Timestamps: {change['old_timestamp_count']} → {change['new_timestamp_count']}")
    
    if dry_run:
        print("\n[DRY RUN] No changes were made. Remove --dry-run to apply changes.")
    else:
        print(f"\n✓ Successfully updated {len(changes)} lessons")

if __name__ == "__main__":
    main()