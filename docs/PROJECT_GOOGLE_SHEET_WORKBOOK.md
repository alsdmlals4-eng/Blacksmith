# 블랙스미스 프로젝트 Google Sheets Workbook

```yaml
project: Blacksmith
sheet_status: PROJECT_SHEET_CONFIGURED
spreadsheet_url: https://docs.google.com/spreadsheets/d/1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg/edit
spreadsheet_id: 1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg
workbook_role: USER_FACING_GDD_WORKSPACE
sheet_edit_policy: PROPOSED_SHEET_CHANGE
base_version: 9.4.0
base_payload_commit: a728712cb776ec98f4875914a580fcf7d0156593
base_trusted_evidence_commit: ef1fba11167e4da0b298123b0c85ebd268191a42
last_verified_at: 2026-08-06
```

Google Sheets는 제작·강화·장비 연대기·고객·경제의 전체 흐름을 사용자가 확인·수정하고 AI가 GitHub 정본·실제 구현과 함께 읽는 GDD 작업면이다.

## 검증된 탭
- `00_프로젝트_허브`
- `01_작업순서`
- `02_현재_확정결정`
- `03_근거_라이브러리`
- `04_누락_충돌_감사`
- `05_GDD_요약`
- `10_제품방향`
- `11_세계관`
- `12_핵심루프`
- `13_주요인물`
- `14_조연_세력_관계`
- `15_조작_게임규칙`
- `20_코어경험_데모목표`
- `30_데모범위_품질기준_제작기반`
- `40_핵심시스템_메인콘텐츠`
- `41_성장_경제`
- `50_메인콘텐츠`
- `60_UX_UI_접근성`
- `70_아트_오디오_에셋`
- `71_이미지기획_생성목록`
- `72_이미지검수_승인로그`
- `80_데모_버티컬슬라이스_플레이테스트`
- `90_본제작_출시_사업`
- `98_Base_반영후보`
- `99_변경이력`

## 프로젝트 책임 매핑

| 의미 구조 | 프로젝트 책임 원본 |
|---|---|
| 핵심루프 | 단조→강화→+5 납품/+10 도전→고객·시장 환류 |
| 핵심시스템 | `BLACKSMITH_GAME_BIBLE.md`, 강화·보호·장비 생애주기 결정 정본 |
| 성장·경제 | 골드·보호석·완충 충전·고강화 시장 정본 |
| 주요인물·관계 | 대장장이·고객4종·상인·검투사 기획 정본 |
| 이미지 계획·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md` |

GitHub에 없는 사용자 수정은 `PROPOSED_SHEET_CHANGE`로 보존하고 승인 후 양쪽을 재조회한다.
