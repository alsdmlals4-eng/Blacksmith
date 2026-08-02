# Active Context

- 갱신일: `2026-08-02 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 Decision: `BS-OPS-20260802-01`
- 기준 main: `ac120fb146cea29bb5f8876682809f76779d86ad`
- 현재 브랜치: `agent/blacksmith-planning-canon-recovery`
- 현재 Draft PR: `#84`
- 기획 Umbrella: Issue `#79`
- 제품 구현: `BLOCKED`
- 다음 기획 Bundle: `R1 Project Core and Player Promise`

## 1. 현재 판정

| 영역 | 상태 |
|---|---|
| Base release adoption | `9.4.0 / MERGED` |
| 프로젝트 운영 정본 | `RECOVERY_IN_PROGRESS` |
| Root current decisions | `CREATED / SHEET_SYNC_PENDING` |
| Google Sheet binding | `CONFIGURATION_CORRECTION_IN_PROGRESS` |
| PR #81 | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| 기획 Coverage | `NOT_STARTED_AFTER_RECOVERY` |
| Grill Me | `0 VERIFIED OPEN QUESTIONS` |
| Codex 구현 | `BLOCKED_BY_PLANNING_GATE` |
| Runtime against latest planning | `NOT_RUN` |
| Android 실기기 | `NOT_RUN` |
| 접근성 사람 검토 | `NOT_RUN` |
| 성능 | `NOT_RUN` |
| 외부 플레이테스트 | `NOT_RUN` |

## 2. 프로젝트 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

보호할 강점:

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 버튼 입력당 결과 1회
- 장비 UID·작품 정체성·소유권·운명·연대기
- 판매·납품 이후 지연된 세계 결과와 관계 환류
- 모바일에서 기억·비교 가능한 정보량
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않는 원칙

R1에서 이 방향을 다시 명확히 정본화한다. 재검토는 현재 강점과 승인 결정을 무효화하는 전면 초기화가 아니다.

## 3. 승인 증거가 확인된 현재 기획

- `BS-ART-20260731-01`: 스타일라이즈드 다크 포지
- `BS-MODAK-20260731-01`: 밝은 불 정령 모닥
- `BS-MAIN-20260801-01`: 별도 메인 화면
- `BS-SHELL-20260801-01`: 단일 BlacksmithApp + View/Overlay
- `BS-GRADE-20260801-02`: 보통·우수·명품·걸작·전설
- `BS-SAVE-20260801-01`: 단일 캠페인·자동 백업2·SaveStatus·AttemptIntent·ResultEnvelope

상세 계약은 PR #81의 자료에서 선별 승격한다. 위 상태는 제품 구현·런타임·기기 검증 완료가 아니다.

## 4. 실제 구현 사실

현재 `project.godot`:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

따라서 승인된 별도 Main Menu와 단일 App Shell은 아직 실제 제품 진입이 아니다.

기존 Prototype/PoC에는 제작·강화·보관·자동 단조·장비 생애 관련 코드와 과거 자동 검증 이력이 있다. 이들은 다음 용도로만 사용한다.

- 현재 파일과 동작 사실 확인
- 회귀 보호 경계
- 최신 기획과의 충돌 발견
- 재사용 가능한 구현 후보 판정

과거 PASS를 최신 기획, Android, 접근성, 성능, 사람 플레이 PASS로 확대하지 않는다.

## 5. 운영 복구 Finding

### MUST_FIX

1. 시작 문서가 PR #35·Issue #34·과거 브랜치를 현행처럼 안내함
2. Base v8·v9.1·v9.3·v9.4 권위가 혼재함
3. PR #81을 전체 병합하기 어려우나 현재 기획 자료의 상당 부분이 그곳에만 존재함
4. current main에 안정적인 Decision 진입점이 없었음
5. Sheet CURRENT 원장에 경로·Commit·승인 증거가 빠진 행이 다수 존재함
6. Issue #60·#79, PR #81·#84 역할이 명시되지 않음
7. Draft/Sheet `USER_APPROVED` 표기를 원 승인 증거와 분리하지 않음
8. 운영 Health가 모든 중요 Gate NOT_RUN에도 PASS 계열 표현을 사용함

### SHOULD_FIX

