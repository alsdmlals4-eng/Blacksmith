# Blacksmith Pre-Work Research Gate Design

## Decision target

- Decision ID: `BS-OPS-20260811-02`
- Status target: `USER_APPROVED / PRE_WORK_RESEARCH_GATE / PLANNING_ONLY`
- Refines: `BS-OPS-20260805-01`의 벤치마킹·현업 비교 범위
- Does not replace: `BS-OPS-20260805-01`의 TDD·조기 체크포인트 규칙
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`

## Problem

현재 정본은 이미 벤치마킹·현업 비교를 요구하지만, `AGENTS.md`의 문구는 주로 질문·추천·새 시스템 설계를 중심으로 설명되어 있다. 사용자는 이를 더 강하게 확장해 **모든 의미 있는 작업을 시작하기 전에 벤치마킹과 현업/공식 자료 조사를 먼저 수행**하도록 요청하고 승인했다.

이 규칙은 메모리나 과거 대화에 의존하지 않고 GitHub 정본과 Google Sheet의 동일 Decision ID로 복구 가능해야 한다.

## Research basis — 2026-08-11 KST

운영 규칙 자체도 선행 조사 Gate를 적용했다.

1. Google Engineering Practices — Code Review
   - https://google.github.io/eng-practices/review/
   - 설계·기능·복잡도·테스트·문서와 시스템 전체 맥락을 함께 검토한다.
2. Google Engineering Practices — Small CLs
   - https://google.github.io/eng-practices/review/developer/small-cls.html
   - 하나의 자족적인 작은 변경이 리뷰 정확도·롤백·설계 품질에 유리하다.
3. GitHub Docs — About pull request reviews
   - https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
   - 병합 전 리뷰로 품질·지식 공유·변경 요청을 관리한다.
4. Godot Engine 4.7 documentation — Project organization
   - https://docs.godotengine.org/en/4.7/tutorials/best_practices/project_organization.html
   - 엔진/프로젝트 특유의 구현 문제는 최신 공식 문서를 우선 비교하는 것이 안전하다.
5. Android Developers — Game quality guidance
   - https://developer.android.com/quality
   - Android 게임은 사용자 가치·UX·기술 품질·안전 요구를 플랫폼 공식 기준과 함께 검토해야 한다.

### ADOPT / ADAPT / REJECT

- `ADOPT`: 최신 공식·1차 자료 우선, 변경 전 넓은 맥락 확인, 작은 자족 변경, 검토·테스트·문서 동반.
- `ADAPT`: 게임 기획/콘텐츠/UX는 직접·인접 유사작을 함께 비교하고 플레이어 판단 구조까지 비교한다.
- `ADAPT`: 기술/운영 작업은 게임 유사작보다 엔진·플랫폼·VCS·도구의 공식 문서와 현업 구현 관행을 우선한다.
- `REJECT`: 출처 수를 채우기 위한 무관한 사례 나열, 유명 사례의 무비판적 복제, 조사만 하고 결정에 반영하지 않는 형식적 절차.

## Mandatory gate

`PRE_WORK_RESEARCH_GATE`는 다음 순서로 적용한다.

```text
Base current main + Blacksmith main/open PR + Google Sheet fresh preflight
→ 작업 유형·변경 경계 분류
→ 벤치마킹
→ 최신 현업/공식/1차 자료 조사
→ ADOPT / ADAPT / REJECT / DIFFERENTIATOR 기록
→ GitHub 정본·Sheet 충돌 검사
→ 적대적 pre-check
→ 설계/정본/구현/TDD 작업 시작
```

Fresh preflight는 조사보다 먼저 실행해 현재 질문과 권위 범위를 정한다. **조사 결과가 준비되기 전에는 새 설계 결론, 정본 변경, 코드·설정·테스트·자산 변경을 시작하지 않는다.**

## Research depth by work type

### A. Game design / content / UX / economy / progression / market positioning

최소:

- 직접 또는 인접 유사작/제품 2개 이상
- 최신 현업·플랫폼·공식·1차 자료 2개 이상
- 각 사례별 `ADOPT / ADAPT / REJECT / DIFFERENTIATOR`
- 플레이어 판단, 정보 구조, 비용/반복 구조, 실패 위험 비교

새 핵심 시스템·경제·출시·법적/권리·접근성처럼 고위험이면 3개 이상의 비교 사례와 2개 이상의 1차/공식 자료를 기본으로 한다.

### B. Technical / Godot / Android / GitHub / CI / tooling / performance

최소:

- 해당 기술의 최신 공식/1차 문서 1개 이상
- 유사 구현/현업 관행 또는 추가 공식 자료 1개 이상
- 현재 프로젝트 버전·권위·제약과의 호환성 판정
- `ADOPT / ADAPT / REJECT`와 회귀 위험 기록

Godot 작업은 현재 사용 버전과 맞는 공식 문서를 우선하고, Android/Google Play 작업은 현재 Android Developers/Play 공식 요구를 우선한다.

### C. Low-risk maintenance / narrow documentation / metadata repair

최소:

- 현재 정본·최근 PR·공식 책임 원본을 다시 읽는다.
- 외부 벤치마크가 의미 있는 경우 1개 이상 비교한다.
- 의미 있는 외부 비교가 없으면 `BENCHMARK_NOT_APPLICABLE` 사유를 명시하고, 관련 공식/1차 자료가 존재하면 최소 1개를 확인한다.

`BENCHMARK_NOT_APPLICABLE`은 조사 생략 토큰이 아니다. 작업 성격상 무관한 게임/제품 사례를 억지로 붙이지 않기 위한 예외다.

## Required evidence packet

의미 있는 작업에는 PR 설명, planning canon, decision 문서 또는 감사 기록 중 하나에 다음을 남긴다.

```yaml
PRE_WORK_RESEARCH_PACKET:
  checked_at_kst:
  base_main_sha:
  project_main_sha:
  open_pr_inventory:
  google_sheet_state:
  work_type:
  benchmark_sources:
  professional_or_official_sources:
  adopt:
  adapt:
  reject:
  differentiator:
  canon_conflict_check:
  adversarial_precheck:
  remaining_uncertainty:
