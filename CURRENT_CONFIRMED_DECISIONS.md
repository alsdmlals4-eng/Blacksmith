# [현재 정본] Blacksmith Current Confirmed Decisions

<!-- BS_OPS_20260811_03_PHASE_C_ENTRY -->
> **PLANNING_COMPLETE / BS-OPS-20260811-03 / PHASE_B_FINAL_REVIEW_COMPLETE / PHASE_C_ENTRY_APPROVED**
>
> 사용자가 `기획 완료`를 명시했다. R3–R7 기획 배치는 승인된 9/10에서 닫으며, 승인되지 않은 Decision10을 만들지 않는다. 이미 승인된 정본 구현만 Phase C로 진입하고 신규 제품 범위는 별도 Decision이 필요하다.
>
> `PLANNING_COMPLETE: USER_DECLARED` / `R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10` / `PHASE_B_FINAL_REVIEW: COMPLETE`
>
> `PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON`
>
> `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`
>
> `P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING`
>
> `IMAGE_GENERATION: DEFERRED_BY_USER`
>
> 전용 로컬 실행환경: self-contained Godot 4.7.1 (`_sc_`) → HiGodot HTTP `8006` / WS `9506` → `C:\Users\user\.codex-blacksmith` → exact Blacksmith 경로에서 Codex. 포트/process 존재는 readiness PASS가 아니며 Codex 내부 fresh HiGodot receipt 전 persistent mutation 금지.


<!-- R3_R7_PLANNING_BATCH_HISTORICAL_CLOSED_AT_9_OF_10 -->
> **HISTORICAL_R3_R7_DESIGN_ACTIVE / BS-CONTENT-20260811-09 / R3_R7_9_OF_10 / PLANNING_ONLY**
>
> 아래 블록은 `기획 완료` 이전 R3–R7 9/10 planning snapshot이다. 당시 `PRODUCT_IMPLEMENTATION: BLOCKED` / `TASK3_IMPLEMENTATION: NOT_APPROVED`였으며, 현재 Phase C gate는 위 `BS-OPS-20260811-03`이 소유한다.

<!-- R2_BATCH_006_CURRENT_AUTHORITY -->
> **R2_BATCH_006_APPROVED_MAIN_CANON**
>
> `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON / IMPLEMENTATION_APPROVED`
>
> source exact head: `388eff03c61126d8021601c3ab84efaa2133253e` / squash merge: `a8a94343c78a68bf7bb14b411e7741f43b257138`
>
> `R2_CHECKPOINT_005_CLOSED_MAIN_CANON / R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`
>
> planning exact head: `77eba15415bc9ede661639b45bb526d5ce4410a5` / planning squash merge: `31384d6397d798d2ac46bd3fb23ea2f4b0d67ad9`
>
> closure exact head: `51d4acf4fc31233b4b218a6f20589fdbf2557ee2` / closure squash merge: `06f03323c1309d8da0e6f5b9f4680a20ce388126`
>
> next batch: `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON` / 제품 구현: `BLOCKED` / 사람 플레이테스트: `NOT_RUN`


> R2 체크포인트 003: PR `#103` / closure `#104` / canon audit `#105`
>
> R2_CHECKPOINT_004 planning: PR `#106` / exact head `227b2dabf0d98832811415156e72f65d601332a9` / squash merge `789c73f38003f40dde5e9a99cd7dcb3ca03863f7`
>
> R2_CHECKPOINT_004 closure: PR `#107` / exact head `1ad791123eaf6c727e964380814ffb69f1357bbf` / squash merge `7a46fa38586a42f268cd0432744203049649ddd5`
>
> 폐쇄 배치: `R2_BATCH_004_CLOSED_2_OF_10 / CLOSED_MERGED_PR107`
>
> 현재 승인 배치: `R2_BATCH_006_APPROVED_10_OF_10 / MERGED_PR120_MAIN_CANON`
>
> 제품 구현: `BLOCKED`
>
> 버티컬 슬라이스 구현: `APPROVED / MERGED_PR120_MAIN_CANON / VERTICAL_SLICE_IMPLEMENTATION_APPROVED`

## 현재 운영 폐쇄 상태

```yaml
BLACKSMITH_BASELINE_MAIN_BEFORE_HANDOFF_REFRESH: fa9595b2df95897c915331a1cb5d9b1a583611f0
TASK2: TASK2_MAIN_MERGED
TASK2_MERGE_MAIN: a61a0bceec4254c4b78350980275cc9a903f9042
POSTMERGE: POSTMERGE_CI_CLOSURE_COMPLETE
CURRENT_TECHNICAL_BASELINE: fa9595b2df95897c915331a1cb5d9b1a583611f0
HIGODOT_EXECUTION_DECISION: BS-HIGODOT-EXEC-20260808-01
HIGODOT_PRODUCTION_EXECUTION_PATH: PROVEN_TASK2_COMPLETED
TOOLCHAIN_CURRENT_VERSION_DECISION: BS-TOOLCHAIN-20260811-02
GODOT_AI_CURRENT_VERSION: 3.1.4
R3_R7_DESIGN_STATE: R3_R7_PLANNING_BATCH_CLOSED_AT_9_OF_10
R3_R7_APPROVAL_COUNTER: 9/10
R3_R7_CURRENT_DECISION: BS-CONTENT-20260811-09
PLANNING_COMPLETE: USER_DECLARED
R3_R7_PLANNING_BATCH: CLOSED_AT_9_OF_10
PHASE_B_FINAL_REVIEW: COMPLETE
LOCAL_EXECUTOR_DECISION: BS-OPS-20260811-03
P0_LOCAL_EXECUTOR_BOOTSTRAP: REQUIRED_BEFORE_PERSISTENT_GODOT_AUTHORING
NEW_PRODUCT_SCOPE: NEW_PRODUCT_SCOPE_USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON
HISTORICAL_R3_TASK3_IMPLEMENTATION: NOT_APPROVED
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
HISTORICAL_R3_PRODUCT_IMPLEMENTATION: BLOCKED
PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
IMAGE_GENERATION: DEFERRED_BY_USER
HUMAN_PLAYTEST: NOT_RUN
ANDROID_DEVICE: NOT_RUN
PRE_WORK_RESEARCH_DECISION: BS-OPS-20260811-02
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
```

