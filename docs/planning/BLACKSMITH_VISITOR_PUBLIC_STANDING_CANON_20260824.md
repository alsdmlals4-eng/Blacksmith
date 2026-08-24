# [현재 정본] Blacksmith 방문고객 공개등급·이명 계약

- Parent: `BS-CUSTOMER-20260805-01`, `BS-UX-20260805-01`, `BS-CONTENT-20260811-01~09`, `BS-LINK-20260824-24`
- Decision: `BS-CUSTOMER-20260824-26`
- 사용자 지시: `2026-08-24 KST / 방문고객도 이명·등급을 나눠 어느 정도 수준인지 알 수 있게`
- 상태: `USER_APPROVED_INTENT / CURRENT_CANON`
- 제품 구현: `APPROVED_TO_BEGIN_CURRENT_CANON_ONLY`
- Human validation: `NOT_RUN`

## 1. 목적

방문고객 카드에서 플레이어가 이름과 직업만 보고 상대의 대략적인 수준을 추측해야 하는 문제를 줄인다.

```text
ROLE
+ PUBLIC_EPITHET
+ PUBLIC_STANDING_GRADE
```

세 정보는 서로 다른 책임을 가진다.

- `ROLE`: 실제 직업·역할. 예: 유적 탐사대장.
- `PUBLIC_EPITHET`: 세계에서 불리는 이명. 개성·기억을 담당.
- `PUBLIC_STANDING_GRADE`: 공개적으로 알려진 경력·명망의 대략적 수준을 5단계로 표시.

## 2. 채택안 — 5단계 공개등급 + 이명

비교안:

### A. 숫자 Lv. 1~100
- 장점: 즉시 비교 가능.
- 문제: 정확한 전투력/성공률처럼 오해하기 쉽고 고객 능력치·적성·상황 판단을 덮는다.
- 판정: `REJECT`.

### B. 5단계 공개등급 + 별도 이명
- 장점: 수준을 즉시 읽으면서도 정확 전투력 점수로 오해하기 어렵다.
- 이명과 등급의 역할이 분리돼 개성과 정보성을 동시에 확보한다.
- 판정: `ADOPT`.

### C. 고객 archetype마다 별도 계급표
- 장점: 세계관 몰입이 높다.
- 문제: 모험가/군인/수집가/귀족마다 계급을 다시 학습해야 하고 서로 비교하기 어렵다.
- 판정: `DEFER / REJECT_FOR_BASELINE`.

## 3. 공개등급

기계 식별자와 한국어 표시는 다음을 사용한다.

| ID | 표시 | 의미 |
|---|---|---|
| `COMMON` | `일반` | 지역에서 흔히 만날 수 있는 통상 수준의 방문고객 |
| `SKILLED` | `숙련` | 충분한 경험과 검증된 실무 경력을 가진 고객 |
| `ELITE` | `정예` | 고위험·고난도 역할을 맡길 수 있는 상위권 전문 고객 |
| `RENOWNED` | `명망` | 지역·세력 단위로 이름이 널리 알려진 중요 인물 |
| `LEGENDARY` | `전설` | 세계적으로 드문 최상위 명성과 생애 기록을 가진 인물 |

순서는 고정한다.

```text
COMMON < SKILLED < ELITE < RENOWNED < LEGENDARY
```

## 4. 등급의 의미 경계

`PUBLIC_STANDING_GRADE`는 **공개 명망/경력 수준의 요약**이다.

다음으로 자동 변환하지 않는다.

```text
NO_DIRECT_COMBAT_POWER_MULTIPLIER
NO_EVENT_SUCCESS_MULTIPLIER
NO_PRICE_MULTIPLIER
NO_RELATION_MULTIPLIER
NO_REWARD_MULTIPLIER
NO_AUTOMATIC_CUSTOMER_ACCESS_GATE
```

즉 `전설` 고객이라고 사건 성공률이 자동 +20%p 되지 않는다.

실제 성공·적합 판단은 기존대로:
- 고객 능력·적성
- 중량 hard gate
- enhancement contribution
- 정밀강화/기능의 실제 context fit
- 사건 위험/환경

이 소유한다.

등급은 플레이어가 **'이 사람은 어느 정도 급의 인물인가'**를 먼저 읽게 하는 정보다.

## 5. 등급 결정 방식

숨은 종합점수로 실시간 계산하지 않는다.

```text
GRADE_SOURCE
= AUTHORITATIVE_CONTENT_FACT
+ EXPLICIT_MAJOR_LIFECYCLE_PROMOTION_ONLY
```

