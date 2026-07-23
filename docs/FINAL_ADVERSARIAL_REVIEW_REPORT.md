# Blacksmith 최종 적대적 검토 및 MVP 마감 보고서

- 검토일: 2026-07-24
- 대상: PR #31·#32·#33, 프로젝트 코어, 통합 명세, 구현계획, 운영 정본
- 현행 Goal: Issue #34
- 최종 판정: `REVISE`

## 1. 최종 판정

### `REVISE`

프로젝트 코어와 장비 한 점의 생애 PoC 명세·구현계획은 정합화됐다. 시작 문서·Game Bible·Roadmap·Gates·Decision Log·Issue·MVP Scope도 현행 코어로 갱신했다.

다만 Issue #34 제품 구현이 `IMPLEMENTATION_NOT_STARTED`이고 Android·접근성·성능·외부 플레이가 미실행이며 PR #31·#32·#33도 미병합이다. 따라서 `구현 완료`, `MVP 완료`, `ACCEPT`를 선언하지 않는다.

## 2. 작업 목표와 완료 기준

- 최신 사용자 결정의 책임 원본 반영
- 문서·계획·실제 구현 상태 분리
- 모순·중복·구형 참조·판정 불가능 표현 제거
- 서로 다른 공격 관점의 적대적 검토 5회
- Red→Green→Refactor와 회귀 증거
- Issue·MVP Scope·PR·PDF·Manifest 정합화

필수 `UNVERIFIED`, 미구현 MVP, 실패 Workflow, 미푸시 상태가 있으면 완료 선언을 금지한다.

## 3. 검토한 현재 대화 범위

현재 대화에서 접근 가능한 메시지와 이전 결정 요약을 검토했다. UI상 `Skipped`로 표시된 개별 메시지 원문은 독립적으로 재열람하지 못했으므로 전체 원문을 직접 읽었다고 주장하지 않는다. 후속 사용자 승인과 결정 요약으로 핵심 결정은 교차 확인했지만 해당 원문 범위는 `UNVERIFIED_CONTEXT`다.

## 4. 대화 결정 원장

| 결정·요구사항 | 상태 | 최신 의도 | 책임 원본 | 구현 | 검증·조치 |
|---|---|---|---|---|---|
| 장비 한 점의 역사·가치 | CONFIRMED | 작품의 출생·성장·소유·사건 기록 | Core, Game Bible | 세계 시스템 미구현 | Issue #34 |
| 한 명의 대장장이 | CONFIRMED | 직원 없음 | Core | 직원 구현 없음 | 유지 |
| 무기·방어구·악세서리 | CONFIRMED | 장기 3계열 | Core | 철검만 구현 | 후속 전이 검증 |
| 영구 완성도 5등급 | CONFIRMED | 제작 시 1회, 재추첨 없음 | Core, Spec | 미구현 | Task 3 |
| 완성도 명칭·배율 | PROPOSED_ONLY | PoC 임시값 | Spec | 미구현 | 플레이 후 변경 가능 |
| 입력당 일반 강화 1회 | CONFIRMED | 누를 때마다 판정 | Core | 구현됨 | 회귀 유지 |
| +10 특수 강화 | CONFIRMED | 수식어·정체성 이정표 | Core | 구현됨 | PoC 연결 |
| +11 하락·+30 파괴 | CONFIRMED | 고위험 구간 | Data·Code | 구현됨 | 첫 PoC 제외 |
| 정확한 +100 불변 | SUPERSEDED | 현재 제품 목표 | Core, Decision | 구현됨 | 장기 증거 뒤 재판정 |
| 피로도·수동 날짜 | CONFIRMED | 하루 작업량, 성공률 영향 없음 | Core, Spec | 미구현 | Task 2·6·8 |
| 잔여 피로도 50% | LATEST_OVERRIDE | 상한 없음 | Core, Spec | 미구현 | 경계 테스트 |
| 작업 예약 | REJECTED | 사용하지 않음 | Core, Scope | 없음 | 재도입 금지 |
| 묶음 강화 세션 | SUPERSEDED | 클릭당 강화로 대체 | Core | 클릭당 구현 | 완료 |
| 판매 장비 세계 잔존 | CONFIRMED | 소유·사건·이력 유지 | Core, Spec | 미구현 | Task 5 |
| 결과 최소 하루 지연 | CONFIRMED | 즉시 보상창 금지 | Spec | 미구현 | Task 5·6 |
| 같은 고객 재방문 | CONFIRMED | 이전 결과 언급 | Scope, Spec | 미구현 | E2E |
| 일상 수리 관리 | REJECTED | 제외 | Core, Game Bible | 없음 | 유지 |
| 중요 장비 선택형 복원 | DEFERRED | 후속 역사 이벤트 | Core | 없음 | PoC 제외 |
| 직접 전투 | REJECTED | 결과형만 | Core | 없음 | 유지 |
| 관전·베팅 | DEFERRED | 판매 검증 후 별도 PoC | Decision | 없음 | 경제·등급 검토 |

