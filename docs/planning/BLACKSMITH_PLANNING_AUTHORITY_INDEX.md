# 블랙스미스 기획 책임 원본 색인

> 상태: `PLANNING_IN_PROGRESS`
>
> 기준일: 2026-07-26
>
> 목적: 기획 문서가 여러 차례 갱신되면서 구형 규칙이 최신 규칙처럼 읽히는 문제를 방지한다.

## 1. 적용 우선순위

같은 주제의 규칙이 충돌하면 아래에서 **더 아래에 있는 최신 문서**가 우선한다.

1. `BLACKSMITH_MASTER_GAME_DESIGN_PLANNING.md`
   - 프로젝트 코어, 고객 생애주기, 거래·국가·역사 장비의 통합 배경
2. `BLACKSMITH_GROWTH_SYSTEM_PLANNING.md`
   - 제작·강화·화술·장비 분야 성장축 통합 구조
3. 성장 시스템 추가 결정 01~03
   - 각 시점의 결정 이력
   - `SUPERSEDED` 표기가 있는 내용은 구현 기준으로 사용하지 않음
4. `BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_04.md`
   - `[강화 한계 돌파]`와 강화 메인 포인트 공유의 최신 기준
5. `BLACKSMITH_PRECISION_ENHANCEMENT_BASELINE.md`
   - 정밀 등급 1개, 수식어 2개, 네 행동, 재료만 손실하는 실패의 최신 기준
6. `BLACKSMITH_INTEGRATED_POC_COMPLETION_BASELINE.md`
   - 통합 체험 POC 범위, POC 전용 수치, 자동·사람 검증 기준
7. `BLACKSMITH_GENRE_BENCHMARK_2026.md`
   - 유사 장르 비교와 개선 후보의 근거
   - 추가 결정 07에서 승인되거나 후순위로 이동한 항목은 최신 결정을 따름
8. `BLACKSMITH_POC_PRIORITY_BASELINE_2026.md`
   - 통합 POC 선행 6개 항목, 임시 수치, 자동 검증 선행 순서의 최신 기준
9. `BLACKSMITH_ENHANCEMENT_VALUE_BENCHMARK_2026.md`
   - 시나리오 런처 배포 범위와 강화 확률·판매가 비교 근거
   - 판매가 수정안은 사용자 승인 전까지 `PROPOSED_ONLY`
10. 최신 `BLACKSMITH_DECISION_LEDGER_ADDENDUM_*.md`
   - 승인·폐기·대체 상태와 문서 충돌 해결 기록

## 2. 현재 명시적 최신 덮어쓰기

### 분야별 기술 돌파

구형 문구:

- 무기·방어구·보조 장비·장신구별 확률형 돌파
- 특수 재료, 이해도, 보장선, 연구 시간

최신 규칙:

- 명칭은 `[강화 한계 돌파]`
- 강화 성장축의 메인 빌드 순차 트리
- 강화 메인 포인트 공유
- 영업 전 준비 단계에서 투자·회수
- 기본 활성 한계 +40, 이후 10강 단위 개방

책임 문서:

- `BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_04.md`
- `BLACKSMITH_DECISION_LEDGER_ADDENDUM_04.md`

### 정밀강화 슬롯과 실패

구형 문구:

- 수식어 슬롯 수 미정
- 실패 시 장비 상태 손실 가능성 미정

최신 규칙:

- 등급 관련 요소 1개
- 수식어 슬롯 2개
- 등급 결정·등급 강화·수식어 추가·수식어 강화
- 각 10강 이정표에서 행동 하나와 결과 한 번
- 실패 시 투입 강화 재료만 소모
- 실패해도 이정표가 종료되고 장비 상태는 유지

책임 문서:

- `BLACKSMITH_PRECISION_ENHANCEMENT_BASELINE.md`
- `BLACKSMITH_DECISION_LEDGER_ADDENDUM_05.md`

### POC 완료 범위

구형 문구:

- 검투사 장비 한 점의 +10 생애 경로만 구현된 POC

최신 확장 목표:

- 기존 Issue #34는 사람·플랫폼 검증을 위해 유지
- 후속 통합 POC는 +60 강화, 정밀강화, 한계 돌파, 보호·회복, 고객 2명, 거래·국가·밀수·역사·수집가 대표 경로를 체험 가능해야 함
- `기획 완료`와 `검수 완료` 전에는 후속 구현을 시작하지 않음

책임 문서:

