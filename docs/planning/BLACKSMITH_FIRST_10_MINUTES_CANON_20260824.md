# [현재 정본] Blacksmith 첫 10분 Core Thesis 온보딩

- Parent: `BS-CORE-20260820-01`, `BS-PROGRESSION-20260820-14~17`, `BS-MAX-20260824-22`
- Cross-reference: `BS-CRAFT-20260804-04~06`, `BS-VIS-20260820-05`
- Decision: `BS-ONBOARD-20260824-23`
- 사용자 승인: `2026-08-24 KST / 권장안 B 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Runtime mutation: `NOT_ALLOWED_IN_THIS_DECISION`
- Human/Player validation: `NOT_RUN`

## 1. 목적

첫 10분의 목적은 전체 시스템을 설명하는 것이 아니다.

```text
GOAL
= 플레이어가 Blacksmith의 핵심 재미를 직접 한 번 경험하고
  왜 다음 작품/다음 강화를 하고 싶은지 설명할 수 있게 한다.
```

핵심 thesis:

```text
좋은 작품을 지킬까
vs
한 번 더 강화해 더 큰 가치를 노릴까
```

정밀제작·고객/세계·경제·작품 UID는 이 질문을 더 의미 있게 만드는 SUPPORT다. 첫 10분에서 SUPPORT가 강화보다 앞서면 안 된다.

## 2. 승인 구조 — CORE_THESIS_FIRST_10_MINUTES

```text
New Game
-> 짧은 첫 작품 제작
-> +1/+2 안전 강화
-> +3~+9 BUILD_CONFIDENCE
-> +10 첫 정밀강화 + checkpoint + 평균 본전선
-> +11 최초 구조 위험 Preview
-> STOP vs PUSH 실제 선택
-> 실제 결과
-> 짧은 UID/의뢰 payoff
-> 다음 작품 질문
```

불변:

```text
NO_SCRIPTED_FAILURE
NO_HIDDEN_SUCCESS_BOOST
NO_TUTORIAL_ONLY_ODDS
NO_FORCED_+11
NO_VENDOR_GATE_BEFORE_FIRST_STOP_DECISION
NO_FULL_SYSTEM_LECTURE
```

첫 10분은 강제 countdown이 아니라 UX pacing 목표다. 플레이어가 10분을 넘었다고 흐름을 강제로 자르지 않는다.

## 3. 시간 Budget

| 목표 시간 | 경험 | 새로 학습하는 것 |
|---:|---|---|
| 0:00~0:45 | New Game -> Workshop | `나는 대장장이이고 첫 작품을 만든다` |
| 0:45~2:00 | 첫 작품의 짧은 직접 제작 | 한 작품이 고유 UID로 태어남 |
| 2:00~3:00 | +1/+2 LEARN | 강화 입력 -> 기대 -> 즉시 결과 |
| 3:00~5:30 | +3~+9 BUILD_CONFIDENCE | 가치 상승, 실제 실패 시 recovery/CURRENT |
| 5:30~7:30 | +10 첫 정밀강화 + checkpoint | 첫 커스터마이즈 + 첫 경제적 확보 |
| 7:30~9:00 | +11 위험 Preview | 최초 영구 MAX 구조 위험 |
| 9:00~10:00 | STOP vs PUSH | 핵심 의사결정 + UID payoff |

시간은 목표이며 장애·읽기속도·접근성 때문에 더 오래 걸려도 실패 처리하지 않는다.

## 4. Stage 0 — MainMenu와 Workshop

현재 실제 App Shell의 `MainMenu -> BlacksmithApp -> WORKSHOP` 구조를 유지한다.

첫 New Game에서 장황한 세계관 exposition, 클래스 선택, 전체 공방 투어, 고객 목록, 상점 투어를 먼저 요구하지 않는다.

처음 보여줄 최소 목표:

```text
첫 의뢰/목표 한 줄
첫 작품 제작 CTA
```

MainMenu/Save는 기존 Task1/Task2 권위를 소비한다. Decision23은 save schema나 main menu 구조를 재설계하지 않는다.

## 5. Stage 1 — 첫 작품 제작

목표: 2분 안에 첫 강화 가능한 작품을 확보한다.

첫 제작은 정밀제작 전체 시스템 강의가 아니다. 직접 단조의 핵심 input과 결과만 경험한다.

완료 시 최소 공개:

```text
작품명
제작 등급
ITEM_UID
기본 성능
강화 가능 상태
```

제작 등급/Artistry/세 수식어의 전체 심층 설명은 필요 시 상세 보기로 미룬다.

첫 작품은 튜토리얼 전용 가짜 UID가 아니라 정상 작품 생애 규칙을 사용한다.

## 6. Stage 2 — +1/+2 LEARN

첫 강화 입력 목표: 약 3분 이내.

처음 필요한 P0 정보:

```text
현재 강화 단계
TARGET
최종 성공률
시도 비용
보강재 필요량
[강화]
```

+1/+2는 현재 LEARN 권위를 그대로 사용한다.

튜토리얼에서 성공률을 몰래 올리거나 실패를 연출하지 않는다.

```text
TUTORIAL_ODDS == CURRENT_CANON_ODDS
```

결과 피드백은 짧고 즉시 이해 가능해야 한다. 반복 단계마다 대형 연출을 강제하지 않는다.

## 7. Stage 3 — +3~+9 BUILD_CONFIDENCE

목표: 반복 클릭을 가르치는 것이 아니라 `강화하면 가치가 올라간다`는 패턴을 읽게 한다.

### 7.1 Just-in-time CURRENT

+3부터 실제 DAMAGE 가능성이 생기므로 그 직전에 CURRENT를 소개한다.

```text
CURRENT = 현재 손상 buffer
```

MAX 심층 설명은 아직 강제하지 않는다.

### 7.2 실제 첫 실패

실패가 실제로 발생했을 때만 해당 결과를 설명한다.

```text
same UID target failure
-> recovery +6%p
```

실패가 발생하지 않았다고 튜토리얼용 scripted failure를 삽입하지 않는다.

필요하면 다음 시도 화면에서 작은 `실패 회복 +6%p` 설명을 활성화한다.

### 7.3 반복 속도

BUILD 구간은 DDD를 `긴 연출`로 표현하지 않는다.

```text
fast expectation
-> short impact
-> immediate state delta
-> next question
```

스킵 불가능한 대형 성공 연출을 매 단계 반복하지 않는다.

## 8. Stage 4 — +10 첫 확보와 첫 정밀강화

+10은 세 의미가 겹친다.

```text
FIRST_ECONOMIC_STOP_STATE
CHECKPOINT_FLOOR +10
FIRST_PRECISION_ENHANCEMENT_MILESTONE
```

따라서 +10을 일반 강화 한 번으로 무시하지 않는다.

### 8.1 Progressive disclosure

첫 +10 정밀강화는 전체 촉매/방식 catalogue를 강의하지 않는다.

기본 화면:

```text
추천 강화 방식
추천 호환 촉매
예상 성능 방향
대가/위험 요약
[이 조합으로 진행]
[다른 방식 보기]
```

전체 정상 규칙과 선택지는 `다른 방식 보기`에서 접근 가능하다.

```text
FULL_RULES_AVAILABLE
DEFAULT_PATH_RECOMMENDED
NO_HARD_LOCK
```

추천은 튜토리얼 전용 보정이 아니며 결과를 확정하지 않는다.

### 8.2 +10 확보 메시지

+10 도달 후 다음 의미를 명확히 보여준다.

```text
+10 확보 완료
최근 checkpoint = +10
대표 기본 공개시장 기준 평균 투자 회수선 확보
```

`평균 본전`을 개별 플레이어의 실제 지출 환급 보장으로 표현하지 않는다.

## 9. Stage 5 — +11 최초 구조 위험 Preview

+11은 첫 `FIRST_STOP_POINT ATTEMPT`다.

이 순간에 MAX와 CRITICAL 구조 위험을 처음 강하게 foreground한다.

필수 비교:

```text
현재 +10을 지키면
- 첫 평균 투자 회수선 확보
- 작품을 그대로 보유/인계 가능

