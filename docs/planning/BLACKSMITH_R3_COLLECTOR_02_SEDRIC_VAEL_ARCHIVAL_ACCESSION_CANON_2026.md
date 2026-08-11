# Blacksmith R3 Collector 02 — Sedric Vael Archival Accession Canon 2026

Decision: `BS-CONTENT-20260811-08`.

```text
COLLECTOR_02 / SEDRIC_VAEL
ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
ARCHIVAL_STEWARDSHIP_THROUGH_EXPLAINABLE_PROVENANCE_AND_CUSTODY
```

상태: `USER_APPROVED / R3_R7_8_OF_10 / PLANNING_ONLY`.

제품 구현: `BLOCKED`.
Task3 구현: `NOT_APPROVED`.
사람 플레이테스트: `NOT_RUN`.
Android 실기기: `NOT_RUN`.
접근성: `NOT_RUN`.

## 1. 목적

기존 `SEDRIC_VAEL`을 두 번째 Collector-family 상세 고객으로 재사용한다. 플레이어는 가장 강하거나 가장 오래된 작품을 자동 선택하는 대신, 공개된 장기 보관 목적에 맞춰 **실제 작품 UID 한 점이 자기 역사와 custody를 충분히 설명할 수 있는지** 판단한다.

플레이어 역할은 `BLACKSMITH_ITEM_AND_HISTORY_DECISION_MAKER_NOT_ARCHIVE_MANAGER`다. 기록 보관소·박물관 운영자가 아니다.

## 2. 기존 책임과 분리

```text
ERSA_ROEN / COLLECTOR_01 / EXHIBITION_EVIDENCE_AND_PROVENANCE
= 공개 전시 의도에 어떤 실제 제작·생애 증거를 강조할지 판단

SEDRIC_VAEL / COLLECTOR_02 / ARCHIVAL_ACCESSION_PROVENANCE_AND_CUSTODY
= 같은 UID의 실제 출처·custody 근거가 장기 보관 인계를 설명할 수 있는지 판단

CEREMONIAL_NOBLE / NOBLE_01 / HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
= 같은 가보 UID에 물리적으로 어디까지 수리·복원·재작업할지 판단
```

보호 토큰:

- `ERSA_EXHIBITION_RESPONSIBILITY_PRESERVED`
- `NOBLE01_TREATMENT_DEPTH_RESPONSIBILITY_PRESERVED`
- `EXISTING_SEDRIC_VAEL_CUSTOMER_REUSED`

Sedric은 전시 reception/thesis, 복원 개입 깊이, storage/visitor/staff/loan logistics를 소유하지 않는다.

## 3. 플레이 흐름

```text
SEDRIC_VAEL 방문
→ archival category / keeping purpose 공개
→ 실제 작품 UID 후보 확인
→ 각 후보에 실제로 기록된 provenance·custody·생애 근거 확인
→ 작품 UID 한 점 선택
→ SAME_ITEM_UID_PRESERVED 상태로 인계
→ archival accession은 비직접 고객/세계 사건으로 해결
→ ARCHIVE_ACCESSION_STATE
 + PROVENANCE_DOCUMENTATION_STATE
 + ITEM_UID_CUSTODY_LEGACY_STATE
→ 실제 원인 2~4개 + 주 후속 행동 1개
```

플레이어는 문서를 타이핑하거나 출처를 창작하지 않고, 선반·수장고·방문객·직원·보존환경·대여 물류를 직접 운영하지 않는다.

## 4. 사용할 수 있는 근거

현재 작품/프로젝트에 이미 존재하고 이번 보관 목적과 실제 관련된 근거만 소비한다.

- item UID와 작품 범주
- 목적에 관련될 때만 재료 정체성
- 실제 제작 provenance
- 기록된 소유·custody 전환
- 해당 UID에 실제 연결된 손상·수리·복원·회수·전시·임무·여정·투기장·계승 등 승인 생애 이력
- 기존 Chronicle/provenance 기록
- 공개 목적상 관련될 때만 제작 등급/Artistry 등 실제 제작 근거
- 기존 eligibility/fit gate

기록되지 않은 소유·출처는 사실로 추론하지 않는다. 누락은 누락으로 보여주고 유리한 점수로 메우지 않는다.

## 5. 선택 구조

inventory가 허용하면 서로 다른 강점을 가진 둘 이상의 방어 가능한 선택을 만든다.

예:

