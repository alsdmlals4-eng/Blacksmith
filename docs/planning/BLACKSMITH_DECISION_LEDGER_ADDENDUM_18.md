# 블랙스미스 결정 원장 추가 기록 18

> 상태: `PLANNING_IN_PROGRESS`
>
> 기준일: 2026-07-26
>
> 사용자 결정: 고객 소유 장비도 파괴 시 소멸하며 다른 장비를 제공할 수 있음

---

## 1. 승인 결정

고객 소유 장비는 일반 장비와 동일한 강화 파괴 규칙을 사용한다.

- 무보호 파괴: 장비 즉시 영구 소멸
- 일반 보호 파괴: 단계 하락 후 즉시 사용 가능
- 완전 보호 파괴: 유지
- 고객 장비 전용 DAMAGED·수리·회복 경로 없음
- 고객 장비 전용 보호석 강제 없음

고객 소유 장비가 소멸해도 고객과 관계 데이터는 유지하며, 플레이어는 이후 다른 신규 장비를 제작해 제공할 수 있다.

---

## 2. 장비와 고객의 분리

파괴 결과는 장비 생애의 종료이며 고객 생애의 종료가 아니다.

```text
기존 고객 장비 파괴
→ 기존 장비 영구 소멸
→ 고객 유지
→ 새 장비 제작 가능
→ 새 장비를 별도 이력으로 제공
```

파괴된 장비의 연대기 종료 기록은 남길 수 있지만 복구 가능한 아이템은 남기지 않는다.

---

## 3. 충돌 해결

### `SUPERSEDED`

`docs/planning/BLACKSMITH_MASTER_GAME_DESIGN_PLANNING.md`의 다음 구형 해석을 폐기한다.

- 고객 소유 장비 파괴 시 삭제하지 않고 DAMAGED로 전환
- 이력·소유권·수식어를 보존한 복원
- 복원 흔적과 전용 복원 비용

또한 `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX_ADDENDUM_17.md`에 남긴 고객 장비 파괴 예외 검토 항목은 이 결정으로 해결된다.

---

## 4. 유지되는 경계

- 장비 잠금은 강화 파괴를 막지 않는다.
- 무보호 파괴 확률과 즉시 소멸 문구는 강화 전에 공개한다.
- 고객의 신뢰 반응과 대화는 별도 고객 규칙을 따른다.
- 이 결정은 고정 신뢰 증감값을 추가하지 않는다.
- 보호석·완전 보호의 요구량과 효과는 기존 강화 책임 원본을 따른다.

---

## 5. 책임 원본

- 규칙 문서: `docs/planning/BLACKSMITH_CUSTOMER_EQUIPMENT_DESTRUCTION_2026.md`
- 기계 판독 데이터: `docs/planning/data/blacksmith_customer_equipment_destruction_2026.json`
- 일반 강화 위험: `docs/planning/BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md`
- 완전 보호: `docs/planning/BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md`

동일 주제에서 구형 문서와 충돌하면 본 기록과 고객 소유 장비 파괴 규칙을 우선한다.

---

## 6. 구현 경계

이번 결정은 문서와 기획 데이터만 변경한다.

Godot 런타임 구현은 정확한 `기획 완료`와 `검수 완료` 이후 별도 계획과 PR로 진행한다. Issue #34는 기존 사람·플랫폼 검증을 위해 열린 상태를 유지한다.