`BS-HIGODOT-EXEC-20260808-01`의 실제 PROVE→PUBLISH→PR #131 병합과 PR #139/#140 postmerge CI 복구가 Task2 실행 경로를 폐쇄했다. 아래 `BS-HIGODOT-20260808-01` 항목에 남아 있는 `BLOCKED_UNAVAILABLE_OR_UNVERIFIED`와 PR #131 별도 승인 문구는 **실행 전 activation-stage 역사 증거**이며 현재 상태를 뜻하지 않는다. 현재 동일 범위 기술 작업은 끝났고 새 제품 Task는 사용자 결정이 필요하다.

## 1. 프로젝트 코어

> 제한된 하루 작업량 안에서 작품을 만들고, 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 작품이 고객과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 단조와 출생 등급
→ 강화 성공·실패와 멈춤 판단
→ 정밀강화 방식·촉매 선택
→ 고객·세계에 작품 전달
→ 같은 UID의 연대기·손상·복원 결과
→ 다음 제작·강화 판단
```

## 2. 현재 승인 Decision

- `BS-WORLD-20260803-03`: 고객 개인 일정과 날짜 예고형 세계 일정 분리
- `BS-CUSTOMER-20260803-02`: 위험도·능력치 `1~10`, 예상 성공률 `5~95%`
- `BS-CUSTOMER-20260805-01`: 근력·기량·체력·판단력, 희소 무기·갑옷 적성, 마력 적성, 장비 적합성 — `R2_BATCH_005_2_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-UX-20260805-01`: 모바일 고객 카드 3단계 정보 공개와 설명 가능한 장비 판단 — `R2_BATCH_005_3_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-CUSTOMER-20260806-01`: 강화 중심 단순 장비 판정과 근력 기반 최대 중량 게이트 — `R2_BATCH_005_4_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-01`: 장비군 고정 기본 중량 포인트와 중량 전용 ±5 강화 효과 — `R2_BATCH_005_5_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-02`: 중량 성능 예산 기억과 정밀강화 경량화·중량화 기회비용 — `R2_BATCH_005_6_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-03`: 중량 성능 예산 1점 환산과 장비 역할 프리셋 자동 배분 — `R2_BATCH_005_7_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-04`: 작품군 단일 역할 원수치와 최초 마법·유틸리티 기능 카탈로그 — `R2_BATCH_005_8_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-05`: 최초 제작 역할 수치 테스트 프리셋과 강화·특수기능 변동 소유권 — `R2_BATCH_005_9_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-ITEM-20260806-06`: 주재료 역할 적합·직접 단조 결과·기능 레시피·사람 플레이테스트 Gate — `R2_BATCH_005_10_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-SCHEDULE-20260804-01`: 주요 일정·소식·묶음 요약·일정 장부
- `BS-CONTENT-20260804-01`: 고객 결과·작품 UID 상태·다음 제작 환류
- `BS-CONTENT-20260804-02`: 검투사·모험가·군인·귀족과 초기 콘텐츠 가족
- `BS-CONTENT-20260811-01`: `ADVENTURER_01` 나디아 벤 유적 탐사 개인 일정. `생환 + 회수`를 목표로 작품 한 점을 맡기고, 하루 종료당 최대 한 번 진행하며, 같은 UID의 즉시 인과 결과와 지연 생애·복원·후속 강화 이유를 만든다. 직접 전투·탐험 미니게임과 단일 항상최적 장비 정답은 추가하지 않는다. — `USER_APPROVED / R3_R7_1_OF_10 / MERGED_PR142_MAIN_CANON / PLANNING_ONLY`
- `BS-CONTENT-20260811-02`: `ADVENTURER_02` 토렌 마치 장거리 여정 개인 일정. 여정 지속성·신뢰성을 목표로 기존 중량·강화·내구도·실제 관련 환경/현장정비 기능을 비교하며, 직접 여행 조작·새 신뢰성/수리성 원수치·자동 마모세를 추가하지 않고 같은 UID의 마모·현장 유지보수·손상 결과를 수리·복원·후속 강화·다음 여정 신작 이유로 환류한다. — `USER_APPROVED / R3_R7_2_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-03`: `SOLDIER_01` 마레크 올덴 소량 표준 주문. 기준품 한 점을 직접 만든 뒤 반복 설정은 압축할 수 있지만 약 10개 baseline fixture의 각 작품은 독립 UID·비용·작업·단조·강화·연대기를 유지한다. 결과는 `UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE`로 분리하며 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제를 추가하지 않는다. — `USER_APPROVED / R3_R7_3_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-04`: `COLLECTOR_01` 에르사 로엔 전시 증거·계보 콘텐츠. `CRAFTSMANSHIP_EVIDENCE / LIVED_HISTORY_EVIDENCE`를 전시 의도 맥락으로 공개하고 작품 한 점의 실제 제작·생애 증거를 비교한다. 새 희귀도·위신·수집가·전시 총점과 Chronicle 개수 최적화를 만들지 않으며 같은 UID의 결과를 `EXHIBITION_RECEPTION_STATE / EXHIBIT_THESIS_FIT_STATE / ITEM_UID_PUBLIC_LEGACY_STATE`로 분리한다. — `USER_APPROVED / R3_R7_4_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-05`: `GLADIATOR_01` 카시아 벨란 투기장 대표 무기·공개 생애 콘텐츠. 요청 무기 범주와 경기 맥락을 공개하고 작품 한 점을 인계하며, 직접 전투 없이 결과를 `ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE`로 분리한다. 새 투기장/명성 총점·최고 강화 자동정답·승리=좋은 작품 단순화·경기 반복 Artistry/Chronicle 파밍을 만들지 않고 같은 UID를 보존한다. legacy Kyle/iron_sword POC 고정 수치·점수식은 역사 fixture로만 유지한다. — `USER_APPROVED / R3_R7_5_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-06`: `NOBLE_01` 의례 귀족 가보 계승 복원·유산 콘텐츠. 기존 `CEREMONIAL_NOBLE` 대표 ID와 같은 작품 UID의 실제 손상·수리·소유·계승·연대기 증거를 읽고, 계승 의식 전에 어디까지 수리·복원·재작업할지 판단한다. 최대 복원·최고 Artistry를 자동 정답으로 만들지 않고 가문 위신·진품성·계승 총점을 추가하지 않으며, 결과를 `CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE`로 분리한다. — `USER_APPROVED / R3_R7_6_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-07`: `SOLDIER_02` 리아나 베르크 전선 지휘관 임무 적합·보호 책임 콘텐츠. 공개된 임무·위험·장비 역할을 읽고 실제 작품 UID 한 점을 선택·인계하며 직접 전술전투 없이 결과를 `MISSION_DUTY_STATE / COMMANDER_RETURN_STATE / ITEM_UID_FIELD_LEGACY_STATE`로 분리한다. Marek의 소량 표준화와 Cassia의 arena contribution 책임을 보존하고, 새 command/hero/leadership/mission-fit 총점·최고 방어/강화 자동정답·작품 단독 인과·baseline permadeath·임무 반복 Artistry/Chronicle 파밍을 만들지 않으며 같은 UID를 보존한다. — `USER_APPROVED / R3_R7_7_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-08`: `COLLECTOR_02` 세드릭 바엘 기록 보관 accession·출처·custody 콘텐츠. 공개된 장기 보관 목적과 실제 작품 UID의 제작·소유·custody·생애 근거를 읽어 같은 UID 한 점을 인계한다. 결과는 `ARCHIVE_ACCESSION_STATE / PROVENANCE_DOCUMENTATION_STATE / ITEM_UID_CUSTODY_LEGACY_STATE`로 분리한다. Ersa의 공개 전시 책임과 Noble01의 물리적 처치 깊이 책임을 보존하며, 진품성/출처/위신 총점, 최고 Artistry·가장 오래된 작품·최고 강화 자동정답, 기록 조작, archive/museum 관리, accession 반복 Artistry/Chronicle farming을 만들지 않는다. `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`는 유지한다. — `USER_APPROVED / R3_R7_8_OF_10 / PLANNING_ONLY`
- `BS-CONTENT-20260811-09`: `GLADIATOR_02` 카일 바렌 베테랑 복귀 장비 연속성·교체 콘텐츠. 실제 prior Kyle 작품의 현재 상태와 생애 기록을 읽고 hard serviceability/eligibility 뒤 `KEEP_IN_SERVICE` 또는 `RETIRE_AND_REPLACE`를 선택한다. keep은 같은 UID를 보존하고, replace는 old UID/history를 보존한 채 distinct new UID로 시작한다. Cassia arena-fit과 Noble01 treatment-depth 책임을 보존하며 legacy `gladiator_kyle/iron_sword` fixed score는 historical fixture로만 남긴다. 결과는 `VETERAN_RETURN_STATE / EQUIPMENT_CONTINUITY_STATE / ITEM_UID_LINEAGE_STATE`로 분리한다. — `USER_APPROVED / R3_R7_9_OF_10 / PLANNING_ONLY`
- `BS-CRAFT-20260804-04`: 보조재료 제거와 정밀강화 방식·촉매 책임 분리
- `BS-CRAFT-20260804-05`: 촉매 수식어 씨앗·계보·진화
- `BS-CRAFT-20260804-06`: `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- `BS-CRAFT-20260804-07`: 제작 등급 5단계와 출생 전설 고정 — `MERGED_PR106 / MAIN_CANON`
- `BS-CRAFT-20260805-01`: 예술성을 고정 설계 최대치 없는 숫자형 무기·작품 능력치로 확정 — `MERGED_PR106 / MAIN_CANON`
- `BS-CRAFT-20260805-02`: 예술성 초기 생성·후천 성장·가치 점감·고객 선호 경계 — `R2_BATCH_005_1_OF_10 / MERGED_PR109 / MAIN_CANON`
- `BS-UX-20260804-01`: 조합 장비명과 UID 연대기 상세
- `BS-OPS-20260804-02`: 정본 드리프트·구형 문서 상태 관리
- `BS-OPS-20260805-01`: 벤치마킹·조기 체크포인트·상시 TDD
- `BS-OPS-20260811-02`: 모든 의미 있는 작업 전에 fresh preflight → 벤치마킹 → 최신 현업/공식/1차 자료 → `ADOPT / ADAPT / REJECT / DIFFERENTIATOR` → 정본 충돌 → 적대 pre-check를 요구한다. 작업 유형별 조사 강도를 적용하고 `BENCHMARK_NOT_APPLICABLE`은 저위험 작업에서 사유를 남긴 제한적 예외다. `BS-OPS-20260805-01`의 benchmark scope만 refine하며 TDD·early checkpoint는 그대로 보존한다. — `USER_APPROVED / PRE_WORK_RESEARCH_GATE / PLANNING_ONLY`
- `BS-CORE-20260811-01`: 기존 저위험 연속강화를 성장형 `AUTO_ENHANCEMENT_CAP_UNLOCK`으로 refine한다. 초기 `수동 15회 → AUTO_CAP +20`을 보존하고, 이후 분야별 기술 돌파보다 한 10강 밴드 뒤까지 목표 지정 자동 강화를 해금한다. 정상 확률·비용·자원·UID 이력을 보존하고 `HIGH / VERY_HIGH`, 정밀강화, 기술 돌파, 무보호 파괴 가능 시도는 자동화하지 않는다. — `USER_APPROVED_DIRECTION / PLANNING_ONLY`
- `BS-HERA-20260808-01`: Hera Agent Godot 1.0.0 vendor tree의 main 존재와 당시 `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE` 상태를 확정한 reconciliation Decision이다. authoring/mutation authority를 `NONE`으로 유지한다. 현재 plugin 활성화 상태는 `BS-TOOLCHAIN-20260809-01`이 후속으로 대체하지만 이 역사 증거와 Hera 권위 `NONE`은 유지된다. — `USER_APPROVED_RECONCILIATION / MERGED_PR132_MAIN_CANON / HISTORICAL_ACTIVATION_STATE`
- `BS-HIGODOT-20260808-01`: HiGodot production authoring 권위를 `FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY / USER_APPROVED_ACTIVE`로 활성화한다. 현재 승인은 `TASK2_SCOPED_AUTHORING_ONLY`이며 일반 제품 구현은 `BLOCKED`로 유지한다. `.tscn`·Resource·`project.godot`은 실제 HiGodot production authoring execution path와 저작 provenance 없이 일반 코드 편집·GitHub API 텍스트 치환으로 우회하지 않는다. 현재 실행 경로는 `BLOCKED_UNAVAILABLE_OR_UNVERIFIED`; GUT는 sole test authority, Hera authority는 `NONE`, PR #131 병합은 별도 승인이다. — `USER_APPROVED_PRODUCTION_AUTHORING_ACTIVATION / SCENE_PROJECT_GREEN_BLOCKED_PENDING_COMPLIANT_EXECUTION_PATH`
- `BS-TOOLCHAIN-20260809-01`: Godot AI vendor/runtime을 `3.1.3`으로 전환하고 GUT 9.7.1 및 Hera Agent Godot 1.0.0 editor plugin 활성화를 승인한다. 현재 plugin 활성화 상태는 `Godot AI + GUT + Hera`이며, 이는 권위 확장이 아니다. HiGodot은 `TASK2_SCOPED_AUTHORING_ONLY` Godot 직렬화 저작 권위, GUT은 `SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY`, Hera는 `VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE / AUTHORITY_NONE`을 유지한다. Hera의 tracked/serialized mutation은 별도 범위 승인 전 금지한다. — `USER_APPROVED_ACTIVE / GITHUB_VENDOR_3_1_3_AND_EDITOR_PLUGIN_STATE_READBACK_PROVEN`
- `BS-TOOLCHAIN-20260811-02`: 현재 Godot AI vendor를 공식 `v3.1.4` exact upstream tree로 승격한다. Task2의 실제 `3.1.3` 실행·PROVE·PUBLISH 증거는 역사로 유지하고, Task2 전용 `set_main_scene` vendor overlay는 현재 vendor에서 재도입하지 않는다. GUT 9.7.1·Hera 비권위 상태·HiGodot scoped authoring authority·제품/Task3 차단은 변경하지 않는다. — `USER_APPROVED / CURRENT_VENDOR_3_1_4 / EXACT_UPSTREAM_V3_1_4 / PRODUCT_BLOCKED / TASK3_NOT_APPROVED`

