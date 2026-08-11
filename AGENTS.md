# Blacksmith AI 작업 규칙

Blacksmith는 Android 세로형 Godot 제작 게임 프로젝트다. 사용자가 `기획 완료`를 선언했으며 **이미 승인된 current canon 범위의 제품 구현은 Phase C에서 허용**된다. 신규 제품 범위는 별도 Decision이 필요하고 Task3는 별도 승인 상태를 유지한다.

```text
P0_LOCAL_EXECUTOR_BOOTSTRAP: PASS
P1_AUTHORITY_AND_CURRENT_STATE_READBACK: PASS
PERSISTENT_MUTATION_GATE: OPEN
PHASE_C_NEXT_PACKAGE: P2_FOUNDATION_DATA_AND_STATE_CONTRACTS
CURRENT_EXECUTION_SURFACE: REUSE_LIVE_DEDICATED_CODEX_WHEN_FRESH
BOOTSTRAP_REENTRY_POLICY: ONLY_WHEN_RUNTIME_ENVELOPE_EXPIRED_OR_RECOVERY_REQUIRED
SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE
RESUME_RULE: FETCH_LATEST_MAIN_BEFORE_USE
PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON
TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED
HIGODOT_SOLE_AUTHORING_AUTHORITY
GUT_SOLE_TEST_AUTHORITY
ENTRY_GATE_FAIL_CLOSED
```

## 1. 권위 순서

1. 사용자의 최신 지시와 승인
2. `AGENTS.md`
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `docs/planning/CURRENT_R2_CANON_REGISTRY.json` 및 `CURRENT_R3_R7_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`와 분야별 current canon
6. Active Context·Start Here·Roadmap·Development Gates
7. 실제 코드·data·Scene·tests
8. Google Sheet와 파생 문서
9. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 정본이다. Google Sheet는 같은 Decision ID·경로·Commit·검증 상태를 연결한다. 새 세션은 저장된 SHA를 latest truth로 가정하지 않고 GitHub latest main/open PR과 Sheet current를 다시 읽는다.

## 2. 필수 작업 순서

```text
현재 권위·변경 경계 확인
→ PRE_WORK_RESEARCH_GATE: 벤치마킹·현업 비교·공식/1차 자료 조사
→ ADOPT / ADAPT / REJECT / DIFFERENTIATOR + 정본 충돌 + 적대 pre-check
→ brainstorming·Existing Solution First·적대적 검토
→ RED: 실패 계약 테스트 작성·의도한 실패 관측
→ GREEN: 최소 정본·구현 변경
→ REFACTOR: 중복·구형 current 참조 정리
→ exact-head 전체 검증
→ PR 영향·untouched consumer 재검토
→ 같은 승인 범위는 재승인 없이 병합 / 새 planning conflict·scope expansion만 사용자 Decision
→ postmerge new-main + Google Sheet targeted readback
→ POST_CHANGE_MONITOR_LOOP
```

### PRE_WORK_RESEARCH_GATE — 벤치마킹·현업 비교·조사

Decision `BS-OPS-20260811-02`. 모든 의미 있는 작업은 fresh authority preflight 뒤 실제 설계·정본·구현·테스트·설정·자산 변경 전에 벤치마킹과 최신 현업/공식/1차 자료 조사를 수행한다.

- 게임 기획·콘텐츠·UX·경제·시장 포지셔닝: 직접/인접 유사작과 현업/공식/1차 자료를 비교한다.
- 기술·Godot·Android·GitHub·CI·tooling·performance: current 공식/1차 자료와 프로젝트 버전 호환성을 우선한다.
- 저위험 maintenance·좁은 metadata repair에서 외부 비교가 실질적으로 무관하면 `BENCHMARK_NOT_APPLICABLE` 근거를 남긴다.
- `ADOPT / ADAPT / REJECT / DIFFERENTIATOR / 남은 불확실성`을 기록한다.
- 외부 수치·확률·경제값을 Blacksmith canon으로 자동 승격하지 않는다.

### 작업마다 TDD

모든 기능·규칙·계약·버그 수정은 TDD를 사용한다.

```text
RED → GREEN → REFACTOR
```

