#!/usr/bin/env python3
"""
Fast transcription script using faster-whisper
Optimized for CPU-only environments
"""

from faster_whisper import WhisperModel
import time
import os

def transcribe_video(video_file="harvard_scalability_lecture.webm", output_file=None):
    # Set default output file if not provided
    if output_file is None:
        base_name = video_file.split('.')[0]
        output_file = f"{base_name}_transcript.txt"
    
    print(f"🎥 Starting transcription of: {video_file}")
    print(f"📝 Output will be saved to: {output_file}")
    
    # Initialize the model with CPU optimizations
    # Using 'base' model for good balance of speed vs accuracy
    # You can change to 'tiny' for faster speed or 'small' for better accuracy
    print("🔄 Loading Whisper model (base)...")
    
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8",  # Use int8 for faster CPU inference
        cpu_threads=0,  # Use all available CPU threads
        num_workers=1   # Single worker for stability
    )
    
    print("✅ Model loaded successfully!")
    print("🚀 Starting transcription... (this may take a few minutes)")
    
    start_time = time.time()
    
    # Transcribe with optimizations
    segments, info = model.transcribe(
        video_file,
        beam_size=1,  # Faster beam search
        language="en",  # Assuming English, remove if you want auto-detection
        condition_on_previous_text=False,  # Faster processing
        vad_filter=True,  # Voice activity detection to skip silence
        vad_parameters=dict(min_silence_duration_ms=500)  # Skip 500ms+ silence
    )
    
    print(f"📊 Detected language: {info.language} (probability: {info.language_probability:.2f})")
    print(f"⏱️  Estimated duration: {info.duration:.2f} seconds")
    
    # Write transcription to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Video Transcription\n")
        f.write(f"Source: {video_file}\n")
        f.write(f"Generated using faster-whisper\n")
        f.write(f"Language: {info.language} (probability: {info.language_probability:.2f})\n")
        f.write(f"Duration: {info.duration:.2f} seconds\n")
        f.write(f"Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        print("📝 Writing transcription...")
        segment_count = 0
        for segment in segments:
            timestamp = f"[{segment.start:.2f}s -> {segment.end:.2f}s]"
            text = segment.text.strip()
            
            # Write to file
            f.write(f"{timestamp} {text}\n")
            
            # Print progress every 10 segments
            segment_count += 1
            if segment_count % 10 == 0:
                print(f"  ✓ Processed {segment_count} segments... ({segment.end:.1f}s)")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n🎉 Transcription completed!")
    print(f"⏱️  Processing time: {processing_time:.2f} seconds")
    print(f"📁 Output saved to: {output_file}")
    print(f"📊 Total segments: {segment_count}")
    
    if info.duration > 0:
        speed_ratio = info.duration / processing_time
        print(f"🚀 Speed: {speed_ratio:.2f}x realtime")

if __name__ == "__main__":
    import sys
    
    # Get video file from command line argument or use default
    if len(sys.argv) > 1:
        video_file = sys.argv[1]
    else:
        video_file = "harvard_scalability_lecture.webm"
    
    # Check if video file exists
    if not os.path.exists(video_file):
        print(f"❌ Error: {video_file} not found in current directory")
        print("   Usage: python transcribe_lecture.py [video_file]")
        print("   Make sure you're running this script from the transcription folder")
        exit(1)
    
    try:
        transcribe_video(video_file)
    except KeyboardInterrupt:
        print("\n🛑 Transcription interrupted by user")
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        print("   You might want to try a smaller model like 'tiny' if you're running out of memory")
