# BS-OPS-20260811-02 — Pre-Work Research Gate

```yaml
DECISION_ID: BS-OPS-20260811-02
STATUS: USER_APPROVED_PRE_WORK_RESEARCH_GATE
REFINES: BS-OPS-20260805-01_BENCHMARK_SCOPE_ONLY
PRE_WORK_RESEARCH_GATE: REQUIRED_BEFORE_MEANINGFUL_WORK
R3_R7_APPROVAL_COUNTER: 2/10
PRODUCT_IMPLEMENTATION: BLOCKED
TASK3_IMPLEMENTATION: NOT_APPROVED
```

## User-approved rule

Blacksmith의 모든 **의미 있는 작업**은 현재 권위 preflight 뒤, 실제 설계·정본·구현·테스트·설정·자산 변경을 시작하기 전에 벤치마킹과 최신 현업/공식/1차 자료 조사를 수행한다. 이 규칙은 대화 메모리에 의존하지 않고 GitHub 정본과 연결 Google Sheet의 동일 Decision ID로 복구한다.

이 Decision은 `BS-OPS-20260805-01`의 **벤치마킹·현업 비교 범위만 상세화**한다. 기존 상시 TDD와 조기 체크포인트 권위는 그대로 유지한다.

## Mandatory sequence

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

Fresh preflight는 조사 대상을 정하기 위한 선행 조회다. 조사 결과가 준비되기 전에는 새로운 설계 결론이나 정본·코드·설정·테스트·자산 변경을 시작하지 않는다.

## Research depth by work type

### A. Game design / content / UX / economy / progression / market positioning

최소 기준:
- 직접 또는 인접 유사작/제품 2개 이상
- 최신 현업·플랫폼·공식·1차 자료 2개 이상
- `ADOPT / ADAPT / REJECT / DIFFERENTIATOR`
- 플레이어 판단·정보 구조·비용/반복 구조·실패 위험 비교

새 핵심 시스템·경제·출시·법적/권리·접근성처럼 고위험이면 직접/인접 비교 3개 이상과 공식/1차 자료 2개 이상을 기본으로 한다.

### B. Technical / Godot / Android / GitHub / CI / tooling / performance

최소 기준:
- 해당 기술의 현재 공식/1차 자료 1개 이상
- 유사 구현/현업 관행 또는 추가 공식 자료 1개 이상
- 현재 프로젝트 버전·권위·제약과의 호환성 판정
- `ADOPT / ADAPT / REJECT`와 회귀 위험 기록

Godot은 현재 사용 버전과 맞는 공식 문서를 우선하고, Android/Google Play는 현재 Android Developers/Play 공식 요구를 우선한다.

### C. Low-risk maintenance / narrow documentation / metadata repair

최소 기준:
- 현재 정본·최근 PR·공식 책임 원본 재조회
- 외부 비교가 의미 있으면 1개 이상 비교
- 외부 벤치마크가 실질적으로 무관하면 `BENCHMARK_NOT_APPLICABLE` 사유를 명시하고 관련 공식/1차 자료가 존재할 때 최소 1개 확인

`BENCHMARK_NOT_APPLICABLE`은 조사 생략 토큰이 아니라 무관한 게임/제품 사례를 억지로 붙이지 않기 위한 제한적 예외다.

## Required evidence

의미 있는 작업은 PR 설명, planning canon, Decision 문서 또는 감사 기록 중 하나에 아래 정보를 남긴다.

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

## Source quality and transfer rules

- 시간에 따라 바뀌는 기술·플랫폼·정책은 현재 공식/1차 자료를 우선한다.
- 게임 벤치마크는 공식 상품 페이지·개발자 문서·개발자 발표·신뢰 가능한 실제 플레이 증거를 우선한다.
- 검색 요약·과거 채팅·메모리·2차 블로그만으로 정본 결론을 확정하지 않는다.
- 외부 사례가 Blacksmith 코어/승인 정본과 충돌하면 성공 사례라도 `REJECT`한다.
- 벤치마크의 수치·확률·경제·보상은 Blacksmith 정본 수치로 자동 승격하지 않는다.

## 2026-08-11 research basis

- Google Engineering Practices — Code Review / Small CLs: 시스템 맥락·테스트·문서까지 검토하고 작은 자족 변경을 선호.
- GitHub Docs — Pull request reviews: 병합 전 품질 검토·변경 요청·지식 공유.
- Godot Engine 4.7 official documentation — Project organization: Godot 작업은 현재 엔진 공식 관행을 우선 비교.
- Android Developers — App/Game quality guidance: Android 게임은 사용자 가치·UX·기술 품질·안전의 플랫폼 기준을 함께 검토.

### ADOPT
- current official/primary evidence first
- small self-contained reviewable changes
- whole-system context + tests + documentation + review

### ADAPT
- 게임/콘텐츠/UX는 직접·인접 유사작의 플레이어 판단 구조까지 비교
- 기술/운영은 게임 사례보다 엔진·플랫폼·VCS·도구 공식 자료와 유사 구현 관행을 우선

### REJECT
- 출처 수만 채우는 형식주의
- 유명 사례의 무비판적 복제
- 벤치마크 수치·경제의 자동 역수입
- `BENCHMARK_NOT_APPLICABLE`의 blanket bypass 사용

### DIFFERENTIATOR
Blacksmith는 조사 결과를 단순 링크 목록이 아니라 `ADOPT / ADAPT / REJECT / DIFFERENTIATOR + canon conflict + adversarial precheck`로 남겨 다음 작업자가 의사결정 근거까지 복구하게 한다.

## Adversarial findings resolved in this Decision

1. 절차 과부하 → 작업 유형별 조사 강도 분리.
2. 출처 수 형식주의 → 실제 채택/수정/비채택/차별점 기록 의무화.
3. 유사작 복제 → Blacksmith 코어·정본 우선과 자동 역수입 금지.
4. 오래된 기술 자료 → current/latest 공식 자료와 프로젝트 버전 호환성 확인.
5. `BS-OPS-20260805-01` 중복 권위 → benchmark scope refinement만 수행, TDD/early checkpoint 보존.
6. merge wording drift → `BS-OPS-20260811-01`/v4.5 r2의 같은 승인 범위 merge authority를 복구하고 새 기획 충돌·범위 확장만 사용자 Decision으로 남긴다.

## Protected boundaries

- `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` v4.5 r2 원문은 이번 Decision에서 수정하지 않는다.
- `R3_R7_APPROVAL_COUNTER`는 `2/10` 그대로다.
- `PRODUCT_IMPLEMENTATION: BLOCKED`.
- `TASK3_IMPLEMENTATION: NOT_APPROVED`.
- `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`을 변경하지 않는다.
- 같은 승인 범위는 exact technical validation 뒤 병합 재승인을 요구하지 않는다. 새 planning conflict·scope expansion만 별도 사용자 Decision을 요구한다.
