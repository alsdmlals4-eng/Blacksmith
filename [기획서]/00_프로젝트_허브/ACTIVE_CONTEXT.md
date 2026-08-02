# Active Context

- 갱신일: `2026-08-02 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 Decision: `BS-OPS-20260802-01`
- 기준 main: `ac120fb146cea29bb5f8876682809f76779d86ad`
- 현재 브랜치: `agent/blacksmith-planning-canon-recovery`
- 현재 Draft PR: `#84`
- 기획 Umbrella: Issue `#79`
- R0 운영·정본 복구: `PASS_FOR_DRAFT_PR`
- 제품 구현: `BLOCKED`
- 다음 Bundle: `R1 Project Core and Player Promise`

## 현재 판정

| 영역 | 상태 |
|---|---|
| Base release adoption | `9.4.0 / COMPLETE` |
| GitHub 운영 정본 | `RECOVERED` |
| Root current decisions | `RECOVERED` |
| Google Sheet binding/readback | `PASS` |
| Issue·PR authority | `PASS` |
| PR #81 | `REFERENCE_ONLY / SUPERSEDED_AS_MERGE_UNIT` |
| Issue #60 | `HISTORY_ONLY / SUPERSEDED` 후보 |
| 기획 Coverage | `R1 NOT_STARTED` |
| verified Grill Me question | `0` |
| Codex 구현 | `BLOCKED_BY_PLANNING_GATE` |
| Runtime against latest planning | `NOT_RUN` |
| Android 실기기 | `NOT_RUN` |
| 접근성 사람 검토 | `NOT_RUN` |
| 성능 | `NOT_RUN` |
| 외부 플레이테스트 | `NOT_RUN` |

## 프로젝트 보호 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화의 위험 앞에서 멈출지 도전할지 선택하며, 그 작품이 다른 이의 손에서 쌓은 역사와 세계의 반응을 돌려받는 Android 세로형 제작 게임.

R1은 이 방향을 더 명확히 정본화한다. 전면 초기화나 승인 결정 폐기가 목적이 아니다.

보호할 강점:

- 한 명의 대장장이와 장비 한 점 중심 경험
- 직접 제작과 강화 위험 선택
- 일반 강화 버튼 입력당 결과 1회
- 장비 UID·작품 정체성·소유권·운명·연대기
- 판매·납품 이후 지연된 세계 결과
- 모바일에서 기억·비교 가능한 정보량
- 스타일라이즈드 다크 포지와 밝은 불 정령 모닥
- 미실행 검증을 PASS로 표시하지 않는 원칙

## 승인 증거가 확인된 기획

- `BS-ART-20260731-01`
- `BS-MODAK-20260731-01`
- `BS-MAIN-20260801-01`
- `BS-SHELL-20260801-01`
- `BS-GRADE-20260801-02`
- `BS-SAVE-20260801-01`

이들은 승인된 기획이며 제품 구현·런타임·기기 검증 완료가 아니다. 상세 계약은 R3 또는 R6에서 PR #81로부터 선별 승격한다.

## 실제 구현 사실

현재 `project.godot`:

```text
run/main_scene="res://scenes/test/enhancement_test.tscn"
```

따라서 승인된 별도 Main Menu와 단일 App Shell은 아직 실제 제품 진입이 아니다.

기존 제작·강화·보관·장비 생애 PoC는 실제 구현과 회귀 기준선으로만 사용한다. 과거 PASS를 최신 기획·Android·접근성·성능·사람 플레이 PASS로 확대하지 않는다.

## R0 적대적 검토 결과

해결된 운영 Finding:

1. PR #35·Issue #34 구형 진입 경로
2. Base v8·v9.1·v9.3·v9.4 권위 혼재
3. PR #81 전체 병합 위험
4. Root Decision entrypoint 누락
5. Sheet CURRENT 원장 추적성 부족
6. Issue #60·#79, PR #81·#84 중복 권위
7. Draft/Sheet 승인 표기 팽창
8. 모든 중요 Gate NOT_RUN 상태의 false-PASS 표현
9. 제품 Test Scene과 승인 Main/Shell 간 상태 미표시
10. 상세 시험값과 중요 기획 Decision 혼합

현재 확인된 Grill Me 대상: `0`. 위 항목은 사용자 취향이 아닌 사실·경로·상태 오류였으므로 자동 교정했다.

## PR·Issue 권위

| Surface | 역할 |
|---|---|
| Issue #79 | 현재 총기획 Umbrella |
| PR #84 | 현재 운영·정본 복구 Draft |
| PR #81 | 기획·승인 Evidence Source, 전체 병합 금지 |
| Issue #60 | 과거 Base v6 전면 재기획, history 후보 |

각 Surface에 동일한 역할 설명 Comment를 남겼다.

## 상세 데이터와 Grill Me 경계

상세 기술값·초기 밸런스·간격·시간·확률·용량 기본값은 방향을 바꾸지 않는 범위에서 GPT 권장안을 사용한다.

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

## 보호 경로

총기획 중 다음을 변경하지 않는다.

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

main과 recovery branch 비교 결과 보호 경로 변경은 `0`이다.

## Google Sheet 동기화

- Spreadsheet ID: `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg`
- 반영 탭: `00·01·02·04·05·90·99`
- 같은 Decision ID, 의미, PR, 상태, GitHub 위치 readback: `PASS`
- 수정 범위 이동·수식 오류: 관찰되지 않음
- exact final Draft HEAD: Sheet `99_변경이력`과 PR metadata가 기록

## 현재 다음 작업

`R1 Project Core and Player Promise`.

R1 산출물:

- 타깃 플레이어·플레이 상황
- 한 문장 플레이어 약속
- 뾰족한 재미와 핵심 고민
- 비타협 조건·변경 가능한 외피
- 제외 범위
- 성공·실패 기준
- 벤치마크·Evidence·반증
- 검증된 중요 충돌이 있을 때만 한 건의 Grill Me

## 검증 상한

운영 복구 검증:

- GitHub entrypoint/readback: `PASS_FOR_DRAFT_PR`
- Sheet bounded write/readback: `PASS`
- Issue/PR authority: `PASS`
- product protected-path diff: `PASS`

실행하지 못한 검증:

- local Python validators: `BLOCKED_UNVERIFIED` (`gh` 없음, container GitHub DNS 실패)
- Godot runtime: `NOT_RUN`
- Android: `NOT_RUN`
- accessibility human: `NOT_RUN`
- performance: `NOT_RUN`
- external playtest: `NOT_RUN`

제품 구현과 전체 기획 완료는 계속 `BLOCKED`다.
