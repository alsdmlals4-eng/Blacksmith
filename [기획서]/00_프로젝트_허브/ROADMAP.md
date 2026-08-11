# [현재 정본] Blacksmith Roadmap

<!-- R3_R7_DESIGN_RESUMED -->
> **R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-07 / SOLDIER_02_LIANA_MISSION_FIT_APPROVED / PLANNING_ONLY**
>
> R2 Batch 006과 Task2 완료 상태를 기반으로 R3–R7 콘텐츠 기획을 재개한다. 제품 구현 Gate는 계속 닫혀 있다.

```yaml
CURRENT_STAGE: R3_R7_DESIGN_ACTIVE
CURRENT_STAGE_STATUS: R3_R7_7_OF_10_USER_APPROVED_PLANNING_ONLY
R2_CHECKPOINT_005: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_005_STATE: R2_BATCH_005_CLOSED_10_OF_10
R2_BATCH_005_MERGE: MERGED_PR109_MAIN_CANON
R2_BATCH_006: APPROVED_10_OF_10
R2_BATCH_006_STATE: R2_BATCH_006_APPROVED_10_OF_10
R3_R7_APPROVAL_COUNTER: 7/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07
R3_R7_RESUME_LOCATOR: SOLDIER_02_LIANA_MISSION_FIT_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
VERTICAL_SLICE_IMPLEMENTATION: APPROVED_TASK2_COMPLETE
VERTICAL_SLICE_IMPLEMENTATION_EVIDENCE: VERTICAL_SLICE_IMPLEMENTATION_APPROVED
HUMAN_PLAYTEST: NOT_RUN
```

## R0–R2 — 완료된 기획 기반

- 프로젝트 코어와 권위 체계
- 직접 단조·제작 등급 5단계·예술성
- 등급·촉매·연대기 3수식어
- 일반 강화와 다섯 정밀강화 이정표
- 작품 역할·중량·기능 용량·재작업 레시피
- 고객 능력·장비 적합·모바일 정보 계층
- 개인 일정·세계 일정 분리와 작품 생애 환류

상태: `R2_BATCH_006_APPROVED_MAIN_CANON / R2_BATCH_006_APPROVED_10_OF_10 / TASK2_MAIN_MERGED / VERTICAL_SLICE_IMPLEMENTATION_APPROVED`.

## 불변 체크포인트 이력

- `R2_CHECKPOINT_004`: 제작 등급 5단계·예술성 원수치 정제와 후속 폐쇄를 완료했다.
- `R2_CHECKPOINT_005 / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`: `BS-CRAFT-20260805-02`를 포함한 승인 10건과 작품 역할·기능 레시피 Gate를 폐쇄했다.
- `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON`: Batch 005 승인과 main 병합을 보존하는 호환 앵커다.
- `R2_BATCH_006 / R2_BATCH_006_APPROVED_10_OF_10`: 대표 버티컬 슬라이스 계획과 승인 범위를 main canon으로 병합했다.
- 체크포인트 004 planning/closure main: `789c73f38003f40dde5e9a99cd7dcb3ca03863f7 / 7a46fa38586a42f268cd0432744203049649ddd5`
- 체크포인트 005 planning/closure main: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9 / 06f03323c1309d8da0e6f5b9f4680a20ce388126`
- Batch 006 merge main: `a8a94343c78a68bf7bb14b411e7741f43b257138`

이 항목은 현재 활성 카운터가 아니라 재현 가능한 병합 증거다. R3–R7 설계 활성화는 이 역사/호환 토큰을 폐기하지 않는다.

## R3–R7 현재 설계 배치

현재 승인 카운터: `7/10`.

### 1/10 — `BS-CONTENT-20260811-01`

```text
ADVENTURER_01 / NADIA_VENN
나디아 벤 유적 탐사 개인 일정
생환 + 회수
```

목표:

- 대장장이가 고객의 목적·위험을 읽고 작품 한 점을 선택한다.
- 강화 단계가 주효과이되 중량 배정 가능 여부와 실제 관련 환경·유틸리티 기능이 설명 가능한 trade-off를 만든다.
- 직접 전투·탐험 미니게임 없이 하루 종료당 최대 한 번 개인 일정이 진행된다.
- 귀환·회수·작품 UID 상태를 분리하고 같은 UID의 복원·후속 강화·새 제작 이유로 환류한다.
- 구조 상태를 전역 고정 3일 계약으로 만들지 않는다.
- 일상 사건 완료만으로 연대기 수식어·예술성을 자동 지급하지 않는다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`

정확한 기간·확률·보상·손실·복구 비용은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

### 2/10 — `BS-CONTENT-20260811-02`