## 3. 제작 등급

```text
[보통] → [우수] → [명품] → [걸작] → [전설]
```

- 최초 직접 단조 완료 시 한 번 확정
- 동일 UID에서 영구 고정
- 제작 후 승격·강등 없음
- `전설`은 최초 제작에서만 극희귀하게 발생
- 제작 등급은 예술성 최소값·상한·배율을 결정하지 않음
- 정확한 확률·배율은 `BASELINE_TEST_PRESET`

## 4. 예술성 원수치

```text
예술성 27
```

- 무기·작품 능력치의 하나
- `0` 이상의 정수, 소수점 없음
- 고정 설계 최대치 없음
- 분모·별점·백분율·예술성 단계명 없음
- 제작 등급과 별도 축
- 다른 능력치와 함께 원수치 표시
- 전투 성능을 기본적으로 올리지 않음
- 범용 전투력·수식어 배율이 아님
- 기술적 자료형 한계는 콘텐츠 최대치가 아님

```text
NON_NEGATIVE_INTEGER_NO_FIXED_DESIGN_MAXIMUM
```

## 5. 예술성 생성·성장·가치 평가

```text
artistry = 작품 UID에 저장되는 원수치
artistry_value = 시장·감정 맥락의 파생 점감 가치
customer_artistry_fit = 고객·일정 맥락의 파생 적합도
```

