# 블랙스미스 프로젝트 Google Sheets Workbook

```yaml
project: Blacksmith
sheet_status: SYNC_PENDING_FINAL_HEAD
spreadsheet_url: https://docs.google.com/spreadsheets/d/1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg/edit
spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
workbook_role: USER_FACING_GDD_WORKSPACE
sheet_edit_policy: IMMEDIATE_CANONICAL_SYNC_FOR_APPROVED_DECISIONS_AND_SHARED_PLANNING_FINDINGS
sync_contract_decision_id: BS-SYNC-20260731-01
latest_grade_decision_id: BS-GRADE-20260801-02
superseded_grade_decision_ids:
  - BS-V9-20260731-01
  - BS-GRADE-20260801-01
latest_customer_decision_id: BS-CUST-20260731-01
latest_enhancement_decision_id: BS-ENH-20260731-01
latest_visual_design_id: BS-VISUAL-20260731-01
latest_art_style_decision_id: BS-ART-20260731-01
latest_mascot_decision_id: BS-MODAK-20260731-01
latest_main_menu_decision_id: BS-MAIN-20260801-01
latest_app_shell_decision_id: BS-SHELL-20260801-01
latest_repository_audit_id: BS-REPO-AUDIT-20260801-01
planning_pr: 81
planning_branch: docs/blacksmith-v9-planning-audit
project_main_commit_at_audit: 500a5a7960146ef229ae172cf9e127306d23f073
base_v9_3_release_commit: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
last_verified_at: 2026-08-01
```

Google Sheets는 제작·강화·장비 연대기·고객·경제와 화면 기획을 사용자가 확인·수정하는 GDD 작업면이다. GitHub Markdown·계획 JSON이 책임 정본이며 Sheet는 같은 ID로 연결된다.

## 동기화 계약

```text
승인 결정 또는 공유할 감사·설계 상태
→ GitHub 권위 Markdown·계획 JSON 커밋
→ 같은 Decision ID·Audit ID·Design ID로 Sheet 갱신
→ 변경이력에 경로·범위·PR·커밋 기록
→ 양쪽 재조회
```

- 병합 전: `SYNCED_TO_DRAFT`
- 병합 후: 같은 ID로 `SYNCED_TO_MAIN`
- 일부 실패: `PARTIAL_SYNC_BLOCKED`
- 기존 결정의 의미가 바뀌면 신규 ID와 `supersedes` 관계를 사용한다.
- 승인 전 설계: `PROPOSED_REVIEW_REQUIRED`
- 사용자 수용 작업안: `USER_ACCEPTED_WORKING_BASELINE`
- Sheet의 `+` 시작 문구는 문자열로 기록한다.

## 책임 원본

| 의미 | GitHub 책임 원본 |
|---|---|
| 제작 등급 5단계 | `docs/planning/BLACKSMITH_CRAFTSMANSHIP_GRADE_CANON_2026-08-01.md`, 연결 JSON |
| 별도 메인·제품 Shell | `docs/planning/BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md`, 연결 JSON |
| 기존 프로젝트 적대적 감사 | `docs/planning/BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md`, 연결 JSON, 최신 Addendum |
| 비주얼 작업 계약 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_WORK_ORDER_2026.md` |
| 현재 비주얼 작업 기준 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_DESIGN_V1_2026.md`, 연결 JSON |
| 그림체·모닥 | `docs/planning/BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md`, 연결 JSON |
| 기술 화면 계약 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md` |
| 고객·+50 정합화 | `docs/planning/BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` |
| 현행 통합 기획 | `docs/planning/BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` |
| 승인 결정 인덱스 | `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, 연결 JSON |
| 현재 Gate | `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md` |
| 정본 동기화 | `docs/planning/BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md` |

## 주요 ID 전파 범위

| ID | 주요 Sheet 탭 |
|---|---|
| `BS-GRADE-20260801-02` | 02·04·05·40·99 |
| `BS-CUST-20260731-01` | 02·05·13·14·20·30·50·80·90 |
| `BS-ENH-20260731-01` | 02·05·30·40·41·50·60·80·90 |
| `BS-SCREEN-20260731-01·02` | 02·04·05·90·98·99 |
| `BS-VISUAL-20260731-01` | 04·05·60·98·99 |
| `BS-ART-20260731-01` | 02·04·05·60·99 |
| `BS-MODAK-20260731-01` | 02·04·05·13·60·99 |
| `BS-MAIN-20260801-01` | 02·04·05·60·90·99 |
| `BS-SHELL-20260801-01` | 02·04·05·60·90·99 |
| `BS-REPO-AUDIT-20260801-01` | 04·05·30·40·50·60·80·90·99 |

