# Blacksmith 최종 적대적 검토 및 MVP 마감 보고서

- 검토일: 2026-07-24
- 대상 저장소: `alsdmlals4-eng/Blacksmith`
- 대상 PR: #31, #32, #33
- 현재 제품 Goal: Issue #34
- 판정 단위: 프로젝트 코어·통합 명세·구현계획·운영 정본·PR 마감
- 최종 판정: `REVISE`

## 1. 최종 판정

### `REVISE`

프로젝트 코어와 첫 장비 생애 PoC의 통합 명세·구현계획은 확정 가능한 수준으로 정합화했다. 시작 문서·Game Bible·Roadmap·Gates·Decision Log·Issue·MVP Scope도 현행 코어에 맞춰 갱신했다.

그러나 다음 차단 조건이 남아 있으므로 `구현 완료`, `MVP 완료` 또는 `ACCEPT`를 선언하지 않는다.

- Issue #34 제품 코드·데이터·Scene·신규 테스트가 `IMPLEMENTATION_NOT_STARTED`다.
- Android 실기기, 접근성, 성능, 외부 플레이 행동 증거가 없다.
- PR #31·#32·#33이 stacked Draft 상태이며 미병합이다.
- Branch protection의 Required Check 강제 여부를 확인하지 못했다.
- 사람이 직접 연 PDF 시각 검토는 `NOT_RUN`이다.
- 현재 대화에서 UI상 `Skipped`로 표시된 메시지 원문은 독립적으로 재열람하지 못했다.

코어와 계획 패키지는 승인 상태지만 프로젝트 구현·MVP 마감은 수정과 검증을 계속해야 한다.

## 2. 작업 목표와 완료 기준

작업 목표는 새 기능을 추가하는 것이 아니라 다음을 증거 기반으로 닫는 것이었다.

1. 최신 사용자 결정의 책임 원본 반영.
2. 문서·계획·코드·데이터·Scene·Test 상태 분리.
3. 모순·중복·구형 참조·판정 불가능 표현 제거.
4. 서로 다른 공격 관점의 적대적 검토 5회.
5. finding별 최소 수정과 Red→Green 회귀.
6. 현행 Issue·MVP Scope·PR·검증 상태 정합화.
7. Markdown 책임 원본에서 사람용 PDF와 Manifest 발행.

완료 금지 조건은 사용자 작업 계약을 그대로 적용했다. 필수 `UNVERIFIED`, 미실행 플랫폼 검증, 미구현 MVP, 실패한 Workflow 또는 미푸시 상태가 있으면 완료 선언을 금지했다.

## 3. 검토한 현재 대화 범위

- 현재 대화에서 접근 가능한 사용자·어시스턴트 메시지와 압축된 이전 결정 요약을 검토했다.
- 사용자가 승인한 선택, 최신 override, 거부·제외·보류를 결정 원장으로 재구성했다.
- UI상 `Skipped`로 표시된 개별 메시지 원문은 현재 인터페이스에서 직접 재열람할 수 없었다.
- 해당 구간의 확정 결정은 제공된 대화 요약과 후속 사용자 승인에서 교차 확인했다.
- 따라서 “모든 원문 메시지를 직접 읽었다”고 주장하지 않고 `UNVERIFIED_CONTEXT`를 남긴다.

## 4. 대화 결정 원장

