# [현재 정본] Blacksmith Roadmap

## 현재 운영 상태

```yaml
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
CURRENT_STAGE_STATUS: R2_CHECKPOINT_003_CANON / ADVERSARIAL_CANON_AUDIT_COMPLETED_WITH_OPEN_USER_DECISIONS
R1_FINAL_APPROVAL: BS-OPS-20260803-05
R2_CHECKPOINT_003_MERGE_PR: 103
R2_CHECKPOINT_003_MERGE_SHA: 674ee21013cb5d41f89a1a3f3b10ecfc31238295
R2_CHECKPOINT_003_CLOSURE_PR: 104
R2_CHECKPOINT_003_CLOSURE_SHA: d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9
CANON_AUDIT: BS-OPS-20260804-02 / BS-ADV-20260804-01 / COMPLETE
NEXT_APPROVAL_COUNTER: 0/10
PRODUCT_IMPLEMENTATION: BLOCKED
```

문서 병합은 승인 기획을 main에 보존하는 작업이며 제품 구현 승인과 다르다.

## R0 — 운영·정본 복구

상태: `PASS / MERGED_TO_MAIN`.

- GitHub·Google Sheet 동일 Decision ID 동기화
- 승인 최대 10건 배치·적대적 검토·expected-head squash 정책
- 권위 진입점·Registry·Hub 복구
- PR #81 전체 병합 단위 `REFERENCE_ONLY / DO_NOT_MERGE`
- 제품 구현 경로 보호

## R1 — 프로젝트 코어·플레이어 약속

상태: `USER_APPROVED / HISTORICAL_BASELINE / R2_REFINED`.

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품을 만들고, 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 작품이 고객과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

R2에서 대체된 R1 구조:

- 일반 수식어 A·B → `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- 보조재료 슬롯 → 제거
- 범용 고정 일정 프리셋 → 개인 일정과 날짜 예고형 세계 일정 분리

## R2 — Core·Session·Meta Loop

상태: `PLANNING_ACTIVE / CHECKPOINT_003_CANON / CANON_AUDIT_COMPLETE`.

병합 완료:

- 고객 능력·위험도 `1~10`, 예상 성공률 `5~95%`
- 개인 일정·세계 일정 분리
- 주요 일정·소식·묶음 요약·일정 장부
- 검투사·모험가·군인·귀족과 콘텐츠 가족
- 예술성 `1~10`
- 보조재료 제거
- 일반 강화 한 입력 한 결과
- 정밀강화 방식과 촉매 책임 분리
- 등급·촉매·연대기 세 수식어
- 장비명 조합과 UID 기반 연대기 상세
- 구형 문서 상태 분류와 자동 드리프트 검사

```text
작품 종류 + 주재료 + 직접 단조
→ 제작 등급·등급 수식어
→ 일반 강화와 멈춤·추가 도전
→ 정밀강화 방식·촉매 선택
→ 촉매 수식어 성장
→ 고객·세계에 작품 전달
→ 연대기 수식어와 UID 생애 결과
→ 다음 강화·복원·제작 판단
```

### 다음 승인 후보 — `0/10`

1. 제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 분리
2. 연대기 수식어의 효과 책임 경계
3. 작품 판매·증여·복원·상속 소유권 상태 머신
4. 모바일 장비명 줄바꿈·축약·스크린리더 순서
5. 첫 작품의 촉매·연대기 정체성 보상 시점
6. 완전 파괴와 작품 애착 검증
7. PR #81 분야별 자산 선별 이관

## R3 — 제작·강화·작품 정체성·실패·저장

시작 조건: `R2_USER_APPROVED`.

- 작품 종류·주재료·제작 등급
- `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- 강화 방식·촉매 계보·정밀 이정표
- 실패·손상·대파·잠금·복원·완전 파괴
- UID·불변 역사·저장·migration
- 작품 소유권 상태 머신
- 연대기 효과 책임 경계

금지:

