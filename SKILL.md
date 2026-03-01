# WAN R2V Skill - /c/c-2/

## 📌 Overview

This skill uses **Alibaba Cloud Model Studio's WAN 2.6 R2V** model to generate videos using **reference images and videos from any URL** (including Cloudinary, OSS, etc.).

✅ Supports `wan2.6-r2v` (high quality) & `wan2.6-r2v-flash` (fast)
✅ Accepts **public URLs directly** (no Base64 needed!)
✅ Portrait mode support (720x1280)
✅ Chinese/English prompts

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd ~/.openclaw/workspace-mari/Mari-Labs/wan-r2v
pip install -r requirements.txt
```

### 2. Set API Key
Edit `~/.openclaw/.env`:
```env
WAN_API_KEY=your_alibaba_cloud_api_key_here
# Optional: WAN_MODEL=wan2.6-r2v  (default) or wan2.6-r2v-flash
```

### 3. Run
```bash
python3 wan_r2v_cloudinary.py \
  --image "https://example.com/your_image.jpg" \
  --video "https://example.com/your_video.mp4" \
  --prompt "Character1 dancing like Character2"
```

Or use direct script:
```bash
python3 wan_r2v_cloudinary.py
```
(Uses default Cloudinary URLs from script)

---

## 📺 Output

| Item | Location |
|------|----------|
| Video | `output/output_r2v_[timestamp].mp4` |
| Status | `cron_status/task_[task_id].json` |
| Logs | `logs/performance_cloudinary_[date].log` |

---

## ⚙️ API Details

| Setting | Value |
|---------|-------|
| Model (default) | `wan2.6-r2v` |
| Model (flash) | `wan2.6-r2v-flash` |
| Default Size | `720*1280` (Portrait) |
| Default Size (landscape) | `1280*720` |
| Duration | 5 seconds |
| Audio | Enabled (from reference video) |

---

## 🌐 URL Support

✅ **Public URLs work directly** (Cloudinary, OSS, etc.)
❌ **No Base64 encoding needed**

Example:
```json
"reference_urls": [
  "https://res.cloudinary.com/xxx/image.jpg",
  "https://res.cloudinary.com/xxx/video.mp4"
]
```

---

## 🇹🇭 Thai Prompts + 🇨🇳 Chinese Prompts

Both languages work! Example:

**Thai:**  
"Character1 เคลื่อนไหวตามวิดีโอ reference อย่างแม่นยำ แสดงท่าเต้น energy มือสร้างรูปหัวใจ"

**Chinese:**  
"Character1 和 Character2 在日本夜晚酒吧里一起跳舞，动作协调一致，充满活力"

---

## 📁 File Structure

```
wan-r2v/
├── SKILL.md                    # This file
├── README.md                   # Quick start guide
├── INSTALL.md                  # Installation steps
├── CRON.md                     # Cron job setup
│
├── wan_r2v.py                  # CLI with Base64 (for local files)
├── wan_r2v_cron.py             # Cron wrapper
├── wan_r2v_test.py             # Quick test with download
├── wan_r2v_cloudinary.py       # Main script (URL-based)
│
├── api_wan_r2v.py              # API client library
├── requirements.txt            # Dependencies
│
├── output/                     # Generated videos (gitignored)
├── cron_status/                # Task status files (gitignored)
└── logs/                       # Performance logs (gitignored)
```

---

## 🔐 Security Rules

1. ❌ **Never commit** `api_key.txt`, `.env`, images, videos
2. ✅ Always read API keys from `~/.openclaw/.env`
3. ✅ Mask keys in logs: `sk-81b2c...1d66`
4. ✅ Gitignore: `output/`, `cron_status/`, `logs/`, `*.env`

---

## 📝 Memory Log

**Created:** 2026-03-01  
**Status:** ✅ Production-ready  
**Tested:** Cloudinary URLs + Chinese prompts  
**Last update:** 2026-03-01

---

*WAN R2V Skill by Mari for Khun Salmon - Teasing Mentor & Technical Partner*
