# Blacksmith 강화 긴장 곡선 — 5회 전체 적대적 검토

- 입력: `BS-CORE-20260820-01`, `BS-ENHANCE-20260820-02~04`
- 대상: `BLACKSMITH_ENHANCEMENT_TENSION_AND_DDD_REWARD_LADDER_20260820.md`
- 상태: `PLAN_REVIEW_EVIDENCE`
- Human/Player evidence: `NOT_RUN`

## Loop 1 — 초반 성공 과잉

### 공격
`LEARN 90~100%`와 `BUILD_CONFIDENCE 80~95%`가 길면 플레이어는 실제 위험 규칙을 배우지 못하고, 첫 TENSION에서 갑작스런 난이도 절벽을 느낄 수 있다.

### 검증
Blacksmith의 메인은 강화 긴장감이므로 첫 세션에서 실패와 회복을 적어도 한 번은 보여줘야 한다.

### 개선
- 첫 **한 번**만 명시적 tutorial-safe 성공 후보.
- 두 번째 강화부터 실패 가능하되 `FAIL_HOLD`만 사용 가능.
- 첫 세션 10분 안에 `실패 → 회복 진전 → 다음 시도`를 한 번은 경험하도록 콘텐츠 시나리오를 설계하되 RNG로 강제하지 않는다. 테스트 fixture에서 두 경로 모두 확인.

### 재검사
강화에 대한 신뢰를 만들면서 실패 규칙도 조기에 학습 가능.

## Loop 2 — 체크포인트 + pity가 긴장 제거

### 공격
이정표가 영구 floor이고 pity가 강하면 '결국 오른다'는 확정 진행바가 되어 강화 긴장감이 약해질 수 있다.

### 검증
현재 핵심은 멈춤/도전이다. 손실 가능성이 실제로 남아야 한다.

### 개선
- 체크포인트 floor는 **major milestone**에만 사용 후보.
- 체크포인트 사이에서는 `limited downgrade / progress loss / damage / resource loss` 중 실제 손실을 유지.
- 회복 진전은 실패 한두 번으로 결과를 뒤집지 않는다.
- hard guarantee는 bad-luck ceiling의 마지막 안전장치로만 사용.

### 재검사
'얻은 것 보호'와 '구간 내 위험'을 함께 유지할 수 있음.

## Loop 3 — UID별 recovery의 sunk-cost lock-in

### 공격
회복 진전이 작품 UID에 귀속되면 플레이어가 손상된 작품에 너무 많은 비용을 이미 썼다는 이유로 새 작품을 시도하지 못할 수 있다.

### 검증
UID 애착은 보조 가치이며 강화 선택을 왜곡해 강제 집착을 만들면 실패다.

### 개선
- recovery progress는 작품을 보관/교체해도 **소멸하지 않음**.
- 다른 작품을 강화한다고 기존 UID recovery가 감소하지 않음.
- recovery는 거래 가능한 재화로 전환하지 않음.
- 새 작품 시작 비용을 과도하게 높이지 않음.

### 재검사
작품 단위 기억은 유지하면서 switching penalty를 줄일 수 있음.

## Loop 4 — 정확 확률 공개가 계산 게임으로 변질

### 공격
모든 확률·비용·보호 수치를 한 화면에 펼치면 플레이어가 감정보다 기대값 계산만 하게 되고 모바일 화면이 복잡해질 수 있다.

### 검증
정보 은폐는 금지지만 정보 계층화는 가능하다.

### 개선
P0:

```text
성공 X%
유지 Y%
손상 Z%
이번 비용
성공 시 얻는 대표 변화
손상 시 잃는 대표 변화
현재 회복 진전
다음 확보점
```

P1 상세:
- 정확 내부 계산식.
- 재료/촉매 세부 기여.
- 역사 통계.

금지:
- expected value 총점 자동 추천.
- `최적 선택` 버튼.

### 재검사
공정성과 감정적 판단을 동시에 유지.

## Loop 5 — 첫 10분에 Meta payoff가 메인 침범

### 공격
고객/세계 payoff를 빠르게 보여주려다 첫 10분이 대화·보고 화면 위주가 되면 강화 메인 선언과 실제 경험이 다시 뒤집힌다.

### 검증
고객/세계는 강화 결과를 증명하는 보조 payoff다.

### 개선
- 첫 10분 플레이어 조작/판단 시간의 **60% 이상을 강화 준비·시도·결과·멈춤/도전**에 배정하는 테스트 목표.
- 첫 고객/세계 payoff는 `30~90s`의 압축 결과.
- 직접 전투·탐험·긴 대화로 확장하지 않음.
- Meta 결과는 반드시 `왜 이전 강화 선택이 중요했는지` 2~4개 원인으로 되돌려 줌.

### 재검사
Meta가 강화의 증거로 기능하고 주인공이 되지 않음.

## Better Alternative Search

### 대안 A · No checkpoint / full downgrade
긴장은 크지만 이미 얻은 성취의 안정감이 낮고 반복 재강화 피로가 커짐.

### 대안 B · Major checkpoint floor + in-band volatility + UID recovery
확보감·실제 위험·작품 애착·bad-luck 제어를 동시에 보존. **현재 권장.**

### 대안 C · No downgrade / damage only
접근성은 높지만 후반 강화의 단계적 손실 공포가 약해질 수 있음.

### 대안 D · Branching enhancement tree only
확률 긴장을 줄이고 선택 중심으로 전환할 수 있으나 사용자가 확정한 `강화 긴장감 + DDD` 1차 코어와 거리가 멀어짐.

결론: **B 유지**.

## Long-term fit

장기적으로 B는:

- 일반 강화의 빠른 반복.
- major milestone의 확보감.
- 작품 생애의 손상/복원.
- 정밀강화의 이정표 선택.
- 고객/세계 결과의 차별 payoff.

를 하나의 강화 중심 구조로 묶기 가장 쉽다.

## Clean-exit 제한

- 5회 전체 기획 공격 완료.
- 새 P0/P1 구조 결함은 현재 없음.
- `BS-ENHANCE-20260820-05`의 단계 하락 정책은 사용자 Decision 필요.
- 정확 수치/플레이 재미는 `NOT_RUN / NOT_FINAL`이므로 최종 제품 clean exit는 아님.
