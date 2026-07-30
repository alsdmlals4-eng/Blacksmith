# 블랙스미스 v9 사용자 결정 기록

> 상태: `USER_ACCEPTED / LOCKED_FOR_CURRENT_PLANNING`
>
> 승인일: `2026-07-31`
>
> 상위 초안: `BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md`
>
> 구현 권한: `NONE`

## 1. 승인 범위

사용자는 2026-07-31에 아래 7개 권장안을 일괄 채택했다.

이 승인은 현재 기획의 기준 결정을 고정한다. 다음을 의미하지는 않는다.

- `기획 완료`
- `검수 완료`
- 제품 구현 승인
- Codex Goal 승인
- Google Sheet 동기화 승인
- 수치 밸런스 확정

```text
권장안 채택
→ 마스터 기획에 반영
→ 남은 P1 세부 기획 진행
→ 전체 정합성·적대적 검수
→ 사용자 기획 완료
→ 사용자 검수 완료
→ 마지막 단계에서 Codex 구현
```

---

## 2. 결정 1 — 제작 등급

### 확정

단조 결과로 고정되는 제작 등급은 5단계를 사용한다.

```text
보통
→ 양질
→ 우수
→ 명품
→ 걸작
```

### 계약

- 제작 등급은 단조 완성도를 나타내는 영구 작품 정보다.
- 강화 단계와 분리한다.
- 낮은 등급도 판매·강화·보관이 가능하다.
- `전설`은 제작 등급명으로 사용하지 않는다.
- 정확한 등급별 수치 배율과 발생 분포는 플레이테스트 조정 대상이다.

```text
CRAFTSMANSHIP_GRADE_MODEL: FIVE_TIERS
CRAFTSMANSHIP_GRADE_NAMES: 보통_양질_우수_명품_걸작
STATUS: ACCEPTED
```

---

## 3. 결정 2 — 수식어 슬롯 구조

### 확정

```text
계보 수식어 1개
+ 보조 수식어 최대 2개
```

### 계약

- 계보 수식어는 장비의 대표 성장 방향과 한 문장 정체성을 담당한다.
- 보조 수식어는 세부 성능·사용 맥락을 담당한다.
- +50 대표 특수 수식어는 새 슬롯이 아니라 계보 수식어의 승격 형태다.
- 수식어를 무제한 누적하지 않는다.
- +10마다 새 슬롯을 추가하지 않는다.

```text
AFFIX_MODEL: ONE_LINEAGE_PLUS_TWO_SECONDARY
PLUS_50_SPECIAL_AFFIX: LINEAGE_UPGRADE
STATUS: ACCEPTED
```

---

## 4. 결정 3 — 강화 이정표

### 확정

| 강화 단계 | 정체성 결과 |
|---:|---|
| +10 | 계보 수식어 최초 획득 |
| +20 | 보조 수식어 1개 획득 |
| +30 | 계보 수식어 강화 또는 방향 선택 |
| +40 | 보조 수식어 2개째 획득 |
| +50 | 진화 + 계보 수식어의 대표 특수 형태 승격 |
| +60 이상 | 신규 슬롯 없이 기존 수식어 심화 |

### 계약

- +50에서 장비 정체성이 한 차례 완성된다.
- +60 이상은 UI와 밸런스가 폭발하지 않도록 신규 슬롯을 늘리지 않는다.
- 정확한 수식어 풀, 효과량, 재선택 규칙은 후속 기획과 플레이테스트 대상이다.

```text
IDENTITY_MILESTONE: COMPLETES_AT_PLUS_50
POST_PLUS_50_GROWTH: EXISTING_IDENTITY_DEEPENING
STATUS: ACCEPTED
```

---

## 5. 결정 4 — 방문 고객의 거래 자격과 적합 신호

### 확정