| 결정·요구사항 | 대화 상태 | 최신 사용자 의도 | 반영 책임 원본 | 실제 구현·데이터 경로 | 검증 상태 | 필요한 조치 |
|---|---|---|---|---|---|---|
| 작품 가치·장비 생애 중심 | CONFIRMED | 장비 한 점이 역사와 가치를 얻음 | Core, Game Bible | 미구현 세계 시스템 | 문서 정합 | Issue #34 구현 |
| 한 명의 대장장이 | CONFIRMED | 직원·복수 대장장이 없음 | Core, Game Bible, AGENTS 경계 | 직원 구현 없음 | 정합 | 유지 |
| 무기·방어구·악세서리 3계열 | CONFIRMED | 장기 상위 범주 | Core, Game Bible | 현재 철검만 구현 | 부분 | 흉갑·반지 후속 |
| 첫 PoC 철검·검투사 | CONFIRMED | 장비 한 점의 생애 검증 | Integrated Spec, MVP-003 | 미구현 | SPEC_READY | Task 1~9 |
| 영구 완성도 5등급 | CONFIRMED | 제작 시 1회 결정, 재추첨 없음 | Core, Integrated Spec | 미구현 | 계획 존재 | 명칭·수치는 PoC 임시 |
| 완성도 정확한 명칭·배율 | PROPOSED_ONLY | PoC 기준값으로 사용 | Integrated Spec | 미구현 | 변경 가능 | 플레이 후 조정 |
| 일반 강화 입력당 1회 | CONFIRMED | 누를 때마다 강화 판정 | Core, Game Bible | EnhancementSession 구현 | 기존 회귀 | 유지 |
| +10 특수 강화·수식어 | CONFIRMED | 장비 정체성 이정표 | Core, Game Bible | 구현됨 | 기존 회귀 | PoC에 연결 |
| +11 하락·+30 파괴 | CONFIRMED | 고위험 구간 | Core, Data | 구현됨 | 기존 회귀 | 첫 PoC에서는 제외 |
| 정확한 +100 코어 불변 | SUPERSEDED | 현재 제품 목표, 재검토 가능 | Core, Decision Log | 구현됨 | 문서 수정 | 장기 플레이 뒤 판정 |
| 피로도 일일 작업량 | CONFIRMED | 터치당 스태미나 아님 | Core, Integrated Spec | 미구현 | 계획 존재 | Task 2·6·8 |
| 남은 피로도 50% 이월 | LATEST_OVERRIDE | 별도 상한 없음 | Core, Integrated Spec | 미구현 | 수학 경계 정의 | Task 2 |
| 작업 예약 | REJECTED | 복잡성 때문에 사용하지 않음 | Core, Scope | 없음 | 정합 | 재도입 금지 |
| 강화 세션 묶음 | SUPERSEDED | 클릭당 판정으로 대체 | Core, Plan | 클릭당 판정 구현 | 정합 | 없음 |
| 판매 장비 세계 잔존 | CONFIRMED | 소유·사건·이력 유지 | Core, Integrated Spec | 미구현 | 상태 계약 보강 | Task 5 |
| 결과 최소 하루 지연 | CONFIRMED | 즉시 보상창으로 축소 금지 | Integrated Spec | 미구현 | 상태 전이 정의 | Task 5·6 |
| 같은 검투사 재방문 | CONFIRMED | 이전 장비 결과 언급 | Scope, Spec | 미구현 | E2E 기준 | Task 8·9 |
| 일상적 수리 관리 | REJECTED | 관리 시스템 제외 | Core, Game Bible | 없음 | 정합 | 유지 |
| 중요 장비 선택형 복원 | DEFERRED | 역사 장비만 후속 복원 | Core, Game Bible | 없음 | PoC 제외 | 별도 승인 후 |
| 직접 전투 | REJECTED | 결과형 관전만 가능 | Core | 없음 | 정합 | 재도입 금지 |
| 관전·베팅 | DEFERRED | 판매 루프 뒤 별도 PoC | Core, Decision Log | 없음 | 보류 | 경제·등급 검토 |
| 직원·시장·세력 확대 | DEFERRED/REJECTED | PoC 전 확장 금지 | Roadmap | 일부 골격만 | 정합 | 행동 증거 뒤 |

## 5. 프로젝트 코어와 보호 대상

### 확정 코어

> 한 명의 대장장이가 제한된 하루 작업량으로 장비 한 점을 직접 만들고, 매 강화마다 멈출지 더 도전할지 선택하며, +10 이정표에서 장비의 성질을 벼린 뒤, 그 장비가 다른 이의 손에서 쌓은 역사가 다시 명성과 다음 의뢰로 돌아오는 모바일 제작 게임.

### 보호 대상

