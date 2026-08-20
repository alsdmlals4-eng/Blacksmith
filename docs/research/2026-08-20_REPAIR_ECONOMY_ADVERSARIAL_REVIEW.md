# Blacksmith 수리 경제 — 5회 전체 적대적 검토

- 대상: `BS-ENHANCE-20260820-10` 권장안
- 상태: `PROPOSED_REVIEW_EVIDENCE / USER_DECISION_REQUIRED`
- Work Mode: `PLAN`
- Human/Player evidence: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 검토 대상

권장 구조:

```text
0 < CURRENT < MAX
→ 한 번의 REPAIR_JOB
→ CURRENT = MAX
→ MAX unchanged
```

비용 기준:

```text
missing_current_points = MAX - CURRENT

repair_cost
= REPAIR_REFERENCE_COST[structural_family, secured_band]
× (setup_fraction + variable_fraction × missing_current_points / 100)
```

첫 제안 shell:

```text
setup_fraction = 0.05
variable_fraction = 0.65
```

`REPAIR_REFERENCE_COST`는 시장 판매가가 아니라 안정된 구조 수리 참조값이며 최종 판매가·예술성·수식어·연대기·고객 수요·실제 다음 강화비에 직접 연동하지 않는다.

---

## Loop 1 — 작은 손상마다 수리가 자동 정답인가

### 공격

순수 비례 비용이면 `CURRENT -1~-5` 같은 작은 손상이 거의 공짜다.

그 결과:
- 모든 실패 직후 수리
- `그대로 한 번 더` 판단 소멸
- 수리 화면이 반복 클릭 단계로 변함

### 대안

1. 비례 비용만 사용
2. 최소 수리 가능 손상 threshold를 둠
3. **고정 준비비 + 비례 비용 + 한 번의 공방 작업**

### 방어

3을 채택 후보로 유지한다.

- 고정 `setup_fraction`으로 아주 작은 수리에도 최소 부담을 만든다.
- `REPAIR_JOB` 한 번이 공방 작업 기회와 경쟁한다.
- 자동수리와 부분수리를 첫 Vertical Slice에서 제외한다.

### 재검사

작은 손상은 모아서 수리할 이유가 생기고, 낮은 CURRENT에서는 큰 회복량 때문에 수리가 자연스럽게 매력적이다.

**Loop 1 판정: PASS_WITH_TUNING.**

---

## Loop 2 — 반대로 수리를 아무도 선택하지 않는가

### 공격

작업량과 비용을 함께 부과하면 수리보다 새 작품 제작 또는 무리한 강화가 항상 싸질 수 있다.

그 경우 CURRENT는 선택 자원이 아니라 죽기 전 숫자 표시가 된다.

### 방어

- 한 번의 `REPAIR_JOB`으로 부분이 아니라 CURRENT 전체를 MAX까지 회복한다.
- 중·대 손상의 일반 수리비는 동일 경험 밴드의 일반 강화 1회 참조비용보다 대체로 낮게 시작한다.
- MAX를 고치지 않으므로 수리를 싸게 만들어도 고위험 강화의 장기 리스크는 남는다.
- 정확 DAY_WORK_COST는 아직 확정하지 않고 수리 1행동이라는 구조만 고정 후보로 둔다.

### 재검사

수리는 즉시 파괴 위험을 낮추는 강한 선택이지만 MAX scar·성공률 페널티·신규 강화 효과 감소를 없애지 않는다.

**Loop 2 판정: PASS.**

---

## Loop 3 — 수리비 공식이 작업 순서 최적화를 강요하는가

### 공격

`최종 판매가 × 손상률`을 쓰면:
- 수식어를 붙이기 전에 수리
- 예술성이 오르기 전에 수리
- 연대기 가치가 생기기 전에 수리
- 강화 성공 전에 수리

같은 비용 최적 순서가 만들어질 수 있다.

`다음 강화비 × 손상률`도 체크포인트 특수 강화 비용 폭증 때문에 비슷한 문제를 만든다.

### 외부 사례

Diablo IV는 마법부여 비용이 판매가에 묶여 플레이어가 대장장이 업그레이드/각인 전에 재굴림해야 가장 싸지는 순서 문제를 만들었고, Blizzard가 비용 기준을 기본 아이템 위력/유형으로 변경했다.

### 방어

수리 공식에서 다음을 제외한다.

```text
final sale value
affix premium
artistry premium
chronicle premium
customer demand
actual next attempt cost
current success chance
failure recovery progress
```

대신 같은 확보 밴드 안에서 안정된 `REPAIR_REFERENCE_COST` table을 사용한다.

### 재검사

수리 견적은 작품의 외부 가치 연출이나 특수 강화 순간에 따라 출렁이지 않는다.

**Loop 3 판정: PASS.**

---

## Loop 4 — MAX 흉터를 수리비로 이중 처벌하는가

### 공격

수리량을 `(MAX-CURRENT)/MAX`로 계산하면:

```text
MAX 50 / CURRENT 20
```

