#!/usr/bin/env python3
"""GitHub-only Notion migration completeness contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTING = ROOT / "docs/decisions/BS-OPS-20260828-35_GITHUB_ONLY_CANON_AND_IMAGE_EXECUTION_ROUTING.md"
RECEIPT = ROOT / "docs/migration/BLACKSMITH_NOTION_TO_GITHUB_MIGRATION_20260828.md"
MANIFEST = ROOT / "docs/migration/BLACKSMITH_NOTION_MIGRATION_MANIFEST_20260828.json"
GDD = ROOT / "docs/design/PROJECT_AI_PRODUCTION_SPEC.md"
AGENTS = ROOT / "AGENTS.md"
VISUAL_APPROVAL = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_ASSET_APPROVAL_2026-08-25.md"

EXPECTED_PAGES = {
    "3c41b237-eb1c-813f-a481-e415e3250d1c": "CURRENT_MAPPED",
    "3c01b237-eb1c-81a1-8cd0-f8bc7eb2f420": "CURRENT_MAPPED",
    "3c51b237-eb1c-81d7-80e0-d7e9fc704489": "CURRENT_MAPPED",
    "3c01b237-eb1c-81a4-af26-c3057bfdcbbf": "CURRENT_MAPPED",
    "3c11b237-eb1c-8143-baef-ecf4e697a258": "CURRENT_MAPPED",
    "3c51b237-eb1c-812b-8572-d6683dbfaf0a": "CURRENT_MAPPED",
    "3c01b237-eb1c-8147-abdf-fab51a8f9ad3": "CURRENT_MAPPED",
    "3c51b237-eb1c-81cf-b5c2-f25c9f14e9b3": "CURRENT_MAPPED",
    "3c01b237-eb1c-817a-b257-cf6e2d299896": "CURRENT_MAPPED",
    "3c01b237-eb1c-8178-82e7-dd74ee265309": "CURRENT_MAPPED",
    "3c01b237-eb1c-810a-b307-eb2cb480b81a": "CURRENT_MAPPED",
    "3c01b237-eb1c-8139-a61fd9917994a726": "CURRENT_MAPPED",
    "3c01b237-eb1c-8125-8e44-ed79bc638813": "OMITTED_STALE_DATA",
}

EXPECTED_ARCHIVE_HASHES = {
    "BS-VIS-20260820-01": "2619843ad82c640e7038acd8a0687752f46326464444f0f24e062464e6cd7066",
    "BS-VIS-20260820-02": "606579edbc51f5a9454e4cf0f694e5f1ef4a40544488fda46512b46ed26175ce",
    "BS-VIS-20260820-04": "b675de17a0a48b5719c6bb80a4e1bf39f7a7dea99583ba2a9923d5dbb8d0b028",
    "BS-VIS-20260820-05": "3329e8b6c341b7482bf59afa00f652dcd930f138d78cbb2dfc04b56b67c4e84e",
    "BS-VIS-20260820-06": "378496097011ebfbcfe80d3611309825fed119f5bd5bbee272d149923aa6bb3f",
    "BS-VIS-20260820-08": "8cb10166a354f13ee0117c279870bc76bb2f226a13e56e37005952aea329bdec",
    "BS-VIS-20260820-09": "b683ae966b4ca4853c9efae7a49aeab1e9e769127f3ca540db276e2e2efda915",
    "BS-VIS-20260824-10": "c1831b39b7d48646bbd07224a301f6cbc6ede4f9da02c3e4cf6e5985f6067aa9",
}


def main() -> None:
    for path in (ROUTING, RECEIPT, MANIFEST, GDD, AGENTS, VISUAL_APPROVAL):
        assert path.exists(), f"missing migration owner: {path.relative_to(ROOT)}"

    routing = ROUTING.read_text(encoding="utf-8")
    assert "GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE" in routing
    assert "NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED" in routing

    receipt = RECEIPT.read_text(encoding="utf-8")
    for token in (
        "NOTION_READ_ONLY_ONE_TIME_SOURCE_MIGRATION",
        "NO_FUTURE_NOTION_READ_WRITE",
        "HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME",
        "OMITTED_STALE_DATA",
    ):
        assert token in receipt, f"migration receipt missing token: {token}"

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["migration_id"] == "BS-OPS-20260828-35/NOTION-MIGRATION"
    assert manifest["source_mode"] == "NOTION_READ_ONLY_ONE_TIME_SOURCE_MIGRATION"
    assert manifest["future_notion_access"] == "NO_FUTURE_NOTION_READ_WRITE"
    assert manifest["stale_numeric_data_policy"] == "OMIT_UNLESS_OWNED_BY_CURRENT_CANON"
    assert manifest["destination_readback"] == "GITHUB_PATH_AND_HASH_VERIFIED"

    page_map = {row["source_page_id"]: row for row in manifest["page_migrations"]}
    assert set(EXPECTED_PAGES).issubset(page_map), "missing Notion page migration mapping"
    for page_id, disposition in EXPECTED_PAGES.items():
        row = page_map[page_id]
        assert row["disposition"] == disposition, page_id
        if disposition == "CURRENT_MAPPED":
            assert row["repository_destinations"], page_id
            for relative_path in row["repository_destinations"]:
                assert (ROOT / relative_path).exists(), f"missing mapped owner: {relative_path}"
        else:
            assert row["omission_reason"], page_id

    archive_map = {row["visual_id"]: row for row in manifest["historical_visual_archive"]}
    assert set(archive_map) == set(EXPECTED_ARCHIVE_HASHES)
    for visual_id, expected_hash in EXPECTED_ARCHIVE_HASHES.items():
        row = archive_map[visual_id]
        assert row["status"] == "HISTORICAL_REFERENCE_ONLY_NOT_RUNTIME", visual_id
        assert row["style_canon"] == "NOT_FINAL_STYLE_CANON", visual_id
        assert row["system_semantics"] == "STALE_DO_NOT_IMPORT", visual_id
        path = ROOT / row["repository_path"]
        assert path.exists(), f"missing archived visual: {path.relative_to(ROOT)}"
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual_hash == expected_hash == row["sha256"], visual_id

    gdd = GDD.read_text(encoding="utf-8")
    assert "SRC-MIG-01" in gdd
    assert "BLACKSMITH_NOTION_TO_GITHUB_MIGRATION_20260828.md" in gdd

    agents = AGENTS.read_text(encoding="utf-8")
    assert "NOTION_MIGRATION_RECEIPT" in agents
    assert "HISTORICAL_NOTION_VISUAL_ARCHIVE" in agents

    visual_approval = VISUAL_APPROVAL.read_text(encoding="utf-8")
    assert "GITHUB_MIGRATION_RECEIPT" in visual_approval
    assert "NOTION_SOURCE_STATUS = RETIRED_AFTER_ONE_TIME_READ_ONLY_MIGRATION" in visual_approval


    print("GitHub-only Notion migration contract: PASS")


if __name__ == "__main__":
    main()
