#!/usr/bin/env python3
"""
Simplified workflow orchestrator for processing pre-downloaded cohort videos.
No authentication required - pure file processing pipeline.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# Import our simplified modules
from batch_transcriber import BatchTranscriber
from content_extractor import ContentExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/simplified_workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimplifiedOrchestrator:
    """Simplified orchestrator for pure file processing workflow."""
    
    def __init__(self, config_path: str = "../config/simplified_config.json"):
        self.config = self._load_config(config_path)
        self.transcriber = None
        self.content_extractor = None
        self.results = {
            'workflow_start': time.strftime('%Y-%m-%d %H:%M:%S'),
            'phases_completed': [],
            'total_videos_found': 0,
            'total_videos_processed': 0,
            'total_transcripts_generated': 0,
            'total_analysis_reports': 0,
            'errors': []
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load simplified configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create simplified default configuration
            default_config = {
                "transcription": {
                    "model_size": "base",
                    "device": "cpu", 
                    "compute_type": "int8",
                    "max_workers": 1,  # Reduced to 1 to avoid threading issues
                    "batch_size": 10
                },
                "extraction": {
                    "enable_content_analysis": True,
                    "difficulty_assessment": True,
                    "code_extraction": True,
                    "generate_summaries": True,
                    "max_workers": 8  # Parallel content analysis
                },
                "input": {
                    "videos_base_path": "../cohorts",
                    "video_extensions": [".mp4", ".webm", ".avi", ".mov", ".mkv"]
                },
                "output": {
                    "reports_path": "../reports",
                    "comprehensive_report": True,
                    "individual_reports": True
                },
                "workflow": {
                    "skip_existing_transcripts": True,
                    "skip_existing_analysis": True,
                    "verify_file_integrity": True,
                    "cleanup_temp_files": True,
                    "checkpoint_frequency": 10  # Save progress every 10 files
                }
            }
            
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            logger.info(f"Created simplified config: {config_path}")
            return default_config
    
    def initialize_components(self):
        """Initialize transcription and analysis components."""
        logger.info("🔧 Initializing simplified workflow components...")
        
        # Initialize transcriber with optimized settings
        self.transcriber = BatchTranscriber(
            model_size=self.config['transcription']['model_size'],
            device=self.config['transcription']['device'],
            compute_type=self.config['transcription']['compute_type'],
            max_workers=self.config['transcription']['max_workers']
        )
        
        # Initialize content extractor
        self.content_extractor = ContentExtractor()
        
        logger.info("✅ All components initialized")
    
    def discover_videos(self) -> List[Path]:
        """Discover all video files in the cohorts directory."""
        logger.info("🔍 Discovering video files...")
        
        videos_path = Path(self.config['input']['videos_base_path'])
        video_extensions = set(self.config['input']['video_extensions'])
        
        video_files = []
        
        # Search through cohort directories
        for cohort_dir in videos_path.iterdir():
            if cohort_dir.is_dir() and cohort_dir.name.startswith('cohort_'):
                logger.info(f"Scanning {cohort_dir.name}...")
                
                for week_dir in cohort_dir.iterdir():
                    if week_dir.is_dir() and week_dir.name.startswith('week_'):
                        
                        for file_path in week_dir.iterdir():
                            if file_path.suffix.lower() in video_extensions:
                                video_files.append(file_path)
        
        self.results['total_videos_found'] = len(video_files)
        logger.info(f"✅ Found {len(video_files)} video files")
        
        return sorted(video_files)
    
    def validate_video_files(self, video_files: List[Path]) -> List[Path]:
        """Validate video files exist and are readable."""
        logger.info("🔍 Validating video files...")
        
        valid_files = []
        invalid_files = []
        
        for video_file in video_files:
            try:
                if video_file.exists() and video_file.stat().st_size > 0:
                    valid_files.append(video_file)
                else:
                    invalid_files.append(video_file)
            except Exception as e:
                logger.warning(f"Cannot access {video_file}: {e}")
                invalid_files.append(video_file)
        
        if invalid_files:
            logger.warning(f"Found {len(invalid_files)} invalid/inaccessible files:")
            for invalid_file in invalid_files[:5]:  # Show first 5
                logger.warning(f"  - {invalid_file}")
        
        logger.info(f"✅ Validated {len(valid_files)} video files")
        return valid_files
    
    def phase_1_transcription(self, video_files: List[Path]) -> bool:
        """Phase 1: Batch transcribe all videos."""
        logger.info("🎙️ Phase 1: Batch Transcription")
        
        try:
            # Filter out videos that already have transcripts if configured
            if self.config['workflow']['skip_existing_transcripts']:
                videos_to_process = []
                for video_file in video_files:
                    transcript_path = video_file.parent / f"{video_file.stem}_transcript.txt"
                    if not transcript_path.exists():
                        videos_to_process.append(video_file)
                    else:
                        logger.info(f"Skipping {video_file.name} - transcript exists")
                
                logger.info(f"Processing {len(videos_to_process)} videos (skipped {len(video_files) - len(videos_to_process)})")
            else:
                videos_to_process = video_files
            
            if not videos_to_process:
                logger.info("No videos to transcribe - all transcripts exist")
                self.results['phases_completed'].append('transcription')
                return True
            
            # Process videos in batches
            successful_transcriptions = 0
            failed_transcriptions = []
            
            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor(max_workers=self.config['transcription']['max_workers']) as executor:
                # Submit all transcription jobs
                future_to_video = {
                    executor.submit(self._transcribe_single_video, video_file): video_file 
                    for video_file in videos_to_process
                }
                
                # Process completed transcriptions
                for future in as_completed(future_to_video):
                    video_file = future_to_video[future]
                    try:
                        result = future.result()
                        if result['success']:
                            successful_transcriptions += 1
                            logger.info(f"✅ Transcribed: {video_file.name}")
                        else:
                            failed_transcriptions.append(video_file)
                            logger.error(f"❌ Failed: {video_file.name} - {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        failed_transcriptions.append(video_file)
                        logger.error(f"❌ Exception transcribing {video_file.name}: {e}")
                    
                    # Checkpoint progress
                    if (successful_transcriptions + len(failed_transcriptions)) % self.config['workflow']['checkpoint_frequency'] == 0:
                        self._save_checkpoint('transcription', successful_transcriptions, len(failed_transcriptions))
            
            self.results['total_transcripts_generated'] = successful_transcriptions
            self.results['phases_completed'].append('transcription')
            
            success_rate = successful_transcriptions / len(videos_to_process) if videos_to_process else 1.0
            logger.info(f"✅ Phase 1 complete - {successful_transcriptions}/{len(videos_to_process)} transcriptions successful ({success_rate:.1%})")
            
            return success_rate > 0.8  # Require 80% success rate
            
        except Exception as e:
            error_msg = f"Phase 1 failed: {e}"
            logger.error(error_msg)
            self.results['errors'].append(error_msg)
            return False
    
    def _transcribe_single_video(self, video_file: Path) -> Dict:
        """Transcribe a single video file."""
        try:
            # Create metadata for this video
            metadata = {
                'cohort': self._extract_cohort_from_path(video_file),
                'week': self._extract_week_from_path(video_file),
                'file_name': video_file.name
            }
            
            # Perform transcription
            result = self.transcriber.transcribe_single_file(
                str(video_file),
                None,  # Auto-generate output path
                metadata
            )
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file': str(video_file)
            }
    
    def phase_2_content_analysis(self) -> bool:
        """Phase 2: Analyze all transcripts for content extraction."""
        logger.info("🧠 Phase 2: Content Analysis")
        
        try:
            # Find all transcript files
            videos_path = Path(self.config['input']['videos_base_path'])
            transcript_files = list(videos_path.rglob("*_transcript.txt"))
            
            if not transcript_files:
                logger.warning("No transcript files found for analysis")
                return False
            
            logger.info(f"Found {len(transcript_files)} transcript files to analyze")
            
            # Filter existing analyses if configured
            if self.config['workflow']['skip_existing_analysis']:
                transcripts_to_process = []
                for transcript_file in transcript_files:
                    analysis_path = transcript_file.parent / f"{transcript_file.stem}_analysis.json"
                    if not analysis_path.exists():
                        transcripts_to_process.append(transcript_file)
                    else:
                        logger.info(f"Skipping {transcript_file.name} - analysis exists")
                
                logger.info(f"Analyzing {len(transcripts_to_process)} transcripts (skipped {len(transcript_files) - len(transcripts_to_process)})")
            else:
                transcripts_to_process = transcript_files
            
            if not transcripts_to_process:
                logger.info("No transcripts to analyze - all analyses exist")
                self.results['phases_completed'].append('content_analysis')
                return True
            
            # Process analyses in parallel
            successful_analyses = 0
            failed_analyses = []
            reports_path = Path(self.config['output']['reports_path'])
            reports_path.mkdir(exist_ok=True)
            
            with ThreadPoolExecutor(max_workers=self.config['extraction']['max_workers']) as executor:
                # Submit all analysis jobs
                future_to_transcript = {
                    executor.submit(self._analyze_single_transcript, transcript_file, reports_path): transcript_file
                    for transcript_file in transcripts_to_process
                }
                
                # Process completed analyses
                for future in as_completed(future_to_transcript):
                    transcript_file = future_to_transcript[future]
                    try:
                        result = future.result()
                        if result.get('success', False):
                            successful_analyses += 1
                            logger.info(f"✅ Analyzed: {transcript_file.name}")
                        else:
                            failed_analyses.append(transcript_file)
                            logger.error(f"❌ Failed analysis: {transcript_file.name}")
                    except Exception as e:
                        failed_analyses.append(transcript_file)
                        logger.error(f"❌ Exception analyzing {transcript_file.name}: {e}")
                    
                    # Checkpoint progress
                    if (successful_analyses + len(failed_analyses)) % self.config['workflow']['checkpoint_frequency'] == 0:
                        self._save_checkpoint('analysis', successful_analyses, len(failed_analyses))
            
            self.results['total_analysis_reports'] = successful_analyses
            self.results['phases_completed'].append('content_analysis')
            
            # Generate comprehensive report
            if self.config['output']['comprehensive_report']:
                self._generate_comprehensive_report(reports_path)
            
            success_rate = successful_analyses / len(transcripts_to_process) if transcripts_to_process else 1.0
            logger.info(f"✅ Phase 2 complete - {successful_analyses}/{len(transcripts_to_process)} analyses successful ({success_rate:.1%})")
            
            return success_rate > 0.8
            
        except Exception as e:
            error_msg = f"Phase 2 failed: {e}"
            logger.error(error_msg)
            self.results['errors'].append(error_msg)
            return False
    
    def _analyze_single_transcript(self, transcript_file: Path, reports_path: Path) -> Dict:
        """Analyze a single transcript file."""
        try:
            # Perform analysis
            session = self.content_extractor.analyze_class_session(str(transcript_file))
            
            # Save individual report if enabled
            if self.config['output']['individual_reports']:
                report_file = reports_path / f"{transcript_file.stem}_analysis.json"
                self.content_extractor.save_analysis_report(session, str(report_file))
            
            return {
                'success': True,
                'transcript_file': str(transcript_file),
                'cohort': session.cohort,
                'week': session.week,
                'principles_count': len(session.principles),
                'instructions_count': len(session.instructions),
                'key_topics': session.key_topics
            }
            
        except Exception as e:
            return {
                'success': False,
                'transcript_file': str(transcript_file),
                'error': str(e)
            }
    
    def _extract_cohort_from_path(self, file_path: Path) -> str:
        """Extract cohort identifier from file path."""
        for part in file_path.parts:
            if 'cohort' in part:
                return part
        return 'unknown_cohort'
    
    def _extract_week_from_path(self, file_path: Path) -> str:
        """Extract week identifier from file path."""
        for part in file_path.parts:
            if 'week' in part:
                return part
        return 'unknown_week'
    
    def _save_checkpoint(self, phase: str, successful: int, failed: int):
        """Save processing checkpoint."""
        checkpoint = {
            'phase': phase,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'successful': successful,
            'failed': failed,
            'total_processed': successful + failed
        }
        
        checkpoint_path = f"../logs/checkpoint_{phase}.json"
        with open(checkpoint_path, 'w') as f:
            json.dump(checkpoint, f, indent=2)
    
    def _generate_comprehensive_report(self, reports_path: Path):
        """Generate comprehensive cross-cohort analysis report."""
        logger.info("📊 Generating comprehensive report...")
        
        # This would aggregate all individual analysis reports
        # Implementation details depend on specific analysis needs
        comprehensive_data = {
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': f"Processed {self.results['total_videos_found']} videos across 5 cohorts",
            'transcription_success_rate': self.results['total_transcripts_generated'] / self.results['total_videos_found'],
            'analysis_success_rate': self.results['total_analysis_reports'] / self.results['total_transcripts_generated'] if self.results['total_transcripts_generated'] > 0 else 0
        }
        
        report_file = reports_path / "comprehensive_cohort_analysis.json"
        with open(report_file, 'w') as f:
            json.dump(comprehensive_data, f, indent=2)
        
        logger.info(f"📊 Comprehensive report saved: {report_file}")
    
    def run_simplified_workflow(self) -> bool:
        """Execute the simplified processing workflow."""
        logger.info("🚀 Starting simplified cohort processing workflow")
        
        self.initialize_components()
        
        # Step 1: Discover and validate videos
        video_files = self.discover_videos()
        if not video_files:
            logger.error("No video files found!")
            return False
        
        valid_videos = self.validate_video_files(video_files)
        if not valid_videos:
            logger.error("No valid video files found!")
            return False
        
        # Step 2: Process transcriptions
        logger.info(f"▶️ Processing {len(valid_videos)} video files...")
        
        if not self.phase_1_transcription(valid_videos):
            logger.error("Transcription phase failed")
            return False
        
        # Step 3: Content analysis
        if not self.phase_2_content_analysis():
            logger.error("Content analysis phase failed")
            return False
        
        # Finalize results
        self.results['workflow_end'] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.results['workflow_success'] = True
        
        # Save final report
        self._save_workflow_report()
        
        logger.info("🎉 Simplified workflow completed successfully!")
        return True
    
    def _save_workflow_report(self):
        """Save comprehensive workflow report."""
        report_path = "../logs/simplified_workflow_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        logger.info(f"Workflow report saved: {report_path}")

def main():
    """Main entry point for simplified workflow."""
    parser = argparse.ArgumentParser(description="Simplified Cohort Processing Workflow")
    parser.add_argument("--config", default="../config/simplified_config.json", help="Configuration file path")
    parser.add_argument("--transcribe-only", action='store_true', help="Run transcription only")
    parser.add_argument("--analyze-only", action='store_true', help="Run content analysis only")
    parser.add_argument("--dry-run", action='store_true', help="Discover videos without processing")
    
    args = parser.parse_args()
    
    orchestrator = SimplifiedOrchestrator(args.config)
    
    try:
        if args.dry_run:
            logger.info("🧪 Dry run - discovering videos only")
            orchestrator.initialize_components()
            video_files = orchestrator.discover_videos()
            valid_videos = orchestrator.validate_video_files(video_files)
            logger.info(f"✅ Dry run complete - found {len(valid_videos)} valid videos")
            return
        
        if args.transcribe_only:
            orchestrator.initialize_components()
            video_files = orchestrator.discover_videos()
            valid_videos = orchestrator.validate_video_files(video_files)
            success = orchestrator.phase_1_transcription(valid_videos)
        elif args.analyze_only:
            orchestrator.initialize_components()
            success = orchestrator.phase_2_content_analysis()
        else:
            success = orchestrator.run_simplified_workflow()
        
        if success:
            logger.info("🎯 Processing completed successfully!")
            sys.exit(0)
        else:
            logger.error("💥 Processing failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