은 30pt만 복구하지만 비율상 60% 결손으로 읽힌다.

MAX가 낮은 작품은 이미:
- 강화 성공 기대 감소
- 심각 구간 신규 강화 효과 감소

를 받고 있으므로 수리비까지 MAX 비율로 할증하면 삼중 벌점이 된다.

### 방어

오직 절대 결손 포인트를 쓴다.

```text
missing_current_points = MAX - CURRENT
```

MAX 자체는 일반 수리 가격 multiplier가 아니다.

### 재검사

MAX는 장기 구조 리스크, CURRENT는 단기 생존/수리 비용으로 역할이 분리된다.

**Loop 4 판정: PASS.**

---

## Loop 5 — 수리가 유지보수 노가다/경제 흡수구로 변하는가

### 공격

다음이 결합되면 강화보다 수리가 더 많은 시간을 먹는다.

- 자동 일일 마모
- 부분 수리 반복
- 여러 수리 전용 재료
- 수리 성공/실패 미니게임
- MAX까지 일반 수리 가능
- 매 손상 자동 알림/자동 수리

### 방어

첫 Vertical Slice 일반 수리에는 다음을 금지한다.

```text
passive daily durability tax
partial repair spam
repair success RNG
repair-only currency
normal MAX restoration
auto-repair
```

허용:

```text
single repair quote
single confirm action
CURRENT → MAX
existing gold/common structural materials
```

### 재검사

수리는 강화 선택의 비용·기회비용을 제공하지만 독립 메인 루프가 되지 않는다.

**Loop 5 판정: PASS.**

---

## Better Alternative Search

### A. 최종 시장가 기반

`repair_cost ∝ final_sale_value × missing`

- 직관적.
- 가치 구성요소 중복 과금과 작업 순서 악용 위험 큼.
- `REJECT`.

### B. 실제 다음 강화비 기반

`repair_cost ∝ next_attempt_cost × missing`

- 수리/강화 비교 쉬움.
- 특수 체크포인트 비용 폭증과 완료 작품 처리 문제가 있음.
- `REJECT_AS_RUNTIME_FORMULA`.
- Balance 검증용 비교 기준으로만 사용.

### C. 안정된 수리 참조비용 + 준비비 + 절대 결손 포인트 — 권장

- 외부 가치와 분리.
- MAX 이중 과금 방지.
- 작은 손상 자동 수리 억제.
- 한 행동으로 큰 손상 회복 가능.
- 데이터 테이블로 독립 튜닝 가능.

**최종 권장: C.**

---

## 첫 수치 shell

```text
setup_fraction = 0.05
variable_fraction = 0.65
```

표준 참조비용 `R` 대비:

```text
missing 1~20pt  ≈ 6~18% R
missing 21~50pt ≈ 19~38% R
missing 51~75pt ≈ 38~54% R
missing 76~99pt ≈ 54~69% R
```

모두 `PROPOSED_BASELINE_TEST_PRESET / NOT_FINAL`.

`R` 자체는 기본 작품 구조/주재료/확보 위험 밴드별 data table로 두고, 실제 다음 특수 강화 비용을 런타임에서 직접 참조하지 않는다.

---

## 검증 신호

### 너무 싼 경우

- 1~10pt 손상 후 대부분 즉시 수리.
- 손상 상태를 거의 보지 않고 수리부터 누름.
- 수리하지 않고 추가 강화하는 사례가 사라짐.

### 너무 비싼 경우

- CURRENT가 매우 낮아도 수리를 거의 하지 않음.
- 새 작품 제작이 항상 일반 수리보다 이득.
- 수리 때문에 강화 세션이 반복적으로 끊김.

### 적절한 경우

- 높은 CURRENT에서는 손상을 감수하는 사례가 흔함.
- 낮은 CURRENT에서는 수리가 강하게 매력적이나 비용/작업 기회를 아끼고 밀어붙이는 사례도 존재.
- 수리 후에도 MAX 리스크가 남는다는 점을 이해함.

---

## 재검토 조건

- 수리 선택률이 거의 0% 또는 거의 100%로 수렴.
- 작은 손상마다 수리가 루틴화.
- 수리비 때문에 작품의 예술성/연대기/수식어 가치 획득 순서를 최적화해야 함.
- 낮은 MAX 작품이 일반 수리에서도 별도 할증되어 폐기 압력이 과도함.
- 수리 경제가 강화 경제보다 더 많은 재화/작업 시간을 소비.
- 수리 견적을 이해하려면 시장가/강화 기대값 계산기가 필요함.

## CLEAN EXIT 경계

- 5회 전체 적대 검토 완료.
- 권장 C는 구조적으로 유지 가능.
- 정확 `REPAIR_REFERENCE_COST` table, 골드/재료 분배, DAY_WORK_COST는 사용자 승인 후 시뮬레이션 입력으로 정교화.
- `BS-ENHANCE-20260820-10`: `PROPOSED_ONLY / USER_DECISION_REQUIRED`.
- 제품 구현: `BLOCKED`.
