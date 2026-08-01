# Blacksmith UI Theme·접근성·Android 생명주기 승인 정본

> Decision ID: `BS-UI-PLATFORM-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-MAIN-20260801-01`, `BS-SHELL-20260801-01`, `BS-SAVE-20260801-01`, `BS-VISUAL-ASSET-GOV-20260801-01`

## 1. 목적

현재 GDScript 런타임 조립 UI와 고정 폭·오프셋을 제품용 공통 Theme·재사용 Scene·안전 영역·설정·Android 생명주기 구조로 전환한다. 시각적 일관성보다 먼저 정보 손실·입력 오작동·상태 손실·접근성 회귀를 차단한다.

## 2. UI 책임 구조

```text
BlacksmithApp
├─ SafeAreaRoot
│  ├─ AppChrome
│  ├─ ScreenRouterViewport
│  ├─ GlobalOverlayLayer
│  └─ SystemFeedbackLayer
├─ UIThemeCoordinator
├─ AccessibilityCoordinator
├─ SettingsCoordinator
├─ AndroidLifecycleCoordinator
└─ InputNavigationCoordinator
```

### 책임

- `SafeAreaRoot`: viewport·cutout·gesture inset을 반영한 실제 콘텐츠 영역 제공
- `UIThemeCoordinator`: Theme Resource와 상태 variant 적용
- `AccessibilityCoordinator`: 텍스트 크기·모션 감소·정밀 보조·색상 외 상태 표현
- `SettingsCoordinator`: `settings.cfg` 로드·검증·저장·기본값 복구
- `AndroidLifecycleCoordinator`: pause/resume/focus/back 이벤트를 AppState·SaveCoordinator에 전달
- `InputNavigationCoordinator`: 터치·키보드·게임패드 포커스와 Android 뒤로가기 우선순위
- 각 화면은 자체 Theme·저장 파일·back 정책을 만들지 않는다.

## 3. Theme Resource 구조

```text
assets/ui/theme/
├─ blacksmith_theme.tres
├─ typography.tres
├─ colors.tres
├─ spacing.tres
├─ control_sizes.tres
├─ panels/
├─ buttons/
├─ cards/
├─ progress/
└─ icons/
```

### 공통 토큰

- 배경·표면·철·황동·화로 강조·위험·성공·정보·비활성
- 제목·본문·보조·수치·경고·버튼 typography
- 4/8 기반 spacing scale
- 최소 터치 크기 48×48 논리 px
- 화면 가장자리 safe padding
- panel·card·modal·toast·tooltip·ResultEnvelope style variants

### 금지

- 화면별로 같은 역할의 색·간격·폰트 값을 직접 하드코딩
- `_draw()` 또는 runtime StyleBox 생성으로 제품 주요 UI를 전부 구성
- 색상 하나만으로 성공·실패·위험·선택 상태 표현
- 상태마다 글자 크기·버튼 높이가 임의로 달라짐

## 4. 재사용 UI Scene

최소 공통 Scene:

```text
AppChrome
TopStatusBar
EquipmentHeroPanel
ResourceSummaryBar
PrimaryActionBar
SecondaryActionRow
InformationCard
RiskBreakdownPanel
CustomerCard
EquipmentCard
ChronologyEntry
ModalSheet
ConfirmationDialog
ToastMessage
BlockingErrorPanel
ResultEnvelopeOverlay
SaveStatusPanel
SettingsOverlay
LoadingAndSaveIndicator
```

각 Scene은 입력 데이터와 Signal 계약만 가지며 도메인 결과를 계산하지 않는다.

## 5. 화면·반응형 기준

### 논리 기준

- 기준 viewport: 720×1280 portrait
- content scale: `canvas_items / expand` 유지
- 최소 지원 논리 영역: 360×640 상당
- 1080×2400 장형 Android와 태블릿 portrait를 별도 fixture로 검증
- landscape는 제품 플레이 범위에서 지원하지 않으며 회전 잠금을 사용한다.

### 레이아웃 원칙

```text
SafeAreaRoot
→ 고정 폭 대신 anchor/container
→ 장비·핵심 상태 우선
→ 하단 PrimaryActionBar
→ 상세는 scroll/expand
```

- 핵심 CTA는 하단 gesture inset 위에 배치한다.
- 긴 한국어 문자열과 텍스트 확대에서 잘림 대신 reflow·scroll을 사용한다.
- 고정 `672px` 같은 값은 최대 폭 token으로만 사용할 수 있고 화면 absolute 위치로 사용하지 않는다.
- modal은 가로·세로 inset을 모두 지키며 키보드가 표시돼도 CTA 접근 가능해야 한다.

