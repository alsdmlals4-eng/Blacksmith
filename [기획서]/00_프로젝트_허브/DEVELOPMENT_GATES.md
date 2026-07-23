# Development Gates

## 판정 원칙

- 문서 승인, 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 외부 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `UNVERIFIED`다.
- 과거 PASS 이력은 현재 변경의 회귀 PASS를 대신하지 않는다.
- 프로젝트 코어 확정은 Production 또는 MVP 전체 완료가 아니다.

## Gate summary

| Gate | 상태 | 증거 | 차단 조건 |
|---|---|---|---|
| Project core confirmation | `PASS` | 사용자 승인, 코어 계약, 적대적 검토 | 코어 재승인 항목 변경 시 재검토 |
| Equipment lifecycle PoC specification | `PASS / SPEC_READY` | 통합 명세, MVP-003 Scope, 구현계획 | 논리·참조·검증 계약 drift |
| Equipment lifecycle PoC implementation | `NOT_STARTED` | Issue #34 | 제품 코드·데이터·Scene·테스트 미구현 |
| Prototype regression | `HISTORICAL_PASS / CURRENT_RECHECK_REQUIRED` | MVP-001/002, 과거 Workflow | 최종 PR head 회귀 미통과 |
| Documentation alignment | `IN_PROGRESS` | `check_project_core_alignment.py` Red #391 | Green CI 미확인 |
| Android device | `NOT_RUN` | 없음 | 실제 빌드·기기 증거 필요 |
| Accessibility | `NOT_RUN` | 설계 가드레일만 존재 | 사람·기기 검증 필요 |
| Performance | `NOT_RUN` | 없음 | 대표·최악 장면 측정 필요 |
| External playtest | `NOT_RUN` | 플레이테스트 계약만 존재 | 신규 플레이어 행동 증거 필요 |
| Production greenlight | `BLOCKED` | SWOT·VRIO는 가설 단계 | 구현·플레이·플랫폼 증거 필요 |

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

## Equipment lifecycle PoC implementation — NOT_STARTED

아직 구현되지 않은 항목:

- 완성도 데이터·판정기
- 날짜·피로도 모델
- 고객 의뢰·납품
- 세계 장비 Registry·결과 Resolver
- 원자 거래 Controller
- PoC telemetry
- 계약·HUD·보고 UI
- 전체 생애 E2E와 신규 CI

구현 완료 조건:

1. 철검 제작부터 재방문까지 E2E 완주
2. +5와 +10 양 경로 유효
3. 자원·납품 원자성
4. 세 결과 밴드 반례 도달
5. 영구 기록과 인과 설명
6. 신규·기존 회귀 전체 PASS
7. Godot import·main·PoC Scene smoke PASS
8. 미실행 검증을 PASS로 표기하지 않음

## Prototype regression — HISTORICAL_PASS

현재 구현된 제작·강화·보관·자동 단조는 기존 테스트와 과거 Workflow PASS 이력이 있다. PR #33은 제품 코드를 변경하지 않지만 문서·검사 변경 후 최신 Data/Godot Workflow를 다시 확인한다.

## Documentation alignment — IN_PROGRESS

Red 증거:

- Data validation #391
- 실패 단계: `Validate confirmed project core alignment`
- 검출 대상: stale 시작 문서, 누락된 MVP-003 Scope, 정본·Registry 전파 누락

Green 조건:

- `python tests/check_project_core_alignment.py` PASS
- Data validation 전체 PASS
- Registry source·publication·Manifest 연결 PASS
- PR 본문과 changed files·검증 결과 일치

## 플랫폼·사람 검증

다음은 현재 적용 대상이지만 실행 증거가 없어 `NOT_RUN`이다.

- Android 세로 화면, 안전 영역, 터치
- 정밀 입력 대안과 모션 감소
- 색상 비의존 위험·결과 전달
- 장시간 반복 성능·메모리
- 외부 6명 권장 플레이테스트
- PDF 사람 시각 확인

## 최종 판정 규칙

- 문서·계획 Green만으로 프로젝트 구현 완료를 선언하지 않는다.
- Issue #34 미구현 상태에서는 최종 프로젝트 판정이 `REVISE`보다 높을 수 없다.
- Required Check 강제 여부가 확인되지 않으면 해당 항목은 `UNVERIFIED`로 유지한다.
