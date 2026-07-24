# Development Gates

## 판정 원칙

- 문서 승인, 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 외부 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `UNVERIFIED`다.
- 과거 PASS 이력은 현재 변경의 회귀 PASS를 대신하지 않는다.
- 프로젝트 코어 확정과 자동 구현 검증은 Production 또는 프로젝트 전체 MVP 완료가 아니다.

## Gate summary

| Gate | 상태 | 증거 | 차단 조건 |
|---|---|---|---|
| Project core confirmation | `PASS` | 사용자 승인, 코어 계약, 5회 적대적 검토 | 코어 재승인 항목 변경 시 재검토 |
| Equipment lifecycle PoC specification | `PASS / SPEC_READY` | 통합 명세, MVP-003 Scope, 구현계획 | 논리·참조·검증 계약 drift |
| Equipment lifecycle PoC implementation | `PASS / IMPLEMENTATION_VALIDATED` | PR validation #468, code head `03c90bb...` | 제품 코드 변경 시 재실행 |
| Lifecycle automated validation | `PASS` | Python, Godot import, Scene smoke, 모델·통합·E2E | 최신 정본 head 재검증·main 회귀 |
| Documentation alignment | `PASS_AT_CODE_HEAD` | core alignment·CI 구조 검사 #468 | 정본 변경 뒤 재실행 |
| Main full validation | `PENDING_MERGE` | 없음 | PR 병합 뒤 matrix·Base suite 실행 |
| Android device | `NOT_RUN` | 없음 | 실제 빌드·기기 증거 필요 |
| Accessibility | `IMPLEMENTED / NOT_REVIEWED` | 정밀 보조·모션 감소·48dp 코드 | 사람·기기 검증 필요 |
| Performance | `NOT_RUN` | 없음 | 대표·최악 장면 측정 필요 |
| External playtest | `NOT_RUN` | 플레이테스트 계약만 존재 | 신규 플레이어 행동 증거 필요 |
| Branch protection | `UNVERIFIED` | 조회 경로 없음 | Required Check 강제 확인 |
| Production greenlight | `BLOCKED` | SWOT·VRIO는 가설 단계 | 플레이·플랫폼·성능 증거 필요 |

## Project core confirmation — PASS

보호 경계:

- 단일 대장장이
- 직접 제작과 영구 완성도
- 일반 강화 버튼 입력당 판정 1회
- `+10` 특수 강화와 수식어 선택
- 판매 장비의 영구 이력과 세계 환류
- 피로도 기반 일일 우선순위와 수동 날짜 진행

재승인 필요:

- 직원·복수 대장장이
- 직접 전투
- 영구 완성도 재추첨
- 판매 장비 기록·세계 환류 제거
- 피로도·날짜 제거
- 자동 단조가 특수 강화와 고위험 판단을 완전히 대체

## Equipment lifecycle PoC specification — PASS / SPEC_READY

책임 원본:

- `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- `docs/MVP-003_SCOPE.md`
- `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- Issue #34

필수 계약:

- 철검 1종·검투사 1명
- +5 납품 또는 +10 추가 도전
- 피로도 20, 50% 이월, 작업 예약 없음
- DEFEAT/WIN/DECISIVE_WIN 도달 가능 반례
- 원자적 골드·재료·피로도·납품 처리
- 영구 장비 기록, 지연 결과, 재방문
- 정밀 입력 대안과 색상 비의존 정보

## Equipment lifecycle PoC implementation — PASS / IMPLEMENTATION_VALIDATED

구현 범위:

- 완성도 데이터·판정기
- 날짜·피로도 모델
- 고객 의뢰·납품
- 세계 장비 Registry·결과 Resolver
- 원자 거래 Controller
- PoC telemetry
- 계약·HUD·제작·강화·보고·재방문 UI
- 기존 Prototype 진입점과 별도 PoC Scene
- 정밀 보조 GOOD 경로·모션 감소
- 전체 생애 E2E와 경계 테스트
- 비용 최적화 CI 구조

코드 기준 head: `03c90bb063103e1c92885e7e21228f963cfe2775`

PR validation #468 증거:

1. Ubuntu Python 문서·CI·데이터·강화·시뮬레이터 계약 PASS
2. Godot 4.7.1 import·parse PASS
3. `main.tscn`·`equipment_lifecycle_poc.tscn` smoke PASS
4. 기존 제작·강화·경제 모델·통합 테스트 PASS
5. 신규 피로도·완성도·고객·세계 기록·telemetry 테스트 PASS
6. 원자 거래·생애 Controller 통합 테스트 PASS
7. 장비 생애 E2E와 세 결과 밴드 경계 PASS

## CI execution — ACTIVE / OPTIMIZED

책임 원본: `docs/CI_EXECUTION_POLICY.md`

- PR `pull_request` 자동 실행 활성화
- 문서 전용 PR: Ubuntu Python 3.12 문서 validator만 실행
- 코드 PR: Ubuntu Python 전체 계약과 Godot 1회 실행
- main/nightly: Ubuntu·Windows Python 매트릭스, Godot 1회, pinned Base suite 1회
- 모든 Workflow에 `concurrency`와 `cancel-in-progress: true`
- reusable Python·Godot Workflow로 중복 실행 방지
- 실패 로그만 artifact 업로드

실제 PR classifier가 코드 범위를 선택하고 Python 1회·Godot 1회를 실행한 것은 #468에서 확인됐다. cancellation과 Required Check 강제 여부는 별도 확인한다.

## Prototype regression — PASS

PR validation #468은 기존 Prototype 회귀를 신규 lifecycle 회귀와 함께 실행했다.

- 제작 모델 7건
- 제작 결과 통합 6건
- EnhancementSession 12건
- WorkshopResources 7건
- 수동 강화 경제 통합 2건

현재 Prototype의 피버 공격력 ×1.05·제작 가치 ×1.03은 한 번만 적용되며 반복 발동 시 중첩되지 않는다. 보통·좋음·완벽에 피버를 적용한 실제 공격력은 21·22·23이다.

실패·보정·위험 책임 원본은 `data/crafting/enhancement_balance.json`, 수식어 이정표 책임 원본은 `data/crafting/enhancement_milestones.json`이다.

## Documentation alignment — PASS_AT_CODE_HEAD

PR validation #468에서 다음이 통과했다.

- core alignment
- CI Workflow 구조
- 프로젝트 운영 감사 wrapper
- lifecycle 데이터 계약
- 기존 제작·강화 문서 계약

이후 상태 문서 동기화 커밋은 최종 PR head에서 다시 검증한다.

## 플랫폼·사람 검증

다음은 코드 또는 설계 적용 대상이지만 실행 증거가 없어 `NOT_RUN`이다.

- Android 세로 화면, 안전 영역, 터치
- 정밀 입력 대안과 모션 감소 실제 사용성
- 색상 비의존 위험·결과 전달
- 장시간 반복 성능·메모리
- 외부 6명 권장 플레이테스트
- PDF와 주요 화면 사람 시각 확인

## 최종 판정 규칙

- 자동 검증 PASS는 MVP-003 코드 구현에 대한 판정이다.
- Android·사람 접근성·외부 플레이 미실행은 프로젝트 전체 MVP PASS가 아니다.
- `main` full-validation은 PR 병합 뒤 별도 확인한다.
- Required Check 강제 여부가 확인되지 않으면 해당 항목은 `UNVERIFIED`로 유지한다.