- `BLACKSMITH_INTEGRATED_POC_COMPLETION_BASELINE.md`
- `BLACKSMITH_DECISION_LEDGER_ADDENDUM_05.md`

### 통합 POC 선행 우선순위

구형 문구:

- 오늘의 대장간 목표를 사람 검증 전에 배치
- 저위험 연속 강화와 실패 상한을 POC 이후 후보로 배치

최신 규칙:

1. POC 시나리오 런처
2. 장비 연대기 요약 카드
3. 위험·결과 사전 카드
4. 저위험 연속 강화
5. 기존 특수 타격을 이용한 실패 상한
6. 경제·성장 수치 조정
7. 통합 E2E·자동 검증
8. Android·접근성·성능·외부 플레이 검증

- 오늘의 대장간 목표는 `PROPOSED_ONLY / POST_POC`
- 상세 임시 수치는 `docs/planning/data/blacksmith_poc_priority_seed_2026.json`을 따른다.

책임 문서:

- `BLACKSMITH_POC_PRIORITY_BASELINE_2026.md`
- `BLACKSMITH_DECISION_LEDGER_ADDENDUM_07.md`

### POC 시나리오 런처 배포

최신 규칙:

- 개발·POC 빌드에서만 접근 가능
- 일반 출시 빌드에서는 메뉴와 진입 경로 제거
- `POC_TOOLS_ENABLED` 런타임 게이트 사용
- POC 전용 저장 프로필 사용
- 일반 플레이 저장 데이터 기록 금지

책임 문서:

- `BLACKSMITH_ENHANCEMENT_VALUE_BENCHMARK_2026.md`
- `BLACKSMITH_DECISION_LEDGER_ADDENDUM_08.md`
- `docs/planning/data/blacksmith_poc_priority_seed_2026.json`

### 공개시장 강화 가격

현재 적용값:

- +0 1,000
- +10 2,500
- +20 6,500
- +30 16,000
- +40 40,000
- +50 105,000
- +60 275,000

상태:

- `POC_TUNABLE / CURRENT`
- 외부 벤치마크와 내부 모의 비용에서 상승폭 부족 가능성이 확인됨
- +0 1,000 / +10 4,000 / +20 12,000 / +30 36,000 / +40 110,000 / +50 330,000 / +60 1,000,000은 `PROPOSED_ONLY`
- 사용자 승인 전에는 기존 JSON 값을 유지

책임 문서:

- 현재값: `docs/planning/data/blacksmith_poc_priority_seed_2026.json`
- 비교·제안: `BLACKSMITH_ENHANCEMENT_VALUE_BENCHMARK_2026.md`
- 상태 원장: `BLACKSMITH_DECISION_LEDGER_ADDENDUM_08.md`

## 3. 상태 해석

| 상태 | 의미 |
|---|---|
| `CONFIRMED` | 구조와 행동 규칙 승인 |
| `CONFIRMED_DIRECTION` | 출시 구조 방향 승인, 세부 수치는 조정 가능 |
| `CONFIRMED_SEQUENCE` | 구현·검증 순서 승인 |
| `POC_CONFIRMED` | 통합 POC 구현·검증에 사용할 정확한 값 또는 규칙 |
| `POC_TUNABLE` | 구조를 바꾸지 않고 데이터로 조정할 값 |
| `BENCHMARK_CONFIRMED` | 비교·분석 결과는 확인됐으나 신규 수치 승인을 의미하지 않음 |
| `REVIEW_REQUIRED` | 현재값에 문제 가능성이 있어 후속 결정을 요구함 |
| `PROPOSED_ONLY` | 사용자 승인 전 임의 확정 금지 |
| `SUPERSEDED` | 최신 문서로 대체됨 |
| `REJECTED` | 사용하지 않음 |

## 4. 구현자 확인 순서

구현 계획을 작성하기 전에 다음을 순서대로 확인한다.

1. 이 색인에서 해당 시스템의 최신 책임 문서 확인
2. 최신 결정 원장에서 `REJECTED`·`SUPERSEDED` 규칙 제외
3. `POC_CONFIRMED`와 출시 수치 분리
4. POC 임시 데이터 JSON과 책임 기획 문서의 값 일치 확인
5. `PROPOSED_ONLY` 가격 후보를 런타임에 적용하지 않음
6. Issue #34의 기존 구현·사람 검증 상태 확인
7. `기획 완료`와 `검수 완료` 게이트 확인

구형 마스터 문서나 벤치마크 후보 절만 읽고 구현을 시작하지 않는다.