- 직접 제작과 즉각적인 터치 피드백.
- 영구 완성도와 장비별 출생 차이.
- 버튼 입력당 강화 판정 한 번.
- +10의 재료·정밀·수식어 선택.
- 판매 뒤에도 남는 장비 이력.
- 결과의 기여·부족 조건 설명.
- 단일 대장장이의 일일 우선순위.
- 낮은 완성도도 다른 역사를 만들 수 있는 접근성.

### 보호 경계

- 직원, 직접 전투, 작업 예약, 일상 수리 관리를 추가하지 않는다.
- 자동 단조가 특수 강화와 위험 판단을 완전히 대체하지 않는다.
- 난수가 결과 밴드를 뒤집지 않는다.
- 문서 승인과 구현 완료를 혼동하지 않는다.

## 6. 확인한 책임 원본과 실제 파일

| 책임 | 확인한 파일 | 판정 |
|---|---|---|
| AI 작업 규칙 | `AGENTS.md` | CURRENT, 일상 수리/선택형 복원 경계 갱신 |
| 시작점 | `START_HERE.md` | UPDATE_REQUIRED → 갱신 |
| 현재 상태 | `ACTIVE_CONTEXT.md` | UPDATE_REQUIRED → 갱신 |
| 문서 지도 | `DOCUMENTATION_MAP.md` | UPDATE_REQUIRED → 갱신 |
| Gate | `DEVELOPMENT_GATES.md` | UPDATE_REQUIRED → 갱신 |
| Roadmap | `ROADMAP.md` | UPDATE_REQUIRED → 갱신 |
| Decision | `DECISION_LOG.md` | UPDATE_REQUIRED → 갱신 |
| 프로젝트 코어 | Core spec | CURRENT_CANONICAL |
| 통합 명세 | Lifecycle integrated spec | CURRENT_CANONICAL, 개선 |
| 구현계획 | Lifecycle implementation plan | CURRENT_CANONICAL, 개선 |
| MVP-003 Scope | `docs/MVP-003_SCOPE.md` | 누락 → 신규 책임 원본 |
| Game Bible | `BLACKSMITH_GAME_BIBLE.md` | UPDATE_REQUIRED → 갱신 |
| 구현 사실 | `scripts/`, `scenes/`, `data/`, `tests/` | 기존 Prototype만 구현 |
| Base 기준 | `BASE_RULES_VERSION.md` | CURRENT |
| Base 감사 | `BASE_ADOPTION_AUDIT.md` | UPDATE_REQUIRED → 갱신 |
| Registry | `DESIGN_DOCUMENT_REGISTRY.json` | UPDATE_REQUIRED |
| PR | #31, #32, #33 | stacked Draft, 미병합 |
| Issue | #34 | 신규 현행 Goal |

## 7. 적대적 검토 1차 결과 - 대화·요구·책임

### Attack

- 최신 사용자 결정을 시작 문서가 실제로 가리키는가.
- 구형 판매 계획과 새 장비 생애 PoC가 동시에 현행처럼 보이는가.
- 현재 Issue·MVP Scope가 존재하는가.

### 검증된 finding

1. `F1-01 MUST_FIX HIGH`: START_HERE·README·Game Bible·Roadmap·Active Context가 과거 방치형/클리커·+100·자동 단조 중심 약속을 현행 코어처럼 제시.
2. `F1-02 MUST_FIX HIGH`: Roadmap은 MVP-003을 다음 작업으로 선언하지만 `docs/MVP-003_SCOPE.md`가 없음.
3. `F1-03 MUST_FIX HIGH`: Issue #29와 #14가 완료된 과거 작업인데 open 상태이며 현행 Goal Issue가 없음.
4. `F1-04 SHOULD_FIX MEDIUM`: Decision Log에 피로도·날짜·장비 생애·+100 재분류 결정이 없음.

### 최소 변경

- 시작 문서·Game Bible·상태 문서 갱신.
- `docs/MVP-003_SCOPE.md` 생성.
- Issue #34 생성, #29·#14 완료 종료.
- DEC-023~025 추가와 stale Base/시뮬레이션 상태 수정.

### Regression recheck

기존 제작·강화·보관·자동 단조 구현 사실은 삭제하지 않고 “현재 구현”으로 보존했다.

