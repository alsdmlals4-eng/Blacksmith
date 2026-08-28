# BS-INC-20260829-42 · 정밀 태그 임시값·선택 범위 드리프트

```text
STATUS = CLOSED_CANONICAL_REPAIR / IMPLEMENTATION_FOLLOWUP_OPEN
CLASS = IMPLEMENTATION_DRIFT_AND_MISSING_PRODUCT_CONTENT
DISCOVERED = 2026-08-29
EVIDENCE = CURRENT_MAIN_VS_ENHANCEMENT_RESOLVER + VS_PRECISION_RESOLVER + V3_ITEM_SCHEMA
CURRENT_OWNER = BS-ENHANCE-20260829-37
NO_BASE_PROMOTION = PROJECT_SPECIFIC_TAG_AND_UID_SEMANTICS
```

## 발견

- 현재 `VSEnhancementResolver`는 `+10` 성공 시
  `PRECISION_KEYWORD_PENDING_CONTENT`를 `CATALYST_AFFIX`에 기록한다.
- 현재 `VSPrecisionResolver`는 이미 `+10`에 도달한 뒤 별도 milestone을 쓰고,
  예술성·환경 기능 재작업·구형 방식 목록을 포함한다.
- `VSItem` V3에는 계보·방식·보류 상태를 저장할 추가 field가 없다. Decision34는
  새 stored field와 네 번째 affix slot을 금지한다.

## 교정

`BS-ENHANCE-20260829-37`은 선택을 `+9 → +10` 시도 전의 attempt-local 입력으로
정하고, 성공 시에만 2×2 표의 composite Tag 하나와 방식 효과 하나를 기존
`CATALYST_AFFIX`/무기 수치에 적용한다. 실패는 선택·태그·수치 효과를 저장하지
않는다. historical placeholder가 남은 pre-release V3 item에는 비용·재굴림 없는
한 번의 backfill만 허용한다.

## Lesson

제품 의미가 아직 결정되지 않은 placeholder는 save-compatible 문자열이라도
player-facing identity가 될 수 없다. 기존 field를 유지해야 할 때는 추가 상태를
만들기보다 가능한 한 입력을 attempt-local로 두고, 성공한 composite 결과만
안정적으로 저장한다. 이 사건의 구체적 태그 표·강화 level·UID 생애는
Blacksmith 고유이므로 Base 승격 대상이 아니다.
