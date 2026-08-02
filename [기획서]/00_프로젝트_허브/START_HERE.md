# Blacksmith 시작 지점

## 프로젝트 약속

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

## 현재 상태

```yaml
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
R1_STATUS: CORE_CONFLICTS_RESOLVED / CANON_ALIGNMENT_AND_PR_AUDIT
MAIN_SHA: b3a852cbb35de73a4b2da32151f845ddd61e1921
LAST_MERGED_PR: 93
CURRENT_AUTHORITY_PR: 94
PRODUCT_IMPLEMENTATION: BLOCKED
HALL_OF_FAME: FUTURE_CONTENT_HOLD_NONCOMPETITIVE_ARCHIVE
```

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
4. `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. 배치별 승인 정본과 Core Resolution 원장
9. 필요한 코드·data·Scene·tests

## 현재 핵심 규칙

- 현재 검증 상한은 `+50`; 정밀 이정표는 `+10/+20/+30/+40/+50`이다.
- 장기 최종 강화 상한은 사람 플레이 이후 결정한다.
- 일반 수식어는 A·B 두 개다.
- 활성 사건·연대기 수식어는 한 개이며 세계일정에 따라 진화한다.
- 작품은 UID·소유자·손상·복원·사건·계승·재방문 기록을 유지한다.
- 일반 실패와 대파는 작품 생애를 삭제하지 않는다.
- 완전 파괴는 명시적이고 정보가 제공된 선택에서만 허용하며 역사 기록은 남긴다.
- 피로도·날짜는 작업 우선순위와 세계 결과의 공통 축이다.
- 정확한 경제 수치는 버전형 테스트 프리셋이다.
- 코어 재미는 행동 증거와 중립적 회상 인터뷰를 함께 사용해 검증한다.
- 명예의 전당은 경쟁·순위 없는 미래 아카이브이며 현재 보류 상태다.

## 첫 코어 버티컬 슬라이스

```text
플레이어 선택 작품 한 점 제작
→ +10/+20/+30/+40/+50 정밀 이정표
→ 방문 고객 납품
→ 즉시 인과 결과
→ 피로도·날짜·세계일정
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
```

`+50` 도달만으로 완료하지 않는다. 작품 생애가 다음 행동 이유로 돌아와야 한다. 다른 작품군은 제한된 비플레이 미리보기로만 제시한다.

## 역사 구현 기준선

- MVP-001·002·003은 과거 구현·자동 검증 증거다.
- MVP-003의 `+5/+10` 흐름은 `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`다.
- 과거 정확한 수치는 `LEGACY_IMPLEMENTED_VALUE`이며 최신 제품 확정값이 아니다.
- 최신 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`이다.

## 열린 PR

- `#94`: 현재 권위 복구 Draft
- `#95`: 병합 없이 종료된 중복 PR
- `#86`: 대체된 PR
- `#61`: 역사 전용 PR
- `#81`: 참고 자산 PR

## 다음 작업

1. Hub·Sheet의 최신 Decision 표현을 맞춘다.
2. PR #94의 changed files·리뷰·스레드·댓글·CI·금지 경로·권위 드리프트를 감사한다.
3. 차단 결함이 없으면 expected HEAD를 고정해 squash merge한다.
4. main SHA와 Sheet를 재동기화한다.
5. 사용자 R1 정본 최종 검수를 진행한다.

제품 구현은 계속 `BLOCKED`다.
