#!/usr/bin/env python3
"""
WAN R2V Test - Quick test with Cloudinary URLs
Download files first, then generate video
"""

import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_wan_r2v import (
    create_video_task,
    poll_task_status,
    download_video,
    log_performance,
    encode_file_to_base64
)

# Constants
WORKSPACE_DIR = Path(__file__).parent
OUTPUT_DIR = WORKSPACE_DIR / "output"
TEST_DIR = WORKSPACE_DIR / "test"
TEST_IMAGE_URL = "https://res.cloudinary.com/dxepor8fh/image/upload/v1772366845/z-image_00231__voi138.png"
TEST_VIDEO_URL = "https://res.cloudinary.com/dxepor8fh/video/upload/v1772366719/Download_13_vblnf6.mp4"
DEFAULT_PROMPT = "Character1 เคลื่อนไหวตามวิดีโอ reference อย่างแม่นยำ แสดงท่าเต้น energy มือสร้างรูปหัวใจ, ปรบมือ, ยิ้มแย้มและ wink ให้กล้อง"
DEFAULT_DURATION = 5
DEFAULT_SIZE = "1280*720"


def ensure_directories():
    """Ensure output directories exist"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)
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
    # Ensure directories exist
    ensure_directories()
    
    # Prepare local files
    image_local = TEST_DIR / "reference_char1.jpg"
    video_local = TEST_DIR / "reference_char1.mp4"
    
    print("=" * 60)
    print("WAN R2V Test - Quick test with Cloudinary URLs")
    print("=" * 60)
    
    # Download files from Cloudinary
    print("\nDownloading reference files from Cloudinary...")
    if not download_file_from_url(TEST_IMAGE_URL, str(image_local)):
        print("❌ Failed to download image")
        return 1
    if not download_file_from_url(TEST_VIDEO_URL, str(video_local)):
        print("❌ Failed to download video")
        return 1
    
    print(f"\n✅ Downloaded files:")
    print(f"   Image: {image_local} ({image_local.stat().st_size} bytes)")
    print(f"   Video: {video_local} ({video_local.stat().st_size} bytes)")
    
    # Create video task with Base64
    print("\nCreating video generation task...")
    
    try:
        image_b64 = encode_file_to_base64(str(image_local))
        video_b64 = encode_file_to_base64(str(video_local))
        reference_urls = [image_b64, video_b64]
        
        task_result = create_video_task(
            prompt=DEFAULT_PROMPT,
            reference_urls=reference_urls,
            size=DEFAULT_SIZE,
            duration=DEFAULT_DURATION
        )
    except Exception as e:
        log_performance(f"Error preparing task: {str(e)}", "ERROR")
        print(f"Error: {str(e)}")
        return 1
    
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
    log_performance(f"Task created: {task_id}", "SUCCESS")
    print(f"\n✅ Task created: {task_id}")
    print("⏱️  Waiting for video generation (5-10 minutes expected)...")
    
    # Poll for completion
    attempts = 0
    max_polls = 60  # 10 minutes max (every 10 seconds)
    
    while attempts < max_polls:
        attempts += 1
        print(f"\nPoliing #{attempts}...")
        
        result = poll_task_status(task_id)
        
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
            error_msg = result.get("output", {}).get("message", "No details")
            log_performance(f"Task failed: {task_status} - {error_msg}", "ERROR")
            print(f"❌ Task {task_status}: {error_msg}")
            return 1
        
        elif task_status == "UNKNOWN":
            log_performance("Task expired or not found", "ERROR")
            return 1
        
        if attempts < max_polls:
            log_performance(f"Waiting 10s for next poll...")
            time.sleep(10)
    
    log_performance("Max polling reached", "WARNING")
    print("⏰ Max polling time reached. Task may still be running.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
