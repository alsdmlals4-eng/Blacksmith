# Active Context

- 갱신일: 2026-07-24
- Work Mode: `IMPLEMENT → VERIFY_PENDING`
- 현재 브랜치: `agent/implement-equipment-lifecycle-poc`
- 현재 PR: #35 Draft
- 선행 PR: #31·#32·#33 `MERGED`
- 현재 Issue·Goal: #34 `MVP-003: 장비 한 점의 생애 PoC 구현 및 플레이 검증`
- 장비 생애 PoC 통합 상태: `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED`
- GitHub Actions: `DEFERRED_UNTIL_ACTIONS_AVAILABLE`

## 1. 현재 판정

| 영역 | 상태 |
|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / CORE_RECORDED` |
| 장비 생애 PoC 통합 명세 | `SPEC_READY` |
| 장비 생애 PoC 구현 | `IMPLEMENTATION_CANDIDATE` |
| 최신 head 자동 검증 | `NOT_RUN / VALIDATION_DEFERRED` |
| 과거 Prototype 자동 검증 | Data #452 PASS, Godot #379 PASS |
| Android 실기기 | `NOT_RUN` |
| 접근성 사람 검토 | `NOT_RUN` |
| 성능 | `NOT_RUN` |
| 외부 플레이테스트 | `NOT_RUN` |
| Production | `NOT_GREENLIT` |

과거 #452/#379는 lifecycle 도메인 계층 일부까지의 증거다. 이후 UI·E2E·CI 최적화·정본 변경이 추가됐으므로 최신 head PASS를 대신하지 않는다.

## 2. 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량으로 장비 한 점을 직접 만들고, 강화 위험과 `+10` 수식어 선택으로 운명을 정한 뒤, 그 장비가 다른 이의 손에서 쌓은 역사를 명성과 다음 의뢰로 돌려받는 모바일 제작 게임.

보호 대상:

- 직접 제작과 빠른 터치 피드백
- 영구 완성도
- 일반 강화 버튼 입력당 결과 1회
- `+10` 특수 강화와 수식어 선택
- 판매·납품 장비의 영구 기록과 세계 환류
- 한 명의 대장장이, 피로도 기반 일일 우선순위
- 수동 날짜 진행과 잔여 피로도 50% 이월

제외:

- 직원·복수 대장장이
- 직접 전투
- 작업 예약·생산 대기열
- 일상적 수리 관리
- 터치당 피로도
- 실시간 전체 세계 시뮬레이션

중요 장비의 선택형 복원은 승인된 후속 기획이며 첫 PoC에서는 제외한다.

## 3. 기존 Prototype 구현 사실

현재 실행 배지: `POC v0.6.4 · main · 2026.07.23.1`

기존 코드·데이터·Scene·테스트가 지원하는 범위:

- 철검 제작, 자동 작업, 광클 피버, 제작 정밀 마감
- 일반 강화와 `+10` 단위 특수 강화
- 최대 +100 목표, 수식어 성장
- +11 하락, +30 파괴, 실패 보정
- 균형·안정·폭주 단조
- 공유 골드·재료 거래
- 보관함과 자동 단조

기존 제작 검증 기준:

- 제작 모델 7건
- 제작 결과 통합 6건
- 보통·좋음·완벽 기본 공격력 20·21·22
- 피버 적용 공격력 21·22·23
- 피버 공격력 ×1.05·제작 가치 ×1.03, 반복 비중첩

## 4. PR #35 구현 후보

작성된 제품 코드·데이터·Scene·테스트:

- lifecycle JSON 4종과 독립 validator
- 영구 완성도 5등급과 정밀 결과 분리
- legacy `quality_*`·AUTO 기록 변환
- 피로도 20, 작업비, 수동 날짜와 50% 이월
- 검투사 계약·+5/+10 판단·적합도 근거
- DEFEAT/WIN/DECISIVE_WIN 결정적 결과
- 영구 장비 Registry와 활동 상한 6
- 제작·강화·납품 원자 거래와 중복 재시도 방지
- 지연 보고·명성·관계·같은 검투사 재방문
- 네트워크 없는 로컬 telemetry
- 기존 Prototype 진입 버튼과 별도 세로 PoC Scene
- 정밀 보조 GOOD 경로·느린 포인터·48dp 입력
- 장비 생애 E2E와 경계 테스트

## 5. CI 비용 게이트

자동 PR, `main` push, nightly 트리거는 사용자가 Actions 사용 가능 상태를 알릴 때까지 중지한다.

최적화 구조:

- 문서 전용: Ubuntu Python 3.12 + 문서 validator
- 코드 PR: Ubuntu Python 전체 계약 + Ubuntu Godot 1회
- main/nightly: Ubuntu·Windows × Python 3.11·3.12·3.13, Godot 1회, pinned Base 전체 suite 1회
- 모든 Workflow `concurrency`와 `cancel-in-progress: true`
- Python·Godot reusable Workflow 사용
- 실패 로그만 artifact 업로드

책임 원본: `docs/CI_EXECUTION_POLICY.md`

## 6. 현행 책임 원본

- 코어: `docs/superpowers/specs/2026-07-23-project-core-design.md`
- 통합 명세: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- MVP Scope: `docs/MVP-003_SCOPE.md`
- 구현계획: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- CI 정책: `docs/CI_EXECUTION_POLICY.md`
- 통합 게임 기획: `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- 상태·게이트: 이 문서, `ROADMAP.md`, `DEVELOPMENT_GATES.md`

## 7. Actions 사용 가능 후 다음 작업

1. PR 자동 검증 트리거 복원
2. 최신 head Python 계약 실행
3. Godot 4.7.1 import·main/PoC Scene smoke 실행
4. 신규·기존 모델·통합·E2E 전체 실행
5. 실패 수정과 재실행
6. Windows Python 매트릭스와 cancellation 확인
7. 실제 check 이름으로 Branch protection 갱신
8. 코드 리뷰 후 PR #35 병합 판정

## 8. 완료 금지 조건

다음이 남아 있으면 프로젝트 구현 또는 MVP 완료로 선언하지 않는다.

- 최신 head 전체 자동 회귀 `NOT_RUN`
- Android·접근성·성능·외부 플레이 `NOT_RUN`
- Branch protection Required Check 강제 상태 `UNVERIFIED`
- PR #35 미병합
- 사람이 PDF를 포함한 주요 화면·문서 실제 열람 `NOT_RUN`
