# Blacksmith 보관함·판매 채널·장비 연대기 승인 정본

> Decision ID: `BS-EQUIPMENT-LIFECYCLE-20260801-01`
>
> 상태: `USER_PREAPPROVED_RECOMMENDED / CANONICAL_DESIGN_COMPLETE`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 선행 결정: `BS-V9-20260731-05`, `BS-SAVE-20260801-01`, `BS-CUSTOMER-PIPELINE-20260801-01`

## 1. 목적

구형 6칸 세션 보관함과 단일 고객 인계 흐름을, 작품의 활성 보관·판매·소유권·운명·연대기를 분리하는 제품 구조로 전환한다.

핵심 원칙:

```text
활성 장비는 제한된 보관함을 사용
판매·인계·파괴·분실된 장비는 활성 칸을 사용하지 않음
모든 장비의 UID와 연대기는 삭제하지 않음
```

## 2. 저장 영역

### `WORKSHOP_STORAGE`

플레이어가 현재 소유하고 제작·강화·판매·인계할 수 있는 활성 장비.

### `RECOVERY_HOLDING`

고객·세계 사건에서 회수됐으나 활성 보관함이 가득 찬 장비를 임시 보존하는 안전 영역.

- 용량 제한으로 장비를 삭제하지 않는다.
- 해당 장비를 이동하거나 판매하기 전 새 제작을 시작할 수 없다.
- 강화·고객 인계는 선택적으로 제한할 수 있으나 기록 열람은 가능하다.

### `EQUIPMENT_ARCHIVE`

모든 장비의 영구 기록. 활성 보관함 용량을 사용하지 않는다.

- 플레이어 소유
- 시장 판매
- 방문 상인 판매
- 이름 고객 소유
- 분실
- 회수
- 영구 파괴
- 역사화

상태와 무관하게 UID·출생·성장·소유권·사건 기록을 유지한다.

## 3. 용량 정책

### Vertical Slice

```text
workshop_storage_capacity = 12
recovery_holding = lossless temporary queue
archive_capacity = unbounded by gameplay
```

- 기존 6칸은 반복 검증용 PoC 수치로 역사화한다.
- 비주얼 시안의 `128/150`은 계속 `PLACEHOLDER / NOT_CANON`이다.
- 12칸은 Vertical Slice 행동·가독성 검증 기준이며 생산 버전 최종값이 아니다.
- 생산 기본 용량·확장·가격은 실제 제작 빈도·판매율·인지 부하 플레이테스트 후 별도 경제 Decision으로 확정한다.
- 프리미엄 재화 기반 확장은 현행 범위에 없다.

## 4. 출력 슬롯 예약

단조를 시작하기 전에 결과 장비가 들어갈 칸을 예약한다.

```text
ForgeOutputReservation
├─ reservation_id
├─ campaign_revision
├─ reserved_storage_slot
├─ source_action
└─ state: RESERVED | CONSUMED | RELEASED
```

- 보관함이 가득 찼으면 새 작품 단조를 시작하지 않는다.
- 단조 도중 다른 거래로 공간이 바뀌어도 예약된 결과 칸을 유지한다.
- 단조 취소·실패 시 예약을 해제한다.
- 완성 결과 저장과 장비 UID 생성·보관함 배치를 같은 revision에 확정한다.
- 저장 실패 시 빈 칸만 소비하거나 장비만 생성되는 부분 상태를 허용하지 않는다.

## 5. 장비 소유권 상태

```text
PLAYER_WORKSHOP
MARKET_SOLD
VISITING_MERCHANT_SOLD
NAMED_CUSTOMER_OWNED
LOST
RECOVERED_PENDING_STORAGE
DESTROYED
HISTORICAL
```

`ownership_state`와 `fate_state`는 분리한다.

예:

```text
owner = KYLE_VAREN
ownership_state = NAMED_CUSTOMER_OWNED
fate_state = BATTLE_TRACE
```

`DESTROYED`는 운명 상태이며 활성 소유권과 판매 가능성을 종료하지만 Archive 기록은 유지한다.

