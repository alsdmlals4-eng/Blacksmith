# Blacksmith 장비 한 점의 생애 PoC 통합 명세

- 작성일: 2026-07-23
- 최종 검토 갱신: 2026-07-24
- 상위 정본: `docs/superpowers/specs/2026-07-23-project-core-design.md`
- MVP Scope: `docs/MVP-003_SCOPE.md`
- Issue: #34
- 상태: `CORE_CONFIRMED / SPEC_READY / IMPLEMENTATION_NOT_STARTED`
- 구현 범위: 철검 1종, 검투사 1명, +0~+10, 피로도·날짜·지연 결과·재방문

## 1. 목적

이 명세는 확정된 프로젝트 코어를 첫 외부 플레이 검증이 가능한 소프트웨어 범위로 변환한다.

> 플레이어가 직접 만든 철검에 애착을 느끼고, +5에서 납품할지 +10까지 더 도전할지 판단하며, 그 선택이 다른 사람의 손에서 만든 결과와 장비 이력으로 돌아오는 과정을 다시 확인하려 하는가?

문서가 존재하는 것과 구현 완료는 다르다. 외부 플레이 행동 증거가 수집되기 전까지 장비 종류, 이벤트 수, 세계 시뮬레이션 규모와 최종 강화 상한을 확정하지 않는다.

## 2. 현재 상태와 책임

| 항목 | 상태 | 책임 |
|---|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / CORE_RECORDED` | 상위 코어 문서 |
| 본 명세 | `SPEC_READY` | 이 문서 |
| 제품 구현 | `IMPLEMENTATION_NOT_STARTED` | Issue #34와 구현계획 |
| 현재 Prototype | 제작·+100 강화·보관·자동 단조 구현 | Script·Scene·Test |
| Android·접근성·성능·외부 플레이 | `NOT_RUN` | 후속 검증 |

PR 병합 순서는 `#31 → #32 → #33`이다. 제품 구현은 #33과 분리된 후속 PR에서 수행한다.

## 3. 진단 점수

아래 값은 플레이 데이터가 아니라 문서·코드·데이터·검증 계약의 정렬을 비교한 분석용 점수다.

| 축 | 점수 | 근거 |
|---|---:|---|
| 정체성 선명도 | 9/10 | 단일 대장장이, 장비 생애, 세계 환류가 일관됨 |
| 시장 차별성 | 8/10 | 생산 수량보다 장비의 출생·소유·사건 기록을 전면화 |
| 코어 루프 인과성 | 8/10 | 제작 선택을 결과 기여와 부족 조건으로 설명 |
| 시스템 집중도 | 8/10 | 직원·직접 전투·예약·실시간 세계 제외 |
| 모바일 적합성 | 8/10 | 입력당 강화 1회, 한 화면 한 판단 |
| 장비 애착 잠재력 | 9/10 | 완성도·강화·수식어·소유자·사건 이력 연결 |
| 세계 잔존 구현 가능성 | 7/10 | 영구 기록과 활동 상태 분리 |
| 위험·보상 가시성 | 8/10 | +5 납품과 +10 욕심 구분 |
| 콘텐츠 확장성 | 7/10 | 공통 문법은 정의됐으나 실제 제작 파이프라인 미검증 |
| 검증 성숙도 | 3/10 | 외부 플레이 행동 증거 없음 |

## 4. 벤치마킹 결론

벤치마크는 요구사항 정본이 아니라 개선 가설의 근거다. 표면 연출·세계관·고유 콘텐츠를 복제하지 않는다.

| 사례 | 채택할 원리 | Blacksmith 적용 | 제외할 요소 |
|---|---|---|---|
| Blacksmith Master | 제작부터 판매까지 가치 사슬 | 제작·강화·납품·세계 결과 연결 | 직원·생산 라인 중심 구조 |
| While the Iron's Hot | 재료가 작품으로 변하는 가시성 | 짧은 제작 피드백과 출생 기록 | 공정별 미니게임 확장 |
| Potion Craft | 직접 도구 조작과 고객 적합 제작 | 촉감·재료·고객 결과 인과성 | 초기 광범위 샌드박스 |
| Anvil Saga | 주문·평판·선택의 세계 결과 | 일정 의뢰·명성·재방문 | 직원 욕구·시설·세력 동시 전면화 |
| Holy Potatoes! A Weapon Shop?! | 무기 판매와 영웅 활동 환류 | 같은 고객 재방문과 외부 활동 결과 | 다수 직원·수량 중심 확장 |
| Fantasy Blacksmith | 재료·부품·숙련으로 장비 정체성 | 영구 완성도와 수식어 | 복수 공정·카지노 동시 핵심화 |

