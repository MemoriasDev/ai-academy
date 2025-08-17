# Simplified Cohort Recording Transcription System

## Overview

This system provides a streamlined workflow for transcribing and analyzing pre-downloaded course recordings from Cohorts 2-6. It focuses on efficient batch transcription using Whisper and intelligent content extraction for LLM training or course creation.

**🎯 SIMPLIFIED APPROACH:** No authentication required - just point to your video files and run!

## System Architecture

```
transcription/
├── scripts/                    # Core workflow scripts
│   ├── auth_handler.py        # Authentication & video discovery
│   ├── batch_transcriber.py   # Batch transcription using faster-whisper
│   ├── content_extractor.py   # Extract principles & instructions
│   └── workflow_orchestrator.py # Main automation coordinator
├── config/                    # Configuration files
│   ├── credentials.json       # Login credentials (update required)
│   ├── workflow_config.json   # System configuration
│   └── requirements.txt       # Python dependencies
├── cohorts/                   # Organized video storage
│   ├── cohort_2/
│   │   ├── week_01/ ... week_09/
│   ├── cohort_3/ ... cohort_6/
├── logs/                      # Processing logs
└── reports/                   # Analysis reports
```

## Quick Start

### 1. Environment Setup

```bash
# Navigate to transcription directory
cd transcription

# Create and activate virtual environment
python3 -m venv whisper_env
source whisper_env/bin/activate

# Install dependencies
pip install -r config/requirements.txt

# Install additional system dependencies (macOS)
brew install ffmpeg
```

### 2. Configuration

```bash
# Update credentials
nano config/credentials.json
# Replace YOUR_USERNAME and YOUR_PASSWORD with actual credentials

# Optionally customize workflow settings
nano config/workflow_config.json
```

### 3. Add Your Videos & Run

```bash
# Place your video files in the cohorts structure:
# cohorts/cohort_2/week_01/class1.mp4
# cohorts/cohort_2/week_01/class2.mp4
# etc.

# Run the complete simplified workflow
cd scripts
python simplified_orchestrator.py

# Or run specific phases
python simplified_orchestrator.py --transcribe-only  # Transcription only
python simplified_orchestrator.py --analyze-only     # Content analysis only
python simplified_orchestrator.py --dry-run          # Discover videos only
```

### 4. Manual Component Testing

```bash
# Test transcription on existing videos
python batch_transcriber.py

# Test content extraction on existing transcripts
python content_extractor.py

# Test video discovery
python simplified_orchestrator.py --dry-run
```

## Simplified Workflow Phases

### Phase 1: Video Discovery & Validation
- Scans cohorts directory for video files
- Validates file accessibility and integrity
- Creates processing queue with smart filtering

### Phase 2: Batch Transcription (OPTIMIZED)
- Uses faster-whisper with 6 parallel workers (increased from 2)
- Processes videos concurrently with intelligent queue management
- Generates timestamped transcripts with comprehensive metadata
- **⚡ 3x faster than original design**

### Phase 3: Content Extraction (ENHANCED)
- Analyzes transcripts for programming principles using 8 parallel workers
- Extracts step-by-step instructions and code examples
- Generates structured learning materials for LLM training
- Cross-references concepts across cohorts for learning progression

## Output Formats

### Transcripts
- **Raw transcripts**: `*_transcript.txt` with timestamps
- **Metadata**: `*_transcript.json` with processing details
- **Analysis reports**: `*_analysis.json` with extracted content

### Extracted Content
- **Learning principles**: Categorized programming concepts
- **Instruction segments**: Step-by-step teaching sequences
- **Code examples**: Extracted code snippets with context
- **Comprehensive reports**: Cross-cohort analysis summaries

## Configuration Options

### Model Settings
```json
{
  "transcription": {
    "model_size": "base",        // tiny, base, small, medium, large
    "device": "cpu",             // cpu, cuda
    "max_workers": 2,            // Parallel transcription workers
    "batch_size": 5              // Videos per batch
  }
}
```

### Processing Options
```json
{
  "workflow": {
    "skip_existing_files": true,  // Skip already processed files
    "verify_downloads": true,     // Verify file integrity
    "max_retries": 3             // Max retry attempts
  }
}
```

## Hardware Requirements

### Minimum
- **RAM**: 8GB (16GB recommended)
- **Storage**: 500GB for videos + transcripts
- **CPU**: 4+ cores

### Recommended
- **RAM**: 32GB for faster processing
- **Storage**: 1TB+ SSD for optimal performance
- **CPU**: 8+ cores with high clock speed
- **GPU**: Optional but significantly faster for transcription

## Monitoring & Logs

- **Workflow logs**: `logs/workflow.log`
- **Transcription logs**: `logs/transcription.log`
- **Processing reports**: `logs/workflow_report.json`
- **Real-time progress**: Console output with progress indicators

## Security Features

- Encrypted credential storage
- Session token management
- Rate limiting to avoid detection
- Audit logging for all activities
- Automatic cleanup of temporary files

## Troubleshooting

### Authentication Issues
```bash
# Verify credentials
cat config/credentials.json

# Test authentication manually
python scripts/auth_handler.py
```

### Transcription Errors
```bash
# Check available memory
free -h

# Test single file transcription
python scripts/batch_transcriber.py --single path/to/video.mp4

# Use smaller model for memory constraints
# Edit config: "model_size": "tiny"
```

### Download Failures
- Check internet connection stability
- Verify authentication hasn't expired
- Review rate limiting settings
- Check available disk space

## Performance Optimization

### CPU Optimization
- Use `int8` compute type for faster CPU inference
- Set `cpu_threads=0` to use all available cores
- Process multiple files in parallel (adjust `max_workers`)

### Memory Management
- Use smaller models (`tiny`, `base`) for limited RAM
- Process files sequentially if parallel processing fails
- Clear browser cache between sessions

### Storage Optimization
- Use SSD for significantly faster I/O
- Compress older transcripts if storage limited
- Implement automatic cleanup policies

## Integration Options

### For LLM Training
- Structured JSON outputs ready for training pipelines
- Categorized content by difficulty and topic
- Clean, timestamped data with metadata

### For Course Creation
- Markdown-formatted learning materials
- Step-by-step instruction sequences
- Code examples with explanatory context
- Progressive difficulty assessment

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Review configuration in `config/`
3. Test individual components before full workflow
4. Ensure all dependencies are properly installed

## Future Enhancements

- GPU acceleration support
- Advanced NLP content analysis
- Automated quiz generation
- Multi-language support
- Cloud storage integration
