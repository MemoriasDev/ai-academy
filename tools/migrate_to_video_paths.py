#!/usr/bin/env python3
"""Migrate course.json from videoUrl to videoPath format for Supabase storage"""

import json
import os
from datetime import datetime
from pathlib import Path

def convert_url_to_path(video_url: str) -> str:
    """
    Convert local video URL to Supabase storage path
    
    From: /videos/cohort_2/week_01/week_1_class_1_2024-05-20.mp4
    To:   cohort_2/week_1_class_1_2024-05-20.mp4
    """
    if not video_url:
        return ""
    
    # Extract filename
    filename = os.path.basename(video_url)
    
    # Determine cohort from path
    if 'cohort_2' in video_url:
        return f"cohort_2/{filename}"
    elif 'cohort_3' in video_url:
        return f"cohort_3/{filename}"
    else:
        # Default to cohort_2 for any unspecified videos
        return f"cohort_2/{filename}"

def migrate_course_json(course_path: str, dry_run: bool = False):
    """Add videoPath field to all lessons while keeping videoUrl for backwards compatibility"""
    
    # Load course data
    with open(course_path, 'r') as f:
        course_data = json.load(f)
    
    # Track changes
    changes = []
    
    # Process each lesson
    for week in course_data['weeks']:
        for lesson in week['lessons']:
            video_url = lesson.get('videoUrl', '')
            
            if video_url:
                # Generate the storage path
                video_path = convert_url_to_path(video_url)
                
                if not dry_run:
                    # Add videoPath field
                    lesson['videoPath'] = video_path
                    # Keep videoUrl for backwards compatibility during migration
                    # Can be removed once frontend is fully updated
                
                changes.append({
                    'week': week['id'],
                    'lesson': lesson['id'],
                    'title': lesson['title'],
                    'videoUrl': video_url,
                    'videoPath': video_path
                })
    
    if not dry_run:
        # Create backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = course_path.replace('.json', f'_backup_migration_{timestamp}.json')
        
        with open(course_path, 'r') as f:
            backup_data = json.load(f)
        
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✓ Created backup: {backup_path}")
        
        # Save updated file
        with open(course_path, 'w') as f:
            json.dump(course_data, f, indent=2)
        
        print(f"✓ Updated {course_path}")
    
    return changes

def main():
    """Main migration process"""
    
    COURSE_JSON = "src/content/course.json"
    
    # Check if file exists
    if not os.path.exists(COURSE_JSON):
        print(f"Error: {COURSE_JSON} not found")
        return
    
    print("="*60)
    print("COURSE.JSON MIGRATION")
    print("="*60)
    print("\nThis will add videoPath fields for Supabase storage")
    print("while keeping videoUrl for backwards compatibility.\n")
    
    # Dry run first
    print("Performing dry run...")
    changes = migrate_course_json(COURSE_JSON, dry_run=True)
    
    print(f"\nFound {len(changes)} videos to migrate:\n")
    
    # Show first few examples
    for change in changes[:3]:
        print(f"  {change['week']}/{change['lesson']}: {change['title']}")
        print(f"    From: {change['videoUrl']}")
        print(f"    To:   {change['videoPath']}")
        print()
    
    if len(changes) > 3:
        print(f"  ... and {len(changes) - 3} more videos\n")
    
    # Ask for confirmation
    response = input("Proceed with migration? (yes/no): ")
    
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return
    
    # Perform actual migration
    print("\nMigrating...")
    changes = migrate_course_json(COURSE_JSON, dry_run=False)
    
    print(f"\n✓ Successfully migrated {len(changes)} videos")
    print("\nNext steps:")
    print("1. Upload videos to Supabase using upload_videos_authenticated.py")
    print("2. Update video player components to use videoPath with SecureVideoPlayer")
    print("3. Test authentication and video playback")
    print("4. Once confirmed working, videoUrl fields can be removed")

if __name__ == "__main__":
    main()