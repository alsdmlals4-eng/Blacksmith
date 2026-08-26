# BS-TOOLCHAIN-20260826-33 — Godot AI 3.2.0 Current Vendor Alignment

- GitHub Issue: `#230`

## Decision

```text
BS-TOOLCHAIN-20260826-33 / GODOT_AI_320_CURRENT_VENDOR_ALIGNMENT
CURRENT_GODOT_AI_VERSION: 3.2.0
UPSTREAM_TAG: v3.2.0
UPSTREAM_TAG_COMMIT: 42c44e4d02ca1836a0e1866361509d3a14d83b0c
UPSTREAM_VENDOR_TREE_SHA: 66a9df59a92f0029efcd35c22fea355c93e8fe49
VENDOR_ALIGNMENT: EXACT_UPSTREAM_V3_2_0
PRODUCT_IMPLEMENTATION_SCOPE: UNCHANGED
```

The vendored `addons/godot_ai` tree on current main is byte-identical to the official `v3.2.0` `plugin/addons/godot_ai` tree. The release tag and tree were fresh-read directly from the official `hi-godot/godot-ai` repository before this record was created.

## Boundary

- This records the already-present vendor payload; it does not authorize a new product feature, scene mutation, or project-settings mutation.
- `BS-TOOLCHAIN-20260811-02` remains historical evidence for the former 3.1.4 state.
- `BS-TOOLCHAIN-20260809-01` and Task2 provenance remain historical 3.1.3 execution evidence.
- HiGodot remains the scoped serialized-authoring authority, GUT remains the sole GDScript test authority, and Hera remains non-authoritative.

## Disposition

```text
ADOPT: exact official v3.2.0 vendor identity
ADAPT: current vendor identity remains separate from historical Task2 execution
REJECT: rewriting Task2 evidence or inferring new product mutation authority
```
