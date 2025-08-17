# AI Course Transcription System Package

This package contains a complete system for transcribing and analyzing AI/system design course recordings. It includes all scripts, processed content, and documentation needed to run the transcription workflow.

## 📦 Package Contents

### Core System Files
- **`README.md`** - Original transcription system documentation
- **`quick_start.py`** - Simple entry point for the transcription system
- **`transcribe_lecture.py`** - Individual lecture transcription script

### Scripts Directory (`scripts/`)
- **`auth_handler.py`** - Authentication for video platforms
- **`batch_transcriber.py`** - Batch video transcription using Whisper
- **`content_extractor.py`** - Extract learning principles from transcripts
- **`curriculum_analyzer.py`** - Analyze curriculum structure and content
- **`simplified_orchestrator.py`** - Main workflow orchestrator
- **`workflow_orchestrator.py`** - Advanced workflow management

### Configuration (`config/`)
- **`requirements.txt`** - Python dependencies
- **`simplified_config.json`** - System configuration

### Processed Content

#### Cohorts (`cohorts/`)
Complete transcribed content from 5 cohorts (cohort_2 through cohort_6):
- **9 weeks per cohort** with 2-3 classes each
- **Video files** (`.mp4`)
- **Transcripts** (`.txt`) with timestamps
- **Analysis reports** (`.json`) with extracted principles
- **Teaching notes** (`.md`) with structured content

#### Reports (`reports/`)
- Individual class analysis reports in JSON format
- Cross-cohort learning progression analysis
- Extracted programming principles and concepts

#### Logs (`logs/`)
- Processing logs and checkpoints
- Workflow execution history

### Sample Content
- **`harvard_scalability_lecture.webm`** - Sample lecture video
- **`harvard_scalability_lecture_transcript.txt`** - Sample transcript
- **`hello_interview_system_design.mp4`** - Interview system design video

### Documentation
- **`cohort_workflow_architecture.md`** - Detailed system architecture
- **`simplified_workflow_architecture.md`** - Simplified workflow guide
- **`AI_Tutor_Question_Framework.md`** - Framework for AI tutoring

### Virtual Environment (`whisper_env/`)
- Pre-configured Python virtual environment with all dependencies
- Ready-to-use Whisper transcription setup

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Navigate to the package directory
cd ai-course-transcription-package

# Activate the pre-configured environment
source whisper_env/bin/activate

# Or create a fresh environment
python3 -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
```

### 2. Run Transcription
```bash
# Simple transcription of a single file
python transcribe_lecture.py

# Batch process existing videos
python quick_start.py

# Full workflow orchestration
cd scripts
python simplified_orchestrator.py
```

### 3. Access Processed Content
- Browse `cohorts/` for transcribed course content
- Check `reports/` for analysis results
- Review `logs/` for processing history

## 📊 What's Included

### Transcribed Content
- **5 cohorts** of system design courses
- **~45 weeks** of content (9 weeks × 5 cohorts)
- **~120 individual classes** transcribed
- **Comprehensive analysis** of programming principles

### Key Features
- **Automated transcription** using OpenAI Whisper
- **Content analysis** with principle extraction
- **Structured learning materials** for LLM training
- **Cross-cohort progression tracking**
- **Batch processing capabilities**

## 🛠 Technical Requirements

### Dependencies (included in requirements.txt)
- `faster-whisper>=0.10.0` - Core transcription engine
- `selenium>=4.15.0` - Web automation
- `requests>=2.31.0` - HTTP requests
- `pandas>=2.1.0` - Data processing
- `transformers>=4.35.0` - NLP models

### System Requirements
- **Python 3.8+**
- **FFmpeg** (for audio processing)
- **8GB+ RAM** (16GB recommended for batch processing)
- **500GB+ storage** (for all video content)

## 📁 Directory Structure
```
ai-course-transcription-package/
├── README.md                          # Original system docs
├── PACKAGE_README.md                  # This file
├── quick_start.py                     # Simple entry point
├── transcribe_lecture.py              # Individual transcription
├── scripts/                           # Core processing scripts
│   ├── simplified_orchestrator.py    # Main workflow
│   ├── batch_transcriber.py          # Batch processing
│   ├── content_extractor.py          # Content analysis
│   └── ...
├── config/                            # Configuration files
│   ├── requirements.txt              # Dependencies
│   └── simplified_config.json        # Settings
├── cohorts/                           # Processed course content
│   ├── cohort_2/                     # 9 weeks of content
│   ├── cohort_3/                     # 9 weeks of content
│   ├── cohort_4/                     # 9 weeks of content
│   ├── cohort_5/                     # 9 weeks of content
│   └── cohort_6/                     # 9 weeks of content
├── reports/                           # Analysis outputs
├── logs/                              # Processing logs
└── whisper_env/                       # Pre-configured environment
```

## 🎯 Use Cases

### For Developers
- **Learn system design** from transcribed courses
- **Extract programming principles** from expert instruction
- **Study teaching methodologies** from successful courses

### For Educators
- **Create structured curricula** from analyzed content
- **Develop learning progressions** based on cross-cohort analysis
- **Generate practice problems** from extracted examples

### For Researchers
- **Train LLMs** on structured educational content
- **Analyze learning patterns** across cohorts
- **Study educational effectiveness** through transcript analysis

## 🔧 Customization

### Adding New Content
1. Place video files in `cohorts/cohort_X/week_XX/`
2. Run `python scripts/simplified_orchestrator.py`
3. Check `reports/` for analysis results

### Modifying Analysis
- Edit prompts in `scripts/content_extractor.py`
- Adjust configuration in `config/simplified_config.json`
- Customize output formats in processing scripts

## 📋 Notes

- **Virtual Environment**: The `whisper_env/` directory contains a pre-configured environment with all dependencies
- **Large Files**: Video files are included but may need to be downloaded separately depending on your setup
- **Processing Time**: Full batch processing can take several hours depending on hardware
- **Storage**: Complete package is ~500GB due to video content

## 🆘 Support

Refer to the original `README.md` for detailed technical documentation and troubleshooting guides.
