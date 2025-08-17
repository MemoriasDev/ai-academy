#!/usr/bin/env python3
"""
Batch transcription system using faster-whisper.
Optimized for processing multiple cohort recordings efficiently.
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from faster_whisper import WhisperModel
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/transcription.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BatchTranscriber:
    """Batch transcription system for cohort recordings."""
    
    def __init__(self, 
                 model_size: str = "base",
                 device: str = "cpu",
                 compute_type: str = "int8",
                 max_workers: int = 2):
        """
        Initialize the batch transcriber.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Processing device (cpu, cuda)
            compute_type: Computation type for optimization
            max_workers: Maximum parallel transcription workers
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.max_workers = max_workers
        self.model = None
        self.stats = {
            'total_processed': 0,
            'total_duration': 0,
            'total_processing_time': 0,
            'failed_files': []
        }
    
    def load_model(self):
        """Load the Whisper model with optimizations."""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                cpu_threads=0,  # Use all available CPU threads
                num_workers=1   # Single worker per model instance
            )
            logger.info("✅ Model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def get_file_hash(self, file_path: str) -> str:
        """Generate MD5 hash of file for integrity checking."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def transcribe_single_file(self, 
                              video_path: str, 
                              output_path: str = None,
                              metadata: Dict = None) -> Dict:
        """
        Transcribe a single video file.
        
        Args:
            video_path: Path to video file
            output_path: Output path for transcript (auto-generated if None)
            metadata: Additional metadata to include
            
        Returns:
            Dict with transcription results and metadata
        """
        if not self.model:
            self.load_model()
        
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Generate output path if not provided
        if output_path is None:
            output_path = video_path.parent / f"{video_path.stem}_transcript.txt"
        
        logger.info(f"🎥 Starting transcription: {video_path.name}")
        start_time = time.time()
        
        try:
            # Transcribe with optimizations
            segments, info = self.model.transcribe(
                str(video_path),
                beam_size=1,  # Faster beam search
                language="en",  # Assuming English
                condition_on_previous_text=False,  # Faster processing
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Collect all segments
            segment_list = list(segments)
            
            # Generate file hash for integrity
            file_hash = self.get_file_hash(str(video_path))
            
            # Create comprehensive metadata
            transcript_metadata = {
                'source_file': str(video_path),
                'output_file': str(output_path),
                'file_hash': file_hash,
                'file_size': video_path.stat().st_size,
                'language': info.language,
                'language_probability': float(info.language_probability),
                'duration_seconds': float(info.duration),
                'model_used': self.model_size,
                'segment_count': len(segment_list),
                'transcription_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'processing_time_seconds': 0,  # Will be updated
                'custom_metadata': metadata or {}
            }
            
            # Write transcript file
            self._write_transcript_file(segment_list, output_path, transcript_metadata)
            
            # Update processing time
            processing_time = time.time() - start_time
            transcript_metadata['processing_time_seconds'] = processing_time
            
            # Update stats
            self.stats['total_processed'] += 1
            self.stats['total_duration'] += info.duration
            self.stats['total_processing_time'] += processing_time
            
            logger.info(f"✅ Completed: {video_path.name} ({processing_time:.1f}s)")
            
            return {
                'success': True,
                'metadata': transcript_metadata,
                'segments': len(segment_list)
            }
            
        except Exception as e:
            error_msg = f"Failed to transcribe {video_path}: {e}"
            logger.error(error_msg)
            self.stats['failed_files'].append(str(video_path))
            
            return {
                'success': False,
                'error': error_msg,
                'file': str(video_path)
            }
    
    def _write_transcript_file(self, segments: List, output_path: Path, metadata: Dict):
        """Write transcript to file with metadata and formatting."""
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write header with metadata
            f.write("# Video Transcription\n\n")
            f.write(f"**Source File:** {metadata['source_file']}\n")
            f.write(f"**Duration:** {metadata['duration_seconds']:.2f} seconds\n")
            f.write(f"**Language:** {metadata['language']} (confidence: {metadata['language_probability']:.2f})\n")
            f.write(f"**Model:** {metadata['model_used']}\n")
            f.write(f"**Segments:** {metadata['segment_count']}\n")
            f.write(f"**Generated:** {metadata['transcription_timestamp']}\n")
            f.write(f"**File Hash:** {metadata['file_hash']}\n\n")
            
            # Add custom metadata if present
            if metadata['custom_metadata']:
                f.write("## Additional Metadata\n")
                for key, value in metadata['custom_metadata'].items():
                    f.write(f"**{key}:** {value}\n")
                f.write("\n")
            
            f.write("---\n\n")
            f.write("## Transcript\n\n")
            
            # Write timestamped segments
            for segment in segments:
                timestamp = f"[{segment.start:.2f}s → {segment.end:.2f}s]"
                text = segment.text.strip()
                f.write(f"**{timestamp}** {text}\n\n")
        
        # Also save metadata as JSON for programmatic access
        json_path = output_path.with_suffix('.json')
        with open(json_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def transcribe_cohort_batch(self, cohort_path: str) -> Dict:
        """
        Transcribe all videos in a cohort directory.
        
        Args:
            cohort_path: Path to cohort directory
            
        Returns:
            Dict with batch processing results
        """
        cohort_path = Path(cohort_path)
        video_extensions = {'.mp4', '.webm', '.avi', '.mov', '.mkv'}
        
        # Find all video files
        video_files = []
        for week_dir in cohort_path.iterdir():
            if week_dir.is_dir() and week_dir.name.startswith('week_'):
                for file_path in week_dir.iterdir():
                    if file_path.suffix.lower() in video_extensions:
                        video_files.append(file_path)
        
        logger.info(f"Found {len(video_files)} video files in {cohort_path.name}")
        
        results = []
        
        # Process files with limited parallelism
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all jobs
            future_to_file = {
                executor.submit(
                    self.transcribe_single_file,
                    str(video_file),
                    None,
                    {'cohort': cohort_path.name, 'week': video_file.parent.name}
                ): video_file for video_file in video_files
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                video_file = future_to_file[future]
                try:
                    result = future.result()
                    result['file'] = str(video_file)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Exception processing {video_file}: {e}")
                    results.append({
                        'success': False,
                        'error': str(e),
                        'file': str(video_file)
                    })
        
        # Generate batch summary
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        batch_summary = {
            'cohort': cohort_path.name,
            'total_files': len(video_files),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': len(successful) / len(video_files) if video_files else 0,
            'failed_files': [r['file'] for r in failed]
        }
        
        logger.info(f"Batch complete - {cohort_path.name}: {len(successful)}/{len(video_files)} successful")
        
        return {
            'summary': batch_summary,
            'results': results
        }
    
    def transcribe_all_cohorts(self, cohorts_base_path: str = "../cohorts") -> Dict:
        """
        Transcribe all videos across all cohorts.
        
        Args:
            cohorts_base_path: Base path containing cohort directories
            
        Returns:
            Dict with complete processing results
        """
        cohorts_path = Path(cohorts_base_path)
        cohort_dirs = [d for d in cohorts_path.iterdir() if d.is_dir() and d.name.startswith('cohort_')]
        
        logger.info(f"Processing {len(cohort_dirs)} cohorts")
        
        all_results = {}
        overall_stats = {
            'cohorts_processed': 0,
            'total_videos': 0,
            'total_successful': 0,
            'total_failed': 0,
            'start_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        for cohort_dir in sorted(cohort_dirs):
            logger.info(f"🚀 Processing {cohort_dir.name}")
            
            cohort_results = self.transcribe_cohort_batch(str(cohort_dir))
            all_results[cohort_dir.name] = cohort_results
            
            # Update overall stats
            summary = cohort_results['summary']
            overall_stats['cohorts_processed'] += 1
            overall_stats['total_videos'] += summary['total_files']
            overall_stats['total_successful'] += summary['successful']
            overall_stats['total_failed'] += summary['failed']
        
        # Final statistics
        overall_stats['end_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        overall_stats['success_rate'] = (
            overall_stats['total_successful'] / overall_stats['total_videos'] 
            if overall_stats['total_videos'] > 0 else 0
        )
        
        # Merge with transcriber stats
        overall_stats.update(self.stats)
        
        logger.info(f"🎉 All cohorts processed!")
        logger.info(f"📊 Success rate: {overall_stats['success_rate']:.1%}")
        
        return {
            'overall_stats': overall_stats,
            'cohort_results': all_results
        }
    
    def save_processing_report(self, results: Dict, output_path: str = "../logs/transcription_report.json"):
        """Save comprehensive processing report."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Processing report saved: {output_path}")

def main():
    """Main execution function."""
    # Initialize transcriber
    transcriber = BatchTranscriber(
        model_size="base",  # Good balance of speed vs accuracy
        device="cpu",      # Change to "cuda" if GPU available
        max_workers=2      # Adjust based on system resources
    )
    
    try:
        # Process all cohorts
        results = transcriber.transcribe_all_cohorts()
        
        # Save comprehensive report
        transcriber.save_processing_report(results)
        
        print("✅ Batch transcription completed!")
        print(f"📊 Processed {results['overall_stats']['total_videos']} videos")
        print(f"🎯 Success rate: {results['overall_stats']['success_rate']:.1%}")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Processing interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error during batch processing: {e}")
        raise

if __name__ == "__main__":
    main()