```

## Source-quality rules

- 시간에 따라 바뀌는 기술·플랫폼·정책은 최신 공식/1차 자료를 우선한다.
- 게임 벤치마크는 공식 상품 페이지·개발자 문서·개발자 발표·신뢰 가능한 실제 플레이 자료를 우선한다.
- 검색 요약, 과거 채팅, 메모리, 2차 블로그만으로 정본 결론을 확정하지 않는다.
- 외부 사례가 프로젝트 코어와 충돌하면 유명하거나 성공한 사례라도 `REJECT`한다.
- 벤치마크에서 관찰한 수치·경제·확률을 Blacksmith 정본 수치로 자동 승격하지 않는다.

## Adversarial review

### Attack

1. **절차 과부하 위험**: 모든 사소한 변경에 동일한 3+2 자료 요구를 강제하면 작은 수정이 느려진다.
2. **형식주의 위험**: 출처 수만 채우고 실제 결정이 바뀌지 않을 수 있다.
3. **유사작 복제 위험**: 시장 사례가 프로젝트 코어보다 우선되는 왜곡이 생길 수 있다.
4. **오래된 자료 위험**: 엔진·Android·GitHub 문서가 현재 버전과 다를 수 있다.
5. **정본 중복 위험**: 기존 `BS-OPS-20260805-01`과 새 규칙이 서로 다른 활성 권위처럼 보일 수 있다.
6. **merge 정책 drift**: 현재 `AGENTS.md`의 일반 병합 문구가 v4.5 r2의 승인 범위 내 자동 병합 정책과 충돌한다.

### Validate critique

- 1 `MUST_FIX`: 작업 유형별 조사 강도를 분리한다.
- 2 `MUST_FIX`: evidence packet에 실제 `ADOPT/ADAPT/REJECT/DIFFERENTIATOR`를 강제한다.
- 3 `MUST_FIX`: 프로젝트 코어/정본 우선과 자동 역수입 금지를 명시한다.
- 4 `MUST_FIX`: current/latest 공식 자료와 프로젝트 버전 호환성을 명시한다.
- 5 `MUST_FIX`: `BS-OPS-20260811-02`는 `BS-OPS-20260805-01`의 벤치마킹 범위만 **refine**하고 TDD/early-checkpoint 권위는 유지한다고 명시한다.
- 6 `SHOULD_FIX`: 같은 운영 정합성 변경에서 `AGENTS.md`의 stale merge wording을 `BS-OPS-20260811-01`/v4.5 r2에 맞춰 교정한다. 새 merge 방향을 만드는 것이 아니라 이미 승인된 권위를 복구하는 수정이다.

## Canon propagation

이번 Decision은 다음을 최소 수정한다.

- `docs/decisions/BS-OPS-20260811-02_PRE_WORK_RESEARCH_GATE.md` — 책임 원본
- `AGENTS.md` — 필수 진입 순서와 조사 강도/merge wording
- `CURRENT_CONFIRMED_DECISIONS.md` — 현재 승인 Decision 인덱스
- `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md` — resume context
- `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md` — 기계 판독 Gate
- 테스트 — 위 정본 전파와 제품/Task3 block 보존
- Google Sheet — 동일 Decision ID와 merge/readback 증거

원본 v4.5 r2 `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md`는 `BS-OPS-20260811-01` provenance 계약 때문에 이번 변경에서 직접 편집하지 않는다. 새 Decision은 프로젝트 override/refinement로 연결한다.

## Acceptance criteria

- `PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK`
- 조사 없는 새 설계·정본·구현 변경을 허용하지 않는다.
- 작업 유형별 최소 조사 강도가 명시된다.
- `ADOPT / ADAPT / REJECT / DIFFERENTIATOR` 증거가 요구된다.
- 기존 `BS-OPS-20260805-01` TDD·early-checkpoint 권위가 유지된다.
- v4.5 r2 승인 범위 내 merge authority가 AGENTS에서 회귀하지 않는다.
- R3–R7 counter는 `2/10` 그대로다.
- `PRODUCT_IMPLEMENTATION: BLOCKED`, `TASK3_IMPLEMENTATION: NOT_APPROVED` 그대로다.