+11에 도전하면
- 더 높은 기본 수익 가능
- DOWNGRADE / DAMAGE / CRITICAL 가능
- CRITICAL은 CURRENT 손상 + MAX 구조 흉터
```

버튼 의미:

```text
[이 작품을 지킨다]
[+11에 도전한다]
```

정확 카피는 후속 UX/Visual에서 다듬을 수 있으나 두 행동이 모두 정상 progression이어야 한다.

튜토리얼 진행을 위해 +11을 강제하지 않는다.

## 10. Stage 6 — STOP와 PUSH 모두 정상 완료

### STOP

```text
+10 작품을 보유/인계
-> 정상 first-session completion
-> 실패/미완료 취급 금지
```

### PUSH

+11을 실제 승인 확률·failure-family로 해결한다.

성공/실패 어느 쪽이든 다음을 남긴다.

```text
same UID actual outcome
visible state change
next meaningful action
```

실패 결과를 튜토리얼용 무손실 버전으로 바꾸지 않는다.

## 11. Stage 7 — 짧은 UID/의뢰 Payoff

Decision23은 새 고객 캐릭터·고객 수치·세계 사건을 발명하지 않는다.

요구 슬롯:

```text
STARTER_ORDER
-> 실제 제작 UID
-> +10에서 납품/보유 선택 가능
-> +11은 optional risk
-> 결과 후 1~2문장 실제 반응
-> UID 생애에 실제 결과 기록
-> 다음 작품/다음 강화 질문
```

정확한 customer/world owner와 결과 매핑은 다음 `PRECISION_CUSTOMER_LINK` Decision이 소유한다.

## 12. 첫 10분 정보 공개 사다리

| 시점 | 새 P0 정보 | 아직 강제하지 않는 것 |
|---|---|---|
| 첫 제작 | 작품명/등급/UID/기본성능 | 전체 Artistry/수식어 경제 |
| +1 | 단계/성공률/비용/보강재 | MAX/대수선/후기 수리 |
| +3 전후 | CURRENT/손상 가능성 | MAX 구조 밴드 전체 |
| 실제 첫 실패 | recovery +6%p | 실패 family 수학 상세 |
| +10 | 정밀강화 추천/선택 + checkpoint + 평균 본전 | 전체 고급 고객/시장 시스템 |
| +11 preview | MAX/CRITICAL/STOP vs PUSH | 후기 HIGH/MASTERY 공식 |
| 첫 결과 | UID 생애 + 짧은 고객/세계 반응 | 전체 관계/세계 일정 관리 |

원칙:

```text
TEACH_WHEN_NEEDED
NOT_ALL_AT_START
```

## 13. 첫 10분에서 제외

다음은 존재하지만 첫 핵심 선택 전에 강제로 가르치지 않는다.

- 후기 일반 수리 상세 공식/secured multiplier
- MAX 생애 1회 대수선
- DESTROYED Archive/Memorial/Successor 관리
- +100 completion payoff
- 전체 고객 관계 관리
- 전체 세계 일정/Chronicle Set 관리
- 고급 Artistry 가치 공식
- 자동 단조
- 모든 촉매/정밀강화 catalogue의 상세 설명

이 시스템들은 실제 상황이 발생하거나 후속 세션에서 just-in-time으로 공개한다.

## 14. 외부 벤치마크 흡수

외부 게임/세션의 UI나 수치를 복사하지 않고 onboarding 원리만 사용한다.

- `GDC 2016 · The Gamer's Brain Part 2 / ADAPT`: 첫 몇 분의 주의 확보, 학습 우선순위, common onboarding pitfalls를 참고한다.
- `GDC 2024 · Start Right, Start Fun / ADAPT`: Attraction -> Goal -> Effectiveness 순으로 첫 경험을 점검한다.
- `GDC 2026 · Creating Player Expertise / ADAPT`: 정보는 urgency/importance 기준으로 `지금 해야 하는 것`, `필요 직전 보여줄 것`, `이미 경험한 뒤 보강할 것`, `아예 자를 것`로 분류한다.
- `Hades / Supergiant · ADAPT`: 긴 preamble보다 빠르게 gameplay에 진입하는 immediacy 원리를 사용한다.
- `Into the Breach / Subset · ADAPT`: 멋진 기능보다 플레이어가 즉시 이해하는 clarity를 우선한다.

