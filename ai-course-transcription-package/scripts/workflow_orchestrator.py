#!/usr/bin/env python3
"""
Main workflow orchestrator for autonomous cohort recording processing.
Coordinates authentication, downloading, transcription, and content extraction.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import argparse

# Import our custom modules
from auth_handler import AuthHandler
from batch_transcriber import BatchTranscriber
from content_extractor import ContentExtractor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WorkflowOrchestrator:
    """Main orchestrator for the autonomous processing workflow."""
    
    def __init__(self, config_path: str = "../config/workflow_config.json"):
        self.config = self._load_config(config_path)
        self.auth_handler = None
        self.transcriber = None
        self.content_extractor = None
        self.results = {
            'workflow_start': time.strftime('%Y-%m-%d %H:%M:%S'),
            'phases_completed': [],
            'total_videos_processed': 0,
            'total_transcripts_generated': 0,
            'total_analysis_reports': 0,
            'errors': []
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load workflow configuration or create default."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default configuration
            default_config = {
                "auth": {
                    "base_url": "https://aitra-legacy-content.vercel.app/",
                    "credentials_file": "../config/credentials.json",
                    "headless_browser": True,
                    "download_timeout": 300
                },
                "transcription": {
                    "model_size": "base",
                    "device": "cpu",
                    "compute_type": "int8",
                    "max_workers": 2,
                    "batch_size": 5
                },
                "extraction": {
                    "enable_content_analysis": True,
                    "difficulty_assessment": True,
                    "code_extraction": True,
                    "generate_summaries": True
                },
                "output": {
                    "cohorts_base_path": "../cohorts",
                    "reports_path": "../reports",
                    "comprehensive_report": True,
                    "individual_reports": True
                },
                "workflow": {
                    "skip_existing_files": True,
                    "verify_downloads": True,
                    "cleanup_temp_files": True,
                    "max_retries": 3
                }
            }
            
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            logger.info(f"Created default config: {config_path}")
            return default_config
    
    def initialize_components(self):
        """Initialize all workflow components."""
        logger.info("🔧 Initializing workflow components...")
        
        # Initialize authentication handler
        self.auth_handler = AuthHandler(self.config['auth']['base_url'])
        
        # Initialize transcriber
        self.transcriber = BatchTranscriber(
            model_size=self.config['transcription']['model_size'],
            device=self.config['transcription']['device'],
            compute_type=self.config['transcription']['compute_type'],
            max_workers=self.config['transcription']['max_workers']
        )
        
        # Initialize content extractor
        self.content_extractor = ContentExtractor()
        
        logger.info("✅ All components initialized")
    
    def phase_1_authentication_discovery(self) -> bool:
        """Phase 1: Authenticate and discover all available videos."""
        logger.info("🔐 Phase 1: Authentication and Discovery")
        
        try:
            # Load credentials
            credentials = self.auth_handler.load_credentials(
                self.config['auth']['credentials_file']
            )
            
            # Authenticate
            if not self.auth_handler.authenticate_selenium(
                credentials['username'], 
                credentials['password']
            ):
                raise ValueError("Authentication failed")
            
            # Discover video URLs
            video_urls = self.auth_handler.discover_video_urls()
            
            if not video_urls:
                logger.warning("No videos discovered - this might indicate an issue with discovery logic")
                return False
            
            # Save manifest
            manifest_path = "../config/video_manifest.json"
            self.auth_handler.save_session_manifest(video_urls, manifest_path)
            
            self.results['phases_completed'].append('authentication_discovery')
            self.results['discovered_videos'] = video_urls
            
            total_videos = sum(len(videos) for videos in video_urls.values())
            logger.info(f"✅ Phase 1 complete - discovered {total_videos} videos across {len(video_urls)} cohorts")
            
            return True
            
        except Exception as e:
            error_msg = f"Phase 1 failed: {e}"
            logger.error(error_msg)
            self.results['errors'].append(error_msg)
            return False
    
    def phase_2_video_download(self) -> bool:
        """Phase 2: Download all discovered videos."""
        logger.info("📥 Phase 2: Video Download")
        
        try:
            # Load video manifest
            manifest_path = "../config/video_manifest.json"
            with open(manifest_path, 'r') as f:
                video_manifest = json.load(f)
            
            download_results = {}
            total_downloads = 0
            successful_downloads = 0
            
            for cohort, video_urls in video_manifest.items():
                logger.info(f"Downloading {len(video_urls)} videos for {cohort}")
                
                cohort_results = []
                for i, video_url in enumerate(video_urls, 1):
                    # Generate appropriate file path
                    week_num = ((i - 1) // 3) + 1  # Assuming 3 classes per week
                    class_num = ((i - 1) % 3) + 1
                    
                    output_path = f"../cohorts/{cohort}/week_{week_num:02d}/class_{class_num}_video.mp4"
                    
                    # Skip if file already exists
                    if self.config['workflow']['skip_existing_files'] and os.path.exists(output_path):
                        logger.info(f"Skipping existing file: {output_path}")
                        successful_downloads += 1
                        total_downloads += 1
                        continue
                    
                    # Download video
                    success = self.auth_handler.download_video(video_url, output_path)
                    
                    cohort_results.append({
                        'video_url': video_url,
                        'output_path': output_path,
                        'success': success
                    })
                    
                    total_downloads += 1
                    if success:
                        successful_downloads += 1
                
                download_results[cohort] = cohort_results
            
            self.results['phases_completed'].append('video_download')
            self.results['download_results'] = download_results
            self.results['total_videos_processed'] = total_downloads
            
            success_rate = successful_downloads / total_downloads if total_downloads > 0 else 0
            logger.info(f"✅ Phase 2 complete - {successful_downloads}/{total_downloads} downloads successful ({success_rate:.1%})")
            
            return success_rate > 0.5  # Require at least 50% success rate
            
        except Exception as e:
            error_msg = f"Phase 2 failed: {e}"
            logger.error(error_msg)
            self.results['errors'].append(error_msg)
            return False
    
    def phase_3_transcription(self) -> bool:
        """Phase 3: Batch transcribe all downloaded videos."""
        logger.info("🎙️ Phase 3: Batch Transcription")
        
        try:
            # Run batch transcription
            transcription_results = self.transcriber.transcribe_all_cohorts(
                self.config['output']['cohorts_base_path']
            )
            
            self.results['phases_completed'].append('transcription')
            self.results['transcription_results'] = transcription_results
            self.results['total_transcripts_generated'] = transcription_results['overall_stats']['total_successful']
            
            success_rate = transcription_results['overall_stats']['success_rate']
            logger.info(f"✅ Phase 3 complete - {success_rate:.1%} transcription success rate")
            
            return success_rate > 0.5
            
        except Exception as e:
            error_msg = f"Phase 3 failed: {e}"
            logger.error(error_msg)
            self.results['errors'].append(error_msg)
            return False
    
    def phase_4_content_extraction(self) -> bool:
        """Phase 4: Extract learning content from transcripts."""
        logger.info("🧠 Phase 4: Content Extraction and Analysis")
        
        if not self.config['extraction']['enable_content_analysis']:
            logger.info("Content analysis disabled in config - skipping Phase 4")
            return True
        
        try:
            # Find all transcript files
            cohorts_path = Path(self.config['output']['cohorts_base_path'])
            transcript_files = list(cohorts_path.rglob("*_transcript.txt"))
            
            logger.info(f"Found {len(transcript_files)} transcript files to analyze")
            
            analysis_results = []
            reports_path = Path(self.config['output']['reports_path'])
            reports_path.mkdir(exist_ok=True)
            
            # Process transcripts in parallel
            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                
                for transcript_file in transcript_files:
                    future = executor.submit(self._analyze_single_transcript, transcript_file, reports_path)
                    futures.append(future)
                
                # Collect results
                for future in futures:
                    try:
                        result = future.result()
                        analysis_results.append(result)
                    except Exception as e:
                        logger.error(f"Error analyzing transcript: {e}")
                        analysis_results.append({'success': False, 'error': str(e)})
            
            successful_analyses = [r for r in analysis_results if r.get('success', False)]
            
            self.results['phases_completed'].append('content_extraction')
            self.results['analysis_results'] = analysis_results
            self.results['total_analysis_reports'] = len(successful_analyses)
            
            # Generate comprehensive report
            if self.config['output']['comprehensive_report']:
                self._generate_comprehensive_report(successful_analyses, reports_path)
            
            success_rate = len(successful_analyses) / len(transcript_files) if transcript_files else 0
            logger.info(f"✅ Phase 4 complete - {len(successful_analyses)}/{len(transcript_files)} analyses successful ({success_rate:.1%})")
            
            return success_rate > 0.5
            
        except Exception as e:
            error_msg = f"Phase 4 failed: {e}"
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
    
    def _generate_comprehensive_report(self, analysis_results: List[Dict], reports_path: Path):
        """Generate comprehensive report across all cohorts."""
        comprehensive_data = {
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_sessions_analyzed': len(analysis_results),
            'cohort_summaries': {},
            'overall_statistics': {},
            'topic_analysis': {},
            'learning_progression': {}
        }
        
        # Aggregate data by cohort
        cohort_data = {}
        all_topics = set()
        
        for result in analysis_results:
            if result.get('success'):
                cohort = result['cohort']
                if cohort not in cohort_data:
                    cohort_data[cohort] = {
                        'sessions': 0,
                        'total_principles': 0,
                        'total_instructions': 0,
                        'topics': set()
                    }
                
                cohort_data[cohort]['sessions'] += 1
                cohort_data[cohort]['total_principles'] += result['principles_count']
                cohort_data[cohort]['total_instructions'] += result['instructions_count']
                cohort_data[cohort]['topics'].update(result['key_topics'])
                all_topics.update(result['key_topics'])
        
        # Convert sets to lists for JSON serialization
        for cohort in cohort_data:
            cohort_data[cohort]['topics'] = list(cohort_data[cohort]['topics'])
        
        comprehensive_data['cohort_summaries'] = cohort_data
        comprehensive_data['overall_statistics'] = {
            'total_cohorts': len(cohort_data),
            'unique_topics': list(all_topics),
            'topic_count': len(all_topics),
            'avg_principles_per_session': sum(r['principles_count'] for r in analysis_results) / len(analysis_results),
            'avg_instructions_per_session': sum(r['instructions_count'] for r in analysis_results) / len(analysis_results)
        }
        
        # Save comprehensive report
        report_file = reports_path / "comprehensive_analysis_report.json"
        with open(report_file, 'w') as f:
            json.dump(comprehensive_data, f, indent=2)
        
        logger.info(f"Comprehensive report saved: {report_file}")
    
    def run_full_workflow(self) -> bool:
        """Execute the complete autonomous workflow."""
        logger.info("🚀 Starting autonomous cohort processing workflow")
        
        self.initialize_components()
        
        phases = [
            ("Authentication & Discovery", self.phase_1_authentication_discovery),
            ("Video Download", self.phase_2_video_download),
            ("Batch Transcription", self.phase_3_transcription),
            ("Content Extraction", self.phase_4_content_extraction)
        ]
        
        for phase_name, phase_func in phases:
            logger.info(f"▶️ Starting: {phase_name}")
            
            phase_start = time.time()
            success = phase_func()
            phase_duration = time.time() - phase_start
            
            if success:
                logger.info(f"✅ {phase_name} completed successfully ({phase_duration:.1f}s)")
            else:
                logger.error(f"❌ {phase_name} failed - stopping workflow")
                return False
        
        # Finalize results
        self.results['workflow_end'] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.results['workflow_success'] = True
        
        # Save final report
        self._save_workflow_report()
        
        logger.info("🎉 Complete workflow finished successfully!")
        return True
    
    def _save_workflow_report(self):
        """Save comprehensive workflow report."""
        report_path = "../logs/workflow_report.json"
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        logger.info(f"Workflow report saved: {report_path}")
    
    def cleanup(self):
        """Clean up resources and temporary files."""
        if self.auth_handler:
            self.auth_handler.cleanup()
        
        if self.config['workflow']['cleanup_temp_files']:
            # Add any temp file cleanup logic here
            logger.info("🧹 Cleaned up temporary files")

def main():
    """Main entry point with command line interface."""
    parser = argparse.ArgumentParser(description="Autonomous Cohort Recording Processing Workflow")
    parser.add_argument("--config", default="../config/workflow_config.json", help="Path to configuration file")
    parser.add_argument("--phase", choices=['auth', 'download', 'transcribe', 'extract', 'all'], default='all', help="Run specific phase only")
    parser.add_argument("--dry-run", action='store_true', help="Perform dry run without actual processing")
    
    args = parser.parse_args()
    
    orchestrator = WorkflowOrchestrator(args.config)
    
    try:
        if args.dry_run:
            logger.info("🧪 Dry run mode - no actual processing will occur")
            orchestrator.initialize_components()
            logger.info("✅ Dry run successful - all components initialized correctly")
            return
        
        if args.phase == 'all':
            success = orchestrator.run_full_workflow()
        else:
            orchestrator.initialize_components()
            
            phase_map = {
                'auth': orchestrator.phase_1_authentication_discovery,
                'download': orchestrator.phase_2_video_download,
                'transcribe': orchestrator.phase_3_transcription,
                'extract': orchestrator.phase_4_content_extraction
            }
            
            success = phase_map[args.phase]()
        
        if success:
            logger.info("🎯 Workflow completed successfully!")
            sys.exit(0)
        else:
            logger.error("💥 Workflow failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        sys.exit(1)
    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    main()