```text
ADVENTURER_02 / TOREN_MARCH
토렌 마치 장거리 여정 개인 일정
JOURNEY_CONTINUITY_AND_RELIABILITY
```

목표:

- 기존 `WEIGHT / DURABILITY / ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY`만 소비해 장거리 환경 노출과 작품 신뢰성을 판단한다.
- 직접 이동·지도 경로 선택·실시간 생존 조작을 추가하지 않는다.
- 새 신뢰성·휴대성·수리 용이성 원수치를 만들지 않는다.
- 자동 매일 내구도 감소·루틴 수리세를 만들지 않는다.
- 결과는 도착·경로 노출·같은 UID 작품 상태를 분리하고 수리·복원·후속 강화·다음 여정 신작 이유로 환류한다.
- 정확한 기간·확률·마모량·수리량·보상·비용은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_ADVENTURER_02_TOREN_MARCH_LONG_RANGE_RELIABILITY_CANON_2026.md`

### 3/10 — `BS-CONTENT-20260811-03`

```text
SOLDIER_01 / MAREK_OLDEN
SMALL_LOT_STANDARD_ORDER
UNIT_READINESS_AND_STANDARD_FIT
```

목표:

- 기준품 + 소량 반복 제작으로 군인 유형을 검증하되 작품을 익명 stack으로 만들지 않는다.
- 첫 약 10개 fixture는 `NON_CANONICAL_BASELINE_TEST_PRESET`이고 각 작품 UID·비용·단조·강화·생애 결과를 보존한다.
- 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제를 추가하지 않는다.
- 결과는 `UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE`를 분리한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_SOLDIER_01_MAREK_OLDEN_SMALL_LOT_STANDARD_ORDER_CANON_2026.md`

### 4/10 — `BS-CONTENT-20260811-04`

```text
COLLECTOR_01 / ERSA_ROEN
EXHIBITION_EVIDENCE_AND_PROVENANCE
PUBLIC_MEANING_THROUGH_CRAFT_AND_LIFECYCLE_EVIDENCE
```

목표:

- `CRAFTSMANSHIP_EVIDENCE / LIVED_HISTORY_EVIDENCE`를 전시 의도 맥락으로 사용해 전투 밖에서도 작품 선택→세계 결과→같은 UID 생애 환류가 성립하는지 증명한다.
- 새 희귀도·위신·수집가·전시 총점을 만들지 않는다.
- Chronicle 개수, 최고 예술성, 최고 강화, 가장 오래된 작품 하나를 보편적 정답으로 만들지 않는다.
- 전시 횟수/전시 자체로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- 전시 실행은 비직접 세계 사건이며 플레이어는 대장장이·작품 증거 선택자로 남는다.
- 결과는 `EXHIBITION_RECEPTION_STATE / EXHIBIT_THESIS_FIT_STATE / ITEM_UID_PUBLIC_LEGACY_STATE`로 분리한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`

### 5/10 — `BS-CONTENT-20260811-05`

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
ARENA_RENOWN_THROUGH_EXPLAINABLE_EQUIPMENT_CONTRIBUTION
```

목표:

- 공개된 무기 범주·경기 맥락을 읽고 같은 작품 UID 한 점을 인계한다.
- 직접 전투 없이 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`를 분리한다.
- 새 투기장/명성/검투사/시그니처 총점, 최고 강화 자동정답, 승리=좋은 작품 단순화를 만들지 않는다.
- 경기/승리 반복으로 `ARTISTRY` 또는 `CHRONICLE_AFFIX`를 자동 성장시키지 않는다.
- legacy Kyle/iron_sword POC 수치와 점수식은 역사 fixture로 유지한다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`

### 6/10 — `BS-CONTENT-20260811-06`

```text
NOBLE_01 / CEREMONIAL_NOBLE
HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE
```

목표:

- 기존 가보 UID의 실제 상태·손상·과거 수리·소유·계승·Chronicle evidence와 공개된 계승 목적을 읽고 개입 깊이를 판단한다.
- 최대 복원·최고 Artistry를 자동 정답으로 만들지 않고 새 가문 위신·진품성·계승 총점을 추가하지 않는다.
- 물리 흔적을 처치하더라도 의미 있는 과거 생애 기록을 삭제하지 않는다.
- 같은 UID를 처치 전·후·의식·반환까지 보존한다.
- 복원/의식 반복으로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.
- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.

책임 원본:

- `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`

## R3 — 버티컬 슬라이스 기반

- 최신 정본 전용 데이터 Schema
- 작품 UID와 저장·로드
- 단일 앱 셸과 화면 전환
- 대표 제작·강화·고객·일정·연대기 경로
- 원인 설명 로그와 로컬 검증 데이터

