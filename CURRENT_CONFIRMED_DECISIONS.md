# Blacksmith Current Confirmed Decisions

> R1 정본 기준 병합: PR `#94`
>
> R1 정본 기준 SHA: `8a0956d6c8b4cf3db545a17d0bd002ba8354d568`
>
> 현재 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE / USER_FINAL_REVIEW_PENDING`
>
> 상태: `R1_CANON_ALIGNED / PRODUCT_BLOCKED`

## 1. 권위 규칙

이 파일은 현재 Decision 상태의 루트 진입점이다. 상세 의미는 병합된 배치 정본, Core Resolution 원장, 통합 Game Bible과 R1 Registry가 소유한다.

우선순위:

1. 최신 사용자 승인 Decision과 병합된 최종 정본
2. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
3. `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
4. 현재 Hub·Roadmap 문서
5. 과거 Prototype·PoC·연구·Draft 문서

과거 문서가 최신 Decision과 충돌하면 최신 Decision이 우선한다. 미검증 정확한 수치·주기·확률·경제값은 제품 확정값이 아니라 버전형 테스트 프리셋이다.

## 2. 운영 Decision

- `BS-OPS-20260802-01`: 총기획·정본 복구를 제품 구현보다 우선
- `BS-OPS-20260802-02`: 승인 배치·적대적 감사·squash 병합 정책
- `BS-OPS-20260802-03`: 배치 002 감사·병합
- `BS-OPS-20260802-04`: 배치 003 감사·병합
- `BS-OPS-20260802-05`: 배치 004 조기 종료·감사·병합
- `BS-OPS-20260802-06`: 주요 Grill Me·작업에 공식 벤치마킹과 현업 비교 적용
- `BS-OPS-20260803-01`: Game Bible·Hub·Roadmap·MVP·Registry·Sheet 정렬
- `BS-OPS-20260803-02`: PR #94 적대적 감사, P0/P1 0, CI 통과, squash 병합

제품 구현은 전체 기획과 최종 사용자 검수 전까지 `BLOCKED`다.

## 3. 승인 정본

병합 배치:

- `BLACKSMITH_GRILLME_APPROVAL_BATCH_001_2026.md`
- `BLACKSMITH_GRILLME_APPROVAL_BATCH_002_2026.md`
- `BLACKSMITH_GRILLME_APPROVAL_BATCH_003_2026.md`
- `BLACKSMITH_GRILLME_BATCH_04_R1_DECISIONS_2026.md`

R1 충돌 해소:

- `BS-CORE-20260802-03`: 현재 검증 상한 `+50`, 매 `+10` 이정표, 최종 상한 `DEFERRED`
- `BS-CORE-20260802-04`: 일반 수식어 A·B 두 개, 세계일정 성질은 별도 계층
- `BS-CORE-20260803-01`: 활성 사건·연대기 수식어 한 개와 진화 이력
- `BS-CORE-20260803-02`: 한 작품 `+50` 생애 왕복 버티컬 슬라이스
- `BS-CORE-20260803-03`: 구조는 정본, 정확한 숫자는 버전형 테스트 프리셋
- `BS-CORE-20260803-04`: 행동 증거+중립적 회상 인터뷰 검증 Gate

통합 정본:

- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `docs/planning/BLACKSMITH_R1_CANON_ALIGNMENT_AND_PR94_AUDIT_2026.md`

