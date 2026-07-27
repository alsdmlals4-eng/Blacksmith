# 블랙스미스 버티컬 슬라이스 마스터 기획서 v6 — 추가 결정 15

> 상태: `CANDIDATE_AUTHORITY / PLANNING_IN_PROGRESS`
>
> 상위 문서: `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_DRAFT.md`
>
> 선행 추가 결정:
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_01.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_02.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_03.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_04.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_05.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_06.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_07.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_08.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_09.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_10.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_11.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_12.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_13.md`
> - `BLACKSMITH_VERTICAL_SLICE_MASTER_V6_ADDENDUM_14.md`
>
> 결정 기록: GitHub Issue #60
>
> 기준일: 2026-07-27

## 대장간 상징 동반자

블랙스미스의 상징 동반자는 **비성장형 불씨 정령**으로 확정한다.

불씨 정령은 강화 작업대 주변에 머무는 작은 상징 존재다. 브랜드 인지, 짧은 상황 안내와 감정적 반응을 담당하지만, 강화 확률·보상·고객 정답·세계 결과에 영향을 주는 성장 시스템이나 전략 자원이 아니다.

```text
대장간 홈
→ 작업대 주변의 불씨 정령

주요 상황 발생
→ 짧은 시각 반응 또는 보조 안내

핵심 정보
→ 기존 UI·문구·아이콘·숫자가 권위 있는 정보원
```

## 핵심 역할

불씨 정령은 다음 역할만 수행한다.

- 첫 일반 강화의 짧은 조작 안내
- 첫 일반 정밀강화의 이정표 안내
- 첫 고위 정밀강화의 전용 반응
- 성공·실패·단계 하락·영구 파괴에 대한 차등 반응
- 새 방문 고객·판매 결과·세계 소식이 도착했을 때 관련 영역 안내
- 미확인 결과·저장 복구·상태 무결성 오류의 보조 안내
- 대장간 홈의 시각적 브랜드 상징
- 긴 설명 대신 현재 가능한 다음 행동의 짧은 방향 제시

불씨 정령의 반응은 플레이어가 이미 확인할 수 있는 상태를 보조한다. 새로운 규칙이나 숨은 정보를 독점적으로 제공하지 않는다.

## 비성장형 계약

불씨 정령에는 다음 성장·경제 요소를 두지 않는다.

- 레벨
- 경험치
- 능력치
- 장비
- 전용 재화
- 호감도 또는 관계 단계
- 강화 성공률 보정
- 비용 할인
- 보상 배율
- 사건 결과 보정
- 동반자 전용 장기 퀘스트
- 수집형 스킨이 핵심 진행에 주는 효과

외형 변형이나 꾸미기 요소를 후속 범위에서 검토할 수 있으나, 버티컬 슬라이스에서는 별도 성장 루프로 취급하지 않는다.

## 정보 권위와 금지 역할

불씨 정령은 다음을 수행할 수 없다.

- 숨은 강화 확률을 알려줌
- 결과를 미리 예측하거나 암시함
- 특정 진화 후보가 정답이라고 판단함
- 고객 판매의 최적해를 대신 결정함
- 배팅 결과나 세계 사건 결과를 예고함
- 보호 사용을 자동 강제함
- 플레이어 입력 없이 강화·판매·지원·배팅을 확정함
- 불씨의 색·움직임·소리만으로 영구 파괴나 저장 오류를 알림

정확한 확률, 비용, 최대 하락, 영구 파괴 여부, 보호 효과, 고객 요구, 남은 영업일과 저장 상태는 기존 UI가 권위 있는 정보원이다.

## 버티컬 슬라이스 필수 반응

최소 반응 세트는 다음으로 고정한다.

| 상황 | 반응 방향 | 정보 전달 방식 |
|---|---|---|
| 첫 일반 강화 | 짧은 집중·타격 기대 반응 | 강화 버튼과 기본 위험 정보 안내 문구 |
| 첫 일반 정밀강화 | 이정표 도달 반응 | 10단위 진입 문구·아이콘과 함께 표시 |
| 첫 고위 정밀강화 | 단계형 집중·진화 반응 | +50·진화 후보·수식어 UI가 주 정보원 |
| 일반 실패·단계 유지 | 짧은 진정 반응 | 결과 문구와 소비 자원 요약 |
| 단계 하락 | 하강·위축 반응 | 이전·현재 단계와 하락량 표시 |
| 영구 파괴 | 명확하지만 과도하지 않은 소멸·충격 반응 | 장비 이름·이전 단계·손실 요약 필수 |
| 고객 판매 | 이동 방향 또는 짧은 축하 반응 | 판매·소유권 이전 결과 표시 |
| 세계 결과 도착 | `[세계]` 영역 방향 안내 | 탭 배지·결과 요약이 주 정보원 |
| 저장 복구·무결성 오류 | 일반 감정 반응과 구분되는 정지·경고 반응 | 복구 이유·시점·손실 범위 문구 필수 |

반복 플레이에서 모든 일반 강화마다 긴 반응을 재생하지 않는다. 첫 경험과 중요 이정표는 충분히 보여주고, 반복 강화는 짧은 대기·호흡 수준으로 축소한다.

## 대사와 말투 경계

불씨 정령의 안내는 짧고 기능적이어야 한다.

- 한 번에 한 가지 행동 또는 상태만 전달한다.
- 강화 확률·비용·위험 수치를 대사로 장황하게 반복하지 않는다.
- 고객과 세계 인물의 서사를 대신 설명하지 않는다.
- 실패를 조롱하거나 플레이어를 비난하지 않는다.
- 영구 파괴를 가볍게 농담으로 처리하지 않는다.
- 저장 오류를 세계관 연출로 숨기지 않는다.
- 반복 안내는 자동 축소하거나 다시 보지 않을 수 있어야 한다.

정확한 이름, 말투, 대사 길이와 문장 세트는 후속 아트·카피 명세에서 확정한다.

## 위치와 화면 점유

불씨 정령은 `[대장간]` 작업대 주변에 기본 배치한다.

- 현재 장비 외형을 가리지 않는다.
- 성공률·비용·위험·보호 정보 영역을 가리지 않는다.
- 강화 버튼과 길게 누르기 진행도를 가리지 않는다.
- 하단 고정 내비게이션과 겹치지 않는다.
- 하단 패널이 열리면 패널의 정보 우선순위를 침범하지 않는다.
- 고객·세계 화면에서는 상시 떠다니지 않고 필요할 때만 제한적으로 나타날 수 있다.
- 작은 화면과 텍스트 확대 상태에서 숨기거나 위치를 조정할 수 있어야 한다.

불씨 정령을 조작 버튼으로 사용하지 않는다. 정령을 정확히 눌러야 핵심 기능을 실행하는 구조는 금지한다.

## 알림·내비게이션 연계

불씨 정령은 기존 3단계 알림 우선순위를 보조한다.

```text
필수 확인
→ 정령 반응 가능
→ 결과 요약·복구 화면이 먼저