### 최초 제작 허용 원천

```text
BASE_ITEM_DESIGN_AESTHETIC_TENDENCY
MATERIAL_VISUAL_PROCESSING_FIT
DIRECT_FORGING_AESTHETIC_RESULT
```

- 재료 가격·희귀도 자체는 예술성으로 직접 변환하지 않음
- 제작 등급을 예술성 보너스표로 변환하지 않음
- 별도 보조재료·장식재료 슬롯을 추가하지 않음

### 제작 후 허용 성장 원천

```text
ARTISTIC_FINISH
ARTISTRY_OWNED_CATALYST_EFFECT
APPROVED_FINISHING_OR_DECORATION_CONTENT
MEANINGFUL_ARTISTIC_REWORK
```

다음은 예술성을 자동 증가시키지 않는다.

```text
GENERAL_ENHANCEMENT_LEVEL
SALE
GIFT
EXHIBITION_COUNT
APPRAISAL_COUNT
OWNERSHIP_TRANSFER
FAME
CHRONICLE_EVENT
LOW_COST_REPEAT_ACTION
```

### 가치 평가

```text
최종 가치
= 기능 가치
+ 제작 등급 가치
+ 예술성 점감 가치
+ 촉매 수식어 가치
+ 연대기 가치
+ 고객·시장 수요 보정
```