기본 고객 콘텐츠 작성 시 한 등급을 명시한다.

등급 변화가 필요하면:
- 실제 중요한 경력/세계 사건
- 장기적인 공개 명망 변화
- 명시적 콘텐츠 Decision

중 하나가 있어야 한다.

일반 강화 장비를 한 번 받았거나 고객 일정 한 번 성공했다는 이유만으로 자동 승급하지 않는다.

## 6. 이명

필드:

```text
PUBLIC_EPITHET: String
```

이명은 다음과 분리한다.

```text
EPITHET != ROLE
EPITHET != GRADE
EPITHET != HIDDEN_STAT
```

원칙:
- 이미 알려진 역할·행적·평판과 모순하지 않는다.
- 미래 사건을 미리 확정하지 않는다.
- 능력치/성공률 보너스를 주지 않는다.
- 같은 이름 고객을 기억하고 세계 생애를 연결하는 식별 장치다.

이름 없는 generic visitor는 이명을 비워둘 수 있다. **정본 named visitor는 실제 출시 콘텐츠로 노출되기 전에 이명 또는 의도적 `NONE`을 명시**해야 한다.

## 7. 카드 표시

권장 기본 헤더:

```text
[정예] 「유적의 길잡이」 나디아 벤
유적 탐사대장
```

등급은 색상만으로 표시하지 않는다.

최소:
- 한국어 등급 텍스트
- 필요 시 등급 아이콘/프레임 보조
- 이명
- 본명
- 역할

모바일 기본 카드에서 전체 경력 설명을 펼치지 않는다. 상세 보기에서 등급 근거가 되는 공개 기록을 최대 1~3개 요약할 수 있다.

## 8. Nadia starter baseline

Decision25/24의 first slice에서 Nadia는 다음 baseline을 사용한다.

```text
customer_id = NADIA_VENN
public_standing_grade = ELITE
player_label = 정예
public_epithet = 유적의 길잡이
role = 유적 탐사대장
```

이 설정은 Nadia의 기존 `SURVIVAL_AND_RECOVERY`, 범용성·경량·생존성·회수 가능성, 유적 탐사대장 역할과 충돌하지 않는다.

이명은 Nadia의 실제 미래 탐사 성공을 보장하거나 예언하지 않는다.

## 9. 다른 named visitor migration

기존 R3–R7 named customer를 runtime에 노출하기 전 다음 필드를 반드시 채운다.

```text
customer_id
role
public_standing_grade
public_epithet or explicit NONE
```

Decision26은 현재 이들의 정확한 등급/이명을 일괄 추측해 확정하지 않는다. 각 콘텐츠의 기존 역할·행적을 읽어 migration 시 명시한다.

첫 구현 필수 대상은 Nadia 하나다.

## 10. 벤치마크

### Monster Hunter rank/tier — ADAPT
공식 매뉴얼은 Hunter Rank와 Low/High-rank Quest를 통해 '현재 어떤 수준의 도전을 다룰 수 있는지'를 빠르게 읽게 한다.

Blacksmith는 숫자 HR과 퀘스트 잠금 자체를 복사하지 않고, **수준을 즉시 읽는 명확한 단계 정보**만 채택한다.

### XCOM — ADAPT PRINCIPLE
병사 개개인을 class/rank와 별도 정체성·커스터마이즈로 구분하는 원리를 참고한다.

Blacksmith는 `등급=수준`, `이명=개성/기억`, `역할=직업`을 분리한다.

## 11. 5회 적대 검토

1. 전투력 오해: 등급을 성공률/스탯 자동 배율에서 분리 -> `PASS`.
2. 이명 남발: generic은 비울 수 있고 named만 명시 -> `PASS`.
3. 등급 인플레이션: 일정 1회 성공 자동 승급 금지 -> `PASS`.
4. 고객 시스템의 메인화: 기본 카드 헤더 수준 정보로 제한 -> `PASS`.
5. 접근성: 색상 단독 금지, 텍스트 라벨 필수 -> `PASS`.

## 12. Implementation Reality Gate

```text
VISITOR_GRADE_CANON = APPROVED
VISITOR_EPITHET_CANON = APPROVED
NADIA_ELITE_EPITHET_BASELINE = APPROVED
CUSTOMER_RUNTIME_MODEL = IMPLEMENTATION_REQUIRED
CUSTOMER_CARD_UI = IMPLEMENTATION_REQUIRED
OTHER_NAMED_VISITOR_MIGRATION = NOT_DONE
HUMAN_READABILITY = NOT_RUN
ANDROID = NOT_RUN
```
