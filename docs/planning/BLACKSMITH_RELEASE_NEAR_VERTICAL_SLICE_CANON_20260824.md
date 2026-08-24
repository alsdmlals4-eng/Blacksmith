# [현재 정본] Blacksmith Release-near Vertical Slice 계약

- Parent: `BS-CORE-20260820-01`, `BS-ONBOARD-20260824-23`, `BS-LINK-20260824-24`
- Cross-reference: `BS-ENHANCE-20260820-02~13`, `BS-PROGRESSION-20260820-14~17`, `BS-RESOURCE-20260824-18`, `BS-REPAIR-20260824-19`, `BS-OVERHAUL-20260824-20`, `BS-DESTRUCTION-20260824-21`, `BS-MAX-20260824-22`
- Decision: `BS-SLICE-20260824-25`
- 사용자 승인: `2026-08-24 KST / 기획 완료 선언으로 권장안 B 승인`
- 상태: `USER_APPROVED / PLANNING_CANON / PLANNING_PACKAGE_CLOSURE`
- Work Mode after closure: `IMPLEMENTATION_READY`
- 제품 구현: `APPROVED_TO_BEGIN_CURRENT_CANON_ONLY`
- Human/Android validation: `NOT_RUN`

## 1. 목적

Blacksmith의 release-near Vertical Slice는 전체 콘텐츠를 넓게 보여주는 데모가 아니라, **한 작품의 제작·강화·고객 사용·생애 결과가 다시 공방 판단으로 돌아오는 한 개의 완전한 인과 루프**를 실제 제품형 runtime에서 증명한다.

```text
ARCHITECTURE
= FULL_CANON_DOMAIN
+ NARROW_POLISHED_PLAYER_PATH
```

## 2. 대표 플레이 경로

```text
MainMenu
-> New Game
-> Workshop
-> Nadia starter context
-> representative SWORD / iron fixture
-> Forge
-> Item Birth / UID
-> +1~+9 일반 강화
-> +10 정밀강화
-> STOP or +11 PUSH
-> Nadia handoff
-> Workshop
-> delayed Nadia personal schedule
-> multi-axis result
-> same UID return/lifecycle state
-> Repair or Item Detail
-> Workshop
-> next craft/enhancement question
```

이 경로가 실제 save/load와 동일 domain/resolver를 사용해야 한다. 화면용 가짜 상태나 tutorial-only RNG를 사용하지 않는다.

## 3. Slice fixture 경계

첫 사람용 slice의 대표 작품군은 다음으로 제한한다.

```text
SLICE_REPRESENTATIVE_ITEM_GROUP = SWORD
SLICE_STARTER_PRIMARY_MATERIAL = iron
```

이는 다음을 뜻하지 않는다.

```text
SWORD/iron != Nadia의 영구 선호
SWORD/iron != 전체 게임 최적해
SWORD/iron != 최종 제품의 장비군 제한
```

## 4. Domain은 처음부터 +0~+100 정본을 표현

사람용 slice가 +11 부근에서 핵심 질문을 검증하더라도 내부 item domain은 +11 전용으로 만들지 않는다.

최소 표현 필드:

```text
ITEM_UID
crafting provenance
crafting_grade
Artistry
enhancement_level 0..100
highest_checkpoint
CURRENT
MAX
same-target recovery
used_precision_milestones [10,20,30,40,50]
overhaul_used
affixes/functions
owner/customer lifecycle
MAX_ENHANCEMENT_REACHED
physical lifecycle ACTIVE / DESTROYED
append-only lifecycle evidence
```

구형 `VSItem`의 `enhancement_level <= 10`, precision milestone `[10]`, `INTACT/DAMAGED/BROKEN/RESTORED`만으로 현재 정본을 대표하지 않는다.

## 5. 후기 시스템 검증 방식

첫 사람 플레이가 +100까지 반복 강화해야 시스템을 검증하도록 만들지 않는다.

Domain fixture로 최소 다음 edge contract를 검증한다.

```text
+99 -> +100 success -> MAX_ENHANCEMENT_REACHED
+60 checkpoint / MAX 35 -> one-lifetime overhaul -> MAX 50 / used=true
CURRENT 20 -> causal damage 25 -> CURRENT 0 -> DESTROYED -> immutable history
```

후기 UI polish는 release-near 대표 경로의 필수조건이 아니다. 해당 domain 규칙이 실제 같은 코드경로에서 동작해야 한다.

## 6. Routing

최신 routing은 지연 고객 결과를 반영한다.

```text
WORKSHOP
-> FORGE
-> ITEM_BIRTH
-> ENHANCEMENT
<-> PRECISION

ENHANCEMENT / PRECISION
-> CUSTOMER
CUSTOMER
-> WORKSHOP
WORKSHOP
-> RESULT [resolved schedule exists]
RESULT
-> REPAIR / ITEM_DETAIL / WORKSHOP
REPAIR
-> ITEM_DETAIL
ITEM_DETAIL
-> WORKSHOP
```

