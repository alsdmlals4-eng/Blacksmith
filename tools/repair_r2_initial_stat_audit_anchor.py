#!/usr/bin/env python3
from pathlib import Path

path = Path("tools/apply_r2_initial_stat_enhancement_ownership.py")
text = path.read_text(encoding="utf-8")
start_token = "    anchor = '}\\n\\nHISTORICAL_ASSERTIONS = {'"
end_token = "    write(relative, text)"
start = text.index(start_token)
end = text.index(end_token, start)
replacement = """    anchor = '    \"docs/planning/BLACKSMITH_R2_ITEMIZATION_BENCHMARK_2026-08-05.md\": (\\n'
    if new_required not in text:
        if anchor not in text:
            raise RuntimeError(\"operating audit assertion insertion anchor missing\")
        text = text.replace(anchor, new_required + anchor, 1)
"""
path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")
print("synchronizer audit anchor repaired")
