# Blacksmith 시작 지점

## 프로젝트 한 문장

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험을 선택하며, 그 장비가 다른 이의 손에서 쌓은 역사를 명성과 다음 의뢰로 돌려받는 모바일 제작 게임.

시장 설명은 다음 문장으로 통일한다.

> 장비를 대량 생산하는 게임이 아니라, 장비의 출생·성장·소유·사건 기록을 제작하는 대장장이 게임.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / CORE_RECORDED` |
| 장비 한 점의 생애 PoC 명세 | `SPEC_READY` |
| 장비 생애 PoC 구현 | `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED` |
| GitHub Actions | `DEFERRED_UNTIL_ACTIONS_AVAILABLE` |
| 프로덕션 진입 | `NOT_GREENLIT` |
| 현재 Issue | #34 |
| 현재 PR | #35 Draft |

현재 Prototype의 제작·강화·보관·자동 단조는 유지된다. PR #35에는 영구 완성도, 피로도·날짜, 검투사 납품, 지연 결과, 세계 장비 기록, 재방문과 세로 PoC Scene이 구현 후보로 추가됐다. 최신 head의 Godot import·Scene·E2E·전체 회귀는 Actions 비용 게이트 때문에 아직 실행되지 않았다.

## 처음 읽을 순서

1. `AGENTS.md`
2. 이 문서
3. `ACTIVE_CONTEXT.md`
4. `DOCUMENTATION_MAP.md`
5. `DEVELOPMENT_GATES.md`
6. `DESIGN_DOCUMENT_REGISTRY.json`
7. `SKILL_REGISTRY.json`
8. `docs/superpowers/specs/2026-07-23-project-core-design.md`
9. `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
10. `docs/MVP-003_SCOPE.md`
11. `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
12. `docs/CI_EXECUTION_POLICY.md`
13. 관련 `data/`, `scripts/`, `scenes/`, `tests/`

## 현행 코어 보호 경계

- 한 명의 대장장이만 운용한다.
- 직접 제작, 영구 완성도, 버튼 입력당 일반 강화 1회 판정을 유지한다.
- `+10`에서 수식어와 장비 정체성을 성장시킨다.
- 판매·납품 장비의 이력과 세계 환류를 보존한다.
- 피로도는 하루 작업량만 제한하며 터치 횟수나 성공 확률을 불리하게 만들지 않는다.
- 날짜는 `하루 마치기`로만 진행하고 작업 예약은 사용하지 않는다.
- 직원, 직접 전투, 생산 대기열, 일상적 수리 관리를 승인 없이 추가하지 않는다.
- `+100`은 현재 제품 목표이며 최종 상한은 후속 실험으로 재검토할 수 있다.

## PR 이력

```text
#31 운영 정본 복구 — merged
→ #32 Base 25 Skill 재동기화 — merged
→ #33 코어 확정·통합 명세·구현계획·최종 검토 — merged
→ #35 MVP-003 구현 후보 — Draft
```

## 검증 상태 읽는 법

- 코드가 작성됐다는 것은 실행 PASS가 아니다.
- 과거 CI 성공은 최신 head의 회귀 PASS를 대신하지 않는다.
- CI 성공도 Android·사람 시각·접근성·성능·플레이 재미 통과를 대신하지 않는다.
- 미실행 검사는 `NOT_RUN`, `UNVERIFIED` 또는 `VALIDATION_DEFERRED`로 유지한다.
- 사용자가 GitHub Actions 사용 가능 상태를 알리면 `docs/CI_EXECUTION_POLICY.md` 순서로 자동 트리거를 복원하고 최신 head를 검증한다.
- MVP 전체 완료는 전체 Godot 회귀, Android·접근성·성능·외부 플레이 행동 증거 뒤 별도 판정한다.
