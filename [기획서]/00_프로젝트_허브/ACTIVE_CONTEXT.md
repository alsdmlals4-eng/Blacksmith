# [현재 정본] Active Context

- 갱신: `2026-08-05 00:34 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R2_CORE_SESSION_META_LOOP / R2_BATCH_004_2_OF_10`
- R2 체크포인트 003: `PR #103 / closure #104 / canon audit #105`
- 정본 감사 Decision: `BS-OPS-20260804-02 / BS-ADV-20260804-01`
- 현재 제작 Decision: `BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01`
- 현재 운영 Decision: `BS-OPS-20260805-01`
- 현재 승인 카운터: `2/10`
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

## 제작 등급 5단계

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID 영구 고정
- 제작 후 승격·강등 없음
- `전설`은 출생 극희귀 결과
- 예술성·촉매·연대기·명성·복원으로 등급 변경 없음

이전 `R2_BATCH_004_1_OF_10`의 4단계 `[보통] → [우수] → [걸작] → [전설]`은 `[대체됨]`이다. 과거 `STANDARD / GOOD / PERFECT`는 `HISTORICAL_IMPLEMENTED_VALUE`다.

## 예술성

```text
예술성 1~10
예술성 7/10
```

- 무기·작품 능력치의 하나
- 정수, 소수점 없음
- 예술성 단계명 없음
- 다른 무기 능력치와 함께 표시
- 판매 가치와 귀족·후원자·수집가·전시·감정·증여·의식 수요에 기여 가능
- 전투 성능을 기본적으로 올리지 않음
- 범용 속성 증폭 배율이 아님

## 장비명

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

```text
[명품] 예리한 강철 장검 - 투기장의 승자 ›
```

연대기 수식어를 누르면 UID 기반 읽기 전용 상세를 연다.

## 운영 계약

### 벤치마킹·현업 비교

질문·추천·설계 전에 유사 게임·현업 사례를 비교한다. 결과는 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록한다.

### 승인 배치

- 최대 배치 크기: `10`
- 현재: `2/10`
- 조기 체크포인트: `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT`
- 조기 체크포인트도 적대적 감사·CI·PR changed files·Sheet readback 필수
- 병합은 명시적 사용자 승인 필요

### 작업마다 TDD

```text
RED → GREEN → REFACTOR
```

- 테스트 먼저
- 의도한 RED 관측
- 최소 변경으로 GREEN
- RED·GREEN 증거 없이 완료 주장 금지

## PR #81 경계

```text
전체 병합 단위: [폐기]
브랜치·원 승인 원문: [역사 증거]
분야별 선별 이관: [보류]
```

## 역사 구현·회귀 기준선

다음은 현재 5등급 제품값이 아니라 과거 reference implementation의 회귀 증거다.

- 최신 역사 구현 배지: `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 과거 제작 품질: `STANDARD / GOOD / PERFECT`
- 과거 피버·품질 정확 수치: `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`
- 과거 PASS는 현재 5등급·예술성 제품 구현 PASS가 아님

## 검증 경계

- 이전 PR #103/#104/#105 exact-head Base·Python·Godot: `PASS`
- 이번 변경 TDD RED: Planning-first run `33`에서 관측
- GREEN exact-head: `PENDING`
- focused planning test standalone: `NOT_RUN`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 다음 작업

1. GREEN exact-head 검증
2. Google Sheet same-ID readback
3. Draft PR #106에 누적, 조기 체크포인트 조건 또는 최대 10건 전 병합 금지
