# `+5 납품 / +10 도전` 사람 검증 Artifact 실행 계획 — 합성 위험 교정판

```yaml
session_packet_id: BLACKSMITH-HV-001
project: Blacksmith
baseline_branch: main
baseline_commit: 9ff3eca5fc6e51c9ccdbf1497a92c9b4ae0a5d07
base_governance_commit: 9c4071c5ecefe28769b512d426442338ceb7acdd
base_governance_path: docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md
base_synthetic_governance_path: docs/knowledge/game-development/SYNTHETIC_TESTER_SIMULATION_GOVERNANCE.md
synthetic_review_source: docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_TESTER_REPORT.md
artifact_status: READY_AFTER_SYNTHETIC_REMEDIATION
human_validation: NOT_RUN
android_validation: NOT_RUN
implementation_authority: NONE
```

> 이 문서는 기존 장비 생애 PoC의 선택 이해·장비 정체성·위험 귀인을 관찰하기 위한 연구 계획이다. 강화 확률, 경제, Scene, Script, JSON, 제품 UI를 변경하지 않는다.

## 1. 결정 질문

> 플레이어가 `+5`를 납품 가능한 완성품으로 이해하면서도 `+10`을 자동 상위 정답이 아니라 비용·위험·기회비용을 가진 별도 도전으로 설명할 수 있는가?

실제 선택 Task와 scripted 실패 이해 Task를 서로 다른 측정으로 취급한다.

## 2. Artifact fidelity와 주장 상한

```yaml
artifact_fidelity: EXISTING_POC_OVERLAY
research_tasks:
  task_1: ACTUAL_CHOICE_UNDER_NEUTRAL_INFORMATION
  task_2: INDEPENDENT_SCRIPTED_FAILURE_COMPREHENSION
simulated_components:
  - 조건 B 중립 완성·선택 카드
  - 요청 시 여는 제작 이력 상세 카드
scripted_components:
  - 참가자 실제 장비와 다른 비교 장비의 표준 실패 결과 카드
fixed_outcomes:
  - 비교 장비의 실패 후 손실·보존 설명
claim_ceiling:
  can_claim:
    - 납품 가치·도전 가치·불확실성 이해 가능성
    - +5를 완성품 또는 실패 중간물로 읽는 반복 패턴
    - 장비 이름·의뢰인·선택 이유의 단기 회상
    - 중립 정보 위계가 만드는 오해·과부하·강요 인식
    - 별도 실패 사례에서 손실과 보존 정보를 구분하는지
  cannot_claim:
    - A/B 표현의 통계적 우월성
    - 실제 강화 확률·장기 경제 밸런스
    - Android 터치·48dp·안전 영역·성능 통과
    - 전체 플레이어의 도전률 또는 매출 행동
    - scripted 실패 이해를 실제 선택 후 감정과 동일시하는 것
```

실제 PoC 결과와 표준 scripted 실패 결과를 같은 것으로 취급하지 않는다. Task 2 결과는 Task 1 선택의 정당성·후회·감정 판정에 사용하지 않는다.

## 3. 보호 경계와 실행 경로

| 역할 | 경로 |
|---|---|
| PoC Scene | `scenes/test/equipment_lifecycle_poc.tscn` |
| 화면 연결 | `scripts/poc/equipment_lifecycle_poc_screen.gd` |
| 강화 위험 | `data/crafting/enhancement_balance.json` |
| 수식어 이정표 | `data/crafting/enhancement_milestones.json` |
| 실행 안내 | `docs/GODOT_PLAYTEST.md` |

고정 제품 흐름은 `카일 의뢰 → 철검 제작 → 마감 → 강화 → +5 선택 → 실제 결과`까지 유지한다. 연구 Task 2는 이 흐름과 분리된 별도 비교 사례다.

## 4. Task 1 연구 조건 — 실제 선택

### A — 현재 PoC 화면

현재 구현 화면만 보고 선택한다.

### B — 중립 완성·선택 카드

현재 수치와 버튼을 가리지 않고 아래 핵심 카드만 보여준다. “두 선택은 모두 유효하다”, “권장”, “상위”, “완전한 선택” 같은 가치 판단 문구는 사용하지 않는다.