## 제작 등급 동기화 위치

| 목적 | 범위 |
|---|---|
| 최초 5단계 결정 이력 | `02_현재_확정결정!D6:H6` |
| 직전 4단계 결정 이력 | `02_현재_확정결정!D23:H23` |
| 현행 5단계 결정 | `02_현재_확정결정!A24:H24` |
| 등급 감사 Addendum | `04_누락_충돌_감사!A18:H18` |
| GDD 게임 시스템 | `05_GDD_요약!A4:H4` |
| v9 마이그레이션 경계 | `40_핵심시스템_메인콘텐츠!A8:H8` |
| 변경이력 | `99_변경이력!A20:H20` |

## 기존 2026-08-01 동기화 위치

| 목적 | 범위 |
|---|---|
| 별도 메인 결정 | `02_현재_확정결정!A21:H21` |
| App Shell 결정 | `02_현재_확정결정!A22:H22` |
| 비주얼 작업안 상태 | `04_누락_충돌_감사!A12:H12` |
| 메인·Shell·감사 원장 | `04_누락_충돌_감사!A15:H17` |
| GDD·로드맵 요약 | `05_GDD_요약!A2:H2,A7:H7` |
| Demo·저장·정합화 | `30_데모범위_품질기준_제작기반!A2:H4` |
| PoC 콘텐츠 정합화 | `50_메인콘텐츠!A9:H9` |
| 메인·Shell·Placeholder UX | `60_UX_UI_접근성!A13:H15` |
| 신규 플레이테스트 | `80_데모_버티컬슬라이스_플레이테스트!A7:H7` |
| 제작·출시 Gate | `90_본제작_출시_사업!A2:H3` |

## 현재 판정

```text
CRAFTSMANSHIP_GRADE: 보통 > 우수 > 명품 > 걸작 > 전설
GRADE_COUNT: 5
QUALITY_GRADE_LABEL_양질: REMOVED
LEGEND_GRADE_LABEL_전설: CURRENT_TOP_GRADE
LEGACY_GRADE_RUNTIME_MIGRATION: OPEN

VISUAL_BOARD: USER_ACCEPTED_WORKING_BASELINE
ART_STYLE_DECISION: USER_APPROVED
MODAK_VISUAL_DECISION: USER_APPROVED
SEPARATE_MAIN_MENU: USER_APPROVED
APP_SHELL_VIEW_OVERLAY_MIX: USER_APPROVED
OPEN_VISUAL_DECISIONS: 0

REPOSITORY_ADVERSARIAL_AUDIT: COMPLETE
P0_FINDINGS: 10
P1_FINDINGS: 10
P2_FINDINGS: 6
TOTAL_FINDINGS: 26

CROSS_SOURCE_VERIFICATION: PENDING_FINAL_HEAD
MAIN_MERGE: NOT_RUN
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
CODEX_IMPLEMENTATION: BLOCKED
```

## 비주얼 Placeholder 경계

다음은 이미지에 등장했지만 시스템 정본이 아니다.

- 플레이어 레벨
- 청색 보석·프리미엄 재화
- 업적·상점
- 상세 도감·가이드
- 별도 특수 제작
- 보관함 128/150
- 시장·경기장 직접 탐색
- 시안의 확률·재화·장비 수치

별도 Decision ID 없이는 `PLACEHOLDER / NOT_CANON`이다.

## 편집 정책

- GitHub에 없는 Sheet 수정은 승인 전 `PROPOSED_SHEET_CHANGE`다.
- 승인 시 새 Decision ID로 GitHub·Sheet에 즉시 동기화한다.
- 감사 Finding은 Audit ID, 설계안은 Design ID로 분리한다.
- 모든 쓰기 후 변경 범위를 재조회한다.
- 사용자 `기획 완료` 전 제품 구현과 Codex Goal은 차단한다.
- P0 Finding이 열린 동안 기획 완료 선언 가능 후보로 표시하지 않는다.
