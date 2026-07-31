# Blacksmith 상황별 인게임 화면 중간점검

> 상태: `MID_CHECK_PASS_1 / FINDINGS_OPEN`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 작업 계약: `BS-SCREEN-20260731-01`
>
> Audit ID: `BS-MIDCHECK-20260731-01`
>
> 추적: Issue #79 / Draft PR #81

## 1. 판정

```text
STRUCTURAL_GAME_PLANNING: COMPLETE_WITH_DEFINED_BOUNDARIES
ACTUAL_SCREEN_BASELINE_AUDIT: COMPLETE_PASS_1
P0_SCREEN_SPEC: DEFINED
P0_FINDINGS: 6
P1_FINDINGS: 4
USER_DECISIONS_REQUIRED: 2
CODE_IMPLEMENTATION: BLOCKED
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
```

고객 4유형·+50 이원화 등 게임 규칙의 구조적 미결정은 0건이다. 그러나 실제 Scene·Script·데이터를 화면 기준으로 재검토한 결과, 최신 기획을 구현 가능한 화면 흐름으로 연결하기 위해 해결해야 할 P0 Finding이 존재한다.

중간점검에서 제품 코드는 수정하지 않았다.

## 2. 확인한 실제 파일

### 진입·Scene

- `project.godot`
- `scenes/main/main.tscn`
- `scenes/test/enhancement_test.tscn`
- `scenes/test/equipment_lifecycle_poc.tscn`

### 화면·흐름 Script

- `scripts/ui/game_flow_screen.gd`
- `scripts/ui/forging_screen.gd`
- `scripts/ui/special_enhancement_screen.gd`
- `scripts/ui/enhancement_screen.gd`
- `scripts/ui/lifecycle_enhancement_screen.gd`
- `scripts/poc/equipment_lifecycle_poc_screen.gd`
- `scripts/ui/customer_contract_screen.gd`
- `scripts/ui/world_report_screen.gd`
- `scripts/ui/workshop_hud.gd`
- `scripts/ui/lifecycle_accessibility_overlay.gd`

### 시스템·데이터

- `scripts/poc/equipment_lifecycle_poc_controller.gd`
- `data/crafting/forging_balance.json`
- `data/crafting/enhancement_balance.json`
- `data/crafting/enhancement_milestones.json`
- `data/customers/gladiator_poc.json`
- `data/world/gladiator_match_poc.json`

## 3. 프로젝트 핵심 정의

- 장르: 모바일 세로형 대장간 제작·강화·장비 생애 시뮬레이션
- 플랫폼: Android, 720×1280 기준 세로형
- 플레이어 역할: 장비를 제작하고 강화·판매·인계하는 대장장이
- 핵심 판타지: 내가 만든 한 작품이 특정 인물과 세계에서 전설이 되는 과정을 만든다.
- 핵심 감정: 단조 손맛 → 강화 욕심과 손실 긴장 → 작품 완성감 → 인계 책임감 → 세계 결과에 대한 자부심
- 주요 선택: 멈춤·추가 강화·보호, +49에서 일반/고위 정밀강화, 어떤 고객에게 작품을 인계할지
- 주요 보상: 작품 정체성, 수익, 고객 관계, 세계 변화, 장비 연대기, 미래 명작 전당
- 대표 장면: 첫 망치, +5 완성/+10 도전, +49→+50 경로 선택, 고객이 작품을 사용하는 결과, 장비 연대기 귀환
- 상징 요소: 화로·망치·모루·불씨 정령 모닥·이름 있는 장비
- 차별점: 장비 수치만 높이는 것이 아니라 제작 등급·강화 경로·소유권·사건·연대기를 한 작품에 누적한다.

## 4. 핵심 플레이 루프

```text
대장간 진입
→ 제작할 작품과 재료 확인
→ 단조
→ 제작 결과·등급 확인
→ 강화 위험·비용 비교
→ 멈춤 또는 추가 도전
→ 방문 고객 요청과 작품 비교
→ 판매·인계
→ 세계 시간 진행
→ 사용 결과·관계·연대기 확인
→ 다음 작품·고객·강화 목표 발생
```

## 5. 현재 시각·UX 방향

### 실제 구현에서 확인

