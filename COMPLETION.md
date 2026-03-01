# 🎬 WAN R2V Skill - Complete

**Created:** 2026-03-01  
**Model:** Alibaba Cloud Model Studio `wan2.6-r2v-flash`  
**API Endpoint:** `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  

---

## 📦 โครงสร้าง Skill

```
wan-r2v/
├── SKILL.md                      # คู่มือการใช้งาน
├── README.md                     # Overview
├── INSTALL.md                    # Setup instructions
├── TEST_LOG.md                   # Test activity log
├── example.env                   # .env template
├── requirements.txt              # Dependencies
├── api_wan_r2v.py                # API client (no API key display)
├── wan_r2v.py                    # CLI tool
├── output/                       # Generated videos
└── test/                         # Test reference files
```

---

## ⚙️ API Configuration

| Setting | Value |
|---------|-------|
| **API Key Source** | `~/.openclaw/.env` → `WAN_API_KEY` |
| **Model** | `wan2.6-r2v-flash` |
| **Endpoint** | `https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| **Size** | `1280*720` (16:9, horizontal) |
| **Audio** | `true` (preserves source audio) |
| **Duration** | 5-10 seconds |

---

## 🚀 Quick Start

```bash
# 1. Go to skill directory
cd ~/.openclaw/workspace-mari/skills/mari-labs/wan-r2v

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Test API key
python3 api_wan_r2v.py

# 4. Generate video (with actual files)
python3 wan_r2v.py \
  --image test/reference_char1.jpg \
  --video test/reference_char1.mp4 \
  --prompt "Character1 ยืนเต้นร缓缓"
```

---

## 🎨 Features

- ✅ **Reference-based generation** — use image + video for character consistency
- ✅ **Audio preserved** — keep audio from reference video
- ✅ **Vertical/Horizontal** — configurable aspect ratio
- ✅ **Logging** — performance logs in `logs/`
- ✅ **Mockup fallback** — graceful degradation without API key
- ✅ **SECRET PROTECTION** — API key masked in all outputs

---

## 🔐 Security Rules (from AGENTS.md)

1. ❌ Never print/display API keys
2. ❌ Never log API keys in plain text
3. ✅ Always use `os.getenv()` + dotenv
4. ✅ Mask keys in logs: `sk-81b2c...1d66`
5. ⚠️ Alert immediately if key exposed

---

**Status:** ✅ Ready for test with actual files  
**Next Steps:** User provides actual `reference_char1.jpg` and `reference_char1.mp4`
