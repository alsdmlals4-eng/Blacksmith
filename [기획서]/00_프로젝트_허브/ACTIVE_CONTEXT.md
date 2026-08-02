# Active Context

- 갱신: `2026-08-02 22:45 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE / CORE_REVIEW_AND_AUTHORITY_REPAIR`
- 최근 main: PR `#93`, `b3a852cbb35de73a4b2da32151f845ddd61e1921`
- 승인 배치: `001~004 MERGED / SHEET_READBACK_PASS`
- 명예의 전당: `FUTURE_CONTENT_HOLD`
- 제품 구현: `BLOCKED`

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 제작 → 한 결과씩 강화 → 멈춤·도전
→ +10 단위 작품 정체성 → 방문 고객 인계
→ 즉시 인과 결과 → 지연 생애·재방문
```

- 순간 동력: 강화 결과와 멈춤·도전 판단
- 장기 의미: 작품의 소유자·손상·복원·사건·연대기가 돌아오는 것

## 핵심 시스템

1. 직접 단조·영구 출생 품질
2. 일반 강화·한 입력 한 결과
3. `+10/+20/+30/+40/+50` 정밀강화
4. UID 기반 작품 생애주기
5. 방문 고객 인계·즉시 원인 피드백
6. 지연된 세계 환류·재방문
7. 피로도·날짜 우선순위

## 최신 경계

- 선택 작품은 데모에서 실제 `+50`까지 진행한다.
- `+5`는 과거 사람 검증 지점이며 최신 데모 종료점이 아니다.
- 손상·대파는 UID와 생애를 유지하고 복원 가능하다.
- 완전 파괴도 명시적 선택만 허용하며 역사 기록은 남는다.
- 명예의 전당은 순위 없는 미래 아카이브다.

## 현재 정본

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_CORE_SYSTEM_FUN_AND_PR_ADVERSARIAL_REVIEW_2026-08-02.md`

## 열린 PR

- `#86`: `SUPERSEDED / CLOSED_WITHOUT_MERGE`
- `#61`: `HISTORY_ONLY / CLOSED_WITHOUT_MERGE`
- `#81`: `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`
- `#94`: 권위·Sheet 충돌 복구 Draft

## 실제 검증 상태

- 과거 장비 생애 PoC: `REFERENCE_IMPLEMENTATION`
- 최신 R1 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## Historical CI compatibility evidence

아래는 과거 PoC·정적 계약의 분류된 증거이며 최신 제품 PASS가 아니다.

- `POC v0.6.4 · main · 2026.07.23.1`
- `자동 단조`
- `+11`
- `제작 모델 7건`
- `통합 6건`
- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`
- `PR validation #468`
- `docs/MVP-003_SCOPE.md`

## 다음 결정

권장: `한 작품 +50 생애 버티컬 슬라이스`.

상태: `RECOMMENDED / USER_APPROVAL_REQUIRED`.
