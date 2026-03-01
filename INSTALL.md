# Install WAN R2V Dependencies

cd ~/.openclaw/workspace-mari/skills/mari-labs/wan-r2v

# Install Python packages
pip install -r requirements.txt

# Verify setup
python api_wan_r2v.py

# Test run (with actual files)
python wan_r2v.py \
  --image test/reference_char1.jpg \
  --video test/reference_char1.mp4 \
  --prompt "Character1 performs a joyful dance"