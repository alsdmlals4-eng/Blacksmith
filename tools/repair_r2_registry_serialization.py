#!/usr/bin/env python3
from pathlib import Path

path = Path("tools/apply_r2_initial_stat_enhancement_ownership.py")
text = path.read_text(encoding="utf-8")
old = '    write(relative, json.dumps(data, ensure_ascii=False, indent=2) + "\\n")'
new = '    write(relative, json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\\n")'
position = text.find(old)
if position < 0:
    if new in text:
        print("registry serialization already repaired")
    else:
        raise SystemExit("registry serialization anchor missing")
else:
    text = text[:position] + new + text[position + len(old):]
    path.write_text(text, encoding="utf-8")
    print("registry serialization repaired")
