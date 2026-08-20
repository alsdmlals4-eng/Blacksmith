# [현재 승인] Blacksmith 강화 체크포인트·내구도 파괴 계약

- Parent: `BS-CORE-20260820-01`
- Refines: `BS-ENHANCE-20260820-03`
- Decisions: `BS-ENHANCE-20260820-05`, `BS-ENHANCE-20260820-06`
- 사용자 승인: `2026-08-20 KST / 권장안 진행 + 내구도 % 감소, 0% 파괴`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- 기준 main: `e714b864ebbdbd73c0b0714f93296044dcf619ee`

## 1. BS-ENHANCE-20260820-05 — 확보점 보호 + 구간 내 제한 단계 하락

강화 단계는 주요 이정표에서 확보된다.

```text
CHECKPOINT
→ 구간 내 추가 강화
→ 실패 시 유지 / 제한 단계 하락 / 내구도 손상 중 결과
→ 현재 체크포인트 아래로는 내려가지 않음
→ 다음 체크포인트 도달 시 새 바닥 확보
```

현재 승인된 정밀강화 이정표 `+10 / +20 / +30 / +40 / +50`은 첫 Balance Budget의 체크포인트 후보로 재사용한다. 정확한 최종 체크포인트 간격은 플레이테스트 전 `TUNABLE`이며, 이 Decision이 +10 간격을 영구 고정하지 않는다.

### 보호 규칙

- `LEARN` 구간에서는 단계 하락을 사용하지 않는다.
- 최초 의미 있는 확보점에 도달한 뒤부터 제한 단계 하락을 사용할 수 있다.
- 기본 제품 후보의 한 번 실패 단계 하락은 **최대 1단계**부터 테스트한다.
- 다단계 대폭 하락을 기본 긴장 수단으로 사용하지 않는다.
- 체크포인트 아래로 하락하지 않는다.
- `FAIL_DOWNGRADE`와 심각 내구도 손실을 같은 실패에서 기본 중첩하지 않는다. 한 실패가 단계·내구도·경제를 동시에 과도하게 벌주지 않는다.
- 모든 실패는 `BS-ENHANCE-20260820-02`의 실패 누적 회복 진전을 남긴다.

## 2. BS-ENHANCE-20260820-06 — 내구도 0~100% 상태와 0% 물리 파괴

기존 작품 공통 원수치 `DURABILITY`의 현재 제품 의미를 **정수형 능력치**에서 **현재 상태형 퍼센트**로 정제한다.

```yaml
DURABILITY_PERCENT:
  type: integer
  minimum: 0
  maximum: 100
  new_item_default: 100
  persistence: ITEM_UID_OWNED
  display: ALWAYS_VISIBLE_WHEN_RELEVANT
```

### 상태 의미

```text
100%                : 새 작품의 기본 완전 상태
1~99%               : 사용/강화 실패로 마모·손상된 살아 있는 작품
0%                   : DESTROYED
```

`0%`에 도달하면 해당 물리 작품은 **파괴**된다.

- 장비 사용 불가.
- 추가 강화 불가.
- 고객에게 정상 장비로 인계 불가.
- 일반 `REPAIR / RESTORE`로 물리 작품을 되살리지 않는다.
- 동일 UID의 물리 아이템을 새 제품 상태로 부활시키지 않는다.

그러나 Blacksmith의 작품 생애 정체성을 위해 다음 기록은 삭제하지 않는다.

```text
ITEM_UID
작품 이름
최초 제작·재료·등급
강화 이력과 확보한 최고 체크포인트
소유 이력
고객·세계 사건
손상·수리·복원 이력
파괴 시점과 직접 원인
Chronicle provenance
```

따라서 `DESTROYED`는 `DATA_DELETED`가 아니다. 물리적으로는 끝난 작품이지만 역사/도감/연대기/후속 고객 반응에서 참조 가능한 최종 생애 상태다.