차별화 문장:

> 장비를 대량 생산하는 게임이 아니라, 장비의 출생·성장·소유·사건 기록을 제작하는 대장장이 게임.

## 5. 채택한 구조

### 채택: 도메인 모델 + 얇은 흐름 컨트롤러

```text
GameFlowScreen
  ├─ EquipmentLifecyclePocController
  │    ├─ WorkshopCalendar
  │    ├─ WorkshopResources
  │    ├─ CustomerContract
  │    ├─ EquipmentWorldRegistry
  │    └─ WorldActivityResolver
  ├─ ForgingScreen / ForgingSession
  ├─ EnhancementScreen / EnhancementSession
  ├─ CustomerContractScreen
  ├─ WorkshopHud
  └─ WorldReportScreen
```

- `GameFlowScreen`: 화면 전환과 UI 신호 연결
- `EquipmentLifecyclePocController`: 작업·납품·날짜·보고·재방문 상태 조정
- `WorkshopCalendar`: 날짜와 피로도
- `WorkshopResources`: 골드와 재료
- `CustomerContract`: 납품 가능 여부와 적합도
- `EquipmentWorldRegistry`: 영구 장비 기록과 상태
- `WorldActivityResolver`: 결과 밴드와 설명 가능한 원인

기존 `game_flow_screen.gd`에 모든 도메인을 직접 추가하는 방식과 범용 이벤트 버스 선구축은 사용하지 않는다.

## 6. 확정 범위

### 포함

- 철검 1종
- 검투사 카일 1명과 재방문 1회
- 제작 정밀 결과 3단계
- 영구 완성도 5등급
- +0~+10 강화
- +5 기본 납품 충족선
- +10 선택적 추가 도전과 첫 수식어
- 화염·날카로움 계열
- 피로도, 수동 하루 종료, 잔여 피로도 50% 이월
- 최소 하루 지연 결과
- 영구 장비 이력·명성·관계
- PoC 행동 로그

### 제외

- +11 이상 하락과 +30 이상 파괴를 PoC 결과에 포함
- 방어구·악세서리
- 자동 단조 PoC 참여
- 상인·시장·전쟁·관전·베팅
- 대표작·선택형 복원
- 직원·생산 대기열·작업 예약
- 실시간 전체 세계 시뮬레이션
- 저장 마이그레이션과 장기 콘텐츠 수량 확정

## 7. 용어와 PoC 기준값

| 용어 | 의미 | 영구 여부 |
|---|---|---|
| 정밀 결과 | 마감 타격 입력의 즉시 결과 `STANDARD / GOOD / PERFECT` | 제작 순간 입력 기록 |
| 영구 완성도 | 장비가 어떻게 태어났는지 나타내는 접두어 | 영구 |
| 강화 단계 | 장비가 감수한 위험과 성장 | 성공·실패로 변경 |
| 수식어 | +10 이정표에서 얻는 역할·성질 | 이정표 규칙에 따라 성장 |
| 세계 장비 기록 | 출생·소유·사건·상태의 누적 기록 | 영구 |

### 영구 완성도

아래 명칭과 수치는 **PoC 임시 기준값**이다. 5등급 구조와 영구성은 확정됐지만 표시명·배율·분포는 플레이 증거에 따라 변경할 수 있다.

| ID | 표시명 | 공격 배율 | 가치 배율 | 세계 평가 점수 |
|---|---|---:|---:|---:|
| `ROUGH` | 미숙한 | 0.98 | 0.92 | 0 |
| `STANDARD` | 평범한 | 1.00 | 1.00 | 5 |
| `REFINED` | 정교한 | 1.02 | 1.05 | 10 |
| `EXCELLENT` | 명품 | 1.04 | 1.10 | 15 |
| `MASTERPIECE` | 걸작 | 1.06 | 1.15 | 20 |

낮은 등급도 +10, 수식어, 납품과 모든 PoC 결과에 접근한다.

### 정밀 결과별 분포

| 정밀 결과 | 미숙한 | 평범한 | 정교한 | 명품 | 걸작 |
|---|---:|---:|---:|---:|---:|
| STANDARD | 20% | 55% | 22% | 3% | 0% |
| GOOD | 5% | 40% | 43% | 11% | 1% |
| PERFECT | 0% | 15% | 50% | 30% | 5% |

## 8. 데이터 계약과 호환성

### 제작 결과

