# [현재 정본] Active Context

- 갱신: `2026-08-05 12:35 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_005_0_OF_10`
- R2 체크포인트 003: `PR #103 / closure #104 / canon audit #105`
- R2 체크포인트 004: `PR #106 / closure #107`
- PR #106 exact head: `227b2dabf0d98832811415156e72f65d601332a9`
- PR #106 squash merge: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
- 현재 제작 Decision: `BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / MERGED_PR106 / MAIN_CANON`
- 현재 운영 Decision: `BS-OPS-20260805-01`
- 현재 승인 카운터: `0/10`
- 제품 구현: `BLOCKED`

## 현재 핵심

```text
직접 단조
→ 제작 등급 5단계
→ 일반 강화와 멈춤·추가 도전
→ 정밀강화 방식·촉매
→ 고객·세계 전달
→ 같은 UID 연대기·손상·복원
→ 다음 제작 판단
```

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

## 체크포인트 004 폐쇄

```text
R2_BATCH_004_CLOSED_2_OF_10 / CLOSED_MERGED_PR106
R2_CHECKPOINT_004 / MAIN_CANON
NEXT: R2_BATCH_005 / 0_OF_10
```

- `BS-CRAFT-20260804-07`: `USER_APPROVED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON`
- `BS-CRAFT-20260805-01`: `USER_APPROVED_REFINED_MERGED_PR106_R2_CHECKPOINT_004_MAIN_CANON`
- Sheet 5개 권위 위치: `MERGED_PR106 / MAIN_CANON / READBACK_PASS`
- 제품 경로 변경: `0`

## 제작 등급 5단계

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID 영구 고정
- 제작 후 승격·강등 없음
- `전설`은 출생 극희귀 결과
- 예술성·촉매·연대기·명성·복원으로 등급 변경 없음

과거 `STANDARD / GOOD / PERFECT`는 `HISTORICAL_IMPLEMENTED_VALUE`다.

## 예술성

대표 원수치 표기: `예술성 27`.

```text
공격력  42
내구도  31
조작성  18
예술성  27
```

- `0` 이상의 정수
- 고정 설계 최대치 없음
- 분모·별점·백분율·예술성 단계명 없음
- 다른 능력치와 함께 원수치 표시
- 전투 성능을 기본적으로 올리지 않음
- 범용 속성·수식어 증폭 배율이 아님
- 제작 등급이 예술성 상한을 만들지 않음
- 기술적 자료형 한계는 콘텐츠 최대치가 아님

`예술성 0`은 미적 투자가 거의 없는 정상 기능품이다.

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

초기 bounded 표현과 named tiers는 `[대체됨]`이다. 정확한 기대 범위·가격 점감·고객 선호 구간·증감값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 장비명

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

연대기 수식어를 누르면 UID 기반 읽기 전용 상세를 연다.

## 운영 계약

- 질문·추천·설계 전 벤치마킹·현업 비교
- 최대 배치 크기: `10`
- 현재: `R2_BATCH_005 / 0/10`
- 조기 체크포인트: `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT`
- 작업마다 TDD: `RED → GREEN → REFACTOR`
- 병합은 명시적 사용자 승인 필요

폐쇄 RED 증거:

- commit `276f62d7477ab48521b814c17832ee24c4c6457f`
- PR validation `1150`: `EXPECTED_FAILURE`
- Base `559`: `PASS`
- 실패 원인: PR106 병합 뒤 저장소 권위 상태가 아직 배치 004 활성·pending으로 남음

GREEN과 최종 exact-head 증거는 PR #107 검증 뒤 기록한다.

## 역사 구현·회귀 기준선

다음은 현재 5등급·예술성 제품 구현 PASS가 아니라 과거 reference implementation의 `[역사 증거]`다.

- 최신 역사 구현 배지: `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 과거 제작 품질: `STANDARD / GOOD / PERFECT`
- 강화 실패·위험 data 소유자: `data/crafting/enhancement_balance.json`
- 정밀 이정표 data 소유자: `data/crafting/enhancement_milestones.json`
- 과거 피버·품질 정확 수치: `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`
- 이 회귀 PASS를 현재 5등급·고정 상한 없는 예술성 제품 구현 PASS로 해석하지 않음

## 검증 경계

- focused closure/artistry/batch test standalone: `NOT_RUN`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 다음 작업

1. PR #107 exact-head CI·리뷰·Sheet readback
2. expected-head squash merge로 체크포인트 004 상태 폐쇄
3. `R2_BATCH_005 / 0/10`에서 다음 설계 후보 벤치마킹·적대적 검토
