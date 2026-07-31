# Blacksmith v9 승인 결정 정본 인덱스

> 상태: `USER_APPROVED_DECISIONS / CANONICAL_ID_INDEX`
>
> 기준일: `2026-08-01`
>
> 원결정: `BLACKSMITH_V9_USER_DECISION_PACKET.md`, `BLACKSMITH_DECISION_LEDGER_ADDENDUM_20.md`, `BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md`, `BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md`
>
> 동기화 계약: `BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md`

## 목적

기존 사용자 승인 내용과 최신 보완 결정을 변경 없이 식별자 기반으로 정규화해 GitHub 계획 데이터와 Google Sheet가 동일한 Decision ID를 사용하도록 한다.

## 결정 목록

### BS-V9-20260731-01 — 제작 등급

```text
보통 → 양질 → 우수 → 명품 → 걸작
```

- 단조 시 확정되는 영구 작품 정보
- 강화 단계와 분리
- 낮은 등급도 강화·판매·보관 가능

### BS-V9-20260731-02 — 수식어 구조

```text
계보 수식어 1개 + 보조 수식어 최대 2개
```

- +50 대표 특수 형태는 새 슬롯이 아니라 계보 승격
- 무제한 슬롯 증가 금지

### BS-V9-20260731-03 — 10단위 정체성 이정표

- +10 계보 선택
- +20 보조 1개 선택
- +30 계보 강화·파생 선택
- +40 보조 2개째 선택
- +50 세부 경로는 `BS-ENH-20260731-01`이 명확화
- +60 이상 신규 슬롯 없이 심화
- 이정표 성공 후 별도 두 번째 실패 판정 금지

### BS-V9-20260731-04 — 고객 거래 자격과 공개 적합도

```text
거래 자격 = 범주 일치 + 제작 완료 + 판매 가능 + 플레이어 보유
공개 적합도 = 제작 등급·수식어·진화·연대기와 고객 가치관의 일치
```

- 낮은 적합도도 거래 가능
- 평가 이유 공개
- 자동 추천·선택 금지

### BS-V9-20260731-05 — 장비 운명 상태

- 수치형 내구도와 반복 수리 없음
- 정상·전투 흔적·분실·회수·영구 파괴 사용
- 전투 흔적은 사용 불가 상태가 아닌 서사 상태

### BS-V9-20260731-06 — 대표 콘텐츠 증명 세트

- 대표 세션은 검투사 카시아
- 별도 결정론적 증명 세트는 수집가 에르사
- 같은 요청·판매·소유권·결과·저장 구조 재사용
- 전체 고객 구조는 `BS-CUST-20260731-01`이 명확화

### BS-V9-20260731-07 — 미래 명작 전당

- +50 이상 작품의 선택적 비교·전시
- 검증 랭킹과 레거시 전시 분리
- 단일 종합 전투력 점수 금지
- 성능 보상 없음
- 등록 실패가 로컬 작품에 영향 없음

### BS-V9-20260731-08 — 벤치마킹 선행 원칙

- 새 시스템·핵심 규칙·콘텐츠 구조·주요 UX 흐름 설계 전 벤치마킹 필수
- 매 작업마다 대규모 조사 반복 금지
- 최근 관련 조사 재사용 허용
- 채택·변형·제외와 전파·검증 기록 필수

### BS-CUST-20260731-01 — 고객 4유형과 유형별 복수 고객

```text
고객 유형 = 수집가·모험가·검투사·군인
유형별 이름 고객 최소 2명
```

- 고객 유형은 공통 세계 환류 파이프라인이다.
- 이름 고객은 개별 목표·성격·예산·선호·관계·사건을 가진다.
- 카시아는 검투사 대표, 에르사는 수집가 대표다.
- 4유형은 한 세션의 고정 4명이 아니다.
- 동시 활성 요청은 최대 2개다.
- 고객 전용 핵심 엔진 금지
- `clarifies: BS-V9-20260731-06`

### BS-ENH-20260731-01 — +50 일반·고위 정밀강화 이원화

```text
+49→+50
├─ 일반 정밀강화: 기존 위험 규칙, 특수 수식어 없음
└─ 고위 정밀강화: 특수재료 사용, 확정 성공, 특수 수식어 획득
```

- 고위 정밀강화의 특수재료는 촉매 또는 특수 보조재료 역할을 가질 수 있다.
- 촉매는 주 진화 계열, 특수 보조재료는 후보·변주를 책임진다.
- 고위 경로는 유효 후보 2~3개를 실행 전에 공개한다.
- 일반 +50도 정상 완성품·+51 이상·명작 전당 자격을 가진다.
- +50 경로와 특수재료 역할을 별도 데이터로 저장한다.
- `clarifies: BS-V9-20260731-03`

### BS-SCREEN-20260731-01 — 상황별 인게임 화면 설계·구현 명세 작업지시문