```json
{
  "record_schema_version": 1,
  "weapon_id": "iron_sword",
  "weapon_name": "철검",
  "precision_result_id": "GOOD",
  "precision_result_label": "좋은 정타",
  "craftsmanship_grade_id": "REFINED",
  "craftsmanship_grade_label": "정교한",
  "raw_base_attack": 20,
  "base_attack": 20,
  "craftsmanship_attack_multiplier": 1.02,
  "craftsmanship_value_multiplier": 1.05,
  "quality_id": "REFINED",
  "quality_label": "정교한",
  "quality_attack_multiplier": 1.02,
  "quality_value_multiplier": 1.05
}
```

`quality_*`는 기존 강화·보관 소비자를 위한 완성도 호환 별칭이다. 기존 Prototype의 `STANDARD / GOOD / PERFECT / AUTO` 제작 정밀 의미를 새 완성도 ID로 조용히 재해석하지 않는다.

호환 규칙:

1. 신규 수동 제작은 `precision_result_*`와 `craftsmanship_grade_*`를 모두 기록한다.
2. `quality_*`는 신규 기록에서 완성도 별칭이다.
3. 기존 기록에 `craftsmanship_grade_id`가 없으면 legacy `quality_id`를 정밀 결과로 읽고 별도 호환 변환을 거친다.
4. 자동 단조 신규 철검은 `precision_result_id: AUTO`, `craftsmanship_grade_id: STANDARD`로 시작한다.
5. 저장 마이그레이션은 첫 PoC 제외 범위다. 영속 저장을 추가하기 전 schema version과 migration fixture를 별도 승인한다.

### 고객 의뢰

```json
{
  "contract_id": "gladiator_kyle_first_sword",
  "customer_id": "gladiator_kyle",
  "requested_weapon_ids": ["iron_sword"],
  "required_level": 5,
  "stretch_level": 10,
  "preferred_affix_ids": ["sharp", "flaming"],
  "deadline_day_offset": 3,
  "report_delay_days": 1,
  "base_payment": 500,
  "immediate_fame": 1
}
```

### 세계 장비 기록

```json
{
  "record_schema_version": 1,
  "world_record_id": "world-iron-sword-001",
  "equipment_record": {},
  "owner_id": "gladiator_kyle",
  "lifecycle_state": "ACTIVE_OWNER",
  "report_state": "PENDING",
  "delivered_day": 2,
  "next_event_day": 3,
  "history": []
}
```

## 9. 상태 이름공간

코어의 장비 생애 상태와 PoC 보고 처리 상태를 같은 enum으로 섞지 않는다.

### `lifecycle_state`

- `WORKSHOP`
- `ACTIVE_OWNER`
- `EVENT_ELIGIBLE`
- `DORMANT`
- `HISTORICAL`
- `BROKEN_OR_LOST`

### `report_state`

- `NONE`
- `PENDING`
- `RESULT_READY`
- `REPORT_OPENED`
- `RESULT_ERROR`

활동 상한을 넘은 장비는 생애를 삭제하지 않고 `DORMANT`로 전환한다. `ARCHIVED`는 파일 보관 용어로만 쓰고 장비 생애 상태로 사용하지 않는다.

## 10. 강화와 멈춤 판단

### 일반 강화

- 버튼 한 번당 판정 한 번
- +1~+9는 빠른 결과 표시
- 시도마다 골드와 일반 강화 피로도 1 소비
- 결과 확인 전 다음 시도 자동 실행 금지

### 특수 강화

- +10 도달 시 보조재료·촉매·정밀 판정·수식어 후보 선택
- 피로도 3 소비
- 화염석은 `flaming`, 숫돌은 `sharp` 계열 우선

### 선택 구조

- +5: 의뢰 최소 조건
- +6~+9: 가치·공격력과 피로도·비용의 교환
- +10: 첫 수식어와 높은 결과 가능성을 얻는 선택적 목표
- 기한·피로도·비용 때문에 +10이 항상 정답이면 실패

## 11. 피로도와 날짜

| 행동 | 피로도 |
|---|---:|
| 철검 제작 시작 | 3 |
| 일반 강화 1회 | 1 |
| +10 특수 강화 | 3 |
| 중요 장비 복원 | 5, PoC 미사용 |

- 기본 피로도: 20
- 이월: `floor(남은 피로도 × 0.5)`
- 다음 날 피로도: `20 + 이월`
- 별도 상한 없음
- 날짜는 `하루 마치기`로만 진행
- 작업 예약·자동 날짜 진행 없음
- 피로도 부족은 작업 시작만 막고 성공률·완성도를 낮추지 않음