```text
이 철검은 지금 납품 가능한 완성품입니다.
장비명 / 현재 완성 단계 / 의뢰인 카일

지금 납품
- 현재 계약에 제출한다.
- 현재 보상과 의뢰 결과가 확정된다.
- 추가 강화 기회는 사용하지 않는다.

한 번 더 벼린다
- +10 특수 강화에 도전한다.
- 비용·재료·실패 위험은 현재 화면과 JSON 계약을 따른다.
- 성공 시 수식어 성장 가능성이 열리며, 결과는 보장되지 않는다.
```

### 선택 카드 중립성 계약

```yaml
presentation_neutrality:
  button_size: EQUAL
  typography_weight: EQUAL
  color_emphasis: EQUAL
  default_focus: NONE_OR_COUNTERBALANCED
  detail_access: AVAILABLE_TO_BOTH_CHOICES
  recommendation_badge: FORBIDDEN
```

화면에 없는 확률·보상, `+10` 단독 강조, provenance=무손실 표현을 금지한다.

### 제작 이력 상세 — 2단계 정보

선택 카드와 동시에 모든 이력을 강제 노출하지 않는다. 참가자가 `상세 보기`를 요청하거나 핵심 선택 설명을 마친 뒤 아래 카드를 열 수 있다.

```text
제작 이력 상세
- 장비명과 제작자
- 마감 결과와 수식어
- 의뢰인과 계약 목적
- 현재까지 사용한 재료·선택 이력
- 납품 또는 추가 도전 뒤 보존되는 항목
```

상세 카드 열기 여부와 시점을 행동 기록으로 남긴다. 상세 카드를 열지 않았다고 오답 처리하지 않는다.

## 5. Task 2 — 독립 scripted 실패 이해

Task 1의 참가자 장비와 다른 연구용 비교 장비를 사용한다. 진행자는 “이 사례는 방금 선택한 철검의 결과가 아니며, 실패 정보 표현을 확인하기 위한 별도 사례”라고 고지한다.

```yaml
component_status: SCRIPTED_OUTCOME
card_id: BS-HV-FAILURE-STANDARD-V2
comparison_item_id: BS-HV-COMPARISON-BLADE-01
scenario: "다른 제작자가 +10 도전에 실패한 독립 비교 사례"
shows:
  - 현재 계약 범위의 비용·기회비용·손실 항목
  - 제작자·장비명·의뢰 연결·제작 이력 중 보존 항목
  - 보존 정보가 손실 없음과 같지 않다는 문구
measures:
  - 실패 원인과 손실·보존 정보 이해
  - 실패 뒤 무엇을 다시 확인할지 설명
not_measured:
  - 실제 실패 발생률
  - 장기 경제 손실 적정성
  - 참가자 본인의 실제 +10 선택 감정
  - Task 1 선택의 옳고 그름
```

Task 1 실제 결과는 `ACTUAL_POC_RESULT`, Task 2 비교 카드는 `INDEPENDENT_SCRIPTED_OUTCOME`으로 분리한다.

## 6. 참가자와 진행

```yaml
pilot_purpose: DIRECTIONAL_FINDING_AND_DEFECT_DISCOVERY
minimum_participants: 8
segments:
  new_mobile_players: 4
  crafting_or_enhancement_experienced: 4
conditions:
  A: CURRENT_POC_SCREEN
  B: NEUTRAL_COMPLETION_CHOICE_CARD
assignment:
  each_segment: 2_A_2_B
session_minutes: 25-35
```

각 참가자는 조건 하나만 본다. 8명으로 A/B 효능이나 통계적 우월성을 주장하지 않는다.

### Task 1 진행 순서

1. 의뢰·제작·마감·+5 도달.
2. A 또는 B 공개.
3. `first_attempt`로 두 선택의 결과·위험·불확실성을 기록.
4. 상세 카드 열기 여부와 시점 기록.
5. 실제 선택과 이유 기록.
6. 실제 결과는 `ACTUAL_POC_RESULT`로 기록.
7. Task 1 자기보고와 장비명·의뢰인·선택 이유 회상을 완료한다.