- 배경: `#17191f`의 어두운 숯·철 계열
- 기본 패널: `#252932`, 보조 패널 `#303641`
- 핵심 행동: 주황 `#d7772e`, 금색 `#f2c14e`
- 성공·안전: 녹색 `#72b879`
- 위험·실패: 적색 `#e36c62`
- 본문: 미색 `#f4f1e8`, 보조 정보 `#b7b0a3`
- 패널·버튼: 둥근 모서리, 큰 세로형 버튼
- 화면 생성: 대부분 GDScript가 런타임에 Control·Container를 생성
- 입력: 모바일 터치와 Space 입력이 같은 행동 경로를 사용

### 판정

현재 색·위험 표현은 일관적이다. 다만 최종 제품의 장비 중심 화면, 화로·모루 배경, 캐릭터·고객·모닥 표현은 실제 UI에 거의 없으며, 텍스트 패널 중심 PoC다.

## 6. 현재 화면·UI 구현 현황

| 화면 영역 | 실제 구현 | 상태 | 최신 기획과의 관계 |
|---|---|---|---|
| 앱 기본 진입 | `enhancement_test.tscn` | 테스트 전용 | 제품 메인 화면 아님 |
| 제작·강화 통합 흐름 | `scenes/main/main.tscn` + `game_flow_screen.gd` | 구현·수동 F6 | 제품 Shell 후보이나 메인 진입 아님 |
| 장비 생애 PoC | `equipment_lifecycle_poc.tscn` | 구현·사람 검증 대기 | 카일 단일 검투사 구형 PoC |
| 단조 | `forging_screen.gd` | 구현 | 최신 첫 5분 계약과 일부 일치 |
| 강화 | `enhancement_screen.gd` 계열 | 구현 | 구형 10단위 특수 강화 구조 |
| 보관함 | `game_flow_screen.gd` 내부 Overlay | 구현 | 무기 6칸·세션 메모리 한정 |
| 고객 요청 | `customer_contract_screen.gd` | 구현 | 카일·철검 하드코딩 |
| 세계 결과 | `world_report_screen.gd` | 구현 | 검투사 경기 결과 한정 |
| 접근성 | 별도 Overlay | 부분 구현 | 실제 기기·포커스·노치 검증 미실행 |
| 저장·복귀 | 상태 Snapshot·원자 롤백 | 도메인 일부 | 파일 영속 저장·앱 재시작 복귀는 미확인 |

---

# 필수 기준 화면 4종

## SCREEN-01 — 대장간 허브·복귀 화면

### 현재 정의 상태

- `project.godot` 기본 실행은 `enhancement_test.tscn`이다.
- 제품 흐름 Scene `scenes/main/main.tscn`은 수동 F6 진입이다.
- 현재 화면은 별도 메인 메뉴나 저장 선택이 아니라 단조 화면부터 시작한다.
- 장비 생애 PoC는 별도 버튼·Scene으로 분리돼 있다.

### 현재 확인안

```text
F5
└─ 강화 테스트 화면
   ├─ 테스트 철검
   ├─ 일반/특수 강화
   ├─ 자동 단조
   └─ 보관함 Overlay
```

### 개선 제안안

```text
┌──────────────────────────────────┐
│ 1일차 · 골드 · 작업량   [설정]  │
├──────────────────────────────────┤
│          화로·모루·현재 작품     │
│          모닥의 짧은 안내         │
├──────────────────────────────────┤
│ [계속 제작] [강화] [새 작품]     │
│ [보관함] [방문 고객 1] [소식 1] │
├──────────────────────────────────┤
│ 현재 목표 · 다음 마감 · 위험 알림│
└──────────────────────────────────┘
```

### 목적

1. 현재 작품과 가장 중요한 다음 행동을 즉시 찾게 한다.
2. 미확인 결과·고객 요청·마감을 놓치지 않게 한다.
3. 제작·강화·보관함·고객·세계 결과로 이동하는 단일 복귀 지점을 제공한다.

### 권장 구현

- 신규 제품 Shell Scene: `BlacksmithApp.tscn` 또는 기존 `main.tscn`의 제품 승격
- `AppStateCoordinator`가 현재 작품, 작업일, 활성 고객, 미확인 결과를 소유
- 화면은 별도 Scene 또는 재사용 가능한 `ForgeHubScreen.tscn`
- 제작·강화·보관함·결과는 Shell 아래 상태 전환 또는 Overlay로 연결

### 상태 변형

- 신규 실행
- 진행 작품 없음
- 제작 중 작품 있음
- 미확인 강화 결과 있음
- 방문 고객 요청 있음
- 세계 보고 도착
- 자원 부족
- 튜토리얼
- 앱 복귀

