# `+5 납품 / +10 도전` Evidence Pack Pilot

```yaml
evidence_pack_id: BLACKSMITH-EVP-001
project: Blacksmith
baseline_branch: main
baseline_commit: 5489e9f10c3f81166f502df5c6c65fb1ddc4faa4
mvp_003_merge_evidence: 639c33611c203581c8dcbc08c85425455b16991a
created_at: 2026-07-29
work_mode: PLAN
status: PILOT_RECOMMENDATION
implementation_authority: NONE
human_validation: NOT_RUN
method_reference: Base dc9603595155989e13fb92edff347df5c725217e
```

> 이 문서는 장비 생애 PoC의 수치·확률·코드를 변경하지 않는다. `+5 납품 또는 +10 추가 도전` 선택을 사람 플레이에서 검증하기 위한 기획 입력이다.

## 1. 현재 코어와 보호 경계

- 장비 한 점을 직접 만들고, 강화 위험과 수식어 선택으로 운명을 정한 뒤, 그 장비의 역사가 명성과 다음 의뢰로 돌아온다.
- `+5 납품 / +10 추가 도전`은 검투사 계약의 핵심 판단이다.
- 일반 강화와 `+10` 특수 강화를 구분한다.
- 광클은 불이익이 아니라 피버 보상으로 연결한다.
- 실패·보정·위험 수치는 `data/crafting/enhancement_balance.json`이 소유한다.
- 수식어 이정표는 `data/crafting/enhancement_milestones.json`이 소유한다.
- 직원·결제·광고·서버·일상 수리 시스템을 이번 판단에 추가하지 않는다.

## 2. 결정 질문

> 플레이어가 직접 완성한 장비에 애착을 느끼면서도 `+10`을 강요받거나 손실 공포에 조종된다고 느끼지 않도록, `+5 납품 / +10 도전` 선택 화면은 무엇을 보여주고 무엇을 보존해야 하는가?

### 성공 조건

- 플레이어가 두 선택의 차이와 불확실성을 자기 말로 설명한다.
- `+5`가 겁쟁이 선택이나 실패가 아니라 완성·납품의 유효한 결말로 느껴진다.
- `+10`은 더 큰 수치만이 아니라 장비 정체성과 이야기를 확장하는 자발적 위험으로 읽힌다.
- 실패 뒤에도 제작 과정과 장비의 역사적 의미가 완전히 지워지지 않는다.
- 같은 장비를 다시 만났을 때 이전 선택과 결과를 기억한다.

### 실패 조건

- 실제 위험을 숨긴 채 감정 문구로만 도전을 유도한다.
- `+5`가 사실상 손해라서 모든 합리적 플레이가 `+10`으로 수렴한다.
- 확인창 반복으로 실수는 줄지만 선택 감정도 사라진다.
- 실패가 제작 노동과 장비 정체성을 무의미하게 만든다.

## 3. Evidence

| ID | 층 | 출처 | 확인된 활용점 | 한계 |
|---|---|---|---|---|
| EVD-BS-01 | T1_PRIMARY_OFFICIAL | Kahneman, Knetsch, Thaler, Journal of Political Economy 1990 | 소유한 대상의 가치를 더 높게 평가하는 endowment effect가 시장 실험에서도 관찰됐다. | 게임 장비·확률 선택에 그대로 일반화할 수 없다. |
| EVD-BS-02 | T1_PRIMARY_OFFICIAL | Norton, Mochon, Ariely, Journal of Consumer Psychology 2012 | 직접 완성한 결과물의 가치 평가가 높아질 수 있으며, 성공적 완성이 경계 조건이다. 실패·미완성에서는 효과가 약해질 수 있다. | 애착을 조작하거나 손실을 정당화하는 근거가 아니다. |
| EVD-BS-03 | T2_PROFESSIONAL_PRACTICE | Nikolaus Davidson, GDC Online 2010, Economic Decision Making in Game Design | 손실 회피·심적 회계 등 플레이어의 경제 판단이 감정적으로 지각될 수 있음을 다룬다. | 과금·MMO 맥락을 Blacksmith에 복제하지 않는다. |
| EVD-BS-04 | T1_PRIMARY_OFFICIAL | Android Accessibility, Touch target size | 모바일 상호작용 대상은 최소 48dp 수준의 신뢰 가능한 터치 영역을 권장한다. | Godot Control 적용 방식과 실제 손 검증은 별도다. |
| EVD-BS-05 | T6_AI_INFERENCE | 본 Pilot 종합 | 장비를 먼저 `완성된 소유물`로 인정한 뒤 확장 위험을 제안해야 애착과 선택의 공정성을 함께 시험할 수 있다. | 사람 플레이 전 가설이다. |

## 4. 대안 비교

### A. `+5`에서 자동 납품

- 장점: 흐름이 빠르고 선택 피로가 없다.
- 위험: 장비의 운명을 정한다는 코어 판단이 사라진다.
- 판정: `AVOID`.

### B. `+5` 완성 선언 후 `납품 / +10 도전` 병렬 선택

- 먼저 현재 장비를 완성품으로 보여준다.
- 장비명·제작자 흔적·완성도·현재 수식어·의뢰 적합도·예상 납품 결과를 표시한다.
- `+10`에는 가능한 보상 범주, 현재 알려진 위험, 실패 보정 또는 보존 항목을 같은 화면에서 비교한다.
- 판정: `ADAPT`.

### C. `+10`을 추천·강조하는 단일 진행 버튼

- 장점: 도전률과 긴장감이 높을 수 있다.
- 위험: 안전 선택을 숨기는 다크 패턴처럼 인식될 수 있다.
- 판정: `AVOID`.

