# Blacksmith Decision Ledger Addendum 20

> 상태: `USER_APPROVED / CURRENT`
>
> 승인일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 구현 권한: `NONE`

## BS-CUST-20260731-01 — 고객 4유형과 유형별 복수 고객

### 결정

```text
CUSTOMER_TYPE_COUNT: 4
CUSTOMER_TYPES:
- COLLECTOR
- ADVENTURER
- GLADIATOR
- SOLDIER
NAMED_CUSTOMERS_PER_TYPE_MINIMUM: 2
ALL_TYPES_SIMULTANEOUS_IN_ONE_SESSION: FORBIDDEN
ACTIVE_REQUEST_LIMIT: 2
```

- 고객 유형은 수집가·모험가·검투사·군인 4개다.
- 각 유형에는 여러 명의 이름 있는 고객이 존재한다.
- 유형은 공통 세계 결과 파이프라인이고, 이름 고객은 개별 목표·성격·예산·선호·관계·사건을 가진다.
- 카시아 벨란은 검투사 대표, 에르사 로엔은 수집가 대표로 유지한다.
- 모험가·군인 대표와 유형별 추가 고객의 이름·아트·대사는 별도 콘텐츠 승인 대상이다.
- 4유형은 전체 콘텐츠 구조이며 한 15~25분 세션의 고정 4명을 의미하지 않는다.

### 관계

- `clarifies: BS-V9-20260731-06`
- `restores_from_legacy: PR61 v6 customer archetypes`
- `supersedes_interpretation: ONLY_CASSIA_AND_ERSA_EXIST`

## BS-ENH-20260731-01 — +50 일반·고위 정밀강화 이원화

### 결정

```text
PLUS_49_TO_50_ROUTE_COUNT: 2
ROUTES:
- GENERAL_PRECISION
- HIGH_PRECISION
```

### 일반 정밀강화

- 특수재료를 사용하지 않는다.
- +40대 기존 정밀강화 성공·유지·하락·파괴·보호 규칙을 그대로 사용한다.
- 성공 시 +50에 도달하고 일반 정밀강화 결과를 적용한다.
- 진화와 대표 특수 수식어는 발생하지 않는다.
- 일반 +50도 정상 완성품이며 +51 이상과 명작 전당 자격을 가진다.

### 고위 정밀강화

- 등록된 특수재료를 촉매 또는 특수 보조재료로 사용한다.
- +49→+50 시도 자체가 고위 정밀강화다.
- 확정 성공하며 실패·유지·하락·파괴가 없다.
- 실행 전 유효 후보 2~3개를 공개하고 하나를 선택한다.
- +50, 진화 또는 특수 형태, 대표 특수 수식어를 확정한다.
- 고비용·희귀 재료·결과 방향 선택이 긴장을 담당한다.

### 역할

- 촉매: 주 진화·특수 수식어 계열 결정
- 특수 보조재료: 기존 계보 기반 후보 추가·제한·변주
- 둘을 함께 쓰면 촉매가 주계열, 보조재료가 변주를 담당

### 관계

- `clarifies: BS-V9-20260731-03`
- `restores_from_legacy: PR61 Addendum 01`
- `supersedes_interpretation: ALL_PLUS_50_ALWAYS_EVOLVE`

## 공통 Gate

```text
GITHUB_DRAFT: UPDATE_REQUIRED
PLANNING_DATA: UPDATE_REQUIRED
GOOGLE_SHEET: UPDATE_REQUIRED
MAIN_MERGE: NOT_RUN
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```