## SCREEN-02 — 단조·강화 핵심 작업대

### 현재 정의 상태

단조와 강화는 각각 동작한다. 단조는 연타·자동 진행·피버·정밀 마감, 강화는 일반/10단위 특수 화면을 제공한다.

### 현재 확인안

```text
단조
제목·상태
→ 재료·무기
→ 진행·피버
→ 큰 망치질 버튼
→ 정밀 마감
→ 제작 결과

강화
제목·단계
→ 작품명·다음 이정표
→ 확률·비용·위험
→ 일반 또는 특수 강화 버튼
→ 결과·보관·자동 단조
```

### 개선 제안안

```text
┌──────────────────────────────────┐
│ 작품명 +49   제작등급   [정보]  │
├──────────────────────────────────┤
│          장비·모루·화로          │
│      판정 연출과 상태 피드백      │
├──────────────────────────────────┤
│ 현재→목표 · 성공률 · 최악 결과   │
│ 비용 · 보호 · 남은 자원          │
├──────────────────────────────────┤
│ [일반 정밀강화]                  │
│ 저비용 / 기존 위험 / 특수 없음   │
│ [고위 정밀강화]                  │
│ 특수재료 / 확정 / 후보·수식어    │
└──────────────────────────────────┘
```

### 핵심 Finding

- 현재 `enhancement_milestones.json`은 +50에서 세 번째 수식어 슬롯을 추가한다.
- 최신 기획은 계보 1개+보조 최대 2개이며 +50은 일반/고위 정밀강화 두 경로다.
- 현재 화면은 `특수 강화`라는 단일 경로와 촉매 성공률 보정 구조다.
- 최신 +50 경로 비교 화면·후보 선택·경로 저장은 미구현이다.

### 권장 Scene 구조

```text
CoreWorkbenchScreen
├─ WorkpieceViewport
├─ WorkbenchHeader
├─ WorkbenchStateMachine
├─ ForgingStateView
├─ EnhancementStateView
├─ PrecisionStateView
├─ Plus50RouteComparisonView
├─ ResultFeedbackLayer
└─ RiskAndCostPanel
```

단조와 강화는 동일 제품 Shell 아래 상태 View로 구성하되, 각 View는 독립 재사용 Scene으로 분리한다.

## SCREEN-03 — 보관함·자원 관리

### 현재 정의 상태

- Prototype 보관함은 `game_flow_screen.gd`에서 생성하는 전체 화면 Overlay다.
- 최대 6개 무기를 저장한다.
- 판매가·누적 강화비·예상 손익·촉매 기록을 표시한다.
- 화면 인스턴스의 배열에 저장되며 앱 재시작 영속성은 확인되지 않았다.
- 고객 적합 비교·장비 유형·상태·소유권·연대기 필터는 없다.

### 현재 확인안

```text
무기 보관함 0/6
→ 설명
→ 무기 카드 목록
→ 판매가·강화비·손익·촉매
→ 대장간 복귀
```

### 개선 제안안

```text
┌──────────────────────────────────┐
│ 보관함 12/20   골드·재료 [필터] │
├──────────────────────────────────┤
│ [작업 중] [완성] [고객 요청]    │
│ [분실/회수] [역사]               │
├──────────────────────────────────┤
│ 작품 카드                        │
│ 등급 · +단계 · 계보/보조 · 경로 │
│ 소유상태 · 고객 적합 신호        │
├──────────────────────────────────┤
│ [작품 정보] [강화] [판매/제안]  │
└──────────────────────────────────┘
```

### 권장 구현

- 재사용 `StorageScreen.tscn`
- `EquipmentRecord` 데이터와 화면 표시 ViewModel 분리
- 자원은 Header 또는 접이식 Resource Panel로 제공
- 고객 요청에서 진입하면 요청 범주·적합 이유를 유지한 필터 상태로 연다.

## SCREEN-04 — 결과·세계 환류·연대기

### 현재 정의 상태

결과 화면이 세 종류로 분산돼 있다.

1. 단조 완료 Panel
2. 강화 완료/실패 화면
3. 검투사 경기 `WorldReportScreen`

세계 보고는 효과가 있었던 선택·부족 조건·기여 점수·명성·관계를 표시한다. 이는 최신 기획의 공개 기여 원인과 잘 맞는다. 그러나 카일·검투사 경기·재방문 문구가 하드코딩돼 있다.

