# Max Durability Structural Scar Design

- Date: 2026-08-20 KST
- Project: Blacksmith
- Path: Architectural planning
- Product implementation: BLOCKED
- Canon owner: `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`

## Intent

일반 내구도 수리만으로 강화 위험을 완전히 초기화하지 못하게 한다. 플레이어는 `현재 내구도`를 수리해 즉시 파괴 위험을 낮출 수 있지만, 강화 실패로 남은 `최대 내구도`의 구조적 흉터는 계속 다음 강화 판단에 영향을 줘야 한다.

## Approved architecture

```text
CURRENT_DURABILITY_PERCENT = short-term survivability
MAX_DURABILITY_PERCENT     = accumulated structural integrity

0 <= CURRENT <= MAX <= 100
```

- 일반 수리는 CURRENT만 MAX까지 회복한다.
- FAIL_DAMAGE는 CURRENT 중심 손상이다.
- FAIL_CRITICAL_DAMAGE와 명시적인 구조 손상 사건만 MAX를 감소시킨다.
- MAX 감소가 CURRENT 아래로 내려가면 CURRENT를 새 MAX로 clamp한다.
- CURRENT 또는 MAX가 0이면 물리 작품은 DESTROYED다.
- UID와 Chronicle provenance는 보존한다.

## Alternatives considered

### A. MAX → success chance only

장점: 단순.
문제: 확률 최적화 화면으로 수렴하기 쉽고 구조 손상의 감각이 약하다.

### B. MAX → existing item performance reduction

장점: 손상 체감이 강하다.
문제: 이미 아끼는 작품의 과거 보상을 소급 박탈하고 빠른 폐기를 유도한다.

### C. MAX → success penalty first, future enhancement output penalty later — selected

- 경미한 MAX 손상은 강화 성공 기대를 조금 낮춘다.
- 심각한 MAX 손상은 앞으로 새로 얻는 강화 성장량까지 감소시킨다.
- 이미 획득한 성능은 소급 삭감하지 않는다.

## Data flow

```text
Enhancement Attempt
→ outcome
→ current durability damage?
→ structural max durability damage?
→ clamp CURRENT <= MAX
→ check DESTROYED
→ calculate structural enhancement modifier
→ persist item UID state + provenance
→ show next decision
```

## UI contract

기본 강화 화면에서 반드시 보이는 정보:

- CURRENT durability
- MAX durability
- structural band
- final success expectation
- whether this attempt can damage CURRENT
- whether this attempt can damage MAX
- future enhancement output multiplier if below 100%

상세 보기에서만 성공률 계산의 내부 분해를 보여준다.

## Initial tuning bands

The exact values are baseline test inputs, not final balance.

```text
81-100 STABLE    : success 0pp,  future effect 100%
61-80  STRESSED  : success -3pp, future effect 100%
41-60  DAMAGED   : success -6pp, future effect 95%
21-40  FRACTURED : success -10pp,future effect 90%
1-20   CRITICAL  : success -15pp,future effect 80%
0      DESTROYED
```

## Failure and recovery boundaries

- Pity/recovery progress never restores MAX durability.
- Normal repair never restores MAX durability.
- No default destruction-prevention insurance in the first Vertical Slice.
- MAX restoration/rebuild is a separate future Decision; no implicit full reset.
- Do not apply success penalty + existing stat penalty + extra destroy chance all at once by default.

## Testing questions

1. Does repairing CURRENT still feel useful?
2. Does damaged MAX keep the next enhancement decision tense after repair?
3. Do players abandon a damaged favorite item too early?
4. Is the structural penalty understandable without reading detailed math?
5. Does MAX damage occur rarely enough to feel like a scar rather than a maintenance tax?
6. Does the system avoid an always-correct `repair first` or `discard item` strategy?

## Non-goals

- No product implementation in this planning batch.
- No final probability or durability-loss values.
- No MAX-restoration economy yet.
- No retroactive conversion of historical integer DURABILITY values.
