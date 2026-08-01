# Blacksmith GitHub·Google Sheet 전체 적대적 검토 Pass 2

> Audit ID: `BS-REPO-AUDIT-20260801-02`
>
> 상태: `PASS2_COMPLETE / REMEDIATION_IN_PROGRESS`
>
> 기준일: `2026-08-01`
>
> Work Mode: `REVIEW → PLAN`
>
> 구현 권한: `NONE`
>
> 대상 main: `500a5a7960146ef229ae172cf9e127306d23f073`
>
> 대상 Draft: PR #81 · `docs/blacksmith-v9-planning-audit`

## 1. 목적

Base 현행 구조 분석과 P0-1 세이브 설계 이후, Blacksmith의 다음 내용을 다시 대조한다.

- 시작·권위·Gate 문서
- 승인 결정·설계·계획 데이터
- 실제 Godot Scene·Script·JSON·Test·CI
- 연결 Google Sheet 25개 탭
- 변경이력·Base adapter·생성 파생물
- 비주얼·아트·고객·경제·출시 준비도

이번 Pass는 기존 `BS-REPO-AUDIT-20260801-01`의 Finding을 대체하지 않는다. 각 Finding의 최신 해결 단계와 새로 확인된 전파·운영 결함을 연결한다.

## 2. 조사 범위

### GitHub

- `AGENTS.md`, README, START_HERE, ACTIVE_CONTEXT, ROADMAP, DEVELOPMENT_GATES, DOCUMENTATION_MAP
- DESIGN_DOCUMENT_REGISTRY, Skill Registry, Base adapter·Snapshot·Router·Health
- v9 승인 정본·계획 JSON·감사 Addendum·미래 구현계획
- `project.godot`, 제작·강화·고객·세계 Registry·자동 단조 코드
- 제작 등급·수식어·이정표·강화 밸런스 JSON
- CI Workflow·실행 정책·tests README

### Google Sheet

25개 탭의 A:H 활성 데이터 영역을 읽었다.

```text
00~05 운영·결정·감사·GDD
10~20 제품·세계·루프·인물·규칙·데모 목표
30~60 제작 기반·시스템·경제·콘텐츠·UX
70~72 아트·이미지 기획·검수
80 플레이테스트
90 제작·출시 Gate
98 Base 후보
99 변경이력
```

## 3. 전체 진행도 판정

| 영역 | 기획 | 구현 | 자동 검증 | Android·사람 검증 | 판정 |
|---|---|---|---|---|---|
| 프로젝트 코어 | 완료 | PoC 존재 | 과거 범위 PASS 이력 | NOT_RUN | KEEP |
| 별도 메인·App Shell | 승인 완료 | 없음 | 없음 | NOT_RUN | IMPLEMENTATION_OPEN |
| 세이브·이어하기·ResultEnvelope | 설계·11 Task 계획 완료 | 없음 | NOT_RUN | NOT_RUN | DESIGN_COMPLETE |
| 제작 등급 5단계 | 규칙 완료 | 구형 5 ID | 구형 테스트만 존재 | NOT_RUN | MIGRATION_OPEN |
| v9 데이터 마이그레이션 | 설계·7 Task 계획 완료 | 없음 | NOT_RUN | 실제 구형 save NOT_RUN | DESIGN_COMPLETE |
| 계보·보조·+50 이원화 | 최신 규칙 완료 | 구형 3슬롯·10단위 | 구형 테스트 보호 | NOT_RUN | MIGRATION_OPEN |
| 고객 4유형 | 공통 방향 완료 | 카일·철검 PoC | 구형 E2E | NOT_RUN | CONTENT_CONTRACT_PARTIAL |
| 자동 단조 | 최신 정지 경계 미정 | 핵심 선택 우회 | 구형 자동화 테스트 | NOT_RUN | PLANNING_OPEN |
| 비주얼 보드 | 작업 기준 승인 | 최종 에셋 없음 | 시각 회귀 없음 | 사람 검수 NOT_RUN | WORKING_BASELINE |
| Theme·안전 영역·설정 | 방향 일부 | 공통 Theme 없음 | 없음 | NOT_RUN | P1_OPEN |
| 아트·오디오·라이선스 | 방향 일부 | 최종 에셋 없음 | 검수 로그 거의 없음 | NOT_RUN | P2_OPEN |
| Base 운영체계 | 분석 완료 | adapter v9.1 drift | local validator NOT_RUN | 해당 없음 | MIGRATION_REQUIRED |

## 4. 적대적 핵심 판정

### 4.1 시작 문서가 현재 Gate를 오도한다

