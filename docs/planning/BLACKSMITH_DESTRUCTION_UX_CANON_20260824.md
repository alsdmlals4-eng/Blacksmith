# [현재 정본] Blacksmith DESTROYED 기록·추모·후계 UX

- Parent: `BS-ENHANCE-20260820-05~09`, `BS-OVERHAUL-20260824-20`
- Cross-reference: `BS-CONTENT-20260811-09 / ITEM_UID_LINEAGE_STATE`
- Decision: `BS-DESTRUCTION-20260824-21`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

Blacksmith에서 `DESTROYED`는 물리 작품의 실제 생애 종료다. 같은 물리 UID는 일반 수리·대수선·강화·판매·정상 인계로 되살리지 않는다.

동시에 작품 UID·생애가 강화 선택의 기억을 증폭하는 보조축이므로 파괴 순간에 기록까지 삭제해서는 안 된다.

```text
PHYSICAL_ITEM_DIES
HISTORY_DOES_NOT_DIE
```

21은 파괴를 되돌리는 보상 시스템이 아니라 다음 네 요소를 승인한다.

```text
CAUSAL_DESTRUCTION
+ IMMUTABLE_HISTORY_ARCHIVE
+ CURATED_MEMORIAL
+ OPTIONAL_SUCCESSOR_PROVENANCE
+ ZERO_POWER_INHERITANCE
```

## 2. 승인안 — Archive + Curated Memorial + Optional Successor

### 2.1 물리 상태

```text
CURRENT == 0 or MAX == 0
→ physical state = DESTROYED
→ active physical item 사용 종료
```

DESTROYED 이후 금지:
- 사용
- 강화
- 일반 CURRENT 수리
- MAX 대수선
- 판매/정상 인계
- 같은 UID 부활

`BS-OVERHAUL-20260824-20`은 파괴 전의 마지막 구조 구제이며 DESTROYED revival이 아니다.

### 2.2 기록 상태

```text
ACTIVE_PHYSICAL_ITEM = false
DESTROYED_HISTORY_RECORD = true
```

파괴된 작품의 UID는 기록 키로 계속 존재할 수 있지만 물리 inventory entity로 다시 활성화하지 않는다.

## 3. Stage 1 — 파괴 순간 UX

파괴 직후의 P0 목적은 보상 제시가 아니라 **무슨 일이 일어났는지 설명하는 것**이다.

필수 표시:

```text
DESTROYED
작품명
ITEM_UID
파괴 직전 강화 단계
파괴 시도/사건
파괴 직전 CURRENT / MAX
직접 적용된 CURRENT/MAX 손실
CURRENT 또는 MAX 중 실제 0 도달 원인
직접 failure family 또는 world-event cause
```

대표 의미 예:

```text
검은별의 장검 +74
CURRENT 31 -> 0
MAX 47 -> 38
직접 원인: +75 강화 / FAIL_CRITICAL_DAMAGE
```

원인이 실제 데이터에 존재하면 `UNKNOWN`으로 축약하지 않는다. 원인을 재현할 evidence가 없을 때만 `UNKNOWN_CAUSE / EVIDENCE_MISSING`으로 구분하며 이를 정상 UX로 간주하지 않는다.

파괴 순간의 주 행동은 하나로 유지한다.

```text
결과 확인 -> 공방으로 돌아가기
```

파괴 팝업에서 즉시 다음을 기본 CTA로 밀지 않는다.
- 후계 작품 자동 생성
- 능력 상속
- 재료 환급
- 즉시 재도전 보너스
- 추모 고정 강요

## 4. Stage 2 — 불변 DESTROYED_HISTORY_RECORD

모든 파괴는 자동 archive record를 남긴다.

최소 보존 필드:

```text
ITEM_UID
작품명
최초 제작 provenance
주재료 / 제작 품질
최종 강화 단계
최고 강화 단계 / 최고 secured checkpoint
소유 이력
고객/세계 사건
주요 Chronicle provenance
손상 / 일반 수리 / MAX 대수선 이력
파괴 직전 CURRENT / MAX
최종 causal loss
실제 파괴 축 = CURRENT_ZERO | MAX_ZERO | BOTH_ZERO
파괴 target/event/cause
OVERHAUL_USED 여부와 대수선 기록
파괴 시점
```

History record는 inventory item, 거래 item, 복구 가능한 item이 아니다.

## 5. Stage 3 — 작품 연대기와 선택적 추모함

두 층을 분리한다.

```text
작품 연대기 / Archive
- 모든 DESTROYED UID 자동 보존
- 검색/필터 가능
- 오래됐다는 이유로 자동 삭제하지 않음

추모함 / Memorial
- Archive 중 플레이어가 중요하다고 선택한 작품을 강조 표시
- 고정 해제해도 Archive record는 삭제하지 않음
```

