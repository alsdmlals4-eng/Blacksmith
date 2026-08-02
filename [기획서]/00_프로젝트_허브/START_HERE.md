# Blacksmith 시작 지점

## 프로젝트 보호 방향

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

핵심 작품 기록 범위는 **장비의 출생·성장·소유·사건 기록**이다.

## 현재 상태

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
  - BS-OPS-20260802-03
  - BS-OPS-20260802-04
  - BS-OPS-20260802-05
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
R1_STATUS: BATCH_001_TO_004_MERGED / CORE_REVIEW_AND_AUTHORITY_REPAIR
CORE_STATUS: CORE_CONFIRMED / CORE_RECORDED
MAIN_SHA: b3a852cbb35de73a4b2da32151f845ddd61e1921
LAST_MERGED_PR: 93
HALL_OF_FAME: FUTURE_CONTENT_HOLD
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_ACTIVITY: REVIEW_ONE_WORK_PLUS50_LIFECYCLE_VERTICAL_SLICE
```

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
4. 이 문서
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `docs/planning/BLACKSMITH_CORE_SYSTEM_FUN_AND_PR_ADVERSARIAL_REVIEW_2026-08-02.md`
8. 배치별 승인 정본
9. 필요한 실제 코드·data·Scene·tests

## 현재 승인 정본

- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`

최신 승인 방향:

- 피로도·날짜는 핵심 불변.
- 강화 성공·실패와 멈춤·추가 도전이 가장 자주 반복되는 즉각 재미.
- 선택한 한 작품은 +10 단위 정밀강화를 거쳐 데모에서 실제 +50까지 진행.
- 작품은 UID·소유자·손상·복원·사건·연대기를 유지.
- 방문 고객 인계 후 즉시 인과 결과와 지연 생애 업데이트가 돌아옴.
- 대파는 생애 종료가 아니며 완전 파괴도 기록을 지우지 않음.
- 명예의 전당은 비경쟁 미래 아카이브이며 현재 `FUTURE_CONTENT_HOLD`.

## 핵심 시스템과 범위

코어:

```text
직접 단조
→ 한 결과씩 강화
→ 멈춤·도전 판단
→ +10 단위 작품 정체성
→ 방문 고객 인계
→ 즉시 원인 결과
→ 지연된 생애·재방문
→ 다음 작품과 더 중요한 선택
```

보조:

- 재료·촉매·보호·완충·지원 자원
- Save·Continue·ResultEnvelope
- 보관·판매·수집가·연대기 조회
- UI·접근성·Android 생명주기
- 자동 강화의 결정 경계
- 검증·마이그레이션·로컬 텔레메트리

후속:

- 명예의 전당 구현
- +60~+100 엔드게임
- 대규모 고객·세력·시장·전쟁·토너먼트

## 열린 PR 상태

- `#86`: 최신 배치와 충돌하는 배치 01 상태 PR — `SUPERSEDED`
- `#61`: v6 대형 초안 — `HISTORY_ONLY`
- `#81`: 고유 v9 설계 자산 보관 Draft — `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`

## 실제 구현 기준선

- 현재 실행 진입은 기존 테스트 Scene이며 최신 R1 제품 구현 완료를 의미하지 않는다.
- 과거 장비 한 점의 생애 PoC는 `REFERENCE_IMPLEMENTATION`이다.
- 최신 R1 제품 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`이다.
- 제품 구현은 계속 `BLOCKED`다.

## Historical CI compatibility evidence

아래 문자열은 `check_project_core_alignment.py`와 과거 PoC 증거 호환성을 위한 역사 기록이다. 최신 R1 제품 PASS를 뜻하지 않는다.

- `CORE_CONFIRMED`
- `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`
- `ACTIONS_AVAILABLE / AUTOMATIC_PR_ENABLED`
- `#35`
- `PR validation #468`

## 다음 작업

1. 최신 권위 진입점과 Sheet 충돌 문구를 복구한다.
2. `한 작품 +50 생애 버티컬 슬라이스` 권장안을 사용자 결정 대상으로 검토한다.
3. 승인 전 제품 구현은 시작하지 않는다.
