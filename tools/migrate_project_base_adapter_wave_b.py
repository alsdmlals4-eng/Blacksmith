from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "skills/PROJECT_BASE_ADAPTER.json"
HEALTH_PATH = ROOT / "docs/PROJECT_OPERATING_HEALTH.json"
STATE_PATH = ROOT / "docs/PROJECT_OPERATING_STATE.json"
MIGRATION_PATH = ROOT / "docs/operations/PROJECT_BASE_ADAPTER_MIGRATION_2026-08-06.md"
PROJECT_REGISTRY_PATH = ROOT / "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"

DECISION = "DEC-BASE-20260805-001"
SOURCE_MAIN = "b1dd945875568098b107815a03e88b0272d384e9"
TRUSTED_BASE = "bfdc9e44d4a6920dc085eaa3f9d19d31b1acd2a1"
BASE_REGISTRY_SHA = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def protected_policy_hash(paths: list[str]) -> str:
    payload = json.dumps(paths, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    return sha256_bytes(payload)


def normalized_route(route: dict) -> dict:
    return {
        "route_id": route["route_id"],
        "skill_id": route["skill_id"],
        "status": "ACTIVE",
    }


def evidence(evidence_id: str, source: str, digest: str) -> dict:
    return {"id": evidence_id, "source": source, "sha256": digest}


def main() -> None:
    original_bytes = ADAPTER_PATH.read_bytes()
    original = json.loads(original_bytes.decode("utf-8"))
    original_health = read_json(HEALTH_PATH)

    forbidden_root = (
        "current_operating_decisions",
        "project_operating_state",
        "current_r1_canon",
        "validation_status",
    )
    preserved_root = {key: copy.deepcopy(original[key]) for key in forbidden_root}

    state_doc = {
        "schema_version": 1,
        "artifact_role": "BLACKSMITH_PROJECT_OPERATING_STATE",
        "repository": "alsdmlals4-eng/Blacksmith",
        "current_state": {
            "operating_decision": preserved_root["project_operating_state"]["current_r2_decision"],
            "stage": preserved_root["project_operating_state"]["stage"],
            "stage_status": preserved_root["project_operating_state"]["stage_status"],
            "product_implementation": preserved_root["project_operating_state"]["product_implementation"],
            "runtime_validation": preserved_root["project_operating_state"]["new_r2_runtime_validation"],
            "android_device_validation": preserved_root["project_operating_state"]["android_device_validation"],
            "human_validation": preserved_root["project_operating_state"]["human_playtest"],
        },
        "adapter_migration": {
            "decision_id": DECISION,
            "status": "PRESERVED_AND_MIGRATED_ON_DRAFT_BRANCH",
            "source_main_commit": SOURCE_MAIN,
            "trusted_base_validator": TRUSTED_BASE,
            "source_adapter_sha256": sha256_bytes(original_bytes),
            "preserved_from_adapter": preserved_root,
            "original_project_operating_health": original_health,
            "preserved_nested_metadata": {
                "base_release_adoption_status": original["base_release"].get("adoption_status"),
                "compatibility_generation_status": {
                    key: copy.deepcopy(original["compatibility"].get(key))
                    for key in (
                        "view_generation_status", "view_freshness", "manual_edit_policy"
                    )
                },
                "gdd_sheet": copy.deepcopy(original["gdd_sheet"]),
                "routing_policy": {
                    "selection_policy": original["routing"].get("selection_policy"),
                    "load_all_skills": original["routing"].get("load_all_skills"),
                    "blacksmith_engineering_original_status": next(
                        route["status"]
                        for route in original["routing"]["project_routes"]
                        if route["route_id"] == "blacksmith-engineering"
                    ),
                },
                "protected_baseline": copy.deepcopy(original["protected_baseline"]),
                "skill_registry": copy.deepcopy(original["skill_registry"]),
                "manual_validator_evidence": [
                    value for value in original["validators"] if value.startswith("manual:")
                ],
            },
            "normalized_contract": {
                "adapter_schema": "BASE_V1_THIN_ADAPTER",
                "health_schema": "BASE_PROJECT_OPERATING_HEALTH_V1",
                "protected_baseline_policy": "OPTION_A_EXACT_TRUSTED_BASE_EQUALITY",
                "gdd_sheet_contract_status": "CURRENT",
                "project_state_authority": "docs/PROJECT_OPERATING_STATE.json",
                "machine_health_authority": "docs/PROJECT_OPERATING_HEALTH.json",
                "product_files": "UNCHANGED",
                "google_sheets": "UNCHANGED",
            },
        },
    }
    write_json(STATE_PATH, state_doc)
    state_digest = sha256_bytes(STATE_PATH.read_bytes())
    state_evidence = evidence("blacksmith-project-state", "docs/PROJECT_OPERATING_STATE.json", state_digest)

    health = {
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
            "operating": [state_evidence],
            "product": [],
            "sheet": [state_evidence],
            "gates": {
                "static": [state_evidence],
                "runtime": [],
                "device": [],
                "accessibility": [],
                "human": [],
            },
        },
    }
    write_json(HEALTH_PATH, health)

    protected_paths = copy.deepcopy(original["protected_paths"])
    project_registry_sha = sha256_bytes(PROJECT_REGISTRY_PATH.read_bytes())
    base_release = {
        key: original["base_release"][key]
        for key in (
            "repository", "version", "release_commit",
            "release_evidence_commit", "finalization_commit",
        )
    }
    compatibility = {
        "cycle": original["compatibility"]["cycle"],
        "views": copy.deepcopy(original["compatibility"]["views"]),
        "legacy_inputs": copy.deepcopy(original["compatibility"]["legacy_inputs"]),
    }
    gdd_sheet = copy.deepcopy(original["gdd_sheet"])
    gdd_sheet["declared_sync_status"] = original["gdd_sheet"]["sync_status"]
    gdd_sheet["sync_status"] = "CURRENT"

    adapter = {
        "artifact_role": "PROJECT_BASE_ADAPTER",
        "base_release": base_release,
        "compatibility": compatibility,
        "gdd_sheet": gdd_sheet,
        "project": copy.deepcopy(original["project"]),
        "protected_baseline": {
            "authority_kind": "REMOTE_TRACKING_REF",
            "authority_ref": "refs/remotes/origin/main",
            "commit": SOURCE_MAIN,
            "policy_sha256": protected_policy_hash(protected_paths),
            "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
            "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
            "protected_paths_pointer": "/protected_paths",
        },
        "protected_paths": protected_paths,
        "routing": {
            "aliases": copy.deepcopy(original["routing"]["aliases"]),
            "base_routes": [normalized_route(route) for route in original["routing"]["base_routes"]],
            "inactive_routes": [
                {"route_id": route["route_id"], "skill_id": route["skill_id"], "status": route["status"]}
                for route in original["routing"]["inactive_routes"]
            ],
            "precedence": "PROJECT_LOCAL_THEN_BASE_SHARED",
            "project_routes": [normalized_route(route) for route in original["routing"]["project_routes"]],
        },
        "schema_version": 1,
        "shared_overrides": copy.deepcopy(original["shared_overrides"]),
        "skill_registry": {
            "base": {
                "hash_definition": "RAW_FILE_BYTES_SHA256",
                "path": "skills/SKILL_REGISTRY.json",
                "sha256": BASE_REGISTRY_SHA,
            },
            "project": {
                "hash_definition": "RAW_FILE_BYTES_SHA256",
                "path": "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json",
                "sha256": project_registry_sha,
            },
        },
        "validators": [
            value for value in original["validators"] if not value.startswith("manual:")
        ] + ["python -m unittest tests.test_project_base_adapter_thin_migration -v"],
    }
    write_json(ADAPTER_PATH, adapter)

    mapping_rows = [
        ("/current_operating_decisions", "/adapter_migration/preserved_from_adapter/current_operating_decisions", "verbatim"),
        ("/project_operating_state", "/adapter_migration/preserved_from_adapter/project_operating_state", "verbatim and current pointers retained"),
        ("/current_r1_canon", "/adapter_migration/preserved_from_adapter/current_r1_canon", "verbatim"),
        ("/validation_status", "/adapter_migration/preserved_from_adapter/validation_status", "verbatim evidence; no promotion"),
        ("previous PROJECT_OPERATING_HEALTH", "/adapter_migration/original_project_operating_health", "verbatim before Base Health normalization"),
        ("/base_release/adoption_status", "/adapter_migration/preserved_nested_metadata/base_release_adoption_status", "removed from Base contract"),
        ("/compatibility/*_status", "/adapter_migration/preserved_nested_metadata/compatibility_generation_status", "official generator becomes authority"),
        ("/routing/selection_policy", "/adapter_migration/preserved_nested_metadata/routing_policy/selection_policy", "removed from strict routing"),
        ("/routing/load_all_skills", "/adapter_migration/preserved_nested_metadata/routing_policy/load_all_skills", "removed from strict routing"),
        ("blacksmith-engineering route status", "/adapter_migration/preserved_nested_metadata/routing_policy/blacksmith_engineering_original_status", "adapter ACTIVE; implementation gate remains project-owned"),
        ("/protected_baseline", "/adapter_migration/preserved_nested_metadata/protected_baseline", "old evidence retained; canonical exact-base contract replaces it"),
        ("/skill_registry/*/hash_status", "/adapter_migration/preserved_nested_metadata/skill_registry", "old evidence retained; raw-byte SHA used in adapter"),
        ("manual validators", "/adapter_migration/preserved_nested_metadata/manual_validator_evidence", "not executable adapter commands"),
        ("/gdd_sheet/sync_status", "/adapter_migration/preserved_nested_metadata/gdd_sheet/sync_status", "SYNCED_TO_MAIN retained; adapter token CURRENT"),
    ]
    table = "\n".join(f"| `{source}` | `{target}` | {rule} |" for source, target, rule in mapping_rows)
    MIGRATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    MIGRATION_PATH.write_text(
        f"""# Blacksmith Project Base Adapter Migration — 2026-08-06

```yaml
decision_id: {DECISION}
source_main: {SOURCE_MAIN}
trusted_base_validator: {TRUSTED_BASE}
strategy: OPTION_A_EXACT_TRUSTED_BASE_EQUALITY
adapter_authority: BASE_V1_THIN_ADAPTER
project_state_authority: docs/PROJECT_OPERATING_STATE.json
machine_health_authority: docs/PROJECT_OPERATING_HEALTH.json
PRODUCT_FILES_UNCHANGED: true
GOOGLE_SHEETS_UNCHANGED: true
runtime_validation: NOT_RUN
android_device_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
```

## Field map

| Original field | Project-owned destination | Treatment |
|---|---|---|
{table}

## Scope boundary

The migration changes the Base connection contract, standard machine health, project-owned state, and official generated views only. It does not edit `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, Blacksmith gameplay canon, or Google Sheet cells. Historical PASS and NOT_RUN values are preserved verbatim and are not promoted.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