## 8. 적대적 검토 2차 결과 - 논리·판정 가능성

### Attack

- 세 결과 밴드가 실제 입력으로 도달 가능한가.
- 확정 코어와 PoC 임시 수치가 구분되는가.
- 구현 사실과 미래 계획이 섞이지 않는가.

### 검증된 finding

1. `F2-01 MUST_FIX HIGH`: 기존 점수는 유효 +5 납품의 최소 점수가 45여서 0~39 DEFEAT가 도달 불가능.
2. `F2-02 SHOULD_FIX MEDIUM`: 완성도 표시명·배율·분포가 사용자 승인된 불변값처럼 보임.
3. `F2-03 MUST_FIX HIGH`: 여러 문서가 코어 확정과 제품 구현 완료를 구분하지 않음.

### 최소 변경

- required 20, attack 10, 밴드 0~34/35~69/70+로 수정.
- 미숙한 +5=30 DEFEAT, 정교한 +5=40 WIN, 명품 +10 preferred=85 DECISIVE_WIN 반례 추가.
- 완성도 명칭·수치를 `PoC 임시 기준값`으로 명시.
- Gate·Active Context에 `SPEC_READY / IMPLEMENTATION_NOT_STARTED` 분리.

### Regression recheck

+5 기본 납품, +10 선택적 욕심, 선호 수식어와 높은 완성도의 가치 차이는 유지됐다.

## 9. 적대적 검토 3차 결과 - 경계·데이터·호환성

### Attack

- legacy `quality_*`, 자동 단조 template, 저장 schema가 안전한가.
- 생애 상태와 보고 상태가 충돌하지 않는가.
- 납품 도중 부분 성공·중복 재시도가 가능한가.

### 검증된 finding

1. `F3-01 MUST_FIX HIGH`: `quality_*`를 완성도 별칭으로 바꾸면 기존 STANDARD/GOOD/PERFECT/AUTO 정밀 의미가 충돌.
2. `F3-02 MUST_FIX HIGH`: Core lifecycle enum과 PoC report enum이 같은 상태 필드처럼 사용됨.
3. `F3-03 MUST_FIX HIGH`: 납품이 보관 제거·대금·소유권·세계 기록 중 일부만 성공할 수 있음.
4. `F3-04 SHOULD_FIX MEDIUM`: 저장 미구현인데도 record version·migration 경계가 없음.
5. `F3-05 SHOULD_FIX MEDIUM`: 결과 데이터 누락 시 소유권과 결과 상태 복구가 불명확.

### 최소 변경

- `record_schema_version: 1`, `precision_result_*`, `craftsmanship_grade_*` 분리.
- legacy 기록 변환과 자동 단조 `AUTO + STANDARD grade` 명시.
- `lifecycle_state`와 `report_state` 이름공간 분리.
- 원자적 납품·transaction ID·전체 rollback·중복 재시도 방지.
- 결과 누락은 `RESULT_ERROR`로 기록하고 결정적 재시도.

### Regression recheck

현재 Prototype 저장·강화 소비자의 `quality_*` 호환 필드를 제거하지 않았다.

## 10. 적대적 검토 4차 결과 - UX·접근성·운영

### Attack

- 피로도 이월이 28/20처럼 오류로 읽히는가.
- 핵심 정보가 색상·빠른 타이밍·반복 탭에만 의존하는가.
- 실패 뒤 복귀 경로가 보이는가.

### 검증된 finding

1. `F4-01 SHOULD_FIX MEDIUM`: 이월 뒤 현재 피로도가 기본 최대치를 넘을 때 단순 current/max 표시는 오류처럼 보임.
2. `F4-02 MUST_FIX HIGH`: 정밀 판정이 빠른 타이밍 입력 하나에 의존하고 대안이 없음.
3. `F4-03 SHOULD_FIX MEDIUM`: 결과·위험이 색상과 효과 위계에 묻힐 수 있음.
4. `F4-04 SHOULD_FIX MEDIUM`: 자원 부족·납품 실패가 복귀 행동을 명확히 안내하지 않음.

