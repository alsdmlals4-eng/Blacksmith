# Blacksmith 핵심 정본 충돌 해소 원장 05

- Decision ID: `BS-CORE-20260803-03`
- 승인 시각: `2026-08-03 07:53 KST`
- 상태: `USER_APPROVED / STRUCTURE_CANON_NUMBERS_VERSIONED_TEST_PRESETS`
- 추적 Issue: `#79`
- 권위 복구 Draft PR: `#94`
- 제품 구현 권한: `NONE`
- 제품 코드·Scene·런타임 데이터·에셋 변경: `PROHIBITED`

## 결정 — 경제 구조는 정본, 정확한 숫자는 버전형 테스트 프리셋

사용자 승인:

- `권장안대로 진행`

### 확정 내용

1. 경제·강화·피로도·날짜 시스템의 관계, 소비 시점, 실패·손상·복원 경계와 정보 공개 규칙은 정본으로 유지한다.
2. 기존 문서·Sheet·Prototype에 남아 있는 강화 비용, 성공 확률, 피로도 소비, 보상량, 날짜 수, 재방문 간격 등 정확한 숫자는 삭제하지 않는다.
3. 사람 플레이와 행동 증거로 검증되지 않은 정확한 숫자는 `CURRENT` 또는 제품 확정값으로 취급하지 않고 `BASELINE_TEST_PRESET`으로 재분류한다.
4. 각 테스트 프리셋에는 고유 버전, 적용 범위, 사용한 빌드·세션, 변경 변수, 검증 가설과 결과를 기록한다.
5. 프리셋은 버티컬 슬라이스를 실행하기 위한 초기값이며 제품 출시 경제를 확정하지 않는다.
6. 한 번의 실험에서는 가능한 한 핵심 변수 하나만 조정하고 나머지 값은 고정해 원인 해석 가능성을 유지한다.
7. 둘 이상의 변수를 함께 조정해야 할 경우에는 복합 변경임을 명시하고 단일 변수 효과를 주장하지 않는다.
8. 수치는 플레이어가 실제로 보인 행동과 이해 증거를 근거로 평가한다. 예: 강화 지속·중단 판단, 자원 우선순위, 피로도 사용, 복원 선택, 세계 결과에 대한 인과 이해.
9. 하나 이상의 테스트에서 긍정적 결과가 나왔다는 이유만으로 즉시 확정하지 않는다. 반복 검증과 반례 확인을 거친 값만 `CURRENT_VALIDATED` 후보가 된다.
10. `CURRENT_VALIDATED` 승격에는 Decision ID, 테스트 프리셋 버전, 증거, 적용 범위와 알려진 한계를 함께 기록해야 한다.
11. 확정된 구조가 바뀌지 않는 범위의 숫자 조정은 밸런스 실험으로 취급한다. 소비 시점, 반환 여부, 파괴 조건, 피로도의 역할처럼 구조적 의미가 바뀌면 새로운 기획 결정과 사용자 승인이 필요하다.
12. 정확한 숫자를 문서에서 제거해 실행 불가능하게 만들지 않고, 숫자가 정본 관계보다 우선하는 상황도 허용하지 않는다.

### 권위 계층

```text
정본 불변 규칙
- 어떤 자원이 존재하는가
- 언제 소비되는가
- 무엇을 사전에 공개하는가
- 실패·손상·복원이 어떤 상태 전이를 따르는가
- 피로도와 날짜가 어떤 판단을 만드는가
- 어떤 행동이 일일·세계 진행을 발생시키는가

버전형 테스트 프리셋
- 강화 비용
- 성공 확률
- 피로도 소비량
- 재료·촉매 수량
- 보상량
- 날짜 진행량
- 재방문 간격
- 손상·복원에 필요한 정확한 수치

검증 결과
- 행동 관찰
- 인터뷰 응답
- 실패·이탈 지점
- 변경 전후 비교
- 반례와 알려진 한계
```

### 상태 분류

- `LEGACY_IMPLEMENTED_VALUE`: 과거 Prototype 또는 기존 빌드에 실제 구현됐던 값
- `BASELINE_TEST_PRESET`: 다음 검증에 사용하는 초기 프리셋
- `EXPERIMENT_VARIANT`: 기준 프리셋과 비교하는 실험값
- `CURRENT_VALIDATED`: 반복 검증과 사용자 승인으로 현재 유효 범위가 확인된 값
- `DEPRECATED_PRESET`: 더 이상 사용하지 않지만 추적을 위해 남기는 값

같은 숫자가 과거 구현값이면서 현재 기준 프리셋으로 재사용될 수 있으나, 두 상태와 근거를 구분해 기록한다.

