# [현재 정본] Active Context

- 갱신: `2026-08-04 10:31 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R2_CORE_SESSION_META_LOOP / CANON_AUDIT_COMPLETE_PENDING_EXACT_HEAD_VALIDATION`
- R2 체크포인트 003: `MERGED_PR103 / CLOSURE_PR104`
- 체크포인트 폐쇄 main: `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`
- 정본 감사: `BS-OPS-20260804-02 / BS-ADV-20260804-01`
- 다음 승인 카운터: `0/10`
- 제품 구현: `BLOCKED`

## 현재 권위 진입점

1. `CURRENT_CONFIRMED_DECISIONS.md`
2. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
4. 본 문서
5. `START_HERE.md`
6. `DOCUMENTATION_MAP.md`
7. `ROADMAP.md`
8. `DEVELOPMENT_GATES.md`

구형 문서 상태:

- `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`
- `docs/planning/BLACKSMITH_CANON_ADVERSARIAL_REVIEW_AND_LEGACY_STATUS_2026-08-04.md`

## GPT 역할 경계

GPT는 핵심 재미·콘텐츠 기획·이미지·아트 방향·적대적 설계 검토를 중심으로 한다. 제품 구현·코드 소유·저수준 기술 실행은 Codex 또는 구현 단계로 넘긴다.

## 프로젝트 코어

```text
작품 종류 + 주재료 + 직접 단조
→ 제작 등급·등급 수식어
→ 일반 강화 한 입력 한 결과
→ 강화 성공·실패와 멈춤·추가 도전
→ +10/+20/+30/+40/+50 정밀강화
→ 강화 방식으로 세부 수치 방향 선택
→ 촉매 이력으로 촉매 수식어 생성·성장·분기·변형
→ 고객·세계에 작품을 보냄
→ 작품 생애로 연대기 수식어 생성·진화
→ [등급] 촉매 수식어 기본 작품명 - 연대기 수식어
→ 같은 UID 작품 결과·재방문
→ 복원·재강화·다음 제작 판단
```

핵심 재미:

- 즉각: 강화 결과와 멈춤·추가 도전
- 세션: 작품·고객·일정 우선순위
- 장기: 작품 UID 생애·연대기·복원·계승

## 세 수식어

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

### 등급 수식어

- 제작 완료 시 즉시 생성
- baseline ID: `STANDARD / GOOD / PERFECT`
- 동일 UID에서 고정
- 제작 등급 효과 중복 가산 금지

### 촉매 수식어

```text
EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED
```

- 현재·누적 촉매 이력에 따라 확률적으로 성장
- 같은 계보 강화·호환 분기·희귀 혼합 변형
- 작품 연대기가 직접 변경하지 않음

### 연대기 수식어

- 의미 있는 고객·사건·사용·손상·복원·소유 이력으로 생성·진화
- 촉매·제작 등급이 직접 변경하지 않음
- 낮은 위험 반복으로 무한 파밍하지 않음

과거 `일반 수식어 A·B` 구조와 보조재료 슬롯은 현재 정본이 아니다.

## 장비명·연대기 상세

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

```text
[명품] 예리한 강철 장검 - 투기장의 승자 ›
                         └ UID 기반 연대기 상세
```

- 빈 촉매 수식어 생략
- 빈 연대기 수식어는 하이픈과 함께 생략
- 현재 연대기 하나만 이름에 표시
- 하단 상세 패널은 읽기 전용
- 실제 UID의 형성 사건·주요 타임라인·진화 계보·가치·소유·손상·복원 기록만 표시
- 미래 결과·기록 없는 사건·열람 보상 금지

## 고객·성공 예측

- 위험도: 정수 `1~10`
- 고객 능력: 기량·체력·판단력 각 `1~10`
- 예상 성공률: 약 10% 단위, `5~95%`
- 작품·도구·조언 선택 뒤 방향 갱신
- 정확한 보정치는 `BASELINE_TEST_PRESET`

## 개인 일정과 세계 일정

개인 일정:

- 방문·판매·납품으로 활성화
- 재방문 없이 하루 종료마다 최대 한 번 진행
- 판매 당일 최종 해결 금지

세계 일정:

- 특정 날짜와 규모 사전 예고
- 작품·도구·조언을 준비 기여로 누적
- 준비 체크포인트와 예정 날짜에서 판정

범용 고정 일정 프리셋은 현재 상태 머신이 아니다.

## 일정 표시

```text
주요 세계 일정 하나 고정
+ 오늘 중요 소식 최대 3건
+ 일반 개인 일정 하루 종료 묶음 요약
+ 중대 결과만 즉시 알림
+ 관심 개인 일정 하나 추적
+ 전체 일정 장부
```

## 예술성

- 정수 `1~10`
- 실용 성능과 분리
- 강화 단계만으로 자동 상승하지 않음
- 제작 등급 수식어와 예술성 시각 단계는 별개

열린 P1:

- 장비명 예시 `[명품]`과 예술성 시각 단계 한국어 `명품`의 어휘 충돌

## PR #81 경계

```text
전체 병합 단위: [폐기]
브랜치·원 승인 원문: [역사 증거]
분야별 선별 이관: [보류]
```

최소 승인 증거 복구:

- 스타일라이즈드 다크 포지
- 밝은 불 정령 모닥
- 별도 메인 화면
- 단일 BlacksmithApp 방향
- 단일 캠페인·자동 백업·ResultEnvelope 방향
- 작업 비주얼 기준선, 최종 에셋 아님

상세 계약은 최신 R2 기준의 별도 소형 PR로만 선별 이관한다.

## 적대적 감사 상태

- 핵심 재미 방향: `VALID`
- P0: `0`
- P1 범주 발견: `7`
- 이번 PR에서 해결한 문서·권위 P1: `6`
- 사용자 Decision이 필요한 P1: 등급·예술성 한국어 명칭 충돌 `1`
- P2 후속 후보: `7`
- 제품 경로 변경: `0`

`START_HERE.md`와 `DOCUMENTATION_MAP.md`의 추가 드리프트는 위 6개 문서·권위 P1 범주의 콜드 스타트 전파 사례로 함께 해결했다.

## 열린 설계 후보 — 아직 승인 아님

1. 제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 분리
2. 연대기 수식어의 효과 책임 경계
3. 작품 판매·증여·복원·상속 소유권 상태 머신
4. 모바일 조합 장비명 표시
5. 첫 작품의 촉매·연대기 정체성 보상 시점
6. 완전 파괴와 작품 애착 검증
7. PR #81 선별 이관 순서

## 역사 구현·검증 추적

- `POC v0.6.4 · main · 2026.07.23.1`
- 과거 일반 강화 실패 기준선: `+11 / LEGACY_IMPLEMENTED_VALUE`
- 실패·위험 data 소유자: `data/crafting/enhancement_balance.json`
- 정밀 이정표 data 소유자: `data/crafting/enhancement_milestones.json`
- 제작 모델 7건
- 통합 6건
- `HISTORICAL_EVIDENCE`, 최신 제품 PASS 아님
- PR #103/#104 exact-head Base·Python·Godot: `PASS`
- focused planning tests standalone: 별도 실행 전 `NOT_RUN`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 다음 작업

1. PR #105 exact-head 검증 완료
2. GitHub·Google Sheet 동일 Decision ID 동기화
3. PR 댓글·리뷰 스레드·보호 경로 재감사
4. expected-head squash 병합
5. 다음 R2 승인 배치를 `0/10`에서 재개
6. 제품 구현은 계속 `BLOCKED`