- START_HERE·ACTIVE_CONTEXT·ROADMAP·DEVELOPMENT_GATES는 장비 생애 PoC를 CURRENT로 취급한다.
- Sheet 00은 `PLANNING_COMPLETE_CANDIDATE`, `READY_FOR_USER_기획_완료_DECLARATION`을 표시한다.
- Sheet 01도 사용자 기획 완료 선언 준비를 다음 단계처럼 표시한다.
- 실제 현재 상태는 P0 10·P1 10·P2 6, Base migration required, 제품 구현 차단이다.

**연결:** `BS-AUD-F11`, `BASE-F08`.

### 4.2 제품 진입은 여전히 테스트 Scene이다

`project.godot`은 다음을 사용한다.

```text
run/main_scene = res://scenes/test/enhancement_test.tscn
```

별도 메인·SaveStatus·App Shell 승인과 직접 충돌한다.

**연결:** `BS-AUD-F01`.

### 4.3 자동·CI 증거는 구형 PoC 계약을 보호한다

현재 Godot CI는:

- enhancement test
- equipment lifecycle PoC
- main PoC Scene
- 구형 제작·강화·고객·세계 Registry 테스트

을 실행한다. `tests/README.md`도 +10~+100 3수식어, 안정·폭주, 6칸 보관함, 자동 단조를 현행 검증 범위로 기술한다.

이는 테스트 품질이 낮다는 뜻이 아니라, **최신 v9에 대한 회귀망이 아직 없고 구형 구조를 강하게 보호한다**는 뜻이다.

**연결:** `BS-AUD-F20`.

### 4.4 구형 데이터와 최신 정본 충돌은 실제다

- 제작 등급 JSON: `APPRENTICE/STANDARD/REFINED/MASTERWORK/PERFECT`
- 최신: `NORMAL/SUPERIOR/EXQUISITE/MASTERPIECE/LEGENDARY`
- 이정표 JSON: +10/+30/+50에서 slot 1/2/3 추가, +100까지 반복 강화
- 최신: 계보 1 + 보조 2, +49→+50 일반/고위 경로

`BS-MIGRATION-20260801-01`로 목표 이전 규칙은 해결됐지만 런타임·데이터·fixture는 열려 있다.

### 4.5 자동 단조는 핵심 결정을 우회한다

현재 자동 단조는:

- 목표 단계까지 반복
- 정밀 위치 무작위 자동 판정
- 특수재료 빈 fallback 허용
- 파괴 후 새 철검 반복
- 보관함이 찰 때까지 반복

을 수행한다. +5 완성 판단, +10~+40 정체성, +49 경로, 판매·인계 같은 최신 선택 경계에서 멈추지 않는다.

**연결:** `BS-AUD-F06`.

### 4.6 고객·세계 결과는 여전히 단일 PoC다

장비 생애 컨트롤러는 기본 고객을 `gladiator_kyle`, 세계 event를 `gladiator_match`로 사용하고 관계를 단일 정수로 관리한다. 최신 4유형·고객별 관계·유형별 결과 파이프라인과 불일치한다.

**연결:** `BS-AUD-F07~F09`.

## 5. Sheet 적대적 검토

### SHEET-F01 — 현재 Gate 오표기

- `00_프로젝트_허브`: planning complete 후보로 표시
- `01_작업순서`: 기획 완료 선언 준비로 표시
- `10_제품방향`: 오래된 PR #61 Gate 참조

**판정:** MUST_FIX.

### SHEET-F02 — CURRENT 원장에 역사 결정 혼재

`02_현재_확정결정`에 SUPERSEDED 제작 등급 결정이 남아 있다. 동일 이력은 `99_변경이력`에 보존돼 있으므로 CURRENT 원장에서는 제거 가능하다.

**판정:** MUST_FIX_WITH_HISTORY_PRESERVATION.

### SHEET-F03 — 수식 오인 오류

- `03_근거_라이브러리`: `=+5...` 문구가 `#ERROR!`
- `71_이미지기획_생성목록`: 같은 유형의 `#ERROR!`

**판정:** MUST_FIX.

### SHEET-F04 — 구형 모닥 표현

`70_아트_오디오_에셋`의 BS-A-03은 아직 `숯 불씨 정령`을 사용한다. 승인된 밝은 불 정령·숯 껍질 없음과 직접 충돌한다.

**판정:** MUST_FIX.

### SHEET-F05 — 대표 고객 콘텐츠 미완성

`14_조연_세력_관계`의 모험가·군인 대표 이름이 미정이다. 유형별 최소 2명 데이터 계약과 대표 검증 시나리오를 작성하려면 이름·가치관·요청·결과 템플릿이 필요하다.

**판정:** P0-3 PLANNING OPEN.

### SHEET-F06 — 경제 수치의 증거 수준 불명확

`41_성장_경제`에는 +100 가격, 보호 비용, 실패 보정 등 구형 시뮬레이션 수치가 현재값처럼 보인다. 최신 v9 마이그레이션·고객 경제·+50 경로 검증 전에는 `LEGACY_BASELINE / TUNING_REQUIRED`로 표시해야 한다.