### 개선 제안안

```text
┌──────────────────────────────────┐
│ 결과 유형 · 작품명 · 소유자     │
├──────────────────────────────────┤
│ 핵심 결과                        │
│ 이전 상태 → 현재 상태            │
├──────────────────────────────────┤
│ 효과가 있었던 선택               │
│ 부족했던 조건                    │
│ 장비가 기여한 이유               │
├──────────────────────────────────┤
│ 관계·세계·연대기 변화            │
│ 다음 요청·목표                   │
├──────────────────────────────────┤
│ [연대기 보기] [다음] [대장간]   │
└──────────────────────────────────┘
```

### 권장 구현

공통 `ResultEnvelope`를 사용한다.

```text
ResultEnvelope
- result_type
- subject_equipment_uid
- actor_id/customer_id
- previous_state
- current_state
- costs
- effective_choices[]
- missing_conditions[]
- contribution_reasons[]
- relationship_changes[]
- world_changes[]
- chronicle_entries[]
- next_actions[]
```

제작·강화·고객·세계 결과는 같은 결과 Shell을 사용하고 본문 Panel만 교체한다.

---

# 대표 상황과 우선순위

| ID·상황 | 빈도 | 재미 | 감정 | 구현 위험 | 차별성 | 우선순위 |
|---|---:|---:|---:|---:|---:|---|
| SIT-001 대장간 첫 진입·복귀 | 5 | 4 | 4 | 5 | 4 | P0 |
| SIT-002 첫 작품 단조·정밀 마감 | 5 | 5 | 4 | 3 | 3 | P0 |
| SIT-003 일반 강화 위험 판단·결과 반복 | 5 | 5 | 5 | 4 | 4 | P0 |
| SIT-004 +49 일반/고위 정밀강화 선택 | 2 | 5 | 5 | 5 | 5 | P0 |
| SIT-005 방문 고객 요청과 작품 비교 | 3 | 5 | 5 | 5 | 5 | P0 |
| SIT-006 세계 결과·연대기 귀환 | 2 | 5 | 5 | 4 | 5 | P0 |
| SIT-007 보관함 작품 비교·재진입 | 4 | 4 | 3 | 4 | 4 | P1 |
| SIT-008 자원 부족·행동 차단·복구 | 3 | 3 | 3 | 3 | 2 | P1 |
| SIT-009 하루 종료·마감 진행 | 2 | 3 | 3 | 3 | 3 | P1 |
| SIT-010 분실·회수·영구 파괴 확인 | 1 | 4 | 5 | 5 | 5 | P1 |
| SIT-011 접근성 설정·복귀 | 1 | 2 | 2 | 3 | 2 | P2 |
| SIT-012 명작 전당 등록·비교 | 1 | 3 | 4 | 5 | 4 | P3·미래 |

---

# P0 상황별 구현 명세

## SIT-001 — 대장간 첫 진입·복귀

### A. 상황 개요

- 발생: 신규 실행 또는 다른 화면에서 대장간 복귀
- 목표: 현재 가장 중요한 행동을 선택
- 위험: 테스트 Scene·미확인 결과·마감·작품 상태를 놓침
- 감정: 작업을 이어갈 준비, 내 대장간으로 돌아온 안정감
- 선택: 제작 계속, 강화, 보관함, 고객, 결과 확인

### B. 근거와 가정

- 확정: Android 세로형, 첫 5분 30초 내 첫 망치, 미확인 결과 우선 확인
- 실제: F5는 강화 테스트, 제품 흐름은 수동 `main.tscn`
- 제안: 제품 Shell과 대장간 허브 신설
- 확인 필요: 앱 시작 시 별도 타이틀 화면을 둘지, 즉시 대장간으로 들어갈지

### C~D. 진입·화면 목적

- 신규 실행은 대장간 첫 화면으로 진입
- 저장 복귀는 미확인 비가역 결과가 있으면 결과 확인 우선
- 입력 잠금 중인 판정이 있으면 재추첨 없이 저장 결과 복원
- 첫 3초: 현재 작품, 주요 행동, 미확인 결과·고객·마감

### E. 와이어프레임

SCREEN-01 개선 제안안 사용.

### F~G. 요소·입력

