# Blacksmith 메인 화면·제품 Shell 승인 정본

> 상태: `USER_APPROVED / CANONICAL_SCREEN_SHELL_DIRECTION`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 추적: Issue #79 / Draft PR #81
>
> 관련 시각 설계: `BS-VISUAL-20260731-01`

## 1. 승인 결정

### BS-MAIN-20260801-01 — 별도 메인 화면

Blacksmith는 앱 실행 후 제품 플레이 화면으로 바로 진입하지 않고 **별도의 메인 화면**을 사용한다.

필수 상태:

```text
최초 실행·저장 없음
→ 새 게임 활성
→ 이어하기 비활성

저장 있음
→ 이어하기 활성
→ 새 게임은 기존 저장 영향 경고 후 진입

설정에서 복귀
→ 메인 화면의 선택·포커스 상태 복구
```

필수 기능:

- 이어하기
- 새 게임
- 설정

추가 메뉴는 다음처럼 처리한다.

- 도감·가이드·제작자·크레딧은 콘텐츠와 정보 구조가 확정된 뒤 추가 가능한 `PROPOSED` 항목이다.
- Android의 `게임 종료` 버튼은 필수가 아니며 플랫폼 UX 검토 전 확정하지 않는다.
- 메인 화면의 배경·로고·모닥 배치는 승인된 `스타일라이즈드 다크 포지`와 `밝은 불 정령 모닥`을 따른다.

### BS-SHELL-20260801-01 — 단일 제품 Shell + View·Overlay 혼합

별도 메인 화면에서 게임을 시작하거나 이어가면 하나의 `BlacksmithApp` 제품 Shell로 진입한다.

```text
MainMenuScene
→ Save load or new campaign
→ BlacksmithApp
   ├─ 대장간 허브 View
   ├─ 단조·강화 작업 View
   ├─ 고객·세계 결과 View
   ├─ 보관함 Overlay 또는 내부 전체 화면 View
   ├─ ResultEnvelope 우선 확인 Overlay
   └─ 설정 Overlay
```

책임 경계:

- 메인 화면은 제품 Shell과 별도 Scene이다.
- 허브·단조·강화는 공통 캠페인 상태를 유지하는 View 전환을 우선한다.
- 보관함·설정은 현재 작업 상태를 보존하는 Overlay 또는 내부 Screen으로 사용한다.
- 비가역 결과는 일반 Toast가 아니라 저장된 `ResultEnvelope`로 표시한다.
- 고객·세계 결과가 큰 배경 연출을 요구하면 Shell 안의 전체 화면 View로 전환할 수 있다.
- 화면 전환이 도메인 객체를 새로 만들거나 결과를 재추첨해서는 안 된다.

## 2. 현재 비주얼 보드의 승인 범위

`BS-VISUAL-20260731-01`과 대화에서 생성한 비주얼 가이드는 **구현 기준 작업안**으로 채택한다.

채택되는 항목:

- 스타일라이즈드 다크 포지
- 별도 메인 화면
- 세로형 모바일 중심 레이아웃
- 단일 제품 Shell과 View·Overlay 혼합
- 장비 중심 정보 위계
- 밝은 불 정령 모닥
- 대장간 허브·강화·보관함·결과 화면의 공통 철·황동 UI 문법

자동으로 승인되지 않는 항목:

- 플레이어 레벨
- 청색 보석 또는 프리미엄 재화
- 업적
- 상점
- 도감·가이드의 상세 기능
- `특수 제작`이라는 별도 신규 시스템
- 보관함 `128/150` 같은 임시 수치
- 시장 거리·경기장의 직접 탐색 플레이
- 이미지 안의 장비 수치·강화 확률·재화량

위 항목은 화면을 채우기 위한 `PLACEHOLDER` 또는 `PROPOSED`로 유지하며 별도 승인 없이 시스템 정본이 되지 않는다.

## 3. 첫 실행·이어하기 계약

### 최초 실행

```text
앱 부팅
→ 로컬 설정 로드
→ 메인 화면
→ 새 게임
→ 캠페인 생성·원자 저장
→ 첫 대장간 진입
```

### 이어하기

```text
앱 부팅
→ 로컬 설정·세이브 메타데이터 로드
→ 메인 화면의 이어하기 활성
→ 이어하기
→ 저장 무결성 확인
→ 미확인 비가역 ResultEnvelope가 있으면 우선 복구
→ 마지막 안전 체크포인트 또는 대장간 허브 진입
```

### 손상·누락

- 세이브가 없으면 이어하기를 비활성화한다.
- 세이브가 손상됐으면 자동으로 새 게임을 시작하지 않는다.
- 복구 스냅샷이 있으면 복구 가능 상태와 영향을 설명한다.
- 복구 스냅샷은 실패 결과를 되돌리는 수단으로 제공하지 않는다.

## 4. Scene 책임 제안

```text
Boot
├─ MainMenuScene                 # BS-MAIN-20260801-01
│  ├─ MainMenuView
│  ├─ SettingsOverlay
│  └─ SaveStatusPanel
└─ BlacksmithApp                 # BS-SHELL-20260801-01
   ├─ AppStateCoordinator
   ├─ SaveCoordinator
   ├─ ScreenRouter
   ├─ ForgeHubView
   ├─ CoreWorkbenchView
   ├─ CustomerAndWorldView
   ├─ StorageViewOrOverlay
   ├─ ResultEnvelope
   └─ CommonUI
```

이는 구현 방향이며 실제 Scene·Node 작성은 사용자 `기획 완료`와 `검수 완료` 이후에만 수행한다.

## 5. 금지 사항

- `project.godot`의 기본 실행 Scene을 테스트 Scene으로 유지한 채 제품 진입이 완료됐다고 표시
- 메인 화면·제품 Shell·PoC가 서로 다른 캠페인 상태를 소유
- 이어하기 버튼이 저장 유무와 무관하게 활성화
- 화면 전환 시 강화·고객·세계 결과를 재판정
- 시안에 등장했다는 이유만으로 신규 재화·상점·업적을 구현
- 메인 메뉴에서 별도 확인 없이 기존 캠페인을 덮어쓰기

## 6. 현재 상태

```text
BS-MAIN-20260801-01: USER_APPROVED
BS-SHELL-20260801-01: USER_APPROVED
BS-VISUAL-20260731-01: USER_ACCEPTED_WORKING_BASELINE
MAIN_MENU_PRODUCT_SCENE: NOT_IMPLEMENTED
PERSISTENT_SAVE_AND_CONTINUE: NOT_IMPLEMENTED
BLACKSMITH_APP_SHELL: NOT_IMPLEMENTED
PRODUCT_ASSET_IMPLEMENTATION: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
