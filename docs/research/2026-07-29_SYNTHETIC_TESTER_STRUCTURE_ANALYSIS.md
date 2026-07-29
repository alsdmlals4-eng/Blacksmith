# Blacksmith 합성 테스터 적용 구조 분석

```yaml
analysis_id: BLACKSMITH-SYNTH-STRUCTURE-001
repository: alsdmlals4-eng/Blacksmith
baseline_branch: main
baseline_commit: 96d718dee178d3acafc275e8e093e3bfaf3db84e
work_mode: PLAN
validation_method: SYNTHETIC_TESTER_SIMULATION
evidence_tier: T6_AI_INFERENCE
base_governance_commit: 9c4071c5ecefe28769b512d426442338ceb7acdd
human_validation: NOT_RUN
android_validation: NOT_RUN
implementation_authority: NONE
```

## 1. 분석 목적

`+5 납품 / +10 도전`의 선택 구조를 가상 페르소나로 공격하기 전에 Blacksmith의 현재 Skill Registry, 기획·구현 책임, QA 경로와 사람 검증 패킷을 복원한다. 합성 결과는 장비 생애 PoC의 실제 선택률·경제 밸런스·Android 경험을 증명하지 않는다.

## 2. 콜드 스타트 구조

```text
AGENTS.md
→ [기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md
→ [기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md
→ [기획서]/00_프로젝트_허브/SKILL_REGISTRY.json
→ 장비 생애 PoC·강화 JSON·실행 안내
→ Evidence Pack
→ 사람 검증 Artifact
→ game-design·QA Skill
→ Base GUR·적대적 검토
```

`ACTIVE_CONTEXT.md`는 과거 PR #35 시점의 구현 설명을 포함하므로 실제 현재 상태는 최신 `main`, PR #64·#65와 함께 읽어야 한다. 합성 보고서는 이 stale 상태를 제품 회귀로 해석하지 않고 문서 발견성 위험으로만 기록한다.

## 3. current_skill_registry

### selected_project_skills

| Skill | Mode | 책임 |
|---|---|---|
| `blacksmith-game-design` | `playtest-and-experiment` | 납품·도전 선택의 가설·자극물·오해 분리 |
| `blacksmith-game-design` | `research-evidence-map` | 장비 정체성·위험·경제·서사 근거의 층 분리 |
| `blacksmith-game-design` | `balance-simulation` | 실제 확률 계산이 아니라 optimizer가 볼 기대값 변수 식별 |
| `blacksmith-qa` | `adversarial-review` | 강요·손실 은폐·지배 선택·scripted outcome 편향 공격 |
| `blacksmith-qa` | `evidence-report` | 합성·실제 PoC·Android·사람 증거 상태 분리 |

### selected_base_skills

| Skill | Mode | 책임 |
|---|---|---|
| `governing-game-user-research-coverage` | `plan-evidence` | 가상 페르소나와 실제 표본 분리 |
| `running-adversarial-review-and-refinement` | `attack` | +10 정답화·후견 문구·후회 조작 공격 |
| `running-adversarial-review-and-refinement` | `validate-critique` | 실제 JSON·화면과 비판 근거 대조 |
| `reviewing-and-validating-project-changes` | `evidence-report` | 제품 경로 비침범·미검증 보고 |

## 4. canonical_sources

| 책임 | 경로 |
|---|---|
| 현재 상태 | `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md` + 최신 `main` |
| 문서 지도 | `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md` |
| Skill Registry | `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json` |
| 장비 생애 Scene | `scenes/test/equipment_lifecycle_poc.tscn` |
| 화면 연결 | `scripts/poc/equipment_lifecycle_poc_screen.gd` |
| 강화 위험 | `data/crafting/enhancement_balance.json` |
| 수식어 이정표 | `data/crafting/enhancement_milestones.json` |
| 실행 안내 | `docs/GODOT_PLAYTEST.md` |
| Evidence Pack | `docs/planning/BLACKSMITH_PLUS5_PLUS10_EVIDENCE_PACK_PILOT_2026.md` |
| 사람 검증 패킷 | `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md` |

## 5. protected_paths

```yaml
protected_paths:
  - scenes/test/equipment_lifecycle_poc.tscn
  - scripts/poc/equipment_lifecycle_poc_screen.gd
  - data/crafting/enhancement_balance.json
  - data/crafting/enhancement_milestones.json
  - save schema and economy data
```

## 6. validation_routes

| 증거 | 상태 |
|---|---|
| 계약·문서 CI | 사용 가능 |
| 장비 생애 PoC 실제 실행 | 기존 실행 가능, 이번 작업 `NOT_RUN` |
| Android·48dp·안전 영역 | `NOT_RUN` |
| 장기 경제·실패율 | `NOT_RUN` |
| 실제 사람 선택·회상 | `NOT_RUN` |
| 합성 위험 검토 | `T6_AI_INFERENCE` |

## 7. 분석 대상 구조

- 조건 A: 현재 PoC 화면.
- 조건 B: 정체성 우선 연구 Overlay.
- 실제 PoC 결과: `ACTUAL_POC_RESULT`.
- 표준 실패 카드: `SCRIPTED_OUTCOME`.
- 선택 전 가치 이해, 실제 선택, 결과 후 손실·보존 이해, 단기 회상.

## 8. 페르소나 렌즈

| ID | 공격 목적 |
|---|---|
| `NEW_MOBILE_PLAYER` | +5와 +10의 기본 의미·텍스트 과밀 |
| `ENHANCEMENT_VETERAN` | 강화 장르의 +10 정답 관습 |
| `LOSS_AVERSE` | 실패 카드가 위험을 과대 인식시키는지 |
| `EV_OPTIMIZER` | 장비 서사를 기대값으로 축소하는지 |
| `COLLECTOR` | 이름·의뢰·제작 이력의 실제 선택 영향 가설 |
| `IMPATIENT_TAPPER` | 버튼 강조·첫 문장만 보고 선택하는 위험 |
| `ADVERSARIAL_REPEATER` | 저장·재시도·정보 선취로 위험을 제거하는 가정 |

## 9. 산출물

```yaml
structure_analysis: COMPLETED
simulation_report: docs/research/2026-07-29_PLUS5_PLUS10_SYNTHETIC_TESTER_REPORT.md
human_session_packet_changed: false
product_code_changed: false
balance_data_changed: false
human_validation: NOT_RUN
implementation_authority: NONE
```
