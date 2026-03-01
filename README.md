# 📝 WAN R2V Skill - README

> **WAN-Ref2Video Skill** - Generate videos using reference images/videos via Alibaba Cloud's WAN 2.6 R2V model

---

## 🎯 Quick Start

### Install
```bash
cd ~/.openclaw/workspace-mari/Mari-Labs/wan-r2v
pip install -r requirements.txt
```

### Set API Key
Add to `~/.openclaw/.env`:
```env
WAN_API_KEY=your_api_key_here
```

### Run (Default Cloudinary URLs)
```bash
python3 wan_r2v_cloudinary.py
```

### Run (Custom URLs)
```bash
python3 wan_r2v_cloudinary.py \
  --image "https://example.com/image.jpg" \
  --video "https://example.com/video.mp4" \
  --prompt "Character1 dancing like Character2"
```

---

## 📺 Output

- **Video:** `output/output_r2v_[timestamp].mp4`
- **Status:** `cron_status/task_[task_id].json`
- **Logs:** `logs/performance_cloudinary_[date].log`

---

## ⚙️ Features

✅ **Cloudinary URLs supported directly** (no download needed!)
✅ **Portrait mode** (`720*1280`) + Landscape mode (`1280*720`)
✅ **WAN 2.6 R2V (quality)** or **R2V-Flash (fast)**
✅ **Chinese/English prompts**
✅ **5-second videos** with audio preserved
✅ **Auto-sends to Telegram**

---

## 📁 Scripts

| File | Purpose |
|------|---------|
| `wan_r2v_cloudinary.py` | **Main script** - Uses Cloudinary URLs directly |
| `wan_r2v.py` | CLI with Base64 (for local files) |
| `wan_r2v_test.py` | Quick test with download |
| `wan_r2v_cron.py` | Cron wrapper with polling |

---

## 🔐 Security

**.gitignore includes:**
```
output/
cron_status/
logs/
*.env
.env.*
```

❌ **Never commit:**
- Images
- Videos  
- `.env` files
- API keys

---

## 📝 Documentation

- **[SKILL.md](SKILL.md)** - Full technical documentation
- **[CRON.md](CRON.md)** - Cron job setup guide
- **[INSTALL.md](INSTALL.md)** - Installation steps

---

## 🌐 URL Format

```json
"reference_urls": [
  "https://res.cloudinary.com/xxx/image.jpg",
  "https://res.cloudinary.com/xxx/video.mp4"
]
```

✅ Works with: Cloudinary, Alibaba OSS, any public URL
❌ No Base64 needed!

---

## 💡 Example Prompt (Chinese)

```txt
Character1 和 Character2 在日本夜晚酒吧里一起跳舞，动作协调一致，充满活力。
酒吧内部灯光昏暗，霓虹灯闪烁，背景有吧台和酒瓶，
氛围浪漫迷人，两人随着音乐节奏律动，笑容灿烂
```

---

## 🐛 Troubleshooting

**Error:** `WAN_API_KEY not found`  
→ Add to `~/.openclaw/.env`

**Error:** `403 Forbidden`  
→ Check API key permissions

**Video not generating?**  
→ Check `logs/performance_cloudinary_[date].log`

---

## 📚 Repository

**GitHub:** `WAN-Ref2Video`  
**Created:** 2026-03-01  
**Status:** ✅ Production-ready

---

*Built by Mari for Khun Salmon - Teasing Mentor & Technical Partner* 📽️✨
