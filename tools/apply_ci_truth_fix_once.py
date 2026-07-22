from pathlib import Path

path = Path("scripts/ui/enhancement_screen.gd")
text = path.read_text(encoding="utf-8")
old = "\tvar can_change := (\n"
new = "\tvar can_change: bool = (\n"
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one can_change inference site, found {count}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("enhancement_screen.gd can_change type fixed")