## 4. 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
강화의 즉각 판단
→ 작품을 세상에 보냄
→ 작품의 생애와 세계 결과가 돌아옴
→ 다음 강화·복원·제작 이유가 생김
```

강화는 반복 동력이고 작품 생애와 세계 환류는 의미·장기 보상이다.

## 5. 코어 구조

### 강화·성장

- 현재 검증 상한: `+50`
- 정밀 이정표: `+10 / +20 / +30 / +40 / +50`
- 장기 최종 상한: `DEFERRED`
- 과거 `+100`: `LEGACY_IMPLEMENTED_VALUE / DEFERRED_TEST_TARGET`
- 일반 수식어: A·B 두 개
- 활성 사건·연대기 수식어: 한 개의 진화 계보

### 작품 생애

- 방문 고객에게 실제 인계한 뒤 생애 활성화
- 같은 UID가 소유·사용·결과·손상·복원·계승·재방문 유지
- 일반 실패와 대파는 UID·역사를 삭제하지 않음
- 수식어는 삭제보다 잠금·복원
- 완전 파괴는 명시적이고 정보가 제공된 선택에서만 허용
- 완전 파괴 후에도 역사 기록 보존

### 피로도·날짜

- 피로도는 오늘의 작업 우선순위 자원
- 성공률·완성도를 몰래 낮추지 않음
- 날짜는 플레이어가 하루 종료를 선택할 때 진행
- 고객·세계일정·재방문의 공통 시간축

## 6. 첫 코어 버티컬 슬라이스

```text
플레이어가 선택한 작품 한 점 제작
→ +10/+20/+30/+40/+50 정밀 이정표
→ 방문 고객 납품
→ 즉시 인과 결과
→ 피로도·날짜·세계일정
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
→ 작품 생애가 다음 강화 이유로 환류
```

- `+50` 도달만으로 완료하지 않음
- 다른 작품군은 제한된 비플레이 미리보기
- 검증 작품을 시스템 대표작 등급으로 승격하지 않음

## 7. 수치 권위

정본이 소유하는 것:

- 자원 종류·소비 시점·반환 여부
- 정보 공개 규칙
- 실패·손상·복원·파괴 상태 전이
- 피로도와 날짜의 역할

버전형 프리셋이 소유하는 것:

- 강화 비용·확률
- 피로도 소비·이월
- 보상량
- 재료·촉매 수량
- 날짜·재방문 간격

상태:

- `LEGACY_IMPLEMENTED_VALUE`
- `BASELINE_TEST_PRESET`
- `EXPERIMENT_VARIANT`
- `CURRENT_VALIDATED`
- `DEPRECATED_PRESET`

## 8. 코어 재미 검증 Gate

행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 결과 인과 설명
- 같은 UID 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류하고 원인을 수정한 뒤 재검증한다. 만족도·완료율·클릭 수는 보조지표이며 단독 통과 근거가 아니다.

## 9. 콘텐츠 상태

- 사건 연대기 세트: 승인된 장기 보조 시스템
- 수집가: 플레이어 제작·납품·처분 작품과 재회하는 보조 콘텐츠
- 명예의 전당: 비경쟁 작품 아카이브 방향 승인, `FUTURE_CONTENT_HOLD`
- 경쟁 랭킹·점수·시즌 보상: 폐기된 방향
- `+60` 이상·대형 세계 콘텐츠: 후속 검토

## 10. 역사 구현 분류

- MVP-001·002·003: 과거 구현·자동 검증 기준선
- MVP-003: `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`
- `+5/+10` 판단: 역사 연구 체크포인트이며 최신 데모 종료 구조가 아님
- 과거 정확한 수치: `LEGACY_IMPLEMENTED_VALUE`
- 과거 PASS: 최신 R1 제품 PASS가 아님

## 11. 감사·검증 상태

- PR #94: squash merged
- R1 정본 감사: P0 `0`, P1 `0`
- 최종 PR CI: `Validate Base v9 adoption` 성공, `PR validation` 성공
- GitHub·Sheet 정본 정렬: 완료, 최종 main SHA 동기화 필요
- 최신 제품 runtime: `NOT_RUN`
- Android 실기기: `NOT_RUN`
- 접근성·성능: `NOT_RUN`
- 행동 증거·회상 인터뷰 사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 12. 다음 Gate

1. PR #94 병합 SHA와 Google Sheet를 최종 동기화
2. 사용자 R1 정본 최종 검수
3. 승인 후 R2 `Core·Session·Meta Loop` 기획 진행
4. 제품 구현은 R1~R8과 최종 사용자 검수 전까지 시작하지 않음
