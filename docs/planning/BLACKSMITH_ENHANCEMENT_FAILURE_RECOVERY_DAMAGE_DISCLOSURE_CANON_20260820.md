# [현재 승인] Blacksmith 강화 실패·회복·파손·정보 공개 계약

- Parent Decision: `BS-CORE-20260820-01`
- Decisions: `BS-ENHANCE-20260820-02`, `BS-ENHANCE-20260820-03`, `BS-ENHANCE-20260820-04`
- 사용자 승인: `2026-08-20 KST / 권장안 승인`
- 상태: `USER_APPROVED / PLANNING_CANON`
- Work Mode: `PLAN`
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`
- planning baseline main: `c09d074bd32be889630922896ffdb8ed8c68118d`

## 1. BS-ENHANCE-20260820-02 — 위험 강화 + 실패 누적 회복

강화의 기본 골격은 `RISK_PLUS_RECOVERY_PROGRESS`다.

```text
강화 단계/가치 상승
→ 성공 보상과 실패 위험이 함께 상승
→ 실패 시 실제 비용·손실 발생
→ 동시에 같은 작품 UID에 회복 진전이 누적
→ 다음 시도의 성공 기대가 개선되거나 bad-luck 상한에 접근
```

보호 규칙:

- 실패는 무보상 클릭이 아니다. 최소 하나의 `상태 변화 / 회복 진전 / 새 의사결정`을 남긴다.
- 회복 진전은 성공을 사실상 자동 진행바로 만드는 수준으로 과도하게 강하지 않게 조정한다.
- 회복 진전은 기본적으로 **작품 UID별**로 귀속한다. 값싼 작품에서 실패를 쌓아 고가 작품에 이전하는 account-wide failstack 최적화를 기본 게임으로 만들지 않는다.
- 일반 강화는 빠른 한 번의 입력-결과 리듬을 유지한다.
- `안정 / 표준 / 강행`과 같은 위험 모드는 모든 시도에 강제하지 않고 이정표·고위험 구간에서만 선택 후보로 사용한다.
- 정확한 성공률·회복 증가량·확정 성공 상한은 `BALANCE_BUDGET / USER_PLAYTEST_REQUIRED`다.

## 2. BS-ENHANCE-20260820-03 — 심각 파손 가능, UID·역사 보존

기본 실패 결과군:

```text
FAIL_HOLD
FAIL_DAMAGE
CRITICAL_BREAK_UID_PRESERVED
```

### FAIL_HOLD

- 강화 결과 미상승.
- 시도 비용/작업량은 소비할 수 있다.
- 작품 UID 유지.
- 실패 누적 회복 진전 증가.

### FAIL_DAMAGE

- 작품 UID 유지.
- 작품에 실제 손상 상태가 생긴다.
- 손상은 `계속 도전 / 수리·복원 / 멈추고 사용·인계` 중 새로운 판단을 만든다.
- 손상 자체가 연대기·예술성·보상 총점을 자동 생산하지 않는다.

### CRITICAL_BREAK_UID_PRESERVED

- 일반 초반 실패가 아니라 **명시된 고위험 구간/선택**에서만 발생 후보.
- 작품이 일시적으로 사용 불가가 되거나 큰 복원 비용/과정이 필요할 수 있다.
- UID·소유·과거 강화·사건·연대기 provenance는 삭제하지 않는다.
- 복원 후 과거 파손 사건을 없었던 일로 덮어쓰지 않는다.

기본 계약에서 제외:

- 일반 실패로 작품 UID 영구 삭제.
- 실패 한 번으로 전체 작품 역사를 삭제.
- 파손 반복을 통한 Artistry/Chronicle 자동 파밍.

## 3. BS-ENHANCE-20260820-04 — 강화 전 위험 정보 공개

플레이어는 강화 버튼을 누르기 전에 최소 다음을 이해할 수 있어야 한다.

```text
현재 강화 상태
다음 성공 결과
최종 성공 확률
시도 비용 / 작업량
실패 결과별 최종 확률 또는 명료한 위험
보호 수단 사용 시 바뀌는 것
현재 실패 누적 회복 효과
다음 확보점 / 이정표
```

정보 계약:

- 핵심 확률을 의도적으로 숨겨 긴장감을 만들지 않는다.
- 조건부 위험을 표시할 때 플레이어가 오해하지 않도록 가능하면 **최종 outcome 확률**로 환산해 보여준다.
- 예: `성공 72% / 유지 20% / 손상 8%`처럼 합계가 이해 가능한 형태를 우선한다.
- 보호 수단은 `파손 방지`, `손상 감소`, `비용 증가`, `보상 감소` 등 실제 변화가 무엇인지 직접 보여준다.
- 실패 누적 회복이 다음 성공률에 영향을 주면 숨기지 않는다.
- 모바일 P0 화면에는 핵심 판단 정보만 두고 상세 계산식·역사 데이터는 상세 보기로 보낸다.
- 색상만으로 성공/손상/위험을 구분하지 않는다.

## 4. 외부 원리 ADAPT / AVOID

### Black Desert — ADAPT

공식 Enhancement Guide는 실패 시 `Enhancement Chance`가 증가해 다음 시도의 성공 확률을 높이는 failstack 구조와 실패 시 최대 내구도 감소·단계 하락·일부 장비 파괴를 명시한다.

또한 Ancient Anvil/Agris Essence는 실패 누적이 임계치에 도달하면 100% 성공을 제공한다.

Blacksmith 채택:

- 실패가 다음 성공 기대를 개선하는 원리.
- 고위험 구간에서 손실·보호를 명료하게 보여주는 원리.

Blacksmith 비채택:

- 값싼 장비로 failstack을 의도적으로 쌓아 다른 장비에 이전하는 메타를 코어로 만들기.
- 장기 MMO 재화 노가다와 수십 회 실패를 전제로 한 progression.

공식 출처:

- https://blackdesert.pearlabyss.com/Console/en-us/Game/Wiki?_masterWikiNo=314
- https://blackdesert.pearlabyss.com/Console/en-us/News/Notice/Detail?_boardNo=11667

### Lost Ark — REFERENCE / AVOID

공식 업데이트는 Honing에서 실패 시 증가한 success rate와 Artisan's Energy가 존재하고, 진행 가속 이벤트에서 honing odds와 Artisan's Energy 누적을 함께 크게 올리는 운영 사례를 보여준다.

Blacksmith 채택:

- 낮은 확률 구간에 실패 누적 회복을 함께 두는 원리.

Blacksmith 비채택:

- 장기간 재료 수급을 전제로 한 반복 강화 경제.
- 강화 실패를 콘텐츠 시간 늘리기 수단으로 사용.

공식 출처:

- https://www.playlostark.com/en-gb/news/articles/august-2023-wield-the-storm-release-notes
- https://www.playlostark.com/en-gb/news/articles/ignite-servers-overview

## 5. 기존 Blacksmith 구현의 재사용 경계

`data/crafting/enhancement_balance.json`에는 역사적으로 다음이 이미 존재한다.

- 실패당 pity `+0.04`, 최대 `+0.24`
- 초기 안전 구간
- downgrade/destroy 위험
- `균형 단조 / 안정 단조 / 폭주 단조`

이는 `HISTORICAL_IMPLEMENTED_FIXTURE / REUSE_CANDIDATE`다.

새 Decision과 일치하는 원리는 재사용할 수 있지만 다음 값은 자동 current canon이 아니다.

- max level 100
- 정확 성공률 곡선
- `safe_until_level = 10`
- `destroy_start_level = 30`
- downgrade/destroy 비율
- pity +4%p / cap +24%p
- safeguard 1.8x cost
- overdrive 8% 2-level leap

새 Balance Budget과 사람 플레이테스트로 다시 결정한다.

## 6. Acceptance / 실패 조건

다음이면 설계 실패다.

- 실패가 여러 번 이어져도 다음 시도 조건이 전혀 좋아지지 않는다.
- 실패 누적이 너무 강해 사실상 실패 횟수만 채우면 되는 진행바가 된다.
- 보호 수단을 모든 시도에 무조건 쓰는 것이 수학적 정답이다.
- 고가치 작품을 잃기 싫어서 강화 메인 루프 자체를 회피한다.
- 성공/비용/손실을 알 수 없어 결과가 불공정하게 느껴진다.
- 정보 공개 때문에 모바일 화면이 계산표가 된다.
- UID 생애가 강화보다 상위 메인 루프로 다시 역전된다.

## 7. 증거 경계

- 기획 Decision: `USER_APPROVED`.
- 기존 구현/시뮬레이터: 역사적 기술 증거.
- 새 수치/런타임 구현: `NOT_STARTED`.
- Human usability: `NOT_RUN`.
- Player experience: `NOT_RUN`.
- Android device: `NOT_RUN`.
