# Blacksmith Current Confirmed Decisions

> 역할: `CURRENT_CONFIRMED_DECISIONS / STABLE_ENTRYPOINT`
>
> 상태: `CURRENT / DETAIL_BY_REFERENCE`
>
> 기준일: `2026-08-01`
>
> 추적: Issue #79 / Draft PR #81

이 파일은 현재 승인 결정의 **발견 경로와 대체 관계**만 책임진다. 시스템 상세 규칙을 복제하지 않는다.

## 현행 결정 인덱스

- 사람용 정본: `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`
- 기계 판독 정본: `docs/planning/data/blacksmith_v9_canonical_decision_set_2026.json`
- 사용자 GDD 작업면: `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`
- 현재 단계·남은 Gate: `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md`

## 현재 핵심 Decision

| Decision ID | 영역 | 현재 결정 | 상세 책임 원본 |
|---|---|---|---|
| `BS-GRADE-20260801-02` | 제작 등급 | 보통→우수→명품→걸작→전설 | `BLACKSMITH_CRAFTSMANSHIP_GRADE_CANON_2026-08-01.md` |
| `BS-SAVE-20260801-01` | 저장·복구 | 단일 캠페인·자동 백업 2개·AttemptIntent·ResultEnvelope | `BLACKSMITH_SAVE_CONTINUE_RESULT_ENVELOPE_CANON_2026.md` |
| `BS-MAIN-20260801-01` | 앱 진입 | 별도 메인 화면 | `BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md` |
| `BS-SHELL-20260801-01` | 화면 구조 | 단일 BlacksmithApp + View·Overlay 혼합 | 같은 문서 |
| `BS-ART-20260731-01` | 그림체 | 스타일라이즈드 다크 포지 | `BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md` |
| `BS-MODAK-20260731-01` | 모닥 | 밝은 불 정령·C안 표정·숯 껍질 없음 | 같은 문서 |
| `BS-CUST-20260731-01` | 고객 | 4유형 × 유형별 복수 이름 고객 | `BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md` |
| `BS-ENH-20260731-01` | +50 | 일반 정밀강화 / 고위 정밀강화 | 같은 문서 |

전체 승인 목록·예외·Sheet 위치는 정본 인덱스를 따른다.

## 대체된 결정

| 이전 ID | 상태 | 대체 결정 |
|---|---|---|
| `BS-V9-20260731-01` | SUPERSEDED | `BS-GRADE-20260801-02` |
| `BS-GRADE-20260801-01` | SUPERSEDED | `BS-GRADE-20260801-02` |

대체된 결정은 구현 근거로 사용하지 않는다. 역사와 변경 이력에서만 보존한다.

## 현재 감사·운영 상태

- 기존 프로젝트 감사: `BS-REPO-AUDIT-20260801-01`
- Base 구조 분석: `BS-BASE-AUDIT-20260801-01`
- 제품 기획 Finding: P0 10 / P1 10 / P2 6
- Base adapter v9.3 migration: REQUIRED / NOT_RUN
- 제품 코드·Scene·런타임 데이터 변경: NOT_RUN
- 사용자 `기획 완료`: NOT_DECLARED
- 사용자 `검수 완료`: NOT_DECLARED
- Codex 구현: BLOCKED

## 권한 순서

```text
최신 사용자 승인
→ 본 파일의 CURRENT Decision 발견 경로
→ 등록된 분야 책임 원본 Markdown·JSON
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 연결 Google Sheet
→ Issue·PR·Commit 이력
```

실제 구현과 승인 정본이 다르면 어느 쪽도 자동으로 덮어쓰지 않고 `CANON_CONFLICT`로 감사한다.
