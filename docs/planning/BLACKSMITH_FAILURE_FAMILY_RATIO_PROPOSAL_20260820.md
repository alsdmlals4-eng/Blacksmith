# [제안] Blacksmith 실패 결과군 비율 Budget

- Parent: `BS-ENHANCE-20260820-02~09`, `BS-ENHANCE-20260820-12`
- Proposed Decision: `BS-ENHANCE-20260820-13`
- 상태: `PROPOSED_ONLY / USER_DECISION_REQUIRED`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- Human/Player evidence: `NOT_RUN`

## 1. 결정 목적

현재 승인된 실패 결과군은 다음과 같다.

```text
FAIL_HOLD
FAIL_DOWNGRADE
FAIL_DAMAGE
FAIL_CRITICAL_DAMAGE
```

13은 **성공/실패 판정이 실패로 끝났을 때** 어떤 실패 결과군이 선택되는지 경험 밴드별 조건부 비율을 정한다.

중요:

```text
failure_family_ratio = P(family | failure)
```

플레이어 UI는 조건부 비율을 그대로 보여주지 않는다.

```text
P(final family per attempt)
= P(failure on this attempt) × P(family | failure)
```

따라서 회복 진전이나 MAX 상태 때문에 최종 성공률이 바뀌면 UI의 최종 결과 확률도 다시 계산한다.

## 2. 기존 승인 계약과의 결합

### 모든 실패 공통

- 시도 비용/작업량은 현재 계약대로 소비할 수 있다.
- 같은 작품 UID의 실패 누적 회복 진전은 증가한다.
- 실패 결과군 선택 때문에 회복 진전이 사라지지 않는다.

### FAIL_HOLD

- 강화 단계 유지.
- CURRENT/MAX 유지.
- 실패 누적 회복만 증가.

### FAIL_DOWNGRADE

- 첫 테스트에서는 최대 1단계 하락.
- 가장 최근 확보 체크포인트 아래로 내려가지 않는다.
- CURRENT/MAX 손상과 기본 중첩하지 않는다.

### FAIL_DAMAGE

- 강화 단계 유지.
- 밴드별 일반 CURRENT 손상 Budget 적용.
- MAX는 감소하지 않는다.

### FAIL_CRITICAL_DAMAGE

- 강화 단계 유지가 기본.
- 밴드별 심각 CURRENT 손상 적용.
- MAX 구조 흉터를 1회 적용.
- 별도 destroy roll은 없다.
- 실제 CURRENT 또는 MAX가 0이 되었을 때만 `DESTROYED`.

## 3. CRITICAL과 기존 MAX scar Budget의 관계

`BS-ENHANCE-20260820-09`의 다음 범위는 13에서 `FAIL_CRITICAL_DAMAGE` 조건부 비율의 허용 범위로 직접 해석한다.

```text
LEARN             0%
BUILD_CONFIDENCE  0%
FIRST_STOP_POINT  0~5%
TENSION           8~12%
HIGH_STAKES       12~20%
MASTERY           15~25%
```

즉 첫 Vertical Slice에서는 CRITICAL 뒤에 별도 MAX-scar 주사위를 한 번 더 굴리지 않는다.

```text
P(CRITICAL | failure)
= P(MAX scar | failure)
```

CRITICAL이면 승인된 MAX loss 범위를 한 번 적용한다.

## 4. 대안 A · 회복 우선형

실패의 대부분을 HOLD로 보내고 CRITICAL을 기존 허용 범위 하단에 둔다.

| 밴드 | HOLD | DOWNGRADE | DAMAGE | CRITICAL |
|---|---:|---:|---:|---:|
| LEARN | 100% | 0% | 0% | 0% |
| BUILD_CONFIDENCE | 95% | 0% | 5% | 0% |
| FIRST_STOP_POINT | 80% | 5% | 14% | 1% |
| TENSION | 60% | 7% | 25% | 8% |
| HIGH_STAKES | 40% | 10% | 38% | 12% |
| MASTERY | 30% | 15% | 40% | 15% |