정확한 Memorial 고정 수는 현재 고정하지 않는다.

```text
MEMORIAL_CAP = UX_SCALE_TEST_REQUIRED
ARCHIVE_RETENTION = NO_FIFO_DELETION_BY_AGE
```

Memorial은 gameplay power source가 아니다.

금지:
- 추모 개수 기반 능력치
- 파괴 횟수 기반 Artistry/Chronicle 자동 성장
- memorial slot을 채우기 위한 destruction farming
- 오래된 record 자동 overwrite

## 6. Stage 4 — 선택적 후계 작품 관계

후계는 파괴 직후 자동 생성하지 않는다. 플레이어가 이후 실제 새 작품을 제작한 뒤 선택적으로 predecessor 관계를 연결할 수 있다.

```text
OLD_DESTROYED_UID -> PREDECESSOR_OF -> NEW_UID
OLD_UID != NEW_UID
```

새 작품은 자기 제작 provenance부터 시작한다.

### 6.1 상속 금지

다음을 새 UID에 복사하지 않는다.

```text
enhancement level
checkpoint
stats / existing power
affix
Artistry
Chronicle
failure recovery
CURRENT / MAX
spent gold
market premium
materials
old UID identity
```

즉 lineage는 provenance relation이며 power progression이 아니다.

```text
NO_UID_REWRITE
NO_HISTORY_TRANSFER_TO_SUCCESSOR
NO_LINEAGE_POWER_BONUS
NO_DESTRUCTION_FARMING_REWARD
```

### 6.2 표시

후계 작품에는 설명형 provenance를 표시할 수 있다.

```text
후계 작품
전작: <작품명 / UID>
```

이 표시는 stat/rarity/price modifier가 아니다.

## 7. 고객 소유 작품 파괴

고객 작품도 물리 작품 규칙은 동일하다.

```text
CUSTOMER != DESTROYED
ITEM_UID = DESTROYED
```

유지:
- 고객 identity
- 고객 관계/활동의 기존 기록
- 파괴 작품의 DESTROYED_HISTORY_RECORD

후속 새 장비:

```text
OLD DESTROYED UID = historical predecessor
NEW crafted item = NEW UID
```

21은 고객 신뢰도 고정 증감, 보상, 배상 수치, 고객별 감정 카피를 새로 만들지 않는다. 고객 반응은 해당 customer/world content owner가 실제 맥락으로 결정한다.

## 8. 파괴와 Chronicle 경계

파괴 자체만으로 무료 성장 보상을 지급하지 않는다.

```text
DESTRUCTION_EVENT != AUTOMATIC_ARTISTRY_GROWTH
DESTRUCTION_EVENT != AUTOMATIC_CHRONICLE_AFFIX
DESTRUCTION_EVENT != MATERIAL_REFUND
DESTRUCTION_EVENT != POWER_INHERITANCE
```

기존 Chronicle 권위가 실제 사건을 의미 있는 Chronicle로 판정할 수는 있지만, 21이 파괴 횟수를 progression resource로 만들지는 않는다.

## 9. 3안 비교

### A. Archive Only — REFERENCE_ONLY
- 단순하고 손실감이 강함.
- 그러나 작품 UID/생애 차별점과 다음 제작 동기를 충분히 활용하지 못함.

### B. Archive + Curated Memorial + Optional Successor — APPROVED
- 모든 기록을 보존하면서 시각 노이즈는 Memorial에서 플레이어가 선별.
- 후계는 relation만 이어지고 gameplay power는 이어지지 않음.
- 상실과 다음 제작 동기를 함께 유지.

### C. 즉시 후계/상속 보상 — REJECT
- 파괴 직후 progression 보상이 붙으면 destruction farming 또는 손실 희석 위험.
- Blacksmith의 `멈춤 vs 한 번 더` 판단을 약화함.

## 10. 외부 벤치마크 흡수

외부 게임의 구체 수치·UI를 복사하지 않고 원리만 사용한다.

- `XCOM 2 · ADAPT`: 영구 손실 캐릭터를 본거지 Memorial에서 계속 확인하는 원리. Blacksmith에서는 모든 파괴 기록은 Archive에 보존하고 일부를 Memorial로 강조한다.
- `Darkest Dungeon · ADAPT`: 사망자의 identity와 사망 맥락을 기록하는 원리. 작품명·강화/소유 이력·직접 파괴 원인을 남긴다.
- `Diablo IV Hall of Fallen Heroes community feedback · AVOID`: 제한 슬롯 때문에 의미 있는 오래된 기록이 새 기록에 밀려나는 문제를 피한다. Archive는 age-based FIFO 삭제를 사용하지 않는다.
- `Rogue Legacy 2 · REFERENCE / REJECT`: 계보 관계는 참고하지만 죽음 이후 power/progression 상속 구조는 Blacksmith에서 사용하지 않는다.

