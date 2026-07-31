# 블랙스미스 프로젝트 Google Sheets Workbook

```yaml
project: Blacksmith
sheet_status: SYNCED_TO_DRAFT_PR81_CROSS_SOURCE_VERIFIED
spreadsheet_url: https://docs.google.com/spreadsheets/d/1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg/edit
spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
workbook_role: USER_FACING_GDD_WORKSPACE
sheet_edit_policy: IMMEDIATE_CANONICAL_SYNC_FOR_APPROVED_DECISIONS
sync_contract_decision_id: BS-SYNC-20260731-01
latest_customer_decision_id: BS-CUST-20260731-01
latest_enhancement_decision_id: BS-ENH-20260731-01
latest_screen_work_order_decision_id: BS-SCREEN-20260731-01
planning_pr: 81
planning_branch: docs/blacksmith-v9-planning-audit
project_main_commit_at_sync: 500a5a7960146ef229ae172cf9e127306d23f073
base_v9_3_release_commit: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
last_verified_at: 2026-07-31
```

Google Sheets는 제작·강화·장비 연대기·고객·경제의 전체 흐름을 사용자가 확인·수정하고 AI가 GitHub 정본·실제 구현과 함께 읽는 GDD 작업면이다.

## 동기화 계약

주요 변경사항과 사용자 승인 결정은 `BS-SYNC-20260731-01` 계약을 따른다.

```text
승인 결정
→ GitHub 권위 Markdown·계획 JSON 커밋
→ 같은 Decision ID로 Sheet 결정 인덱스·직접 영향 탭 갱신
→ 감사·변경이력에 경로·범위·PR·커밋 기록
→ 양쪽 재조회
```

상태 규칙:

- 병합 전: `SYNCED_TO_DRAFT`와 PR·브랜치 commit 기록
- 병합 후: 같은 Decision ID를 `SYNCED_TO_MAIN`과 merge commit으로 갱신
- 일부 실패: `PARTIAL_SYNC_BLOCKED`와 실패 범위 기록
- Draft를 main 정본으로 표시하지 않음

## 최신 결정의 Sheet 전파 범위

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

### BS-SCREEN-20260731-01

- `02_현재_확정결정`
- `04_누락_충돌_감사`
- `05_GDD_요약`
- `90_본제작_출시_사업`
- `98_Base_반영후보`
- `99_변경이력`

공통 감사·이력:

- `04_누락_충돌_감사`
- `99_변경이력`

## 프로젝트 책임 매핑

| 의미 구조 | 프로젝트 책임 원본 |
|---|---|
| 상황별 화면 중간점검 | `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md` |
| 최신 고객·+50 정합화 | `docs/planning/BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` |
| 현행 통합 기획 | `docs/planning/BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` |
| 승인 결정 ID | `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, 연결 JSON |
| 정본 동기화 | `docs/planning/BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md` |
| 핵심루프 | 단조→강화→+5 완성/+10 도전→고객·세계 환류→+50 장기 명작 |
| +50 강화 | 일반 정밀강화 또는 특수재료 기반 고위 정밀강화 |
| 고객 구조 | 수집가·모험가·검투사·군인 4유형 × 유형별 복수 이름 고객 |
| 기준 화면 초기 대응 | 대장간 허브 / 단조·강화 작업대 / 보관함·자원 관리 / 강화·고객·세계 결과 |
| 성장·경제 | +5 최초 평균 흑자, 골드·보호석·특수재료·고강화 미래 계약 |
| 첫 5분 UX | `docs/planning/BLACKSMITH_FIRST_FIVE_MINUTES_AND_MASTERWORKS_UX_2026.md` |
| 이미지 계획·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md` |

## 재검증 결과

```text
DECISION_ID_MATCH: PASS
CUSTOMER_TYPE_COUNT: 4
NAMED_CUSTOMER_MINIMUM_PER_TYPE: 2
PLUS_50_ROUTE_COUNT: 2
SPECIAL_MATERIAL_ROLES: CATALYST | SPECIAL_AUXILIARY
SITUATION_SCREEN_MID_CHECK: REQUIRED_NOT_RUN
READY_FOR_USER_기획_완료_DECLARATION: NO_PENDING_MID_CHECK
DRAFT_STATUS_DISCLOSED: PASS
```

## 편집 정책

- GitHub에 없는 사용자 수정은 승인 전 `PROPOSED_SHEET_CHANGE`다.
- 사용자가 승인하면 새 Decision ID를 부여하고 GitHub·Sheet 양쪽에 즉시 정본 동기화한다.
- Sheet의 `+` 시작 문구는 문자열로 기록해 수식 오류를 방지한다.
- 모든 쓰기 후 변경 범위를 재조회한다.
- 사용자 `기획 완료` 전 제품 구현과 Codex Goal은 차단한다.
- `BS-SCREEN-20260731-01` 중간점검 완료 전 `READY_FOR_USER_기획_완료_DECLARATION`으로 복귀하지 않는다.
