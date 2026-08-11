# Blacksmith R3 Gladiator 01 — Cassia Bellan Arena Signature Weapon Canon

## Authority

- Decision: `BS-CONTENT-20260811-05`
- Content ID: `GLADIATOR_01`
- Customer: `CASSIA_BELLAN / 카시아 벨란`
- Activity family: `ARENA_SIGNATURE_WEAPON_AND_LEGACY`
- R3–R7 approval slot: `5/10`
- Work mode: `PLANNING_ONLY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

이 정본은 검투사 경기를 직접 플레이하는 콘텐츠가 아니다. 카시아가 공개한 무기 범주와 경기 맥락을 읽고 대장장이가 작품 한 점을 선택·인계한 뒤, 경기 결과와 그 작품의 실제 기여와 같은 UID의 공개 생애를 분리해서 돌려받는 첫 검투사 대표 상세 콘텐츠다.

## Core promise

```text
CASSIA_BELLAN 방문
→ 요청 무기 범주 + 경기 맥락 공개
→ 후보 작품의 hard eligibility와 contextual fit 비교
→ 같은 작품 UID 한 점 선택·인계
→ 경기는 비직접 세계 사건으로 해결
→ ARENA_MATCH_STATE
 + EQUIPMENT_CONTRIBUTION_STATE
 + ITEM_UID_ARENA_LEGACY_STATE
→ 실제 원인 2~4개 + 주 후속 행동 1개
→ 같은 UID의 수리·복원·후속 강화·재대결 신작·보존·전시 판단
```

플레이어 권위는 `BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER`다.

## Request and fit contract

카시아는 최소한 요청 무기 **범주**와 이번 경기에서 중요한 맥락을 인계 전에 공개한다. 판정은 현재 Blacksmith가 실제로 소유하는 정보만 소비한다.

허용되는 예시는 다음과 같다.

- 무기 범주와 hard eligibility
- 일반 강화 단계와 승인된 역할 원수치
- 실제 관련성이 있을 때의 중량·취급 관련 기존 속성
- 맥락이 요구할 때의 승인된 수식어·기능 적합
- 카시아가 공개적으로 이름·상징·계보를 중시하는 요청일 때만 `ARTISTRY`, provenance, 기존 Chronicle 증거

새 `ARENA_SCORE`, `FAME_SCORE`, `GLADIATOR_SCORE`, `SIGNATURE_SCORE` 또는 숨은 범용 전투력 총점을 만들지 않는다.

`NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`. 최고 강화 작품이 항상 최선이 아니다. 공개된 경기 맥락과 작품의 실제 적합이 다르면 더 낮은 강화 작품도 방어 가능한 선택이어야 한다. 가장 유명하거나 가장 오래된 작품도 자동 정답이 아니다.

## Result contract

경기 결과와 장비 기여는 같은 값이 아니다.

```text
ARENA_MATCH_STATE
EQUIPMENT_CONTRIBUTION_STATE
ITEM_UID_ARENA_LEGACY_STATE
```

- `ARENA_MATCH_STATE`: 경기 자체가 어떤 결과로 끝났는지.
- `EQUIPMENT_CONTRIBUTION_STATE`: 공개된 경기 맥락과 실제 작품 속성에 근거해 작품이 무엇을 도왔거나 방해했는지.
- `ITEM_UID_ARENA_LEGACY_STATE`: 결정적 장면, 경기 손상, 라이벌 흔적, 공개적으로 기억될 사건 또는 의미 있는 공개 생애 없음 등 같은 UID에 남는 결과.

`NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE`.

- 승리했다고 작품이 최적이었다고 단정하지 않는다.
- 패배했다고 작품이 나빴다고 단정하지 않는다.
- 강한 장비 기여와 경기 패배가 함께 존재할 수 있다.
- 약한 장비 기여와 경기 승리가 함께 존재할 수 있다.

결과 화면은 세 축을 하나의 `%`, 별점, 위신 총점으로 합치지 않는다. 실제 원인 2~4개와 다음 제작 판단에 가장 직접적인 주 행동 이유 1개를 보여준다.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

인계 전·경기 중·귀환 뒤 작품은 같은 UID다. 경기 사용은 기존 작품 생애 권위가 허용하는 범위에서 손상·수리 필요·소유/인계 provenance·라이벌 흔적·Chronicle 후보 사건을 만들 수 있지만 작품을 복제·대체·재추첨하지 않는다.

후속 수리·복원·후속 강화·재판매·보존·재대결 의뢰·전시는 같은 UID의 과거 경기 증거를 다시 읽을 수 있어야 한다.

## Progression boundaries

경기는 무료 성장 파밍이 아니다.

- 경기 횟수만으로 `ARTISTRY`가 증가하지 않는다.
- 승리 횟수나 명성만으로 `ARTISTRY`가 증가하지 않는다.
- 경기 출전 또는 승리 사실만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 기존 Chronicle 권위가 충분히 의미 있는 특정 경기 사건을 Chronicle 결과로 판정할 때만 그 사건과 같은 UID에 연결한다.
- 반복 경기는 자동 누적 보너스나 farming multiplier를 만들지 않는다.

```text
NO_MATCH_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE
NO_MATCH_FARMING_MULTIPLIER
```

## Player authority boundary

다음은 이 Decision의 코어가 아니다.

- 직접 검투사 전투 조작
- 전투 중 위치 지정·행동 명령
- 검투사 팀·길드·로스터 경영
- 배팅 시스템
- 실시간 투기장 운영

```text
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT
NO_BETTING_SYSTEM
NO_OPAQUE_ARENA_SCORE
```

경기 실행은 Blacksmith 밖의 비직접 세계 사건이며 플레이어는 대장장이로 남는다.

## Legacy gladiator PoC boundary

현재 저장소의 `data/customers/gladiator_poc.json`과 `data/world/gladiator_match_poc.json`은 역사 POC fixture다. 이 Decision은 그 파일을 수정하거나 현재 설계 권위로 승격하지 않는다.

```text
LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05
NO_FIXED_IRON_SWORD_CANON
NO_LEGACY_ARENA_SCORE_FORMULA_CANON
NO_UNIVERSAL_FIXED_DAY_COUNT
```

따라서 과거의 `iron_sword`, +5/+10, preferred-affix 목록, 고정 3일, grade score, score weight, result band 수치는 Decision05의 정본 수치가 아니다.

## Information contract

카시아 기본 카드와 인계 전 판단층은 다음을 분리해 보여준다.

- 요청 무기 범주와 hard eligibility
- 이번 경기 맥락에서 실제 관련 있는 판단 차원
- 선택된 작품 UID
- 지지 또는 충돌 원인 2~4개

자동 `BEST` 추천은 제공하지 않는다.

결과는 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`, 실제 원인 2~4개, 주 후속 행동 1개를 보여준다. 색상만으로 핵심 상태를 전달하지 않는다.

