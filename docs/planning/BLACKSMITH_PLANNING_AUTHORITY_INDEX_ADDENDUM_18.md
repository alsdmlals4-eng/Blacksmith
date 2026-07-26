# 블랙스미스 기획 책임 원본 색인 추가 기록 18

> 상태: `PLANNING_IN_PROGRESS`
>
> 기준일: 2026-07-26
>
> 목적: 고객 소유 장비 파괴 처리의 최신 책임 원본과 구형 예외의 폐기를 명시한다.

---

## 1. 최신 책임 원본

고객 소유 장비 파괴는 다음 문서를 우선 적용한다.

1. `docs/planning/BLACKSMITH_CUSTOMER_EQUIPMENT_DESTRUCTION_2026.md`
2. `docs/planning/data/blacksmith_customer_equipment_destruction_2026.json`
3. `docs/planning/BLACKSMITH_DECISION_LEDGER_ADDENDUM_18.md`
4. `docs/planning/BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md`
5. `docs/planning/BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md`

---

## 2. 최신 규칙

- 고객 소유 장비도 무보호 강화 가능
- 무보호 파괴 시 해당 장비 즉시 영구 소멸
- DAMAGED·수리·회복 경로 없음
- 고객과 관계 기록은 유지
- 플레이어는 다른 신규 장비를 제작·제공 가능
- 신규 장비는 새 장비 ID와 별도 이력을 사용
- 파괴된 장비는 복구 불가능한 연대기 종료 기록만 유지

---

## 3. 구형 문서 덮어쓰기

다음 구형 내용은 `SUPERSEDED`다.

### `docs/planning/BLACKSMITH_MASTER_GAME_DESIGN_PLANNING.md`

- 고객 소유 장비 파괴를 DAMAGED로 변환
- 이력·수식어·소유권을 유지한 복원
- 복원 흔적과 고객 장비 전용 복구 루프

### `docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX_ADDENDUM_17.md`

- 고객 소유 장비 무보호 파괴 예외를 미결정 충돌로 남긴 상태

해당 검토 항목은 `RESOLVED_BY_ADDENDUM_18`로 변경한다.

---

## 4. 구현자 주의

- 고객 장비라는 이유로 파괴 결과를 자동 완화하지 않는다.
- 고객 장비에 보호석을 자동 적용하거나 사용을 강제하지 않는다.
- 무보호 시도 전 파괴 확률과 즉시 소멸을 정확히 표시한다.
- 장비 소멸과 고객 삭제를 연결하지 않는다.
- 파괴된 장비의 연대기 기록을 인벤토리 아이템으로 복원하지 않는다.
- 새 장비 제공은 기존 장비 복구가 아니라 신규 장비 생성이다.

---

## 5. 상태

이 항목의 구조적 충돌은 해결됐다.

세부 신뢰 반응·대화 문구·교체 장비 요청 빈도는 고객 시스템의 `POC_TUNABLE` 데이터로 조정할 수 있으며, 고객 소유 장비의 파괴 규칙을 변경하지 않는다.

Godot 런타임 구현은 정확한 `기획 완료`와 `검수 완료` 이후 별도 계획과 PR로 진행한다.
