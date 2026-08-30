# Task 6.1 approved art integration report

- RED: the updated Python contract failed before promotion because each requirement remained `GENERATED_CANDIDATE`; the three approved PNG paths were absent. GUT entrypoint invocations produced only the Godot 4.7.1 banner and no test summary, so they are `INCONCLUSIVE`, never PASS.
- Approved source verification and copied runtime assets: `main_menu_dawn_background_v1.png` `5870f6958135516b9d5f42f81e0d11e0724a5cbf27af9e3382f1de155a7f713a`, `precision_tag_workshop_background_v1.png` `45679f660ad9fc24796e0080aded8474be6b0c462ae7bb2d58a91b6c0530ef32`, `customer_result_return_illustration_v1.png` `716ce4dd4c6c4bdf48255c4b10aef906573d1113b331d20304e4f75f6e74eca1`; all are `941x1672`.
- Implemented: script-only dynamic bindings, Precision exact-ATTEMPT visibility, customer saved-result illustration/veil with opaque fallback, manifest/coverage/provenance lifecycle registration.
- Verification: `python tests/check_recurring_precision_visual_requirements_contract.py` PASS; JSON parse PASS; Godot 4.7.1 headless editor smoke exit 0; `git diff --check` clean. Focused GUT `test_vs_main_menu.gd`, `test_vs_workshop_screen.gd`, and `test_vs_customer_result_screen.gd`: INCONCLUSIVE (0 reported tests/assertions; no GUT summary).
- Runtime evidence: no Godot client, Android, accessibility, performance, or human review observed. Release remains `RELEASE_BLOCKED_UNVERIFIED`.
- Generated import/sidecar cleanup remains required before integration: Godot generated tracked `.import` drift plus new PNG `.import` and `.uid` sidecars; none are intended task files.

- P1 follow-up: review found a post-outcome Precision re-exposure and invalid-result visual preservation. The focused GUT runner remains INCONCLUSIVE (no totals emitted); updated tests now require post-success/post-hold hiding and invalid-result fallback. Static headless parse and Python contract remain the available machine evidence.
