#!/usr/bin/env python3
"""
S3-compatible batch transcription system using faster-whisper.
Processes videos directly from S3 URLs without downloading.
"""

import os
import json
import time
import logging
import tempfile
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from faster_whisper import WhisperModel
import hashlib
import boto3
from botocore.config import Config
from botocore import UNSIGNED
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/s3_transcription.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class S3BatchTranscriber:
    """S3-compatible batch transcription system for cohort recordings."""
    
    def __init__(self, 
                 model_size: str = "base",
                 device: str = "cpu",
                 compute_type: str = "int8",
                 max_workers: int = 2,
                 use_temp_files: bool = True):
        """
        Initialize the S3 batch transcriber.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Processing device (cpu, cuda)
            compute_type: Computation type for optimization
            max_workers: Maximum parallel transcription workers
            use_temp_files: Whether to use temp files for S3 videos
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.max_workers = max_workers
        self.use_temp_files = use_temp_files
        self.model = None
        self.s3_client = None
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
    
    def initialize_s3_client(self, aws_access_key: str = None, aws_secret_key: str = None, region: str = 'us-east-1'):
        """Initialize S3 client for authenticated or public bucket access."""
        try:
            if aws_access_key and aws_secret_key:
                # Authenticated access
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region
                )
                logger.info("✅ S3 client initialized with credentials")
            else:
                # Public bucket access
                self.s3_client = boto3.client(
                    's3',
                    config=Config(signature_version=UNSIGNED),
                    region_name=region
                )
                logger.info("✅ S3 client initialized for public access")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise
    
    def download_from_s3(self, s3_url: str, temp_dir: str = None) -> str:
        """
        Download video from S3 URL to temporary file.
        
        Args:
            s3_url: S3 URL (s3://bucket/key or https://bucket.s3.amazonaws.com/key)
            temp_dir: Temporary directory for downloads
            
        Returns:
            Path to downloaded temporary file
        """
        try:
            # Parse S3 URL
            if s3_url.startswith('s3://'):
                # s3://bucket/key format
                parts = s3_url[5:].split('/', 1)
                bucket = parts[0]
                key = parts[1] if len(parts) > 1 else ''
            elif 's3.amazonaws.com' in s3_url or 's3-' in s3_url:
                # HTTPS URL format
                # Extract bucket and key from URL
                if '.s3.amazonaws.com/' in s3_url:
                    parts = s3_url.split('.s3.amazonaws.com/')
                    bucket = parts[0].split('/')[-1]
                    key = parts[1]
                elif '.s3-' in s3_url:  # Regional endpoint
                    parts = s3_url.split('.s3-')[1].split('/', 1)
                    bucket = s3_url.split('//')[1].split('.')[0]
                    key = parts[1] if len(parts) > 1 else ''
                else:
                    # Direct HTTPS download for public URLs
                    return self.download_from_https(s3_url, temp_dir)
            else:
                # Assume it's a direct HTTPS URL
                return self.download_from_https(s3_url, temp_dir)
            
            # Create temporary file
            if not temp_dir:
                temp_dir = tempfile.gettempdir()
            
            file_extension = Path(key).suffix or '.mp4'
            temp_file = tempfile.NamedTemporaryFile(
                suffix=file_extension,
                dir=temp_dir,
                delete=False
            )
            temp_path = temp_file.name
            temp_file.close()
            
            # Download from S3
            if self.s3_client:
                logger.info(f"Downloading from S3: s3://{bucket}/{key}")
                self.s3_client.download_file(bucket, key, temp_path)
            else:
                # Fallback to HTTPS download
                https_url = f"https://{bucket}.s3.amazonaws.com/{key}"
                return self.download_from_https(https_url, temp_dir)
            
            logger.info(f"✅ Downloaded to: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Failed to download from S3: {e}")
            raise
    
    def download_from_https(self, url: str, temp_dir: str = None) -> str:
        """Download video from HTTPS URL to temporary file."""
        try:
            if not temp_dir:
                temp_dir = tempfile.gettempdir()
            
            # Get file extension from URL
            file_extension = Path(url.split('?')[0]).suffix or '.mp4'
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=file_extension,
                dir=temp_dir,
                delete=False
            )
            temp_path = temp_file.name
            
            logger.info(f"Downloading from URL: {url}")
            
            # Download with progress
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if downloaded % (1024 * 1024 * 10) == 0:  # Log every 10MB
                                logger.info(f"Download progress: {progress:.1f}%")
            
            logger.info(f"✅ Downloaded to: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Failed to download from URL: {e}")
            raise
    
    def transcribe_from_url(self, 
                           url: str,
                           output_path: str = None,
                           metadata: Dict = None,
                           cleanup: bool = True) -> Dict:
        """
        Transcribe a video from S3 or HTTPS URL.
        
        Args:
            url: S3 or HTTPS URL to video
            output_path: Output path for transcript
            metadata: Additional metadata to include
            cleanup: Whether to delete temp file after transcription
            
        Returns:
            Dict with transcription results and metadata
        """
        if not self.model:
            self.load_model()
        
        temp_file = None
        start_time = time.time()
        
        try:
            # Download video to temp file
            logger.info(f"Processing: {url}")
            temp_file = self.download_from_s3(url) if url.startswith('s3://') else self.download_from_https(url)
            
            # Get file info
            file_size = os.path.getsize(temp_file) / (1024 * 1024)  # MB
            logger.info(f"File size: {file_size:.2f} MB")
            
            # Transcribe
            logger.info("Starting transcription...")
            segments, info = self.model.transcribe(
                temp_file,
                beam_size=5,
                language="en",
                condition_on_previous_text=True,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    threshold=0.6,
                    speech_pad_ms=400
                )
            )
            
            # Process segments
            transcript_lines = []
            transcript_json = []
            
            for segment in segments:
                start = segment.start
                end = segment.end
                text = segment.text.strip()
                
                # Format timestamp
                timestamp = f"[{self._format_timestamp(start)} - {self._format_timestamp(end)}]"
                transcript_lines.append(f"{timestamp} {text}")
                
                # JSON format
                transcript_json.append({
                    "start": start,
                    "end": end,
                    "text": text
                })
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare result
            result = {
                "source_url": url,
                "duration": info.duration if info else 0,
                "language": info.language if info else "en",
                "processing_time": processing_time,
                "segments_count": len(transcript_json),
                "transcript_text": "\n".join(transcript_lines),
                "transcript_segments": transcript_json,
                "metadata": metadata or {},
                "file_size_mb": file_size,
                "model_used": self.model_size,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save output if path provided
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save text transcript
                txt_path = output_path.with_suffix('.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(result['transcript_text'])
                
                # Save JSON transcript
                json_path = output_path.with_suffix('.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                logger.info(f"✅ Saved transcript to: {txt_path}")
                logger.info(f"✅ Saved metadata to: {json_path}")
            
            # Update stats
            self.stats['total_processed'] += 1
            self.stats['total_duration'] += result['duration']
            self.stats['total_processing_time'] += processing_time
            
            logger.info(f"✅ Transcription complete in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            logger.error(f"Transcription failed for {url}: {e}")
            self.stats['failed_files'].append({"url": url, "error": str(e)})
            raise
            
        finally:
            # Cleanup temp file
            if cleanup and temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logger.info(f"Cleaned up temp file: {temp_file}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file: {e}")
    
    def process_manifest(self, manifest_path: str):
        """
        Process videos from a manifest file containing S3 URLs.
        
        Manifest format:
        {
            "videos": [
                {
                    "url": "s3://bucket/path/to/video.mp4",
                    "cohort": 3,
                    "week": 1,
                    "lesson": 1,
                    "output_path": "cohorts/cohort_3/week_01/lesson_1"
                }
            ]
        }
        """
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            videos = manifest.get('videos', [])
            logger.info(f"Processing {len(videos)} videos from manifest")
            
            # Process videos with thread pool
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                
                for video in videos:
                    url = video.get('url')
                    output_path = video.get('output_path')
                    metadata = {
                        'cohort': video.get('cohort'),
                        'week': video.get('week'),
                        'lesson': video.get('lesson'),
                        'title': video.get('title', ''),
                        'date': video.get('date', '')
                    }
                    
                    future = executor.submit(
                        self.transcribe_from_url,
                        url,
                        output_path,
                        metadata
                    )
                    futures[future] = video
                
                # Process results
                for future in as_completed(futures):
                    video = futures[future]
                    try:
                        result = future.result()
                        logger.info(f"✅ Completed: {video.get('url')}")
                    except Exception as e:
                        logger.error(f"❌ Failed: {video.get('url')} - {e}")
            
            # Print summary
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Failed to process manifest: {e}")
            raise
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds to MM:SS or HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def print_summary(self):
        """Print processing summary."""
        print("\n" + "="*50)
        print("TRANSCRIPTION SUMMARY")
        print("="*50)
        print(f"Total videos processed: {self.stats['total_processed']}")
        print(f"Total duration: {self.stats['total_duration']:.2f} seconds")
        print(f"Total processing time: {self.stats['total_processing_time']:.2f} seconds")
        
        if self.stats['total_processed'] > 0:
            avg_time = self.stats['total_processing_time'] / self.stats['total_processed']
            speed_ratio = self.stats['total_duration'] / self.stats['total_processing_time']
            print(f"Average processing time: {avg_time:.2f} seconds per video")
            print(f"Processing speed: {speed_ratio:.2f}x realtime")
        
        if self.stats['failed_files']:
            print(f"\n❌ Failed files: {len(self.stats['failed_files'])}")
            for failed in self.stats['failed_files']:
                print(f"  - {failed['url']}: {failed['error']}")


def main():
    """Main entry point for S3 batch transcription."""
    import argparse
    
    parser = argparse.ArgumentParser(description='S3 Batch Video Transcription')
    parser.add_argument('--manifest', type=str, help='Path to manifest JSON file')
    parser.add_argument('--url', type=str, help='Single S3/HTTPS URL to transcribe')
    parser.add_argument('--output', type=str, help='Output path for transcripts')
    parser.add_argument('--model', type=str, default='base', help='Whisper model size')
    parser.add_argument('--device', type=str, default='cpu', help='Device (cpu/cuda)')
    parser.add_argument('--workers', type=int, default=2, help='Parallel workers')
    parser.add_argument('--aws-key', type=str, help='AWS Access Key (optional)')
    parser.add_argument('--aws-secret', type=str, help='AWS Secret Key (optional)')
    
    args = parser.parse_args()
    
    # Initialize transcriber
    transcriber = S3BatchTranscriber(
        model_size=args.model,
        device=args.device,
        max_workers=args.workers
    )
    
    # Initialize S3 client if credentials provided
    if args.aws_key and args.aws_secret:
        transcriber.initialize_s3_client(args.aws_key, args.aws_secret)
    
    # Process based on input
    if args.manifest:
        transcriber.process_manifest(args.manifest)
    elif args.url:
        result = transcriber.transcribe_from_url(
            args.url,
            args.output
        )
        print(f"✅ Transcription complete!")
        print(f"Duration: {result['duration']:.2f} seconds")
        print(f"Segments: {result['segments_count']}")
    else:
        print("Please provide either --manifest or --url")
        parser.print_help()


if __name__ == "__main__":
    main()