### Task 2 진행 순서

1. Task 1 종료를 명확히 알리고 별도 비교 사례임을 고지한다.
2. `BS-HV-COMPARISON-BLADE-01` 카드를 공개한다.
3. 공개 시점·문구를 `facilitator_intervention`에 기록한다.
4. 손실·보존·다음 확인 사항을 자기 말로 설명하게 한다.
5. Task 2 결과는 `scripted_failure_comprehension`에만 기록한다.

진행자는 어느 선택도 추천하지 않으며 Task 2의 비교 실패를 Task 1 선택 평가로 연결하지 않는다.

## 7. 관찰 기록

### Task 1 필드

- 참가자·경험군·조건.
- `first_completion_view`.
- 납품 가치·도전 가치·불확실성의 최초 설명.
- 실제 선택·이유·실제 PoC 결과.
- 상세 카드 열기 여부·시점·이후 설명 변화.
- 장비명·의뢰인·선택 이유 회상.
- 버튼 크기·색·기본 포커스를 추천으로 읽은 행동.
- 강요감·납품 실패감·후회 예상 자기보고.

### Task 2 필드

- 비교 장비 ID와 scripted 카드 공개 시점.
- `loss_items_understood`, `preserved_items_understood`.
- 보존 정보와 무손실을 혼동했는지.
- 다음 시도 전에 확인할 정보.
- Task 1 실제 장비와 비교 사례를 혼동한 critical incident.

공통으로 심각도 높은 위험 은폐·새 확률 암시·가치 판단 주입 사례를 기록한다.

## 8. 별도 경제 TEST_REQUIRED

사람 Artifact는 경제 지배 전략을 판정하지 않는다. 다음은 별도 분석이 책임진다.

```yaml
economy_test_required:
  source: data/crafting/enhancement_balance.json
  questions:
    - +5 납품과 +10 도전의 기대 보상·비용·기회비용
    - 재시도 가능성이 선택을 사실상 고정하는지
    - 실패 뒤 보존 가치가 경제 손실을 과장 또는 은폐하는지
  status: NOT_RUN
```

## 9. 판정

비율은 `n/N` 참고값으로만 사용한다.

```yaml
PROMISING_DIRECTION:
  required_patterns:
    - "서로 다른 참가자 2명 이상이 납품과 도전의 결과·위험을 가치 판단 문구 없이 자기 말로 설명"
    - "+5를 실패한 중간물로 강제 인식하는 심각 결함이 반복되지 않음"
    - "독립 비교 실패에서 손실과 보존 정보를 구분"
    - "Task 1 실제 장비와 Task 2 비교 장비를 혼동하지 않음"
  claim: "중립 완성 정보 위계를 더 높은 fidelity 제품 UI 후보로 검증할 가치가 있음"
ADAPT:
  condition: "방향은 이해되지만 위험·보존·텍스트 양·버튼 위계에서 동일 오해가 반복됨"
REWORK:
  condition: "조건과 무관하게 +5가 실패로 읽히거나 선택과 실패 이해 Task가 계속 혼합됨"
REJECT:
  condition: "중립 카드가 이해·회상을 돕지 않고 선택 시간·감정 조작만 증가시킴"
STOP:
  condition: "연구 문구와 현재 화면·강화 JSON 불일치, 실제/scripted 결과 혼합, 진행자 선택 추천"
```

이 fidelity에서는 제품 UI `ADOPT`를 선언하지 않는다.

## 10. 현재 상태

```yaml
synthetic_must_fix_applied:
  paternal_copy_removed: true
  choice_and_scripted_failure_separated: true
  information_progressive_disclosure_added: true
  presentation_neutrality_contract_added: true
human_session_executed: false
product_ui_change: NOT_APPROVED
android_touch: NOT_RUN
accessibility: NOT_RUN
performance: NOT_RUN
long_term_economy: NOT_RUN
external_sample: NOT_RUN
human_validation: NOT_RUN
product_code_changed: false
balance_data_changed: false
canon_changed: false
implementation_authority: NONE
next_gate: RUN_REVISED_TWO_TASK_PILOT_AND_SEPARATE_ECONOMY_SENSITIVITY_TEST
```