기존 POC의 구형 품질·보조재료·범용 수식어 구조는 재사용하지 않는다.

`BS-CONTENT-20260811-01`부터 `BS-CONTENT-20260811-07`까지는 R3–R7 상세 **콘텐츠 설계** 승인이다. 어느 Decision도 실제 제품 구현을 열지 않는다.

## R4 — 콘텐츠와 경제

- 장비군·주재료·기능·고객 확장
- 판매·증여·복원·상속 소유권 상태
- 가격·예술성·수요 점감
- 피로도·장기 성장·세계 일정

## R5–R6 — 모바일 제품화

- Android 세로형 UX
- 접근성·성능·저사양 검증
- 아트·오디오·피드백
- 세이브 migration과 복구

## R7 — 첫 코어 버티컬 슬라이스

```text
대표 작품 한 점 직접 단조
→ 제작 등급·예술성·역할·중량 확인
→ 일반 강화 지속·중단
→ 대표 정밀강화와 촉매 계보
→ 고객에게 배정하고 성공률·핵심 원인 확인
→ 결과·연대기·손상 또는 복원
→ 같은 UID로 재방문
→ 다음 제작 판단
```

필수 행동 증거:

- 플레이어가 강화 지속·중단을 고민한다.
- 등급·예술성·촉매·연대기의 원인을 구분한다.
- 고객 결과와 작품 선택의 인과를 설명한다.
- 같은 작품의 변화와 다음 행동을 기억한다.

R3–R7 상세 콘텐츠 플레이테스트는 작품 선택 행동과 중립적 회상 인터뷰를 함께 사용한다. 실제 playable scope와 사람 검증은 아직 `NOT_RUN`이다.

## R8 — 적대적 최종 검토

- 핵심 재미와 모바일 복잡도
- 현재 정본·구형 문서·PR·데이터 충돌
- 저장·migration·접근성·성능
- 내부 테스트와 외부 사람 플레이테스트

## 구현 Gate

현재 상태:

```yaml
R3_R7_DESIGN_ACTIVE: true
BS-CONTENT-20260811-01: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-02: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-03: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-04: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-05: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-06: USER_APPROVED_PLANNING_ONLY
BS-CONTENT-20260811-07: USER_APPROVED_PLANNING_ONLY
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
HUMAN_PLAYTEST: NOT_RUN
VERTICAL_SLICE_TASK2: COMPLETE
NEW_PRODUCT_SCOPE: USER_DECISION_REQUIRED
```

R3–R7 기획 재개는 제품 코드·Scene·Resource·Godot authoring 범위를 자동으로 열지 않는다.

## 세 수식어 불변 계약

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

일반 수식어 A·B와 보조재료 슬롯은 재도입하지 않는다.

<!-- BS-CONTENT-20260811-07 CURRENT -->
## R3–R7 current 7/10 — Liana Soldier02

```text
R3_R7_DESIGN_ACTIVE
R3_R7_APPROVAL_COUNTER: 7/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-07
R3_R7_RESUME_LOCATOR: SOLDIER_02_LIANA_MISSION_FIT_APPROVED
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

Nadia 1/10, Toren 2/10, Marek 3/10, Ersa 4/10, Cassia 5/10, Noble01 6/10은 승인 이력으로 유지한다. 현재 Decision은 `BS-CONTENT-20260811-07`이다.

### 7/10 — `BS-CONTENT-20260811-07`

```text
SOLDIER_02 / LIANA_BERG
FRONTLINE_COMMANDER_MISSION_FIT_AND_PROTECTIVE_RESPONSIBILITY
MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE
```

목표:

- 기존 Liana 고객을 한 명의 전선 지휘관 책임 콘텐츠로 상세화한다.
- 공개된 임무·위험·필요 역할과 실제 작품 UID 증거를 비교해 한 작품을 인계한다.
- Marek의 multi-UID 소량 표준화와 Cassia의 arena contribution 책임을 침범하지 않는다.
- 임무 성공·리아나 귀환·같은 UID 작품 생애를 별도 결과로 유지한다.
- 최고 방어·최고 강화·command/hero/leadership/mission-fit 총점을 자동 정답으로 만들지 않는다.
- 직접 전술전투·대형/이동·실시간 병참·사상자 관리·baseline permadeath·replacement loop를 추가하지 않는다.
- 작품 단독 인과와 임무 반복 Artistry/Chronicle farming을 금지한다.
- 정확 임무·임계값·부상·경제·보상·분포는 `NON_CANONICAL_BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

책임 원본:

- `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`
- `docs/planning/BLACKSMITH_R3_SOLDIER_02_LIANA_BERG_FRONTLINE_COMMANDER_MISSION_FIT_CANON_2026.md`