### 최소 변경

- HUD에 `현재 작업 가능량`과 `기본 일일량`을 별도 표시.
- 느린 게이지·넓은 판정·GOOD 분포의 정밀 보조 추가. PERFECT 자동 보상 금지.
- 텍스트·아이콘 병기, 자동 닫힘 금지, 모션·진동 감소.
- NO_FATIGUE/NO_GOLD/NO_MATERIAL/납품 부적합 메시지에 부족량·조건·복귀 경로 포함.

### Regression recheck

빠른 직접 입력과 PERFECT 희귀 보상의 의미는 유지됐다. 실제 접근성 PASS는 사람·기기 증거 전까지 부여하지 않았다.

## 11. 적대적 검토 5차 결과 - GitHub·참조·PR

### Attack

- Registry·Map·README·START_HERE·Roadmap·Gates·Issue가 같은 현행 상태를 가리키는가.
- 파생 PDF와 Manifest가 등록 원본과 동기화되는가.
- PR 설명과 실제 diff·검증이 일치하는가.

### 검증된 finding

1. `F5-01 MUST_FIX HIGH`: 동일 책임의 활성 소비자들이 서로 다른 현재 Goal과 코어를 주장.
2. `F5-02 MUST_FIX HIGH`: 프로젝트 코어 정렬을 자동 차단하는 검사가 없음.
3. `F5-03 UNVERIFIED HIGH`: 최종 Markdown은 Registry에 등록했으나 PDF 바이너리의 저장소 publication은 connector 제약으로 완료하지 못함.
4. `F5-07 MUST_FIX HIGH`: 구현계획의 미래 생성 경로가 활성 깨진 참조로 오판되어 정확한 Plan과 reference audit가 충돌함.
5. `F5-04 SHOULD_FIX MEDIUM`: 기존 core review report가 2회 검토·3개 changed files라는 과거 상태를 CURRENT로 표시.
6. `F5-05 UNVERIFIED HIGH`: Branch protection Required Check 강제 상태 확인 불가.
7. `F5-06 UNVERIFIED HIGH`: PR #31·#32·#33 미병합 상태에서 main 정합성 보장 불가.

### 최소 변경

- `tests/check_project_core_alignment.py`와 Data validation step 추가.
- Red run #391로 drift 재현.
- 시작 문서·Scope·Spec·Plan·Game Bible·Decision·Base Audit 갱신.
- 최종 보고서를 Registry에 등록하고 사람용 PDF·Manifest를 로컬 산출물로 생성. 저장소 PDF publication은 미완료로 유지.
- 이전 core review report를 역사 분석본으로 재분류.
- PR #33 제목·본문·검증 증거 갱신.

### Regression recheck

과거 Changelog·MVP-001/002·닫힌 Issue는 역사 기록으로 보존했다. 활성 시작점에서만 최신 책임 원본을 사용하도록 했다.

## 12. Finding 판정 요약

| ID | 판정 | 심각도 | 상태 |
|---|---|---:|---|
| F1-01 | MUST_FIX | HIGH | 수정 |
| F1-02 | MUST_FIX | HIGH | 수정 |
| F1-03 | MUST_FIX | HIGH | 수정 |
| F1-04 | SHOULD_FIX | MEDIUM | 수정 |
| F2-01 | MUST_FIX | HIGH | 수정 |
| F2-02 | SHOULD_FIX | MEDIUM | 수정 |
| F2-03 | MUST_FIX | HIGH | 수정 |
| F3-01 | MUST_FIX | HIGH | 수정 |
| F3-02 | MUST_FIX | HIGH | 수정 |
| F3-03 | MUST_FIX | HIGH | 수정 |
| F3-04 | SHOULD_FIX | MEDIUM | 수정 |
| F3-05 | SHOULD_FIX | MEDIUM | 수정 |
| F4-01 | SHOULD_FIX | MEDIUM | 수정 |
| F4-02 | MUST_FIX | HIGH | 설계·계획 수정, 구현 미착수 |
| F4-03 | SHOULD_FIX | MEDIUM | 설계·계획 수정 |
| F4-04 | SHOULD_FIX | MEDIUM | 설계·계획 수정 |
| F5-01 | MUST_FIX | HIGH | 수정 |
| F5-02 | MUST_FIX | HIGH | Red 생성, Green 최종 CI 필요 |
| F5-03 | UNVERIFIED | HIGH | 로컬 PDF PASS, 저장소 publication 미완료 |
| F5-07 | MUST_FIX | HIGH | 감사 wrapper·단위 테스트 수정 |
| F5-04 | SHOULD_FIX | MEDIUM | Registry 재분류 |
| F5-05 | UNVERIFIED | HIGH | 후속 확인 |
| F5-06 | UNVERIFIED | HIGH | PR 순차 병합 필요 |

