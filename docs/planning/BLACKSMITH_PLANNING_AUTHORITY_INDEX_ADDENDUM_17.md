# 블랙스미스 기획 책임 원본 색인 추가 기록 17

> 상태: `PLANNING_IN_PROGRESS`
>
> 기준일: 2026-07-26
>
> 목적: 최근 강화·보호·경제 결정의 책임 우선순위를 추가하고 구형 `REVIEW_REQUIRED` 상태를 정리한다.

---

## 1. 최신 강화 관련 적용 순서

같은 주제의 규칙이 충돌하면 아래에서 더 아래에 있는 문서가 우선한다.

1. `docs/planning/BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md`
   - `+0~+60` 대표 철검 공개시장 가격과 평균 기대원가 기준
2. `docs/planning/BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md`
   - 일반 강화 6결과 확률, 숙련, 일반 보호와 무보호 파괴
3. `docs/planning/BLACKSMITH_FAILURE_BOUND_PROTECTION_INTERACTION_2026.md`
   - 일반 보호와 실패 완충의 결과 변환
4. `docs/planning/BLACKSMITH_STABLE_STRIKE_SPECIALIZATION_2026.md`
   - 안정 타격의 충전 잔존 효과
5. `docs/planning/BLACKSMITH_ENHANCEMENT_PROBABILITY_DISCLOSURE_2026.md`
   - 일반 강화 정확한 최종 확률 공개
6. `docs/planning/BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md`
   - `+60~+100` 완전 보호, 보호석 경제, `+61~+100` 강화 비용·판매 가격
7. `docs/planning/BLACKSMITH_DECISION_LEDGER_ADDENDUM_17.md`
   - 사용자 승인과 충돌 처리 상태

연결된 `docs/planning/data/*.json`은 해당 문서의 기계 판독 책임 원본이다.

---

## 2. 구형 검토 상태 정리

다음 항목은 최신 문서에서 해결됐으므로 구현 준비 시 `REVIEW_REQUIRED`로 취급하지 않는다.

| 구형 항목 | 최신 책임 원본 | 최신 상태 |
|---|---|---|
| 보호석 가격·제작·획득 곡선 | `BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md` | `POC_TUNABLE / APPROVED_CURRENT` |
| +61~+100 강화 비용·판매가 | `BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md` | `POC_TUNABLE / APPROVED_CURRENT` |
| 실패 완충·보호 파괴 상호작용 | `BLACKSMITH_FAILURE_BOUND_PROTECTION_INTERACTION_2026.md` | `POC_CONFIRMED / APPROVED_CURRENT` |
| 안정 타격 대체 효과 | `BLACKSMITH_STABLE_STRIKE_SPECIALIZATION_2026.md` | `POC_CONFIRMED / APPROVED_CURRENT` |
| 강화 확률 공개 여부 | `BLACKSMITH_ENHANCEMENT_PROBABILITY_DISCLOSURE_2026.md` | `POC_CONFIRMED / APPROVED_CURRENT` |

구형 문서나 JSON에 위 문자열이 남아 있으면 이 색인 추가 기록과 최신 책임 원본을 우선한다.

---

## 3. 현재 남은 구조 충돌

### 고객 소유 장비의 무보호 파괴 예외

구형 통합 게임 기획:

- 고객 소유 장비가 파괴 판정을 받으면 삭제하지 않고 `DAMAGED`로 전환
- 이력·소유권·수식어를 보존하고 복원·교체·기념 보존 선택 제공

최신 일반 강화:

- 보호석 미사용 파괴는 장비 즉시 영구 소멸
- 지속형 `DAMAGED`, 수리, 회복석은 존재하지 않음

상태:

```text
REVIEW_REQUIRED_CUSTOMER_OWNED_EQUIPMENT_DESTROY_EXCEPTION
```

이 충돌은 숫자 조정이 아니라 고객 관계와 역사 장비 보존 철학을 결정하므로 사용자 승인 전 임의로 해결하지 않는다.

---

## 4. 구현 전 확인

1. 최신 강화 확률은 risk 문서·JSON 사용
2. 일반 보호·실패 완충은 interaction 문서·JSON 사용
3. 완전 보호와 고강화 경제는 full protection endgame 문서·JSON 사용
4. 확률 UI는 probability disclosure 문서·JSON 사용
5. 구형 `review_required` 배열만 보고 구현을 차단하지 않음
6. 고객 소유 장비 파괴 예외는 사용자 결정 전 구현하지 않음
7. 정확한 `기획 완료`와 `검수 완료` 게이트 확인
8. Issue #34 유지

Godot 런타임 변경은 없다.