- 작품/모루: 제작·강화 진입
- 보관함: Overlay 또는 별도 Screen
- 방문 고객·소식 Badge: 해당 데이터가 있을 때만 표시
- 뒤로 가기: 앱 종료 확인 또는 OS Back 규칙
- 모바일 터치만 P0 입력으로 정의

### H~I. 흐름·반응

```text
앱 시작
→ SaveCoordinator 복구
├─ 미확인 결과 있음 → SIT-006/결과 확인
└─ 없음 → 허브 표시
→ 행동 선택
→ 조건 검증
→ 대상 화면 전환
```

중복 입력은 전환 토큰으로 차단하고, 조건이 바뀌면 행동을 취소한 뒤 이유를 표시한다.

### J~N. 시스템·Godot·데이터

- `AppStateCoordinator`: 화면 상태와 현재 작품
- `SaveCoordinator`: 마지막 확정 상태·미확인 결과
- `ScreenRouter`: 전환·중복 방지
- `ForgeHubScreen.tscn`: 사용자 표시
- `NotificationQuery`: 고객·소식·마감 Badge
- 저장: 현재 작품 ID, 화면 복귀 위치, 미확인 결과 ID, 튜토리얼 완료

### O~R. 유지·연출·예외

- 반드시 유지: 작품·자원·작업일·고객 요청·보고 상태
- 초기화: 임시 Hover·확장 Panel
- 첫 진입 연출은 짧고 건너뛸 수 있어야 함
- 데이터 누락 시 안전한 허브와 복구 안내 표시

### S~T. 완료·테스트

- 첫 행동을 3초 내 찾을 수 있음
- 저장 복귀 시 같은 결과가 표시됨
- 고객·소식 Badge가 실제 데이터와 일치
- 화면 전환 중 중복 입력 0건
- 360×640 override와 720×1280에서 핵심 버튼 잘림 없음

## SIT-002 — 첫 작품 단조·정밀 마감

### A. 상황 개요

- 목표: 첫 작품 완성
- 정보: 진행·피버·정밀 마감
- 감정: 손맛·집중·완성감
- 선택: 연타, 기다림, 정밀 마감 사용

### B. 근거

- 실제 구현: 자동 진행, 연타 피버, 정밀 마감, 결과 Panel
- 확정 기획: 첫 30초 1~3회 핵심 입력, 장비 중심 시각, 제작 등급은 강화와 분리
- 불일치: 현재 망치 버튼이 화면의 주인공이며 실제 장비·모루 연출은 없음

### C~I. 진입·흐름

```text
제작 비용 검증
→ 제작 상태 저장
→ 단조 입력
→ 진행·피버 피드백
→ 마감 판정
→ 제작 등급·최초 연대기 생성
→ 원자 저장
→ 제작 결과
```

자원 부족·중복 제작·앱 종료를 방어한다.

### J~N. Godot

```text
ForgingStateView.tscn
├─ WorkpieceView
├─ HammerInputArea
├─ ProgressHud
├─ FeverFeedback
├─ PrecisionPanel
└─ ForgingResultPreview
```

기존 `ForgingSession`을 유지하고 UI만 Scene으로 분리할 수 있다.

### O~T. 완료

- 첫 입력 30초 이내 후보
- 색·소리·진동 없이 진행 상태 인지
- 제작 결과 저장 전 성공 연출 금지
- 마감 실패가 장비 삭제로 오인되지 않음
- 제작 등급·강화 단계의 차이를 설명 가능

## SIT-003 — 일반 강화 위험 판단·결과 반복

### A. 상황 개요

- 목표: 현재 작품을 더 강화할지 판단
- 정보: 단계·총성공률·결과별 확률·비용·최악 결과·보호
- 감정: 욕심과 손실 긴장
- 선택: 강화, 보호, 멈춤, 상세 보기

### B. 근거·불일치

- 실제: 일반 강화와 10단위 특수 강화가 다른 화면
- 실제: 현재 Prototype 확률·비용·유지·하락·파괴 표시
- 확정: 결과 확률 합계 100.00%, 중복 판정 금지, 결과 확인 후 재시도
- 제안: 결과 Panel을 공통 Result Shell로 통합

### C~I. 흐름

```text
작품 선택
→ 다음 단계 규칙 계산
→ 확률·비용 표시
→ 입력 잠금 토큰 확보
→ 자원 원자 차감
→ 1회 판정
→ 결과 저장
→ 결과 표시
→ 재시도·완성·나가기
```

### J~N. Godot·데이터

