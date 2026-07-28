# `+5 납품 / +10 도전` 사람 검증 Artifact 실행 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans only after a separate product-build approval. This document authorizes research preparation and human observation only.

**Goal:** 기존 장비 생애 PoC에서 `+5`를 완성·납품의 유효한 결말로 느끼면서도 `+10`을 자발적인 서사·성장 위험으로 이해하는지 사람 증거로 판정한다.

**Architecture:** `equipment_lifecycle_poc.tscn`과 현재 강화 JSON을 그대로 사용한다. 참가자는 기존 화면 또는 같은 실제 정보를 정체성 우선으로 재배열한 연구용 선택 시트를 한 번만 본다. 연구용 시트는 화면 위에 겹쳐 보여주는 관찰 보조물이며 제품 UI·확률·경제를 변경하지 않는다.

**Tech Stack:** Godot 4.7.1, `scenes/test/equipment_lifecycle_poc.tscn`, `scripts/poc/equipment_lifecycle_poc_screen.gd`, 현재 강화 JSON, Markdown 선택 시트, 수기 또는 스프레드시트 관찰 기록.

## Global Constraints

- 기준 `main`: `1e5df0c77e2b2e858b1c63f007c62d43ce7887cb`.
- 상위 Evidence Pack: `docs/planning/BLACKSMITH_PLUS5_PLUS10_EVIDENCE_PACK_PILOT_2026.md`.
- 실행 안내: `docs/GODOT_PLAYTEST.md`.
- 강화 확률·실패 정책은 `data/crafting/enhancement_balance.json`만 소유한다.
- 수식어 이정표는 `data/crafting/enhancement_milestones.json`만 소유한다.
- 기존 장비 생애 PoC 코드·Scene·JSON을 이번 문서로 변경하지 않는다.
- `+5`와 `+10`의 실제 결과·비용·위험은 실행 중 현재 화면과 JSON을 기준으로 읽는다.
- 도전률을 성공 지표로 사용하지 않는다.
- 실제 Android·접근성·성능 검증 전 해당 상태를 `NOT_RUN`으로 유지한다.

---

## 1. 검증 대상과 현재 실행 경로

| 역할 | 현재 경로 |
|---|---|
| 장비 생애 PoC Scene | `scenes/test/equipment_lifecycle_poc.tscn` |
| PoC 화면 연결 | `scripts/poc/equipment_lifecycle_poc_screen.gd` |
| 장비 생애 통합 테스트 | `tests/integration/test_equipment_lifecycle_poc.gd` |
| Controller 테스트 | `tests/integration/test_equipment_lifecycle_controller.gd` |
| 강화 위험 | `data/crafting/enhancement_balance.json` |
| 수식어 성장 | `data/crafting/enhancement_milestones.json` |
| 현재 수동 실행 절차 | `docs/GODOT_PLAYTEST.md` |

고정 플레이 흐름:

```text
검투사 카일 의뢰 수락
→ 철검 제작
→ 마감 정타·영구 완성도 확인
→ 일반 강화
→ +5에서 납품 또는 +10 추가 도전
→ 하루 마치기
→ 지연 경기 결과
→ 장비 이력과 카일 재방문
```

## 2. 최소 Artifact 구성

### 조건 A — 현재 PoC 화면

참가자는 `+5` 도달 시 현재 구현 화면만 보고 선택한다. 진행자는 설명을 추가하지 않는다.

### 조건 B — 정체성 우선 연구 시트

현재 구현 화면 위에 다음 한 장을 보여준다. 화면의 실제 수치와 버튼은 가리지 않는다.

