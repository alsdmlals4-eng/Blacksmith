# Blacksmith 기존 프로젝트 감사 보완 — 보관함·판매·연대기

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A11`
>
> Decision ID: `BS-EQUIPMENT-LIFECYCLE-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

- 구형 제품 흐름은 6칸 세션 보관함을 사용한다.
- 비주얼 시안에는 승인되지 않은 `128/150`이 존재한다.
- 일반 판매·방문 상인·이름 고객 인계가 공통 소유권 모델로 분리되지 않았다.
- 판매·파괴·분실 뒤 작품 기록과 활성 보관 공간의 관계가 명확하지 않다.
- 고객별 관계와 장비별 연대기 UI가 부족하다.

## 2. 해결된 기획 목표

`BS-EQUIPMENT-LIFECYCLE-20260801-01`로 다음을 확정했다.

- Vertical Slice 활성 보관함 12칸
- 무손실 `RECOVERY_HOLDING`
- 게임 용량 제한을 받지 않는 `EQUIPMENT_ARCHIVE`
- 단조 전 출력 슬롯 예약
- 소유권·운명·판매 가능 상태 분리
- 일반 시장·방문 상인·이름 고객 3채널
- 판매·인계·회수 원자 트랜잭션
- UID·소유권·운명·연대기 영구 보존
- 6칸 저장의 무손실 이전과 `128/150` 제품 제거

## 3. Finding 판정

| Finding | 기획 목표 | 런타임·경제·검증 |
|---|---|---|
| `BS-AUD-F17` | RESOLVED | OPEN |
| `BS-AUD-F18` | RESOLVED | OPEN |
| `BS-AUD-F19` | RESOLVED | OPEN |

P1 Finding 수는 실제 보관함·판매·Archive·UI·저장·플레이테스트 전까지 유지한다.

## 4. 적대적 실패 조건

```text
보관함 full인데 단조 결과가 유령 상태로 생성
회수 장비가 공간 부족으로 삭제
판매·파괴 뒤 UID 또는 연대기 삭제
ownership와 fate를 하나의 상태로 합침
같은 transaction ID 이중 지급
자동 강화가 판매·인계를 실행
방문 상인이 숨은 가격·무한 재협상 사용
128/150 Placeholder가 제품 용량으로 구현
Archive가 활성 보관함 용량을 사용
```

## 5. 상태

```text
EQUIPMENT_LIFECYCLE_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
RUNTIME_STORAGE_SALES_ARCHIVE: NOT_RUN
ECONOMY_CAPACITY_PLAYTEST: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
