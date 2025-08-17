# Whisper Transcription Environment Setup Guide

## Overview
This guide helps you set up the Python environment needed for the Module Mind transcription system, which uses OpenAI's Whisper model to convert video lectures into timestamped transcripts.

## Prerequisites

### 1. System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 8GB RAM (16GB recommended for large videos)
- **Storage**: ~2GB for models and dependencies
- **OS**: macOS, Linux, or Windows (with WSL2 recommended)

### 2. Required Software

#### FFmpeg (Required for audio extraction)
FFmpeg is essential for processing video files.

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
```bash
winget install ffmpeg
```

#### Python 3.8+
Verify your Python version:
```bash
python3 --version
```

## Setup Instructions

### Step 1: Navigate to Transcription Package
```bash
cd ai-course-transcription-package
```

### Step 2: Create Virtual Environment
```bash
# Create a new virtual environment
python3 -m venv whisper_env

# Activate the environment
# On macOS/Linux:
source whisper_env/bin/activate

# On Windows:
whisper_env\Scripts\activate
```

### Step 3: Upgrade pip
```bash
pip install --upgrade pip
```

### Step 4: Install Requirements
```bash
# Install all dependencies from requirements.txt
pip install -r config/requirements.txt
```

### Step 5: Download Whisper Models (Optional)
The first run will automatically download models, but you can pre-download:
```python
# Python script to pre-download models
import whisper
model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
```

### Step 6: Verify Installation
```bash
# Run the setup verification script
python setup.py

# Or manually test:
python -c "import whisper; print('Whisper installed successfully')"
```

## Usage

### Basic Transcription
```bash
# Activate environment
source whisper_env/bin/activate  # or whisper_env\Scripts\activate on Windows

# Transcribe a single video
python transcribe_lecture.py path/to/video.mp4

# Batch transcribe videos
python scripts/batch_transcriber.py
```

### Workflow Orchestration
```bash
# Run the complete workflow for course creation
python scripts/workflow_orchestrator.py
```

## Troubleshooting

### Common Issues

#### 1. "No module named 'whisper'"
**Solution**: Ensure you've activated the virtual environment:
```bash
source whisper_env/bin/activate
```

#### 2. "FFmpeg not found"
**Solution**: Install FFmpeg and ensure it's in your PATH:
```bash
which ffmpeg  # Should return the path to ffmpeg
```

#### 3. Out of Memory Errors
**Solution**: Use a smaller Whisper model:
```python
# In your transcription script, change:
model = whisper.load_model("large")  # Memory intensive
# To:
model = whisper.load_model("base")   # Less memory required
```

#### 4. CUDA/GPU Issues (Optional GPU Acceleration)
If you have an NVIDIA GPU and want faster transcription:
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## Model Selection Guide

| Model  | Parameters | English-only | Multilingual | Required VRAM | Relative Speed |
|--------|-----------|--------------|--------------|---------------|----------------|
| tiny   | 39 M      | ✓            | ✓            | ~1 GB         | ~32x           |
| base   | 74 M      | ✓            | ✓            | ~1 GB         | ~16x           |
| small  | 244 M     | ✓            | ✓            | ~2 GB         | ~6x            |
| medium | 769 M     | ✓            | ✓            | ~5 GB         | ~2x            |
| large  | 1550 M    | ✗            | ✓            | ~10 GB        | 1x             |

**Recommendation**: Start with "base" model for good balance of speed and accuracy.

## Environment Variables

Create a `.env` file in the transcription package directory:
```bash
# Optional: Specify default model
WHISPER_MODEL=base

# Optional: Set cache directory for models
WHISPER_CACHE_DIR=~/.cache/whisper

# Optional: Enable verbose logging
WHISPER_VERBOSE=true
```

## Deactivating the Environment

When finished with transcription work:
```bash
deactivate
```

## Cleaning Up (Optional)

To completely remove the environment and start fresh:
```bash
# Deactivate if currently active
deactivate

# Remove the environment directory
rm -rf whisper_env/

# Then follow setup instructions again
```

## Additional Resources

- [OpenAI Whisper Repository](https://github.com/openai/whisper)
- [Faster Whisper (Optimized Version)](https://github.com/guillaumekln/faster-whisper)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

## Support

If you encounter issues not covered here:
1. Check the [project issues](https://github.com/your-repo/module-mind/issues)
2. Ensure all prerequisites are installed
3. Try with a fresh virtual environment
4. Test with a smaller video file first