## 6. 판매·인계 채널

### A. 일반 시장 판매 `GENERAL_MARKET`

- 즉시 판매
- 공개 기본 가격 산식
- 고객 관계·지연 세계 결과 없음
- 소유권은 `MARKET_SOLD`
- 판매 기록과 최종 장비 Snapshot을 Archive에 보존
- 동일 거래 ID 이중 지급 금지

용도: 보관함 정리와 기본 현금화.

### B. 방문 상인 `VISITING_MERCHANT`

- 일정 또는 조건으로 나타나는 제한 구매자
- 장비 범주·등급·태그 기반 공개 구매 조건
- 기본 시장가 대비 공개 가감 이유
- 이름 고객 관계와 장기 세계 결과 없음
- 거래 후 `VISITING_MERCHANT_SOLD`
- 현재 Scope에서 흥정 미니게임·숨은 가격·랜덤 재협상 없음

용도: 특정 장비를 더 나은 가격에 정리하는 간헐적 선택.

### C. 이름 고객 인계 `NAMED_CUSTOMER`

- `BS-CUSTOMER-PIPELINE-20260801-01` 사용
- 계약·범주 eligibility·공개 fit·고객별 관계
- 소유권 이전·지연 세계 결과·운명·연대기
- `DeliveryIntent`와 ResultEnvelope 원자 저장

용도: 작품의 장기 이야기와 관계·세계 환류.

## 7. 채널 공통 금지

- 현재 소유하지 않은 장비 판매
- 제작 미완료·판매 불가·예약 중 장비 판매
- 같은 transaction ID 이중 골드·관계 지급
- 자동 강화가 판매 채널을 선택하거나 실행
- 숨은 정답 채널 추천
- 판매 후 장비 UID·연대기 삭제
- 이름 고객 장비를 일반 시장에서 재판매
- 결과 화면 진입 시 거래 결과 재계산

## 8. 장비 기록 모델

```text
EquipmentRecord
├─ equipment_uid
├─ record_schema_version
├─ creation_snapshot
├─ craftsmanship_grade_id
├─ identity_snapshot
├─ enhancement_summary
├─ current_owner
├─ ownership_state
├─ fate_state
├─ saleability_state
├─ active_storage_location
├─ chronology
├─ applied_transaction_ids
├─ applied_event_ids
└─ last_updated_revision
```

### ChronologyEntry

```text
chronology_entry_id
equipment_uid
event_type
game_day
source_action
actor_id
previous_owner
new_owner
previous_fate
new_fate
summary_key
summary_parameters
related_transaction_or_event_id
save_revision
```

표시 문구 전체를 저장하지 않고 안정적인 key와 parameters를 저장해 localization과 문구 개선을 허용한다.

## 9. 연대기 사건 유형

최소 유형:

```text
CRAFTING_STARTED
CRAFTING_COMPLETED
CRAFTSMANSHIP_GRADE_ASSIGNED
ENHANCEMENT_SUCCESS
ENHANCEMENT_HOLD
ENHANCEMENT_DOWNGRADE
ENHANCEMENT_DESTROYED
IDENTITY_CHOSEN
PLUS50_ROUTE_CHOSEN
SOLD_GENERAL_MARKET
SOLD_VISITING_MERCHANT
DELIVERED_TO_CUSTOMER
WORLD_RESULT_APPLIED
BATTLE_TRACE_GAINED
LOST
RECOVERED
PERMANENTLY_DESTROYED
LEGACY_MIGRATED
```

- 반복 일반 강화는 상세 전체 로그와 요약을 모두 저장할 수 있으나 UI 기본은 구간 요약을 사용한다.
- 비가역 사건은 개별 항목을 숨기지 않는다.
- 구형 데이터에 없는 선택 이유를 발명하지 않는다.

## 10. 보관함 UI

### 목록

