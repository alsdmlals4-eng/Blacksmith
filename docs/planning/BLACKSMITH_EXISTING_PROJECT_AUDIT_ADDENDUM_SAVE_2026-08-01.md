# Blacksmith 기존 프로젝트 감사 보완 — 세이브·ResultEnvelope

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A3`
>
> Decision ID: `BS-SAVE-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / CROSS_SOURCE_VERIFIED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 감사 대상

- `scripts/forging/forging_session.gd`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/economy/workshop_resources.gd`
- `scripts/progression/workshop_calendar.gd`
- `scripts/world/equipment_world_registry.gd`
- 기존 UI·PoC 흐름의 메모리 상태와 Snapshot 패턴

## 2. 보존할 강점

- 도메인별 `snapshot()` 사용
- 자원 부족 선검증
- 시도 시작 실패 시 골드·재료 복원
- 거래·세계 결과의 transaction/event ID 멱등성
- 강화 입력당 결과 한 번

## 3. 확인된 구조적 위험

1. Snapshot이 저장 복원용 스키마·버전·hash·참조 검증을 제공하지 않는다.
2. 단조·강화·장비 생애 PoC가 서로 다른 상태 소유자를 사용한다.
3. `EnhancementSession`의 RNG 상태와 시도 중단 경계가 영속 저장되지 않는다.
4. 비용·재료 차감 뒤 결과 확정 전 프로세스 종료 시 자원만 소실될 수 있다.
5. 세계 결과는 멱등성 ID가 있지만 캠페인 파일과 함께 원자 저장되지 않는다.
6. 결과 화면이 공통 Envelope를 사용하지 않아 재진입·복구 정책이 분산된다.
7. 손상 정본을 백업으로 회전하면 정상 백업까지 오염될 수 있다.
8. 새 게임 생성 실패 시 기존 캠페인을 먼저 삭제하면 복구 불가능한 손실이 발생한다.

## 4. 해결된 기획 목표

`BS-SAVE-20260801-01`로 다음을 승인했다.

- 단일 캠페인 + 자동 백업 2개
- 캠페인과 설정 파일 분리
- `SaveCoordinator` 단일 파일 쓰기 책임
- `CampaignSnapshot` 스키마·revision·hash
- 정상 정본만 백업 회전
- `SaveStatus` 기반 이어하기
- 사용자 고지 후 백업 복구
- 신규 캠페인 검증 후 기존 캠페인 교체
- `AttemptIntent PREPARED/RESOLVED`
- `ResultEnvelope CREATED/APPLIED/PRESENTED/ACKNOWLEDGED`
- 중단 복구 우선순위
- 자동·Android·사람 검증 매트릭스

## 5. Finding 판정

| Finding | 이전 | 현재 기획 판정 | 런타임 판정 |
|---|---|---|---|
| `BS-AUD-F02` | 영속 세이브·이어하기·복구 없음 | 목표 계약 해결 | OPEN |
| `BS-AUD-F09` | 공통 ResultEnvelope 없음 | 목표 계약 해결 | OPEN |
| `BS-AUD-F16` | Android 중단 복구 미정 | pause/process-death 목표 해결 | OPEN |

P0·P1 Finding 수는 제품 구현·마이그레이션·테스트 전까지 줄이지 않는다.

## 6. 적대적 검토 차단 조건

다음 중 하나라도 발생하면 구현은 실패다.

```text
손상 primary가 backup1으로 회전됨
동일 intent가 두 번 적용됨
앱 재실행으로 결과가 재추첨됨
APPLIED 저장 전에 결과 화면이 열림
PREPARED 중 종료 후 골드·재료만 소실됨
새 게임 첫 저장 실패 후 기존 캠페인이 사라짐
마이그레이션 실패가 원본 파일을 덮어씀
```

## 7. 연결 정본·Sheet

- 권위 Markdown: `docs/planning/BLACKSMITH_SAVE_CONTINUE_RESULT_ENVELOPE_CANON_2026.md`
- 계획 데이터: `docs/planning/data/blacksmith_save_continue_result_envelope_canon_2026.json`
- 구현 계획: `docs/superpowers/plans/2026-08-01-save-continue-result-envelope-implementation.md`
- 결정 인덱스: `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, 연결 JSON
- Sheet 결정: `02_현재_확정결정!A25:H25`
- Sheet 감사: `04_누락_충돌_감사!A19:H19`
- 직접 영향: `05!A2:H2,A7:H7,A10:H10`, `30!A3:H3`, `40!A9:H9`, `60!A16:H16`, `80!A8:H8`, `90!A5:H5`
- 변경이력: `99_변경이력!A21:H21`

## 8. 다음 연결 작업

1. Base 저장소 전체 스킬·작업 구조 재분석
2. Blacksmith GitHub·Google Sheet 전체 진행도 재감사
3. P0-2 제작 등급·수식어·+50 저장 마이그레이션
4. P0-3 고객 4유형과 관계·소유권 Snapshot
5. P0-4 자동 단조와 비가역 저장 경계
6. P1 Android lifecycle·뒤로가기·설정 영속성 상세

## 9. 상태

```text
SAVE_DESIGN: USER_APPROVED
RESULT_ENVELOPE_DESIGN: USER_APPROVED
IMPLEMENTATION_PLAN: COMPLETE
CROSS_SOURCE_SYNC: PASS
PRODUCT_CODE_CHANGE: NOT_RUN
RUNTIME_TEST: NOT_RUN
ANDROID_TEST: NOT_RUN
HUMAN_TEST: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
