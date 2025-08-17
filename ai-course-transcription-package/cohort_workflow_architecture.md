# Cohort Recording Transcription Workflow Architecture

## Overview
Autonomous system to download and transcribe recordings from Cohorts 2-6 (5 cohorts total, 2-3 classes/week, 9 weeks each).

## System Architecture

### 1. Authentication & Download Layer
- **Primary**: Selenium WebDriver for authentication
- **Secondary**: Requests session for file downloads
- **Backup**: Playwright as fallback option

### 2. Content Organization
```
transcription/
├── cohorts/
│   ├── cohort_2/
│   │   ├── week_01/
│   │   │   ├── class_1_video.mp4
│   │   │   ├── class_1_transcript.txt
│   │   │   ├── class_1_summary.md
│   │   │   └── class_1_principles.json
│   │   ├── week_02/
│   │   └── ... (9 weeks total)
│   ├── cohort_3/
│   ├── cohort_4/
│   ├── cohort_5/
│   └── cohort_6/
├── scripts/
│   ├── auth_handler.py          # Handle login/authentication
│   ├── video_downloader.py      # Download video files
│   ├── batch_transcriber.py     # Transcribe using faster-whisper
│   ├── content_extractor.py     # Extract principles/instructions
│   └── workflow_orchestrator.py # Main automation script
├── config/
│   ├── credentials.json         # Encrypted credentials
│   ├── cohort_schedule.json     # Class schedules and URLs
│   └── extraction_prompts.txt   # LLM prompts for content extraction
└── logs/
    └── workflow_log.txt         # Processing logs
```

### 3. Transcription Pipeline
- **Engine**: faster-whisper (already configured)
- **Model**: base (good speed/accuracy balance)
- **Optimization**: Batch processing with parallel workers
- **Output**: Timestamped transcripts with metadata

### 4. Content Extraction Pipeline
- **Stage 1**: Raw transcript cleaning
- **Stage 2**: Segment identification (lectures, discussions, exercises)
- **Stage 3**: Principle extraction using NLP/LLM
- **Stage 4**: Structured output (JSON + Markdown)

## Workflow Phases

### Phase 1: Discovery & Authentication
1. Connect to https://aitra-legacy-content.vercel.app/
2. Authenticate using provided credentials
3. Discover all available video URLs for Cohorts 2-6
4. Build comprehensive download manifest

### Phase 2: Content Acquisition
1. Download videos systematically (cohort → week → class)
2. Verify file integrity
3. Organize in structured directories
4. Create metadata files

### Phase 3: Transcription
1. Batch process videos using faster-whisper
2. Generate timestamped transcripts
3. Extract audio features for quality assessment
4. Create searchable transcript database

### Phase 4: Content Analysis
1. Segment transcripts by topic/activity
2. Extract core programming principles
3. Identify instruction patterns
4. Generate structured learning materials

## Technical Requirements

### Dependencies
```python
# Core automation
selenium>=4.15.0
playwright>=1.40.0
requests>=2.31.0

# Video processing
faster-whisper>=0.10.0
ffmpeg-python>=0.2.0

# Content analysis
spacy>=3.7.0
transformers>=4.35.0
beautifulsoup4>=4.12.0

# Data handling
pandas>=2.1.0
numpy>=1.24.0
```

### System Requirements
- **Storage**: ~500GB for videos + transcripts
- **RAM**: 16GB minimum (32GB recommended)
- **CPU**: Multi-core (8+ cores recommended)
- **GPU**: Optional but recommended for faster transcription

## Security Considerations
- Encrypted credential storage
- Session token management
- Rate limiting to avoid detection
- Error handling for authentication failures
- Audit logging for all activities

## Output Formats

### Transcripts
- **Raw**: Timestamped text files
- **Cleaned**: Formatted markdown with sections
- **Structured**: JSON with metadata

### Extracted Content
- **Principles**: JSON database of programming concepts
- **Instructions**: Step-by-step guides in markdown
- **Examples**: Code snippets with explanations
- **Exercises**: Practice problems and solutions

## Automation Schedule
- **Full sync**: Weekly (check for new content)
- **Incremental**: Daily (process new downloads)
- **Maintenance**: Monthly (cleanup and optimization)

## Success Metrics
- **Coverage**: 100% of available recordings
- **Quality**: >95% transcription accuracy
- **Extraction**: Comprehensive principle database
- **Usability**: Structured content for LLM training/course creation
