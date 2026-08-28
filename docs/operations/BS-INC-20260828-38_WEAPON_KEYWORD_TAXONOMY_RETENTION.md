# BS-INC-20260828-38 · 무기 키워드 분류 보존

```text
STATUS = RESOLVED_CURRENT_CANON
CLASS = CANONICAL_TERMINOLOGY_DRIFT
DISCOVERED_AT = 2026-08-28
SOURCE = USER_CORRECTION + ORIGIN_MAIN_FRESH_READ
NO_BASE_PROMOTION = PROJECT_SPECIFIC_ITEM_SCHEMA_AND_PLAYER_LANGUAGE
```

## Incident

현재 main의 저장 구조는 `grade_affix`, `catalyst_affix`,
`chronicle_affix` 세 field를 유지했지만, 상위 current-canon 문서가 이를
플레이어에게 보이는 **등급 키워드 / 태그 키워드 / 사건 키워드**로 일관되게
명시하지 않았다. 이 누락은 `+10`의 weapon-owned 결과를 generic keyword로
오독하거나 사건 키워드·플레이어 칭호와 혼동하게 만들 위험이 있었다.

## Evidence

- `data/vertical_slice/vertical_slice_schema.json`: 세 field를 직렬화 schema의
  `affix_fields`로 요구한다.
- `scripts/vertical_slice/domain/vs_item.gd`: 같은 세 field를 item UID에
  저장·복원한다.
- `scripts/vertical_slice/resolvers/vs_enhancement_resolver.gd`: 현 historical
  runtime evidence에서 `+10` 결과를 `catalyst_affix`에 기록한다. 현재
  placeholder `PRECISION_KEYWORD_PENDING_CONTENT`는 player-facing content가 아니며
  새 구현 계약에서 노출 금지다.
- `BS-ENHANCE-20260828-34`: `+10` 결과는 무기 귀속이며 player title이 아님을
  소유한다.

## Solution

`BS-ENHANCE-20260828-34`에 다음 mapping을 current field owner로 기록했다.

```text
GRADE_KEYWORD -> GRADE_AFFIX
TAG_KEYWORD -> CATALYST_AFFIX
EVENT_KEYWORD -> CHRONICLE_AFFIX
+10_PRECISION_OUTPUT_KEYWORD = TAG_KEYWORD
```

새 field, 네 번째 affix 슬롯, `+10` player title, 모든 사건의 자동 사건
키워드 부여는 생성하지 않았다.

## Lesson

기술 owner 이름(`*_AFFIX`)과 플레이어 언어(키워드 분류)는 함께 기록한다.
후속 content row·UI는 이 mapping을 사용하며, 생성 원인과 표시 문구를
분리한다.

## Validation

`python tests/check_phase1_unified_implementation_contract.py`가 Decision34,
Core Canon, Phase-1 contract, handoff의 taxonomy tokens를 동시에 검사한다.
