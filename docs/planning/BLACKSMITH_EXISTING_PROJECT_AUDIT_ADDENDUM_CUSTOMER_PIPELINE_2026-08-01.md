# Blacksmith 기존 프로젝트 감사 보완 — 고객 공통 파이프라인

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A6`
>
> Decision ID: `BS-CUSTOMER-PIPELINE-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

현행 장비 생애 PoC는 기본 고객 `gladiator_kyle`, 정확 장비 `iron_sword`, 세계 event `gladiator_match`, 단일 관계 정수를 중심으로 동작한다.

최신 정본은:

- 수집가·모험가·검투사·군인 4유형
- 유형별 최소 2명 이름 고객
- 범주 eligibility와 공개 fit 분리
- 고객별 관계·계약·소유권·유형별 세계 결과
- 공통 ResultEnvelope·CampaignSnapshot

을 요구한다.

## 2. 해결된 기획 목표

`BS-CUSTOMER-PIPELINE-20260801-01`로 다음을 확정했다.

- 이름 고객 8명과 영구 Customer ID
- 카일 구형 ID를 `KYLE_VAREN`으로 이전
- 모험가 대표 `NADIA_VENN`, 군인 대표 `MAREK_OLDEN`
- CustomerType·NamedCustomer·RequestTemplate·Contract·Relationship 공통 모델
- exact item ID가 아닌 장비 범주 의뢰
- eligibility와 공개 fit 분리
- DeliveryIntent 원자 트랜잭션
- 유형별 Profile·공통 Resolver
- 고객별 관계 저장
- 공통 Customer Board·Delivery·World Result UX
- 카시아·에르사·나디아·마레크 재사용 증명

## 3. Finding 판정

| Finding | 기획 목표 | 런타임·콘텐츠 |
|---|---|---|
| `BS-AUD-F07` | RESOLVED | OPEN |
| `BS-AUD-F08` | RESOLVED | OPEN |
| `BS-AUD-F09` 고객 통합 | RESOLVED | OPEN |
| `SHEET-F05` | RESOLVED | 데이터 fixture OPEN |

P0 Finding 수는 실제 공통 코드·데이터·화면·fixture·저장 검증 전까지 유지한다.

## 4. 적대적 실패 조건

```text
고객 이름별 Core Engine 분기
exact iron_sword ID 요구
낮은 fit 장비 판매 차단
자동 장비 추천·선택
동일 납품 이중 보상
동일 세계 결과 이중 적용
결과 화면에서 RNG 재호출
소유권·관계·보상·Registry 부분 저장
legacy Kyle 관계·장비 이력 손실
```

## 5. 상태

```text
CUSTOMER_PIPELINE_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
PRODUCT_CODE_DATA_UI: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
ANDROID_HUMAN_TESTS: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