## 11. 5회 전체 적대 검토

### Loop 1 — 기록이 손실을 희석하는가
- physical UID는 영구 종료.
- Archive/Memorial은 사용 가능한 아이템을 부활시키지 않음.
- `PASS`.

### Loop 2 — death farming이 생기는가
- power/material/discount/automatic growth reward 없음.
- successor는 relation-only.
- `PASS`.

### Loop 3 — 숨은 즉사로 보이는가
- before state + causal loss + zero axis + cause를 결과 화면에 표시.
- evidence가 있는데 UNKNOWN으로 축약하지 않음.
- `PASS`.

### Loop 4 — Archive가 폭증하는가
- 모든 record는 compact archive, Memorial은 curated view.
- 정확한 scale/performance는 구현·실사용 검증 필요.
- `PASS_WITH_SCALE_TEST`.

### Loop 5 — successor가 복제처럼 보이는가
- new UID / new provenance / zero gameplay inheritance.
- predecessor relation만 허용.
- `PASS`.

Human emotion/attachment는 실제 플레이테스트 전 PASS를 주장하지 않는다.

## 12. 기존 runtime Reality

현행 historical runtime의 `scripts/enhancement/enhancement_session.gd`에는 과거 별도 destroy 확률과 파괴 시 성장 상태를 0/clear하는 처리가 남아 있다.

```text
old runtime:
DESTROY -> destroyed=true
         -> enhancement_level=0
         -> progression_attack=0
         -> affixes.clear()
```

이는 현재 06/13/21 계약의 구현 증거가 아니다.

현재 판정:

```text
DESIGN_CANON = VERIFIED
OLD_DESTROY_RUNTIME = CONTRADICTED / IMPLEMENTATION_DRIFT
CURRENT_MAX_CAUSAL_DESTRUCTION_RUNTIME = IMPLEMENTATION_UNVERIFIED
IMMUTABLE_HISTORY_ARCHIVE_RUNTIME = IMPLEMENTATION_UNVERIFIED
SUCCESSOR_PROVENANCE_RUNTIME = IMPLEMENTATION_UNVERIFIED
HUMAN_EMOTION = NOT_RUN
PRODUCT_IMPLEMENTATION = BLOCKED
```

구현 Gate가 열린 뒤에는 active physical state 종료와 immutable history record 생성을 분리해야 하며, historical state를 0/clear한 값만 저장해서 파괴 전 생애 evidence를 잃으면 안 된다.

## 13. 구현 입력 계약

구현 Gate 이후 최소 데이터 모델 후보:

```text
DestroyedHistoryRecord
- item_uid
- identity/provenance snapshot
- final progression snapshot
- ownership/lifecycle snapshot
- durability/destruction cause snapshot
- destroyed_at
- predecessor/successor relation refs (optional)

PhysicalItem
- active=false / destroyed=true
- no revive transition
```

정확 schema/API는 구현 단계 TDD에서 현재 save/UID owner를 fresh read하고 결정한다. 21은 새 runtime schema를 선구현하지 않는다.

## 14. Acceptance / Player Evidence

Technical acceptance 후보:
- DESTROYED 후 물리 사용/강화/수리/대수선 불가.
- 파괴 전 provenance/progression snapshot이 history에 보존.
- archive record age-based overwrite 없음.
- successor는 new UID.
- gameplay stat/progression inheritance 없음.

Human evidence 필요:
- 파괴 원인을 플레이어가 설명할 수 있는가.
- Archive/Memorial이 상실감을 지우지 않고 작품 기억을 강화하는가.
- 후계 관계가 복제/부활로 오해되지 않는가.
- 파괴 직후 UX가 다음 제작을 강요하지 않는가.

## 15. Implementation Reality Gate

```text
DECISION_21 = USER_APPROVED
GITHUB_CANON_SYNC = REQUIRED
NOTION_SYNC = REQUIRED
PRODUCT_RUNTIME = BLOCKED
OLD_RUNTIME_MATCH = CONTRADICTED
HUMAN_PLAYER = NOT_RUN
```

## 16. 다음 작업

```text
MAX_LEVEL_PAYOFF
-> FIRST_10_MINUTES
-> PRECISION_CUSTOMER_LINK
-> RELEASE_NEAR_VERTICAL_SLICE
```
