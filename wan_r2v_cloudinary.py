#!/usr/bin/env python3
"""
WAN R2V Cloudinary Test - Use Cloudinary URLs directly (no download needed)
Prompt in Chinese: Character1 moves and dances like Character2
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ENV_PATH = os.path.expanduser("~/.openclaw/.env")
load_dotenv(ENV_PATH)

# Constants
API_ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
DEFAULT_MODEL = "wan2.6-r2v"  # Default: high quality R2V
MODEL_NAME = os.getenv("WAN_MODEL", DEFAULT_MODEL)
WAN_API_KEY = os.getenv("WAN_API_KEY")

# Input URLs from Cloudinary
CLOUDINARY_IMAGE_URL = "https://res.cloudinary.com/dxepor8fh/image/upload/v1772366845/z-image_00231__voi138.png"
CLOUDINARY_VIDEO_URL = "https://res.cloudinary.com/dxepor8fh/video/upload/v1772366719/Download_13_vblnf6.mp4"

# Chinese prompt for Character1 and Character2 dancing together in Japanese night bar
PROMPT_CN = "Character1 和 Character2 在日本夜晚酒吧里一起跳舞，动作协调一致，充满活力。酒吧内部灯光昏暗，霓虹灯闪烁，背景有吧台和酒瓶，氛围浪漫迷人，两人随着音乐节奏律动，笑容灿烂"

# Output video settings
OUTPUT_DIR = Path(__file__).parent / "output"
LOGS_DIR = Path(__file__).parent / "logs"
DEFAULT_SIZE = "720*1280"  # Portrait mode


def ensure_directories():
    """Ensure output directories exist"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def log_performance(message: str, status: str = "INFO"):
    """Log performance to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOGS_DIR / f"performance_cloudinary_{datetime.now().strftime('%Y-%m-%d')}.log"
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {status}: {message}\n")


def create_video_task():
    """Create video task with Cloudinary URLs"""
    if not WAN_API_KEY:
        log_performance("API Key not found!", "ERROR")
        print("❌ WAN_API_KEY not found in ~/.openclaw/.env")
        return None
    
    # Use Cloudinary URLs directly (no Base64 encoding needed)
    reference_urls = [
        CLOUDINARY_IMAGE_URL,
        CLOUDINARY_VIDEO_URL
    ]
    
    headers = {
        "X-DashScope-Async": "enable",
        "Authorization": f"Bearer {WAN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "input": {
            "prompt": PROMPT_CN,
            "reference_urls": reference_urls
        },
        "parameters": {
            "size": DEFAULT_SIZE,
            "duration": "5",
            "audio": True,
            "shot_type": "multi",
            "watermark": False
        }
    }
    
    log_performance(f"Creating task with Cloudinary URLs...")
    log_performance(f"Image: {CLOUDINARY_IMAGE_URL[:50]}...")
    log_performance(f"Video: {CLOUDINARY_VIDEO_URL[:50]}...")
    log_performance(f"Prompt (CN): {PROMPT_CN[:50]}...")
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            log_performance(f"✅ Task created: {result['output']['task_id']}", "SUCCESS")
            return result
        else:
            log_performance(f"❌ API Error: {result.get('code', 'UNKNOWN')} - {result.get('message', '')}", "ERROR")
            return result
            
    except Exception as e:
        log_performance(f"Request exception: {str(e)}", "ERROR")
        return {"error": str(e)}


def poll_task_status(task_id: str) -> dict:
    """Poll task status"""
    status_url = f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {WAN_API_KEY}"
    }
    
    max_polls = 60
    poll_interval = 10
    
    log_performance(f"Polling task status for: {task_id}")
    
    for attempt in range(max_polls):
        try:
            response = requests.get(status_url, headers=headers, timeout=30)
            result = response.json()
            
            task_status = result.get("output", {}).get("task_status", "UNKNOWN")
            log_performance(f"Poll #{attempt+1}: status={task_status}")
            
            if task_status == "SUCCEEDED":
                video_url = result.get("output", {}).get("video_url")
                log_performance("✅ Task completed!", "SUCCESS")
                return result
                
            elif task_status in ["FAILED", "CANCELED"]:
                log_performance(f"❌ Task {task_status}", "ERROR")
                return result
            
            if attempt < max_polls - 1:
                log_performance(f"Waiting {poll_interval}s...")
                import time
                time.sleep(poll_interval)
                
        except Exception as e:
            log_performance(f"Polling exception: {str(e)}", "ERROR")
            continue
    
    log_performance("Max polls reached", "WARNING")
    return {"error": "TIMEOUT"}


def main():
    print("=" * 60)
    print("WAN R2V - Cloudinary URLs Direct Test (Chinese Prompt)")
    print("=" * 60)
    print(f"\nModel: {MODEL_NAME}")
    print(f"Size: {DEFAULT_SIZE} (Portrait mode)")
    print(f"\nCloudinary URLs:")
    print(f"  Image: {CLOUDINARY_IMAGE_URL}")
    print(f"  Video: {CLOUDINARY_VIDEO_URL}")
    print(f"\nPrompt (Chinese):")
    print(f"  {PROMPT_CN}")
    
    # Ensure directories exist
    ensure_directories()
    
    # Create task
    print("\nCreating video generation task...")
    task_result = create_video_task()
    
    if task_result is None:
        return 1
    
    if "error" in task_result:
        print(f"❌ Failed: {task_result.get('message', task_result['error'])}")
        return 1
    
    task_id = task_result["output"]["task_id"]
    print(f"\n✅ Task created: {task_id}")
    print("⏱️  Waiting for video generation (5-10 minutes)...")
    
    # Poll for completion
    result = poll_task_status(task_id)
    
    if "error" in result:
        print(f"❌ Generation failed: {result['error']}")
        return 1
    
    task_status = result.get("output", {}).get("task_status", "UNKNOWN")
    
    if task_status == "SUCCEEDED":
        video_url = result["output"].get("video_url")
        log_performance(f"Video generated: {video_url[:50]}...", "SUCCESS")
        print("✅ Video generation completed!")
        
        # Download video
        import urllib.request
        output_path = OUTPUT_DIR / f"output_r2v_cloudinary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        print(f"\nDownloading video to: {output_path}")
        try:
            req = urllib.request.Request(video_url, headers={'User-Agent': 'Mari/1.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
            log_performance(f"Video saved: {output_path}", "SUCCESS")
            print(f"✅ Video saved: {output_path} ({output_path.stat().st_size} bytes)")
            
            # Send to Telegram
            print("\n📞 Sending video to Telegram...")
            return 0
            
        except Exception as e:
            log_performance(f"Download failed: {str(e)}", "ERROR")
            print(f"❌ Failed to download: {str(e)}")
            return 1
    
    elif task_status == "FAILED":
        error_msg = result.get("output", {}).get("message", "No details")
        log_performance(f"Task failed: {error_msg}", "ERROR")
        print(f"❌ Failed: {error_msg}")
        return 1
    
    else:
        log_performance(f"Unknown status: {task_status}", "WARNING")
        print(f"Unknown status: {task_status}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