기한·행동
→ 짧은 방향 안내 가능
→ 남은 영업일과 탭 배지가 주 정보

일반 소식
→ 강화 중 방해 금지
→ 대장간 복귀 또는 유휴 상태에서만 제한 반응
```

- 필수 확인을 정령 대사로만 처리하지 않는다.
- 기한 알림은 플레이어를 강제 이동시키지 않는다.
- 일반 소식 반응은 강화 실행·길게 누르기·결과 연출을 중단시키지 않는다.
- 같은 소식에 대한 정령 반응과 탭 배지를 중복 필수 확인으로 집계하지 않는다.
- 안내를 닫아도 실제 약속·기한·세계 상태는 유지한다.

## 접근성 계약

불씨 정령은 특정 감각이나 반응 속도에 의존하지 않는다.

- 모든 기능적 반응에는 텍스트 또는 아이콘 대체 정보가 있다.
- 불씨 색상만으로 성공·실패·위험·오류를 구분하지 않는다.
- 모션 감소 시 흔들림·급격한 이동·섬광·반복 파티클을 줄인다.
- 효과음과 진동을 꺼도 의미가 유지된다.
- 화면 읽기 환경에서는 정령의 장식 반응보다 핵심 UI 읽기 순서를 우선한다.
- 반복 반응과 말풍선을 줄이거나 숨길 수 있는 설정을 제공한다.
- 정령 안내에는 짧은 시간 제한 입력을 요구하지 않는다.
- 정령이 포커스를 강제로 가져가거나 사용자의 화면 읽기 흐름을 중단하지 않는다.

## 성능·적응형 품질

성능 저하 시 불씨 정령의 장식 효과는 우선 축소 대상이다.

권장 축소 순서:

```text
보조 불꽃 입자 감소
→ 잔광·왜곡·반사 축소
→ 대기 애니메이션 빈도 감소
→ 핵심 이정표에만 짧은 반응 유지
```

다음은 성능 때문에 삭제할 수 없다.

- 영구 파괴 결과 문구
- 단계 변화 숫자
- 저장 복구·무결성 오류 정보
- 고객·사건 기한
- 고위 정밀강화 진화와 대표 수식어 정보

불씨 정령의 효과가 안정적인 반복 강화 성능이나 저사양 기기 30fps 하한을 훼손하면 정령 효과를 먼저 축소한다.

## 콘텐츠 제작 파이프라인 경계

불씨 정령은 대표 검투사 세트와 모험가 증명 세트 모두에서 같은 반응 시스템을 사용한다.

- 고객 이름별 전용 핵심 로직을 만들지 않는다.
- 장비 이름별 하드코딩 반응을 만들지 않는다.
- 결과 유형, 이정표 유형, 알림 우선순위와 영역 이동 상태로 반응을 선택한다.
- 콘텐츠별 대사와 연출 자산 차이는 데이터로 교체 가능해야 한다.
- 두 번째 콘텐츠 세트를 위해 별도 동반자 시스템을 만들지 않는다.

권장 반응 키 예시:

```text
FIRST_ENHANCEMENT
FIRST_PRECISION_ENHANCEMENT
FIRST_HIGH_PRECISION_ENHANCEMENT
OUTCOME_SUCCESS
OUTCOME_FAILURE_HOLD
OUTCOME_DOWNGRADE
OUTCOME_DESTRUCTION
CUSTOMER_SALE_CONFIRMED
WORLD_RESULT_AVAILABLE
RECOVERY_REQUIRED
INTEGRITY_ERROR
```

정확한 데이터 스키마와 자산 연결 방식은 구현 계획에서 결정한다.

## 범위 제외

버티컬 슬라이스 필수 범위에서 제외한다.

- 동반자 육성
- 동반자 전투
- 동반자 수집 도감
- 동반자 전용 상점
- 동반자 스킨 판매
- 동반자 관계 엔딩
- 동반자 음성 전체 녹음
- 장시간 대화 장면
- 고객보다 정령이 중심이 되는 서사
- 정령이 강화 결과를 직접 결정하는 기능

## 검증 항목

- 정령이 강화 버튼·위험·비용 정보를 가리지 않는지 확인
- 첫 강화·정밀강화·고위 정밀강화 반응이 서로 구분되는지 확인
- 일반 반복 강화에서 반응이 템포를 방해하지 않는지 확인
- 영구 파괴 반응이 결과를 가볍게 만들지 않는지 확인
- 저장 오류 반응이 일반 실패와 혼동되지 않는지 확인
- 일반 소식 반응이 강화 입력·연출을 중단시키지 않는지 확인
- 무음·무진동·모션 감소 상태에서도 동일 정보를 이해할 수 있는지 확인
- 텍스트 확대와 작은 세로 화면에서 핵심 UI를 가리지 않는지 확인
- 저사양 기준 기기에서 정령 효과 축소 후 성능 하한을 유지하는지 확인
- 검투사·모험가 세트가 같은 반응 키와 구조를 재사용하는지 확인

```text
SYMBOLIC_COMPANION: NON_PROGRESSION_EMBER_SPIRIT
COMPANION_PRIMARY_LOCATION: FORGE_WORKBENCH
COMPANION_ROLE: BRAND_SYMBOL_AND_CONTEXTUAL_GUIDANCE
COMPANION_LEVEL_STATS_CURRENCY: NONE
COMPANION_GAMEPLAY_ADVANTAGE: FORBIDDEN
COMPANION_HIDDEN_INFORMATION_OR_OPTIMAL_CHOICE: FORBIDDEN
COMPANION_AUTO_CONFIRMS_IRREVERSIBLE_ACTION: FORBIDDEN
COMPANION_ONLY_CRITICAL_INFORMATION: FORBIDDEN
COMPANION_REQUIRED_REACTIONS: FIRST_ENHANCEMENT_PRECISION_HIGH_PRECISION_DESTRUCTION_SALE_WORLD_RESULT_RECOVERY
COMPANION_REPEAT_REACTION_REDUCTION: REQUIRED
COMPANION_MOTION_AUDIO_ACCESSIBILITY_FALLBACK: REQUIRED
COMPANION_EFFECTS_ADAPTIVE_QUALITY_PRIORITY: DECORATIVE_EFFECTS_FIRST
COMPANION_SYSTEM_REUSED_ACROSS_CONTENT_SETS: REQUIRED
EXACT_NAME_APPEARANCE_COLOR_VOICE: FOLLOW_UP_ART_AND_COPY_DECISION
MUST_FIX_02_SYMBOLIC_COMPANION: RESOLVED_AT_PLANNING_LEVEL
```
