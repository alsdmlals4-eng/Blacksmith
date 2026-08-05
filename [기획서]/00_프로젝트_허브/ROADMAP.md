# [현재 정본] Blacksmith Roadmap

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
CURRENT_STAGE_STATUS: R2_CHECKPOINT_004_MAIN_CANON / R2_BATCH_005_ACTIVE_2_OF_10
R2_CHECKPOINT_003: PR103 / CLOSURE_PR104 / CANON_AUDIT_PR105
R2_CHECKPOINT_004: PR106 / CLOSURE_PR107 / CANON_AUDIT_PR108
CURRENT_DECISIONS: BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-CRAFT-20260805-02 / BS-OPS-20260805-01
NEXT_APPROVAL_COUNTER: 1/10
MAXIMUM_BATCH_SIZE: 10
PRODUCT_IMPLEMENTATION: BLOCKED
```

## R0–R1

운영 정본과 프로젝트 코어는 승인·병합된 역사 기반이며 R2에서 세 수식어·개인/세계 일정 분리·보조재료 제거로 정제됐다.

## R2 — 현재 기획

체크포인트 004 main canon:

- 제작 등급: `[보통] → [우수] → [명품] → [걸작] → [전설]`
- 제작 등급은 출생 기술 완성도이며 동일 UID에서 고정
- 예술성은 `예술성 27`처럼 표시하는 고정 설계 최대치 없는 수치형 작품 능력치
- 예술성 0은 정상 기능품
- 제작 등급은 예술성 상한을 만들지 않음
- `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- 벤치마킹·현업 비교, 조기 체크포인트, 작업마다 TDD

배치 005 승인 Decision:

- `BS-CRAFT-20260805-02`
- 예술성 최초 생성 원천과 제작 후 허용 성장 원천을 분리
- 일반 강화·판매·전시·감정·소유권·명성·연대기로 자동 증가 금지
- 가격은 구성요소별 가산이며 예술성은 구간별 한계 가치 점감
- 고객 관심 유형은 `IGNORE / SECONDARY / PRIMARY / REQUIREMENT`
- 같은 원인의 이중 계산과 반복 파밍 금지
- 정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`

```text
R2_CHECKPOINT_004
PR106_HEAD_227b2dabf0d98832811415156e72f65d601332a9
MERGE_789c73f38003f40dde5e9a99cd7dcb3ca03863f7
R2_BATCH_004_CLOSED_2_OF_10
R2_BATCH_005_ACTIVE_2_OF_10
```

### 다음 승인 후보 — `1/10`

1. 제작 등급 5단계의 실제 판정 조건과 확률 구조
2. 정밀강화 6방식의 실제 능력치 방향
3. 촉매 수식어 가족과 진화·분기 규칙
4. 연대기 수식어의 효과 책임 경계
5. 판매·증여·복원·상속 소유권 상태 머신
6. 모바일 긴 장비명 표시
7. 완전 파괴와 작품 애착 검증
8. 예술성·가격·고객 선호 테스트 프리셋
9. PR #81 분야별 선별 이관

각 후보는 벤치마킹·적대적 검토를 먼저 수행하며 정확한 값은 사용자 승인 전 고정하지 않는다.

## R3 — 제작·강화·저장

- 5단계 제작 등급 Schema·확률 프리셋
- 예술성 초기값·변화 원천·가격 계수
- 세 수식어와 정밀강화
- 손상·복원·완전 파괴
- UID·저장·migration·소유권

금지:

- 일반 수식어 A·B 재도입 금지
- 보조재료 슬롯 재도입 금지
- 예술성을 범용 전투력으로 변환 금지
- 고정 설계 최대치 재도입 금지
- 저장·로드 재추첨 금지

## R4–R6

- 고객·일정·세계 사건과 작품 연대기
- 경제·피로도·장기 성장
- Android 세로형 UX·접근성·아트·오디오
- 제작 등급·예술성·세 수식어 시각 위계

## R7 — 첫 코어 버티컬 슬라이스

```text
작품 한 점 직접 단조
→ 제작 등급
→ 일반 강화와 멈춤 판단
→ 정밀강화와 촉매 수식어
→ 고객 납품과 일정
→ 연대기 수식어 가능성
→ 같은 UID 재방문
→ 복원·재강화 판단
```

### 행동 증거

- 강화 지속·중단 고민
- 등급·예술성·촉매·연대기 원인 설명
- 고객 결과와 작품 선택 인과 설명
- 다음 행동 자발적 선택

## R8–R9

R8에서 핵심 재미·모바일 복잡도·정본·구형 문서·PR·CI를 적대적으로 검토한다. R1~R8와 최종 사용자 승인 후에만 구현 Gate를 연다.

제품 구현은 현재 `BLOCKED`다.

## 고객 능력·장비 적합성 승인

- Decision: `BS-CUSTOMER-20260805-01`
- 고객: 근력·기량·체력·판단력 `1~10`, 희소 무기·갑옷 적성 `0~3`, 마력 적성 `0~10`
- 작품: `WEAPON / SHIELD_OR_OFFHAND / ARMOR / ACCESSORY_OR_TOOL`
- 파생: 총 중량·적정 하중·균형 상태·특수기능 적합도
- 상태: `R2_BATCH_005_2_OF_10 / APPROVED_PENDING_MERGE / PRODUCT_IMPLEMENTATION_BLOCKED`