- 장비 이미지·이름·제작 등급·강화 단계·계보·소유 상태
- 검색
- 장비 범주·등급·강화 구간·판매 가능·고객 적합 가능 필터
- 이름·생성일·강화 단계·시장가 정렬
- 기본 정렬은 최근 작업, 자동 최적 추천은 없음

### 상세

```text
장비 중심 비주얼
→ 현재 소유·운명·판매 가능 상태
→ 제작 등급·정체성·강화
→ 가치·공개 가격 근거
→ 현재 가능한 행동
→ 연대기
```

- 소유권·운명·판매 가능 여부를 분리 표시한다.
- 연대기는 시간 순서와 사건 유형 필터를 제공한다.
- 판매·인계 CTA는 결과와 소유권 변화를 명시한다.

### 용량 표시

```text
활성 보관함 7 / 12
회수 대기 1
전체 작품 기록 43
```

Archive 수를 용량처럼 표현하지 않는다.

## 11. 공간 부족 UX

### 단조 시작 전

```text
새 작품을 둘 공간이 없습니다.
보관함 장비를 판매하거나 인계한 뒤 다시 시작하세요.
```

가능 행동:

- 보관함 보기
- 일반 시장 판매 화면
- 활성 고객 요청 보기
- 취소

### 회수 발생

- 장비를 `RECOVERY_HOLDING`에 안전 보존
- 결과 Envelope에서 보관함 가득 참을 명시
- 어떤 장비도 자동 판매·파기하지 않음
- 사용자가 공간을 만든 뒤 이동

## 12. 원자 트랜잭션

### 판매

```text
SaleIntent PREPARED 저장
→ 자격·가격 재검증
→ 골드·소유권·보관함·Archive·연대기 변경
→ ResultEnvelope APPLIED 동일 revision 저장
→ 결과 표시
```

### 회수

```text
WorldResult APPLIED
→ 장비 fate RECOVERED
→ 보관함 여유 확인
→ PLAYER_WORKSHOP 또는 RECOVERY_HOLDING
→ 연대기·ResultEnvelope 동일 revision 저장
```

## 13. 테스트 매트릭스

1. 12번째 장비까지 정상 보관
2. 12칸 full에서 단조 시작 차단
3. 예약 후 동시 판매·결과 완료 시 슬롯 중복 0
4. 단조 저장 실패 시 빈 슬롯·유령 장비 0
5. 시장·상인·고객 채널별 소유권과 결과 차이
6. 동일 sale/delivery transaction 이중 지급 0
7. 판매 뒤 Archive UID·기록 유지
8. 파괴 장비 활성 칸 해제·Archive 유지
9. full 상태에서 회수 장비 `RECOVERY_HOLDING`
10. 회수 대기 장비 자동 판매·삭제 0
11. owner/fate/saleability 독립 표시
12. legacy 6칸 저장의 장비 손실 없는 12칸 이전
13. `128/150` Placeholder 제품 데이터 잔존 0
14. 연대기 localization key/parameter 재렌더
15. 자동 강화의 판매·인계 실행 0

## 14. 감사 판정

```text
BS-AUD-F17_PLANNING_TARGET: RESOLVED
BS-AUD-F18_PLANNING_TARGET: RESOLVED
BS-AUD-F19_PLANNING_TARGET: RESOLVED
RUNTIME_STORAGE_SALES_ARCHIVE: NOT_RUN
ECONOMY_CAPACITY_TUNING: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
P1_FINDING_COUNT: 유지
```

## 15. 현재 Gate

```text
VERTICAL_SLICE_ACTIVE_CAPACITY: 12
PRODUCTION_FINAL_CAPACITY: PLAYTEST_REQUIRED
ARCHIVE_CAPACITY: NOT_GAMEPLAY_LIMITED
RECOVERY_HOLDING: LOSSLESS
GENERAL_MARKET: APPROVED
VISITING_MERCHANT: APPROVED
NAMED_CUSTOMER_CHANNEL: APPROVED
EQUIPMENT_UID_HISTORY_PRESERVATION: REQUIRED
PRODUCT_CODE_DATA_UI: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
