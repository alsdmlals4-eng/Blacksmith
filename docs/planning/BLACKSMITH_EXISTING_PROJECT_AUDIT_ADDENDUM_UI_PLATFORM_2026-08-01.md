# Blacksmith 기존 프로젝트 감사 보완 — UI Theme·접근성·Android

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A9`
>
> Decision ID: `BS-UI-PLATFORM-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

- 주요 UI가 GDScript에서 런타임 조립된다.
- 공통 Theme Resource·재사용 UI Scene 경계가 없다.
- 고정 폭·오프셋과 720×1280 단일 화면 전제가 강하다.
- 설정은 제한적이며 캠페인과 분리된 영속 저장이 없다.
- Android 뒤로가기·safe area·pause/resume/process death 계약과 실기기 증거가 없다.
- 접근성 보조는 일부 PoC에 있으나 공통 Coordinator와 제품 검증 기준이 없다.

## 2. 해결된 기획 목표

`BS-UI-PLATFORM-20260801-01`로 다음을 확정했다.

- SafeAreaRoot와 Theme·Accessibility·Settings·Lifecycle·Input Coordinator
- Theme token과 공통 UI Scene
- 360×640~1080×2400·tablet portrait fixture
- 48×48 논리 px 터치·긴 한국어·텍스트 1.0/1.15/1.30
- 색상 외 상태·focus 복구·transition 입력 잠금
- settings.cfg와 손상 복구
- reduced motion·precision assist의 판정 불변
- Android back 우선순위
- 이벤트 원자 저장 우선·pause best-effort·pause callback 없는 process death 복구

## 3. Finding 판정

| Finding | 기획 목표 | 런타임·기기·사람 |
|---|---|---|
| `BS-AUD-F13` | RESOLVED | OPEN |
| `BS-AUD-F14` | RESOLVED | OPEN |
| `BS-AUD-F15` | RESOLVED | OPEN |
| `BS-AUD-F16` | RESOLVED | OPEN |

P1 Finding 수는 실제 Theme·Scene·설정·Android 기기·접근성 검증 전까지 유지한다.

## 4. 적대적 실패 조건

```text
화면별 Theme·색·간격·폰트 하드코딩
48px 미달 핵심 입력
cutout/gesture inset 위 CTA
텍스트 확대 시 수치·정지 이유·결과 생략
색상만으로 성공·하락·파괴 표현
back 입력 이중 처리
ResultEnvelope를 back으로 무확인 폐기
pause callback을 유일한 저장 수단으로 사용
reduced motion·precision assist가 확률·판정을 변경
설정 손상이 캠페인 손상으로 전파
```

## 5. 상태

```text
UI_PLATFORM_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
THEME_SCENES_SETTINGS_RUNTIME: NOT_RUN
ANDROID_DEVICE_TEST: NOT_RUN
ACCESSIBILITY_HUMAN_REVIEW: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