Blacksmith 변환:

```text
FIRST HOOK = 첫 강화 input
FIRST GOAL = +10 확보
FIRST CORE DECISION = +10 STOP vs +11 PUSH
FIRST META PROOF = 같은 UID 결과가 짧은 의뢰/세계 반응에 남음
```

## 15. 3안 비교

### A. WORKSHOP_TOUR_FIRST — REJECT

공방/고객/시장/제작/정밀/경제 메뉴를 먼저 모두 설명한다.

문제:
- 강화 코어 체험이 늦어진다.
- 신규 플레이어가 아직 필요하지 않은 용어를 기억해야 한다.
- SUPPORT가 PRIMARY CORE보다 앞선다.

### B. CORE_THESIS_SPRINT — APPROVED

첫 작품 -> 강화 -> +10 확보 -> +11 STOP/PUSH를 10분 목표로 경험한다.

장점:
- 코어 질문을 실제 플레이로 배운다.
- 현재 권위와 직접 맞는다.
- 이후 시스템을 just-in-time으로 확장 가능하다.

### C. HIGH_LEVEL_COLD_OPEN — REJECT

가짜 +90 작품을 먼저 제공해 극적 파괴/성공을 보여준 뒤 본 게임을 시작한다.

문제:
- 애착 없는 작품의 큰 손실은 Blacksmith UID 생애의 의미를 증명하지 못한다.
- 실제 progression과 다른 tutorial-only 상태가 생긴다.
- spectacle이 코어 decision보다 앞선다.

