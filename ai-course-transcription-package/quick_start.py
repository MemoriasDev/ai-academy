#!/usr/bin/env python3
"""
Quick start script for cohort video processing.
Handles setup, validation, and execution with minimal user input.
"""

import os
import sys
import json
from pathlib import Path
import subprocess
import logging

def setup_logging():
    """Setup basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def check_environment():
    """Check if environment is properly set up."""
    logger = logging.getLogger(__name__)
    
    # Check if we're in the right directory
    if not Path("scripts").exists() or not Path("cohorts").exists():
        logger.error("❌ Please run this script from the transcription directory")
        logger.info("Expected structure:")
        logger.info("  transcription/")
        logger.info("    ├── scripts/")
        logger.info("    ├── cohorts/")
        logger.info("    └── quick_start.py")
        return False
    
    # Check Python environment
    try:
        import faster_whisper
        logger.info("✅ faster-whisper is available")
    except ImportError:
        logger.error("❌ faster-whisper not installed")
        logger.info("Run: pip install faster-whisper")
        return False
    
    return True

def discover_videos():
    """Discover video files in cohorts directory."""
    logger = logging.getLogger(__name__)
    
    cohorts_path = Path("cohorts")
    video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv'}
    
    videos_by_cohort = {}
    total_videos = 0
    
    for cohort_dir in cohorts_path.iterdir():
        if cohort_dir.is_dir() and cohort_dir.name.startswith('cohort_'):
            videos = []
            
            for week_dir in cohort_dir.iterdir():
                if week_dir.is_dir():
                    for file_path in week_dir.iterdir():
                        if file_path.suffix.lower() in video_extensions:
                            videos.append(file_path)
            
            if videos:
                videos_by_cohort[cohort_dir.name] = videos
                total_videos += len(videos)
    
    logger.info(f"📁 Found videos in {len(videos_by_cohort)} cohorts:")
    for cohort, videos in videos_by_cohort.items():
        logger.info(f"  {cohort}: {len(videos)} videos")
    
    logger.info(f"🎬 Total: {total_videos} videos")
    
    return videos_by_cohort, total_videos

def estimate_processing_time(total_videos):
    """Estimate processing time based on video count."""
    logger = logging.getLogger(__name__)
    
    # Rough estimates based on 1-hour videos
    transcription_time_per_video = 10  # minutes (with 6 workers)
    analysis_time_per_video = 2       # minutes (with 8 workers)
    
    total_transcription_time = (total_videos * transcription_time_per_video) // 6  # Parallel processing
    total_analysis_time = (total_videos * analysis_time_per_video) // 8
    
    total_time_minutes = total_transcription_time + total_analysis_time
    hours = total_time_minutes // 60
    minutes = total_time_minutes % 60
    
    logger.info(f"⏱️ Estimated processing time: {hours}h {minutes}m")
    logger.info(f"  📝 Transcription: ~{total_transcription_time}m")
    logger.info(f"  🧠 Analysis: ~{total_analysis_time}m")
    
    return total_time_minutes

def check_storage_space(total_videos):
    """Check available storage space."""
    logger = logging.getLogger(__name__)
    
    # Estimate storage needs
    estimated_transcript_size = total_videos * 5  # MB per transcript
    estimated_analysis_size = total_videos * 2   # MB per analysis
    total_needed_mb = estimated_transcript_size + estimated_analysis_size
    
    # Check available space
    stat = os.statvfs('.')
    available_mb = (stat.f_bavail * stat.f_frsize) // (1024 * 1024)
    
    logger.info(f"💾 Storage requirements:")
    logger.info(f"  Estimated needed: {total_needed_mb} MB")
    logger.info(f"  Available: {available_mb} MB")
    
    if available_mb < total_needed_mb * 1.5:  # 50% buffer
        logger.warning(f"⚠️ Low disk space! Consider freeing up space.")
        return False
    
    logger.info("✅ Sufficient storage available")
    return True

def run_processing(mode="full"):
    """Run the processing workflow."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Starting {mode} processing...")
    
    # Change to scripts directory
    os.chdir("scripts")
    
    # Choose command based on mode
    if mode == "transcribe":
        cmd = [sys.executable, "simplified_orchestrator.py", "--transcribe-only"]
    elif mode == "analyze":
        cmd = [sys.executable, "simplified_orchestrator.py", "--analyze-only"]
    elif mode == "dry-run":
        cmd = [sys.executable, "simplified_orchestrator.py", "--dry-run"]
    else:
        cmd = [sys.executable, "simplified_orchestrator.py"]
    
    try:
        # Run the workflow
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        # Change back to parent directory
        os.chdir("..")
        
        if result.returncode == 0:
            logger.info("🎉 Processing completed successfully!")
            return True
        else:
            logger.error(f"❌ Processing failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running processing: {e}")
        os.chdir("..")  # Ensure we're back in the right directory
        return False

def main():
    """Main quick start flow."""
    logger = setup_logging()
    
    print("🎬 Cohort Video Processing - Quick Start")
    print("=" * 50)
    
    # Step 1: Environment check
    logger.info("Step 1: Checking environment...")
    if not check_environment():
        return False
    
    # Step 2: Video discovery
    logger.info("\nStep 2: Discovering videos...")
    videos_by_cohort, total_videos = discover_videos()
    
    if total_videos == 0:
        logger.error("❌ No videos found!")
        logger.info("📁 Please place your video files in the cohorts structure:")
        logger.info("  cohorts/cohort_2/week_01/class1.mp4")
        logger.info("  cohorts/cohort_2/week_01/class2.mp4")
        logger.info("  etc.")
        return False
    
    # Step 3: Time and storage estimates
    logger.info("\nStep 3: Calculating requirements...")
    estimate_processing_time(total_videos)
    if not check_storage_space(total_videos):
        logger.warning("Consider freeing up disk space before continuing.")
    
    # Step 4: User confirmation
    print(f"\n🎯 Ready to process {total_videos} videos across {len(videos_by_cohort)} cohorts")
    
    while True:
        choice = input("\nChoose processing mode:\n"
                      "1. Full workflow (transcribe + analyze)\n"
                      "2. Transcription only\n"
                      "3. Analysis only (requires existing transcripts)\n"
                      "4. Dry run (discovery only)\n"
                      "5. Exit\n"
                      "Enter choice (1-5): ").strip()
        
        if choice == "1":
            return run_processing("full")
        elif choice == "2":
            return run_processing("transcribe")
        elif choice == "3":
            return run_processing("analyze")
        elif choice == "4":
            return run_processing("dry-run")
        elif choice == "5":
            logger.info("👋 Goodbye!")
            return True
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