- `EnhancementStateView.tscn`
- `RiskBreakdownPanel.tscn`
- `AttemptTransactionService`
- `EnhancementResultEnvelope`
- 데이터는 기존 balance JSON을 사용하되 최신 정본 전파 후 Schema를 갱신

### O~T. 완료

- 표시 확률과 판정 데이터 일치
- 중복 입력 0건
- 자원 부족 시 판정·실패 보정 미변경
- 유지·하락·파괴를 색 외 문구·아이콘으로 구분
- 앱 재진입 시 동일 판정 결과

## SIT-004 — +49 일반/고위 정밀강화 선택

### A. 상황 개요

- 목표: +50 도달 경로 선택
- 일반: 낮은 비용, 기존 위험, 특수 수식어 없음
- 고위: 특수재료, 확정 성공, 후보·특수 수식어
- 감정: 희귀재료를 지금 쓸지 고민하는 명작 제작 긴장

### B. 근거

- 확정: `BS-ENH-20260731-01`
- 실제: +50은 구형 세 번째 수식어 추가 특수 강화
- 미구현: 경로 비교, 촉매/특수 보조 역할, 후보 2~3개, 경로 저장

### C~I. 흐름

```text
+49 도달
→ 두 경로 비교
├─ 일반 정밀
│  → 기존 결과 확률 확인
│  → 보호 선택
│  → 1회 판정
└─ 고위 정밀
   → 특수재료 역할 선택
   → 유효 후보 2~3개 생성
   → 후보 선택
   → 최종 비용·남는 자원 확인
   → 길게 누르기 또는 2단계 접근성 확인
   → 확정 성공·+50·특수 수식어 저장
```

고위 후보가 2개 미만이면 실행하지 않는다.

### J~N. Godot·데이터

```text
Plus50RouteComparisonView.tscn
├─ GeneralPrecisionCard
├─ HighPrecisionCard
├─ MaterialRoleSelector
├─ EvolutionCandidateList
├─ ResourceAfterActionPanel
└─ IrreversibleConfirmControl
```

필수 저장:

- `enhancement_route_at_50`
- `special_material_uses[]`
- `special_affix_id`
- `high_precision_evolution_id`
- 확정 결과 Transaction ID

### O~T. 완료

- 6명 중 5명 이상 두 경로 차이 설명 후보
- 일반 경로가 함정 버튼으로 인식되지 않음
- 특수재료 역할과 후보 변화가 실행 전 표시
- 고위 무변화 결과 0건
- 취소·앱 종료 시 자원 미소비 또는 동일 확정 결과 복구

## SIT-005 — 방문 고객 요청과 작품 비교

### A. 상황 개요

- 목표: 고객 요청에 어떤 작품을 제안할지 결정
- 정보: 요청 범주, 최소 조건, 공개 적합 이유, 가격, 야망, 기한, 후속 활동
- 감정: 즉시 수익과 작품의 다음 삶 사이의 책임감

### B. 근거

- 확정: 4유형×유형별 복수 고객, 범주 자격과 공개 적합 분리
- 실제: 카일 한 명·철검·+5/+10·선호 수식어 하드코딩
- 미구현: CustomerType/NamedCustomer 분리, 복수 요청, 작품 비교

### C~I. 흐름

```text
고객 요청 발생
→ 요청 카드 확인
→ 보관함을 요청 필터 상태로 열기
→ 거래 자격 작품 표시
→ 각 작품의 적합 이유·가격·후속 방향 비교
→ 작품 선택
→ 소유권·보상 원자 거래
→ 고객 유형별 후속 활동 예약
```

### J~N. Godot·데이터

- `CustomerRequestScreen.tscn`
- `EquipmentOfferList.tscn`
- `FitReasonPanel.tscn`
- `CustomerTypeResource` 또는 JSON
- `NamedCustomerResource` 또는 JSON
- 공통 `CustomerOutcomePipeline`

고객 이름에 따른 분기 코드 대신 `customer_type_id`, `customer_id`, `request_category`, `fit_weights`를 사용한다.

### O~T. 완료

- 같은 유형 2명 이상이 최소 3개 변주 축으로 구분
- 낮은 적합도도 거래 가능하며 이유 표시
- 잘못된 장비·기한 종료·중복 판매 차단
- 소유권·골드·고객 상태가 하나의 Transaction으로 저장

## SIT-006 — 세계 결과·연대기 귀환

### A. 상황 개요

