# `+5 납품 / +10 도전` 사람 검증 Artifact 실행 계획 — Governance 교정판

```yaml
session_packet_id: BLACKSMITH-HV-001
project: Blacksmith
baseline_branch: main
baseline_commit: 1623c982f9d441ef4e1fa8211db0741433195045
base_governance: BASE_PR_56_PENDING_MERGE
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

고정 흐름:

```text
카일 의뢰 수락
→ 철검 제작
→ 마감·완성도 확인
→ 일반 강화
→ +5에서 납품 또는 +10 도전
→ 실제 결과
→ 표준 실패 결과 이해 카드
→ 장비 이력·회상
```

## 4. 연구 조건

### 조건 A — 현재 PoC 화면

참가자는 현재 구현 화면만 보고 선택한다. 진행자는 추가 설명을 하지 않는다.

### 조건 B — 정체성 우선 연구 시트

현재 수치와 버튼을 가리지 않고 다음 정보를 보여준다.

```text
이 철검은 지금 납품 가능한 완성품입니다.

장비: 현재 장비명·완성도·수식어
제작 흔적: 마감 결과와 피버 여부
의뢰인: 검투사 카일

지금 납품
- 현재 계약에 제출한다.
- 경기 결과와 장비 이력이 뒤에 남는다.

한 번 더 벼린다
- +10 특수 강화에 도전한다.
- 비용·보조재료·촉매·위험은 현재 화면과 JSON 계약을 따른다.
- 성공하면 수식어 성장 가능성이 열린다.

두 선택은 모두 유효하다.
```

금지:

- 실제 화면에 없는 확률·보상 약속.
- `추천`, `최고`, `겁쟁이`, `안전한 정답` 같은 가치 판단.
- `+10`만 강한 색·크기·애니메이션으로 강조.
- provenance 보존을 수치 손실 없음으로 설명.

## 5. 표준 scripted 실패 결과 카드

참가자의 실제 선택과 별도로, 모든 참가자에게 선택·기억 질문을 끝낸 뒤 같은 실패 사례를 보여준다.

```yaml
component_status: SCRIPTED_OUTCOME
card_id: BS-HV-FAILURE-STANDARD
scenario: "+10 도전이 실패한 비교 사례"
shows:
  - 실패로 변한 수치·기회 비용은 현재 계약 범위에서만 설명
  - 제작자·장비명·의뢰 연결·제작 이력 중 보존되는 항목
  - 보존 정보가 손실 없음과 같지 않다는 문구
measures:
  - 실패 원인과 보존 정보 이해
  - 실패 뒤 장비 정체성·후회 귀인
not_measured:
  - 실제 실패 발생률
  - 실제 경제 손실의 장기 적정성
  - 참가자가 실제로 +10을 선택했을 때의 감정과 동일성
```

실제 게임 결과는 `ACTUAL_POC_RESULT`, 표준 카드는 `SCRIPTED_OUTCOME`으로 별도 기록한다.

## 6. 참가자와 배정

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

각 참가자는 A 또는 B 하나만 본다. 8명 Pilot으로 A/B 효능·통계적 우월성을 주장하지 않는다.

## 7. 진행자 스크립트

시작 문구:

> 직접 만든 철검을 지금 납품할지 더 강화할지 결정하게 됩니다. 어느 선택이 정답인지 보는 시험이 아닙니다. 화면에서 이해한 차이와 선택 이유를 말해 주세요.

순서:

1. 의뢰 수락·제작·마감·+5 도달.
2. 조건 A 또는 B 공개.
3. **first attempt**로 두 선택의 가치·위험·불확실성 설명 기록.
4. 실제 선택과 이유 기록.
5. 실제 PoC 결과를 진행한 경우 `ACTUAL_POC_RESULT`로 기록.
6. 실제 결과와 무관하게 표준 실패 카드를 별도 공개.
7. 공개 행위를 `facilitator_intervention`에 기록.
8. **post-feedback attempt**로 실패 원인·보존 정보·다시 고려할 요소 기록.
9. 장비 이름·의뢰인·선택 이유를 회상하게 한다.

진행자는 `+10이 더 좋다`, `+5가 안전하다`를 말하지 않는다.

## 8. 관찰 기록

| 필드 | 정의 |
|---|---|
| `participant_id` | 개인정보 없는 코드 |
| `segment` | NEW_MOBILE / EXPERIENCED |
| `condition` | A/B |
| `first_completion_view` | COMPLETE_ITEM / INCOMPLETE_ITEM / UNCLEAR |
| `first_delivery_value` | 납품 가치 설명 원문 |
| `first_challenge_value` | 도전 가치 설명 원문 |
| `first_uncertainty` | 확정·불확실 구분 원문 |
| `actual_choice` | DELIVER_AT_5 / CHALLENGE_TO_10 |
| `actual_choice_reason` | 실제 선택 이유 |
| `actual_poc_result` | 실제 결과 또는 NOT_APPLICABLE |
| `facilitator_intervention` | 표준 카드 공개 시점·문구 |
| `post_failure_understanding` | 실패·보존 정보 설명 |
| `post_failure_item_meaning` | 1~5와 이유 |
| `item_name_recalled` | 0/1 |
| `client_recalled` | 0/1 |
| `choice_reason_recalled` | 0/1 |
| `behavior_observation` | 읽기 누락·오조작·되돌리기·시간 |
| `player_self_report` | 강요감·납품 실패감·후회 예상 |
| `critical_incident` | 실제 정보 오해·감정 문구의 위험 은폐 |

## 9. 판정

먼저 다음을 본다.

1. 연구 시트와 실제 화면·JSON 불일치가 있으면 `STOP`.
2. 심각도 높은 위험 은폐·새 확률 암시·한쪽 선택 강요 사례.
3. 서로 다른 참가자 2명 이상에게 반복된 동일 오해.
4. 경험군·조건별 차이와 반대 사례.
5. 실제 선택 행동, 사후 자기보고, 표준 실패 카드 후 수정의 차이.
6. 비율은 실제 `n/N` 참고값으로만 기록.

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
  condition: "연구 문구와 현재 화면·강화 JSON 불일치 또는 실제/ scripted 결과 혼합"
```

이 fidelity에서는 `ADOPT_IDENTITY_FIRST_HIERARCHY` 또는 제품 UI 채택을 선언하지 않는다.

## 10. 미실행 검증과 현재 상태

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
