# Blacksmith v9 승인 결정 정본 인덱스

> 상태: `USER_APPROVED_DECISIONS / CANONICAL_ID_INDEX`
>
> 기준일: `2026-08-01`
>
> 기계 판독본: `docs/planning/data/blacksmith_v9_canonical_decision_set_2026.json`
>
> 동기화 계약: `BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md`

## 목적

사용자 승인 내용을 Decision ID로 정규화해 GitHub 권위 문서·계획 JSON·Google Sheet가 같은 결정을 참조하도록 한다. 의미가 변경된 결정은 기존 ID를 덮어쓰지 않고 신규 ID로 대체 관계를 기록한다.

## 승인 결정 목록

| Decision ID | 영역 | 승인 내용 | 상태 |
|---|---|---|---|
| `BS-V9-20260731-01` | 제작 등급 | 보통→양질→우수→명품→걸작 | `SUPERSEDED_BY_BS-GRADE-20260801-01` |
| `BS-GRADE-20260801-01` | 제작 등급 | 보통→우수→명품→걸작 | USER_APPROVED |
| `BS-V9-20260731-02` | 수식어 | 계보 1개 + 보조 최대 2개 | USER_APPROVED |
| `BS-V9-20260731-03` | 이정표 | +10·20·30·40·50 성공 후 별도 실패 없이 정체성 선택 | USER_APPROVED_CLARIFIED |
| `BS-V9-20260731-04` | 고객 거래 | 범주 거래 자격과 공개 적합도 분리 | USER_APPROVED |
| `BS-V9-20260731-05` | 장비 운명 | 정상·전투 흔적·분실·회수·영구 파괴, 수치 내구도 없음 | USER_APPROVED |
| `BS-V9-20260731-06` | 대표 콘텐츠 | 카시아 대표 + 에르사 재사용 증명 | USER_APPROVED_CLARIFIED |
| `BS-V9-20260731-07` | 명작 전당 | +50 이상 선택 등록, 검증 랭킹·레거시 전시 분리 | USER_APPROVED_FUTURE |
| `BS-V9-20260731-08` | 작업 원칙 | 새 시스템·핵심 규칙·콘텐츠 구조·주요 UX 전 벤치마킹 | USER_APPROVED |
| `BS-CUST-20260731-01` | 고객 구조 | 수집가·모험가·검투사·군인 4유형 × 유형별 복수 이름 고객 | USER_APPROVED |
| `BS-ENH-20260731-01` | +50 강화 | 일반 정밀강화 / 특수재료 고위 정밀강화 | USER_APPROVED |
| `BS-SCREEN-20260731-01` | 기술 화면 명세 | 필수 화면 감사→상황 P0~P3→P0 A~T Godot 명세 | USER_APPROVED_WORK_ORDER |
| `BS-SCREEN-20260731-02` | 비주얼 보드 | 비주얼 기준→필수 화면→핵심 시퀀스→기술 부록 | USER_APPROVED_WORK_ORDER |
| `BS-ART-20260731-01` | 그림체 | 스타일라이즈드 다크 포지 | USER_APPROVED |
| `BS-MODAK-20260731-01` | 마스코트 | C안 표정 기반 밝은 불 정령 모닥, 숯 껍질 없음 | USER_APPROVED |
| `BS-MAIN-20260801-01` | 앱 진입 | 별도 메인 화면, 이어하기·새 게임·설정 | USER_APPROVED |
| `BS-SHELL-20260801-01` | 제품 화면 구조 | 단일 BlacksmithApp + View·Overlay 혼합 | USER_APPROVED |
| `BS-SYNC-20260731-01` | 운영 | 승인 결정·감사 상태를 같은 ID로 GitHub·Sheet 즉시 동기화 | USER_APPROVED |

## 제작 등급 최신 정본

책임 원본:

- `docs/planning/BLACKSMITH_CRAFTSMANSHIP_GRADE_CANON_2026-08-01.md`
- `docs/planning/data/blacksmith_craftsmanship_grade_canon_2026-08-01.json`

```text
보통 → 우수 → 명품 → 걸작
```

