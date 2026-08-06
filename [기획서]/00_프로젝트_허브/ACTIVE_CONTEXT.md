# [현재 정본] Active Context

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`
>
> `R2_BATCH_006_NOT_STARTED_0_OF_10`

- 갱신: `2026-08-06 18:30 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 단계: `R2_CORE_SESSION_META_LOOP / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`
- 현재 승인 카운터: `0/10`
- 제품 구현: `BLOCKED`
- 사람 플레이테스트: `NOT_RUN`

```yaml
R2_CHECKPOINT_005: CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: NOT_STARTED_0_OF_10
PRODUCT_IMPLEMENTATION: BLOCKED
HUMAN_PLAYTEST: NOT_RUN
```

## 현재 권위

1. `CURRENT_CONFIRMED_DECISIONS.md`
2. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
4. 이 문서와 `ROADMAP.md`, `DEVELOPMENT_GATES.md`

PR #109는 Batch 005 기획 정본, PR #117은 체크포인트 폐쇄 정본, PR #118은 BCA 워크플로 복구로 병합됐다.

## 현재 게임 코어

```text
직접 단조
→ 제작 등급·예술성·역할 수치 확정
→ 일반 강화 지속·중단 판단
→ 정밀강화 방식·촉매 선택
→ 고객·일정에 작품 전달
→ 같은 UID의 결과·연대기·손상·복원
→ 다음 제작 판단
```

## 현재 승인 계약

### 작품·제작

- 제작 등급: `[보통] → [우수] → [명품] → [걸작] → [전설]`
- 최초 직접 단조 완료 시 확정하고 동일 UID에서 고정한다.
- 예술성은 `0` 이상의 정수이며 고정 설계 최대치가 없다.
- 수식어 슬롯은 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 개다.
- 보조재료 슬롯은 없다.
- 주재료는 장비군별 명시적 역할 적합성을 가진다.
- 직접 단조 결과는 역할별 3구간 판정으로 결정한다.
- 최초 역할 수치 프리셋은 `5 / 10 / 15`다.
- 작품 기본 중량은 장비군별 `0 / 5 / 10 / 15 / 20 / 30 WEIGHT_POINT`다.
- 기능 레시피는 역할·주재료·중량·상황·기능 용량을 함께 사용한다.

### 강화

- 일반 강화는 한 입력에 한 결과만 낸다.
- 일반 강화가 역할 원수치나 예술성을 자동 증가시키지 않는다.
- 정밀강화 이정표는 `+10 / +20 / +30 / +40 / +50`이다.
- 정밀강화 수치 패키지와 기능 재작업은 같은 이정표에서 상호배타다.
- 촉매 계보는 `EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED`다.

### 고객·일정·UX

- 고객 능력은 근력·기량·체력·판단력 `1~10`이다.
- 최대 중량은 `STRENGTH × 10 WEIGHT_POINT`; 초과 장비는 배정 불가다.
- 성공률의 주효과는 강화 단계이며 고객 능력·적성은 작은 보조 보정이다.
- 고객 카드는 기본 → 장비 선택 후 판단 → 상세 보기의 3단계 공개를 사용한다.
- 핵심 원인 2~4개를 설명하고 48dp·비색상 단독 신호 금지를 지킨다.
- 고객 개인 일정과 날짜 예고형 세계 일정을 분리한다.
- 작품 결과는 고객 결과, UID 상태·연대기, 다음 제작·복원 판단으로 환류한다.

## 현재 구현 현실

현재 Godot 코드는 `POC v0.6.4` 역사 구현이다. 실행·테스트 기반은 보존하지만 다음 요소는 현재 정본 구현으로 간주하지 않는다.

- `STANDARD / GOOD / PERFECT` 구형 품질
- 보조재료 입력
- 범용 `affixes` 배열
- 고정 3일 계약 중심 고객 판정
- 현재 기획과 다른 정확한 확률·배율

따라서 기존 POC를 그대로 확장하지 않고, 최신 정본을 소비하는 별도 버티컬 슬라이스 경로를 설계해야 한다.

## 다음 작업

1. Godot 버티컬 슬라이스 범위 승인
2. Batch 006에서 데모용 데이터 Schema·UID·저장 경계를 확정
3. 대표 콘텐츠 한 경로의 테스트 프리셋 작성
4. 별도 승인 후에만 제품 경로 구현
5. 내부 구조 테스트 후 외부 3~5명 사람 플레이테스트

과거 배치 진행 카운터와 PR 대기 문구는 역사 문서에서만 조회한다.

## 승인 Decision 호환 인덱스

다음 카운터는 현재 활성 상태가 아니라 Batch 005의 **역사적 승인 순서**다.

```text
BS-CRAFT-20260805-02 / R2_BATCH_005_1_OF_10
BS-CUSTOMER-20260805-01 / R2_BATCH_005_2_OF_10
BS-UX-20260805-01 / R2_BATCH_005_3_OF_10
BS-CUSTOMER-20260806-01 / R2_BATCH_005_4_OF_10
BS-ITEM-20260806-01 / R2_BATCH_005_5_OF_10
BS-ITEM-20260806-02 / R2_BATCH_005_6_OF_10
BS-ITEM-20260806-03 / R2_BATCH_005_7_OF_10
BS-ITEM-20260806-04 / R2_BATCH_005_8_OF_10
BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10
BS-ITEM-20260806-06 / R2_BATCH_005_10_OF_10
```

대표 예술성 표기는 `예술성 27`이며, 도메인은 `고정 설계 최대치 없음`이다.

## 불변 체크포인트 증거

다음은 현재 활성 단계가 아니라 삭제하면 안 되는 병합 이력이다.

- R2 체크포인트 004 기획 PR #106 squash merge: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
- R2 체크포인트 004 폐쇄 PR #107 squash merge: `7a46fa38586a42f268cd0432744203049649ddd5`
- R2 체크포인트 005 기획 PR #109 squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`
- R2 체크포인트 005 폐쇄 PR #117 squash merge: `06f03323c1309d8da0e6f5b9f4680a20ce388126`

## 역사 상태 호환 표기

- 체크포인트 004 제작 기획 상태: `MERGED_PR106 / MAIN_CANON`
- 이 표기는 현재 활성 배치가 아니라 불변 병합 이력이다.

## 역사 구현·회귀 기준선

다음은 현재 제품 구현 승인이 아니라 보존해야 하는 `[역사 증거]`다.

- 최신 역사 구현 배지: `POC v0.6.4 · main · 2026.07.23.1`
- 제작 모델 7건
- 제작 결과 통합 6건
- 정확한 구형 품질·피버 수치는 `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET`

## 강화 데이터 소유권

- 실패·위험·소재 소비 정책의 현재 역사 구현 소유자는 `data/crafting/enhancement_balance.json`이다.
- 정밀강화 이정표 구조의 현재 역사 구현 소유자는 `data/crafting/enhancement_milestones.json`이다.
- 버티컬 슬라이스는 이 파일의 구형 보조재료 계약을 정본으로 승격하지 않고, 최신 R2 Schema로 명시적으로 이관한다.
