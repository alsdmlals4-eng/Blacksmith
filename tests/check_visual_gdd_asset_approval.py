from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/planning/BLACKSMITH_VISUAL_GDD_ASSET_APPROVAL_2026-08-25.md"

REQUIRED = {
    "BS-VIS-20260820-01": ("f18d7a58-21b4-469c-b16e-2cbeaa22530b", "2619843ad82c640e7038acd8a0687752f46326464444f0f24e062464e6cd7066"),
    "BS-VIS-20260820-02": ("0f76cb2f-b5c0-45bf-b891-f814e5d14e16", "606579edbc51f5a9454e4cf0f694e5f1ef4a40544488fda46512b46ed26175ce"),
    "BS-VIS-20260820-05": ("7fa82021-aee3-49ad-84a5-01cbfb836202", "3329e8b6c341b7482bf59afa00f652dcd930f138d78cbb2dfc04b56b67c4e84e"),
    "BS-VIS-20260820-06": ("e25e6e23-c370-46b0-b9d1-013f90794c93", "378496097011ebfbcfe80d3611309825fed119f5bd5bbee272d149923aa6bb3f"),
    "BS-VIS-20260820-09": ("66aed12c-f13c-41df-b6f5-027067898713", "b683ae966b4ca4853c9efae7a49aeab1e9e769127f3ca540db276e2e2efda915"),
    "BS-VIS-20260824-10": ("5c8090ff-898d-4a9f-80d9-4b36b3938fb6", "c1831b39b7d48646bbd07224a301f6cbc6ede4f9da02c3e4cf6e5985f6067aa9"),
}


def main() -> int:
    errors = []
    try:
        text = MANIFEST.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Visual GDD asset approval contract FAILED\n- cannot read {MANIFEST.relative_to(ROOT)}: {exc}")
        return 1

    for visual_id, (gen_id, sha256) in REQUIRED.items():
        for token in (visual_id, gen_id, sha256, "USER_APPROVED_VISUAL_GDD"):
            if token not in text:
                errors.append(f"missing token: {token}")

    for token in (
        "STYLIZED_DARK_FORGE = CURRENT",
        "APPROVED_REPRESENTATIVE_VISUAL = AVAILABLE",
        "FINAL_PRODUCT_ASSET_APPROVAL = NOT_GRANTED",
        "PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION",
        "RUNTIME_VALIDATION = NOT_RUN",
    ):
        if token not in text:
            errors.append(f"missing guard: {token}")

    if errors:
        print("Visual GDD asset approval contract FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Visual GDD asset approval contract PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
