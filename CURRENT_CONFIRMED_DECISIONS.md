# Blacksmith Current Confirmed Decisions

> 기준 main: `b3a852cbb35de73a4b2da32151f845ddd61e1921`
>
> 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE / CORE_REVIEW_AND_AUTHORITY_REPAIR`
>
> 상태: `BATCH_001_TO_004_MERGED / HALL_FUTURE_CONTENT_HOLD / PRODUCT_BLOCKED`
>
> 최근 병합: PR `#93`

## 1. 권위 규칙

이 파일은 현재 Decision 상태의 루트 진입점이다. 상세 의미는 아래 배치별 GitHub 정본이 소유하며, Google Sheet는 같은 Decision ID를 사용하는 연결 작업공간이다. 실제 구현 사실은 코드·Scene·Resource·data·tests가 소유한다.

우선순위:

1. 최신 사용자 승인 Decision과 최종 배치 정본
2. `CURRENT_R1_CANON_REGISTRY.json`
3. 현재 Hub 문서
4. 과거 Draft·PR·PoC 문서

과거 문서가 최신 Decision과 충돌하면 최신 Decision이 우선한다. 수치·주기·확률·경제값은 명시 승인되지 않은 한 `RECOMMENDED_DEFAULT / TEST_VALUE`다.

## 2. 현재 운영 Decision

- `BS-OPS-20260802-01`: 총기획·정본 복구를 제품 구현보다 우선
- `BS-OPS-20260802-02`: 승인 배치·적대적 감사·squash 병합 정책
- `BS-OPS-20260802-03`: 배치 002 감사·병합
- `BS-OPS-20260802-04`: 배치 003 감사·병합
- `BS-OPS-20260802-05`: 배치 004 사용자 지시 조기 종료·감사·병합

제품 구현은 전체 기획·최종 적대적 검수·사용자 검수 전까지 `BLOCKED`다.

## 3. 현재 승인 정본

- 배치 001: `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- 배치 002: `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- 배치 003: `docs/planning/BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- 배치 004: `docs/planning/BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`
- 현재 핵심·PR 감사: `docs/planning/BLACKSMITH_CORE_SYSTEM_FUN_AND_PR_ADVERSARIAL_REVIEW_2026-08-02.md`

## 4. 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 안에서 작품을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

### 핵심 재미

- 즉각 반복 재미: 강화 성공·실패와 멈춤·추가 도전 판단
- 장기 의미: 작품의 UID·소유자·손상·복원·사건·연대기가 세계에서 돌아오는 것

강화는 동력이고 작품 생애와 세계 환류는 의미·보상이다.

### 최신 데모 방향

- 플레이어가 선택한 한 작품을 실제로 `+50`까지 진행
- 정밀강화 이정표: `+10 / +20 / +30 / +40 / +50`
- `+5`는 과거 사람 검증 체크포인트이며 최신 데모 종료점이 아님
- 방문 고객 인계 후 즉시 인과 결과와 지연된 생애 업데이트·재방문을 검증

## 5. 보호되는 방향

- 한 명의 대장장이; 직원·다중 대장장이·공장식 대량 생산 아님
- 직접 제작과 한 결과씩 확인하는 강화
- 영구 출생 품질; 같은 작품의 완성도 reroll 금지
- 중요 이정표와 위험·재료·판매·소유·날짜 판단을 자동화가 우회하지 않음
- 대파·손상은 UID와 생애를 유지하며 복원 가능
- 완전 파괴는 명시적이고 정보가 제공된 선택만 허용; 역사 기록은 남음
- 방문 고객에게 실제 인계된 작품만 고객 생애 활성화
- 피로도·날짜는 핵심 우선순위 축
- 플레이어 직접 전투는 현재 코어가 아님
- Android portrait·한 손 가독성

## 6. 콘텐츠 상태

- 연대기 세트: 승인됨; 코어를 보조하는 장기 기록·상황 보상
- 수집가: 플레이어 제작·납품·처분 작품 재회용 보조 콘텐츠
- 명예의 전당: 비경쟁 작품 아카이브로 방향 승인, 현재 `FUTURE_CONTENT_HOLD`
- +60~+100·완전 보호 경제·전쟁·토너먼트·대규모 고객 확장: 후속 검토

## 7. 현재 열린 PR 판정

- PR `#86`: `SUPERSEDED / CLOSE_WITHOUT_MERGE`
- PR `#61`: `HISTORY_ONLY / CLOSE_WITHOUT_MERGE`
- PR `#81`: `REFERENCE_ASSET / DO_NOT_MERGE_AS_UNIT`; 고유 문서만 최신 main 기반 소형 PR로 선별 이관

상세 근거는 `BS-CORE-AUDIT-20260802-01`을 따른다.

## 8. 현재 검증 상태

- 배치 004 main·Sheet readback: `PASS`
- 최신 승인 제품 runtime: `NOT_RUN`
- Android 실기기: `NOT_RUN`
- 접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

과거 `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`은 장비 생애 PoC 당시 HEAD의 역사 증거이지 최신 R1 제품 PASS가 아니다.

## 9. 다음 중요 결정

권장 검증 범위:

> `한 작품 +50 생애 버티컬 슬라이스`

한 작품의 직접 제작, +10 단위 성장, 방문 고객 인계, 즉시 원인 결과, 지연 생애 업데이트와 재방문까지 먼저 완주한 뒤 고객 수·작품 종류·세트·후속 콘텐츠를 확장한다.

상태: `RECOMMENDED / USER_APPROVAL_REQUIRED`.