## 13. 실제 반영한 최소 변경

- 현행 프로젝트 약속과 구현/설계 분리를 README·START_HERE에 반영.
- Active Context·Documentation Map·Roadmap·Gates를 Issue #34와 연결.
- `docs/MVP-003_SCOPE.md` 생성.
- 통합 명세의 점수·상태·호환성·원자성·접근성 보강.
- 구현계획 Task 1~9에 실제 반례와 파일·검증을 연결.
- Game Bible을 확정 코어 기반으로 동기화.
- Decision Log에 최신 override와 DEC-023~025 기록.
- Base Audit에 최신 25 Skill CI 증거 기록.
- Issue #34 생성, #29·#14 완료 종료.
- 정적 core alignment gate와 Workflow step 추가.
- 최종 보고서 책임 원본 등록과 로컬 PDF·Manifest 발행 계약 추가.

제품 GDScript·Scene·게임 데이터 수치는 변경하지 않았다.

## 14. Red → Green → Refactor 증거

### Red

- commit: `a1a810d...` 검사 생성.
- commit: `09551dc...` Workflow 연결.
- Data validation #391 실패.
- JSON·강화·시뮬레이터 계약은 통과하고 새 core alignment step에서 실패.

### Green

- 시작 문서, 상태 문서, MVP Scope, Spec, Plan, Game Bible, Decision, Base Audit 갱신.
- Issue·Goal을 #34로 전환.
- 세 결과 밴드 도달 반례 추가.
- legacy·상태·납품·접근성 계약 추가.

### Refactor

- 같은 상태를 여러 문서에 장문 복제하지 않고 각 책임 원본으로 라우팅.
- 코어 계약, 통합 설명, MVP 실행 범위, 구현계획과 상태 문서를 분리.
- 구형 review report는 역사 자료로 유지.

### Green 재검증 진행

- Godot validation #338과 #339는 PASS했다.
- Data validation #412는 JSON·강화 실패·시뮬레이터·코어 정렬까지 PASS했고, 운영 감사에서 구현계획의 미래 생성 경로와 아직 발행 전인 PDF·Manifest를 현재 깨진 참조로 분류해 FAIL했다.
- 구현계획 미래 경로만 `PLANNED_PATH_NOT_YET_CREATED` 경고로 재분류하는 wrapper와 단위 테스트를 추가했다. 일반 활성 문서의 깨진 참조는 계속 ERROR다.
- PDF·Manifest 로컬 생성 뒤 저장소 참조를 깨지 않도록 source-only 상태로 유지하고 최종 Data validation을 다시 실행한다.

## 15. GitHub 최신성·구형 참조 감사