```text
[완성 선언]
이 철검은 지금 납품 가능한 완성품입니다.

장비: 현재 화면의 장비명·외형·완성도·수식어
제작 흔적: 마감 결과와 피버 여부
의뢰인: 검투사 카일

[지금 납품]
- 현재 계약에 제출한다.
- 경기 결과는 최소 하루 뒤 확인한다.
- 소유자·결과·장비 이력이 남는다.

[한 번 더 벼린다]
- +10 특수 강화에 도전한다.
- 현재 화면에 표시된 비용·보조재료·촉매·위험을 그대로 적용한다.
- 성공하면 현재 수식어 이정표 계약에 따른 성장 가능성이 열린다.
- 실패 정책은 현재 화면과 enhancement_balance.json 설명을 따른다.

두 선택은 모두 유효하다. 선택하지 않은 길은 자동으로 열등 처리되지 않는다.
```

연구 시트는 다음을 금지한다.

- 실제 화면에 없는 확률이나 보상을 추가로 약속하기.
- `추천`, `최고`, `안전`, `겁쟁이` 같은 가치 판단 문구.
- `+10` 쪽만 큰 글자·강한 색·애니메이션으로 강조하기.
- provenance 보존을 수치 손실 없음으로 오해하게 쓰기.

## 3. 실험 설계

```yaml
minimum_participants: 8
segments:
  new_mobile_players: 4
  crafting_or_enhancement_experienced: 4
conditions:
  A: current_poc_screen
  B: identity_first_research_sheet
assignment:
  new_mobile_players: 2_A_2_B
  experienced_players: 2_A_2_B
session_minutes: 20-30
```

각 참가자는 조건 하나만 본다. 같은 참가자가 A와 B를 연속으로 비교하면 연구 목적을 눈치채므로 금지한다.

## 4. 진행자 스크립트

### 시작 안내

> "철검을 직접 만든 뒤 의뢰에 납품할지 더 강화할지 결정하게 됩니다. 어느 선택이 정답인지를 보는 시험이 아닙니다. 화면에서 이해한 차이와 선택 이유를 말해 주세요. 진행자는 강화 결과를 예측하거나 추천하지 않습니다."

### 진행 순서

1. 참가자가 직접 검투사 카일 의뢰를 수락한다.
2. 철검 제작과 마감 정타를 진행한다.
3. 장비 이름·완성도·마감·피버 여부를 읽게 하되 기억시키기 위한 퀴즈는 하지 않는다.
4. 일반 강화를 통해 `+5`에 도달한다.
5. 조건 A는 현재 화면만, 조건 B는 연구 시트를 추가로 보여준다.
6. 참가자에게 두 선택의 차이와 불확실성을 자기 말로 설명하게 한다.
7. `지금 납품` 또는 `+10 도전`을 선택하고 이유를 말하게 한다.
8. 선택 후 확신·후회 예상·장비 가치 인식을 기록한다.
9. 납품을 선택한 경우 하루를 마치고 지연 경기 결과·재방문까지 진행한다.
10. `+10`을 선택한 경우 현재 PoC 계약대로 결과를 진행하고 결과 설명을 읽는다.
11. 마지막에 장비 이름, 의뢰인, 선택 이유, 남은 장비 의미를 회상하게 한다.

진행자는 `+10이 더 좋다`, `+5가 안전하다`와 같은 해석을 제공하지 않는다.

## 5. 참가자 질문

### 선택 전

1. 지금 이 장비는 완성된 물건인가, 아직 실패한 중간 결과인가?
2. 지금 납품하면 무엇을 얻고 무엇을 포기하는가?
3. 한 번 더 벼리면 무엇이 달라질 수 있고 무엇이 위험한가?
4. 화면에서 확정된 정보와 아직 불확실한 정보를 구분해 달라.

### 선택 직후

1. 선택의 가장 큰 이유는 무엇인가?
2. 반대 선택도 합리적일 수 있는 상황은 무엇인가?
3. 실수로 눌렀다고 느끼는가, 의도적으로 선택했다고 느끼는가?

### 결과 후