장점:
- 실패 스트레스가 낮다.
- 골드+재료 수리 부담이 과도하게 자주 발생하지 않는다.

문제:
- TENSION/HIGH_STAKES에서도 실패가 HOLD로 자주 끝나 `멈춤 vs 한 번 더`의 실질 손실 압력이 약할 수 있다.
- 강화가 실패 누적 회복 진행바처럼 느껴질 위험이 있다.

판정: `LOWER_CONSEQUENCE_BOUND / REJECT_AS_BASELINE`.

## 5. 대안 B · 상태 변화 균형형 — 권장

초반은 HOLD 중심, 중반은 DAMAGE 중심, 후반에 제한 DOWNGRADE와 CRITICAL을 함께 연다.

| 밴드 | HOLD | DOWNGRADE | DAMAGE | CRITICAL |
|---|---:|---:|---:|---:|
| LEARN | **100%** | **0%** | **0%** | **0%** |
| BUILD_CONFIDENCE | **90%** | **0%** | **10%** | **0%** |
| FIRST_STOP_POINT | **65%** | **10%** | **23%** | **2%** |
| TENSION | **45%** | **10%** | **35%** | **10%** |
| HIGH_STAKES | **30%** | **15%** | **39%** | **16%** |
| MASTERY | **20%** | **20%** | **40%** | **20%** |

상태 목표:

```text
PROPOSED_BASELINE_TEST_PRESET / NOT_FINAL_PRODUCT_BALANCE
```

장점:
- LEARN 실패는 작품을 훼손하지 않는다.
- BUILD는 실패 경험을 보여주되 손상 사건은 드물다.
- FIRST_STOP부터 `멈추는 것도 정답`이라는 확보감과 실제 위험이 동시에 생긴다.
- TENSION에서는 실패의 55%가 HOLD가 아닌 상태 변화다.
- HIGH_STAKES에서는 실패의 70%가 HOLD가 아닌 상태 변화지만, 심각 구조 손상은 16%로 제한한다.
- CRITICAL 비율이 기존 MAX scar Budget의 중앙권에 맞는다.

판정: `RECOMMENDED_BASELINE`.

## 6. 대안 C · 결과 압박형

CRITICAL을 기존 허용 범위 상단에 두고 DOWNGRADE/DAMAGE 비율을 크게 올린다.

| 밴드 | HOLD | DOWNGRADE | DAMAGE | CRITICAL |
|---|---:|---:|---:|---:|
| LEARN | 100% | 0% | 0% | 0% |
| BUILD_CONFIDENCE | 85% | 0% | 15% | 0% |
| FIRST_STOP_POINT | 50% | 15% | 30% | 5% |
| TENSION | 30% | 18% | 40% | 12% |
| HIGH_STAKES | 15% | 20% | 45% | 20% |
| MASTERY | 10% | 20% | 45% | 25% |

장점:
- 실패 결과가 무겁고 긴장감이 즉각적이다.

문제:
- 12에서 수리가 골드+일반 구조재료를 모두 요구하므로 DAMAGE 빈도까지 높이면 유지보수 루프가 강화보다 커질 수 있다.
- FIRST_STOP 직후 확보감이 빠르게 훼손될 수 있다.
- HIGH_STAKES가 `도전`보다 `수리/재강화 반복`으로 읽힐 위험이 높다.

판정: `UPPER_CONSEQUENCE_BOUND / REJECT_AS_BASELINE`.

## 7. 권장 B의 최종 시도 확률 예시

아래는 **성공률 범위의 중간값을 예시로 사용한 설명용 계산**이다. 실제 UI는 현재 최종 성공률로 매번 다시 계산한다.

### LEARN · success 95% 예시

```text
SUCCESS   95.00%
HOLD       5.00%
DOWN       0.00%
DAMAGE     0.00%
CRITICAL   0.00%
```