### 프리셋 최소 계약

각 프리셋은 최소한 다음 정보를 가진다.

```text
preset_id
version
status
source_decision_ids
build_or_slice_scope
changed_variable
fixed_variables
hypothesis
values
observed_evidence
result
known_limitations
next_action
```

### 보호 조건

- 과거 숫자를 근거 없이 삭제하거나 현재 제품값으로 승격하지 않는다.
- 프리셋 숫자를 Game Bible의 불변 규칙처럼 서술하지 않는다.
- 여러 값을 동시에 바꾸고 특정 하나가 원인이었다고 단정하지 않는다.
- 평균 성공률이나 세션 완료율만으로 핵심 재미가 증명됐다고 보지 않는다.
- 경제 수치가 플레이 시간을 인위적으로 늘리거나 피로도를 모바일 스태미나 장벽으로 만들지 않게 한다.
- 확률·비용·위험은 플레이어의 판단 전에 확인 가능해야 한다는 기존 원칙을 유지한다.
- 테스트 과정에서 과도한 손실·강제 대기·반복 노동이 발생하면 수치 문제가 아니라 구조 문제인지 함께 검토한다.
- 원격 설정·실험 도구의 존재를 전제로 제품 범위를 확장하지 않는다. 초기 검증은 로컬 데이터 프리셋으로도 가능하다.

### 벤치마킹 적용

- 상용 게임 개발에서는 밸런스 숫자를 코드·정본에 영구 고정하기보다 설정값과 실험 변형으로 관리하고, 통제군과 변경군을 비교해 조정하는 방식이 널리 사용된다.
- Blacksmith는 온라인 운영·서버 기능을 현재 구현 범위로 확정하지 않았으므로 원격 설정 시스템 자체를 요구하지 않는다.
- 채택하는 것은 `정본 구조와 조정 가능한 숫자의 분리`, `버전 추적`, `가설 기반 단일 변수 실험` 원칙이다.
- 경쟁작이나 도구의 수치·운영 방식을 복제하지 않는다.

참고한 공식 자료:

- Unity Remote Config documentation: `https://docs.unity.com/ugs/en-us/manual/remote-config/manual/what-is-remote-config`
- Unity Game Overrides / A/B testing guidance: `https://docs.unity.com/ugs/en-us/manual/game-overrides/manual/ab-testing`
- PlayFab Experiments documentation: `https://learn.microsoft.com/en-us/gaming/playfab/live-service-management/game-configuration/experiments/`

### 정본 우선순위

본 결정은 다음 표현보다 우선한다.

- 과거 Prototype의 정확한 비용·확률·피로도·보상값을 현재 확정 요구사항으로 보는 해석
- 모든 정확한 숫자를 삭제해 버티컬 슬라이스 초기 프리셋을 없애는 해석
- 한 번의 테스트 결과만으로 숫자를 제품 확정값으로 승격하는 해석
- 숫자 변경을 기록하지 않거나 어떤 빌드·가설에서 사용했는지 추적하지 않는 방식

정리 후 표준 문구:

> Blacksmith의 경제·강화·피로도·날짜 관계와 상태 전이 규칙은 정본으로 관리한다. 정확한 비용·확률·소비량·보상량·간격은 버전형 `BASELINE_TEST_PRESET`과 실험 변형으로 관리하고, 반복된 사람 플레이 증거와 사용자 승인을 거친 값만 적용 범위를 명시해 `CURRENT_VALIDATED`로 승격한다.

### 후속 정본 조치

모든 충돌 질문을 완료한 뒤 PR #94에서 일괄 적용한다.

- Game Bible: 정확한 숫자를 불변 규칙과 테스트 프리셋으로 구분
- POC·Prototype 문서: 기존 수치를 `LEGACY_IMPLEMENTED_VALUE`로 보존하고 현재 기준 프리셋 여부를 별도 표시
- Roadmap·MVP Scope: 버티컬 슬라이스 프리셋 버전과 행동 가설 연결
- Sheet: `CURRENT`로 남은 미검증 경제 수치를 `BASELINE_TEST_PRESET` 또는 `LEGACY_IMPLEMENTED_VALUE`로 재분류
- 데이터 계약: 프리셋 ID·버전·상태·가설·증거·결과·한계 필드 추가
- R7: 단일 변수 비교, 행동 관찰, 인터뷰와 실패 판정 기록 계약 추가

## 제품 상태

- 현재 단계: `TOTAL_PLANNING / CANON_CONFLICT_RESOLUTION`
- 제품 구현: `BLOCKED`
- Godot·Android·접근성·성능·사람 플레이 검증: 본 결정에 대해 `NOT_RUN`
