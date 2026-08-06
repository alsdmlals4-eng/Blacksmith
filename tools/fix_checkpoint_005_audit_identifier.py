from pathlib import Path

path = Path("tools/audit_project_operating_system.py")
text = path.read_text(encoding="utf-8")
old = '        "R2 체크포인트 005",\n        "R2_BATCH_005_CLOSED_10_OF_10",'
new = '        "R2_CHECKPOINT_005",\n        "R2_BATCH_005_CLOSED_10_OF_10",'
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one audit identifier match, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8", newline="\n")
print("updated=tools/audit_project_operating_system.py")