### BUILD_CONFIDENCE · success 87.5% 예시

```text
SUCCESS   87.50%
HOLD      11.25%
DAMAGE     1.25%
```

### FIRST_STOP_POINT · success 80% 예시

```text
SUCCESS   80.00%
HOLD      13.00%
DOWN       2.00%
DAMAGE     4.60%
CRITICAL   0.40%
```

### TENSION · success 67.5% 예시

```text
SUCCESS   67.50%
HOLD      14.625%
DOWN       3.250%
DAMAGE    11.375%
CRITICAL   3.250%
```

### HIGH_STAKES · success 50% 예시

```text
SUCCESS   50.00%
HOLD      15.00%
DOWN       7.50%
DAMAGE    19.50%
CRITICAL   8.00%
```

따라서 `HIGH_STAKES CRITICAL 16%`는 버튼을 누를 때마다 16% 파손이라는 뜻이 아니다. 성공률 50% 예시에서는 최종 시도 기준 8%다.

## 8. 기존 CURRENT 손실 Budget과 결합한 기대 손상

현재 승인 손상량 범위의 중앙값을 설명용으로 사용한다.

| 밴드 | 일반 DAMAGE 중앙값 | CRITICAL 중앙값 | 권장 B 기준 실패 1회당 기대 CURRENT 손실 |
|---|---:|---:|---:|
| BUILD_CONFIDENCE | 4.5 | 없음 | 약 0.45pt |
| FIRST_STOP_POINT | 6 | 12.5 | 약 1.63pt |
| TENSION | 9 | 20 | 약 5.15pt |
| HIGH_STAKES | 15 | 37.5 | 약 11.85pt |

이 값은 출시 목표가 아니라 구조 검증용 산술이다.

의도:
- 초반 실패는 수리 루프를 거의 만들지 않는다.
- TENSION부터 손상을 무시할지 수리할지 고민이 실제로 생긴다.
- HIGH_STAKES에서는 이미 손상된 작품을 한 번 더 미는 선택이 실제 파괴 위험으로 연결된다.

## 9. 실패 resolution — 13 제안

```text
1. final success expectation 계산
2. SUCCESS / FAILURE 판정
3. SUCCESS면 성공 처리
4. FAILURE면 현재 경험 밴드의 family table로 정확히 1개 선택
5. 모든 FAILURE에 item-UID recovery progress 증가
6. HOLD: 추가 상태 손실 없음
7. DOWNGRADE: 최대 1단계, checkpoint floor 적용, CURRENT/MAX 유지
8. DAMAGE: ordinary CURRENT loss 적용, MAX 유지
9. CRITICAL: severe CURRENT loss + MAX loss 1회
10. CURRENT = min(CURRENT_after_direct_loss, MAX_after_scar)
11. CURRENT == 0 or MAX == 0이면 DESTROYED
12. 최종 outcome과 recovery를 UID history에 기록
```

금지:
- DOWNGRADE + DAMAGE 기본 중첩.
- DAMAGE + CRITICAL 이중 선택.
- CRITICAL 뒤 별도 destroy roll.
- CRITICAL 뒤 별도 MAX-scar roll.
- 회복 진전이 높다고 실패 family를 몰래 더 위험하게 바꾸기.

## 10. 실패 누적 회복과 family ratio 분리

첫 Vertical Slice에서는 실패 누적 회복이 **성공률 축만** 변경한다.

```text
recovery_progress -> P(success) 변화
failure_family_table -> band에 고정
```

따라서 플레이어가 여러 번 실패해 성공률이 올라가면 최종 DAMAGE/CRITICAL 확률은 자동으로 내려간다.

예:

```text
TENSION family: HOLD45 / DOWN10 / DAMAGE35 / CRITICAL10

success 60%일 때:
CRITICAL final = 40% × 10% = 4%

recovery로 success 75%가 되면:
CRITICAL final = 25% × 10% = 2.5%
```

