# Blacksmith 기존 프로젝트 감사 보완 — 비주얼·에셋·라이선스

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A8`
>
> Decision ID: `BS-VISUAL-ASSET-GOV-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / EXECUTION_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

- 비주얼 보드에는 레벨·청색 재화·업적·상점·특수 제작·128/150·시장/경기장 직접 플레이·임시 수치가 포함돼 있다.
- 그림체와 모닥은 방향 승인됐지만 최종 파일·실제 화면·라이선스·실기기 검증은 없다.
- Sheet 70~72는 방향·생성 Queue·검수 로그이며 실제 Asset Manifest와 License Ledger가 아니다.
- 과거 모닥 `숯 불씨 정령` 표현과 최신 밝은 불 정령 방향이 충돌했다.

## 2. 해결된 기획 목표

`BS-VISUAL-ASSET-GOV-20260801-01`로 다음을 확정했다.

- Placeholder/NOT_CANON 고정 목록
- 에셋 상태 승격 단계
- Asset Manifest·License Ledger 필수 필드
- AI 생성·외부·폰트·오디오 권리 검토 경계
- 모닥 화면별 최대 논리 크기와 정보 비가림 규칙
- 12개 Screenshot Baseline과 해상도·safe inset·text scale 검수
- Manifest 미등록·권리 미검토 에셋의 릴리스 차단

초기 Manifest와 License Ledger를 생성했으며 현재 제품 승인 에셋은 0개다.

## 3. Finding 판정

| Finding | 기획 목표 | 실행·증거 |
|---|---|---|
| `BS-AUD-F10` | RESOLVED | 제품 화면 정리 OPEN |
| `BS-AUD-F23` | 검수 계약 RESOLVED | 실제 모닥 UI·기기 OPEN |
| `BS-AUD-F24` | 구조 RESOLVED | 실제 자산·권리 검토 OPEN |
| `BS-AUD-F25` | 기준 세트 RESOLVED | Screenshot baseline 생성·회귀 OPEN |

Finding 수는 실제 제품 에셋과 검수 증거 전까지 줄이지 않는다.

## 4. 적대적 실패 조건

```text
Placeholder가 승인 시스템처럼 구현됨
대화 생성 이미지가 Manifest 없이 제품에 포함됨
License REVIEW_REQUIRED/BLOCKED 에셋이 릴리스됨
모닥이 장비·확률·비용·정지 이유·ResultEnvelope를 가림
48dp 미달 핵심 터치
색상만으로 핵심 상태 구분
실제 화면 검수 없이 CONCEPT_DIRECTION_APPROVED를 RELEASE_APPROVED로 변경
```

## 5. 상태

```text
VISUAL_ASSET_GOVERNANCE: COMPLETE
INITIAL_MANIFEST: CREATED
INITIAL_LICENSE_LEDGER: CREATED
CROSS_SOURCE_SYNC: PENDING
FINAL_PRODUCT_ASSETS: NOT_RUN
RUNTIME_INTEGRATION: NOT_RUN
DEVICE_VISUAL_REVIEW: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