- 발생: 영업일 진행 후 고객 활동 결과 도착 또는 앱 복귀 시 미확인 결과 존재
- 목표: 작품이 무엇에 기여했고 무엇이 부족했는지 이해
- 감정: 자부심·후회·다음 작품 욕구

### B. 근거

- 실제: 카일 경기 보고는 효과적 선택·부족 조건·기여 점수 제공
- 확정: 수집가·모험가·검투사·군인의 서로 다른 세계 환류
- 미구현: 공통 결과 Envelope·유형별 View·미확인 결과 복귀

### C~I. 흐름

```text
세계 결과 생성
→ 원자 저장
→ 미확인 결과 Queue 등록
→ 결과 화면 진입
→ 결과·기여·부족·운명·관계·세계 변화 확인
→ 연대기 기록 확인
→ 다음 요청·지원·복귀 선택
→ 확인 상태 저장
```

### J~N. Godot·데이터

- `ResultScreen.tscn`
- `ResultEnvelope`
- 유형별 `CollectorResultPanel`, `AdventurerResultPanel`, `GladiatorResultPanel`, `SoldierResultPanel`
- 공통 `ChroniclePanel`
- `PendingResultQueue`

### O~T. 완료

- 결과를 다시 열어도 보상이 중복 적용되지 않음
- 결과 확인 순서가 판정을 바꾸지 않음
- 장비 운명·소유자·연대기가 일치
- 앱 종료 후 동일 결과 복귀
- 승리뿐 아니라 실패·부분 성공도 다음 목표 제공

---

# 전체 상황 연결

```text
SIT-001 대장간 허브
├─ 새 작품 → SIT-002 단조
│  └─ 제작 결과 → SIT-003 일반 강화
│     ├─ 멈춤 → SIT-007 보관함
│     ├─ +49 도달 → SIT-004 +50 경로 선택
│     └─ 파괴·결과 → SCREEN-04 결과
├─ 고객 요청 → SIT-005 작품 비교·인계
│  └─ 영업일 진행 → SIT-006 세계 결과·연대기
├─ 보관함 → SIT-007 작품 비교
└─ 미확인 결과 → SIT-006
```

## 전환 계약

| 이전 | 조건 | 다음 | 유지 데이터 | 방식 |
|---|---|---|---|---|
| 허브 | 제작 선택 | 단조 | 자원·작업일 | Shell 상태 전환 |
| 단조 | 제작 저장 완료 | 결과/강화 | 작품 UID·제작 등급 | 결과 Panel→상태 전환 |
| 강화 | 결과 확인 | 강화/보관함/허브 | 작품·자원·판정 | 상태 전환 |
| +49 | 경로 선택 | 일반/고위 정밀 | 작품·재료·후보 | 전용 View |
| 고객 | 작품 선택·거래 | 허브 | 소유권·보상·요청 | 원자 저장 후 전환 |
| 영업일 | 결과 도착 | 결과 | 세계 결과·연대기 | 우선 Overlay/Screen |

---

# 시스템 의존 관계

```text
AppStateCoordinator
├─ ScreenRouter
├─ SaveCoordinator
├─ EquipmentRepository
├─ WorkshopCalendar
├─ WorkshopResources
├─ ForgingSession
├─ EnhancementSession
├─ CustomerRequestService
├─ CustomerOutcomePipeline
├─ EquipmentWorldRegistry
├─ PendingResultQueue
└─ Telemetry
```

UI는 도메인 객체를 직접 생성하지 않고 Coordinator 또는 Service에서 Snapshot·Command를 받는 방향을 권장한다.

# 공통 UI와 화면 전용 UI

## 공통

- 작품 요약 카드
- 단계·확률·비용·위험 Panel
- 자원 Header
- 상태·오류·복구 Banner
- 결과 Shell
- 연대기 Panel
- 고객 적합 이유 Panel
- 불가역 행동 확인 Control
- 빈 상태·잠김·로딩·오류 View

## 화면 전용

- 망치질·피버·정밀 마감
- +49→+50 경로 비교
- 고객 유형별 결과 Panel
- 모닥 첫 타격 안내
- 미래 명작 전당 목록

# 재사용 Scene과 프로젝트 전용 Scene

## 재사용 후보

- `ResourceHeader.tscn`
- `EquipmentSummaryCard.tscn`
- `RiskBreakdownPanel.tscn`
- `ResultScreen.tscn`
- `ChroniclePanel.tscn`
- `EmptyStatePanel.tscn`
- `IrreversibleConfirmControl.tscn`
- `StatusBanner.tscn`