- 중간점검은 `docs/planning/BLACKSMITH_SITUATION_SCREEN_SPEC_WORK_ORDER_2026.md`를 따른다.
- 실제 코드를 작성하지 않고 문서·실제 구현·해석·가정·제안을 분리한다.
- 대표 상황 도출 전에 메인, 핵심 플레이, 보유 자원 관리, 결과 화면을 필수 기준 화면으로 감사한다.
- Blacksmith 초기 대응 화면은 대장간 허브, 단조·강화 작업대, 보관함·자원 관리, 강화·고객·세계 결과다.
- 화면을 정적 메뉴로 다루지 않고 `SCREEN → SIT` 상태 변형과 전체 상황 전환으로 연결한다.
- P0 상황은 Godot Scene·Node·Resource·Signal·저장·예외·완료·테스트까지 A~T 형식으로 상세화한다.
- P1~P3는 요약 후 필요 시 확장한다.
- 공통 절차는 Base 승격 후보이며 Blacksmith 고유 화면·시스템은 프로젝트에 유지한다.

### BS-SCREEN-20260731-02 — 비주얼 중심 화면 보드 상위 계약

- 메인 산출물은 비주얼 기준·필수 화면 4종·핵심 상황 시퀀스다.
- 기술 구조는 `BS-SCREEN-20260731-01` 기반 PART D 부록으로 분리한다.
- 모든 화면은 `CURRENT / INFERRED / PROPOSED / PLACEHOLDER`를 구분한다.
- 화면 판독성을 우선하고 기술 보고서형 보드를 금지한다.

### BS-ART-20260731-01 — 프로젝트 그림체

```text
스타일라이즈드 다크 포지
```

- 어두운 대장간의 무게감, 선명한 장비, 따뜻한 불빛을 결합한 스타일라이즈드 2D
- 장비가 화면의 시각적 주인공
- 캐릭터는 반실사보다 단순화된 게임 일러스트
- UI는 철·황동 재질을 암시하되 가독성을 우선
- 밝은 캐주얼 공방풍·완전 반실사·일반 모바일 판타지 UI 제외
- `resolves: DEC-VIS-03`

### BS-MODAK-20260731-01 — 모닥 디자인

```text
C안의 차분한 표정 + 밝은 노랑·주황 불꽃 몸체
```

- 숯 껍질 몸체 폐기
- 검은색·숯색은 손·발·목 장식·작은 테두리에만 제한
- 기본·호기심·걱정·기쁨·놀람·슬픔·집중 표정 사용
- 항상 웃는 유아형 마스코트 금지
- 플레이어 선택·확률·결과를 예측하거나 추천하지 않음
- 장비·확률표·버튼을 가리지 않는 작은 비성장형 동반자

### BS-MAIN-20260801-01 — 별도 메인 화면

```text
앱 실행 → 별도 메인 화면 → 새 게임 또는 이어하기 → 제품 Shell
```

- 필수 메뉴는 이어하기·새 게임·설정
- 저장이 없으면 이어하기 비활성
- 새 게임이 기존 저장에 영향을 주면 명시적 확인 필요
- 도감·가이드·크레딧·게임 종료는 별도 검토 전 `PROPOSED`
- `resolves: DEC-VIS-01`

### BS-SHELL-20260801-01 — 단일 제품 Shell + View·Overlay 혼합

- 메인 화면은 제품 Shell과 별도 Scene
- 허브·단조·강화·고객·세계 결과는 한 캠페인 상태를 공유
- 보관함·설정·ResultEnvelope는 Overlay 또는 내부 Screen 사용
- 화면 전환으로 도메인 상태를 재생성하거나 비가역 결과를 재추첨하지 않음
- `resolves: DEC-VIS-02`

### BS-SYNC-20260731-01 — 기획 정본 즉시 동기화

- 주요 변경과 승인 내용은 GitHub 권위 문서·계획 데이터·연결 Sheet에 즉시 반영
- 모든 대상에 같은 Decision ID 사용
- 변경 위치·PR·커밋·Sheet 범위·검증 상태 기록
- 병합 전 `SYNCED_TO_DRAFT`, 병합 후 `SYNCED_TO_MAIN`

## 시각 설계 상태

`BS-VISUAL-20260731-01`은 `USER_ACCEPTED_WORKING_BASELINE`이다.

- 최종 제품 에셋이 아님
- 플레이어 레벨·청색 보석·업적·상점·특수 제작·128/150 보관함·직접 시장/경기장 플레이는 `PLACEHOLDER / NOT_CANON`
- 승인된 항목은 별도 메인, 단일 제품 Shell, 스타일라이즈드 다크 포지, 밝은 모닥, 장비 중심 정보 위계다.

## 권한

충돌 시 다음 순서를 따른다.

```text
사용자 최신 결정
→ BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md
→ BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md
→ BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md
→ BLACKSMITH_CUSTOMER_ARCHETYPES_AND_PLUS50_RECONCILIATION_2026.md
→ BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md
→ BLACKSMITH_V9_USER_DECISION_PACKET.md·Decision Ledger Addenda
→ 본 ID 인덱스
→ 연결 계획 데이터와 Google Sheet
```

## 동기화 상태

```text
GITHUB_AUTHORITY: GITHUB_DRAFT_COMMITTED
PLANNING_DATA: UPDATED
GOOGLE_SHEET: UPDATE_REQUIRED_FOR_20260801_DECISIONS_AND_AUDIT
CROSS_SOURCE_VERIFICATION: PENDING
MAIN_MERGE: NOT_RUN
USER_기획_완료: NOT_DECLARED
```
