# BS-OPS-20260811-01 — Project Work Instruction v4.5 r2 Canon

Status: `USER_APPROVED / CANON_REPLACEMENT / PLANNING_ONLY`

## Decision

Blacksmith의 프로젝트 총 작업지시문 정본을 `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md`의 v4.5 r2 source로 교체한다.

- source contract: `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION`
- contract version: `4.5`
- revision: `2026-08-11-r2`
- source SHA-256: `3f898b7e2749a2e1900e9df48183f02d4fbc735fd0e80297f28bb09317144de4`
- source bytes: `77734`
- source handling: `SOURCE_VERBATIM_CANON`

## Source path conflict and current Blacksmith override

첨부 v4.5 r2 source는 역사적으로 `Switchy-Express-Cargo-Puzzle` 로컬 경로를 보존한다. source 자체를 조용히 수정해 충돌을 숨기지 않는다: `SOURCE_PATH_CONFLICT_EXPLICIT_OVERRIDE / DO_NOT_EDIT_SOURCE_TO_HIDE_CONFLICT`.

사용자의 최신 프로젝트 바인딩이 상위 권위이므로 현재 Blacksmith 실행 경로는 아래 값을 사용한다.

```yaml
project_repository: alsdmlals4-eng/Blacksmith
project_local_path: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
canonical_local_checkout: C:\Users\user\Documents\GitHub\Ninza\Blacksmith
godot_project_path: C:/Users/user/Documents/GitHub/Ninza/Blacksmith
```

이 override는 source 원문 보존과 동시에 적용한다. Base current main은 매 작업마다 다시 읽으며 source의 historical Base snapshot은 current authority가 아니다.

## Protected gates

- `PRODUCT_IMPLEMENTATION: BLOCKED`
- `TASK3_IMPLEMENTATION: NOT_APPROVED`
- R3–R7 planning may continue under approved Decisions.
- PowerShell/Codex/Godot BUILD는 v4.5 r2의 planning-complete 사용자 Gate 전에는 시작하지 않는다.
- 같은 승인 범위의 planning/document PR은 모든 current Gate 통과 후 병합 재승인을 요구하지 않는다.
- PR #81은 `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`로 유지한다.

## Canon routing

1. `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md`
2. 이 Decision — current Blacksmith binding override
3. `AGENTS.md`
4. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
5. `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
6. Google Sheet same Decision ID `BS-OPS-20260811-01`

## Verification contract

`tests/test_project_total_instruction_v45_r2_canon.py`가 source SHA-256, v4.5 r2 핵심 token, override Decision, router consumer를 검증한다.
