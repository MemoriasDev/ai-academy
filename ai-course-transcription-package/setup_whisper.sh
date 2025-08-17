#!/bin/bash

# Module Mind - Whisper Environment Setup Script
# This script automates the setup of the Python environment for transcription

set -e  # Exit on error

echo "==========================================="
echo "Module Mind - Whisper Environment Setup"
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    REQUIRED_VERSION="3.8"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        print_status "Python $PYTHON_VERSION found (>= 3.8 required)"
    else
        print_error "Python $PYTHON_VERSION found, but 3.8+ is required"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    print_status "FFmpeg is installed"
else
    print_error "FFmpeg not found"
    echo ""
    echo "Please install FFmpeg:"
    echo "  macOS:    brew install ffmpeg"
    echo "  Ubuntu:   sudo apt install ffmpeg"
    echo "  Windows:  Download from https://ffmpeg.org/"
    exit 1
fi

# Check if virtual environment already exists
echo ""
echo "Setting up virtual environment..."
if [ -d "whisper_env" ]; then
    print_warning "Virtual environment 'whisper_env' already exists"
    read -p "Do you want to delete and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf whisper_env
        print_status "Removed existing environment"
    else
        print_status "Using existing environment"
        source whisper_env/bin/activate
        print_status "Environment activated"
        exit 0
    fi
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv whisper_env
print_status "Virtual environment created"

# Activate virtual environment
echo "Activating virtual environment..."
source whisper_env/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet
print_status "pip upgraded"

# Install requirements
echo ""
echo "Installing requirements (this may take a few minutes)..."
if [ -f "config/requirements.txt" ]; then
    pip install -r config/requirements.txt --quiet
    print_status "Requirements installed"
else
    print_error "requirements.txt not found at config/requirements.txt"
    exit 1
fi

# Test whisper installation
echo ""
echo "Testing Whisper installation..."
python -c "from faster_whisper import WhisperModel; print('Whisper test successful')" 2>/dev/null
if [ $? -eq 0 ]; then
    print_status "Whisper is working correctly"
else
    print_warning "Whisper test failed, trying alternative import..."
    python -c "import whisper; print('Alternative whisper import successful')" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "Alternative Whisper module is working"
    else
        print_error "Whisper installation failed"
        exit 1
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating default .env file..."
    cat > .env << EOL
# Whisper Configuration
WHISPER_MODEL=base
WHISPER_CACHE_DIR=~/.cache/whisper
WHISPER_VERBOSE=false
EOL
    print_status ".env file created with defaults"
fi

# Success message
echo ""
echo "==========================================="
echo -e "${GREEN}Setup completed successfully!${NC}"
echo "==========================================="
echo ""
echo "To use the transcription environment:"
echo "  1. Activate: source whisper_env/bin/activate"
echo "  2. Run transcription: python transcribe_lecture.py <video_file>"
echo "  3. Deactivate when done: deactivate"
echo ""
echo "For more information, see WHISPER_SETUP.md"