1. 장비 이름과 의뢰인은 누구였는가?
2. 결과 뒤에도 이 장비가 자신의 제작물로 느껴지는가?
3. 무엇이 변했고 무엇이 남았는가?
4. 같은 상황에서 다시 선택한다면 무엇을 고려하겠는가?

## 6. 관찰 기록지

| 필드 | 기록 규칙 |
|---|---|
| `participant_id` | 개인 식별정보 없는 코드 |
| `segment` | `NEW_MOBILE` 또는 `EXPERIENCED` |
| `condition` | A 또는 B |
| `completion_view` | `COMPLETE_ITEM / INCOMPLETE_ITEM / UNCLEAR` |
| `choice` | `DELIVER_AT_5 / CHALLENGE_TO_10` |
| `choice_reason_primary` | `RELATION / HISTORY / SAFETY / GROWTH / NUMERIC_OPTIMIZATION / CURIOSITY / UI_EMPHASIS / OTHER` |
| `explains_delivery_value` | 0/1 |
| `explains_challenge_value` | 0/1 |
| `explains_uncertainty` | 0/1 |
| `reads_live_risk_info` | 0/1 |
| `decision_seconds` | 선택 화면 공개부터 확정까지 |
| `confirmation_delay_seconds` | 위험 재확인 표시부터 확정까지 |
| `misclick_or_backtrack` | 횟수 |
| `item_name_recalled` | 0/1 |
| `client_recalled` | 0/1 |
| `choice_reason_recalled` | 0/1 |
| `item_still_meaningful_after_failure` | 1~5, 실패가 발생한 경우만 |
| `delivery_seen_as_failure` | 1~5 |
| `challenge_seen_as_forced` | 1~5 |
| `observer_note` | 실제 행동과 발화 |

## 7. 핵심 계산

- 선택 이해율: 납품 가치·도전 가치·불확실성 중 2개 이상을 정확히 설명한 참가자 비율.
- 유효한 양자 선택 설명률: 반대 선택도 합리적일 수 있는 이유를 말한 참가자 비율.
- 정체성 회상률: 장비 이름·의뢰인·선택 이유 중 2개 이상 회상한 참가자 비율.
- 강요 인식률: `challenge_seen_as_forced >= 4`인 참가자 비율.
- 납품 실패화 비율: `delivery_seen_as_failure >= 4`인 참가자 비율.
- 오조작률: 선택 확정 전 오터치·뒤로가기·선택 취소가 발생한 참가자 비율.

## 8. Pilot 판정 기준

```yaml
ADOPT_IDENTITY_FIRST_HIERARCHY:
  choice_understanding_rate: ">= 0.75"
  valid_dual_choice_explanation_rate: ">= 0.625"
  identity_recall_rate: ">= 0.75"
  forced_challenge_rate: "<= 0.25"
  delivery_as_failure_rate: "<= 0.25"
ADAPT:
  condition: "선택 차이는 이해하지만 한쪽 가치·위험·보존 문구가 반복 오해됨"
REWORK_BALANCE_OR_PROMISE:
  condition: "조건과 무관하게 합리적 이유가 수치 최적화 하나로만 수렴하거나 +5가 실패로 해석됨"
REJECT_PRESENTATION:
  condition: "정체성 우선 시트가 선택을 더 느리게 만들면서 이해·회상을 개선하지 못함"
STOP:
  condition: "연구 시트 문구와 현재 화면·enhancement_balance.json·enhancement_milestones.json이 불일치함"
```

8명 Pilot은 방향성 검증이며 통계적 유의성을 주장하지 않는다. A와 B의 단순 선택 비율 차이만으로 우열을 결정하지 않는다.

## 9. 실제 기기 검증 경계

이 Pilot에서 확인 가능한 것:

- 정보 위계 이해.
- `+5` 완성감.
- `+10` 자발적 위험 인식.
- 장비·의뢰 회상.
- 현재 PC 실행 환경에서의 오조작.

이 Pilot으로 확인하지 않는 것:

