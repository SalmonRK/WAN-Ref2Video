# WAN R2V Cron Jobs

##.hours 1 - Quick Test Job (Every 2 Minutes)
**Command:**
```bash
cd /Users/salmonrk/.openclaw/workspace-mari/Mari-Labs/wan-r2v && python3 wan_r2v_test.py 2>&1 | tee -a logs/cron_test.log
```

**Schedule:** `*/2 * * * *`

##.hours 2 - Main Job with URLs (Every 2 Minutes)
**Command:**
```bash
cd /Users/salmonrk/.openclaw/workspace-mari/Mari-Labs/wan-r2v && python3 wan_r2v_cron.py \
  --image "https://res.cloudinary.com/dxepor8fh/image/upload/v1772366845/z-image_00231__voi138.png" \
  --video "https://res.cloudinary.com/dxepor8fh/video/upload/v1772366719/Download_13_vblnf6.mp4" \
  --prompt "Character1 เคลื่อนไหวตามวิดีโอ reference อย่างแม่นยำ แสดงท่าเต้น energy มือสร้างรูปหัวใจ, ปรบมือ, ยิ้มแย้มและ wink ให้กล้อง" \
  --interval 120 \
  2>&1 | tee -a logs/cron_main.log
```

**Schedule:** `*/2 * * * *`

---

## Setup Instructions

### 1. Add to crontab
```bash
crontab -e
```

### 2. Add these lines (choose one job):
```cron
# Quick test job (every 2 minutes)
*/2 * * * * cd /Users/salmonrk/.openclaw/workspace-mari/Mari-Labs/wan-r2v && python3 wan_r2v_test.py 2>&1 | tee -a logs/cron_test.log

# OR Main job with Cloudinary URLs (every 2 minutes)
*/2 * * * * cd /Users/salmonrk/.openclaw/workspace-mari/Mari-Labs/wan-r2v && python3 wan_r2v_cron.py --image "https://res.cloudinary.com/dxepor8fh/image/upload/v1772366845/z-image_00231__voi138.png" --video "https://res.cloudinary.com/dxepor8fh/video/upload/v1772366719/Download_13_vblnf6.mp4" --prompt "Character1 เคลื่อนไหวตามวิดีโอ reference" --interval 120 2>&1 | tee -a logs/cron_main.log
```

### 3. Verify cron is running
```bash
crontab -l
```

### 4. Check logs
```bash
tail -f logs/cron_test.log
# or
tail -f logs/cron_main.log
```

---

## Status Files

Each task creates a status file in `cron_status/` directory:
- `task_<task_id>.json` - Contains task status and progress

---

## Notes

- Logs are saved to `logs/cron_*.log` (append mode)
- Test results are also logged to `logs/performance_*.log`
- Check status files to see current progress
- If task exceeds 10 minutes, it will timeout automatically
