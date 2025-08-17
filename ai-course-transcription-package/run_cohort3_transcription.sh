#!/bin/bash

# Cohort 3 Batch Transcription Runner
# This script processes all Cohort 3 videos with error handling and progress tracking

echo "🎓 Cohort 3 Batch Transcription System"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Activating virtual environment...${NC}"
    if [ -f "whisper_env/bin/activate" ]; then
        source whisper_env/bin/activate
    else
        echo -e "${RED}❌ Virtual environment not found!${NC}"
        echo "Please run: python3 -m venv whisper_env && source whisper_env/bin/activate"
        exit 1
    fi
fi

# Configuration
MANIFEST="s3_manifest_cohort3.json"
LOG_FILE="logs/cohort3_transcription_$(date +%Y%m%d_%H%M%S).log"
CHECKPOINT_FILE="logs/cohort3_checkpoint.json"

# Create logs directory
mkdir -p logs

echo "Configuration:"
echo "  Manifest: $MANIFEST"
echo "  Log file: $LOG_FILE"
echo "  Checkpoint: $CHECKPOINT_FILE"
echo ""

# Function to count videos in manifest
count_videos() {
    python3 -c "import json; print(len(json.load(open('$MANIFEST'))['videos']))"
}

# Function to check completed transcripts
check_completed() {
    local completed=0
    local total=$(count_videos)
    
    for week in cohorts/cohort_3/week_*/; do
        if [ -d "$week" ]; then
            completed=$((completed + $(ls -1 "$week"/*.txt 2>/dev/null | wc -l)))
        fi
    done
    
    echo "$completed/$total"
}

# Show current status
echo "Current Status:"
echo "  Videos in manifest: $(count_videos)"
echo "  Transcripts completed: $(check_completed)"
echo ""

# Ask for confirmation
read -p "Start transcription? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${GREEN}Starting batch transcription...${NC}"
echo "================================"
echo ""

# Run transcription with detailed logging
cd scripts
python3 - << 'EOF'
import json
import sys
import os
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from s3_batch_transcriber import S3BatchTranscriber

def run_batch_with_checkpointing():
    manifest_path = "../s3_manifest_cohort3.json"
    checkpoint_path = "../logs/cohort3_checkpoint.json"
    
    # Load manifest
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Load checkpoint if exists
    completed = set()
    if os.path.exists(checkpoint_path):
        with open(checkpoint_path, 'r') as f:
            checkpoint = json.load(f)
            completed = set(checkpoint.get('completed', []))
    
    # Initialize transcriber
    transcriber = S3BatchTranscriber(
        model_size="base",
        device="cpu",
        max_workers=1  # Process one at a time for stability
    )
    
    videos = manifest['videos']
    total = len(videos)
    
    print(f"📚 Processing {total} videos from Cohort 3")
    print(f"⏭️  Skipping {len(completed)} already completed")
    print("")
    
    for i, video in enumerate(videos, 1):
        video_id = f"week_{video['week']}_class_{video['lesson']}"
        
        # Skip if already completed
        if video_id in completed:
            print(f"[{i}/{total}] ⏭️  Skipping {video_id} (already done)")
            continue
        
        print(f"[{i}/{total}] 🎥 Processing {video_id}")
        print(f"           Date: {video['date']}")
        
        try:
            # Check if output already exists
            output_path = Path(f"../{video['output_path']}.txt")
            if output_path.exists():
                print(f"           ✅ Transcript already exists")
                completed.add(video_id)
            else:
                # Process video
                result = transcriber.transcribe_from_url(
                    video['url'],
                    f"../{video['output_path']}",
                    metadata={
                        'cohort': video['cohort'],
                        'week': video['week'],
                        'lesson': video['lesson'],
                        'date': video['date']
                    }
                )
                
                print(f"           ✅ Completed in {result['processing_time']:.1f}s")
                print(f"           📝 {result['segments_count']} segments")
                completed.add(video_id)
            
            # Save checkpoint after each success
            with open(checkpoint_path, 'w') as f:
                json.dump({'completed': list(completed), 'timestamp': time.time()}, f)
                
        except Exception as e:
            print(f"           ❌ Failed: {str(e)}")
            print(f"           Will retry in next run")
            continue
        
        print("")
    
    # Final summary
    print("=" * 50)
    print("FINAL SUMMARY")
    print("=" * 50)
    print(f"✅ Completed: {len(completed)}/{total}")
    
    if len(completed) < total:
        failed = total - len(completed)
        print(f"❌ Failed/Skipped: {failed}")
        print("\nRe-run this script to retry failed videos")
    else:
        print("\n🎉 All videos transcribed successfully!")
    
    # Print stats
    transcriber.print_summary()

if __name__ == "__main__":
    run_batch_with_checkpointing()
EOF

echo ""
echo -e "${GREEN}✅ Batch transcription complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review transcripts in cohorts/cohort_3/"
echo "2. Check logs for any errors: $LOG_FILE"
echo "3. Create course manifest for course.json generation"
echo ""
echo "To generate course content:"
echo "  - Create week manifests (like week2_manifest.json)"
echo "  - Use transcript-course-processor agent"