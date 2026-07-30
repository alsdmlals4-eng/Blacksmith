# Blacksmith v9 승인 결정 정본 인덱스

> 상태: `USER_APPROVED_DECISIONS / CANONICAL_ID_INDEX`
>
> 기준일: `2026-07-31`
>
> 원결정: `BLACKSMITH_V9_USER_DECISION_PACKET.md`, `BLACKSMITH_DECISION_LEDGER_ADDENDUM_20.md`
>
> 동기화 계약: `BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md`

## 목적

기존 사용자 승인 내용과 최신 보완 결정을 변경 없이 식별자 기반으로 정규화해 GitHub 계획 데이터와 Google Sheet가 동일한 Decision ID를 사용하도록 한다.

## 결정 목록

### BS-V9-20260731-01 — 제작 등급

```text
보통 → 양질 → 우수 → 명품 → 걸작
```

- 단조 시 확정되는 영구 작품 정보
- 강화 단계와 분리
- 낮은 등급도 강화·판매·보관 가능

### BS-V9-20260731-02 — 수식어 구조

```text
계보 수식어 1개 + 보조 수식어 최대 2개
```

- +50 대표 특수 형태는 새 슬롯이 아니라 계보 승격
- 무제한 슬롯 증가 금지

### BS-V9-20260731-03 — 10단위 정체성 이정표

- +10 계보 선택
- +20 보조 1개 선택
- +30 계보 강화·파생 선택
- +40 보조 2개째 선택
- +50 세부 경로는 `BS-ENH-20260731-01`이 명확화
- +60 이상 신규 슬롯 없이 심화
- 이정표 성공 후 별도 두 번째 실패 판정 금지

### BS-V9-20260731-04 — 고객 거래 자격과 공개 적합도

```text
거래 자격 = 범주 일치 + 제작 완료 + 판매 가능 + 플레이어 보유
공개 적합도 = 제작 등급·수식어·진화·연대기와 고객 가치관의 일치
```

- 낮은 적합도도 거래 가능
- 평가 이유 공개
- 자동 추천·선택 금지

### BS-V9-20260731-05 — 장비 운명 상태

- 수치형 내구도와 반복 수리 없음
- 정상·전투 흔적·분실·회수·영구 파괴 사용
- 전투 흔적은 사용 불가 상태가 아닌 서사 상태

### BS-V9-20260731-06 — 대표 콘텐츠 증명 세트

- 대표 세션은 검투사 카시아
- 별도 결정론적 증명 세트는 수집가 에르사
- 같은 요청·판매·소유권·결과·저장 구조 재사용
- 전체 고객 구조는 `BS-CUST-20260731-01`이 명확화

### BS-V9-20260731-07 — 미래 명작 전당

- +50 이상 작품의 선택적 비교·전시
- 검증 랭킹과 레거시 전시 분리
- 단일 종합 전투력 점수 금지
- 성능 보상 없음
- 등록 실패가 로컬 작품에 영향 없음

### BS-V9-20260731-08 — 벤치마킹 선행 원칙

- 새 시스템·핵심 규칙·콘텐츠 구조·주요 UX 흐름 설계 전 벤치마킹 필수
- 매 작업마다 대규모 조사 반복 금지
- 최근 관련 조사 재사용 허용
- 채택·변형·제외와 전파·검증 기록 필수

### BS-CUST-20260731-01 — 고객 4유형과 유형별 복수 고객

```text
고객 유형 = 수집가·모험가·검투사·군인
유형별 이름 고객 최소 2명
```

- 고객 유형은 공통 세계 환류 파이프라인이다.
- 이름 고객은 개별 목표·성격·예산·선호·관계·사건을 가진다.
- 카시아는 검투사 대표, 에르사는 수집가 대표다.
- 4유형은 한 세션의 고정 4명이 아니다.
- 동시 활성 요청은 최대 2개다.
- 고객 전용 핵심 엔진 금지
- `clarifies: BS-V9-20260731-06`

### BS-ENH-20260731-01 — +50 일반·고위 정밀강화 이원화

```text
+49→+50
├─ 일반 정밀강화: 기존 위험 규칙, 특수 수식어 없음
└─ 고위 정밀강화: 특수재료 사용, 확정 성공, 특수 수식어 획득
```

- 고위 정밀강화의 특수재료는 촉매 또는 특수 보조재료 역할을 가질 수 있다.
- 촉매는 주 진화 계열, 특수 보조재료는 후보·변주를 책임진다.
- 고위 경로는 유효 후보 2~3개를 실행 전에 공개한다.
- 일반 +50도 정상 완성품·+51 이상·명작 전당 자격을 가진다.
- +50 경로와 특수재료 역할을 별도 데이터로 저장한다.
- `clarifies: BS-V9-20260731-03`

### BS-SYNC-20260731-01 — 기획 정본 즉시 동기화

- 주요 변경과 승인 내용은 GitHub 권위 문서·계획 데이터·연결 Sheet에 즉시 반영
- 모든 대상에 같은 Decision ID 사용
- 변경 위치·PR·커밋·Sheet 범위·검증 상태 기록
- 병합 전 `SYNCED_TO_DRAFT`, 병합 후 `SYNCED_TO_MAIN`

## 권한

충돌 시 권한 순서:

```text
사용자 최신 결정
→ BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md
→ BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md
→ BLACKSMITH_V9_USER_DECISION_PACKET.md·Decision Ledger Addenda
→ 본 ID 인덱스
→ 연결 계획 데이터와 Google Sheet
```

## 동기화 상태

```text
GITHUB_AUTHORITY: GITHUB_DRAFT_COMMITTED
PLANNING_DATA: GITHUB_DRAFT_COMMITTED
GOOGLE_SHEET: SYNCED_TO_DRAFT_PR81
CROSS_SOURCE_VERIFICATION: PASS
FORMULA_ERROR_RECHECK: PASS_ON_DIRECTLY_AFFECTED_TABS
MAIN_MERGE: NOT_RUN
USER_기획_완료: NOT_DECLARED
```
