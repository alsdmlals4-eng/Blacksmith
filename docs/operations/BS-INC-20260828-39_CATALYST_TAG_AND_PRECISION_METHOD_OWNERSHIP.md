# BS-INC-20260828-39 · 촉매 태그와 정밀강화 방식 소유권 교정

```text
STATUS = SUPERSEDED_BY_LATER_USER_DECISION / HISTORICAL_REPAIR_RECORD
SUPERSEDED_BY_BS-INC-20260828-40 = TRUE
CLASS = OWNERSHIP_SCOPE_DRIFT
DISCOVERED = 2026-08-28
SOURCE = USER_DIRECT_CLARIFICATION + FRESH_MAIN_CANON_AND_RUNTIME_READBACK
FIELD_OWNER = BS-ENHANCE-20260828-34
NO_BASE_PROMOTION = PROJECT_SPECIFIC_WEAPON_KEYWORD_OWNERSHIP
```

> **[대체됨]** 이 기록은 촉매 계보만으로 태그를 결정하고 정밀강화 방식을
> 능력치·내구도 전용으로 제한했던 2026-08-28의 중간 교정 증거다. 사용자가
> 같은 날 태그 정체성을 `촉매 계보 + 강화 방식`의 조합으로 직접 수정했으므로,
> current owner는 `BS-INC-20260828-40`과 갱신된 Decision34다.

## 문제

기존 current Decision34는 태그 키워드의 저장 owner가 `CATALYST_AFFIX`임을
확정했지만, 태그 정체성을 촉매 **계보**가 결정한다는 점과 정밀강화 방식의
효과 한계를 분리해 명시하지 않았다. 역사 R2 문서는 방식의 `FUNCTION_REWORK`,
예술성, 환경 처리 출력을 계속 적고 있으며, 현재 vertical-slice resolver에는
계보를 해석하지 않는 `PRECISION_KEYWORD_PENDING_CONTENT` 임시 문자열이 남아
있다.

## 근거와 판정

| 항목 | 판정 | 근거 |
| --- | --- | --- |
| 세 개의 무기 키워드와 machine owner | CURRENT | Decision34, current item schema의 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` |
| `+9 -> +10`의 단 하나 태그 키워드 | CURRENT | Decision25/34 및 Phase-1 contract |
| 태그 정체성의 source | CURRENT | 사용자 직접 결정: `C 태그는 촉매 계보 안에서 결정` |
| 정밀강화 방식의 영향 범위 | CURRENT | 사용자 직접 결정: `무기 능력치, 내구도만 영향` |
| `FUNCTION_REWORK`·예술성·환경 처리 방식 output | SUPERSEDED | R2 historical precision document versus 최신 사용자 결정 |
| `PRECISION_KEYWORD_PENDING_CONTENT`를 +10에 쓰는 runtime 흔적 | HISTORICAL_RUNTIME_DRIFT | `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd` |
| 빈 촉매 계보의 +10 처리 | UNKNOWN_UNVERIFIED | current owner에 선택/기본값/차단 규칙 없음 |

## 교정

```text
TAG_KEYWORD_SOURCE = CATALYST_LINEAGE
TAG_KEYWORD_RESOLUTION = CATALYST_LINEAGE_GOVERNS_TAG_IDENTITY
PRECISION_METHOD_EFFECT_SCOPE = WEAPON_STATS_AND_DURABILITY_ONLY
PRECISION_METHOD_CANNOT_DETERMINE_OR_MUTATE_TAG_KEYWORD = TRUE
PRECISION_METHOD_CANNOT_AFFECT_GRADE_OR_EVENT_KEYWORD = TRUE
EMPTY_CATALYST_LINEAGE_BEHAVIOR = UNDECIDED / BLOCKS_TAG_WRITE_IMPLEMENTATION
```

이 교정은 새 slot, 촉매 catalogue, 확률, resource cost, `+20` Precision,
player title, function-rework, 또는 production asset을 추가하지 않는다. 태그의
실제 content row·표시 문구·catalyst selection flow는 별도 승인 대상이다.

## 벤치마크 결정

| 구분 | 판단 |
| --- | --- |
| ADOPT | item 결과의 source/effect layer를 하나의 owner로 분리해 플레이어가 원인을 읽을 수 있게 한다. |
| ADAPT | Blacksmith의 태그 정체성은 촉매 계보가, 수치·내구 변화는 정밀강화 방식이 각각 소유한다. |
| REJECT | 다른 게임의 다중 재련, 충전, 재굴림, 추가 슬롯, catalogue 구조를 가져오지 않는다. |
| DIFFERENTIATION | 같은 UID의 고객·사건 생애를 보존하면서 강화가 여전히 주 콘텐츠인 구조를 유지한다. |
| REMAINING_UNCERTAINTY | 빈 촉매 계보에서 +10의 선택/기본값/차단 흐름과 첫 태그 content row의 player comprehension은 Human validation이 필요하다. |

참조: [Diablo IV Itemization Update](https://news.blizzard.com/en-us/article/24243142/sanctuary-ignites-with-itemization-systems-changes), [Last Epoch Forging Potential](https://support.lastepoch.com/hc/en-us/articles/46361900702363-What-is-Forging-Potential). 비교는 layer separation 원칙만 참고했으며 수치·표현·콘텐츠를 이식하지 않는다.

## 후속 검증

1. 구조화 문서 계약 테스트가 Decision34, Core Canon, Handoff, Phase-1 contract의
   같은 소유권 경계를 확인한다.
2. 실제 태그 write/presentation 구현 전에는 catalyst-lineage content row와 빈
   계보 흐름을 사용자 승인으로 잠근다.
3. 그 구현 후 Human test에서 플레이어가 “촉매가 태그를, 방식이 성능·내구를
   바꾼다”고 구분하는지 확인한다.