- 테스트를 먼저 작성하고 의도한 이유의 RED를 실제 관측한다.
- 최소 변경으로 GREEN을 만든다.
- 테스트를 약화·삭제해 Green을 만들지 않는다.
- 문서·기획·handoff 변경도 가능한 경우 machine-readable contract로 보호한다.
- 현재 HEAD가 바뀌면 이전 HEAD의 성공을 current 증거로 재사용하지 않는다.

## 3. 승인 배치와 조기 체크포인트

- 승인 10건은 **최대 배치 크기**다. R3–R7 batch는 사용자 `기획 완료`로 승인된 9건에서 닫혔고 Decision10을 만들지 않는다.
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT`이면 **조기 체크포인트**를 허용한다.
- 같은 승인 범위는 exact technical validation 뒤 병합 재승인을 요구하지 않는다.
- 신규 gameplay/UX/economy/canon scope, Task3, 기존 결정을 뒤집는 변경만 별도 사용자 Decision으로 격리한다.

## 4. 현재 코어 보호

- 강화 성공·실패와 멈춤·추가 도전이 즉각 반복 재미다.
- 작품은 UID·소유·손상·복원·사건·연대기를 유지한다.
- 일반 강화는 한 입력에 한 결과다.
- 정밀강화는 주재료 맥락 + 강화 방식 + 촉매 한 개다.
- 수식어는 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 슬롯이다.
- 제작 등급은 `보통 / 우수 / 명품 / 걸작 / 전설` 다섯 단계의 출생 완성도다.
- 예술성은 고정 설계 최대치가 없는 non-negative integer 원수치이며 전투력을 기본적으로 올리지 않는다.
- 보조재료 슬롯과 일반 수식어 A·B는 재도입하지 않는다.
- D01–D09의 same-UID/history/provenance 경계를 보존한다.
- replacement는 old UID/history를 유지하고 distinct new UID로 시작한다.
- 새 opaque total score나 highest-stat always-best 규칙을 편의상 추가하지 않는다.
- `P1_BS_CT_06_TAXONOMY_AMBIGUITY_DEFERRED`를 임의 해결하지 않는다.

## 5. 보호 경로와 Phase C 저작 경계

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

위 경로는 더 이상 “일반 제품 구현 전체 BLOCKED”라는 과거 Gate로 묶지 않는다. **현재 Phase C에서 이미 승인된 canon의 bounded package만 변경 가능**하며 신규 제품 범위는 별도 Decision이 필요하다.

- `.tscn`, Resource, `project.godot` 등 Godot persistent serialization surface는 HiGodot production authoring authority를 사용한다.
- 일반 code/data edit은 해당 기존 프로젝트 owner/authority를 따른다.
- GUT test surface는 GUT authority를 따른다.
- Hera는 observational/live-QA only이며 tracked product mutation authority가 없다.
- 동일 파일 dual authority는 금지한다.

## 6. 정본·구형 문서·Continuation

- 한 질문에는 활성 책임 원본 하나만 둔다.
- `[대체됨] / [부분 대체됨] / [보류] / [폐기] / [역사 증거]`를 직접 표시한다.
- 과거 PASS/old PID/session/SHA는 historical evidence일 뿐 current authority가 아니다.
- PR #81은 `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`이다.
- current router를 압축할 때 machine consumer가 필요로 하는 compatibility locator를 inventory하고 history와 live state를 분리한다.
- Handoff 자체 merge SHA를 기록하려고 연쇄 PR을 만들지 않는다. `RESUME_RULE: FETCH_LATEST_MAIN_BEFORE_USE`가 최종 live truth를 복원한다.

## 7. 완료 증거

- review head와 실제 CI validation identity를 구분한다.
- current exact HEAD의 required checks와 producer를 확인한다.
- changed files·보호 경로·same-goal PR·unresolved threads를 확인한다.
- GitHub new-main readback과 Google Sheet same-ID targeted readback을 한다.
- Sheet write는 `SHEET_SYNC_WRITE_POLICY: TARGETED_RANGES_ONLY_PRESERVE_HISTORICAL_EVIDENCE`를 따른다. broad replacement로 historical SHA/status를 덮어쓰지 않는다.
- 미실행 Human QA·Android device·접근성·성능은 `NOT_RUN`이다.

## 8. 플랫폼 출시·에셋 권리

출시·외부 자산·AI·외주·참조 기반 독립 제작 작업은 다음 프로젝트 증거를 읽는다.

- `docs/PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE.md`
- `docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- `docs/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

Android·Google Play 출시에서는 콘텐츠 등급, target audience, Families, 광고 SDK, 데이터·개인정보, ads/IAP, build·store·questionnaire 정합을 함께 검토한다. 원본을 조금 수정하거나 AI로 변환했다는 이유만으로 독립 자산으로 보지 않는다. 필수 권리·약관·플랫폼 답변이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다. **Phase C 구현 Gate가 열린 것과 실제 출시/법률/등급 Gate가 열린 것은 별개**다.

## 9. HiGodot·GUT·Hera 권위와 runtime 진입 Gate

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: `BS-HIGODOT-20260808-01`에서 HiGodot production authoring authority가 활성화됐다. 당시 Task2-scoped activation은 역사 증거이며 현재 저작 범위는 `BS-OPS-20260811-03`의 Phase C existing-approved-canon Gate가 제한한다.
- `GUT_SOLE_TEST_AUTHORITY`: GUT 9.7.1은 `FORMALLY_ADOPTED_ACTIVE` GDScript test authority다.
- `ENTRY_GATE_FAIL_CLOSED`: exact Blacksmith project/session/version/authority identity가 fresh하게 묶이지 않으면 persistent mutation을 시작하지 않는다.
- `HERA_AGENT_AUTHORITY: NONE`: Hera는 enabled non-authoritative이며 별도 승인 없이 tracked mutation을 만들지 않는다.
- 현재 Godot AI vendor는 `BS-TOOLCHAIN-20260811-02`에 따른 exact upstream `3.1.4`; Task2의 3.1.3 runtime은 historical provenance다.

현재 Blacksmith runtime receipt:

```text
Godot 4.7.1: PASS
Godot-AI 3.1.4: PASS
HTTP 8006: PASS
WS 9506: PASS
dedicated CODEX_HOME: PASS
exact Blacksmith project session: 1
editor_state / hierarchy / project settings: PASS
PERSISTENT_MUTATION_GATE: OPEN
```

listener/process 존재만으로 readiness를 추론하지 않는다. fresh exact HiGodot receipt가 필요하다. 동일 exact dedicated session이 계속 live/fresh하면 `CURRENT_EXECUTION_SURFACE: REUSE_LIVE_DEDICATED_CODEX_WHEN_FRESH`; 만료/충돌/recovery 때만 `BOOTSTRAP_REENTRY_POLICY`에 따라 전용 bootstrap으로 돌아간다.

## 10. 현재 프로젝트 총 작업지시문

- 작업지시문 정본: `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` (`v4.5 r2`)
- 프로젝트 바인딩 override Decision: `BS-OPS-20260811-01`
- 선행 조사 Gate: `BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE`
- Phase C/runtime binding: `BS-OPS-20260811-03`
- 현재 구현 권한: `PRODUCT_IMPLEMENTATION: PHASE_C_ENTRY_APPROVED_WITHIN_EXISTING_APPROVED_CANON`
- 새 제품 범위: `USER_DECISION_REQUIRED_BEYOND_EXISTING_APPROVED_CANON`
- Task3: `TASK3_IMPLEMENTATION: NOT_SEPARATELY_APPROVED`
- 이미지 생성: `DEFERRED_BY_USER`
- 다음 package: `P2_FOUNDATION_DATA_AND_STATE_CONTRACTS`

## 11. Post-change monitor

유지 변경 또는 merge 뒤:

```text
retained-change-or-merge
→ attack
→ validate-critique
→ same-goal open/recent PR recheck
→ untouched consumer / derivative / canon recheck
→ OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP
→ minimal fix if needed
→ regression
→ exact-head/new-main validation
→ continuation readback
```

`NO_MATERIAL_FOLLOWUP`이면 루프를 채우기 위한 억지 변경을 만들지 않는다.