회복을 쌓았는데 숨은 실패 severity가 올라가는 반대 보정은 첫 Vertical Slice에서 금지한다.

## 11. 5회 전체 적대적 검토

### Loop 1 — 첫 10분에 실패가 너무 무서운가

공격:
- 강화가 메인인데 첫 실패가 손상/하락이면 신규 플레이어가 강화 자체를 회피할 수 있다.

방어:
- LEARN 실패는 HOLD 100%.
- BUILD는 실패 중 DAMAGE 10%, DOWN/CRITICAL 0%.
- 성공률 중앙 예시에서는 BUILD DAMAGE가 최종 시도 기준 약 1.25%다.

재검사:
- 초반은 규칙 학습과 보상 기대를 먼저 형성한다.

판정: `PASS`.

### Loop 2 — 반대로 TENSION/HIGH가 가짜 위험인가

공격:
- HOLD가 너무 많으면 실패해도 아무 일도 안 일어나고 recovery만 올라가 강화가 진행바가 된다.

방어:
- TENSION 실패의 55%, HIGH 실패의 70%가 HOLD가 아닌 상태 변화다.
- DAMAGE가 주 결과이고 CRITICAL은 제한한다.

재검사:
- 실패가 `수리 / 계속 / 멈춤` 질문을 충분히 만든다.

판정: `PASS_WITH_PLAYTEST`.

### Loop 3 — 골드+재료 수리 때문에 maintenance가 메인을 덮는가

공격:
- DAMAGE 빈도가 높으면 12의 필수 골드+재료 수리와 결합해 정비 반복이 강화보다 더 많은 시간을 차지할 수 있다.

방어:
- BUILD 손상은 매우 낮게 유지.
- TENSION/HIGH에서만 DAMAGE 빈도를 본격 상승.
- 일반 수리는 한 번의 REPAIR_JOB이고 부분수리 연타 없음.
- DAMAGE/CRITICAL은 서로 중첩하지 않는다.

재검사 신호:
- 첫 10분에서 수리 행동이 강화 의사결정 행동의 25% 이상을 지속적으로 차지하면 DAMAGE share 또는 CURRENT loss를 먼저 낮춘다.

판정: `PASS_WITH_MONITORING`.

### Loop 4 — DOWNGRADE가 체크포인트 재노동을 만드는가

공격:
- 단계 하락이 잦으면 확보점 보호가 있어도 같은 1단계를 반복 복구하는 노동이 생긴다.

방어:
- FIRST/TENSION은 10%, HIGH 15% of failures로 제한.
- 한 번에 최대 1단계.
- checkpoint floor 아래로 내려가지 않음.
- downgrade와 durability 손상을 기본 중첩하지 않음.

재검사:
- DOWNGRADE는 손상과 다른 종류의 순간 손실을 만들지만 주 실패 결과가 되지 않는다.

판정: `PASS_WITH_PLAYTEST`.

### Loop 5 — MAX scar Budget과 UI가 서로 어긋나는가

공격:
- failure family와 MAX-scar 주사위를 따로 두면 플레이어가 실제 파손 확률을 이해하기 어렵고 내부 확률도 중복될 수 있다.

방어:
- 13에서 `P(CRITICAL | failure) = P(MAX scar | failure)`로 단일화.
- UI는 최종 시도 확률로 `성공 / 유지 / 하락 / 손상 / 심각손상`을 표시.
- recovery는 성공률만 바꾸고 family ratio는 밴드 안에서 고정.

재검사:
- 숨은 위험 보정 없이 한 화면에서 합계 100% outcome을 계산할 수 있다.

판정: `PASS`.

## 12. 외부 벤치마크 적용

### MapleStory Star Force — ADAPT

공식 가이드는 초반 구간에서 실패 시 하락·파괴를 막고, 높은 단계에서 파괴 위험을 연다. 일부 확보 단계 아래로 떨어지지 않는 보호와 파괴 후 흔적 보존도 존재한다.