- 비교적 새 작품이지만 provenance/custody가 매우 연속적인 경우
- 오래 사용됐고 중요한 생애가 있지만 소유 기록 일부가 비어 있는 경우
- Artistry는 높지 않지만 제작·회수·소유 전환이 명료한 경우
- 역사적 의미는 강하지만 unresolved custody gap이 있는 경우

다음 하나로 자동 정답을 만들지 않는다.

- 최고 Artistry
- 가장 오래된 작품
- 가장 많은 Chronicle 사건
- 최고 강화
- 단일 숨은 aggregate score

## 6. 결과 3축

### `ARCHIVE_ACCESSION_STATE`

현재 공개된 archival request가 실제 근거에 따라 accepted / conditional / deferred / declined 계열로 귀결되는 상태다. 전체 품질 총점이 아니다.

### `PROVENANCE_DOCUMENTATION_STATE`

선택한 UID의 실제 origin/custody evidence가 공개 목적을 얼마나 설명하는지 나타낸다. 누락·모순은 이유로 노출하며 하나의 총점으로 숨기지 않는다.

### `ITEM_UID_CUSTODY_LEGACY_STATE`

archival handoff 뒤 **같은 UID**의 custody/public-record 생애가 어떻게 바뀌었는지 나타낸다.

세 축은 서로 다를 수 있다. accession 성공이 완전 복원을 뜻하지 않고, documentation이 강해도 다른 작품이 특정 목적에 더 적합할 수 있다.

## 7. 후속 환류

실제 기존/후속 owner가 지원할 때만 다음 이유로 연결한다.

- 현 상태 보존
- 기존 treatment owner를 통한 수리·복원
- 승인된 새 근거가 생긴 뒤 재평가
- 후속 승인된 loan/exhibition hook
- farming이 아닌 research/appraisal hook
- 다음 archival request용 다른 작품 선택·신작

Decision08 자체가 이 미래 시스템을 제품 구현하지 않는다.

## 8. 같은 UID와 성장 경계

`SAME_ITEM_UID_PRESERVED`는 필수다.

- accession/review/custody transfer가 item clone 또는 새 replacement UID를 만들지 않는다.
- archive에 들어갔다는 이유만으로 Artistry가 증가하지 않는다.
- acceptance/storage/review/display 자체만으로 `CHRONICLE_AFFIX`를 자동 지급하지 않는다.

## 9. 명시적 금지선

- `NO_AUTHENTICITY_TOTAL_SCORE`
- `NO_PROVENANCE_COMPLETENESS_SCORE`
- `NO_ARCHIVE_PRESTIGE_SCORE`
- `NO_RARITY_SCORE_FOR_ARCHIVAL_ACCESSION`
- `NO_HIGHEST_ARTISTRY_ALWAYS_BEST`
- `NO_OLDEST_ITEM_ALWAYS_BEST`
- `NO_MOST_CHRONICLE_EVENTS_ALWAYS_BEST`
- `NO_HIGHEST_ENHANCEMENT_ALWAYS_BEST`
- `NO_DOCUMENT_FABRICATION`
- `NO_UNRECORDED_HISTORY_AUTOFILL`
- `NO_ACCESSION_COUNT_ARTISTRY_GROWTH`
- `NO_APPRAISAL_OR_REVIEW_COUNT_ARTISTRY_GROWTH`
- `NO_AUTOMATIC_CHRONICLE_AFFIX_FROM_ARCHIVING`
- `NO_ARCHIVE_STORAGE_MANAGEMENT`
- `NO_MUSEUM_MANAGEMENT_SIM`
- `NO_VISITOR_MANAGEMENT`
- `NO_STAFF_OR_SHELF_MANAGEMENT`
- `NO_PRESERVATION_ENVIRONMENT_SIMULATION`
- `NO_LOAN_LOGISTICS_MANAGEMENT`

## 10. 정확 값과 taxonomy

정확 archive-purpose 분포, acceptance threshold, 기간, 경제 보상, 관계 보상, 후속 timing, 결과 분포는 모두 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

Decision08은 Sheet의 `BS-CT-06 / 고객 4유형×이름 고객 8명` 의미를 재정의하지 않는다. Sedric이 기존 8명 중 한 명이라는 사실만 재사용하며, `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 계속 열린다.

## 11. 기대 결과

Ersa는 **“무엇을 공개적으로 보여줄 것인가”**, Sedric은 **“이 작품의 실제 역사를 장기 보관 대상으로 책임지고 받아들일 수 있는가”**를 묻는다. 작품 가치는 archive score가 아니라 같은 UID에 실제 남은 출처·소유·생애를 플레이어가 읽고 방어할 수 있기 때문에 커진다.
