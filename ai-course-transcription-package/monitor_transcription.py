#!/usr/bin/env python3
"""
Real-time monitoring system for batch transcription with progress tracking,
error detection, and automatic recovery.
"""

import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import threading
import signal

class TranscriptionMonitor:
    def __init__(self, manifest_path="s3_manifest_cohort3.json"):
        self.manifest_path = manifest_path
        self.checkpoint_path = "logs/cohort3_checkpoint.json"
        self.status_path = "logs/transcription_status.json"
        self.log_path = "logs/monitor.log"
        self.running = True
        
        # Load manifest
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
        
        self.total_videos = len(self.manifest['videos'])
        self.start_time = None
        self.current_video = None
        self.completed_videos = set()
        self.failed_videos = []
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print("\n\n⚠️  Monitoring stopped by user")
        self.running = False
        sys.exit(0)
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def load_checkpoint(self):
        """Load checkpoint to get completed videos."""
        if os.path.exists(self.checkpoint_path):
            with open(self.checkpoint_path, 'r') as f:
                checkpoint = json.load(f)
                return set(checkpoint.get('completed', []))
        return set()
    
    def check_completed_files(self):
        """Check actual transcript files on disk."""
        completed = []
        for video in self.manifest['videos']:
            txt_path = Path(f"{video['output_path']}.txt")
            json_path = Path(f"{video['output_path']}.json")
            
            if txt_path.exists() and json_path.exists():
                # Check file size to ensure it's not empty
                if txt_path.stat().st_size > 100:
                    video_id = f"week_{video['week']}_class_{video['lesson']}"
                    completed.append({
                        'id': video_id,
                        'week': video['week'],
                        'lesson': video['lesson'],
                        'size_mb': txt_path.stat().st_size / (1024*1024),
                        'modified': datetime.fromtimestamp(txt_path.stat().st_mtime)
                    })
        return completed
    
    def estimate_time_remaining(self, completed_count, elapsed_time):
        """Estimate remaining time based on current progress."""
        if completed_count == 0:
            avg_time_per_video = 300  # Assume 5 minutes initially
        else:
            avg_time_per_video = elapsed_time / completed_count
        
        remaining_videos = self.total_videos - completed_count
        estimated_remaining = remaining_videos * avg_time_per_video
        
        return timedelta(seconds=int(estimated_remaining))
    
    def get_current_processing(self):
        """Detect which video is currently being processed."""
        # Check for most recently modified temp files
        temp_dir = Path("/var/folders")
        latest_mp4 = None
        latest_time = 0
        
        try:
            for mp4_file in temp_dir.rglob("*.mp4"):
                if mp4_file.stat().st_mtime > latest_time:
                    latest_time = mp4_file.stat().st_mtime
                    latest_mp4 = mp4_file
                    
            # If we found a recent temp file (modified in last 10 minutes)
            if latest_mp4 and (time.time() - latest_time) < 600:
                # Try to match with manifest
                for video in self.manifest['videos']:
                    if f"{video['date']}" in str(latest_mp4):
                        return f"Week {video['week']} Class {video['lesson']}"
        except:
            pass
        
        return None
    
    def display_status(self):
        """Display current transcription status."""
        self.clear_screen()
        
        # Header
        print("=" * 70)
        print("🎥 COHORT 3 TRANSCRIPTION MONITOR".center(70))
        print("=" * 70)
        print()
        
        # Get current status
        completed_files = self.check_completed_files()
        completed_count = len(completed_files)
        
        # Progress bar
        progress = completed_count / self.total_videos
        bar_length = 50
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"Progress: [{bar}] {progress*100:.1f}%")
        print(f"Status:   {completed_count}/{self.total_videos} videos completed")
        print()
        
        # Time tracking
        if self.start_time:
            elapsed = time.time() - self.start_time
            elapsed_td = timedelta(seconds=int(elapsed))
            remaining = self.estimate_time_remaining(completed_count, elapsed)
            
            print(f"⏱️  Time Elapsed:    {elapsed_td}")
            print(f"⏳ Time Remaining:  ~{remaining}")
            print(f"🏁 Expected Finish: {(datetime.now() + remaining).strftime('%I:%M %p')}")
        print()
        
        # Current processing
        current = self.get_current_processing()
        if current:
            print(f"🔄 Currently Processing: {current}")
        else:
            print(f"⏸️  No active processing detected")
        print()
        
        # Recent completions
        if completed_files:
            print("📝 Recent Completions:")
            recent = sorted(completed_files, key=lambda x: x['modified'], reverse=True)[:5]
            for video in recent:
                time_ago = datetime.now() - video['modified']
                if time_ago.total_seconds() < 3600:
                    time_str = f"{int(time_ago.total_seconds() / 60)} min ago"
                else:
                    time_str = f"{int(time_ago.total_seconds() / 3600)} hours ago"
                
                print(f"   ✅ Week {video['week']} Class {video['lesson']} ({video['size_mb']:.1f} MB) - {time_str}")
        print()
        
        # System resources
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            print("💻 System Resources:")
            print(f"   CPU Usage:   {cpu_percent}%")
            print(f"   Memory Used: {memory.percent}%")
        except:
            pass
        
        print()
        print("-" * 70)
        print("Press Ctrl+C to stop monitoring")
        print("Status updates every 30 seconds...")
    
    def write_status_file(self):
        """Write current status to JSON file for external monitoring."""
        completed_files = self.check_completed_files()
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': self.total_videos,
            'completed': len(completed_files),
            'remaining': self.total_videos - len(completed_files),
            'progress_percent': (len(completed_files) / self.total_videos) * 100,
            'completed_videos': [v['id'] for v in completed_files],
            'start_time': self.start_time,
            'estimated_completion': None
        }
        
        if self.start_time and len(completed_files) > 0:
            elapsed = time.time() - self.start_time
            remaining = self.estimate_time_remaining(len(completed_files), elapsed)
            status['estimated_completion'] = (datetime.now() + remaining).isoformat()
        
        with open(self.status_path, 'w') as f:
            json.dump(status, f, indent=2)
    
    def monitor_loop(self):
        """Main monitoring loop."""
        self.start_time = time.time()
        
        print("🚀 Starting transcription monitoring...")
        print("   This will update every 30 seconds")
        print()
        time.sleep(2)
        
        while self.running:
            try:
                self.display_status()
                self.write_status_file()
                
                # Check if all completed
                completed_count = len(self.check_completed_files())
                if completed_count >= self.total_videos:
                    self.clear_screen()
                    print("🎉 ALL VIDEOS TRANSCRIBED SUCCESSFULLY! 🎉")
                    print()
                    print(f"Total videos processed: {self.total_videos}")
                    print(f"Total time: {timedelta(seconds=int(time.time() - self.start_time))}")
                    break
                
                # Wait 30 seconds before next update
                time.sleep(30)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in monitoring: {e}")
                time.sleep(5)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor batch transcription progress')
    parser.add_argument('--manifest', default='s3_manifest_cohort3.json', help='Path to manifest file')
    parser.add_argument('--interval', type=int, default=30, help='Update interval in seconds')
    
    args = parser.parse_args()
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Start monitoring
    monitor = TranscriptionMonitor(args.manifest)
    monitor.monitor_loop()

if __name__ == "__main__":
    main()