```text
거래 자격
= 요청 범주 일치 + 제작 완료 + 판매 가능 + 플레이어 보유

공개 적합 신호
= 제작 등급·계보·보조 수식어·연대기와 고객 가치관의 일치
```

### 적합 신호 영향

- 공개 매입 가격
- 관계 변화 방향
- 후속 세계 사건의 유리·불리 방향
- 고객 반응
- 장비 연대기 결과 문구

### 필수 원칙

- 낮은 적합도여도 거래할 수 있다.
- 숨은 합격·실패 조건을 두지 않는다.
- 고객이 왜 해당 장비를 높거나 낮게 평가하는지 공개한다.
- 자동 추천·자동 선택·자동 확정을 사용하지 않는다.
- 적합도는 단일 정답이 아니라 작품 보존, 현금화, 관계, 세계 결과 사이의 선택을 만든다.

```text
CUSTOMER_MODEL: CATEGORY_ELIGIBILITY_PLUS_DISCLOSED_FIT
HIDDEN_CUSTOMER_REQUIREMENTS: FORBIDDEN
AUTO_SELECT_PRODUCT: FORBIDDEN
STATUS: ACCEPTED
```

---

## 6. 결정 5 — 장비 운명 상태

### 확정

수치형 내구도와 반복 수리 운영은 사용하지 않는다.

허용되는 장비 운명 상태는 다음과 같다.

```text
정상
전투 흔적
분실
회수
영구 파괴
```

### 전투 흔적 계약

- 내구도 수치가 아니다.
- 장비 사용 불가 상태가 아니다.
- 반복 수리 비용을 요구하지 않는다.
- 외형, 가치, 수식어 설명, 장비 연대기에 영향을 주는 서사 상태다.
- 세계에서 실제로 사용된 작품이라는 기억을 강화한다.

```text
DURABILITY_SYSTEM: NOT_PRESENT
REPAIR_MAINTENANCE_LOOP: NOT_PRESENT
FATE_STATE_MODEL: NARRATIVE_ONLY
STATUS: ACCEPTED
```

---

## 7. 결정 6 — 두 번째 콘텐츠 제작 기반 증명

### 확정

두 번째 콘텐츠 세트는 `수집가`를 사용한다.

```text
방어구 또는 의식 장비 범주 요청
→ 제작 등급·희소성·계보·연대기 적합 신호 비교
→ 제품 직접 선택·판매
→ 짧은 감정·전시 결과
→ 가치·연대기 갱신
```

### 적용 범위

- 대표 15~25분 Vertical Slice는 검투사 루프를 완주한다.
- 수집가 세트는 별도 결정론적 제작 파이프라인 증명 시나리오로 완주한다.
- 검투사와 같은 요청·선택·판매·소유권·저장 구조를 재사용한다.
- 수집가 전용 핵심 엔진이나 별도 저장 구조를 만들지 않는다.
- 상인과 모험가의 장기 콘텐츠는 본제작 후순위다.

```text
SECOND_CONTENT_SET: COLLECTOR
SECOND_SET_EXECUTION: SEPARATE_DETERMINISTIC_PIPELINE_SCENARIO
CUSTOMER_SPECIFIC_CORE_ENGINE: FORBIDDEN
STATUS: ACCEPTED
```

---

## 8. 결정 7 — 미래 온라인 명칭

### 확정

```text
사용자 노출명: 명작 전당
내부 기능 분류: +50 이상 고등급 작품 랭킹·비교
```

### 계약

- 단일 전투력 점수만으로 작품을 줄 세우지 않는다.
- 강화 단계, 제작 등급, 수식어, 장비 종류, 진화 형태, 공개 연대기를 함께 비교한다.
- 시즌 명작과 역대 명작을 분리할 수 있다.
- 등록은 선택적이며 서버 검증을 통과한 작품만 허용한다.
- 온라인 등록 실패가 로컬 장비·저장·싱글플레이에 영향을 주지 않는다.
- 게임 성능 보상을 제공하지 않고 명예·감상·비교 중심으로 둔다.

