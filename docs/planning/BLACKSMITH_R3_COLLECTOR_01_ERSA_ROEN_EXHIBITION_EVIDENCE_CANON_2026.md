# Blacksmith R3 Collector 01 — Ersa Roen Exhibition Evidence Canon

## Authority

- Decision: `BS-CONTENT-20260811-04`
- Content ID: `COLLECTOR_01`
- Customer: `ERSA_ROEN / 에르사 로엔`
- Activity family: `EXHIBITION_EVIDENCE_AND_PROVENANCE`
- R3–R7 approval slot: `4/10`
- Work mode: `PLANNING_ONLY`
- 제품 구현: `BLOCKED`
- Task3 구현: `NOT_APPROVED`

이 정본은 기존 작품 UID·제작·예술성·계보·연대기·소유·손상·복원 정보를 전투가 아닌 전시 맥락에서 재사용하는 첫 수집가 상세 콘텐츠다. 플레이어는 전시관 운영자가 아니라 대장장이이며, 작품 한 점과 그 작품에 이미 존재하는 증거를 선택한다.

## Core promise

```text
ERSA_ROEN 방문
→ 전시 의도 공개
→ 후보 작품의 실제 UID 증거 비교
→ 같은 작품 UID 한 점 선택
→ 제작자 설명에서 기존 증거 2~4개 강조
→ 작품 인계
→ 전시는 비직접 세계 사건으로 해결
→ EXHIBITION_RECEPTION_STATE
 + EXHIBIT_THESIS_FIT_STATE
 + ITEM_UID_PUBLIC_LEGACY_STATE
→ 같은 UID의 후속 제작·복원·판매·재전시 판단 이유
```

`maker statement`는 설명 계층이다. 플레이어가 강조한 증거를 새로 만들거나 원수치를 올리거나 결과를 보장하지 않는다.

## Exhibition intent families

첫 Collector proof는 다음 두 넓은 맥락 가족을 사용한다.

- `CRAFTSMANSHIP_EVIDENCE`: 작품이 **어떻게 만들어졌는지**를 전면에 둔다.
- `LIVED_HISTORY_EVIDENCE`: 같은 작품이 **실제로 무엇을 겪어 왔는지**를 전면에 둔다.

두 값은 새 작품 타입·등급·원수치가 아니다. 전시 요청의 맥락을 설명하는 분류이며, 미래 모든 수집가 콘텐츠의 고정 답안 목록으로 확대하지 않는다.

## Existing evidence only

### CRAFTSMANSHIP_EVIDENCE

현재 정본이 실제로 소유하는 경우에만 다음 증거를 사용할 수 있다.

- 제작 등급·`GRADE_AFFIX`
- `ARTISTRY`와 승인된 제작/후천 성장 출처
- 직접 단조 결과
- 마감·촉매·승인된 재작업 provenance
- 같은 UID에 이미 기록된 제작자·제작 과정 이력

### LIVED_HISTORY_EVIDENCE

현재 정본이 실제로 소유하는 경우에만 다음 증거를 사용할 수 있다.

- 소유·인계·대여·반환 provenance
- 고객 또는 세계 사용 사건
- 손상·분실·회수·수리·복원·계승 이력
- 기존 규칙이 실제로 부여한 `CHRONICLE_AFFIX` 또는 Chronicle 사건

새 `RARITY_SCORE`, `PRESTIGE_SCORE`, `COLLECTOR_SCORE`, `EXHIBITION_SCORE`를 만들지 않는다. 전시 가치는 기존 증거와 요청 맥락의 설명 가능한 적합으로 판단한다.

## Multiple defensible works

한 가지 수치의 최대값이 자동 정답이 되지 않는다.

- 새 작품도 강한 제작 증거가 전시 의도와 맞으면 유효한 선택이다.
- 오래 사용된 작품도 구체적 생애 증거가 의도와 맞으면 유효한 선택이다.
- 높은 강화가 전시 주제와 무관하면 약한 선택일 수 있다.
- Chronicle 항목이 많아도 관련 없는 사건이면 약한 선택일 수 있다.
- 오래된 작품이 항상 최선이 아니다.
- 예술성이 가장 높은 작품이 항상 최선이 아니다.
- 강화가 가장 높은 작품이 항상 최선이 아니다.

`NO_CHRONICLE_COUNT_OPTIMIZATION`을 보호 경계로 둔다. 사건의 **개수**가 아니라 요청과의 **관련성**을 사용한다.

## Result contract

전시 결과는 하나의 `%`, 별점, 위신 점수로 합치지 않는다.

```text
EXHIBITION_RECEPTION_STATE
EXHIBIT_THESIS_FIT_STATE
ITEM_UID_PUBLIC_LEGACY_STATE
```

- `EXHIBITION_RECEPTION_STATE`: 공개 반응이 어떤 상태였는지.
- `EXHIBIT_THESIS_FIT_STATE`: 선택한 작품과 강조 증거가 발표된 전시 의도에 얼마나 설득력 있게 맞았는지.
- `ITEM_UID_PUBLIC_LEGACY_STATE`: 같은 UID의 공개 생애에 어떤 사건·맥락이 남았는지.

강한 공개 반응과 약한 thesis fit이 동시에 존재할 수 있고, 반대로 소박한 반응 속에서도 작품의 공개 생애에 의미 있는 사건이 남을 수 있다. 결과 화면은 2~4개의 구체적 원인을 기존 작품 증거와 전시 의도에서 가져와 설명한다.

