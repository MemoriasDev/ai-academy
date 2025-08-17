#!/usr/bin/env python3
"""
Setup script for AI Course Transcription System Package

This script helps set up the environment and verify the package is ready to use.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ FFmpeg not found")
    if platform.system() == "Darwin":  # macOS
        print("Install with: brew install ffmpeg")
    elif platform.system() == "Linux":
        print("Install with: sudo apt-get install ffmpeg")
    else:
        print("Please install FFmpeg from https://ffmpeg.org/")
    return False

def setup_virtual_environment():
    """Set up a fresh virtual environment if needed."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    print("🔧 Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install Python dependencies."""
    config_path = Path("config/requirements.txt")
    
    if not config_path.exists():
        print("❌ requirements.txt not found")
        return False
    
    print("🔧 Installing dependencies...")
    try:
        if platform.system() == "Windows":
            pip_path = "venv/Scripts/pip"
        else:
            pip_path = "venv/bin/pip"
        
        subprocess.run([pip_path, "install", "-r", str(config_path)], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def verify_package_structure():
    """Verify the package structure is complete."""
    required_paths = [
        "scripts/simplified_orchestrator.py",
        "scripts/batch_transcriber.py",
        "config/requirements.txt",
        "README.md",
        "PACKAGE_README.md"
    ]
    
    missing = []
    for path in required_paths:
        if not Path(path).exists():
            missing.append(path)
    
    if missing:
        print("❌ Missing required files:")
        for path in missing:
            print(f"   - {path}")
        return False
    
    print("✅ Package structure verified")
    return True

def show_quick_start():
    """Show quick start instructions."""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\nQuick Start Commands:")
    print("1. Activate environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Transcribe a single file:")
    print("   python transcribe_lecture.py")
    
    print("\n3. Run batch processing:")
    print("   python quick_start.py")
    
    print("\n4. Full workflow:")
    print("   cd scripts")
    print("   python simplified_orchestrator.py")
    
    print("\n📖 Read PACKAGE_README.md for detailed documentation")
    print("📁 Explore cohorts/ for transcribed content")
    print("📊 Check reports/ for analysis results")

def main():
    """Main setup function."""
    print("🚀 AI Course Transcription System Setup")
    print("="*50)
    
    checks = [
        ("Python Version", check_python_version),
        ("FFmpeg", check_ffmpeg),
        ("Package Structure", verify_package_structure),
        ("Virtual Environment", setup_virtual_environment),
        ("Dependencies", install_dependencies)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
    
    if all_passed:
        show_quick_start()
    else:
        print("\n❌ Setup incomplete. Please resolve the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
