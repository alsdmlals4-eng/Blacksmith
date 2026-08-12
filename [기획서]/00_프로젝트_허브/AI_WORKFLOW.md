# Blacksmith AI·GitHub 작업 흐름

## Base v9.4 계약

- `[모델 추천]`은 난도·실패 비용·재작업 위험을 기준으로 모델과 추론 단계를 제안한다. 실제 모델 설정 변경은 사용자가 수행하며 다음 checkpoint부터 적용한다.
- 보안·권한·데이터 무결성·저장 호환성·불가역 변경은 `HARD_CONSTRAINT`다.
- 일반 기술 구조는 `RECOMMENDED_DEFAULT`, 비파괴 표현 초안은 `JUDGMENT_SPACE`다.
- Prompt는 `problem / player_or_user_value / inputs / authority_and_source / output_contract / invariants / failure_conditions / validation`의 Interface-first 계약으로 작성한다.
- `Example-as-Fixture`: 예시는 정답 권위가 아니라 정상·실패·경계·회귀 Fixture 또는 Golden Set이다.
- Context는 `decision_question / include_criteria / exclude_criteria / authority_level / freshness / known_conflicts / progressive_load_trigger / refresh_trigger`를 기록한다.
- 화면·Schema·Fixture는 실제 Android 런타임·사람 이해·성능을 자동 증명하지 않는다. 실행하지 않은 Android·provider 검증은 `NOT_RUN`, 사람 이해·반복 피로는 `HUMAN_NOT_RUN`이다.

## Loop Engineering Pilot

Decision: `BS-OPS-20260813-LOOP-01`.

```text
PLANNING_COMPLETE
→ PLANNING_LOCKED
→ SHADOW(A0_OBSERVE)
→ exact-head 계약·보호면 검증
→ 별도 승인된 기존 canon 작업만 A2_EXECUTE_ISOLATED
```

- 프로젝트 Profile: `docs/operations/BLACKSMITH_LOOP_ENGINEERING_PROFILE.md`
- 현재 Run: `docs/operations/BLACKSMITH_LOOP_RUN_CONTRACT.json`
- 승격 순서: `SHADOW → A2_EXECUTE_ISOLATED`
- SHADOW에서는 `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`을 포함한 제품 root를 변경하지 않는다.
- A2는 별도 잠금된 승인 작업만 격리 Branch/Worktree에서 수행한다. Godot persistent authoring은 기존 `P0_LOCAL_EXECUTOR_BOOTSTRAP`과 fresh HiGodot receipt 뒤에만 가능하다.
- Task3·신규 제품 범위·project core·제작/강화/경제·save·major UX 의미 변경은 `USER_DECISION_REQUIRED`다.
- A3 auto-merge allowlist는 비어 있고 scheduler/runtime provider는 `NOT_CONFIGURED`다.
- 이 Pilot의 Base 계약 출처는 exact main `453f790821a108a1d4f6e1f4e45f6931c2396ee0`이며, Blacksmith의 Base v9.4.3 adapter pin을 자동 변경하지 않는다.

## Blacksmith 보호

제작·강화·경제·저장·승인 아트는 프로젝트 정본과 실제 파일이 소유한다. Base 기본값으로 수치나 제품 의미를 덮어쓰지 않는다.

Base identity: payload `a728712cb776ec98f4875914a580fcf7d0156593`, evidence `ef1fba11167e4da0b298123b0c85ebd268191a42`, Registry `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