- 제품 진입 Test Scene과 승인 Main/Shell의 차이를 모든 현재 상태 문서에 명시
- 상세 수치와 중요 기획 결정을 분리
- CURRENT와 HISTORY_ONLY를 분리
- PC 고려와 모바일 현재 범위를 분리
- PR 중간 HEAD를 최종 동기화 증거로 사용하지 않음

현재 운영 Finding은 사용자 취향 결정이 아니라 사실·경로·상태 오류이므로 Grill Me 없이 교정한다.

## 6. PR·Issue 권위

| Surface | 역할 |
|---|---|
| Issue #79 | 현재 총기획 Umbrella. Base v9.4와 R0~R9 순서로 갱신 필요 |
| PR #84 | 현재 운영·정본 복구 Draft |
| PR #81 | 기획·승인 증거와 선별 승격 소스. 전체 병합 금지 |
| Issue #60 | 과거 Base v6 전면 재기획. HISTORY_ONLY 후보 |

PR #81을 닫거나 삭제하기 전에 선별 승격 목록과 승인 증거 위치를 현재 정본에 남긴다.

## 7. 상세 데이터와 Grill Me 경계

상세 기술값·초기 밸런스·간격·시간·확률·용량 기본값은 프로젝트 방향을 바꾸지 않는 범위에서 GPT 권장안을 사용한다.

```text
RECOMMENDED_DEFAULT
또는
TEST_VALUE
```

다음만 검증 후 Grill Me로 올린다.

- 코어·플레이어 판타지·뾰족한 재미 변경
- 주요 시스템·UX 원칙의 양립 불가능한 충돌
- 버티컬 슬라이스·본제작 범위 선택
- 주요 실패·파괴·복구·보상 의미
- 승인 Decision 대체
- 플레이 경험·제작 비용이 실질적으로 다른 대안

## 8. 현재 금지 범위

운영·기획 복구 중 다음을 변경하지 않는다.

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

또한 다음을 시작하지 않는다.

- Codex 제품 구현
- 별도 Main/Shell/Save 실제 구현
- 최신 데이터 Migration
- 고객 파이프라인·자동 강화 실제 구현
- 최종 에셋 제작·교체
- PC 동시 UI 범위

## 9. 현재 실행 순서

```text
R0 운영·정본 복구
→ GitHub·Sheet BS-OPS-20260802-01 동기화
→ Issue·PR 권위 정리
→ 적대적 검토·콜드 스타트·exact-HEAD 검증
→ R1 프로젝트 코어·플레이어 약속
→ R2 Core/Session/Meta Loop
→ R3 제작·강화·작품 정체성·실패·저장
→ R4 고객·세계 환류·장비 연대기
→ R5 경제·성장·장기 목표
→ R6 모바일 UX·접근성·아트·오디오
→ R7 버티컬 슬라이스·데이터·검증·제작 계획
→ R8 최종 적대적 검수·사용자 검수
→ R9 Codex 구현 인계
```

## 10. 다음 작업

1. `DEVELOPMENT_GATES`, `DOCUMENTATION_MAP`, `ROADMAP`, Registry, Base Adapter, Health를 복구한다.
2. Google Sheet `00·01·02·04·05·90·99`를 같은 Decision ID로 갱신한다.
3. GitHub와 Sheet의 최종 Commit을 재조회한다.
4. Issue #79·#60과 PR #81·#84 권위를 정리한다.
5. 운영 적대적 검토와 보호 경로 diff 검사를 통과한다.
6. R1 총기획을 시작한다.

## 11. 완료 금지 조건

다음이 남아 있으면 R0 완료 또는 전체 기획 완료로 선언하지 않는다.

- GitHub·Sheet의 Decision ID·의미·Commit 불일치
- PR #81·Issue #60의 활성 권위 오해 가능성
- 미해결 운영 MUST_FIX
- 보호 제품 경로 변경
- 검증하지 않은 상태의 PASS 표기
- 승인 증거 없는 Draft의 자동 승격
- 중요 사용자 결정을 AI가 임의 확정

## 12. 검증 상태 상한

이 문서 갱신은 운영 정본 교정이다. Godot import, 런타임, Android, 접근성, 성능, 사람 플레이 증거를 만들지 않는다. 해당 상태는 계속 `NOT_RUN`이다.
