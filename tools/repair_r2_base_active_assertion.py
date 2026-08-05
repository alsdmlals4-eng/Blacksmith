#!/usr/bin/env python3
from pathlib import Path

path = Path("tests/test_base_v942_planning_first_adoption.py")
text = path.read_text(encoding="utf-8")
text = text.replace("test_batch_005_is_active_at_eight_of_ten", "test_batch_005_is_active_at_nine_of_ten")
text = text.replace('self.assertEqual("R2_BATCH_005_ACTIVE_8_OF_10", self.registry["stage_status"])', 'self.assertEqual("R2_BATCH_005_ACTIVE_9_OF_10", self.registry["stage_status"])')
text = text.replace('self.assertEqual("8/10", self.registry["next_approval_counter"])', 'self.assertEqual("9/10", self.registry["next_approval_counter"])')
text = text.replace('self.assertEqual(8, active["approved_decisions"])', 'self.assertEqual(9, active["approved_decisions"])')
text = text.replace('self.assertEqual("8/10", active["counter"])', 'self.assertEqual("9/10", active["counter"])')
anchor = '                "BS-ITEM-20260806-04",\n            ],\n            active["decisions"],'
replacement = '                "BS-ITEM-20260806-04",\n                "BS-ITEM-20260806-05",\n            ],\n            active["decisions"],'
if replacement not in text:
    if anchor not in text:
        raise SystemExit("active decision list anchor missing")
    text = text.replace(anchor, replacement, 1)
path.write_text(text, encoding="utf-8")
print("planning-first active batch assertion repaired")