## 5. 프로젝트 코어와 보호 대상

> 한 명의 대장장이가 제한된 하루 작업량으로 장비 한 점을 직접 만들고, 강화 위험과 +10 수식어 선택으로 운명을 정한 뒤, 그 장비가 다른 이의 손에서 쌓은 역사를 명성과 다음 의뢰로 돌려받는 모바일 제작 게임.

보호 대상은 직접 제작, 영구 완성도, 입력당 강화 1회, +10 선택, 세계 장비 이력, 결과 인과 설명, 단일 대장장이의 일일 우선순위다.

## 6. 확인한 책임 원본과 실제 파일

| 책임 | 파일 | 사전 판정 | 조치 |
|---|---|---|---|
| 시작점 | README, START_HERE | UPDATE_REQUIRED | 코어·현재 구현·다음 구현 분리 |
| 현재 상태 | ACTIVE_CONTEXT | UPDATE_REQUIRED | Issue #34·PR·미검증 갱신 |
| 문서 지도 | DOCUMENTATION_MAP | UPDATE_REQUIRED | Core·Spec·Scope·Plan·Report 연결 |
| Gate | DEVELOPMENT_GATES | UPDATE_REQUIRED | PASS/NOT_STARTED/NOT_RUN 분리 |
| Roadmap | ROADMAP | UPDATE_REQUIRED | 장비 생애 PoC CURRENT |
| Decision | DECISION_LOG | UPDATE_REQUIRED | DEC-023~025, stale 상태 수정 |
| 통합 기획 | Game Bible | UPDATE_REQUIRED | 확정 코어 기반 재정렬 |
| Core | project-core-design | CURRENT_CANONICAL | 보호 |
| Spec | lifecycle integrated spec | CURRENT_CANONICAL | 논리·호환성 개선 |
| Plan | lifecycle implementation plan | CURRENT_CANONICAL | 반례·원자성 개선 |
| MVP Scope | MVP-003_SCOPE | MISSING | 생성 |
| 구현 | data/scripts/scenes/tests | Prototype만 구현 | 제품 비변경 |

## 7. 적대적 검토 1차 결과

### 관점
대화·요구사항·책임 범위.

### Findings
- `F1-01 MUST_FIX HIGH`: 시작 문서가 과거 +100·자동 단조를 현행 코어처럼 제시.
- `F1-02 MUST_FIX HIGH`: Roadmap의 MVP-003 Scope 파일이 없음.
- `F1-03 MUST_FIX HIGH`: 완료된 Issue #29·#14가 open, 현행 Goal Issue 없음.
- `F1-04 SHOULD_FIX MEDIUM`: 최신 피로도·날짜·세계 잔존 결정이 Decision Log에 없음.

### 반영
시작·상태 문서 갱신, MVP-003 Scope 생성, Issue #34 생성, #29·#14 종료, DEC-023~025 추가.

## 8. 적대적 검토 2차 결과

