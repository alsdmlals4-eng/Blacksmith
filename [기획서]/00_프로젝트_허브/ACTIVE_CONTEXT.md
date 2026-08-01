# Active Context

- 갱신일: `2026-08-01`
- Work Mode: `PLAN → REVIEW`
- 현재 브랜치: `docs/blacksmith-v9-planning-audit`
- 현재 PR: `#81 Draft / NOT_MERGED`
- 현재 Issue: `#79`
- 대상 제품 main: `500a5a7960146ef229ae172cf9e127306d23f073`
- 현재 단계: `PLANNING_REMEDIATION_IN_PROGRESS`
- 제품 구현 권한: `NONE`

## 1. 현재 판정

| 영역 | 상태 |
|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / KEEP` |
| 승인 결정 인덱스 | `CURRENT / CROSS_SOURCE_SYNC` |
| 그림체·모닥·화면 구조 | `USER_APPROVED` |
| 제작 등급 5단계 | `USER_APPROVED` |
| 세이브·ResultEnvelope | `DESIGN_COMPLETE / 11-TASK_PLAN_COMPLETE` |
| v9 데이터 마이그레이션 | `DESIGN_COMPLETE / 7-TASK_PLAN_COMPLETE` |
| Base current 구조 분석 | `COMPLETE` |
| Base v9.3 프로젝트 이관 | `REQUIRED / NOT_RUN` |
| GitHub·Sheet 적대적 검토 | `PASS2_COMPLETE / REMEDIATION_IN_PROGRESS` |
| 고객 공통 계약 | `PARTIAL` |
| 자동 단조 최신 경계 | `OPEN` |
| Theme·Android·설정 | `OPEN` |
| 제품 기획 Finding | `P0 10 / P1 10 / P2 6` |
| 런타임·Android·사람 검증 | `NOT_RUN` |
| Codex 구현 | `BLOCKED` |

## 2. 현재 제품 방향

> 한 명의 대장장이가 장비 한 점을 직접 만들고 강화 위험과 정체성을 선택하며, 장비가 다른 이의 손에서 만든 사건과 역사를 다시 돌려받는 Android 세로형 제작 게임.

불변 경계:

- 단일 대장장이
- 직접 제작과 장비 중심 화면
- 제작 등급은 작품의 영구 정보
- 일반 강화 입력당 결과 1회
- 계보 1개 + 보조 최대 2개
- 비가역 결과 재추첨·이중 적용 금지
- 판매·인계 후 장비 UID·소유권·연대기 보존
- 직원·직접 전투·생산 예약·일상 수리 루프 제외

## 3. 현행 승인 결정

- `BS-GRADE-20260801-02`: 보통→우수→명품→걸작→전설
- `BS-SAVE-20260801-01`: 단일 캠페인·자동 백업2·AttemptIntent·ResultEnvelope
- `BS-MIGRATION-20260801-01`: 구형 등급·수식어·+50 결정론적 마이그레이션
- `BS-MAIN-20260801-01`: 별도 메인
- `BS-SHELL-20260801-01`: 단일 BlacksmithApp + View·Overlay
- `BS-ART-20260731-01`: 스타일라이즈드 다크 포지
- `BS-MODAK-20260731-01`: 밝은 불 정령 모닥
- `BS-CUST-20260731-01`: 고객 4유형 × 복수 이름 고객
- `BS-ENH-20260731-01`: +49→+50 일반/고위 정밀강화

상세와 대체 관계는 `CURRENT_CONFIRMED_DECISIONS.md`와 결정 인덱스를 따른다.

## 4. 실제 main 구현 사실

- 기본 실행 Scene: `res://scenes/test/enhancement_test.tscn`
- 제작·강화·6칸 보관함·자동 단조 PoC 존재
- 장비 생애는 카일·철검·검투사 경기 중심
- 제작 등급은 구형 `APPRENTICE~PERFECT`
- 강화는 구형 3수식어 슬롯·10단위 특수 강화
- 저장은 메모리 Snapshot/rollback 수준이며 제품 영속 저장 없음
- 주요 UI는 GDScript 런타임 조립
- 기존 CI는 PoC 계약을 검증하며 최신 v9 fixture는 없음

## 5. Base 운영 상태

```text
Base latest main observed: 90ec6f33953f80f607d4e79f58cc2174eb178f73
Target released line: Base v9.3.0
release: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
evidence: 462a86db192d23d0f386281a1eb54b0a8cbad62e
```

Blacksmith canonical adapter는 아직 v9.1이며 protected baseline·Sheet binding·Registry provenance·generated Snapshot/Router/Health가 현행 상태와 충돌한다. latest Base main과 미출시 v9.4 제안을 직접 pin하지 않는다.

## 6. 현재 책임 원본

- 결정 발견: `CURRENT_CONFIRMED_DECISIONS.md`
- 결정 인덱스: `docs/planning/BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`, JSON
- 현재 Gate: `docs/planning/BLACKSMITH_REMAINING_PLANNING_STATUS_2026.md`
- Pass2 감사: `docs/planning/BLACKSMITH_FULL_GITHUB_SHEET_ADVERSARIAL_REVIEW_2026-08-01.md`, JSON
- Base 분석: `docs/planning/BLACKSMITH_BASE_CURRENT_SKILLS_AND_WORKFLOW_ANALYSIS_2026-08-01.md`, JSON
- 저장 정본·계획: `BLACKSMITH_SAVE_CONTINUE_RESULT_ENVELOPE_CANON_2026.md`, 연결 계획
- 마이그레이션 정본·계획: `BLACKSMITH_V9_DATA_AND_LEGACY_MIGRATION_CANON_2026.md`, 연결 계획
- Google Sheet binding: `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`

## 7. 현재 작업

```text
1. 시작 문서·Registry·Sheet 정합성 교정
2. Base v9.3 adapter migration 준비
3. P0-3 고객 4유형 공통 데이터·화면 계약
4. P0-4 자동 단조 정지 경계
5. P0-5 비주얼 Placeholder·Asset/License 정리
6. P1 Theme·안전 영역·설정·Android lifecycle
7. 최신 validator·fixture·E2E 계획
8. 적대적 검토 Pass 3
```

## 8. 완료 금지

- 기존 PoC 자동 PASS를 최신 v9 PASS로 재사용하지 않는다.
- 문서 설계 완료를 런타임 구현 완료로 표시하지 않는다.
- Base adapter generator·validator를 실행하지 않은 상태에서 operating integrity PASS를 주장하지 않는다.
- P0/P1 Finding이 열려 있으면 사용자 기획 완료 후보로 표시하지 않는다.
- Android·사람·성능 증거가 없으면 플랫폼·접근성·Production 완료로 표시하지 않는다.