## Blacksmith 전용

- `ForgeHubScreen.tscn`
- `ForgingStateView.tscn`
- `Plus50RouteComparisonView.tscn`
- `CustomerRequestScreen.tscn`
- 유형별 세계 결과 Panel

# Finding Ledger

## P0

1. `BS-SCR-F01` — F5 진입이 강화 테스트이며 제품 메인 허브가 없음
2. `BS-SCR-F02` — 최신 +50 두 경로와 구형 10단위 특수 강화·세 번째 슬롯 충돌
3. `BS-SCR-F03` — 고객 화면·결과가 카일/검투사에 하드코딩됨
4. `BS-SCR-F04` — 제작·강화·세계 결과가 공통 결과 계약 없이 분산됨
5. `BS-SCR-F05` — 미확인 결과·앱 종료·재진입을 책임지는 영속 Save Shell이 실제 화면 경로에서 미확인
6. `BS-SCR-F06` — 대부분 UI가 런타임 Script 생성이라 Scene 재사용·시각 검수 경계가 불명확

## P1

1. `BS-SCR-F07` — 보관함이 무기 6칸·세션 메모리 구조이며 최신 작품·소유권·고객 비교를 표현하지 못함
2. `BS-SCR-F08` — 접근성 Overlay가 화면 위에 별도 부착되고 실기기·포커스·노치 검증 미실행
3. `BS-SCR-F09` — 4개 정보의 수평 Workshop HUD가 작은 폭·텍스트 확대에서 과밀 위험
4. `BS-SCR-F10` — 구형 용어·등급·수식어 데이터가 최신 정본과 다름

# 권장 Vertical Slice 화면 구현 순서

```text
1. 제품 Shell·Save/Result 복귀 계약
2. 공통 EquipmentRecord·ResultEnvelope 화면 데이터
3. 대장간 허브
4. 단조 View 재구성
5. 일반 강화·결과 반복
6. +49→+50 경로 비교·고위 후보 선택
7. 보관함·작품 비교
8. CustomerType/NamedCustomer 요청 화면
9. 카시아 결과 + 에르사 분리 검증
10. 모험가·군인 데이터 시나리오
11. 접근성·Android·사람 검증
```

# 사용자 확인이 필요한 결정

## DECISION-NEEDED-01 — 앱 시작 방식

- A안 권장: 별도 타이틀 메뉴 없이 저장 복구 후 대장간 허브로 즉시 진입
- B안: 타이틀/이어하기/설정 화면을 거쳐 진입

권장 이유: 모바일 반복 플레이와 30초 첫 망치 목표에 A안이 적합하다. 설정·계정·온라인 기능은 허브 설정과 필요 시 시작 전 Overlay로 제공한다.

## DECISION-NEEDED-02 — 제품 Shell 내 화면 전환 방식

- A안 권장: 하나의 앱 Shell 아래 허브·작업대 상태 전환 + 보관함/결과 Overlay 혼합
- B안: 모든 기능을 완전히 별도 Scene으로 교체

권장 이유: 현재 작품·자원·BGM·화로 맥락을 유지하고 모바일 전환 비용을 줄이기 위해 A안이 적합하다.

# Base 승격 후보

- 필수 기준 화면 4종을 프로젝트 대응 화면으로 치환하는 감사 절차
- `SCREEN → SIT` 상태 변형 구조
- 현재 구현·기획·가정·제안 분리
- 공통 `ResultEnvelope`와 미확인 결과 복귀 체크리스트
- P0 A~T 상황 명세
- 런타임 Script 생성 UI를 Scene 재사용 후보로 판정하는 기준

# 프로젝트 전용 유지

- 대장간 허브와 화로·모루 맥락
- 단조·피버·정밀 마감
- +5/+10·+49/+50 강화 판단
- 고객 4유형과 장비 세계 환류
- 장비 소유권·운명·연대기
- 모닥·카시아·에르사

# 다음 Gate

```text
사용자 DECISION-NEEDED-01·02 승인
→ P0 Finding 대응 기획 정본 갱신
→ 화면 보드와 상세 명세 최종화
→ 적대적 검토 Pass 2
→ 구조 P0 Finding 0건 확인
→ 사용자 기획 완료 선언 가능 후보 복귀
```
