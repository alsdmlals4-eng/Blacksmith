# Blacksmith 시작 지점

> 상태: `PLANNING_REMEDIATION_IN_PROGRESS / NOT_READY_FOR_기획_완료`
>
> 갱신일: `2026-08-01`
>
> 현재 추적: Issue #79 / Draft PR #81
>
> 제품 구현 권한: `BLOCKED`

## 프로젝트 한 문장

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험을 선택하며, 그 장비가 다른 이의 손에서 쌓은 역사를 명성과 다음 의뢰로 돌려받는 Android 세로형 제작 게임.

시장 설명:

> 장비를 대량 생산하는 게임이 아니라, 장비의 출생·성장·소유·사건 기록을 제작하는 대장장이 게임.

## 현재 상태

| 영역 | 상태 |
|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / KEEP` |
| 현행 승인 결정 | `CURRENT_CONFIRMED_DECISIONS.md` |
| 비주얼 방향 | `USER_APPROVED / WORKING_BASELINE` |
| 제작 등급 | `보통→우수→명품→걸작→전설` |
| 세이브·이어하기·ResultEnvelope | `DESIGN_AND_PLAN_COMPLETE / RUNTIME_OPEN` |
| v9 데이터 마이그레이션 | `DESIGN_AND_PLAN_COMPLETE / RUNTIME_OPEN` |
| Base 구조 분석 | `COMPLETE / ADAPTER_MIGRATION_REQUIRED` |
| 기존 프로젝트 감사 | `PASS2_COMPLETE / REMEDIATION_IN_PROGRESS` |
| 제품 기획 Finding | `P0 10 / P1 10 / P2 6` |
| 제품 main Scene | 구형 강화 테스트 Scene |
| Android·사람·성능 | `NOT_RUN` |
| 사용자 기획 완료 | `NOT_DECLARED` |
| Codex 구현 | `BLOCKED` |

과거 장비 생애 PoC 구현·CI PASS 이력은 보존하지만 현재 제품 정본과 동일하지 않다. 최신 기획과 실제 코드·데이터가 충돌하는 항목은 `CANON_CONFLICT`로 관리한다.

## 처음 읽을 순서

1. `AGENTS.md`
2. 이 문서
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `ACTIVE_CONTEXT.md`
5. `DOCUMENTATION_MAP.md`
6. `DEVELOPMENT_GATES.md`
7. `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md`
8. `docs/planning/BLACKSMITH_FULL_GITHUB_SHEET_ADVERSARIAL_REVIEW_2026-08-01.md`
9. `docs/planning/BLACKSMITH_BASE_CURRENT_SKILLS_AND_WORKFLOW_ANALYSIS_2026-08-01.md`
10. 분야별 승인 정본 Markdown·JSON
11. `DESIGN_DOCUMENT_REGISTRY.json`
12. `SKILL_REGISTRY.json`
13. 실제 `project.godot`, `data/`, `scripts/`, `scenes/`, `tests/`

## 현재 핵심 승인

- 그림체: 스타일라이즈드 다크 포지
- 모닥: 밝은 불 정령, C안 표정, 숯 껍질 없음
- 앱 진입: 별도 메인 화면
- 제품 구조: 단일 `BlacksmithApp` + View·Overlay
- 제작 등급: 보통·우수·명품·걸작·전설
- 작품 정체성: 계보 1개 + 보조 최대 2개
- +49→+50: 일반 정밀강화 / 고위 정밀강화
- 고객: 수집가·모험가·검투사·군인 4유형 × 유형별 복수 이름 고객
- 저장: 단일 캠페인 + 자동 백업 2개
- 비가역 결과: AttemptIntent + ResultEnvelope

세부 규칙과 대체 결정은 `CURRENT_CONFIRMED_DECISIONS.md`와 승인 결정 인덱스를 따른다.

## 현재 구현 사실

- `project.godot` 기본 실행은 `res://scenes/test/enhancement_test.tscn`이다.
- 기존 제작·강화·6칸 보관함·자동 단조·카일 검투사 PoC가 존재한다.
- 구형 제작 등급 5 ID와 수식어 3슬롯·10단위 특수 강화 데이터가 존재한다.
- SaveCoordinator·AppStateCoordinator·제품 메인·공통 ResultEnvelope는 없다.
- 기존 자동 테스트와 CI는 구형 PoC 계약을 보호한다.

이 구현은 폐기 대상이 아니라 마이그레이션·책임 분리 대상이다.

## 다음 작업 순서

```text
정본·Sheet 정합성 수정
→ Base v9.3 adapter migration 준비
→ 고객 4유형 공통 계약
→ 자동 단조 정지 경계
→ 비주얼 Placeholder·Asset/License 구조
→ Theme·안전 영역·설정·Android lifecycle
→ 최신 validator·fixture·E2E 계획
→ 적대적 검토 Pass 3
```

## 완료 금지 조건

다음이 남아 있으면 기획 완료·검수 완료·제품 구현 Ready를 선언하지 않는다.

- P0/P1 기획 Finding
- Base adapter·protected baseline·Sheet binding 충돌
- 최신 v9 데이터·고객·자동 단조 계약 미정
- 제품 코드와 승인 정본의 미해결 충돌
- Android·접근성·성능·외부 플레이 `NOT_RUN`
- 최신 head의 자동 검증 증거 부재
