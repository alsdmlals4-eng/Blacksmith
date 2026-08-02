# Active Context

- 갱신일: `2026-08-02 22:45 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 운영 Decisions: `BS-OPS-20260802-01` ~ `BS-OPS-20260802-05`
- 최근 main 병합: PR `#93`, SHA `b3a852cbb35de73a4b2da32151f845ddd61e1921`
- 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE`
- 현재 상태: `CORE_CONFIRMED / CORE_RECORDED / BATCH_001_TO_004_MERGED / CORE_REVIEW_AND_AUTHORITY_REPAIR`
- 명예의 전당: `FUTURE_CONTENT_HOLD`
- 제품 구현: `BLOCKED`

## 현재 판정

| 영역 | 상태 |
|---|---|
| R0 정본 복구 | `MERGED_TO_MAIN` |
| R1 승인 배치 001~004 | `MERGED / SHEET_READBACK_PASS` |
| 핵심 시스템·재미 적대적 검토 | `COMPLETE_WITH_FINDINGS` |
| 루트·Registry·Hub 권위 | `REPAIR_IN_PROGRESS` |
| Sheet 직접 충돌 | `CORRECTION_REQUIRED` |
| 열린 PR #86·#61 | `SUPERSEDED / HISTORY_ONLY` |
| 열린 PR #81 | `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT` |
| 최신 제품 Runtime | `NOT_RUN` |
| Android·접근성·성능·사람 플레이 | `NOT_RUN` |

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 제작
→ 한 결과씩 강화
→ 멈춤·추가 도전
→ +10 단위 작품 정체성
→ 방문 고객 인계
→ 즉시 인과 결과
→ 지연된 작품 생애·재방문
→ 새로운 작품과 더 중요한 의뢰
```

핵심 재미는 두 층이다.

- 순간 동력: 강화 성공·실패와 멈춤·도전 판단
- 장기 의미: 내가 만든 작품의 소유자·손상·복원·사건·연대기가 세계에서 돌아오는 것

## 현재 핵심 시스템

1. 직접 단조·영구 출생 품질
2. 일반 강화·한 입력 한 결과
3. +10/+20/+30/+40/+50 정밀강화와 작품 정체성
4. UID 기반 작품 생애주기
5. 방문 고객·인계·즉시 원인 피드백
6. 지연된 세계 환류·재방문
7. 피로도·날짜 우선순위

보조 시스템과 후속 콘텐츠는 `docs/planning/BLACKSMITH_CORE_SYSTEM_FUN_AND_PR_ADVERSARIAL_REVIEW_2026-08-02.md`에서 분리한다.

## 최신 중요 경계

- 선택한 한 작품은 데모에서 실제 +50까지 진행한다.
- +5는 과거 사람 검증 체크포인트이며 최신 데모 종료점이 아니다.
- 대파·손상은 UID와 생애를 유지한다.
- 완전 파괴는 명시적 선택으로만 가능하며 역사 기록은 남는다.
- 모든 작품은 같은 강화 대상이며 방문 고객 인계 후 고객 생애가 활성화된다.
- 명예의 전당은 순위 없는 미래 아카이브이고 현재 상세화 중지 상태다.

## 정본

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_CORE_SYSTEM_FUN_AND_PR_ADVERSARIAL_REVIEW_2026-08-02.md`

## 열린 PR 판정

- PR #86: 최신 main보다 뒤처진 배치 01 상태 PR — 종료 대상
- PR #61: v6 대형 초안 — 역사 자료로 종료 대상
- PR #81: v9 고유 설계 자산 원본 — 분야별 선별 이관 전까지 Draft 유지

## 실제 구현과 책임 원본

- 현재 실행 진입: `res://scenes/test/enhancement_test.tscn`
- 기존 장비 생애 PoC 범위: `docs/MVP-003_SCOPE.md`
- 기존 장비 생애 PoC: `REFERENCE_IMPLEMENTATION`
- 최신 승인 피로도·날짜·+50 데모·고객 생애·명예의 전당은 제품 구현 완료가 아니다.

## Historical CI compatibility evidence

아래 문자열은 과거 PoC·CI 계약의 분류된 증거이며 최신 R1 구현 완료를 뜻하지 않는다.

- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`
- `PR validation #468`
- `docs/MVP-003_SCOPE.md`

## 다음 작업

1. 루트·Registry·Hub와 Sheet의 직접 충돌을 복구한다.
2. `한 작품 +50 생애 버티컬 슬라이스`를 첫 코어 증명 범위로 확정할지 사용자 검토한다.
3. PR #81 고유 자산은 최신 main 기반 소형 PR로만 선별 이관한다.
4. 제품 구현은 계속 차단한다.