```text
ADDITIVE_COMPONENTS_WITH_PIECEWISE_DIMINISHING_MARGINAL_VALUE
```

- 예술성이 증가하면 가치 기여는 감소하지 않음
- 높은 구간일수록 추가 1점의 한계 가치는 작아짐
- 원수치는 압축하지 않음
- 구간별 한계 가치 테이블을 우선
- 제작 등급·재료·예술성·촉매·연대기의 연속 곱셈 금지
- 같은 원인의 이중 계산 금지

### 고객 관심 유형

```text
IGNORE / SECONDARY / PRIMARY / REQUIREMENT
```

예술성에 관심 없는 고객은 초과 예술성에 추가 비용을 지불하지 않을 수 있지만, 높은 예술성 자체에 패널티를 주지 않는다.

### 악용 방지

- 수리·손상·판매·전시·감정·증여 반복으로 예술성 순증가 금지
- 동일 저비용 세공 반복 파밍 금지
- 촉매 직접 증가와 가격·수식어 배율의 이중 계산 금지
- 연대기·명성은 예술성 원수치를 자동 변경하지 않음
- 모든 예술성 변화는 작품 UID와 출처를 기록

정확한 초기 분포·증감값·가격 구간·고객 요구치는 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 6. 고객 능력·장비 적합성

```text
근력 / 기량 / 체력 / 판단력 = 각 1~10
무기 적성 / 갑옷 적성 = 희소 저장, 0~3
마력 적성 = 0~10, 선택 친화 태그 최대 2개
```

작품 종류는 `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`로 분리한다. 공통 작품 능력치는 `WEIGHT / DURABILITY / HANDLING / ARTISTRY`, 조건부 능력치는 `ATTACK / DEFENSE / STABILITY / ENVIRONMENTAL_RESPONSE / SPECIAL_FUNCTIONS`다. 적용되지 않는 수치는 생략한다.

현재 착용 조합에서 `TOTAL_WEIGHT / COMFORTABLE_LOAD / BALANCE_STATE / SPECIAL_FUNCTION_FIT`을 파생한다. 균형 상태는 `부적합 / 불안정 / 안정 / 능숙`이며, 적정 하중 이내에는 중량 페널티가 없고 초과 시 단계적으로 부담이 증가한다.

고객 능력은 작품 공격·방어 값을 직접 다시 더하지 않는다. 작품 원수치는 UID에 남고 고객 능력·적성은 활용도·위험·예상 성공률을 조정한다. 정확한 공식은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.

## 7. 작품 이름과 수식어

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

연대기 수식어를 누르면 같은 UID의 형성 사건·주요 타임라인·진화 계보·소유·손상·복원 기록을 읽기 전용 하단 패널에서 확인한다.

## 8. 운영 계약

