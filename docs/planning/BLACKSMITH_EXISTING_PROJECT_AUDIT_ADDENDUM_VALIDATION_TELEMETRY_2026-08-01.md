# Blacksmith 기존 프로젝트 감사 보완 — 검증·증거·텔레메트리

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A12`
>
> Decision ID: `BS-VALIDATION-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / EXECUTION_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

- 기존 CI와 tests README는 구형 PoC 계약을 강하게 보호한다.
- 과거 PASS가 최신 v9 Save·Migration·Customer·Auto Enhance·Storage·UI의 PASS처럼 오인될 수 있다.
- 테스트 파일 존재, CI 실행, 실제 Scene, Android, 접근성, 외부 플레이의 증거 단계가 분리돼 있지 않다.
- 메인·복구·+50·고객·자동 강화·연대기 이해도를 확인하는 텔레메트리가 없다.

## 2. 해결된 기획 목표

`BS-VALIDATION-20260801-01`로 다음을 확정했다.

- E0~E8 증거 성숙도
- Static·Unit·Transaction·Product Flow·Rendered UI·Android·Human Lane
- 과거 PoC 증거의 `HISTORICAL_POC_BASELINE` 격리
- Decision→validator→test→device/human 추적
- 결정론적 Fixture Registry
- 동일 PR head required CI와 수동/기기 Gate 분리
- 증거 보고서 필수 필드
- 네트워크 전송 없는 로컬·비식별·수동 내보내기 텔레메트리
- 개인정보·안정 기기 ID·자유문·전체 save 수집 금지

## 3. Finding 판정

| Finding | 기획 목표 | 실행·증거 |
|---|---|---|
| `BS-AUD-F20` | RESOLVED | 최신 v9 validator·fixture·CI OPEN |
| `BS-AUD-F26` | RESOLVED | local telemetry 구현·playtest OPEN |

P1/P2 Finding 수는 실제 실행 증거 전까지 유지한다.

## 4. 적대적 실패 조건

```text
다른 commit의 CI PASS를 현재 head PASS로 사용
테스트 파일 존재를 실행 PASS로 표시
Android·접근성·사람 검증을 자동 테스트로 대체
구형 PoC PASS를 최신 v9 PASS로 재사용
validator NOT_RUN인데 operating/product PASS 표시
안정 기기 ID·개인정보·자유문·전체 save 수집
일반 릴리스에서 동의 없이 로컬 텔레메트리 활성
네트워크 자동 업로드
결과 재추첨을 텔레메트리 분석용으로 허용
```

## 5. 상태

```text
VALIDATION_EVIDENCE_DESIGN: COMPLETE
LOCAL_TELEMETRY_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
CURRENT_V9_CI: NOT_RUN
ANDROID_DEVICE: NOT_RUN
ACCESSIBILITY_HUMAN: NOT_RUN
EXTERNAL_PLAYTEST: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
