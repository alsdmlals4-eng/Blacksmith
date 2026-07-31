# 블랙스미스 프로젝트 Google Sheets Workbook

```yaml
project: Blacksmith
sheet_status: UPDATE_REQUIRED_FOR_20260801_DECISIONS_AND_AUDIT
spreadsheet_url: https://docs.google.com/spreadsheets/d/1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg/edit
spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
workbook_role: USER_FACING_GDD_WORKSPACE
sheet_edit_policy: IMMEDIATE_CANONICAL_SYNC_FOR_APPROVED_DECISIONS_AND_SHARED_PLANNING_FINDINGS
sync_contract_decision_id: BS-SYNC-20260731-01
latest_customer_decision_id: BS-CUST-20260731-01
latest_enhancement_decision_id: BS-ENH-20260731-01
latest_visual_work_order_decision_id: BS-SCREEN-20260731-02
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

Google Sheets는 제작·강화·장비 연대기·고객·경제와 화면 기획의 전체 흐름을 사용자가 확인·수정하는 GDD 작업면이다.

## 동기화 계약

```text
승인 결정 또는 공유할 감사·설계 상태
→ GitHub 권위 Markdown·계획 JSON 커밋
→ 같은 Decision ID·Audit ID·Design ID로 Sheet 갱신
→ 변경이력에 경로·범위·PR·커밋 기록
→ 양쪽 재조회
```

상태 규칙:

- 병합 전: `SYNCED_TO_DRAFT`와 PR·브랜치 commit 기록
- 병합 후: 같은 ID를 `SYNCED_TO_MAIN`과 merge commit으로 갱신
- 일부 실패: `PARTIAL_SYNC_BLOCKED`와 실패 범위 기록
- Draft를 main 정본으로 표시하지 않음
- 승인 전 설계안은 `PROPOSED_REVIEW_REQUIRED`로 기록
- 사용자가 작업 기준안으로 승인한 설계는 `USER_ACCEPTED_WORKING_BASELINE`으로 기록하되 최종 에셋과 분리

## 주요 ID의 Sheet 전파 범위

### BS-CUST-20260731-01

- `02_현재_확정결정`
- `05_GDD_요약`
- `13_주요인물`
- `14_조연_세력_관계`
- `20_코어경험_데모목표`
- `30_데모범위_품질기준_제작기반`
- `50_메인콘텐츠`
- `80_데모_버티컬슬라이스_플레이테스트`
- `90_본제작_출시_사업`

### BS-ENH-20260731-01

- `02_현재_확정결정`
- `05_GDD_요약`
- `30_데모범위_품질기준_제작기반`
- `40_핵심시스템_메인콘텐츠`
- `41_성장_경제`
- `50_메인콘텐츠`
- `60_UX_UI_접근성`
- `80_데모_버티컬슬라이스_플레이테스트`
- `90_본제작_출시_사업`

### BS-SCREEN-20260731-01·02

- `02_현재_확정결정`
- `04_누락_충돌_감사`
- `05_GDD_요약`
- `90_본제작_출시_사업`
- `98_Base_반영후보`
- `99_변경이력`

### BS-VISUAL-20260731-01

- `04_누락_충돌_감사`: 설계 상태·근거 태그·작업 기준 승인 상태
- `05_GDD_요약`: 메인·필수 화면·시퀀스·전환도 요약
- `60_UX_UI_접근성`: 화면별 첫 3초 정보 위계와 상태 변형
- `98_Base_반영후보`: 공통 비주얼 보드 템플릿 후보
- `99_변경이력`: GitHub 경로·PR·commit·Sheet 범위

### BS-ART-20260731-01

- `02_현재_확정결정`: 스타일라이즈드 다크 포지 승인
- `04_누락_충돌_감사`: DEC-VIS-03 해결 기록
- `05_GDD_요약`: 아트·사운드 방향
- `60_UX_UI_접근성`: 화면 재질·정보 가독성 규칙
- `99_변경이력`: 변경 위치·커밋

### BS-MODAK-20260731-01

- `02_현재_확정결정`: 밝은 불 정령 모닥 승인
- `04_누락_충돌_감사`: 숯 껍질 구형안 대체 기록
- `05_GDD_요약`: 상징 요소·마스코트 방향
- `13_주요인물`: 외형·표정·기능 경계
- `60_UX_UI_접근성`: UI 비가림·상태 반응 규칙
- `99_변경이력`: 변경 위치·커밋

### BS-MAIN-20260801-01

- `02_현재_확정결정`: 별도 메인 화면 승인
- `04_누락_충돌_감사`: 기본 실행 테스트 Scene 충돌
- `05_GDD_요약`: 앱 진입·새 게임·이어하기
- `60_UX_UI_접근성`: 메인 화면 상태와 정보 위계
- `90_본제작_출시_사업`: 제품 진입 Gate
- `99_변경이력`: 변경 위치·커밋

### BS-SHELL-20260801-01

- `02_현재_확정결정`: 단일 App Shell·View·Overlay 혼합 승인
- `04_누락_충돌_감사`: 세 흐름의 상태 소유권 충돌
- `05_GDD_요약`: 화면 전환·상태 유지
- `60_UX_UI_접근성`: 화면 전환·Overlay 규칙
- `90_본제작_출시_사업`: 제품 Shell Gate
- `99_변경이력`: 변경 위치·커밋

### BS-REPO-AUDIT-20260801-01

- `04_누락_충돌_감사`: P0 10·P1 10·P2 6 요약 및 우선순위
- `05_GDD_요약`: 현재 제품 정합화 상태
- `30_데모범위_품질기준_제작기반`: Vertical Slice 차단 Finding
- `40_핵심시스템_메인콘텐츠`: 제작 등급·수식어·+50·자동화 충돌
- `50_메인콘텐츠`: 고객·세계 결과·연대기 충돌
- `60_UX_UI_접근성`: 메인·Shell·설정·안전 영역·Placeholder
- `80_데모_버티컬슬라이스_플레이테스트`: 신규 검증 범위
- `90_본제작_출시_사업`: 구현 차단·출시 전 Gate
- `99_변경이력`: GitHub 경로·PR·commit·Sheet 범위

## 프로젝트 책임 매핑

| 의미 구조 | 프로젝트 책임 원본 |
|---|---|
| 별도 메인·제품 Shell | `docs/planning/BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md`, 연결 JSON |
| 기존 프로젝트 최신 적대적 감사 | `docs/planning/BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md`, 연결 JSON |
| 비주얼 중심 화면 작업 계약 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_WORK_ORDER_2026.md` |
| 현재 비주얼 화면 작업 기준 | `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_DESIGN_V1_2026.md`, 연결 JSON |
| 승인된 그림체·모닥 | `docs/planning/BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md`, 연결 JSON |
| 기술 화면 작업 계약 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md` |
| 초기 실제 파일 중간점검 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_MID_CHECK_2026.md`, 연결 JSON |
| 최신 고객·+50 정합화 | `docs/planning/BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` |
| 현행 통합 기획 | `docs/planning/BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` |
| 승인 결정 ID | `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, 연결 JSON |
| 정본 동기화 | `docs/planning/BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md` |
| 핵심루프 | 단조→강화→+5 완성/+10 도전→고객·세계 환류→+50 장기 명작 |
| +50 강화 | 일반 정밀강화 또는 특수재료 기반 고위 정밀강화 |
| 고객 구조 | 수집가·모험가·검투사·군인 4유형 × 유형별 복수 이름 고객 |
| 그림체 | 스타일라이즈드 다크 포지 |
| 모닥 | C안 표정 기반 밝은 불 정령, 숯 껍질 미사용 |
| 제품 진입 | 별도 메인 화면 → 새 게임/이어하기 → BlacksmithApp |
| 제품 Shell | 단일 캠페인 상태 + View·Overlay 혼합 |
| 첫 5분 UX | `docs/planning/BLACKSMITH_FIRST_FIVE_MINUTES_AND_MASTERWORKS_UX_2026.md` |
| 이미지 계획·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md` |

## 현재 화면·감사 상태

```text
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

READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
CODEX_IMPLEMENTATION: BLOCKED
```

비주얼 시안의 다음 항목은 `PLACEHOLDER / NOT_CANON`이다.

- 플레이어 레벨
- 청색 보석·프리미엄 재화
- 업적·상점
- 상세 도감·가이드
- 별도 특수 제작 시스템
- 보관함 128/150
- 시장·경기장 직접 탐색
- 시안의 수치

## 편집 정책

- GitHub에 없는 사용자 수정은 승인 전 `PROPOSED_SHEET_CHANGE`다.
- 사용자가 승인하면 새 Decision ID를 부여하고 GitHub·Sheet 양쪽에 즉시 정본 동기화한다.
- 감사 Finding은 Audit ID, 승인 전 설계안은 Design ID로 분리한다.
- Sheet의 `+` 시작 문구는 문자열로 기록해 수식 오류를 방지한다.
- 모든 쓰기 후 변경 범위를 재조회한다.
- 사용자 `기획 완료` 전 제품 구현과 Codex Goal은 차단한다.
- P0 Finding이 열린 동안 `READY_FOR_USER_기획_완료_DECLARATION`으로 복귀하지 않는다.