- 질문·추천·새 시스템 설계 전 벤치마킹·현업 비교
- 결과를 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록
- 승인 10건은 최대 배치 크기
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT` 조기 체크포인트 허용
- 작업마다 TDD: `RED → GREEN → REFACTOR`
- 병합은 명시적 사용자 승인 필요

`R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109 / MAIN_CANON`이다.

## 9. 보호 조건

- 일반 수식어 A·B 재도입 금지
- 보조재료 슬롯 재도입 금지
- 세 수식어 교차 생성·진화·덮어쓰기 금지
- 제작 등급 후천 변경 금지
- 예술성 고정 설계 최대치·분모 표기·named tier 재도입 금지
- 예술성을 범용 전투력·수식어 배율로 변환 금지
- 예술성·연대기·명성을 하나의 영구 총점으로 통합 금지
- 제품 구현: `BLOCKED`

<!-- BS-UX-20260805-01 -->
## 모바일 고객 카드 정보 계층

```text
기본 카드 → 장비 선택 후 판단층 → 상세 보기
```

- 기본: 고객 역할·일정, 4능력치, 관련 주·보조 적성, 관련 시 마력 적성
- 장비 선택 후: 균형·예상 성공률·핵심 원인 2~4개·관련 특수기능 위험
- 상세: 전체 관련 적성, 총 중량·적정 하중, 특수기능 근거, 적용 능력치
- 전체 적성 행렬 기본 노출 금지
- 불투명한 결과 전용 적합도 점수 금지
- 색상·길게 누르기·호버 단독 핵심 정보 금지
- 최소 `48dp` 터치 목표
- 제품 구현: `BLOCKED`

<!-- BS-CUSTOMER-20260806-01 -->
## 강화 중심 단순 장비 판정

```text
최대 중량 = 근력 × 10
총 중량 ≤ 최대 중량 → 사용 가능, 보너스·페널티 없음
총 중량 > 최대 중량 → 중량 초과, 배정 불가
```

```text
위험도 기본 성공률
+ 강화 레벨(+1당 +1%p)
+ 관련 능력 충족(+5%p)
+ 적성 보정(-10/0/+5/+10%p)
```

- 강화가 주효과이며 고객 능력·적성은 작은 보조 보정이다.
- `COMFORTABLE_LOAD / BALANCE_STATE / 단계적 초과 페널티`는 현재 중량 계약이 아니다.
- 공격·방어·조작성·예술성 원수치를 일반 성공률에 범용 합산하지 않는다.
- 제품 구현: `BLOCKED`

<!-- BS-ITEM-20260806-01 -->
## 장비군 기본 중량 포인트

```text
장신구 0 / 도구 5
의복·로브 5 / 경갑 10 / 중갑 20 / 중장갑 30
검·원거리·방패보조 10 / 도끼·둔기 15 / 장병기 20
```

`ITEM_WEIGHT = max(0, BASE_WEIGHT + EXPLICIT_WEIGHT_MODIFIER)`다. 중량 전용 효과는 작품당 하나만 허용하며 `LIGHTWEIGHT -5 / NONE 0 / WEIGHTED +5`다. 재료·제작 등급·예술성·공격·방어·조작성·내구도·일반 강화 단계는 중량을 자동 변경하지 않는다. 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-02 -->
## 중량 성능 예산 기억과 정밀강화 중량 조정

```text
최초 제작 중량 5당 초기 성능 예산 +1
경량화 -5 중량 / 기존 예산 유지
중량화 +5 중량 / 과거 최고 인정 중량 초과분만 예산 추가
```

고객 배정은 현재 중량을 사용하고 성능 예산은 UID의 역대 최고 인정 중량을 사용한다. 중량 조정은 `+10/+20/+30/+40/+50` 정밀강화에서만 선택하며 이정표당 최대 한 번, 서로 다른 이정표에서는 누적할 수 있다. 같은 이정표의 반복·환불은 허용하지 않는다. 중량 성능 예산은 공격·방어·마법 기능·유틸리티 중 호환 축 하나에만 배분하며 일반 사건 성공률에는 직접 더하지 않는다.

제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-03 -->
## 중량 성능 예산 환산과 자동 역할 프리셋

```text
1 ATTACK_BUDGET = ATTACK +5
1 DEFENSE_BUDGET = DEFENSE +5
1 MAGIC_FUNCTION_BUDGET = MAGIC_FUNCTION_CAPACITY +1
1 UTILITY_BUDGET = UTILITY_CAPACITY +1
```

- 기본 작품 설계가 최초 제작 시 하나의 역할 프로필을 확정한다.
- 무기는 기본 공격, 방어구·방패는 기본 방어, 도구·의복은 기본 유틸리티로 자동 배분한다.
- 마법 장비 프로필은 승인된 기본 작품 설계에만 명시한다.
- UID 생성 후 플레이어 자유 재배분과 별도 포인트 배분 UI는 없다.
- 새 최고 중량 예산은 기존 프로필에 자동 배분한다.
- 경량화는 기존 공격·방어·기능 용량을 유지한다.
- 일반 사건 성공률에는 자동 합산하지 않는다.
- 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-04 -->
## 작품 역할 원수치와 최초 특수기능 카탈로그

- Decision: `BS-ITEM-20260806-04`
- 상태: `R2_BATCH_005_8_OF_10 / MERGED_PR109 / MAIN_CANON`
- 모델: `SINGLE_PRIMARY_RAW_STAT_PLUS_OPTIONAL_FUNCTIONS`
- 무기는 공격, 방패·갑옷은 방어를 주 역할 원수치로 사용한다.
- 표시 공격·방어는 최초 제작 + 중량 기반 + 승인된 강화 출력만 가산한다.
- 기본 다중 전투 보조 수치는 추가하지 않는다.
- 최초 마법 기능: `ARCANE_CONDUCTION / ELEMENTAL_WARD / ARCANE_SENSING`.
- 최초 유틸리티 기능: `ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY / TASK_INTEGRATION`.
- 기능 용량은 기능을 자동 생성하지 않으며 일반 사건 성공률에 자동 합산하지 않는다.
- 제품 구현: `BLOCKED`.

<!-- BS-ITEM-20260806-05 CURRENT AUTHORITY -->
## 현재 작품 역할 수치·강화 변동 소유권

- Decision: `BS-ITEM-20260806-05 / R2_BATCH_005_9_OF_10`
- 통합 변동 장부: `GENERAL_ENHANCEMENT / STAT_METHOD / FUNCTION_REWORK`
- 최초 역할 수치: `장비군 기준값 5·10·15 + 주재료 -2·0·+2 + 직접 단조 -1·0·+1`
- 일반 강화: 강화 단계와 사건 성공률 `+1%p/단계`만 소유하고 작품 원수치를 자동 변경하지 않음
- 정밀강화: 공격·방어·취급·예술성 `+5`, 경량화·중량화 `±5`, 환경 기능 재작업 중 한 패키지만 선택
- 기능 재작업: `ADD / REPLACE / REBIND / REMOVE`, 정밀 이정표 소비, 실패 시 기존 기능 보존
- Google Sheet 미러: `42_능력치_강화_참조표`
- 밸런스: `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`
- 제품 구현: `BLOCKED`

## 16. 주재료 역할 적합·기능 레시피·사람 플레이테스트

- 철은 모든 역할 장비에서 `STANDARD_ROLE_FIT(0)`이다.
- 은은 검·원거리·경갑에 `+2`, 도끼·둔기·장병기·중장갑에 `-2`다.
- 운석철은 도끼·둔기·장병기·중장갑에 `+2`, 원거리·경갑에 `-2`다.
- 직접 단조 역할 타격은 `OUTSIDE / GOOD / PERFECT = -1 / 0 / +1`이며 제작 등급과 분리된다.
- 최초 기능은 `ROLE_PROFILE_MATERIAL_WEIGHT_CONTEXT_CAPACITY` 레시피를 충족할 때만 결정적으로 생성된다.
- 현재 즉시 가용한 결속 재작업은 `ELEMENTAL_WARD(FIRE)`와 `ENVIRONMENTAL_SEALING(FIRE)`다.
- 솔로 48케이스와 외부 3~5명 검증 전까지 수치는 `BASELINE_TEST_PRESET_USER_PLAYTEST_REQUIRED`다.
- 사람 플레이테스트: `NOT_RUN`.
- 제품 구현: `BLOCKED`.

## 17. R3–R7 첫 상세 콘텐츠 — 나디아 벤 유적 탐사

Decision: `BS-CONTENT-20260811-01`.

```text
ADVENTURER_01 / NADIA_VENN
유적 탐사 개인 일정
생환 + 회수
```

- 나디아는 모험가 유형 대표 고객·유적 탐사대장이다.
- 플레이어는 직접 탐험하거나 전투하지 않고 작품 한 점을 골라 인계한다.
- 선택 축은 강화 단계·위험, 중량/고객 적합, 실제 관련 환경·유틸리티 적합이다.
- 단일 항상최적 장비 정답을 만들지 않는다.
- 일정은 `PERSONAL_SCHEDULE`이며 활성 중 `ONE_END_OF_DAY_CHECK_MAXIMUM_WHILE_ACTIVE`를 따른다.
- `PREP_AND_ENTRY → HAZARD_AND_RECOVERY_ATTEMPT → RETURN_AND_RESULT`는 구조 상태이며 고정 3일 계약이 아니다.
- 결과는 귀환·회수·같은 UID 작품 상태를 분리하고, 즉시 인과 결과 뒤 복원·후속 강화·새 제작 이유로 환류한다.
- 일상 사건 완료만으로 `CHRONICLE_AFFIX`나 예술성을 자동 지급하지 않는다.
- 정확한 기간·확률·보상·손실·복구 비용은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 책임 원본: `docs/planning/BLACKSMITH_R3_ADVENTURER_01_NADIA_VENN_RUINS_SURVIVAL_RECOVERY_CANON_2026.md`.
- Registry: `docs/planning/CURRENT_R3_R7_CANON_REGISTRY.json`.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 18. R3–R7 두 번째 상세 콘텐츠 — 토렌 마치 장거리 여정

Decision: `BS-CONTENT-20260811-02`.

```text
ADVENTURER_02 / TOREN_MARCH
장거리 여정 개인 일정
JOURNEY_CONTINUITY_AND_RELIABILITY
```

- 플레이어는 토렌을 직접 이동시키거나 지도에서 경로를 선택하지 않고 작품 한 점을 비교·인계한다.
- 새 신뢰성·휴대성·수리 용이성 원수치를 만들지 않고 `WEIGHT / DURABILITY / ENVIRONMENTAL_SEALING / FIELD_SERVICEABILITY`의 현재 소유권을 소비한다.
- `OVERWEIGHT`는 배정 불가 Gate이며 강화는 일반 사건 성공의 주효과를 유지한다.
- 환경·현장정비 기능은 실제 결속 맥락에서만 `ELIGIBILITY / RISK_MITIGATION / SPECIFIC_INTERACTION`으로 작동한다.
- 자동 매일 내구도 감소나 루틴 완료 강제 수리를 만들지 않는다.
- 일정은 `PREP_AND_DEPARTURE → EXPOSURE_AND_ROUTE_ADAPTATION → ARRIVAL_AND_ITEM_ASSESSMENT` 구조이며 고정 3일 계약이 아니다.
- 결과는 `JOURNEY_ARRIVAL_STATE / ROUTE_EXPOSURE_STATE / ITEM_UID_LIFECYCLE_STATE`를 분리하고 같은 UID를 수리·복원·후속 강화·다음 여정 신작 판단으로 돌려보낸다.
- 정확한 기간·확률·마모량·수리량·보상·비용은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 19. R3–R7 세 번째 상세 콘텐츠 — 마레크 올덴 소량 표준 주문

Decision: `BS-CONTENT-20260811-03`.

```text
SOLDIER_01 / MAREK_OLDEN
SMALL_LOT_STANDARD_ORDER
UNIT_READINESS_AND_STANDARD_FIT
```

- 첫 검증 수량은 `ORDER_QUANTITY = 10 / NON_CANONICAL_BASELINE_TEST_PRESET`다.
- 기준품 뒤 반복 설정은 압축할 수 있지만 각 작품의 UID·비용·작업·단조·강화·연대기는 독립한다.
- 결과는 `UNIT_MISSION_STATE / STANDARD_ADOPTION_STATE / BATCH_ITEM_LIFECYCLE_STATE`로 분리한다.
- 직접 전술 전투·실시간 병참·작업자 생산라인·무료 복제·불투명 표준화 점수는 추가하지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 20. 자동 강화 최대치 해금

Decision: `BS-CORE-20260811-01 / AUTO_ENHANCEMENT_CAP_UNLOCK`.

- 기존 `수동 강화 15회 뒤 해금 / +1~+20` 저위험 연속강화를 보존한다.
- 이후 해당 분야의 수동 기술 돌파보다 한 10강 밴드 뒤까지 자동 상한을 해금한다.
- 플레이어가 목표 강화 수치를 지정하며 목표는 해당 분야 `AUTO_CAP` 이하만 가능하다.
- 자동 시도는 정상 강화 확률·비용·자원·작업 기회비용·동일 UID 이력을 그대로 사용한다.
- `HIGH / VERY_HIGH`, 정밀강화, 기술 돌파, 무보호 파괴 가능 시도는 수동 전용이다.
- 이 시스템 Decision은 R3 콘텐츠 승인 카운터를 증가시키지 않는다.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 21. R3–R7 네 번째 상세 콘텐츠 — 에르사 로엔 전시 증거·계보

Decision: `BS-CONTENT-20260811-04`.

```text
COLLECTOR_01 / ERSA_ROEN
EXHIBITION_EVIDENCE_AND_PROVENANCE
CRAFTSMANSHIP_EVIDENCE / LIVED_HISTORY_EVIDENCE
```

- 플레이어는 전시관 운영자가 아니라 대장장이이며, 공개된 전시 의도에 맞춰 같은 작품 UID 한 점과 그 작품에 이미 존재하는 제작·생애 증거를 선택한다.
- `CRAFTSMANSHIP_EVIDENCE`는 제작 등급·Artistry·단조·마감·촉매·재작업 provenance 등 실제 제작 증거를, `LIVED_HISTORY_EVIDENCE`는 소유·세계 사용·손상·분실·회수·수리·복원·Chronicle 등 실제 생애 증거를 소비한다.
- `RARITY_SCORE / PRESTIGE_SCORE / COLLECTOR_SCORE / EXHIBITION_SCORE`를 추가하지 않는다.
- Chronicle 개수·가장 오래된 작품·최고 예술성·최고 강화를 보편적 자동 정답으로 만들지 않는다.
- 전시 횟수 또는 전시 자체만으로 `ARTISTRY`가 증가하거나 `CHRONICLE_AFFIX`가 자동 부여되지 않는다.
- 결과는 `EXHIBITION_RECEPTION_STATE / EXHIBIT_THESIS_FIT_STATE / ITEM_UID_PUBLIC_LEGACY_STATE`로 분리하며 2~4개의 실제 원인을 설명한다.
- 같은 작품 UID를 전시 전·중·후 보존하고 후속 제작·복원·판매·재전시 판단으로 환류한다.
- 직접 전시 미니게임·전시관 장식·방문객 관리·경매·실시간 큐레이터 조작을 추가하지 않는다.
- 책임 원본: `docs/planning/BLACKSMITH_R3_COLLECTOR_01_ERSA_ROEN_EXHIBITION_EVIDENCE_CANON_2026.md`.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 22. R3–R7 다섯 번째 상세 콘텐츠 — 카시아 벨란 투기장 대표 무기·공개 생애

Decision: `BS-CONTENT-20260811-05`.

```text
GLADIATOR_01 / CASSIA_BELLAN
ARENA_SIGNATURE_WEAPON_AND_LEGACY
ARENA_MATCH_STATE / EQUIPMENT_CONTRIBUTION_STATE / ITEM_UID_ARENA_LEGACY_STATE
```

- 플레이어는 카시아를 직접 조작하지 않고 공개된 무기 범주·경기 맥락을 읽어 같은 작품 UID 한 점을 선택·인계한다.
- 경기 승패와 작품의 실제 기여를 분리한다. 승리=좋은 작품, 패배=나쁜 작품으로 단순화하지 않는다.
- 새 `ARENA_SCORE / FAME_SCORE / GLADIATOR_SCORE / SIGNATURE_SCORE`를 만들지 않는다.
- 최고 강화·최고 명성·가장 오래된 작품을 보편적 자동 정답으로 만들지 않는다.
- 경기/승리 횟수만으로 `ARTISTRY`를 올리거나 `CHRONICLE_AFFIX`를 자동 부여하지 않는다.
- `data/customers/gladiator_poc.json`, `data/world/gladiator_match_poc.json`의 Kyle/iron_sword 고정 수치와 점수식은 역사 POC fixture이며 Decision05 권위가 아니다.
- 책임 원본: `docs/planning/BLACKSMITH_R3_GLADIATOR_01_CASSIA_BELLAN_ARENA_SIGNATURE_WEAPON_CANON_2026.md`.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.

## 23. R3–R7 여섯 번째 상세 콘텐츠 — 의례 귀족 가보 계승 복원·유산

Decision: `BS-CONTENT-20260811-06`.

```text
NOBLE_01 / CEREMONIAL_NOBLE
HEIRLOOM_SUCCESSION_RESTORATION_AND_LEGACY
CEREMONY_READINESS_STATE / HEIRLOOM_TREATMENT_FIT_STATE / ITEM_UID_DYNASTIC_LEGACY_STATE
```

- 기존 `ceremonial_noble` 대표 fixture를 재사용하며 새 이름·가문 lore를 추가하지 않는다.
- 같은 UID의 실제 상태·과거 수리·소유·계승·Chronicle provenance를 보고 개입 깊이를 판단한다.
- 최대 복원·최고 Artistry는 보편적 자동 정답이 아니다.
- 새 가문 위신·진품성·계승 총점을 만들지 않는다.
- 수리·복원으로 물리 흔적이 바뀌어도 의미 있는 과거 생애 기록은 삭제하지 않는다.
- 복원/의식 반복으로 Artistry 또는 Chronicle Affix를 자동 성장시키지 않는다.
- 직접 의식·귀족 가문·궁정·외교 경영을 추가하지 않는다.
- 책임 원본: `docs/planning/BLACKSMITH_R3_NOBLE_01_CEREMONIAL_NOBLE_HEIRLOOM_SUCCESSION_RESTORATION_CANON_2026.md`.
- 제품 구현: `BLOCKED`.
- Task3 구현: `NOT_APPROVED`.
