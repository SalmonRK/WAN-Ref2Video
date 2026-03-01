# Test Assets for WAN R2V

This directory contains reference materials for testing the WAN R2V skill.

## Reference Files

### User's Reference Video
- `reference_char1.mp4`: Video of the user's character performing dance movements
- `reference_char1.jpg`: Still image of the same character

### Test Prompts

**Thai:**
- "Character1 ยืนเต้นร缓缓, ยิ้มแย้ม, หันหน้าเข้ากล้อง"
- "Character1 ทำท่าเต้น欢快, วิ่งจากซ้ายไปขวา"

**English:**
- "Character1 dances freely with a smile, facing the camera."
- "Character1 performs joyful choreography from left to right."

## Usage

```bash
# Test basic generation
python wan_r2v.py \
  --image reference_char1.jpg \
  --video reference_char1.mp4 \
  --prompt "Character1 performs a joyful dance"
```