**판정:** SHOULD_FIX.

### SHEET-F07 — 이미지 검수 증거 부족

`72_이미지검수_승인로그`는 초기 UI v0 한 건만 있고 모두 NOT_RUN이다. 그림체와 모닥은 방향 승인됐지만 실제 제품 에셋·화면 가독성·권리 검수는 수행되지 않았다.

**판정:** KEEP_NOT_RUN / ADD_DIRECTION_LOG.

### SHEET-F08 — 에셋·라이선스 원장 부재

탭 70~72는 아트 방향·이미지 기획·검수이며 실제 Asset Manifest·License Ledger를 대체하지 않는다.

**판정:** `BS-AUD-F24` OPEN.

### SHEET-F09 — 상태·근거 태그 불균일

여러 탭에서 CURRENT·PROPOSED·LEGACY·PLACEHOLDER 구분 없이 과거 PR 수치와 최신 정본이 섞인다.

**판정:** PROPAGATION_AUDIT_REQUIRED.

## 6. Design Document Registry 판정

현재 Registry는 다음 과거 문서를 ACTIVE/CURRENT로 유지한다.

- 장비 생애 PoC 통합 명세
- 구형 구현 계획
- 과거 최종 적대적 검토 보고서
- +100 강화 범위

하지만 저장·v9 결정·Base 분석·Pass2 감사가 등록되지 않았다. `FINAL_ADVERSARIAL_REVIEW_REPORT`를 현재 최종 검토로 오인할 위험이 있다.

**판정:** MUST_UPDATE_REGISTRY.

## 7. Base 운영 무결성 연결

`BS-BASE-AUDIT-20260801-01`의 `BASE-F01~F11`을 확인했다.

- canonical adapter v9.1
- protected baseline stale
- Sheet binding conflict
- Base rules/adoption provenance drift
- Snapshot·Router·Health regeneration required
- 최신 Base main/v9.4 직접 pin 금지

이 문제는 제품 게임 규칙 Finding 수를 늘리지 않지만 Base shared route와 Codex 인계 전 해결해야 한다.

## 8. 즉시 안전 수정 범위

다음은 새 게임 규칙을 발명하지 않고 현재 승인 정본에 맞출 수 있다.

1. Sheet 00·01·10의 Gate를 `PLANNING_REMEDIATION_IN_PROGRESS / NOT_READY`로 수정
2. Sheet 03·71 수식 오류를 문자열로 교정
3. Sheet 70 모닥 표현을 밝은 불 정령으로 교정
4. Sheet 02의 SUPERSEDED 등급 행을 99 이력 보존 확인 후 CURRENT 원장에서 제거
5. Sheet 41 구형 경제 수치 상태를 `LEGACY_BASELINE / TUNING_REQUIRED`로 명시
6. Sheet 72에 그림체·모닥 방향 승인과 최종 에셋 미검증을 기록
7. Design Document Registry에 최신 저장·마이그레이션·Base 분석·Pass2 감사 등록
8. START_HERE·ACTIVE_CONTEXT·ROADMAP·DEVELOPMENT_GATES를 현재 Gate로 정리

## 9. 남은 기획 순서

```text
A. 즉시 정본·Sheet 정합성 수정
B. Base v9.3 adapter migration 설계·실행 환경 준비
C. P0-3 고객 4유형 공통 데이터·화면·관계·세계 결과 계약
D. P0-4 자동 단조 정지·수동 승인 경계
E. P0-5 비주얼 Placeholder·Asset/License 구조 정리
F. P1 Theme·Scene·안전 영역·설정·Android lifecycle
G. 최신 validator·fixture·E2E·시각 회귀 계획
H. 적대적 검토 Pass 3
```

## 10. 현재 판정

```text
CORE_DIRECTION: COMPLETE
VISUAL_DIRECTION: COMPLETE
SAVE_DESIGN_AND_PLAN: COMPLETE
V9_MIGRATION_DESIGN_AND_PLAN: COMPLETE
BASE_ANALYSIS: COMPLETE

CANON_AND_SHEET_REMEDIATION: IN_PROGRESS
BASE_ADAPTER_MIGRATION: REQUIRED
CUSTOMER_COMMON_CONTRACT: PARTIAL
AUTO_FORGE_BOUNDARY: OPEN
ASSET_LICENSE_STRUCTURE: OPEN
THEME_ANDROID_SETTINGS: OPEN

PRODUCT_CODE_CHANGE: NOT_RUN
CURRENT_V9_AUTOMATED_TESTS: NOT_RUN
ANDROID_HUMAN_VALIDATION: NOT_RUN
READY_FOR_기획_완료: NO
CODEX_IMPLEMENTATION: BLOCKED
```