- 일반 수식어 A·B 재도입 금지
- 보조재료 슬롯 재도입 금지
- 수식어 슬롯 간 덮어쓰기
- 같은 이정표 무한 리롤
- 저장·로드 결과 재추첨

## R4 — 고객·일정·사건·작품 연대기

시작 조건: `R3_APPROVED`.

- 고객 목적·능력·특기·약점
- 판매·납품·증여와 소유권 이전
- 개인 일정과 세계 일정
- 고객·작품·세계 후속 결과
- 연대기 수식어 형성·진화
- 재방문·관계·명성·복원·계승

차단:

- 직접 전투 범위 팽창
- 사건 RNG가 작품 선택을 압도
- 반복 저위험 사건 연대기 파밍
- 날짜 경과만으로 수식어 자동 성장

## R5 — 경제·피로도·성장·장기 목표

시작 조건: `R4_APPROVED`.

- 골드·재료 Source/Sink
- 강화·촉매·복원 비용
- 예술성·실용 성능·희소성·연대기의 가격 책임
- 피로도·날짜 전환
- 소프트락 방지
- 단일 변수 중심 밸런스 실험

정확한 비용·확률·보상·기간은 사람 플레이 전까지 테스트 프리셋이다.

## R6 — 모바일 UX·접근성·아트·오디오

시작 조건: `R5_APPROVED`.

- Android portrait·safe area·one-hand flow
- 한 화면에 중요한 판단 하나
- 위험·확률·소유권·자원 소비 사전 표시
- 제작 등급·예술성·세 수식어 시각 위계
- 긴 장비명 줄바꿈·축약·스크린리더 순서
- 연대기 탭과 하단 상세 패널
- 비색상 정보·모션 감소·터치 목표
- PR #81 아트·메인·UI 자산 선별 이관

## R7 — 버티컬 슬라이스·데이터·검증·제작 계획

시작 조건: `R6_APPROVED`.

### 첫 코어 버티컬 슬라이스

```text
플레이어 선택 작품 한 점
→ 제작과 등급 수식어
→ +10/+20/+30/+40/+50
→ 촉매 수식어 형성·성장
→ 고객 납품
→ 개인 또는 세계 일정
→ 연대기 수식어 형성 가능성
→ 같은 UID 재방문
→ 복원·재강화·후속 판단
```

### 행동 증거

- 강화 지속·중단 고민
- 등급·촉매·연대기 생성 원인 설명
- 작품 선택과 고객 결과 인과 설명
- 일정 우선순위 이해
- 재방문 뒤 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 작품 생애 의미 이해

산출물:

- 포함·제외 범위
- Schema·ID·저장·migration
- 소유권·일정·수식어 상태 머신
- 테스트 프리셋·행동 가설
- 자동 테스트·Godot·Android·접근성·성능·사람 플레이 계획
- Codex 실행 Packet 초안

## R8 — 최종 적대적 검수·사용자 검수

- 플레이어 약속 ↔ 반복 행동
- 강화 코어 ↔ 피로도·날짜·고객·세계 환류
- 세 수식어 ↔ 실제 작품 판단과 애착
- 경제 수치 ↔ 행동 가설
- 복잡도 ↔ 모바일 온보딩
- GitHub 정본 ↔ Sheet ↔ 구현
- 구형 문서 상태 ↔ 실제 참조 경로
- 리뷰·CI·금지 경로·드리프트 감사

## R9 — Codex 구현 인계

시작 조건:

```text
R1~R8 COMPLETE
+ 최종 사용자 승인
+ Codex 구현 Gate 별도 승인
```

제품 구현은 현재 `BLOCKED`다.

## 문서 상태 정책

- `[현재 정본]`: Current Decisions, R2 Registry, R2 Game Bible, Hub
- `[부분 대체됨]`: 일부 원칙만 유효한 R1·역사 문서
- `[대체됨]`: 최신 정본이 책임을 인수
- `[보류]`: 승인 전 참고만 가능
- `[폐기]`: 재사용 금지
- `[역사 증거]`: 당시 과정 보존, 현재 제품 PASS 아님

상태 원장: `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`