- 총 4단계다.
- `양질`은 현행 등급에서 제거한다.
- 제작 등급은 단조 완료 시 확정되는 영구 작품 정보다.
- 강화 단계·계보·보조·+50 경로·운명 상태와 분리한다.
- 네 등급 모두 강화·보관·판매 가능한 유효 완성품이다.
- `전설`은 제작 등급이 아니다.
- 내부 런타임 ID·구형 5개 ID의 변환표·확률·배율은 P0-2 마이그레이션 설계에서 별도 승인한다.

## 제작·강화 나머지 계약

```text
작품 정체성: 계보 1개 + 보조 최대 2개
```

- +10: 계보 선택
- +20: 보조 1개 선택
- +30: 계보 강화·파생 선택
- +40: 보조 2개째 선택
- +50: `BS-ENH-20260731-01`의 두 경로
- +60 이상: 새 슬롯 없이 기존 정체성 심화
- 이정표 진입 성공 뒤 두 번째 실패 판정 금지

```text
+49→+50
├─ 일반 정밀강화: 기존 위험, 특수 수식어 없음
└─ 고위 정밀강화: 특수재료, 성공 확정, 후보 2~3개, 특수 수식어
```

일반 +50도 정상 완성품이며 +51 이상과 명작 전당 자격을 가진다.

## 고객·장비 생애

```text
고객 유형 = 수집가·모험가·검투사·군인
유형별 이름 고객 최소 2명
동시 활성 요청 최대 2개
```

- 카시아는 검투사 대표, 에르사는 수집가 대표다.
- 고객은 공통 요청·거래·소유권·결과·저장 파이프라인을 공유한다.
- 거래 자격은 범주·제작 완료·판매 가능·플레이어 보유로 판단한다.
- 적합도는 제작 등급·수식어·진화·연대기와 고객 가치관의 일치 이유를 공개한다.
- 낮은 적합도도 판매 가능하며 자동 추천·자동 선택을 금지한다.

## 비주얼·화면

- 그림체: 스타일라이즈드 다크 포지
- 장비가 화면의 시각적 주인공
- 어두운 대장간·따뜻한 불빛·철·황동 UI
- 모닥: 밝은 노랑·황금·주황 불꽃, 차분한 표정 7종, 비성장형 동반자
- 별도 메인 화면 뒤 단일 `BlacksmithApp` 제품 Shell로 진입한다.
- 화면 전환으로 상태를 재생성하거나 비가역 결과를 재추첨하지 않는다.

## 비주얼 작업안 경계

`BS-VISUAL-20260731-01`은 `USER_ACCEPTED_WORKING_BASELINE`이며 최종 제품 에셋이 아니다.

다음은 `PLACEHOLDER / NOT_CANON`이다.

- 플레이어 레벨
- 청색 보석·프리미엄 재화
- 업적·상점
- 상세 도감·가이드
- 별도 특수 제작 시스템
- 보관함 128/150
- 시장·경기장 직접 탐색
- 시안의 확률·재화·장비 수치

## 감사 연결

최신 기존 프로젝트 감사:

- Audit ID: `BS-REPO-AUDIT-20260801-01`
- P0 10건 / P1 10건 / P2 6건
- `BS-AUD-F04`의 목표 등급 구조는 `BS-GRADE-20260801-01`로 명확해졌지만 실제 main의 구형 5개 ID·분포·고객 점수·테스트 마이그레이션은 계속 열린 P0다.

## 권한

```text
사용자 최신 결정
→ BLACKSMITH_CRAFTSMANSHIP_GRADE_CANON_2026-08-01.md
→ BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md
→ BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md
→ BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md와 최신 Addendum
→ BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md
→ BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md
→ 본 ID 인덱스와 연결 계획 JSON
→ 연결 Google Sheet
```

## 동기화 상태

```text
GITHUB_AUTHORITY: GITHUB_DRAFT_COMMITTED
PLANNING_DATA: UPDATED
GOOGLE_SHEET: SYNCED_TO_DRAFT_PR81
CROSS_SOURCE_VERIFICATION: PASS
MAIN_MERGE: NOT_RUN
USER_기획_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```