## 6. 터치·포커스·입력

- 핵심 터치 영역 최소 48×48 논리 px
- 인접 위험 버튼 간 최소 8px 간격
- 비가역 CTA는 결과가 드러나는 동사형 문구 사용
- 버튼 비활성은 색상+아이콘/문구+접근성 설명을 제공
- 키보드·게임패드 focus order는 시각 순서와 일치
- Overlay 종료 시 이전 control focus 복구
- transition 중 중복 입력 잠금
- 장시간 누르기·복잡 제스처를 필수 행동으로 사용하지 않음

## 7. 텍스트 크기

설정 단계:

| ID | 배율 | 용도 |
|---|---:|---|
| `NORMAL` | 1.00 | 기본 |
| `LARGE` | 1.15 | 확대 |
| `EXTRA_LARGE` | 1.30 | 최대 제품 지원 |

- 폰트 크기만 확대하지 않고 line height·button/card min size·scroll 영역을 같이 갱신한다.
- 수치·확률·정지 이유·결과 변화는 최대 단계에서도 생략하지 않는다.
- 한 줄 고정 대신 wrapping을 기본으로 한다.
- 비정상적인 overflow가 발생하면 화면을 축소하지 않고 scroll 또는 계층 재배치한다.

## 8. 색상·상태·대비

핵심 상태는 항상 두 가지 이상으로 표현한다.

```text
색상 + 텍스트
색상 + 아이콘
색상 + 패턴/테두리
```

예:

- 성공: 녹색 계열 + `성공` + 체크
- 하락: 주황 계열 + `단계 하락` + 아래 화살표
- 파괴: 적색 계열 + `영구 파괴` + 파손 아이콘
- 선택 필요: 황동 강조 + `선택 필요` + 손/분기 아이콘

실제 대비 수치는 최종 폰트·배경 에셋에서 측정하고 증거를 남긴다. 방향 승인만으로 대비 PASS를 주장하지 않는다.

## 9. 설정 계약

`settings.cfg`에 저장:

```text
music_volume
sfx_volume
vibration_enabled
reduced_motion
precision_assist
text_size
extra_status_labels
```

### 기본값

| 설정 | 기본 |
|---|---|
| 음악 | 80% |
| 효과음 | 100% |
| 진동 | 켜짐 |
| 모션 감소 | 꺼짐 |
| 정밀 보조 | 꺼짐 |
| 텍스트 크기 | NORMAL |
| 추가 상태 문구 | 켜짐 |

- 설정은 변경 즉시 적용하고 짧은 debounce 후 저장한다.
- 캠페인 저장과 분리한다.
- 설정 손상은 기본값 복구 후 한 번 알리고 캠페인에 영향을 주지 않는다.
- 음량은 0~100 UI를 사용하고 내부 값은 0.0~1.0으로 정규화한다.
- 진동이 지원되지 않는 기기에서는 설정을 숨기거나 지원 불가 문구를 표시한다.

## 10. 모션 감소

`reduced_motion=true`에서:

- 화면 transition 시간 50% 이하 또는 즉시 전환
- 반복 불꽃·흔들림·화면 확대·강한 hit shake 제거
- 의미 전달에 필요한 결과 변화는 fade·텍스트·아이콘으로 유지
- 모닥 idle 빈도·이동량 감소
- 입력 완료를 기다리는 장식 animation 금지

모션 감소가 게임 판정·정밀 성공 범위·강화 확률을 변경하지 않는다.

## 11. 정밀 보조

- target 영역 대비 강화
- 이동 속도 완화 또는 시각 표식 확대
- 진동·소리 cue 제공 가능
- 플레이어 입력은 유지
- 자동 PERFECT·자동 정밀 완료·확률 직접 상승 금지
- 보조 사용 여부는 결과 화면에서 불필요하게 낙인찍지 않는다.

## 12. Android 뒤로가기 우선순위

```text
1. OS permission/system dialog는 OS가 처리
2. Blocking error·confirmation dialog
3. ResultEnvelope: 확인 완료 전 임의 dismiss 금지
4. Settings·Storage·Customer detail 등 Overlay 닫기
5. 내부 View의 하위 detail → 상위 View
6. 작업 중 화면 → 허브 복귀 확인 또는 안전 복귀
7. BlacksmithApp 허브 → 메인 화면 복귀 확인
8. 메인 화면 → 별도 종료 버튼 없음; Android 시스템 동작 사용
```

- 같은 back 입력을 두 화면이 동시에 처리하지 않는다.
- 저장·transition 중 back 연타는 한 요청으로 병합한다.
- 비가역 작업의 PREPARED/RESOLVED 사이에는 결과를 취소하지 않고 저장 복구 계약을 따른다.