구형 `CUSTOMER -> RESULT` 즉시 결과만을 정상 흐름으로 사용하지 않는다.

## 7. Save V2

현재 pre-release V1 계약을 그대로 확장하지 않는다.

```text
VERTICAL_SLICE_SCHEMA = 2
PRESET_VERSION = VS-2026.08.24-B
```

V1 pre-release save 처리:

```text
V1 detected
-> LEGACY_PRE_RELEASE_SAVE
-> Continue disabled with explicit reason
-> New Game uses existing explicit overwrite confirmation
-> confirmed replacement creates V2
```

금지:
- silent migration
- silent delete
- load-time reroll
- corrupt backup overwrite

기존 UID, run identity, atomic save/backup 구조는 재사용한다.

## 8. 책임 분리

```text
DOMAIN
- Item V2
- Lifecycle / Ledger
- Content Result

RESOLVERS
- Forge
- Enhancement
- Precision
- Repair / Overhaul
- Customer Context
- Nadia Schedule / Result

SERVICES
- UID
- Save V2
- Run Initialization
- Day / Schedule progression

UI
- Workshop
- Forge
- Item Birth
- Enhancement
- Precision
- Nadia Customer / Handoff
- Result
- Repair
- Item Detail
```

RNG, 고객 결과, UI mutation을 하나의 script에 혼합하지 않는다.

## 9. Visual 단계

### Gate A — Functional Slice

```text
engine-native UI
placeholder 또는 기존 승인 자산
정확한 정보 계층
실제 interaction
실제 runtime/save
```

### Gate B — Representative Presentation

별도 승인된 실제 자산을 사용해 강화 anticipation/result, CURRENT/MAX, precision context, Nadia presentation, VFX/SFX를 교체한다.

기획 완료는 이미지 생성 승인을 자동으로 의미하지 않는다.

## 10. 자동 Acceptance

최소 자동 검증:

```text
New Game -> valid V2 save
same UID after save/load
resolved facts do not reroll
0..100 enhancement domain
checkpoint [10,30,60,90]
same-target recovery
failure family 13
CURRENT/MAX invariant
repair
one-lifetime overhaul
causal destruction + archive
+100 terminal
+10 precision
STOP and PUSH both legal
Nadia hard load gate
0.30pp/level customer enhancement TEST budget
no universal fit score
handoff
delayed schedule
multi-axis result
causal reasons
same UID return
primary next action
```

## 11. Human Acceptance

다음은 자동 테스트로 PASS 처리하지 않는다.

- 첫 강화 input 약 3분 목표
- +10에서 멈출 이유 이해
- +11 구조 위험 이해
- STOP/PUSH 모두 실제 선택으로 인식
- precision 선택이 Nadia 맥락에 미치는 이유 설명
- 결과 뒤 같은 UID 인식
- 다음 행동을 스스로 고를 수 있음
- 모바일 48dp/readability/색상 비의존

상태는 실행 전 `NOT_RUN`.

## 12. 완료 상태 분리

```text
DOMAIN_VERIFIED
-> FUNCTIONAL_SLICE_VERIFIED
-> RELEASE_NEAR_VERIFIED
```

`RELEASE_NEAR_VERIFIED`에는 최소 Human playtest, Android real-device, 접근성/readability, save recovery, performance/crash smoke가 필요하다.

CI green만으로 이를 주장하지 않는다.

## 13. 5회 적대 검토

1. Fake slice: 실제 backend/save를 사용하도록 강제 -> PASS.
2. +11 throwaway: domain 0~100 정본 지원 -> PASS.
3. Scope explosion: 사람용 경로 Nadia 1명 + 대표 작품 1군 -> PASS.
4. Legacy save corruption: V2 bump + fail-closed -> PASS.
5. CI overclaim: Domain/Functional/Release-near 상태 분리 -> PASS.

## 14. Implementation Reality Gate

```text
MainMenu / App Shell = IMPLEMENTED_FOUNDATION
UID / Save / Ledger = IMPLEMENTED_V1_FOUNDATION
ContentResultRecord = IMPLEMENTED_REUSE_PRIMITIVE
Workshop = PLACEHOLDER
Forge product screen = NOT_IMPLEMENTED
current enhancement 13~24 runtime = NOT_IMPLEMENTED
VSItem current-canon fit = CONTRADICTED / V2_MIGRATION_REQUIRED
Nadia runtime data/resolver = NOT_IMPLEMENTED
CURRENT/MAX runtime = NOT_IMPLEMENTED
+100 runtime = NOT_IMPLEMENTED
Human = NOT_RUN
Android = NOT_RUN
```

## 15. Planning Closure

사용자의 `기획 완료` 선언으로 `BS-CORE-20260820-01`부터 `BS-SLICE-20260824-25`까지의 현재 계획 묶음을 구현 기준으로 닫는다.

이후 새 요구는 명시적 추가 Decision으로 기록하고, 승인된 current canon 범위의 제품 구현을 TDD로 시작할 수 있다.
