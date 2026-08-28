# BS-ENHANCE-20260828-34 · +10 무기 키워드 귀속

```text
STATUS = USER_APPROVED_CURRENT
DECISION_DATE = 2026-08-28
DECISION_SOURCE = USER_CLARIFICATION_IN_IMPLEMENTATION_CONTRACT_REVIEW
BENCHMARK = NOT_APPLICABLE / DIRECT_USER_CORRECTION_OF_EXISTING_OWNERSHIP_SEMANTICS
FIELD_OWNER = WEAPON_KEYWORD_OWNERSHIP
FIELD_PRECEDENCE = OVERRIDES_INTEGRATED_CORE_CANON_WHEN_KEYWORD_OWNERSHIP_FIELDS_CONFLICT
ITEM_KEYWORD_RECIPIENT = WEAPON_ITEM_ONLY
ITEM_KEYWORD_MACHINE_OWNER = CATALYST_AFFIX
PLAYER_TITLE_REWARD = FUTURE_CONTENT_NOT_GRANTED_BY_+10
WEAPON_KEYWORD_CONTENT_ID = UNDECIDED / USER_CONTENT_DECISION_REQUIRED
HISTORICAL_FIXTURE_OR_CUSTOMER_EPITHET_REUSE = FORBIDDEN
```

## 결정

성공한 `+9 -> +10` 정밀강화는 작품의 `CATALYST_AFFIX`에 정확히 하나의
무기 키워드를 기록한다. 이 키워드는 플레이어 자신에게 귀속되는 칭호나
능력치가 아니며, 무기의 정체성과 이후 같은 UID 생애 기록을 위한 정보다.

플레이어 칭호 콘텐츠는 이후 별도 콘텐츠로 존재할 수 있으나, 이 Slice의
`+10` 성공으로 생성·지급·표시하지 않는다.

## 범위와 금지

- 키워드는 정확히 하나이며 네 번째 affix 슬롯을 만들지 않는다.
- 키워드의 실제 content ID와 표시 문구는 아직 미결정이다. 역사 fixture나
  예전 고객 이명을 자동 재사용하지 않는다.
- 일반 강화, `+20` 이후 milestone, 확률, 비용, 수리, 고객 피해 profile에
  새 효과를 추가하지 않는다.
- generic keyword가 고객 실제사용 피해를 보편적으로 경감하지 않는다.

## 정본 영향

- `docs/planning/BLACKSMITH_CORE_SIMPLIFICATION_CANON_20260825.md`
- `docs/planning/BLACKSMITH_PHASE1_UNIFIED_IMPLEMENTATION_CONTRACT_20260828.md`
- `docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md`

## 검증 계약

- `+10` 성공은 item-owned `CATALYST_AFFIX` 하나만 쓴다.
- 플레이어 title/칭호 필드, 보상, UI를 생성하지 않는다.
- 실제 키워드 content row가 승인되기 전 `PRECISION_KEYWORD_PENDING_CONTENT`를
  플레이어에게 노출하지 않는다.