## Same-UID lifecycle

`SAME_ITEM_UID_PRESERVED`.

전시 전·전시 중·전시 후의 작품은 같은 작품 UID다. 전시는 작품을 복제하거나 대체하지 않는다. 대여·소유권·반환 상태는 기존 작품 생애 권위를 따른다. 공개 인지도는 숨은 새 원수치가 아니라 특정 사건과 provenance 결과로 남아야 한다.

후속 수리·복원·재판매·반환·계승·재전시는 같은 UID의 과거 증거를 다시 읽을 수 있어야 한다.

## Artistry and Chronicle boundaries

전시는 무료 성장 행동이 아니다.

- 전시 횟수만으로 `ARTISTRY`가 증가하지 않는다.
- 공개 반응만으로 `ARTISTRY`가 증가하지 않는다.
- Chronicle 사건이라는 이유만으로 `ARTISTRY`가 증가하지 않는다.
- 전시했다는 사실만으로 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- 기존 Chronicle 권위가 충분히 의미 있는 특정 전시 사건을 Chronicle 결과로 판정하는 경우에만, 그 구체적 사건과 같은 작품 UID에 연결한다.

```text
NO_EXHIBITION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_DISPLAY
```

## Information contract

Ersa의 기본 카드에는 전시 의도와 관련 증거 차원을 보여주되 `BEST` 자동 추천을 제공하지 않는다.

작품 선택 뒤 판단 계층은 다음을 보여준다.

- 선택된 작품 UID
- 관련 있는 지지 또는 충돌 증거 2~4개
- 제작자 설명에서 강조할 기존 증거
- hard eligibility와 contextual fit의 분리

전시 결과는 세 결과 축과 구체적 원인 2~4개를 보여준다. 색상만으로 핵심 상태를 전달하지 않는다.

정확한 문구·임계값·경제값·결과 분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## Player authority boundary

플레이어는 `BLACKSMITH_ITEM_AND_EVIDENCE_DECISION_MAKER_NOT_CURATOR_CONTROLLER`다.

다음은 이 Decision의 코어가 아니다.

- 직접 전시 배치 미니게임
- 전시관 장식 경영
- 관람객 동선·방문자 관리
- 경매 운영
- 실시간 큐레이터 조작

전시는 작품을 세계에 보내 결과를 돌려받는 기존 Blacksmith 세계 환류 구조 안에서 해결한다.

## Protected boundaries

```text
NO_RARITY_SCORE
NO_PRESTIGE_SCORE
NO_COLLECTOR_SCORE
NO_EXHIBITION_SCORE
NO_CHRONICLE_COUNT_OPTIMIZATION
NO_OLDEST_ITEM_ALWAYS_BEST
NO_HIGHEST_ARTISTRY_ALWAYS_BEST
NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST
NO_EXHIBITION_COUNT_ARTISTRY_GROWTH
NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_DISPLAY
SAME_ITEM_UID_PRESERVED
BLACKSMITH_ITEM_DECISION_MAKER_NOT_CURATOR_CONTROLLER
NO_DIRECT_EXHIBITION_MINIGAME
NO_GALLERY_DECORATION_OR_VISITOR_MANAGEMENT_CORE
PRODUCT_IMPLEMENTATION_BLOCKED
TASK3_IMPLEMENTATION_NOT_APPROVED
```

## Adversarial decision report

검증된 실패 가정과 대응은 다음과 같다.

1. **Lore quiz drift** — 숨은 세계관 지식이 아니라 작품 UID에 실제 존재하는 증거만 판정에 사용한다. `MUST_FIX`.
2. **Prestige score drift** — 희귀도·위신·수집가·전시 총점을 새 원수치로 만들지 않는다. `MUST_FIX`.
3. **Chronicle count optimization** — 사건 개수가 아니라 전시 의도와 사건의 관련성을 본다. `MUST_FIX`.
4. **Old-item dominance** — 새 작품의 강한 제작 증거와 오래된 작품의 강한 생애 증거가 각각 맥락에 따라 방어 가능한 선택이 되게 한다. `MUST_FIX`.
5. **Curator-game drift** — 플레이어 권위를 작품·증거 선택에 두고 전시 실행은 비직접 세계 사건으로 유지한다. `MUST_FIX`.
6. **Free progression farming** — 전시 횟수/전시 자체로 Artistry나 Chronicle Affix를 자동 성장시키지 않는다. `MUST_FIX`.
7. **Universal deterministic best** 요구는 Blacksmith의 설명 가능한 선택과 no-auto-BEST 보호 강점을 약화하므로 `REJECTED_CRITIQUE`.

## Acceptance

- `BS-CONTENT-20260811-04 / COLLECTOR_01 / ERSA_ROEN / EXHIBITION_EVIDENCE_AND_PROVENANCE`가 R3–R7 `4/10` 현재 기획 Decision이 된다.
- Nadia 1/10, Toren 2/10, Marek 3/10은 승인 이력으로 보존한다.
- 두 exhibition intent family는 맥락 분류이며 새 원수치/작품 타입이 아니다.
- 결과는 세 축으로 분리된다.
- 같은 UID와 기존 증거가 권위다.
- 전시 총점·희귀도/위신 총점·Chronicle 개수 최적화를 만들지 않는다.
- 전시 횟수/표시 자체로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.
- 제품 구현과 Task3 구현 Gate는 열리지 않는다.
