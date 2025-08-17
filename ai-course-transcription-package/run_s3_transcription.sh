#!/bin/bash

# S3 Batch Transcription Runner
# Usage: ./run_s3_transcription.sh [cohort_number]

echo "🎥 S3 Batch Transcription System"
echo "================================"

# Check if Python environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated. Activating..."
    if [ -f "whisper_env/bin/activate" ]; then
        source whisper_env/bin/activate
    else
        echo "❌ Virtual environment not found. Please run setup first:"
        echo "   python3 -m venv whisper_env"
        echo "   source whisper_env/bin/activate"
        echo "   pip install faster-whisper boto3 requests"
        exit 1
    fi
fi

# Check dependencies
echo "Checking dependencies..."
python -c "import faster_whisper" 2>/dev/null || {
    echo "Installing faster-whisper..."
    pip install faster-whisper
}
python -c "import boto3" 2>/dev/null || {
    echo "Installing boto3..."
    pip install boto3
}
python -c "import requests" 2>/dev/null || {
    echo "Installing requests..."
    pip install requests
}

# Parse arguments
COHORT=${1:-"3"}
MANIFEST_FILE="s3_manifest_cohort${COHORT}.json"

echo ""
echo "Configuration:"
echo "  Cohort: $COHORT"
echo "  Manifest: $MANIFEST_FILE"
echo ""

# Check if manifest exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "⚠️  Manifest file not found: $MANIFEST_FILE"
    echo ""
    echo "Please create your manifest file based on s3_manifest_template.json"
    echo "Example:"
    echo "  cp s3_manifest_template.json $MANIFEST_FILE"
    echo "  nano $MANIFEST_FILE  # Edit with your S3 URLs"
    exit 1
fi

# Run transcription
echo "Starting transcription..."
echo "------------------------"
cd scripts
python s3_batch_transcriber.py --manifest "../$MANIFEST_FILE"

echo ""
echo "✅ Transcription complete!"
echo ""
echo "Next steps:"
echo "1. Review transcripts in cohorts/cohort_${COHORT}/"
echo "2. Create course manifest for transcript-to-course conversion"
echo "3. Run the transcript-course-processor agent"