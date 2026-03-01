#!/usr/bin/env python3
"""
WAN R2V Cron Wrapper - Generate video from URL and poll status every 2 minutes
"""

import argparse
import os
import sys
import time
import json
import urllib.request
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_wan_r2v import (
    create_video_task,
    poll_task_status,
    download_video,
    log_performance
)

# Constants
WORKSPACE_DIR = Path(__file__).parent
OUTPUT_DIR = WORKSPACE_DIR / "output"
CRON_DIR = WORKSPACE_DIR / "cron_status"
DEFAULT_DURATION = 5
DEFAULT_SIZE = "1280*720"


def ensure_directories():
    """Ensure output directories exist"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CRON_DIR.mkdir(parents=True, exist_ok=True)
    (WORKSPACE_DIR / "logs").mkdir(parents=True, exist_ok=True)


def download_file_from_url(url: str, output_path: str) -> bool:
    """Download file from URL"""
    try:
        log_performance(f"Downloading from URL: {url[:50]}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mari/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        log_performance(f"Downloaded to: {output_path}", "SUCCESS")
        return True
    except Exception as e:
        log_performance(f"Download failed: {str(e)}", "ERROR")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="WAN R2V Cron - Generate video with URL inputs and poll every 2 minutes"
    )
    parser.add_argument(
        "--image", "-i",
        required=True,
        help="Reference image URL (jpg/png)"
    )
    parser.add_argument(
        "--video", "-v",
        required=True,
        help="Reference video URL (mp4)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Video prompt describing the action"
    )
    parser.add_argument(
        "--interval", "-t",
        type=int,
        default=120,
        help="Polling interval in seconds (default: 120 / 2 minutes)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=DEFAULT_DURATION,
        choices=[5, 10],
        help="Video duration in seconds (default: 5)"
    )
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    # Prepare local files from URLs
    image_local = OUTPUT_DIR / "ref_image.jpg"
    video_local = OUTPUT_DIR / "ref_video.mp4"
    
    print("Downloading reference files from Cloudinary...")
    if not download_file_from_url(args.image, str(image_local)):
        print("❌ Failed to download image")
        return 1
    if not download_file_from_url(args.video, str(video_local)):
        print("❌ Failed to download video")
        return 1
    
    # Create video task
    print("Creating video generation task...")
    task_result = create_video_task(
        prompt=args.prompt,
        reference_urls=[
            f"data:image/jpeg;base64,{open(image_local, 'rb').read().hex()}",  # Using hex for URL
            f"data:video/mp4;base64,{open(video_local, 'rb').read().hex()}"
        ],
        size=DEFAULT_SIZE,
        duration=args.duration
    )
    
    # Check for API key error
    if task_result.get("error") == "API_KEY_NOT_FOUND":
        print("⚠️  API Key not found! Using mockup mode...")
        print("   (This is a demo - no real video will be generated)")
        
        import shutil
        shutil.copy2(str(video_local), str(OUTPUT_DIR / "output_mockup.mp4"))
        print(f"✅ Mockup saved to: {OUTPUT_DIR / 'output_mockup.mp4'}")
        return 0
    
    if "error" in task_result:
        log_performance(f"Task creation failed: {task_result['error']}", "ERROR")
        print(f"Failed to create task: {task_result.get('message', task_result['error'])}")
        return 1
    
    task_id = task_result["output"]["task_id"]
    status_file = CRON_DIR / f"task_{task_id}.json"
    
    # Save task status
    status_data = {
        "task_id": task_id,
        "image_url": args.image,
        "video_url": args.video,
        "prompt": args.prompt,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "attempts": 0
    }
    
    with open(status_file, "w") as f:
        json.dump(status_data, f, indent=2)
    
    log_performance(f"Task created: {task_id}", "SUCCESS")
    print(f"✅ Task created: {task_id}")
    print(f"📊 Status file: {status_file}")
    print(f"⏱️  Polling every {args.interval} seconds...")
    
    # Poll for completion
    attempts = 0
    max_polls = 60  # 10 minutes max
    
    while attempts < max_polls:
        attempts += 1
        print(f"\nPoliing #{attempts}...")
        
        result = poll_task_status(task_id)
        
        # Update status file
        with open(status_file, "w") as f:
            json.dump(result, f, indent=2)
        
        if "error" in result:
            log_performance(f"Generation failed: {result['error']}", "ERROR")
            print(f"❌ Generation failed: {result['error']}")
            return 1
        
        task_status = result.get("output", {}).get("task_status", "UNKNOWN")
        
        if task_status == "SUCCEEDED":
            video_url = result["output"].get("video_url")
            log_performance(f"Video generated: {video_url[:50]}...", "SUCCESS")
            print("✅ Video generation completed!")
            
            # Download video
            output_path = OUTPUT_DIR / f"output_r2v_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            if download_video(video_url, str(output_path)):
                print(f"✅ Video saved: {output_path}")
                print("🎉 Task completed successfully!")
                return 0
            else:
                log_performance("Failed to download video", "ERROR")
                print("❌ Failed to download generated video")
                return 1
        
        elif task_status in ["FAILED", "CANCELED"]:
            log_performance(f"Task failed: {task_status}", "ERROR")
            print(f"❌ Task {task_status}")
            return 1
        
        elif task_status == "UNKNOWN":
            log_performance("Task expired or not found", "ERROR")
            return 1
        
        if attempts < max_polls:
            log_performance(f"Waiting {args.interval}s for next poll...")
            time.sleep(args.interval)
    
    log_performance("Max polling reached", "WARNING")
    print("⏰ Max polling time reached. Task may still be running.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
