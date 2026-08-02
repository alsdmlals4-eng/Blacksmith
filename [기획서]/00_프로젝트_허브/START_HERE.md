# Blacksmith 시작 지점

## 프로젝트 한 문장 — 현재 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

이 문장은 `R1 Project Core and Player Promise`에서 근거·벤치마크·적대적 검토를 거쳐 다시 정본화한다. 재검토는 현재 강점과 승인 결정을 삭제하기 위한 전면 초기화가 아니다.

## 현재 상태

| 항목 | 상태 |
|---|---|
| 현재 Decision | `BS-OPS-20260802-01` |
| Work Mode | `TOTAL_PLANNING` |
| 현재 단계 | `CANONICAL_RECOVERY_IN_PROGRESS` |
| 기준 main | `ac120fb146cea29bb5f8876682809f76779d86ad` |
| 작업 브랜치 | `agent/blacksmith-planning-canon-recovery` |
| 현재 Draft PR | `#84` |
| 기획 Umbrella | Issue `#79` |
| PR #81 | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| Base release adoption | `9.4.0 / MERGED` |
| Google Sheet | `SYNC_IN_PROGRESS_BS-OPS-20260802-01` |
| 제품 구현 | `BLOCKED` |
| 다음 기획 | `R1 Project Core and Player Promise` |

## 실제 구현 기준선

- 현재 `project.godot` 실행 진입은 `res://scenes/test/enhancement_test.tscn`이다.
- 기존 제작·강화·보관·장비 생애 PoC 코드와 테스트는 역사적 구현 기준선으로 보존한다.
- 별도 메인 화면, 단일 `BlacksmithApp`, 최신 저장·복구 계약, v9 데이터 마이그레이션, 최신 고객 파이프라인은 아직 제품 구현 증거가 없다.
- Android 실기기, 최신 접근성, 성능, 최신 총기획 기준 사람 플레이는 `NOT_RUN`이다.

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. 이 문서
4. `ACTIVE_CONTEXT.md`
5. `DOCUMENTATION_MAP.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DESIGN_DOCUMENT_REGISTRY.json`
9. `SKILL_REGISTRY.json`
10. `docs/operations/BS-OPS-20260802-01_BASELINE.md`
11. `docs/superpowers/specs/2026-08-02-planning-canon-recovery-design.md`
12. `docs/superpowers/plans/2026-08-02-blacksmith-planning-canon-recovery.md`
13. 현재 기획 Bundle의 분야 정본
14. 필요한 실제 코드·데이터·Scene·테스트

과거 PR·Issue·PoC 문서는 위 현행 진입 문서에서 참조하라고 지정한 경우에만 현재 작업 근거로 사용한다.

## 현재 확정된 운영 규칙

- 기획 작성부터 진행한다.
- 상세 기술값·초기 수치는 GPT 권장안을 사용하되 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 표시한다.
- 중요 기획·실제 충돌만 한 질문씩 Grill Me로 사용자에게 묻는다.
- 저장소나 Sheet에서 확인 가능한 사실과 이미 승인된 결정은 다시 묻지 않는다.
- 주요 승인 Decision은 GitHub와 Google Sheet에 같은 ID로 즉시 동기화한다.
- 전체 기획·최종 적대적 검수·사용자 검수 전 제품 구현과 Codex Build를 시작하지 않는다.

## 현행 보호 경계

- 한 명의 대장장이
- 직접 제작과 강화 위험 선택
- 일반 강화 입력당 결과 1회
- 장비 UID·소유권·운명·연대기
- 판매·인계 이후 세계 결과
- 모바일에서 읽을 수 있는 작품 정체성
- 스타일라이즈드 다크 포지
- 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않음

현재 기획·운영 복구 PR에서는 다음을 변경하지 않는다.

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

## 승인 증거가 있는 제품 기획

현재 Root Decision 원장이 확인한 승인 기획은 다음과 같다.

- `BS-ART-20260731-01`
- `BS-MODAK-20260731-01`
- `BS-MAIN-20260801-01`
- `BS-SHELL-20260801-01`
- `BS-GRADE-20260801-02`
- `BS-SAVE-20260801-01`

이들은 기획 승인 상태이며 구현·런타임·Android·사람 검증 완료를 의미하지 않는다.

## PR과 Issue 역할

```text
Issue #79
= 총기획 Umbrella

PR #84
= 현재 운영·정본 복구 Draft

PR #81
= 기획·승인 Evidence Source
= 전체 병합 금지
= 선별 승격 대상

Issue #60
= 과거 Base v6 재기획 계약
= HISTORY_ONLY 후보
```

## 현재 다음 작업

1. 운영 문서·Decision 원장·Registry·Base Adapter를 current main 기준으로 복구한다.
2. `BS-OPS-20260802-01`을 Google Sheet `00·01·02·04·05·90·99`에 반영하고 재조회한다.
3. Issue #60·#79, PR #81·#84의 권위 관계를 정리한다.
4. 적대적 검토와 콜드 스타트 검증을 통과한다.
5. `R1 Project Core and Player Promise` 총기획을 시작한다.

## 완료 금지 조건

다음이 남아 있으면 운영 복구 또는 기획 완료로 선언하지 않는다.

- GitHub·Sheet Decision ID·Commit 불일치
- PR #81 또는 Issue #60이 현행 작업으로 해석되는 활성 경로
- 미해결 운영 `MUST_FIX`
- 보호 제품 경로 변경
- `NOT_RUN` 검증을 PASS로 표시
- 사용자 결정을 AI가 임의 확정

기획 완료 뒤에도 실제 제품 구현과 데모 완료는 별도의 Codex·런타임·기기·사람 검증 Gate를 통과해야 한다.
