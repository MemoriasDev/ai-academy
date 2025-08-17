#!/usr/bin/env python3
"""
Robust batch transcription runner with checkpointing, error recovery, and monitoring.
"""

import json
import sys
import os
import time
import traceback
from pathlib import Path
from datetime import datetime
import threading
import signal

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from s3_batch_transcriber import S3BatchTranscriber

class RobustBatchRunner:
    def __init__(self, manifest_path, checkpoint_path="logs/cohort3_checkpoint.json"):
        self.manifest_path = manifest_path
        self.checkpoint_path = checkpoint_path
        self.error_log_path = "logs/transcription_errors.json"
        self.status_log_path = "logs/transcription_status.json"
        
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Load manifest
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
        
        # Initialize transcriber
        self.transcriber = S3BatchTranscriber(
            model_size="base",
            device="cpu",
            max_workers=1  # Process sequentially for stability
        )
        
        # State tracking
        self.completed = set()
        self.failed = {}
        self.current_video = None
        self.start_time = time.time()
        self.stop_requested = False
        
        # Setup signal handler
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Load existing checkpoint
        self.load_checkpoint()
    
    def signal_handler(self, sig, frame):
        """Handle graceful shutdown."""
        print("\n\n⚠️  Stopping after current video completes...")
        print("   (Press Ctrl+C again to force stop)")
        self.stop_requested = True
        
        # Save checkpoint
        self.save_checkpoint()
        
        # Second Ctrl+C forces exit
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    def load_checkpoint(self):
        """Load existing checkpoint if available."""
        if os.path.exists(self.checkpoint_path):
            try:
                with open(self.checkpoint_path, 'r') as f:
                    checkpoint = json.load(f)
                    self.completed = set(checkpoint.get('completed', []))
                    self.failed = checkpoint.get('failed', {})
                    print(f"📂 Loaded checkpoint: {len(self.completed)} completed, {len(self.failed)} failed")
            except Exception as e:
                print(f"⚠️  Could not load checkpoint: {e}")
    
    def save_checkpoint(self):
        """Save current progress to checkpoint."""
        checkpoint = {
            'completed': list(self.completed),
            'failed': self.failed,
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(self.manifest['videos'])
        }
        
        try:
            with open(self.checkpoint_path, 'w') as f:
                json.dump(checkpoint, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save checkpoint: {e}")
    
    def save_error_log(self, video_id, error_details):
        """Save error details for debugging."""
        errors = {}
        if os.path.exists(self.error_log_path):
            try:
                with open(self.error_log_path, 'r') as f:
                    errors = json.load(f)
            except:
                pass
        
        errors[video_id] = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error_details),
            'traceback': traceback.format_exc()
        }
        
        with open(self.error_log_path, 'w') as f:
            json.dump(errors, f, indent=2)
    
    def update_status(self, current_video=None, phase="processing"):
        """Update status file for monitoring."""
        status = {
            'timestamp': datetime.now().isoformat(),
            'phase': phase,
            'current_video': current_video,
            'completed': len(self.completed),
            'failed': len(self.failed),
            'total': len(self.manifest['videos']),
            'progress_percent': (len(self.completed) / len(self.manifest['videos'])) * 100,
            'elapsed_seconds': time.time() - self.start_time
        }
        
        try:
            with open(self.status_log_path, 'w') as f:
                json.dump(status, f, indent=2)
        except:
            pass
    
    def check_existing_transcript(self, video):
        """Check if transcript already exists and is valid."""
        txt_path = Path(f"{video['output_path']}.txt")
        json_path = Path(f"{video['output_path']}.json")
        
        if txt_path.exists() and json_path.exists():
            # Check file sizes to ensure they're not empty
            if txt_path.stat().st_size > 100 and json_path.stat().st_size > 100:
                return True
        return False
    
    def process_video(self, video, retry_count=0):
        """Process a single video with error handling."""
        video_id = f"week_{video['week']}_class_{video['lesson']}"
        max_retries = 3
        
        try:
            # Check if already exists
            if self.check_existing_transcript(video):
                print(f"           ✅ Transcript already exists")
                return True
            
            # Update status
            self.current_video = video_id
            self.update_status(video_id, "downloading")
            
            # Process video
            result = self.transcriber.transcribe_from_url(
                video['url'],
                f"{video['output_path']}",
                metadata={
                    'cohort': video['cohort'],
                    'week': video['week'],
                    'lesson': video['lesson'],
                    'date': video['date']
                }
            )
            
            # Verify output was created
            if not self.check_existing_transcript(video):
                raise Exception("Transcript files were not created")
            
            print(f"           ✅ Completed in {result['processing_time']:.1f}s")
            print(f"           📝 {result['segments_count']} segments")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a recoverable error
            recoverable_errors = [
                "timed out",
                "connection",
                "temporary",
                "500",
                "502",
                "503",
                "504"
            ]
            
            is_recoverable = any(err in error_msg.lower() for err in recoverable_errors)
            
            if is_recoverable and retry_count < max_retries:
                wait_time = 30 * (retry_count + 1)  # Exponential backoff
                print(f"           ⚠️  Recoverable error: {error_msg}")
                print(f"           🔄 Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries})")
                time.sleep(wait_time)
                return self.process_video(video, retry_count + 1)
            else:
                print(f"           ❌ Failed after {retry_count + 1} attempts: {error_msg}")
                self.save_error_log(video_id, e)
                return False
    
    def run(self):
        """Main batch processing loop."""
        videos = self.manifest['videos']
        total = len(videos)
        
        print(f"\n📚 Processing {total} videos from Cohort 3")
        print(f"⏭️  Skipping {len(self.completed)} already completed")
        print(f"🔄 Retrying {len(self.failed)} previously failed")
        print("\n" + "=" * 70 + "\n")
        
        processed_count = 0
        failed_count = 0
        
        for i, video in enumerate(videos, 1):
            if self.stop_requested:
                print("\n⚠️  Batch processing stopped by user")
                break
            
            video_id = f"week_{video['week']}_class_{video['lesson']}"
            
            # Skip if already completed
            if video_id in self.completed:
                print(f"[{i}/{total}] ⏭️  Skipping {video_id} (already done)")
                continue
            
            # Check retry limit for failed videos
            if video_id in self.failed and self.failed[video_id] >= 3:
                print(f"[{i}/{total}] ⚠️  Skipping {video_id} (max retries exceeded)")
                continue
            
            print(f"[{i}/{total}] 🎥 Processing {video_id}")
            print(f"           Date: {video['date']}")
            
            # Process video
            success = self.process_video(video)
            
            if success:
                self.completed.add(video_id)
                # Remove from failed if it was there
                if video_id in self.failed:
                    del self.failed[video_id]
                processed_count += 1
            else:
                # Track failures
                if video_id not in self.failed:
                    self.failed[video_id] = 0
                self.failed[video_id] += 1
                failed_count += 1
            
            # Save checkpoint after each video
            self.save_checkpoint()
            self.update_status(None, "waiting")
            
            print()
            
            # Brief pause between videos
            if i < total and not self.stop_requested:
                time.sleep(2)
        
        # Final summary
        print("\n" + "=" * 70)
        print("FINAL SUMMARY")
        print("=" * 70)
        print(f"✅ Successfully processed: {processed_count}")
        print(f"✅ Previously completed: {len(self.completed) - processed_count}")
        print(f"❌ Failed: {failed_count}")
        
        if len(self.failed) > 0:
            print(f"\n⚠️  {len(self.failed)} videos need attention:")
            for vid_id, retry_count in list(self.failed.items())[:5]:
                print(f"   - {vid_id} (failed {retry_count} times)")
            if len(self.failed) > 5:
                print(f"   ... and {len(self.failed) - 5} more")
            print("\nCheck logs/transcription_errors.json for details")
            print("Re-run this script to retry failed videos")
        
        if len(self.completed) == total:
            print("\n🎉 ALL VIDEOS TRANSCRIBED SUCCESSFULLY! 🎉")
        
        # Print timing stats
        elapsed = time.time() - self.start_time
        print(f"\nTotal time: {elapsed/3600:.1f} hours")
        if processed_count > 0:
            print(f"Average time per video: {elapsed/processed_count/60:.1f} minutes")
        
        # Final checkpoint save
        self.save_checkpoint()
        self.update_status(None, "completed")

def main():
    """Main entry point."""
    manifest_path = "../s3_manifest_cohort3.json"
    
    if not os.path.exists(manifest_path):
        print(f"❌ Manifest not found: {manifest_path}")
        sys.exit(1)
    
    print("🚀 Starting Robust Batch Transcription Runner")
    print("   Press Ctrl+C to pause (progress will be saved)")
    print("   Re-run script to resume from checkpoint")
    
    runner = RobustBatchRunner(manifest_path)
    runner.run()

if __name__ == "__main__":
    main()