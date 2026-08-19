# [제안] Blacksmith 강화 코어 Player Experience Contract

- Parent: `BS-CORE-20260820-01`
- 상태: `PROPOSED / IMPLEMENTATION_BLOCKED`

## 대표 감정 곡선

```text
이 정도면 충분하다
→ 그래도 한 번 더 가면 훨씬 좋아진다
→ 실패하면 아깝다
→ 누를까 / 멈출까
→ 시도
→ 즉시 결과
→ 안도 / 환희 / 아쉬움 / 손상 충격
→ 다음 행동이 바로 떠오름
```

## DDD Micro Contract

강화 한 번은 다음을 모두 가져야 한다.

1. `READ`: 2~3초 안에 현재 상태·성공 기대·비용·주요 실패를 파악
2. `ANTICIPATE`: 입력 직후 너무 길지 않은 짧은 기대 구간
3. `IMPACT`: 결과 순간의 시각·음향·진동/모션 피드백
4. `RESOLVE`: 성공/실패/손상과 바뀐 상태를 즉시 읽음
5. `NEXT`: 멈춤·재도전·보호·수리·정밀강화 중 현재 가능한 다음 행동이 드러남

## 실패도 다음 행동을 만들어야 함

```text
무의미한 실패
= 비용만 사라짐 + 상태 변화 없음 + 다음 시도도 똑같음
→ AVOID

의미 있는 실패
= 비용/기회비용 + 회복 진전 또는 작품 상태 변화 + 새 판단
→ TARGET
```

## 첫 세션 Reward Ladder

```text
SAFE SUCCESS
→ QUICK SECOND SUCCESS
→ FIRST SECURE STOP POINT
→ FIRST REAL RISK
→ RESULT
→ SHORT META PAYOFF
```

첫 위험 강화 이전까지 플레이어는 반드시:
- 강화 성공이 무엇을 주는지 봤고
- 멈추면 무엇을 확보하는지 알고
- 실패하면 무엇을 잃는지 알고
- 자신의 첫 작품을 식별할 수 있어야 한다.

## Player Evidence Questions

실제 release-near Vertical Slice에서 확인:

- 강화 직전 플레이어가 멈춤과 도전 중 하나를 실제로 고민했는가?
- 선택 이유를 자기 말로 설명할 수 있는가?
- 결과 직후 무엇이 바뀌었는지 설명할 수 있는가?
- 실패 후 다시 시도할 의향이 남는가, 아니면 허탈해서 중단하는가?
- 작품의 과거 강화 결과가 다음 판단에 영향을 주는가?
- 정밀제작/고객 콘텐츠가 강화보다 더 재미있다고 느껴져 중심이 뒤집히는가?

현재 실제 Player Evidence: `NOT_RUN`.
