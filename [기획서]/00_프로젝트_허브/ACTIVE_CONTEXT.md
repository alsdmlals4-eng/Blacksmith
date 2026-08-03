# Active Context

- 갱신: `2026-08-03 08:30 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE / CANON_ALIGNMENT_AND_PR_AUDIT`
- 최근 main: PR `#93`, `b3a852cbb35de73a4b2da32151f845ddd61e1921`
- 현재 권위 Draft: PR `#94`
- 승인 배치: `001~004 MERGED / SHEET_READBACK_PASS`
- 핵심 충돌: `RESOLVED`
- 명예의 전당: `FUTURE_CONTENT_HOLD / NONCOMPETITIVE_ARCHIVE`
- 제품 구현: `BLOCKED`

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 제작
→ 한 결과씩 강화
→ 멈춤·추가 도전 판단
→ +10 단위 정밀강화
→ 방문 고객 인계
→ 즉시 인과 결과
→ 날짜·세계일정
→ 같은 UID 생애·재방문
→ 복원·재강화·다음 목표
```

- 순간 동력: 강화 결과와 멈춤·도전 판단
- 장기 의미: 작품의 소유자·손상·복원·사건·계승·연대기가 돌아오는 것

## 현재 핵심 시스템

1. 직접 단조·영구 출생 품질
2. 일반 강화·한 입력 한 결과
3. `+10/+20/+30/+40/+50` 정밀강화
4. 일반 수식어 A·B
5. 활성 사건·연대기 수식어 한 개와 진화 이력
6. UID 기반 작품 생애주기
7. 방문 고객 인계·즉시 인과 결과
8. 지연된 세계 환류·재방문
9. 피로도·날짜 우선순위
10. 버전형 경제 테스트 프리셋

## 확정된 경계

- 현재 검증 상한은 `+50`; 최종 상한은 `DEFERRED`다.
- `+5/+10`은 역사 PoC 체크포인트이며 최신 데모 종료점이 아니다.
- 일반 수식어는 두 개이며 사건 수식어는 별도 한 개다.
- 손상·대파는 UID와 생애를 유지하고 복원 가능하다.
- 수식어는 삭제보다 잠금·복원을 따른다.
- 완전 파괴는 명시적 선택만 허용하며 역사 기록은 남긴다.
- 정확한 비용·확률·피로도·보상·간격은 테스트 프리셋이다.
- 명예의 전당은 순위 없는 미래 아카이브다.

## 강화 데이터 권위

- `data/crafting/enhancement_balance.json`: 현재 구현의 강화 비용·확률·실패·위험·단계 하락·파괴 비율과 시도 소비 정책을 소유한다. 정확한 값은 `LEGACY_IMPLEMENTED_VALUE` 또는 버전형 테스트 프리셋이며 최신 기획 불변 규칙과 구분한다.
- `data/crafting/enhancement_milestones.json`: 현재 구현의 정밀강화 이정표·보상 정의를 소유한다. 최신 제품 방향은 `+10/+20/+30/+40/+50`이며 실제 데이터 정렬은 제품 구현 승인 뒤 별도 수행한다.
- 실패·위험 규칙의 기획 의미는 최신 Decision과 Game Bible이 소유하고, 실제 구현값은 위 data 파일과 tests가 증명한다.

## 첫 코어 버티컬 슬라이스

```text
플레이어 선택 작품 한 점 제작
→ +10/+20/+30/+40/+50
→ 방문 고객 납품
→ 즉시 결과
→ 날짜·세계일정
→ 같은 UID 재방문
→ 손상·복원·재강화 판단
```

다른 작품군은 제한된 비플레이 미리보기로만 제공한다.

## 코어 재미 검증

행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 결과 인과 설명
- 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

직후 중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류하고 최소 수정 후 재검증한다.

## 역사 구현·보조 기능 추적

- `POC v0.6.4 · main · 2026.07.23.1`은 현재 저장소의 제작 품질 구현 기준선 버전이다. 최신 제품 기획 버전 번호가 아니라 `REFERENCE_IMPLEMENTATION / HISTORICAL_POC` 증거다.
- 해당 기준선의 자동 검증 기록은 `제작 모델 7건`, `통합 6건`이다. 최신 +50 생애 슬라이스의 사람 검증을 대신하지 않는다.
- `POC v` 계열 문서는 MVP-001~003의 역사 구현 기준선이며 현재 제품 범위를 소유하지 않는다.
- 과거 `+11` 단계 하락과 `+30` 파괴 경계는 `LEGACY_IMPLEMENTED_VALUE`이며 최신 손상·대파·복원 정본이 우선한다.
- `자동 단조`는 반복 편의용 보조 시스템으로 유지하되 `+10` 정밀 이정표·위험·소유권·날짜 판단을 자동으로 통과하지 않는다.

## 현재 정본

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `[기획서]/00_프로젝트_허브/ROADMAP.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- `docs/planning/BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`
- `docs/planning/BLACKSMITH_CORE_CANON_RESOLUTION_01_2026.md` ~ `06_2026.md`

## 열린 PR

- `#94`: `CURRENT_AUTHORITY_REPAIR / DRAFT`
- `#95`: `SUPERSEDED / CLOSED_WITHOUT_MERGE`
- `#86`: `SUPERSEDED / CLOSE_WITHOUT_MERGE`
- `#61`: `HISTORY_ONLY / CLOSE_WITHOUT_MERGE`
- `#81`: `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`

## 실제 검증 상태

- MVP-003: `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`
- 최신 R1 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 다음 작업

1. Sheet 구형 표현 정렬
2. PR #94 changed files·리뷰·스레드·댓글·CI·금지 경로·드리프트 감사
3. 차단 결함 0이면 expected HEAD squash merge
4. main SHA·Sheet 재동기화
5. 사용자 R1 정본 최종 검수
