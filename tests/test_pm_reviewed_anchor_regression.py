from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from tests import test_pm_real_base_integration as integration


PM_SHA = "96bee2700c8931b9262ad5a24a0664a400858f20"
MANIFEST = integration.REVIEWED_INTEGRATION_MANIFEST_RELATIVE


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=check,
        timeout=20,
        env={"GIT_NO_REPLACE_OBJECTS": "1"},
    )


def init_reviewed_repo(root: Path, marker: str) -> tuple[str, str]:
    root.mkdir(parents=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "fixture")

    receipt = {
        "project_work_kanban": {
            "work_items": [
                {"work_item_id": "BS-PM-04", "status": "VERIFY_REVIEW"}
            ]
        }
    }
    payloads = {
        ".github/workflows/validate-current-base-adaptation-work-contract.yml": f"name: {marker}\n",
        "docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md": f"# {marker}\n",
        "docs/operations/receipts/2026-09-02-pm-execution-gate.json": json.dumps(receipt, indent=2) + "\n",
        "tests/test_pm_execution_gate.py": f"# {marker}\n",
        "tests/test_pm_real_base_integration.py": f"# {marker}\n",
        "tools/check_pm_work_receipt.py": (
            f"PM_TOOLING_COMMIT = '{PM_SHA}'\n"
            "GIT_NO_REPLACE_OBJECTS = '1'\n"
        ),
    }
    for relative, content in payloads.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-qm", f"{marker} functional artifacts")
    artifact_commit = git(root, "rev-parse", "HEAD").stdout.strip()

    artifacts: dict[str, dict[str, str]] = {}
    for relative in integration.REQUIRED_MERGED_PM_PATHS:
        fields = git(root, "ls-tree", artifact_commit, "--", relative).stdout.strip().split(None, 3)
        artifacts[relative] = {
            "mode": fields[0],
            "object_type": fields[1],
            "object_id": fields[2],
        }
    manifest = {
        "schema_version": 1,
        "manifest_role": "reviewed-pm-integration-artifact-identities",
        "artifact_set_commit": artifact_commit,
        "artifacts": artifacts,
    }
    manifest_path = root / MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    git(root, "add", MANIFEST)
    git(root, "commit", "-qm", f"{marker} reviewed manifest")
    return artifact_commit, git(root, "rev-parse", "HEAD").stdout.strip()


def receipt_tail_clone(source: Path, target: Path) -> str:
    subprocess.run(
        ["git", "clone", "-q", "--no-local", str(source), str(target)],
        check=True,
        capture_output=True,
        timeout=20,
    )
    git(target, "config", "user.email", "fixture@example.invalid")
    git(target, "config", "user.name", "fixture")
    receipt_path = target / integration.RECEIPT_RELATIVE
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["closeout_tail"] = "fixture"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    git(target, "add", integration.RECEIPT_RELATIVE)
    git(target, "commit", "-qm", "receipt-only closeout")
    return git(target, "rev-parse", "HEAD").stdout.strip()


class PMReviewedAnchorRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_self_consistent_unreviewed_base_is_rejected(self) -> None:
        reviewed = self.root / "reviewed"
        _, reviewed_head = init_reviewed_repo(reviewed, "reviewed")
        unreviewed = self.root / "unreviewed"
        _, unreviewed_head = init_reviewed_repo(unreviewed, "unreviewed")
        subject = self.root / "subject"
        subject_head = receipt_tail_clone(unreviewed, subject)

        errors = integration.verify_receipt_only_closure(
            subject,
            unreviewed,
            unreviewed_head,
            subject_head,
            reviewed_root=reviewed,
            reviewed_head_sha=reviewed_head,
            reviewed_merge_sha=reviewed_head,
            reviewed_merged=True,
        )

        self.assertIn("trusted reviewed integration", "\n".join(errors))

    def test_matching_reviewed_base_accepts_receipt_only_tail(self) -> None:
        reviewed = self.root / "reviewed"
        _, reviewed_head = init_reviewed_repo(reviewed, "reviewed")
        subject = self.root / "subject"
        subject_head = receipt_tail_clone(reviewed, subject)

        errors = integration.verify_receipt_only_closure(
            subject,
            reviewed,
            reviewed_head,
            subject_head,
            reviewed_root=reviewed,
            reviewed_head_sha=reviewed_head,
            reviewed_merge_sha=reviewed_head,
            reviewed_merged=True,
        )

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