### 관점
논리·모순·판정 가능성.

### Findings
- `F2-01 MUST_FIX HIGH`: 기존 정상 +5 납품 최소 점수가 45여서 0~39 DEFEAT가 도달 불가능.
- `F2-02 SHOULD_FIX MEDIUM`: 완성도 표시명·배율이 코어 불변처럼 보임.
- `F2-03 MUST_FIX HIGH`: 문서 승인과 제품 구현 완료 상태가 혼합됨.

### 반영
점수를 required 20, attack 10으로 조정하고 밴드를 0~34/35~69/70+로 수정했다. 미숙한 +5=30 DEFEAT, 정교한 +5=40 WIN, 명품 +10 preferred=85 DECISIVE_WIN 반례를 추가했다. 정확한 완성도 명칭·수치는 `PoC 임시 기준값`으로 분류했다.

## 9. 적대적 검토 3차 결과

### 관점
경계 조건·데이터·호환성.

### Findings
- `F3-01 MUST_FIX HIGH`: 신규 `quality_*`와 legacy STANDARD/GOOD/PERFECT/AUTO 의미 충돌.
- `F3-02 MUST_FIX HIGH`: 장비 생애 상태와 보고 상태 enum 혼용.
- `F3-03 MUST_FIX HIGH`: 납품 중 일부 상태만 성공할 위험.
- `F3-04 SHOULD_FIX MEDIUM`: record version·migration 경계 부재.
- `F3-05 SHOULD_FIX MEDIUM`: 결과 데이터 누락 복구 불명확.

### 반영
`record_schema_version: 1`, `precision_result_*`, `craftsmanship_grade_*`를 분리했다. legacy 변환과 자동 단조 AUTO+STANDARD grade를 명시했다. `lifecycle_state`와 `report_state`를 분리하고 원자적 납품·transaction ID·rollback·결정적 결과 재시도를 추가했다.

## 10. 적대적 검토 4차 결과

### 관점
플레이어 경험·UX·접근성·운영.

### Findings
- `F4-01 SHOULD_FIX MEDIUM`: 28/20 피로도 표기가 오류처럼 보일 수 있음.
- `F4-02 MUST_FIX HIGH`: 정밀 판정이 빠른 타이밍 입력 하나에 의존.
- `F4-03 SHOULD_FIX MEDIUM`: 결과·위험이 색상에 의존할 가능성.
- `F4-04 SHOULD_FIX MEDIUM`: 실패 뒤 복귀 경로가 불명확.

### 반영
현재 작업 가능량과 기본 일일량을 분리했다. 느린 게이지·넓은 판정·GOOD 분포의 정밀 보조를 추가하되 PERFECT 자동 보상은 금지했다. 텍스트·아이콘 병기, 자동 닫힘 금지, 모션 감소, 부족량·복귀 경로를 명시했다.

## 11. 적대적 검토 5차 결과

### 관점
GitHub 최신성·참조·통합 회귀·PR.

### Findings
- `F5-01 MUST_FIX HIGH`: 활성 소비자가 서로 다른 현재 코어·Goal을 주장.
- `F5-02 MUST_FIX HIGH`: 코어 정렬 자동 차단 검사 부재.
- `F5-03 MUST_FIX HIGH`: 최종 보고서·PDF·Manifest 미등록.
- `F5-04 SHOULD_FIX MEDIUM`: 과거 2회 검토 보고서가 CURRENT.
- `F5-05 UNVERIFIED HIGH`: Branch protection Required Check 강제 여부.
- `F5-06 UNVERIFIED HIGH`: stacked PR 미병합 상태의 main 정합성.

### 반영
`check_project_core_alignment.py`와 Workflow step을 추가하고 #391 Red를 재현했다. 시작 문서·Registry 소비자를 갱신하고 최종 보고서·PDF·Manifest 발행 경로를 추가했다. 과거 core review report는 역사 자료로 재분류한다.

## 12. MUST_FIX / SHOULD_FIX / DEFER / REJECT / UNVERIFIED