HUD는 `현재 작업 가능량 / 기본 일일량`으로 표시한다. 28/20처럼 기본량보다 큰 값이 오류로 보이지 않게 `현재 28 · 기본 20`을 병기한다.

## 12. 고객 납품과 원자성

납품 가능 조건:

- `iron_sword`
- +5 이상
- 기한 이내
- 파괴되지 않은 대장간 보유 장비

### 원자적 납품

납품은 다음 다섯 효과를 하나의 거래로 처리한다.

1. 보관함 제거
2. 고객 소유권 이전
3. 기본 대금 지급
4. 즉시 명성 지급
5. 세계 장비 기록 생성

모든 사전 검증을 먼저 수행한다. 중간 단계 하나라도 실패하면 장비·골드·명성·소유권·세계 기록을 전부 이전 상태로 복구한다. 같은 `delivery_transaction_id` 재시도는 중복 지급·중복 기록을 만들지 않는다.

결과 데이터 누락은 납품을 되돌리지 않고 `report_state: RESULT_ERROR`로 기록하며 결정적 입력으로 보고 생성을 재시도한다.

## 13. 세계 결과 인과성

### 결정 점수

| 항목 | 점수 |
|---|---:|
| +5 요구 조건 충족 | 20 |
| +10 추가 목표 충족 | 15 |
| 선호 수식어 보유 | 25 |
| 완성도 등급 | 0 / 5 / 10 / 15 / 20 |
| 공격력 기준 충족 | 10 |

### 결과 밴드

| 점수 | 결과 ID | 표시 |
|---:|---|---|
| 0~34 | `DEFEAT` | 패배 |
| 35~69 | `WIN` | 승리 |
| 70 이상 | `DECISIVE_WIN` | 압도적 승리 |

대표 반례:

- 미숙한 +5 철검, 수식어 없음, 공격 기준 충족: 30점 → `DEFEAT`
- 정교한 +5 철검, 수식어 없음, 공격 기준 충족: 40점 → `WIN`
- 명품 +10 철검, 선호 수식어 보유, 공격 기준 충족: 85점 → `DECISIVE_WIN`

난수는 결과 밴드를 바꾸지 않는다. 같은 밴드 안의 문장, 추가 골드 ±10%, 부상·손상 같은 세부 강도만 바꾼다.

보고서는 다음을 분리한다.

1. 효과가 있었던 선택
2. 부족했던 조건
3. 발생한 사건
4. 추가된 장비 이력
5. 명성·관계·다음 의뢰 변화

## 14. 세계 잔존과 재방문

- 납품 장비 기록은 삭제하지 않는다.
- 새 사건을 생성할 `ACTIVE_OWNER / EVENT_ELIGIBLE` 장비 수를 제한한다.
- PoC 활동 상한은 6개지만 실제 첫 PoC에서는 카일의 철검 1개만 활성화한다.
- 상한 초과 시 가장 오래된 비대표 장비를 `DORMANT`로 전환한다.
- 결과 보고를 연 뒤 재방문 플래그가 활성화된다.
- 다음 날 카일이 이전 결과와 부족 조건을 언급한다.
- 첫 PoC는 두 번째 장비 제작 시작 버튼까지 구현한다.

## 15. UI 상태 전이

```text
CONTRACT
→ FORGING
→ ENHANCEMENT
→ INVENTORY_DELIVERY
→ DAY_END
→ DAY_SUMMARY
→ WORLD_REPORT
→ FOLLOW_UP_CONTRACT
```

공통 HUD:

- 날짜
- 현재 작업 가능량·기본 일일량
- 골드
- 의뢰 마감까지 남은 날짜
- `하루 마치기`

기본 카드에는 완성도·강화 단계·대표 수식어 1개·조건 충족·남은 날짜·피로도만 표시한다. 전체 수치와 이력은 상세 영역으로 분리한다.

## 16. 접근성·모바일 계약

- 세로 화면에서 한 번에 주 행동 버튼 1개
- 최소 터치 영역 48dp 상당
- 결과·위험은 색상만으로 구분하지 않고 텍스트·아이콘 병기
- 자동으로 닫히는 결과 창 없음
- 화면 흔들림·진동·모션 감소 옵션
- 반복 탭을 수행하지 못하는 플레이어를 위해 기존 자동 작업을 유지
- **정밀 입력 대안**: 느린 게이지 모드와 넓은 판정 구간을 제공하고, 운동·시간 압박 장벽이 큰 경우 `정밀 보조`를 선택해 GOOD 분포를 사용한다. PERFECT 희귀 보너스를 자동 제공하지 않는다.
- 실패 메시지는 부족 자원·미충족 조건과 복귀 경로를 명시

