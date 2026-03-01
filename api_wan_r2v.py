# WAN R2V Skill - API Client

import base64
import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from ~/.openclaw/.env
ENV_PATH = os.path.expanduser("~/.openclaw/.env")
load_dotenv(ENV_PATH)

# Constants
API_ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
MODEL_NAME = "wan2.6-r2v-flash"
WAN_API_KEY = os.getenv("WAN_API_KEY")


def log_performance(message: str, status: str = "INFO"):
    """Log performance to file (without exposing API keys)"""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"performance_{datetime.now().strftime('%Y-%m-%d')}.log")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {status}: {message}\n")


def encode_file_to_base64(file_path: str) -> str:
    """Encode file to Base64 data URI"""
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"
    
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"


def create_video_task(prompt: str, reference_urls: list, size: str = "1280*720", 
                      duration: int = 5) -> dict:
    """Create a video generation task using Alibaba Cloud R2V API"""
    if not WAN_API_KEY:
        return {"error": "API_KEY_NOT_FOUND", "message": "WAN_API_KEY not found in ~/.openclaw/.env"}
    
    headers = {
        "X-DashScope-Async": "enable",
        "Authorization": f"Bearer {WAN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "input": {
            "prompt": prompt,
            "reference_urls": reference_urls
        },
        "parameters": {
            "size": size,
            "duration": duration,
            "audio": True,
            "shot_type": "multi",
            "watermark": False
        }
    }
    
    log_performance(f"Creating task with prompt: '{prompt[:50]}...'")
    
    try:
        response = requests.post(API_ENDPOINT, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        if response.status_code == 200:
            log_performance(f"Task created: {result['output']['task_id']}", "SUCCESS")
            return result
        else:
            log_performance(f"API Error: {result.get('code', 'UNKNOWN')} - {result.get('message', '')}", "ERROR")
            return result
            
    except Exception as e:
        log_performance(f"Request exception: {str(e)}", "ERROR")
        return {"error": str(e)}


def poll_task_status(task_id: str) -> dict:
    """Poll task status and return result when complete"""
    # Correct status endpoint for Alibaba Cloud
    status_url = f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}"
    
    headers = {
        "Authorization": f"Bearer {WAN_API_KEY}"
    }
    
    max_polls = 60  # 60 attempts * 10s = ~10 minutes
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
                log_performance("Task completed successfully!", "SUCCESS")
                return result
                
            elif task_status in ["FAILED", "CANCELED"]:
                log_performance(f"Task failed with status: {task_status}", "ERROR")
                return result
                
            elif task_status == "UNKNOWN":
                log_performance("Task not found or expired", "ERROR")
                return result
            
            time.sleep(poll_interval)
            
        except Exception as e:
            log_performance(f"Polling exception: {str(e)}", "ERROR")
            continue
    
    log_performance("Max polls reached, task may still be running", "WARNING")
    return {"error": "TIMEOUT"}


def download_video(video_url: str, output_path: str) -> bool:
    """Download generated video from URL"""
    try:
        log_performance(f"Downloading video to: {output_path}")
        
        # Note: video_url expires in 24 hours, download immediately
        response = requests.get(video_url, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            log_performance(f"Video saved: {output_path}", "SUCCESS")
            return True
        else:
            log_performance(f"Download failed: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log_performance(f"Download exception: {str(e)}", "ERROR")
        return False


def generate_video_with_mockup(prompt: str, output_path: str) -> str:
    """Mockup mode when no API key available"""
    import subprocess
    import shutil
    
    # This is a placeholder for mockup implementation
    # In real implementation, you'd copy reference video and add overlay
    
    log_performance("Using mockup mode (no API key)", "WARNING")
    
    # Return placeholder path (will be replaced in main script)
    return output_path


def main():
    """Test function"""
    print("WAN R2V API Client")
    print("=" * 40)
    print(f"API Endpoint: {API_ENDPOINT}")
    print(f"Model: {MODEL_NAME}")
    print(f"API Key configured: {'YES' if WAN_API_KEY else 'NO'}")
    print(f"Mockup mode: {'ENABLED' if not WAN_API_KEY else 'DISABLED'}")
    print("=" * 40)
    
    if not WAN_API_KEY:
        print("\n⚠️  No WAN_API_KEY found in ~/.openclaw/.env")
        print("   Video generation will fail or use mockup mode.")
    else:
        print("\n✅ API key loaded successfully")
        # Mask key for display
        masked_key = WAN_API_KEY[:8] + "..." + WAN_API_KEY[-4:]
        print(f"   Key preview: {masked_key}")


if __name__ == "__main__":
    main()
