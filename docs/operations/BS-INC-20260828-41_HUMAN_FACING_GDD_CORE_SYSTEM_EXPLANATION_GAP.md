# BS-INC-20260828-41 · 사람용 GDD 핵심 시스템 설명 결손

```text
STATUS = CLOSED_CANONICAL_DOCUMENTATION_REPAIR
CLASS = HUMAN_FACING_CANON_CLARITY_GAP
DISCOVERED = 2026-08-28
SOURCE = USER_REVIEW
SCOPE = DOCUMENTATION_AND_PDF_ONLY
NO_BASE_PROMOTION = BLACKSMITH_SPECIFIC_SYSTEM_RELATIONSHIP
```

## 발견

사람용 GDD가 강화 우선, `+10` 무기 태그, 고객 실제 사용을 각각 언급했지만,
다음 연결을 독자가 한 번에 이해할 만큼 설명하지 못했다.

```text
강화 판단 → 촉매 계보·정밀강화 방식 → 무기 태그 → 고객 실제 사용 사건 → 다음 판단
```

그 결과 태그가 단순 보상처럼, 고객 이벤트가 임의의 귀환 알림처럼 읽힐 위험이
있었다. 이는 승인된 제품 규칙의 부재가 아니라 사람용 정본의 설명 결손이다.

## 교정

`docs/design/BLACKSMITH_HUMAN_FACING_GDD_20260828.md`와 사람용 PDF에 다음을
독립 섹션으로 추가했다.

- 강화 → 태그 → 생애의 플레이 경험 연결;
- 세 키워드의 출처·의미·보호 경계;
- `촉매 계보 → 정밀강화 방식 → 태그 키워드` 해석 순서;
- 같은 UID의 인계 → 실제 사용 → 사건 결과 → 다음 판단 생애 주기;
- 고객 이벤트의 실제 사용·원인·한 사건 한 UID 한 번의 손상 판정·결과 공개 규칙;
- 태그 콘텐츠와 빈 촉매 계보 동작의 `UNDECIDED` 경계.

독립 적대 검토 뒤, 촉매 계보·방식의 **플레이어 선택 UX**는 아직 미확정임을
명시하고, 실제 원인과 내구도 전후 공개 의무는 **손상이 발생했을 때**로 한정했다.
`PRECISION_KEYWORD_PENDING_CONTENT`도 플레이어 표기가 아닌 내부 임시 값/구현
흔적으로 바로잡았다. 태그 기록은 **유효하게 승인된 촉매 계보·방식 조합이 있는
성공**에만 가능하고 빈 촉매 계보는 현재 기록을 막는다는 조건도 추가했다.

정밀강화 방식의 정확한 수치, 실제 태그 명칭, 빈 촉매 계보 흐름, 새 고객 관리
콘텐츠는 추가하거나 확정하지 않았다.

## 검증과 교훈

```text
MECHANICAL_CANON = UNCHANGED
PRODUCT_SCOPE = UNCHANGED
HUMAN_GDD_CONTRACT_TEST = REQUIRED
PDF_RENDER_AND_RECEIPT = REQUIRED
HUMAN_PLAYTEST = NOT_RUN
```

**교훈:** 시스템을 사람용으로 설명할 때는 기능 이름을 나열하지 말고,
플레이어의 선택이 어떤 영속 결과를 만들고 그 결과가 다음 행동을 어떻게 바꾸는지
한 개의 인과 흐름으로 보여야 한다. 이 사건의 촉매·태그·고객 생애 값은 Blacksmith
고유 기획이므로 Base 공용 규칙으로 승격하지 않는다.
