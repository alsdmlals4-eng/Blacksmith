# Active Context

- 갱신일: `2026-08-02 15:38 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 운영 Decisions: `BS-OPS-20260802-01`, `BS-OPS-20260802-02`
- 최근 main 병합: PR `#84`, SHA `bd68c2dbf20592e84c1bebfdc83c4c925d010dbf`
- 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE`
- 현재 상태: `CORE_CONFIRMED / CORE_RECORDED / GRILL_BATCH_01_MERGED / NEW_COUNTER_0_OF_10 / R1_IN_PROGRESS`
- 제품 구현: `BLOCKED`

## 현재 판정

| 영역 | 상태 |
|---|---|
| R0 정본 복구 | `MERGED_TO_MAIN` |
| R1 승인 배치 01 | `5 APPROVED / MERGED` |
| 신규 Grill Me 카운터 | `0/10` |
| Root·R1 Registry·Hub | `POSTMERGE_SYNC` |
| PR #84 사전 감사 | `PASS / P0 0 / P1 0` |
| 기존 Reference Godot contracts | `PASS_AT_PR84_HEAD` |
| 최신 R1 제품 기능 Runtime | `NOT_RUN` |
| Android·접근성·성능·사람 플레이 | `NOT_RUN` |

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 고객과 세계 사건에서 남긴 역사와 반응을 돌려받는 Android 세로형 제작 게임.

```text
직접 제작
→ 강화 성공·실패와 멈춤·추가 도전
→ 피로도에 따른 하루 우선순위
→ 고객 판매·납품
→ 짧은 세계 사건 결과
→ 작품의 소유·운명·연대기·세트
→ 새로운 작품과 더 높은 강화
```

## 병합된 R1 Decision

- `BS-CORE-20260802-01`: 피로도·날짜 핵심 불변
- `BS-CORE-20260802-02`: 강화 메인, 고객·세계 환류
- `BS-SET-20260802-01`: 다양한 작품 제작 동기와 세트
- `BS-SET-20260802-02`: 실제 기여 작품의 사건 연대기 세트
- `BS-SET-20260802-03`: 범용 보정 + 상황 태그 + 역사 기록
- `BS-SET-20260802-04`: 실패·참패도 실제 기여 시 세트 성립

정본:

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R1_APPROVED_CORE_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_EVENT_CHRONICLE_SET_CANON_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_01_AND_MERGE_POLICY_2026.md`

## 실제 구현과 책임 원본

- 현재 실행 진입: `res://scenes/test/enhancement_test.tscn`
- 기존 장비 생애 PoC 범위: `docs/MVP-003_SCOPE.md`
- 기존 장비 생애 PoC: `REFERENCE_IMPLEMENTATION`
- 강화 실패·하락·파괴·재료 소비·연속 실패 보정: `data/crafting/enhancement_balance.json`
- +10 단위 이정표·특수 강화·수식어 성장: `data/crafting/enhancement_milestones.json`
- `enhancement_milestones.json`은 실패 정책을 소유하지 않는다.
- 최신 피로도·날짜·연대기 세트·Main/Shell/Save는 아직 구현되지 않았다.

## Historical CI compatibility evidence

아래 문자열은 과거 PoC·CI 계약의 분류된 증거이며 최신 R1 구현 완료를 뜻하지 않는다.

- `POC v0.6.4 · main · 2026.07.23.1`
- `제작 모델 7건`
- `통합 6건`
- `POC v`
- `자동 단조`
- `+11`
- `+30`
- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`
- `PR validation #468`

PR #84의 실제 최종 검증은 Base v9 adoption run #247과 PR validation run #838에서 성공했다.

## 병합 운영

`BS-OPS-20260802-02`:

1. 배치 01은 PR #84로 squash 병합 완료.
2. 현재 신규 승인 카운터 `0/10`.
3. 이후 새 승인 10건마다 GitHub·Sheet·PR·리뷰·CI·충돌·금지 경로를 적대적으로 감사.
4. P0/P1 발견 시 병합 중단.
5. 통과 시 squash 병합하고 main SHA를 재동기화.

## 보호 경로

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

PR #84의 보호 제품 경로 변경은 `0`이었다.

## 다음 작업

1. postmerge sync PR #85를 검증·병합하고 최종 main SHA를 Sheet에 기록한다.
2. 신규 카운터 `0/10`에서 R1의 남은 프로젝트 코어·플레이어 약속을 계속 기획한다.
3. 제품 구현은 계속 차단한다.