## 3. 내구도 감소 소유권

내구도는 **시간 경과만으로 자동 감소하지 않는다.** 실제 원인이 있는 사건만 감소시킨다.

허용 원천:

1. 강화 실패 중 내구도 손상 결과
2. 고객/세계 일정의 실제 마모·충격·환경 노출 사건
3. 별도로 승인된 고위험 제작·재작업 결과

금지 원천:

- 단순 하루 종료
- 메뉴 열기/닫기
- 판매/소유권 이전 자체
- 전시 횟수 자체
- 저비용 반복으로 내구도를 의도적으로 깎아 보상을 파밍하는 행위

## 4. 강화 실패 결과와 내구도

강화 실패 결과는 상호 구분한다.

```text
FAIL_HOLD
- 단계 유지
- 내구도 기본 유지
- 비용/작업량 소비 가능
- 실패 누적 회복 증가

FAIL_DOWNGRADE
- 체크포인트 이상에서 최대 1단계 하락부터 테스트
- 내구도 기본 유지
- 실패 누적 회복 증가

FAIL_DAMAGE
- 단계 기본 유지
- DURABILITY_PERCENT 감소
- 실패 누적 회복 증가

FAIL_CRITICAL_DAMAGE
- 명시적 고위험 구간/선택에서만 발생 후보
- 큰 DURABILITY_PERCENT 감소
- 0% 도달 가능
- 실패 누적 회복 증가
```

정확한 감소량과 결과 확률은 `BALANCE_BUDGET / USER_PLAYTEST_REQUIRED`다.

## 5. 0% 파괴 판정

모든 내구도 감소는 원자적으로 다음 순서를 따른다.

```text
current_durability
→ causal durability loss
→ max(0, current - loss)
→ 0이면 DESTROYED
→ 파괴 event와 cause 기록
```

0%를 지나 음수로 저장하지 않는다.

### 파괴의 인과성

파괴 전에는 플레이어가 다음을 알 수 있어야 한다.

- 현재 내구도 `%`
- 이번 시도에서 내구도 손실이 가능한지
- 가능한 주요 손실 범위 또는 파괴 가능성
- 보호 수단이 있다면 무엇을 막는지

숨은 즉사 판정으로 0%를 만들지 않는다.

## 6. 수리·복원

### 1~99%

- 공방에서 `REPAIR`로 내구도를 회복할 수 있다.
- 고객/세계 맥락에서 승인된 `FIELD_SERVICEABILITY`는 제한적인 현장 회복만 제공한다.
- 수리 비용·회복량·작업량은 강화 위험과 경쟁하는 기회비용이어야 한다.
- 수리는 강화 단계, 제작 등급, 예술성, 수식어를 자동 상승시키지 않는다.
- 수리 반복으로 새 Chronicle/Artistry를 자동 파밍하지 않는다.

### 0%

- 일반 수리 불가.
- 일반 복원 불가.
- 물리 아이템은 `DESTROYED`로 고정.
- 기록 보존만 허용.

미래에 `RELIC_REFORGE / SUCCESSOR_ITEM` 같은 별도 시스템을 만들 경우 새 UID로 시작해야 하며 이전 작품의 강화·성장 수치를 복사하지 않는다. 별도 사용자 승인 전에는 `OUT_OF_SCOPE`다.

## 7. 기존 DURABILITY 문서 정제

다음 구형/현재 문서의 `DURABILITY` 정수 원수치 표현은 이 Decision 이후 **퍼센트 현재 상태**로 해석한다.