## 16. 5회 전체 적대 검토

### Loop 1 — 핵심 재미가 늦는가

- 첫 강화 input 목표를 3분 이내로 둔다.
- 장황한 exposition/공방 tour 금지.
- `PASS_WITH_HUMAN_TIMING_TEST`.

### Loop 2 — 튜토리얼 RNG 조작이 신뢰를 깨는가

- scripted failure/hidden success boost/tutorial-only odds 금지.
- 실제 실패가 발생했을 때만 recovery를 teach.
- `PASS`.

### Loop 3 — +10 정밀강화가 인지부하를 폭발시키는가

- full rules는 접근 가능하게 유지하되 추천 경로를 먼저 보여준다.
- hard lock 없음.
- 실제 신규 플레이어가 추천과 전체 선택을 구분하는지는 Human test 필요.
- `PASS_WITH_PLAYTEST`.

### Loop 4 — STOP가 가짜 선택인가

- +10에서 멈춰도 정상 first-session completion.
- +11을 누르지 않아도 progression failure가 아니다.
- `PASS`.

### Loop 5 — 첫 10분이 전체 시스템 강의가 되는가

- 후기 수리/대수선/Archive/+100/customer management/world management/고급 economy를 뒤로 미룬다.
- `PASS`.

새 구조 blocker가 생기면 Loop1로 돌아가 재검토한다.

## 17. Implementation Reality Gate

현재 실제 구현 사실:

```text
MainMenu / New Game = existing runtime
BlacksmithApp shell = existing runtime
WORKSHOP initial state = existing runtime
future route graph = declared
current product WORKSHOP = placeholder-level visual
```

현재 미구현/미검증:

```text
Decision23 first-10 onboarding runtime = NOT_IMPLEMENTED
current-authority Forge flow = IMPLEMENTATION_UNVERIFIED
current-authority Enhancement 13~22 integrated runtime = IMPLEMENTATION_UNVERIFIED
starter-order binding = UNRESOLVED_BY_23
human first-10 completion timing = NOT_RUN
Android first-session validation = NOT_RUN
```

Historical `game_flow_screen.gd`, auto-forge, old enhancement balance는 재사용 후보/역사 증거일 뿐 Decision23 구현 증거가 아니다.

## 18. 구현 이후 Acceptance 후보

Technical:
- New Game에서 실제 first-session 시작 가능.
- 첫 강화 입력까지 불필요한 필수 메뉴 tour 없음.
- tutorial odds와 canonical odds가 동일.
- +10 STOP와 +11 PUSH가 모두 정상 route.
- 실제 작품 UID가 제작부터 첫 결과까지 유지.
- +10 first precision UI는 full rules 접근을 막지 않음.
- +11 preview에서 MAX/CRITICAL 위험을 비색상 정보로 전달.

Human:
- 신규 플레이어 median first enhancement input <= 3분 목표.
- 신규 플레이어 median first STOP/PUSH decision <= 10분 목표.
- 첫 +11 전 `멈추면 무엇을 지키는지 / 도전하면 무엇을 잃을 수 있는지` 설명 가능.
- +10에서 멈추는 것이 실패가 아니라고 이해.
- 첫 실패 시 recovery가 같은 작품의 다음 시도를 돕는다고 이해.
- +10 정밀강화 화면을 `게임 전체를 이해해야만 지나가는 벽`으로 느끼지 않음.

정확 threshold는 Human Playtest 전 product PASS가 아니다.

## 19. 다음 Decision 경계

다음 작업:

```text
PRECISION_CUSTOMER_LINK
```

23이 고정하지 않는 것:
- starter order에 바인딩할 정확 고객/세계 content owner.
- 고객별 요구 능력치와 정밀강화 방식의 exact mapping.
- 고객 반응 수치/보상.
- world-event result formula.
- release-near 화면/Scene 구현.

## 20. 증거 경계

```text
DECISION_23 = USER_APPROVED / PLANNING_CANON
ONBOARDING_TIMING = TARGET_BUDGET / HUMAN_NOT_RUN
HISTORICAL_RUNTIME = REUSE_EVIDENCE_ONLY
CURRENT_PRODUCT_RUNTIME = BLOCKED / IMPLEMENTATION_UNVERIFIED
HUMAN_PLAYER_VALIDATION = NOT_RUN
ANDROID = NOT_RUN
```

제품 구현은 새 사용자 `기획 완료` 선언 전 시작하지 않는다.
