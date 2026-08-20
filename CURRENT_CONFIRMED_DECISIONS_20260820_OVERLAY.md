# [현재 우선 Overlay] Blacksmith 2026-08-20 Confirmed Decisions

- 상태: `CURRENT_PRIORITY_OVERLAY`
- 적용 시작: `2026-08-20 KST`
- 이유: 기존 `CURRENT_CONFIRMED_DECISIONS.md`는 2026-08-11 Phase C 진입과 다수 과거 Decision을 장기 원장으로 보존하므로, 최신 재기획을 과거 원장을 파괴하지 않고 우선 적용하기 위한 overlay다.
- 제품 구현: `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`

## 현재 상태

사용자는 2026-08-20 Blacksmith 기획을 다시 열었다. 따라서 기존 원장의 다음 상태는 **역사적 상태**다.

```text
PLANNING_COMPLETE: USER_DECLARED        -> HISTORICAL_2026-08-11
PHASE_C_ENTRY_APPROVED                  -> HISTORICAL_SCOPE_ONLY
PRODUCT_IMPLEMENTATION                  -> BLOCKED_BY_2026-08-20_REPLANNING
```

새 `기획 완료` 사용자 선언 전에는 `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot` 제품 구현을 시작하지 않는다.

## 현재 승인 Decision

### `BS-CORE-20260820-01`

Blacksmith의 1차 코어는 **강화의 긴장감 + DDD**다.

```text
강화 전 기대/위험
→ 멈춤 / 추가 도전
→ 짧고 강한 결과 피드백
→ 보상/손실
→ 다음 한 번의 질문
```

작품 UID·생애는 강화 선택의 무게·기억을 증폭한다. 정밀제작과 고객/세계 생애주기는 강화의 보조 콘텐츠다.

### `BS-ENHANCE-20260820-02`

기본 실패/회복 골격은 `RISK_PLUS_RECOVERY_PROGRESS`다. 실패는 실제 비용/손실을 만들되 작품별 회복 진전을 남겨 무의미한 연속 실패를 제한한다.

### `BS-ENHANCE-20260820-03`

고위험 실패는 작품 손상을 만들 수 있다. 작품 UID와 역사 기록을 보존한다. 이 Decision의 `파손 후 복원 가능` 초기 제안은 `BS-ENHANCE-20260820-06`의 0% 파괴 계약으로 정제된다.

### `BS-ENHANCE-20260820-04`

강화 전에 성공률, 비용, 주요 실패 결과, 보호 효과, 실패 누적 회복, 다음 체크포인트를 이해할 수 있게 공개한다.

### `BS-ENHANCE-20260820-05`

주요 강화 이정표는 확보점으로 보호한다. 체크포인트 사이에서만 제한 단계 하락을 사용하며, 기본 제품 후보는 한 실패 최대 1단계 하락부터 테스트한다. 체크포인트 아래로 내려가지 않는다.

### `BS-ENHANCE-20260820-06`

현재 내구도는 `0~100%` 상태다. `0%`에서 물리 작품은 `DESTROYED`이며 일반 수리/복원/추가 강화/정상 인계가 불가능하다. UID·이름·제작·강화·소유·사건·손상·수리·파괴 원인·Chronicle provenance는 기록으로 영구 보존한다.

### `BS-ENHANCE-20260820-07`

첫 Vertical Slice 기본 강화에는 별도의 `0% 파괴 방지 보험`을 두지 않는다. 일반 수리는 안전 선택이지만 작품을 새 상태로 초기화하지 않는다. 일반 수리는 현재 내구도만 현재 최대 내구도까지 회복한다.

### `BS-ENHANCE-20260820-08`

내구도를 이중 상태로 정제한다.

```text
CURRENT_DURABILITY_PERCENT <= MAX_DURABILITY_PERCENT <= 100
```

- 새 작품: `CURRENT 100 / MAX 100`.
- 일반 수리: `CURRENT = MAX`, MAX는 변화 없음.
- `FAIL_DAMAGE`: CURRENT 손실이 기본이며 MAX는 유지.
- `FAIL_CRITICAL_DAMAGE` 또는 명시적 구조 손상 사건: CURRENT와 MAX를 함께 손상시킬 수 있음.
- MAX가 CURRENT 아래로 내려가면 CURRENT도 새 MAX로 clamp.
- MAX 0%는 CURRENT 0%와 동일하게 물리 작품 `DESTROYED`.
- MAX 손상은 일반 수리로 제거하지 못하는 구조적 흉터다.
- MAX가 낮아질수록 강화 성공 기대에 페널티를 주고, 심한 손상에서는 **앞으로 새로 얻는 강화 성장량**도 감소한다.
- 이미 획득한 공격력·방어력·수식어·과거 강화 보상은 MAX 손상만으로 소급 삭감하지 않는다.

## 현재 튜닝 / 미확정

다음은 승인된 방향의 Balance/UX 테스트 입력이며 확정 수치가 아니다.

- 정확한 성공률과 레벨 매핑
- CURRENT 내구도 손실 범위
- MAX 내구도 손실 범위와 발생 확률
- MAX 상태별 성공률 페널티
- MAX 상태별 신규 강화 효과 배율
- 수리 비용·작업량
- MAX 구조 복구/대수선 기능의 필요 여부와 대가
- 체크포인트 최종 간격
- 저내구도/저최대내구도 경고 threshold
- 파괴된 작품의 memorial/successor 콘텐츠

첫 MAX band 테스트 후보:

```text
MAX 81~100: success 0pp / new effect 100%
MAX 61~80 : success -3pp / new effect 100%
MAX 41~60 : success -6pp / new effect 95%
MAX 21~40 : success -10pp / new effect 90%
MAX 1~20  : success -15pp / new effect 80%
```

`TUNABLE_BASELINE_TEST_PRESET / NOT_FINAL`이다.

## 책임 원본

1. 이 Overlay — 현재 상태와 2026-08-20 승인 요약
2. `docs/planning/BLACKSMITH_CORE_ENHANCEMENT_DDD_HIERARCHY_20260820.md`
3. `docs/planning/BLACKSMITH_ENHANCEMENT_FAILURE_RECOVERY_DAMAGE_DISCLOSURE_CANON_20260820.md`
4. `docs/planning/BLACKSMITH_ENHANCEMENT_CHECKPOINT_AND_DURABILITY_CANON_20260820.md`
5. `docs/planning/BLACKSMITH_MAX_DURABILITY_STRUCTURAL_SCAR_CANON_20260820.md`
6. `CURRENT_CONFIRMED_DECISIONS.md` — 2026-08-11 이전 세부 Decision·역사 원장
7. R2/R3 분야별 기존 canon — 위 최신 Decision과 충돌하지 않는 범위에서 소비

## 검증 경계

- Human/Player validation: `NOT_RUN`
- Android device: `NOT_RUN`
- Accessibility: `NOT_RUN`
- Performance: `NOT_RUN`
- 정확 Balance: `NOT_FINAL`
- 제품 구현: `BLOCKED`