- `docs/planning/BLACKSMITH_R2_ITEM_ROLE_STAT_AND_INITIAL_FUNCTION_CATALOG_CANON_2026.md`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`
- 이를 소비하는 Soldier/Gladiator 등 현재 콘텐츠

예전 `내구도 18` 같은 숫자는 역사 설계 표현이며 새 제품 UI 계약이 아니다.

`ENVIRONMENTAL_SEALING`은 특정 환경의 내구도 손실을 완화할 수 있고, `FIELD_SERVICEABILITY`는 1% 이상인 작품의 제한 현장 회복에 사용할 수 있다. 둘 다 0% 파괴를 자동 무효화하지 않는다.

## 8. 화면 계약

강화 메인 화면의 P0 정보:

```text
현재 강화 단계
현재 체크포인트
현재 내구도 NN%
성공 확률
시도 비용
실패 결과군
내구도 손실/파괴 가능성
실패 누적 회복
다음 체크포인트
```

내구도는 색상만으로 전달하지 않고 숫자 `%`를 항상 함께 표시한다.

저내구도 경고 threshold의 정확한 구간은 Visual/Balance test 값이며 아직 고정하지 않는다.

## 9. DDD 연결

내구도는 별도 생존 게이지가 아니라 강화 DDD의 **손실 감각**을 담당한다.

```text
강화 성공 욕구
+ 현재 작품의 가치
+ 체크포인트로 확보한 진전
+ 남은 내구도
= 지금 멈출지 더 도전할지의 실제 긴장
```

성공 시 내구도를 기본 소비하지 않는다. 성공 보상과 실패 손실의 경계를 선명하게 유지한다.

내구도가 낮을수록 무조건 강화를 금지하지 않는다. 위험을 알고도 계속 도전할 수 있어야 하며, 0% 파괴 가능성은 명확히 공개한다.

## 10. 벤치마크 해석

### Nintendo · Breath of the Wild — `ADAPT`

Nintendo 공식 Explorer's Guide는 무기가 사용으로 손상되어 결국 파괴되고, 플레이어가 상태를 확인하고 파괴 전 판단하도록 설명한다. 또한 특별한 일부 무기는 파괴 후 별도 재료로 재제작되는 예외 구조를 가진다.

Blacksmith는 `상태를 보고 파괴 위험을 판단`하는 원리는 채택하되, 대량 교체 무기 게임이 아니므로 파괴된 작품의 UID·생애 기록을 보존한다.

Reference:
- `https://assets.nintendo.com/image/upload/v1675114089/Microsites/zelda-breath-of-the-wild/pdf/ExplorersGuide.pdf`

### FINAL FANTASY XIV · Durability — `ADAPT / REJECT`

FFXIV 공식 UI Guide는 내구도를 퍼센트로 표시하며 0%에서 장비 효과가 사라지지만 아이템은 인벤토리에 남아 수리 가능하다고 설명한다.

Blacksmith는 `0~100% 명시 상태와 사전 관리`는 채택한다. 그러나 사용 불가 후 즉시 수리해 같은 물리 작품을 되살리는 구조는 사용자의 최신 `0% 파괴` 결정과 충돌하므로 비채택한다.

Reference:
- `https://na.finalfantasyxiv.com/uiguide/equipment/equipment-repair/uiguide_faq_display_q00018.html`

## 11. 정확 수치 경계

아직 확정하지 않는다.

```yaml
balance_budget_needed:
  fail_damage_loss_range_percent:
  critical_damage_loss_range_percent:
  world_wear_loss_range_percent:
  repair_cost_curve:
  repair_amount_percent:
  protection_cost:
  protection_effect:
  checkpoint_interval:
  fail_downgrade_probability:
  damage_probability:
  critical_damage_probability:
  max_bad_luck_window:
```

모든 값은 `TUNABLE / USER_PLAYTEST_REQUIRED`다.

## 12. 구현/검증 경계

- 이 Decision은 기획 계약이다.
- `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 변경 금지.
- 기존 런타임의 `DESTROY -> item deletion/zeroed state`, raw durability 숫자, 다단계 downgrade는 현재 제품 의미로 자동 승격하지 않는다.
- Human/Player validation: `NOT_RUN`.
- Android/accessibility/performance: `NOT_RUN`.
