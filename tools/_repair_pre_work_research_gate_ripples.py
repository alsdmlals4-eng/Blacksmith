import json
from pathlib import Path

agents_path = Path("AGENTS.md")
agents = agents_path.read_text(encoding="utf-8")
old_heading = "### PRE_WORK_RESEARCH_GATE — 벤치마킹·현업 조사"
new_heading = "### PRE_WORK_RESEARCH_GATE — 벤치마킹·현업 비교·조사"
if agents.count(old_heading) != 1:
    raise SystemExit(f"AGENTS compatibility heading count={agents.count(old_heading)}")
agents_path.write_text(agents.replace(old_heading, new_heading, 1), encoding="utf-8")

health_path = Path("docs/PROJECT_OPERATING_HEALTH.json")
health = json.loads(health_path.read_text(encoding="utf-8"))
records = {item["id"]: item for item in health["evidence"]["operating"]}
records["BS-CURRENT-DECISIONS"]["sha256"] = "4024ab0cfd6a974c2c03315722396e187c96cefcf0c9dab3ccef5505975be7e2"
health_path.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

Path(".github/workflows/pre-work-research-gate-ripple-repair.yml").unlink()
Path("tools/_repair_pre_work_research_gate_ripples.py").unlink()
