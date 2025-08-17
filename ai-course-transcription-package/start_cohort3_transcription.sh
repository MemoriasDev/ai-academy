#!/bin/bash

# Master control script for Cohort 3 transcription with monitoring
# This script runs the transcription in background and monitors progress

echo "🎬 COHORT 3 BATCH TRANSCRIPTION SYSTEM"
echo "======================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
VENV_PATH="whisper_env"
MANIFEST="s3_manifest_cohort3.json"
LOG_DIR="logs"
TRANSCRIPTION_LOG="$LOG_DIR/cohort3_transcription_$(date +%Y%m%d_%H%M%S).log"
MONITOR_LOG="$LOG_DIR/monitor_$(date +%Y%m%d_%H%M%S).log"

# Create logs directory
mkdir -p $LOG_DIR

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
        python3 -m venv $VENV_PATH
        source $VENV_PATH/bin/activate
        pip install -q faster-whisper boto3 requests psutil
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        source $VENV_PATH/bin/activate
        echo -e "${GREEN}✅ Virtual environment activated${NC}"
    fi
}

# Function to show menu
show_menu() {
    echo ""
    echo "Choose an option:"
    echo "  1) Start fresh transcription (clear checkpoints)"
    echo "  2) Resume from checkpoint"
    echo "  3) Monitor only (view existing progress)"
    echo "  4) Check status"
    echo "  5) Exit"
    echo ""
    read -p "Enter choice [1-5]: " choice
    return $choice
}

# Function to clear checkpoints
clear_checkpoints() {
    echo -e "${YELLOW}Clearing previous checkpoints...${NC}"
    rm -f $LOG_DIR/cohort3_checkpoint.json
    rm -f $LOG_DIR/transcription_status.json
    rm -f $LOG_DIR/transcription_errors.json
    echo -e "${GREEN}✅ Checkpoints cleared${NC}"
}

# Function to start transcription
start_transcription() {
    echo ""
    echo -e "${GREEN}Starting batch transcription...${NC}"
    echo "  Log: $TRANSCRIPTION_LOG"
    echo ""
    
    # Run transcription in background
    nohup python scripts/batch_runner_with_monitoring.py > "$TRANSCRIPTION_LOG" 2>&1 &
    TRANS_PID=$!
    
    echo -e "${GREEN}✅ Transcription started (PID: $TRANS_PID)${NC}"
    
    # Wait a moment for it to start
    sleep 3
    
    # Start monitoring in foreground
    echo ""
    echo -e "${GREEN}Starting monitor (updates every 30 seconds)...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop monitoring (transcription continues)${NC}"
    echo ""
    sleep 2
    
    python monitor_transcription.py
    
    echo ""
    echo -e "${YELLOW}Monitor stopped. Transcription continues in background.${NC}"
    echo "  To check status: ./start_cohort3_transcription.sh (option 4)"
    echo "  To stop transcription: kill $TRANS_PID"
}

# Function to monitor only
monitor_only() {
    echo ""
    echo -e "${GREEN}Starting monitor...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    sleep 2
    
    python monitor_transcription.py
}

# Function to check status
check_status() {
    echo ""
    echo "📊 Current Status"
    echo "=================="
    
    # Check if transcription is running
    if pgrep -f "batch_runner_with_monitoring.py" > /dev/null; then
        echo -e "${GREEN}✅ Transcription is RUNNING${NC}"
        echo "   PID: $(pgrep -f batch_runner_with_monitoring.py)"
    else
        echo -e "${YELLOW}⚠️  Transcription is NOT running${NC}"
    fi
    
    # Check status file
    if [ -f "$LOG_DIR/transcription_status.json" ]; then
        echo ""
        echo "Latest status:"
        python3 -c "
import json
from datetime import datetime
with open('$LOG_DIR/transcription_status.json', 'r') as f:
    status = json.load(f)
    print(f\"  Completed: {status['completed']}/{status['total']} ({status['progress_percent']:.1f}%)\" )
    print(f\"  Failed: {status.get('failed', 0)}\")
    if status.get('current_video'):
        print(f\"  Currently processing: {status['current_video']}\")
    print(f\"  Last update: {status['timestamp']}\")
"
    else
        echo "  No status file found"
    fi
    
    # Check checkpoint
    if [ -f "$LOG_DIR/cohort3_checkpoint.json" ]; then
        echo ""
        echo "Checkpoint info:"
        python3 -c "
import json
with open('$LOG_DIR/cohort3_checkpoint.json', 'r') as f:
    checkpoint = json.load(f)
    print(f\"  Videos completed: {len(checkpoint.get('completed', []))}\")
    print(f\"  Videos failed: {len(checkpoint.get('failed', {}))}\")
    print(f\"  Last checkpoint: {checkpoint.get('timestamp', 'Unknown')}\")
"
    fi
    
    # Count actual transcript files
    echo ""
    echo "Actual transcript files:"
    TRANSCRIPT_COUNT=$(find cohorts/cohort_3 -name "*.txt" -type f 2>/dev/null | wc -l)
    echo "  Found: $TRANSCRIPT_COUNT transcript files"
    
    echo ""
}

# Main script
echo "Checking environment..."
check_venv

# Check if manifest exists
if [ ! -f "$MANIFEST" ]; then
    echo -e "${RED}❌ Manifest not found: $MANIFEST${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Manifest found${NC}"

# Show current status first
check_status

# Menu loop
while true; do
    show_menu
    choice=$?
    
    case $choice in
        1)
            clear_checkpoints
            start_transcription
            break
            ;;
        2)
            start_transcription
            break
            ;;
        3)
            monitor_only
            ;;
        4)
            check_status
            ;;
        5)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option${NC}"
            ;;
    esac
done