정확한 문구·임계값·기간·경제값·보상·결과 분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## Protected boundaries

```text
NO_DIRECT_ARENA_COMBAT
NO_GLADIATOR_TEAM_OR_GUILD_MANAGEMENT
NO_BETTING_SYSTEM
NO_OPAQUE_ARENA_SCORE
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_WIN_EQUALS_GOOD_ITEM_COLLAPSE
NO_MATCH_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_WIN_OR_APPEARANCE
NO_MATCH_FARMING_MULTIPLIER
SAME_ITEM_UID_PRESERVED
LEGACY_GLADIATOR_POC_NON_AUTHORITATIVE_FOR_DECISION05
BLACKSMITH_EQUIPMENT_DECISION_MAKER_NOT_ARENA_CONTROLLER
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

## Adversarial decision report

1. **Combat-RPG drift** — 경기 실행은 비직접 세계 사건으로 유지하고 플레이어 권위를 작품 판단에 둔다. `MUST_FIX`.
2. **Opaque score drift** — 새 투기장/명성/검투사 총점을 만들지 않는다. `MUST_FIX`.
3. **Win=item quality collapse** — 경기 결과와 작품 기여를 별도 축으로 유지한다. `MUST_FIX`.
4. **Highest-enhancement dominance** — 공개 맥락과 기존 작품 속성의 설명 가능한 적합을 사용한다. `MUST_FIX`.
5. **Progression farming** — 경기/승리 횟수로 Artistry 또는 Chronicle을 자동 성장시키지 않는다. `MUST_FIX`.
6. **UID loss** — 경기 전·중·후 같은 작품 UID를 보존한다. `MUST_FIX`.
7. **Legacy fixture resurrection** — Kyle/iron_sword POC 수치와 점수식은 역사 fixture로만 남긴다. `MUST_FIX`.
8. 전투를 직접 조작해야 더 극적이라는 비판은 Blacksmith의 대장장이 역할을 무너뜨리는 범위 확대이므로 `REJECTED_CRITIQUE`.

## Acceptance

- `BS-CONTENT-20260811-05 / GLADIATOR_01 / CASSIA_BELLAN / ARENA_SIGNATURE_WEAPON_AND_LEGACY`가 R3–R7 `5/10` 현재 기획 Decision이 된다.
- Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10은 승인 이력으로 보존한다.
- 경기 결과와 작품 기여와 같은 UID 공개 생애를 세 축으로 분리한다.
- 직접 전투·팀/길드 경영·배팅·불투명 투기장 총점을 추가하지 않는다.
- 최고 강화와 경기 승리를 작품 품질의 자동 정답으로 만들지 않는다.
- 경기 횟수/승리만으로 Artistry 또는 Chronicle을 자동 성장시키지 않는다.
- legacy gladiator POC 고정 수치와 점수식을 현재 권위로 승격하지 않는다.
- 제품 구현과 Task3 구현 Gate는 열리지 않는다.
