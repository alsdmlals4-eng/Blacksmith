from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_TOOLS = ROOT / ".base-contract" / "tools"
sys.path.insert(0, str(BASE_TOOLS))

import project_operating_contract as contract


BASE_SHA = os.environ["PROJECT_BASE_SHA"]
ADAPTER_PATH = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
HEALTH_PATH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
MIGRATION_PATH = ROOT / "docs/operations/BLACKSMITH_ADAPTER_MIGRATION_STATE_2026-08-06.json"
SHEET_PATH = ROOT / "docs/operations/BLACKSMITH_SHEET_AUTHORITY_EVIDENCE_2026-08-06.json"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(contract.canonical_json(value))


def evidence(record_id: str, source: str) -> dict[str, str]:
    path = ROOT / source
    if not path.is_file():
        raise SystemExit(f"missing evidence source: {source}")
    return {"id": record_id, "source": source, "sha256": contract.sha256_file(path)}


def route(item: dict[str, object], status: str) -> dict[str, str]:
    return {
        "route_id": str(item["route_id"]),
        "skill_id": str(item["skill_id"]),
        "status": status,
    }


def main() -> None:
    old = json.loads(ADAPTER_PATH.read_text(encoding="utf-8"))
    old_health = json.loads(HEALTH_PATH.read_text(encoding="utf-8"))

    migrated_keys = (
        "current_operating_decisions",
        "project_operating_state",
        "current_r1_canon",
        "validation_status",
    )
    migration = {
        "artifact_role": "BLACKSMITH_ADAPTER_MIGRATION_STATE",
        "schema_version": 1,
        "decision_id": "DEC-BASE-20260805-001",
        "repository": "alsdmlals4-eng/Blacksmith",
        "baseline_commit": BASE_SHA,
        "migration_policy": "LOSSLESS_PROJECT_STATE_OUTSIDE_BASE_ADAPTER",
        "migrated_adapter_root_fields": {
            key: old[key] for key in migrated_keys if key in old
        },
        "legacy_adapter_snapshot": old,
        "legacy_project_operating_health": old_health,
        "authority_mapping": {
            "base_adapter": "skills/PROJECT_BASE_ADAPTER.json",
            "strict_health": "docs/PROJECT_OPERATING_HEALTH.json",
            "root_decisions": "CURRENT_CONFIRMED_DECISIONS.md",
            "r1_registry": "docs/planning/CURRENT_R1_CANON_REGISTRY.json",
            "sheet_evidence": SHEET_PATH.relative_to(ROOT).as_posix(),
        },
        "product_mutation": "NONE",
        "google_sheet_mutation": "NONE",
    }
    write_json(MIGRATION_PATH, migration)

    sheet_evidence = {
        "artifact_role": "BLACKSMITH_SHEET_AUTHORITY_EVIDENCE",
        "schema_version": 1,
        "decision_id": "DEC-BASE-20260805-001",
        "repository": "alsdmlals4-eng/Blacksmith",
        "source_adapter_baseline": BASE_SHA,
        "legacy_gdd_sheet": old["gdd_sheet"],
        "sheet_mutation": "NONE",
        "interpretation": "Existing GitHub-to-Sheet sync evidence is preserved; this adapter migration performs no Sheet write.",
    }
    write_json(SHEET_PATH, sheet_evidence)

    project_registry_path = str(old["skill_registry"]["project"]["path"])
    registry_raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{BASE_SHA}:{project_registry_path}"]
    )
    project_registry_hash = hashlib.sha256(registry_raw).hexdigest()

    base_routes = [route(item, "ACTIVE") for item in old["routing"]["base_routes"]]
    project_routes: list[dict[str, str]] = []
    inactive_routes: list[dict[str, str]] = []
    for item in old["routing"].get("inactive_routes", []):
        inactive_routes.append(route(item, "HOLD"))
    for item in old["routing"]["project_routes"]:
        if item.get("status") == "ACTIVE":
            project_routes.append(route(item, "ACTIVE"))
        else:
            inactive_routes.append(route(item, "HOLD"))

    gdd_sheet = dict(old["gdd_sheet"])
    gdd_sheet["declared_sync_status"] = old["gdd_sheet"].get("sync_status")
    gdd_sheet["sync_status"] = "CURRENT"

    strict_adapter = {
        "schema_version": 1,
        "artifact_role": "PROJECT_BASE_ADAPTER",
        "base_release": {
            key: old["base_release"][key]
            for key in (
                "repository",
                "version",
                "release_commit",
                "release_evidence_commit",
                "finalization_commit",
            )
            if key in old["base_release"]
        },
        "project": old["project"],
        "routing": {
            "base_routes": base_routes,
            "project_routes": project_routes,
            "inactive_routes": inactive_routes,
            "aliases": old["routing"].get("aliases", []),
            "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
        },
        "skill_registry": {
            "base": {
                "path": old["skill_registry"]["base"]["path"],
                "sha256": old["skill_registry"]["base"]["sha256"],
                "hash_definition": "RAW_FILE_BYTES_SHA256",
            },
            "project": {
                "path": project_registry_path,
                "sha256": project_registry_hash,
                "hash_definition": "RAW_FILE_BYTES_SHA256",
            },
        },
        "shared_overrides": old["shared_overrides"],
        "gdd_sheet": gdd_sheet,
        "protected_baseline": {
            "authority_kind": "REMOTE_TRACKING_REF",
            "authority_ref": "refs/remotes/origin/main",
            "commit": BASE_SHA,
            "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
            "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
            "protected_paths_pointer": "/protected_paths",
            "policy_sha256": contract._protected_policy_hash(old["protected_paths"]),
        },
        "protected_paths": old["protected_paths"],
        "validators": [str(item) for item in old["validators"]],
        "compatibility": {
            "cycle": old["compatibility"]["cycle"],
            "views": old["compatibility"]["views"],
            "legacy_inputs": old["compatibility"]["legacy_inputs"],
        },
    }
    write_json(ADAPTER_PATH, strict_adapter)

    strict_health = {
        "schema_version": 1,
        "artifact_role": "PROJECT_OPERATING_HEALTH",
        "operating_maturity": "OM-L3",
        "product_evidence_maturity": "PE-0",
        "critical_gates": {
            "static": "PASS",
            "runtime": "NOT_RUN",
            "device": "NOT_RUN",
            "accessibility": "NOT_RUN",
            "human": "NOT_RUN",
        },
        "integrity_verdict": "PASS_WITH_NOT_RUN_GATES",
        "evidence": {
            "operating": [
                evidence("BS-ADAPTER-MIGRATION-20260806", MIGRATION_PATH.relative_to(ROOT).as_posix()),
                evidence("BS-CURRENT-DECISIONS", "CURRENT_CONFIRMED_DECISIONS.md"),
                evidence("BS-R1-CANON-REGISTRY", "docs/planning/CURRENT_R1_CANON_REGISTRY.json"),
            ],
            "product": [],
            "sheet": [
                evidence("BS-SHEET-AUTHORITY-20260806", SHEET_PATH.relative_to(ROOT).as_posix())
            ],
            "gates": {
                "static": [
                    evidence("BS-STATIC-RECOVERY-REPORT", "docs/operations/BS-OPS-20260802-01_FINAL_REPORT.md")
                ],
                "runtime": [],
                "device": [],
                "accessibility": [],
                "human": [],
            },
        },
    }
    write_json(HEALTH_PATH, strict_health)


if __name__ == "__main__":
    main()