| 파일·참조 | 현재 역할 | 최신 정본 | 구형 여부 | 활성 소비자 | 조치 | 결과 |
|---|---|---|---|---|---|---|
| README | 프로젝트 소개 | Core + Active Context | drift | 사용자·새 작업자 | 갱신 | 수정 |
| START_HERE | cold start | Active Context·Map | drift | AI·개발자 | 갱신 | 수정 |
| Game Bible | 통합 설명 | Core | drift | 기획·개발 | 갱신 | 수정 |
| Active Context | 현재 상태 | 자체 | drift | 모든 작업 | 갱신 | 수정 |
| Roadmap | 개발 순서 | Issue #34·Plan | drift | PM·개발 | 갱신 | 수정 |
| Gates | 상태 판정 | 테스트·실행 증거 | drift | QA·PR | 갱신 | 수정 |
| Decision Log | 결정 이력 | 최신 대화 | stale Base/Goal | 모든 discipline | 갱신 | 수정 |
| PROJECT_CORE_REVIEW_REPORT | 과거 2회 검토 | Final report | historical | Registry | STALE로 재분류 | 완료 |
| Issue #29 | 완료 기준선 | Report | historical | 없음 | closed | 완료 |
| Issue #14 | 구형 Base migration | PR #31/#32 | historical | 없음 | closed | 완료 |
| legacy `quality_*` | 호환 필드 | 신규 schema plan | active compatibility | 현재 코드·test | 변환 계약 | 보존 |
| MVP-001/002 Scope | 구현 slice 역사 정본 | 자체 | current historical slice | 테스트·docs | 보존 | 유지 |

`old`, `legacy`, `final`, `latest`, `v2/v3` 이름만으로 파일을 삭제하지 않았다. 고유 정보·활성 참조·대체 경로를 확인한 뒤 역할만 분류했다.

## 16. 책임 원본·Registry·Documentation Map 동기화

현행 질문별 정본:

- 프로젝트 정체성: Core contract.
- 통합 시스템: Game Bible.
- 현재 상태: Active Context.
- 개발 순서: Roadmap·Issue #34·Implementation Plan.
- MVP 경계: MVP-003 Scope.
- 상세 PoC 규칙: Integrated Spec.
- 최종 검토 증거: 이 보고서.
- 발행 상태: Design Document Registry·Publication Manifest.

## 17. 정적·런타임·회귀 검증 결과

| 검증 | 결과 |
|---|---|
| 미해결 Git conflict | Data #412 PASS |
| JSON game data | Data #412 PASS |
| 강화 실패 계약 | Data #412 PASS |
| 밸런스 시뮬레이터 계약 | Data #412 PASS |
| Core alignment gate | Data #412 PASS |
| Base adoption audit | Data #412 FAIL: 계획 미래 경로·발행 전 PDF 오분류; wrapper 수정 후 재실행 필요 |
| Base 전체 회귀 | Data #412에서 audit 이후 skip; 최종 재실행 필요 |
| Godot validation | #338 PASS, #339 PASS |
| 제품 lifecycle runtime | NOT_RUN - 구현 미착수 |
| Android | NOT_RUN |
| 접근성 사람 검증 | NOT_RUN |
| 성능 | NOT_RUN |
| 외부 플레이 | NOT_RUN |

## 18. PDF·Manifest·전 페이지 렌더 결과

- 책임 원본: `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md`.
- 다운로드 PDF: `BLACKSMITH_FINAL_ADVERSARIAL_REVIEW_2026-07-24.pdf`.
- 다운로드 Manifest: `BLACKSMITH_FINAL_ADVERSARIAL_REVIEW_2026-07-24.manifest.json`.
- 생성 방식: DOCX 작성→LibreOffice PDF 변환.
- 자동 렌더: 200 DPI 전 15페이지 검사.
- 자동 시각 판정: `PASS` — 빈 페이지, 한글 깨짐, 표·문단 잘림, 페이지 중복·누락 없음.
- PDF 프리플라이트: 정상 열림, 비암호화, 텍스트 문서.
- `human_visual_review`: `NOT_RUN`.
- 저장소 publication: `NOT_RUN`. GitHub connector에서 PDF 바이너리를 파일로 커밋하는 경로를 확인하지 못해 Registry는 `source_only`, `output_pdf: null`을 유지한다.

## 19. PR 및 Required Check 결과

- PR #31: open Draft, #32 선행.
- PR #32: open Draft, #31 기반.
- PR #33: open Draft, mergeable, #32 기반.
- PR #33 review comments: 없음.
- 병합 순서: #31→#32→#33.
- Required Check 강제 설정: `UNVERIFIED`.
- 최종 Workflow와 PR changed files는 발행 뒤 갱신한다.

## 20. 커밋 목록과 목적