## 13. Android pause·resume·process death

### 원칙

이벤트 단위 원자 저장이 주 보호 수단이며 pause 저장은 보조 수단이다.

```text
비가역 행동 전 PREPARED 저장
→ 결과 APPLIED 저장
→ pause 시 마지막 dirty state best-effort flush
```

### pause

- 새 비가역 행동 시작 차단
- 진행 중 저장 요청을 짧게 완료하거나 현재 정상 revision 유지
- dirty한 안전 상태가 있으면 저장 요청
- UI animation·timer·audio pause
- pause 완료를 기다리며 긴 작업·압축·네트워크 수행 금지

### resume

- AppState와 저장 revision 일치 확인
- 미확인 ResultEnvelope 우선 처리
- PREPARED Intent 복구
- 화면 focus·audio·timer 복구
- safe area와 viewport 재조회

### process death

- 메모리 상태에 의존하지 않는다.
- 재실행은 Boot→SaveStatus→primary/backup/migration→ResultEnvelope/Intent→last safe view 순서다.
- pause callback이 호출되지 않는 종료도 이벤트 저장으로 복구돼야 한다.

## 14. 저장 표시

- 일반 자동 저장은 방해하지 않는 작은 indicator 사용
- 저장 실패·복구 필요·마이그레이션 실패는 BlockingErrorPanel 사용
- `저장됨`은 실제 검증된 revision 이후에만 표시
- spinner가 사라졌다는 이유로 저장 성공을 추정하지 않는다.

## 15. 접근성·상태 설명

- 아이콘에 tooltip/accessible label 제공
- 수치 변화는 이전→이후와 원인을 표시
- 확률은 퍼센트와 결과 범주를 함께 표시
- 선택 비활성 이유를 즉시 확인 가능
- 시간 제한이 있는 UX를 핵심 판단에 사용하지 않는다.
- 모닥 반응만으로 상태를 전달하지 않는다.

## 16. 테스트 매트릭스

### 자동·Scene

1. Theme token 누락·직접 하드코딩 validator
2. 공통 Scene 최소 크기·focus order
3. 360×640, 720×1280, 1080×2400, tablet portrait fixture
4. safe inset top/bottom/left/right
5. text size 1.0/1.15/1.30 긴 한국어
6. 터치 48px·위험 버튼 간격
7. color-independent state snapshots
8. Overlay focus restore·중복 입력 잠금
9. settings round trip·손상 복구
10. reduced motion에서 판정 불변
11. precision assist에서 자동 PERFECT 0
12. back priority 모든 계층
13. pause 중 새 비가역 행동 0
14. pause callback 없이 process death 복구
15. 저장 실패 indicator 오표기 0

### Android 실기기

- notch·gesture navigation·3-button navigation
- 저사양/중간/대표 기기
- 홈 이동·앱 전환·화면 잠금·전화/알림 interruption
- process kill 후 ResultEnvelope·Intent 복구
- vibration 지원/미지원
- 오디오 focus 상실·복귀
- 폴더블/태블릿 portrait 가능한 범위

### 사람 검증

최소 6명:

- 3초 내 주요 CTA와 현재 장비 상태 이해
- 확대 텍스트에서 정보 누락 없음
- back 동작 예측 가능
- 저장 중·저장 실패·복구 상태 이해
- 모션 감소·정밀 보조 효과 이해

## 17. 감사 판정

```text
BS-AUD-F13_THEME_SCENE_TARGET: RESOLVED
BS-AUD-F14_SAFE_AREA_TARGET: RESOLVED
BS-AUD-F15_SETTINGS_TARGET: RESOLVED
BS-AUD-F16_ANDROID_LIFECYCLE_TARGET: RESOLVED
RUNTIME_THEME_SCENES_SETTINGS: NOT_RUN
ANDROID_DEVICE_TEST: NOT_RUN
ACCESSIBILITY_HUMAN_REVIEW: NOT_RUN
P1_FINDING_COUNT: 유지
```

## 18. 현재 Gate

```text
THEME_RESOURCE_CONTRACT: APPROVED
REUSABLE_UI_SCENES: APPROVED
SAFE_AREA_AND_RESPONSIVE: APPROVED
TEXT_SCALE: APPROVED
SETTINGS_PERSISTENCE: APPROVED
REDUCED_MOTION: APPROVED
PRECISION_ASSIST_BOUNDARY: APPROVED
ANDROID_BACK_PRIORITY: APPROVED
PAUSE_RESUME_PROCESS_DEATH: APPROVED
PRODUCT_UI_CODE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