```text
FUTURE_ONLINE_NAME: 명작 전당
FUTURE_ONLINE_SCOPE: PLUS_50_OR_HIGHER_MASTERWORK_COMPARISON
IMPLEMENTATION: NOT_AUTHORIZED
STATUS: ACCEPTED
```

---

## 9. 결정 8 — 벤치마킹 선행 작업 원칙

### 확정

매 작업마다 대규모 조사를 반복하지 않는다.

다만 다음 항목을 새로 설계하거나 핵심 계약을 변경할 때는 설계 전에 벤치마킹을 반드시 수행한다.

- 새 시스템
- 핵심 규칙
- 콘텐츠 구조
- 주요 UX 흐름
- 경제·저장·서버·랭킹처럼 여러 소비자에 전파되는 규칙

### 계약

```text
새 설계 질문 정의
→ 관련 공식·1차 출처 조사
→ 채택·변형·제외 분류
→ Blacksmith 코어에 맞춘 추천안
→ 전파 지도와 검증 기준 기록
→ 기획 반영
```

- 이미 최근 조사한 동일 작업군은 관련 결과를 재사용할 수 있다.
- 문장 정리·단순 동기화·승인 계약 내부의 미세 조정은 새 조사를 요구하지 않는다.
- 다른 게임의 명칭·캐릭터·수치·카피·아트를 복제하지 않는다.
- 상세 규칙은 `BLACKSMITH_BENCHMARK_FIRST_WORKING_PRINCIPLE.md`를 따른다.

```text
BENCHMARK_BEFORE_NEW_SYSTEM: REQUIRED
BENCHMARK_BEFORE_CORE_RULE_CHANGE: REQUIRED
BENCHMARK_BEFORE_CONTENT_STRUCTURE_CHANGE: REQUIRED
BENCHMARK_BEFORE_MAJOR_UX_FLOW_CHANGE: REQUIRED
REPEAT_FULL_RESEARCH_EVERY_TASK: FORBIDDEN
STATUS: ACCEPTED
```

---

## 10. 일괄 승인 결과

```text
CRAFTSMANSHIP_GRADE: FIVE_TIERS
AFFIX_MODEL: ONE_LINEAGE_PLUS_TWO_SECONDARY
IDENTITY_MILESTONE: COMPLETES_AT_PLUS_50
CUSTOMER_MODEL: CATEGORY_ELIGIBILITY_PLUS_DISCLOSED_FIT
DURABILITY: NOT_PRESENT
FATE_STATE: NARRATIVE_ONLY
SECOND_CONTENT_SET: COLLECTOR
FUTURE_ONLINE_NAME: 명작 전당
BENCHMARK_FIRST_WORKING_PRINCIPLE: ACCEPTED
USER_RECOMMENDATION_DECISIONS: ACCEPTED
READY_FOR_기획_완료: NO
READY_FOR_검수_완료: NO
CODEX_IMPLEMENTATION: BLOCKED
```

## 11. 다음 기획 대상

채택 결정 이후 다음 항목을 구체화한다.

1. 불씨 정령의 이름·성격·말투·외형
2. 대표 검투사의 이름·성격·야망·경기 맥락
3. +50 대표 진화 후보 2~3개
4. 계보·보조 수식어의 초기 콘텐츠 풀
5. 수집가 두 번째 세트의 장비·전시 결과
6. 첫 5분 튜토리얼과 화면별 정보 위계
7. 명작 전당의 공개 제작자명·삭제·시즌 정책
8. Google Sheet 동기화 계획

1~7의 벤치마킹 기반 추천안은 `BLACKSMITH_P1_CONTENT_UX_BENCHMARK_AND_DESIGN_2026.md`에서 관리한다.

이 항목의 전체 정합성을 검토한 뒤에만 사용자 `기획 완료` 판정을 요청한다.
