# Blacksmith 시작 지점

## 프로젝트 약속

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

## 현재 상태

```yaml
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R1_STATUS: USER_APPROVED / CANON_COMPLETE
R2_STATUS: PLANNING_ACTIVE
R1_FINAL_APPROVAL: BS-OPS-20260803-05
CANON_BASELINE_PR: 94
CANON_BASELINE_SHA: 8a0956d6c8b4cf3db545a17d0bd002ba8354d568
SHEET_SYNC_BASELINE: COMPLETE / BS-OPS-20260803-04 / READBACK_PASS
PRODUCT_IMPLEMENTATION: BLOCKED
WORLD_SCHEDULE: DAILY_STAGED_PROGRESS / SCALE_INCREASES_DURATION
HALL_OF_FAME: FUTURE_CONTENT_HOLD_NONCOMPETITIVE_ARCHIVE
```

`CANON_BASELINE_SHA`는 R1 정본을 확정한 병합 기준이며 파일 자신의 현재 Git commit을 뜻하지 않는다.

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
4. `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
5. `docs/planning/BLACKSMITH_R1_FINAL_APPROVAL_AND_WORLD_SCHEDULE_PROGRESS_2026.md`
6. `ACTIVE_CONTEXT.md`
7. `DEVELOPMENT_GATES.md`
8. `ROADMAP.md`
9. 배치별 승인 정본과 Core Resolution 원장
10. 필요한 코드·data·Scene·tests

## 현재 핵심 규칙

- 현재 검증 상한은 `+50`; 정밀 이정표는 `+10/+20/+30/+40/+50`이다.
- 장기 최종 강화 상한은 사람 플레이 이후 결정한다.
- 일반 수식어는 A·B 두 개다.
- 활성 사건·연대기 수식어는 한 개이며 세계일정에 따라 진화한다.
- 작품은 UID·소유자·손상·복원·사건·계승·재방문 기록을 유지한다.
- 일반 실패와 대파는 작품 생애를 삭제하지 않는다.
- 완전 파괴는 명시적이고 정보가 제공된 선택에서만 허용하며 역사 기록은 남긴다.
- 피로도·날짜는 작업 우선순위와 세계 결과의 공통 축이다.
- 세계일정은 날짜마다 최대 한 단계씩 진행하고 최소 하나의 중간 상태 뒤 별도 날짜에 결말이 나온다.
- 세계일정은 규모가 클수록 더 많은 단계와 게임 날짜가 필요하다.
- 정확한 경제·세계일정 기간 수치는 버전형 테스트 프리셋이다.
- 코어 재미는 행동 증거와 중립적 회상 인터뷰를 함께 사용해 검증한다.
- 명예의 전당은 경쟁·순위 없는 미래 아카이브이며 현재 보류 상태다.

## 첫 코어 버티컬 슬라이스

```text
플레이어 선택 작품 한 점 제작
→ +10/+20/+30/+40/+50 정밀 이정표
→ 방문 고객 납품
→ 즉시 사용 계획·초기 인과 피드백
→ 날짜별 세계일정 중간 진행
→ 별도 날짜의 최종 결과
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
```

`+50` 도달만으로 완료하지 않는다. 작품 생애가 다일 세계일정을 거쳐 다음 행동 이유로 돌아와야 한다. 다른 작품군은 제한된 비플레이 미리보기로만 제시한다.

## 역사 구현 기준선

- MVP-001·002·003은 과거 구현·자동 검증 증거다.
- MVP-003의 `+5/+10` 흐름과 단일 날짜 결과는 `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`다.
- 과거 정확한 수치는 `LEGACY_IMPLEMENTED_VALUE`이며 최신 제품 확정값이 아니다.
- 최신 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`이다.

## PR·감사 상태

- PR #94: `MERGED_CANON_BASELINE`
- PR #96: `MERGED_POST_MERGE_FINALIZATION`
- PR #97: `MERGED_SHEET_SYNC_GATE_CLOSURE`
- Audit ID: `BS-OPS-20260803-02`
- P0: `0`
- P1: `0`
- PR #94·#96·#97 CI: `Validate Base v9 adoption PASS / PR validation PASS`
- PR #81: 참고 자산 Draft, 독립 병합 금지
- PR #95·#86·#61: 병합 없이 종료 또는 역사 전용

## 다음 Gate

1. R2 `Core·Session·Meta Loop` 기획
2. 세계일정 규모·기간 프리셋·날짜별 정보·플레이어 개입 규칙 확정
3. 제품 구현은 계속 `BLOCKED`