## 5. Pilot 권장안

최종 판정: **`ADAPT` — B안을 검증한다.**

### 선택 화면의 정보 계층

1. **장비 정체성:** 이름, 외형 또는 실루엣, 영구 완성도, 제작 과정의 핵심 흔적.
2. **현재 약속:** 의뢰인, 납품 적합도, `+5`에서 확정되는 관계·명성·기록.
3. **추가 도전:** `+10`에서 열리는 수식어 선택 또는 성장 가능성.
4. **위험 설명:** 숨기지 않은 결과 범주와 현재 보정 상태. 미확정 수치는 정확 확률처럼 꾸미지 않는다.
5. **결정:** `지금 납품`과 `한 번 더 벼린다`를 동등한 크기·가독성으로 제시한다.

### 보존 원칙

- 강화 실패가 발생해도 제작자·제작일·완성도·의뢰 연결 같은 provenance를 임의로 삭제하지 않는다.
- 통계적 손실과 서사적 존재 삭제를 구분한다.
- 파괴 계약이 적용되는 더 높은 단계는 별도 위험 Gate로 다루며 `+5 / +10` Pilot에서 암묵적으로 끌어오지 않는다.
- 결과 뒤 `무엇이 변했고 왜 변했는가`를 한 화면에서 설명한다.

### 모바일 UX

- 주요 선택의 실제 터치 영역을 최소 48dp 수준으로 설계 후보화한다.
- 두 선택을 너무 가깝게 두지 않고, 위험 선택만 색으로 구분하지 않는다.
- 위험 재확인은 1회로 제한해 반복 확인창이 리듬을 깨지 않게 시험한다.
- 모션 감소 상태에서도 열기·망치·불꽃 없이 결과를 이해할 수 있어야 한다.

## 6. 플레이테스트 계약

```yaml
build_or_artifact: existing_equipment_lifecycle_poc_with_scripted_choice_observation
tester_segment:
  - 신규 모바일 플레이어 4명 이상
  - 제작 또는 강화 게임 경험자 4명 이상
tasks:
  - 철검 제작 후 +5 선택 화면 설명
  - 납품 또는 +10 선택과 이유 말하기
  - 결과 후 장비 가치·후회·재도전 의향 설명
primary_metrics:
  - 선택 결과 이해율
  - +5와 +10의 유효한 가치 차이 설명률
  - 장비 이름·의뢰인·결과 회상률
  - 오터치·뒤로가기·확인 지연
guardrails:
  - +5가 열등 선택으로만 인식되는 비율
  - 위험을 실제보다 확정적으로 오해하는 비율
  - 실패 뒤 장비가 무의미해졌다는 응답
success:
  - 두 선택 모두 합리적 이유로 선택되고 위험·보존 항목을 대체로 정확히 설명한다
failure:
  - 대부분이 보상 최적화 때문에 +10만 고르거나 +5를 실패로 해석한다
stop:
  - 표시 정보가 실제 JSON 계약과 다르면 테스트 중단
```

행동, 선택 이유, 결과 회상을 분리해 기록한다. 도전률 자체를 성공 지표로 사용하지 않는다.

## 7. 적대적 검토

| Finding | 공격 | 판정 | 대응 |
|---|---|---|---|
| ADV-BS-01 | 행동경제학을 이용해 손실 공포를 극대화한다. | REJECT | 투명성과 선택 공정성을 위해 사용하며 도전률 극대화를 목표로 하지 않는다. |
| ADV-BS-02 | 직접 만들면 무조건 애착이 생긴다고 가정한다. | MUST_FIX | 성공적 완성·회상·소유감이 실제로 나타나는지 측정한다. |
| ADV-BS-03 | +5가 수치상 열등해 가짜 선택이 된다. | MUST_FIX | 관계·기록·시간·안정 가치까지 비교하고 데이터 수치는 별도 밸런스 검토한다. |
| ADV-BS-04 | 실패 보존이 위험을 무력화한다. | SHOULD_FIX | 수치·기회 비용은 유지하되 provenance와 존재 자체만 분리한다. |
| ADV-BS-05 | 48dp 문서 기재를 Android 검증으로 주장한다. | MUST_FIX | 실제 기기·손 사용성은 `NOT_RUN` 유지. |

## 8. 현재 결정에 미치는 영향

- MVP-003 코드·JSON·확률: `NO_CHANGE`.
- `+5 / +10` 사람 검증 질문: `PILOT_RECOMMENDATION`.
- Android·접근성·성능: `NOT_RUN`.
- Production 확대: `NOT_APPROVED`.
- 구현 변경은 Pilot 결과와 사용자 승인 뒤 별도 PR로 분리한다.

## 9. 원출처

- https://www.journals.uchicago.edu/doi/10.1086/261737
- https://doi.org/10.1016/j.jcps.2011.08.002
- https://www.gdcvault.com/play/1013861/Economic-Decision-Making-in-Game
- https://support.google.com/accessibility/android/answer/7101858

게시일·접근 조건·Android 최신 가이드는 실제 적용 시 재검증한다.

## 10. 실행 보고

```yaml
selected_skills:
  - managing-project-intake-and-work-contract
  - analyzing-and-refining-game-concepts
  - governing-game-user-research-coverage
  - running-adversarial-review-and-refinement
work_modes_used: PLAN -> REVIEW
product_paths_changed: false
runtime_validation: NOT_APPLICABLE
human_validation: NOT_RUN
rollback: remove this planning-input document and its Documentation Map link
```