Blacksmith 적용:
- 초반 HOLD 중심.
- 확보점 floor 유지.
- 심각 파손은 후반으로 지연.

비채택:
- 외부 Star Force 확률/메소 수치 복사.
- 자동강화를 메인 DDD 경험으로 사용.

공식 참고:
- https://maplestory.nexon.com/Guide/N23GameInformation/Articles/412
- https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force

### Lost Ark Honing — ADAPT / AVOID

공식 운영 자료에서 실패 후 success-rate bonus와 Artisan's Energy가 지속적으로 progression 완화 수단으로 사용된다.

Blacksmith 적용:
- 모든 실패가 UID별 recovery progress를 남김.
- recovery가 높아질수록 최종 실패 결과 확률도 자연스럽게 낮아짐.

비채택:
- 긴 재료 소모형 반복 실패를 콘텐츠 시간으로 사용.

공식 참고:
- https://www.playlostark.com/en-us/news/articles/ignite-servers-overview
- https://www.playlostark.com/en-us/news/articles/august-2023-wield-the-storm-release-notes

### Black Desert Enhancement — ADAPT / AVOID

공식 가이드는 장비 종류와 강화 단계에 따라 실패 시 최대 내구도 감소, 단계 하락, 파괴가 발생할 수 있고 위험 정보를 강화 전에 제공한다.

Blacksmith 적용:
- 실패 결과를 여러 family로 분리.
- 고위험에서 CURRENT/MAX 손상을 실제 결과로 사용.
- 사전 outcome 위험 공개.

비채택:
- 장비 종류별 복잡한 failstack/파괴 메타.
- 수십 회 실패와 복구 재료 파밍을 전제로 한 MMO식 progression.

공식 참고:
- https://www.sa.playblackdesert.com/Pt-BR/Wiki?wikiNo=48
- https://www.kr.playblackdesert.com/ko-KR/Wiki?wikiNo=234

## 13. MASTERY 경계

`MASTERY 20/20/40/20`은 family share의 첫 후보로 포함하지만, 현재 MASTERY의 정확 CURRENT 일반/심각 손실량이 아직 미확정이다.

따라서:

```text
MASTERY family share = PROPOSED_LATE_GAME_TEST_PRESET
MASTERY CURRENT damage magnitude = UNRESOLVED
```

첫 Vertical Slice 승인 핵심은 `LEARN~HIGH_STAKES`다.

## 14. 재검토 조건

다음 중 하나면 B를 재검토한다.

- 첫 세션에서 첫 위험 실패 후 강화 회피가 급증.
- BUILD에서 수리 행동이 의미 있게 반복됨.
- TENSION 실패가 여전히 대부분 `아무 일 없음`으로 인식됨.
- HIGH_STAKES에서 한 번 실패 후 새 작품 제작이 수리/계속보다 지배전략이 됨.
- 수리 행동이 강화 의사결정 행동의 25% 이상을 지속적으로 차지.
- DOWNGRADE 복구가 강화 플레이시간의 큰 비율을 차지.
- CRITICAL final per-attempt 확률을 플레이어가 조건부 확률로 오해.
- recovery가 높아질수록 숨은 severity도 함께 올라가는 구현이 제안됨.

## 15. 승인 요청

현재 권장:

```text
B · 상태 변화 균형형

LEARN             100 /  0 /  0 /  0
BUILD_CONFIDENCE   90 /  0 / 10 /  0
FIRST_STOP_POINT   65 / 10 / 23 /  2
TENSION            45 / 10 / 35 / 10
HIGH_STAKES        30 / 15 / 39 / 16
MASTERY            20 / 20 / 40 / 20 (late-game test only)

order = HOLD / DOWNGRADE / DAMAGE / CRITICAL
```

상태:

```text
PROPOSED_ONLY / USER_DECISION_REQUIRED
```

승인 전에는 Overlay/Authority/current main canon으로 승격하지 않고 제품 code/data/runtime에 반영하지 않는다.