실제 접근성 PASS는 Android와 사람 검증 뒤에만 판정한다.

## 17. 행동 로그

| 이벤트 | 핵심 필드 |
|---|---|
| `poc_contract_viewed` | day, fatigue, deadline |
| `poc_forging_completed` | precision_result, craftsmanship_grade, tap_count |
| `poc_enhancement_attempted` | from_level, target_level, outcome, fatigue_after |
| `poc_enhancement_stopped` | stop_level, remaining_days, remaining_fatigue |
| `poc_equipment_discarded` | grade, level, reason |
| `poc_equipment_delivered` | grade, level, affixes, fit_score |
| `poc_day_ended` | unused_fatigue, carryover, pending_reports |
| `poc_world_report_opened` | outcome_band, contribution_ids |
| `poc_follow_up_started` | prior_outcome, prior_equipment_id |

네트워크 전송과 개인정보 수집은 하지 않는다. 테스트 세션 내 메모리 로그 또는 명시적 로컬 export만 사용한다.

## 18. 오류 처리

| 오류 | 처리 |
|---|---|
| 피로도 부족 | 부족량 표시, 무차감, 날짜 자동 진행 금지 |
| 골드 부족 | `NO_GOLD`, 피로도·재료 무차감 |
| 재료 부족 | `NO_MATERIAL`, 골드·피로도 무차감 |
| 납품 부적합 | 미충족 조건 표시, 장비·자원 불변 |
| 기한 초과 | 의뢰 종료, 장비 대장간 보유 유지 |
| 납품 중간 실패 | 원자 거래 전체 롤백 |
| 결과 데이터 누락 | `RESULT_ERROR`, 결정적 재시도 |
| 활동 상한 | 비대표 장비 `DORMANT` 전환 |
| UI 화면 손실 | Controller snapshot으로 재구성 |

## 19. 검증 매트릭스

| 영역 | 자동 검증 | 사람 검증 |
|---|---|---|
| 완성도 | 고정 난수·호환 별칭 테스트 | 낮은 등급 폐기 행동 |
| 피로도 | 단위·경계 테스트 | 날짜 진행 체감 |
| 강화 원자성 | 골드·재료·피로도 회귀 | 실패 메시지 이해 |
| 납품 원자성 | 실패 주입·중복 재시도 | 납품 선택 이해 |
| 결과 | 세 밴드·기여 결정 테스트 | 결과 원인 회상 |
| 세계 기록 | 상태 이름공간·이력 순서 | 장비 애착 |
| 재방문 | 상태 전이 통합 테스트 | 다음 제작 의도 |
| UI | Scene smoke·정적 계약 | 세로 화면·터치·가독성 |
| Android | 빌드·실기기 | 발열·프레임·입력 지연 |

## 20. 완료 기준

1. 철검 제작부터 재방문까지 E2E 완주
2. +5 납품과 +10 도전 모두 유효
3. 골드·재료·피로도·납품 원자성
4. DEFEAT/WIN/DECISIVE_WIN 대표 반례 도달
5. 난수가 결과 밴드를 뒤집지 않음
6. 납품 뒤 장비 기록 유지
7. 신규·기존 테스트 전체 PASS
8. Godot import·main·PoC Scene smoke PASS
9. Android·접근성·성능·외부 플레이 미실행을 PASS로 표시하지 않음

## 21. KEEP / AMPLIFY / CHANGE / DEFER

### KEEP

- 한 명의 대장장이
- 직접 제작과 빠른 터치 피드백
- 버튼 입력당 강화 1회
- +10 특수 강화와 수식어 선택
- 판매 장비 세계 이력
- 수동 날짜와 50% 피로도 이월

### AMPLIFY

- +5 납품과 +10 욕심의 멈춤 판단
- 결과의 기여·부족 조건 설명
- 같은 고객 재방문
- 낮은 등급 장비의 다른 역사 가능성

### CHANGE

- 정밀 결과와 영구 완성도 의미 중복
- 도달 불가능한 패배 밴드
- 코어 생애 상태와 PoC 보고 상태 혼용
- 부분 성공 가능한 납품 순서
- 자동 단조 기록의 legacy `quality_*` 의미 충돌
- 색상·빠른 타이밍에만 의존하는 정보·입력

### DEFER

- 최종 강화 상한 확정
- 방어구·악세서리
- 전쟁·관전·베팅
- 대표작·복원
- 다수 고객·시장
- 영속 저장·마이그레이션
- 범용 이벤트 버스
