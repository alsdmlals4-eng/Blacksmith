# `+5 납품 / +10 도전` 사람 검증 Artifact 실행 계획 — Governance 교정판

```yaml
session_packet_id: BLACKSMITH-HV-001
project: Blacksmith
baseline_branch: main
baseline_commit: 1623c982f9d441ef4e1fa8211db0741433195045
base_governance_commit: dd6ae48225da58088045733e8fdc3de5784bdeff
base_governance_path: docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md
base_template_path: templates/research/HUMAN_VALIDATION_SESSION_PACKET.md
artifact_status: READY_FOR_HUMAN_SESSION_PREPARATION
human_validation: NOT_RUN
android_validation: NOT_RUN
implementation_authority: NONE
```

> 이 문서는 기존 장비 생애 PoC의 선택 이해·장비 정체성·위험 귀인을 관찰하기 위한 연구 계획이다. 강화 확률, 경제, Scene, Script, JSON, 제품 UI를 변경하지 않는다.

## 1. 결정 질문

> 플레이어가 `+5`를 유효한 완성·납품 결말로 이해하면서도 `+10`을 강제된 정답이 아니라 자발적인 성장·서사 위험으로 설명할 수 있는가?

## 2. Artifact fidelity와 주장 상한

```yaml
artifact_fidelity: EXISTING_POC_OVERLAY
simulated_components:
  - 조건 B 정체성 우선 연구 시트
scripted_components:
  - 표준 실패 결과 카드
fixed_outcomes:
  - 비교 가능한 실패 후 장비 이력·손실 설명
claim_ceiling:
  can_claim:
    - 납품 가치·도전 가치·불확실성 이해 가능성
    - +5를 완성품 또는 실패 중간물로 읽는 반복 패턴
    - 장비 이름·의뢰인·선택 이유의 단기 회상
    - 정체성 우선 정보가 만드는 오해·과부하·강요 인식
  cannot_claim:
    - A/B 표현의 통계적 우월성
    - 실제 강화 확률·장기 경제 밸런스
    - Android 터치·48dp·안전 영역·성능 통과
    - 전체 플레이어의 도전률 또는 매출 행동
```

실제 PoC 결과와 표준 scripted 실패 결과를 같은 것으로 취급하지 않는다.

## 3. 보호 경계와 실행 경로

| 역할 | 경로 |
|---|---|
| PoC Scene | `scenes/test/equipment_lifecycle_poc.tscn` |
| 화면 연결 | `scripts/poc/equipment_lifecycle_poc_screen.gd` |
| 강화 위험 | `data/crafting/enhancement_balance.json` |
| 수식어 이정표 | `data/crafting/enhancement_milestones.json` |
| 실행 안내 | `docs/GODOT_PLAYTEST.md` |

고정 흐름은 `카일 의뢰 → 철검 제작 → 마감 → 강화 → +5 선택 → 실제 결과 → 표준 실패 결과 이해 → 장비 이력·회상`이다.

## 4. 연구 조건

### A — 현재 PoC 화면

현재 구현 화면만 보고 선택한다.

### B — 정체성 우선 연구 시트

현재 수치와 버튼을 가리지 않고 다음을 보여준다.

```text
이 철검은 지금 납품 가능한 완성품입니다.
장비명·완성도·수식어 / 마감 결과 / 의뢰인 카일

지금 납품
- 현재 계약에 제출한다.
- 경기 결과와 장비 이력이 남는다.

한 번 더 벼린다
- +10 특수 강화에 도전한다.
- 비용·재료·위험은 현재 화면과 JSON 계약을 따른다.
- 성공하면 수식어 성장 가능성이 열린다.

두 선택은 모두 유효하다.
```

화면에 없는 확률·보상, 가치 판단 문구, `+10` 단독 강조, provenance=무손실 표현을 금지한다.

## 5. 표준 scripted 실패 결과

