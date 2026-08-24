# [현재 우선 Gate] Blacksmith 2026-08-24 Planning Complete / Implementation Entry

- 상태: `CURRENT_PRIORITY_IMPLEMENTATION_GATE`
- 사용자 선언: `2026-08-24 KST / 기획 완료`
- 적용 정본: `BS-CORE-20260820-01` ~ `BS-SLICE-20260824-25` + `BS-CUSTOMER-20260824-26`
- Work Mode: `IMPLEMENTATION_READY`
- 제품 구현: `APPROVED_TO_BEGIN_CURRENT_CANON_ONLY`
- 구현 방식: `TDD_RED_GREEN_REFACTOR`
- Human/Android validation: `NOT_RUN`

## 1. 권위

이 Gate는 2026-08-20 Overlay의 `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION` 조건이 실제 사용자 `기획 완료` 선언으로 충족되었음을 기록한다.

따라서 기존 Overlay/Authority 문서의 `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION` 문구는 **조건 충족 전 상태를 설명하는 역사적 Gate 표현**이며, 현재 구현 진입을 다시 차단하지 않는다.

우선순위:

```text
latest user instruction
-> CURRENT_IMPLEMENTATION_GATE_20260824.md
-> Decision25/26
-> CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md
-> individual current canon
-> historical R2/R3/PoC
```

## 2. 현재 구현 범위

```text
FULL_CANON_DOMAIN
+ ONE_COMPLETE_NADIA_LIFECYCLE_SLICE
+ VISITOR_PUBLIC_STANDING_AND_EPITHET
```

대표 사람용 경로는 Nadia + SWORD/iron fixture지만 domain은 +0~+100, CURRENT/MAX, checkpoint/recovery, repair/overhaul, causal destruction/archive, +100 terminal을 지원한다.

## 3. 방문고객 추가 정본

방문고객은 다음을 구분한다.

```text
ROLE
PUBLIC_EPITHET
PUBLIC_STANDING_GRADE
```

등급:

```text
COMMON 일반
SKILLED 숙련
ELITE 정예
RENOWNED 명망
LEGENDARY 전설
```

등급은 전투력·성공률·가격·보상 multiplier가 아니다.

Nadia slice baseline:

```text
[정예] 「유적의 길잡이」 나디아 벤
유적 탐사대장
```

## 4. 구현 금지/미검증

- 이미지 생성/대표 아트 자동 승인 없음.
- Human fun/readability `NOT_RUN`.
- Android real-device `NOT_RUN`.
- 접근성/성능은 실제 실행 전 PASS 금지.
- historical PoC runtime를 current implementation evidence로 자동 승격 금지.

## 5. 구현 계획

`docs/superpowers/plans/2026-08-24-release-near-v2-implementation.md`를 실행한다.