| 분류 | 항목 |
|---|---|
| MUST_FIX 수정 | F1-01~03, F2-01·03, F3-01~03, F4-02, F5-01~03 |
| SHOULD_FIX 수정 | F1-04, F2-02, F3-04·05, F4-01·03·04, F5-04 |
| DEFER | 방어구·악세서리, 전쟁·관전·베팅, 대표작·복원, 저장, 최종 +100 판정 |
| REJECT | 직원·직접 전투·작업 예약·일상 수리 관리의 재도입 |
| UNVERIFIED | skipped 원문, Required Check 강제, Android, 사람 접근성·성능·외부 플레이, 사람 PDF 검토 |

## 13. 실제 반영한 최소 변경

README·START_HERE·Active Context·Documentation Map·Roadmap·Gates·Game Bible·Decision Log·Base Audit를 갱신했다. `docs/MVP-003_SCOPE.md`, Issue #34, 코어 정렬 검사, 최종 보고서를 추가했다. Spec과 Plan의 점수·호환성·상태·원자성·접근성을 보강했다. 제품 GDScript·Scene·게임 데이터 수치는 변경하지 않았다.

## 14. Red → Green → Refactor 증거

### Red
- `a1a810d...`: core alignment 검사 추가.
- `09551dc...`: Data Workflow 연결.
- Data validation #391: 기존 JSON·강화·시뮬레이터 검사는 PASS, 새 core alignment 단계에서 예상 FAIL.

### Green
- 활성 문서·MVP Scope·Issue·Spec·Plan 갱신.
- 세 결과 밴드와 호환·원자성 반례 추가.

### Refactor
- Core, Game Bible, MVP Scope, Spec, Plan, Active Context의 책임을 분리했다.
- 과거 구현 slice와 역사 문서는 삭제하지 않고 역할을 명시했다.

최종 Green Workflow 결과는 PDF·Manifest 반영 뒤 기록한다.

## 15. GitHub 최신성·구형 참조 감사

| 파일·참조 | 역할 | 구형 여부 | 조치 | 결과 |
|---|---|---|---|---|
| README·START_HERE | 활성 시작점 | content drift | 갱신 | 완료 |
| Active·Roadmap·Gates | 현재 상태 | stale goal | 갱신 | 완료 |
| Game Bible | 통합 설명 | core drift | 갱신 | 완료 |
| Decision Log DEC-015·022 | 결정 이력 | stale version/state | 최신 override | 완료 |
| Issue #29·#14 | 역사 작업 | open stale | 완료 종료 | 완료 |
| PROJECT_CORE_REVIEW_REPORT | 과거 분석 | CURRENT stale | 역사 자료로 재분류 | Registry 반영 |
| legacy `quality_*` | 호환 필드 | ACTIVE_COMPATIBILITY | 변환 계약 | 보존 |
| MVP-001/002 | 과거 구현 slice | CURRENT_CANONICAL | 보존 | 유지 |

이름에 old·legacy·final·latest·v2/v3가 있다는 이유만으로 파일을 삭제하지 않았다.

## 16. 책임 원본·Registry·Documentation Map 동기화

- 정체성: Core contract.
- 통합 시스템: Game Bible.
- 현재 상태: Active Context.
- 순서: Roadmap·Issue #34·Plan.
- MVP 경계: MVP-003 Scope.
- 상세 규칙: Integrated Spec.
- 최종 검토: 이 보고서.
- 발행 상태: Registry·Publication Manifest.

## 17. 정적·런타임·회귀 검증 결과

| 검증 | 결과 |
|---|---|
| Git conflict | Red 이전 PASS |
| JSON game data | #391에서 PASS |
| 강화 실패 계약 | #391에서 PASS |
| 시뮬레이터 계약 | #391에서 PASS |
| Core alignment | #391 Red 예상 FAIL, 최종 Green 대기 |
| Base audit·전체 회귀 | Red 이후 skip, 최종 Green 대기 |
| Godot validation | 최종 head 결과 대기 |
| Lifecycle runtime | `NOT_RUN` - 미구현 |
| Android·접근성·성능·외부 플레이 | `NOT_RUN` |