```yaml
component_status: SCRIPTED_OUTCOME
card_id: BS-HV-FAILURE-STANDARD
scenario: "+10 도전이 실패한 비교 사례"
shows:
  - 현재 계약 범위의 수치·기회 비용
  - 제작자·장비명·의뢰 연결·제작 이력 중 보존 항목
  - 보존 정보가 손실 없음과 같지 않다는 문구
measures:
  - 실패 원인과 보존 정보 이해
  - 실패 뒤 장비 정체성·후회 귀인
not_measured:
  - 실제 실패 발생률
  - 장기 경제 손실 적정성
  - 실제 +10 선택 감정과의 동일성
```

실제 결과는 `ACTUAL_POC_RESULT`, 표준 카드는 `SCRIPTED_OUTCOME`으로 분리한다.

## 6. 참가자와 진행

```yaml
pilot_purpose: DIRECTIONAL_FINDING_AND_DEFECT_DISCOVERY
minimum_participants: 8
segments:
  new_mobile_players: 4
  crafting_or_enhancement_experienced: 4
conditions:
  A: CURRENT_POC_SCREEN
  B: IDENTITY_FIRST_OVERLAY
assignment:
  each_segment: 2_A_2_B
session_minutes: 20-30
```

각 참가자는 조건 하나만 본다. 8명으로 A/B 효능이나 통계적 우월성을 주장하지 않는다.

진행 순서:

1. 의뢰·제작·마감·+5 도달.
2. A 또는 B 공개.
3. `first_attempt`로 두 선택의 가치·위험·불확실성 기록.
4. 실제 선택과 이유 기록.
5. 실제 결과는 `ACTUAL_POC_RESULT`로 기록.
6. 표준 실패 카드를 별도 공개하고 `facilitator_intervention`에 기록.
7. `post_feedback_attempt`로 실패·보존 정보·재선택 고려사항 기록.
8. 장비 이름·의뢰인·선택 이유 회상.

진행자는 어느 선택도 추천하지 않는다.

## 7. 관찰 기록

- 참가자·경험군·조건.
- `first_completion_view`.
- 납품 가치·도전 가치·불확실성의 최초 설명.
- 실제 선택·이유·실제 PoC 결과.
- 표준 카드 공개 시점·문구.
- 실패 뒤 손실·보존 설명과 장비 의미.
- 장비명·의뢰인·선택 이유 회상.
- 읽기 누락·오조작·시간 등 행동 관찰.
- 강요감·납품 실패감·후회 예상 자기보고.
- 심각도 높은 위험 은폐·새 확률 암시 사례.

## 8. 판정

비율은 `n/N` 참고값으로만 사용한다.

```yaml
PROMISING_DIRECTION:
  required_patterns:
    - "서로 다른 참가자 2명 이상이 납품과 도전의 가치를 모두 자기 말로 설명"
    - "+5를 실패한 중간물로 강제 인식하는 심각 결함이 반복되지 않음"
    - "표준 실패 뒤 손실과 보존 정보를 구분"
  claim: "정체성 우선 정보 위계를 더 높은 fidelity 제품 UI 후보로 검증할 가치가 있음"
ADAPT:
  condition: "방향은 이해되지만 위험·보존·텍스트 양에서 동일 오해가 반복됨"
REWORK:
  condition: "조건과 무관하게 +5가 실패로 읽히거나 수치 최적화 외 이유가 형성되지 않음"
REJECT:
  condition: "정체성 시트가 이해·회상을 돕지 않고 선택 시간·감정 조작만 증가시킴"
STOP:
  condition: "연구 문구와 현재 화면·강화 JSON 불일치 또는 실제/scripted 결과 혼합"
```

이 fidelity에서는 제품 UI `ADOPT`를 선언하지 않는다.

## 9. 현재 상태

```yaml
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
next_gate: RUN_DIRECTIONAL_PILOT_AND_WRITE_ACTUAL_VS_SCRIPTED_SEPARATED_REPORT
```
