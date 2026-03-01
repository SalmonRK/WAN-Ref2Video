# WAN-Ref2Video GitHub Repo Plan

## 📋 Plan for Approval

### 1. **Repository Details**
- **Name:** `WAN-Ref2Video`
- **Owner:** `openclaw` or `SalmonRK`
- **Description:** Generate videos using Alibaba Cloud's WAN 2.6 R2V model with reference images/videos
- **Visibility:** Public

### 2. **What's Included**
- ✅ `wan_r2v_cloudinary.py` - Main script (Cloudinary URL support)
- ✅ `api_wan_r2v.py` - API client library
- ✅ `requirements.txt`
- ✅ `SKILL.md` - Full documentation
- ✅ `README.md` - Quick start guide
- ✅ `CRON.md` - Cron job setup
- ✅ `test/` - Test reference files

### 3. **What's Excluded (.gitignore)**
```
# Output files
output/*.mp4
cron_status/*.json
logs/*.log

# Sensitive files
.env
.env.*
api_key.txt

# Large test files (user must upload individually)
test/reference_char1.jpg
test/reference_char1.mp4
```

### 4. **Installation Instructions**
```bash
cd ~/.openclaw/workspace-mari/Mari-Labs/wan-r2v
pip install -r requirements.txt
```

Add to `~/.openclaw/.env`:
```env
WAN_API_KEY=your_alibaba_cloud_api_key
WAN_MODEL=wan2.6-r2v  # optional: wan2.6-r2v-flash
```

### 5. **Security Features**
- ✅ API keys masked in all logs
- ✅ No secrets in code
- ✅ `.env` included in `.gitignore`
- ✅ Large files excluded from commit

---

## 🚀 Next Steps (After Approval)

1. Create GitHub repo `WAN-Ref2Video`
2. Push all except `.gitignore`d files
3. Add `WAN_API_KEY` instructions to README
4. Update MEMORY.md & TOOLS.md
5. Set up cron job for automated testing

---

**Status:** Awaiting approval  
**Created:** 2026-03-01  
**Ready to deploy:** Yes