## 18. PDF·Manifest·전 페이지 렌더 결과

- 책임 원본: `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md`.
- PDF: `docs/publications/BLACKSMITH_FINAL_ADVERSARIAL_REVIEW_2026-07-24.pdf`.
- Manifest: `docs/publications/BLACKSMITH_FINAL_ADVERSARIAL_REVIEW_2026-07-24.manifest.json`.
- 방식: DOCX 작성 후 LibreOffice PDF 변환.
- 자동 렌더: 200 DPI 전 페이지 검사.
- `human_visual_review: NOT_RUN`.

최종 페이지 수·해시·자동 렌더 결과는 Manifest가 책임진다.

## 19. PR 및 Required Check 결과

- #31·#32·#33: open Draft, 미병합.
- 병합 순서: #31→#32→#33.
- #33 review comments: 없음.
- Required Check 강제 설정: `UNVERIFIED`.
- 최종 PR 제목·본문·changed files·Workflow는 발행 뒤 재검토한다.

## 20. 커밋 목록과 각 커밋 목적

- Red core alignment 검사·Workflow.
- 시작·상태·Roadmap·Gate 정렬.
- MVP-003 Scope.
- Spec 논리·호환성·접근성.
- Plan 반례·원자성·호환성.
- Game Bible·Decision·Base Audit.
- Final report·Registry·PDF·Manifest.

GitHub connector가 파일별 독립 commit을 생성했다. 최종 PR commit·changed files를 다시 확인한다.

## 21. MVP 파일 갱신 결과

`docs/MVP-003_SCOPE.md`를 생성했다. 철검·검투사 1명, +5/+10 판단, 피로도·날짜, 원자 거래, 세 결과 밴드, 세계 기록과 재방문, `IMPLEMENTATION_NOT_STARTED`를 고정했다.

## 22. 원격 푸시 결과

GitHub connector의 create/update 작업은 원격 `agent/propose-project-core-contract`에 직접 commit된다. 최종 head와 PR head 일치는 발행·최종 CI 뒤 확인한다.

## 23. 남은 위험·미검증·후속 작업

- Issue #34 Task 1~9 구현.
- 신규·기존 Godot 전체 회귀.
- Android 실기기·접근성·성능·외부 플레이.
- PR #31·#32·#33 순차 병합.
- Branch protection Required Check 확인.
- 사람이 직접 PDF 열람.
- UI상 skipped 메시지 원문 확인.

## 24. 사람이 직접 확인할 체크리스트

- [ ] PDF 실제 뷰어 전 페이지 확인.
- [ ] PR #31→#32→#33 diff·병합 순서 확인.
- [ ] Branch protection Required Check 설정 확인.
- [ ] Issue #34 구현 PR의 Red/Green 분리 확인.
- [ ] Android 세로 화면·터치·안전 영역 확인.
- [ ] 정밀 보조가 입력 장벽을 줄이는지 확인.
- [ ] 신규 플레이어가 +5/+10 선택과 결과 원인을 설명하는지 확인.

## 25. Base 공용 규칙 승격 후보

- 구현계획 미래 경로와 활성 깨진 참조의 표기 분리.
- 코어 확정 뒤 시작·상태·Map·Roadmap·Gates coupled-change 검사.
- 결과 밴드 도달 가능 fixture lint.
- source·manifest·render 성공 뒤 PDF CURRENT를 원자 전환하는 gate.

반복 증거가 한 프로젝트에만 있으므로 즉시 Base에 반영하지 않는다.

## 26. 프로젝트 전용으로 유지할 내용

단일 대장장이, +10 강화, 피로도 20·50% 이월, 검투사 카일, +5/+10 판단, 결과 점수, lifecycle/report 상태 이름공간, Blacksmith 콘텐츠 확장 순서는 프로젝트 전용으로 유지한다.