- Android 48dp 실제 손 사용성.
- 노치·안전 영역.
- 접근성 서비스 읽기 순서.
- 프레임·발열·AAB.
- 장기 경제·강화 확률 밸런스.

따라서 결과가 좋아도 Android·접근성·성능 상태는 `NOT_RUN`이다.

## 10. 증거 저장 계약

사람 테스트를 실행한 뒤에만 다음 보고서를 별도 PR로 만든다.

```text
docs/validation/BLACKSMITH_PLUS5_PLUS10_HUMAN_VALIDATION_REPORT_2026.md
```

보고서 필수 항목:

- 실행 SHA·Godot 버전·사용 조건 A/B.
- 참가자 구분과 수.
- 현재 강화 JSON SHA.
- 원자료 표와 계산 결과.
- 예상과 달랐던 선택 이유.
- 선택 화면 문제인지 경제·보상 문제인지 분리한 Finding.
- `ADOPT / ADAPT / REWORK / REJECT` 판정.
- 제품 UI 변경 권한은 별도 사용자 승인 대기라고 명시.

## 11. 실행 작업

### Task 1: 기준선 검증

- [ ] `scenes/test/equipment_lifecycle_poc.tscn`을 Godot 4.7.1에서 실행한다.
- [ ] `docs/GODOT_PLAYTEST.md`의 제작→+5→납품/도전→결과 흐름을 한 번 완주한다.
- [ ] 현재 화면의 비용·위험·수식어 설명이 JSON과 일치하는지 확인한다.
- [ ] 불일치가 있으면 연구 세션을 시작하지 않는다.

### Task 2: 조건 패킷 준비

- [ ] 조건 A 화면 캡처 또는 실시간 화면을 준비한다.
- [ ] 조건 B 연구 시트를 동일한 화면 크기에서 읽을 수 있게 준비한다.
- [ ] B 시트가 실제 수치를 덮거나 새로운 확률을 암시하지 않는지 검토한다.
- [ ] 위험 선택만 색상으로 강조하지 않는다.

### Task 3: 사람 세션 실행

- [ ] 두 경험 집단을 A/B에 각각 2명씩 배정한다.
- [ ] 진행자는 선택을 추천하지 않는다.
- [ ] 선택 행동과 사후 설명을 별도 열에 기록한다.
- [ ] 실패 결과가 발생하면 장비 의미·보존 인식을 추가 기록한다.

### Task 4: 판정

- [ ] 도전률을 성공 지표에서 제외한다.
- [ ] UI 문제와 경제·보상 구조 문제를 분리한다.
- [ ] 사람 검증 전 `PRODUCTION_APPROVED`를 사용하지 않는다.
- [ ] 보고서 병합 전 제품 코드 변경 PR을 만들지 않는다.

## 12. 적대적 셀프 리뷰

- 정체성 문구가 장비 손실 위험을 감정적으로 덮을 수 있음 → 실제 위험 정보와 같은 화면에서 읽게 함.
- provenance 보존이 손실 없음으로 오인될 수 있음 → 수치·기회 비용과 장비 기록을 분리해 질문함.
- `+5` 납품 가치가 경제상 지나치게 낮을 수 있음 → UI 실패가 아니라 밸런스 Finding으로 분리함.
- 조건 B가 더 많은 텍스트 때문에 유리할 수 있음 → 의사결정 시간과 정보 미확인을 함께 기록함.
- 48dp 문구를 Android 검증으로 과장할 수 있음 → 실제 기기 항목을 명시적으로 제외함.

## 13. 현재 상태

```yaml
artifact_status: READY_FOR_HUMAN_SESSION_PREPARATION
product_code_changed: false
balance_data_changed: false
canon_changed: false
human_validation: NOT_RUN
android_validation: NOT_RUN
implementation_authority: NONE
next_gate: RUN_EIGHT_PARTICIPANT_COUNTERBALANCED_PILOT
rollback: remove this document only
```