- core alignment Red 검사 추가.
- Data Workflow에 Red gate 연결.
- README·START_HERE·Active Context·Map·Roadmap·Gates 정렬.
- MVP-003 Scope 생성.
- Integrated Spec 논리·호환성·접근성 개선.
- Implementation Plan 반례·원자성·호환성 개선.
- Game Bible·Decision Log·Base Audit 동기화.
- Final report·Registry source 동기화, 로컬 PDF·Manifest, 계획 미래 경로 감사 wrapper.

Connector가 파일별 commit을 생성하므로 최종 PR commit 목록에서 목적을 재확인한다.

## 21. MVP 파일 갱신 결과

`docs/MVP-003_SCOPE.md`를 생성해 다음을 고정했다.

- +5 납품 / +10 추가 도전.
- 철검·검투사 1명.
- 피로도·날짜·세계 기록·재방문.
- 원자 거래와 세 결과 밴드.
- 접근성 가드레일.
- `IMPLEMENTATION_NOT_STARTED`.

MVP-001/002 Scope는 기존 구현 slice의 역사 정본으로 유지했다.

## 22. 원격 푸시 결과

GitHub connector의 create/update 작업은 원격 `agent/propose-project-core-contract` 브랜치에 직접 commit됐다. 최종 head와 PR #33 head 일치 여부는 최종 발행 뒤 다시 확인한다.

## 23. 남은 위험·미검증·후속 작업

### MUST remain open

- Issue #34 Task 1~9 구현.
- 최종 PDF의 저장소 publication과 Registry `always_sync` 전환.
- 전체 Godot 신규·기존 회귀.
- Android 실기기.
- 외부 플레이테스트.
- 접근성·성능 실측.
- PR #31·#32·#33 순차 병합.

### UNVERIFIED

- UI상 skipped 메시지 원문.
- Branch protection Required Check 강제.
- 사람 PDF 시각 검토.
- 로컬 Godot AI MCP client.

### DEFER

- 최종 +100 상한 판정.
- 방어구·악세서리.
- 전쟁·관전·베팅.
- 대표작·선택형 복원.
- 상인·시장·다수 고객.
- 저장·복귀.

## 24. 사람이 직접 확인할 체크리스트

- [ ] PDF를 실제 뷰어에서 전 페이지 확인.
- [ ] PR #31→#32→#33 diff와 병합 순서 확인.
- [ ] Branch protection Required Check 설정 확인.
- [ ] Issue #34 구현 PR의 Red/Green commit 분리 확인.
- [ ] Android 세로 화면·터치·안전 영역 확인.
- [ ] 느린 정밀 게이지·정밀 보조가 실제로 장벽을 줄이는지 확인.
- [ ] +5와 +10 선택 이유를 신규 플레이어가 설명하는지 확인.
- [ ] 결과 기여·부족 조건과 장비 이력을 플레이어가 회상하는지 확인.

## 25. Base 공용 규칙 승격 후보

후보:

1. 구현계획 Markdown의 미래 경로를 활성 깨진 참조와 구분하는 명시적 표기 규칙.
2. 새 코어 확정 뒤 README·START_HERE·Active Context·Map·Roadmap·Gates를 자동 coupled-change로 검사하는 템플릿.
3. 결과 밴드가 실제 fixture로 모두 도달 가능한지 검증하는 설계 데이터 lint.
4. 파생 PDF CURRENT 전환 전에 source·manifest·render를 원자적으로 교체하는 publication gate.

한 프로젝트에서만 관찰됐으므로 즉시 Base에 반영하지 않고 반복 증거 뒤 제안한다.

## 26. 프로젝트 전용으로 유지할 내용

- 단일 대장장이와 장비 생애 코어.
- +10 강화·수식어 구조.
- 피로도 20·50% 이월 PoC 기준.
- 검투사 카일, +5/+10 납품 판단.
- DEFEAT/WIN/DECISIVE_WIN 점수.
- 장비 lifecycle/report 상태 이름공간.
- 모바일 정밀 입력 대안의 구체 수치.
- Blacksmith의 MVP·콘텐츠 확장 순서.
