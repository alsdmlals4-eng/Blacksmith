# Development Gates

## 판정 원칙

- 문서 승인, 구현 작성, 자동 테스트 실행, 실제 렌더, Android, 접근성, 성능, 외부 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN`, `UNVERIFIED` 또는 `VALIDATION_DEFERRED`다.
- 과거 PASS 이력은 현재 변경의 회귀 PASS를 대신하지 않는다.
- 프로젝트 코어 확정은 Production 또는 MVP 전체 완료가 아니다.

## Gate summary

| Gate | 상태 | 증거 | 차단 조건 |
|---|---|---|---|
| Project core confirmation | `PASS` | 사용자 승인, 코어 계약, 5회 적대적 검토 | 코어 재승인 항목 변경 시 재검토 |
| Equipment lifecycle PoC specification | `PASS / SPEC_READY` | 통합 명세, MVP-003 Scope, 구현계획 | 논리·참조·검증 계약 drift |
| Equipment lifecycle PoC implementation | `IMPLEMENTATION_CANDIDATE` | PR #35 코드·데이터·Scene·테스트 | 최신 head 실행 증거 없음 |
| Lifecycle automated validation | `VALIDATION_DEFERRED` | Actions 비용 게이트 | Python·Godot·E2E 전체 실행 필요 |
| Prototype regression | `HISTORICAL_PASS_ONLY` | Data #452, Godot #379 | 이후 변경 포함 재실행 필요 |
| Documentation alignment | `CANDIDATE` | 정본 동기화·core alignment 검사 갱신 | 최신 정적 검사 실행 필요 |
| Android device | `NOT_RUN` | 없음 | 실제 빌드·기기 증거 필요 |
| Accessibility | `IMPLEMENTED / NOT_REVIEWED` | 정밀 보조·모션 감소·48dp 코드 | 사람·기기 검증 필요 |
| Performance | `NOT_RUN` | 없음 | 대표·최악 장면 측정 필요 |
| External playtest | `NOT_RUN` | 플레이테스트 계약만 존재 | 신규 플레이어 행동 증거 필요 |
| Production greenlight | `BLOCKED` | SWOT·VRIO는 가설 단계 | 구현 검증·플레이·플랫폼 증거 필요 |

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

## Equipment lifecycle PoC implementation — IMPLEMENTATION_CANDIDATE

PR #35에 작성된 항목:

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

구현 완료 판정 조건:

1. 철검 제작부터 재방문까지 E2E 실행 PASS
2. +5와 +10 양 경로 유효
3. 자원·납품 원자성 PASS
4. 세 결과 밴드 반례 PASS
5. 영구 기록과 인과 설명 확인
6. 신규·기존 회귀 전체 PASS
7. Godot import·main·PoC Scene smoke PASS
8. 미실행 검증을 PASS로 표기하지 않음

현재는 코드 작성 완료 후보이며 위 실행 증거가 없으므로 `PASS`가 아니다.

## CI 비용 게이트 — VALIDATION_DEFERRED

책임 원본: `docs/CI_EXECUTION_POLICY.md`

- 자동 `pull_request`, `main` push, nightly 실행 중지
- 문서 전용 PR은 Ubuntu Python 3.12 문서 validator만 실행하도록 설계
- 코드 PR은 Ubuntu Python 계약과 Godot 1회만 실행하도록 설계
- main/nightly는 Ubuntu·Windows Python 매트릭스와 Godot·Base suite를 분리
- 모든 Workflow에 `concurrency`와 `cancel-in-progress: true`
- reusable Python·Godot Workflow로 중복 실행 방지
- 실패 로그만 artifact 업로드

실제 이벤트 라우팅·Windows·cancellation·Required Check는 Actions 사용 가능 후 검증한다.

## Prototype regression — HISTORICAL_PASS_ONLY

과거 기준선:

- Data validation #452 PASS
- Godot validation #379 PASS
- 제작 모델 7건
- 제작 결과 통합 6건
- EnhancementSession 12건
- WorkshopResources 7건
- 수동 강화 경제 통합 2건

현재 Prototype의 피버 공격력 ×1.05·제작 가치 ×1.03은 한 번만 적용되며 반복 발동 시 중첩되지 않는다. 보통·좋음·완벽에 피버를 적용한 실제 공격력은 21·22·23이다.

이후 lifecycle UI·E2E·Workflow 변경이 추가됐으므로 위 이력은 최신 head 회귀 PASS가 아니다.

## Documentation alignment — CANDIDATE

동기화 대상:

- README
- START_HERE
- ACTIVE_CONTEXT
- ROADMAP
- DEVELOPMENT_GATES
- BLACKSMITH_GAME_BIBLE
- MVP-003 Scope
- CI 실행 정책
- core alignment 정적 계약

최신 정적 검사 실행 전까지 `PASS`로 올리지 않는다.

## 플랫폼·사람 검증

다음은 코드 또는 설계 적용 대상이지만 실행 증거가 없어 `NOT_RUN`이다.

- Android 세로 화면, 안전 영역, 터치
- 정밀 입력 대안과 모션 감소
- 색상 비의존 위험·결과 전달
- 장시간 반복 성능·메모리
- 외부 6명 권장 플레이테스트
- PDF와 주요 화면 사람 시각 확인

## 최종 판정 규칙

- 코드 작성만으로 프로젝트 구현 완료를 선언하지 않는다.
- 최신 head 전체 회귀 전에는 MVP-003을 PASS로 올리지 않는다.
- Android·사람 접근성·외부 플레이 미실행은 PASS가 아니다.
- Required Check 강제 여부가 확인되지 않으면 해당 항목은 `UNVERIFIED`로 유지한다.
