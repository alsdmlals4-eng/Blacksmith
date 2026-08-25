# Blacksmith Visual GDD Brief Approval · 2026-08-25

- Status: `USER_APPROVED_CURRENT_VISUAL_BRIEF_GATE`
- User directive: `승인 진행해`
- Work mode: `PLAN`
- Blacksmith baseline main: `d2857047b6aac6dfcdee353e62bf7fc6865055d4`
- Base main fresh-read: `3c3376845b9a1b7921a4260aa6259cd61533ffc4`
- Current style: `STYLIZED_DARK_FORGE = CURRENT`
- Example images: `REFERENCE_ONLY_LAYOUT_DENSITY`
- `IMAGE_GENERATION = NOT_RUN`
- `PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`

## Scope

사용자가 직전 Living GDD 정리에서 다음 단계로 제시된 6개 Blacksmith 전용 Visual GDD 브리프의 승인을 명시했다. 이 승인은 **브리프가 이미지 생성 단계로 넘어갈 수 있다는 승인**이며, 이미지 자체·최종 제품 자산·런타임 화면의 승인이 아니다.

승인된 6개 Decision ID는 기존 ID를 유지한다.

| Decision ID | Visual GDD | 승인 상태 |
| --- | --- | --- |
| `BS-VIS-20260820-01` | 강화 메인 화면 | `USER_APPROVED_FOR_GENERATION` |
| `BS-VIS-20260820-02` | 강화 DDD Feedback Ladder | `USER_APPROVED_FOR_GENERATION` |
| `BS-VIS-20260820-05` | 첫 10분 DDD Storyboard | `USER_APPROVED_FOR_GENERATION` |
| `BS-VIS-20260820-06` | CURRENT/MAX 이중 내구도 상태 | `USER_APPROVED_FOR_GENERATION` |
| `BS-VIS-20260820-09` | 수리 판단 카드 | `USER_APPROVED_FOR_GENERATION` |
| `BS-VIS-20260824-10` | 정밀강화 → 고객 Context 판단 카드 | `USER_APPROVED_FOR_GENERATION` |

## Shared generation guard

모든 6개 브리프는 다음 공통 시각 기준을 소비한다.

- `BS-ART-20260731-01 / STYLIZED_DARK_FORGE`를 바꾸지 않는다.
- 장비·작품과 판단 정보가 시각적 주인공이다.
- 어두운 forge 물성 + 따뜻한 국소 화로광 + iron/brass UI 언어를 유지한다.
- 모바일 세로 판독성을 장식 밀도보다 우선한다.
- 확률·위험·등급·구조 상태를 색상 하나로만 전달하지 않는다.
- 사용자가 제공한 예시 이미지는 레이아웃·정보 밀도 참고이며 Blacksmith asset으로 직접 사용하지 않는다.
- 실제 생성 결과는 별도 review/approval을 통과하기 전 `APPROVED_REPRESENTATIVE_VISUAL`이나 production asset이 아니다.

## Per-brief contract

### `BS-VIS-20260820-01` · 강화 메인 화면

**Approval:** `USER_APPROVED_FOR_GENERATION`

2~3초 안에 `현재 강화 상태 / 성공 기대 / 시도 비용 / 실패 위험 / STOP 또는 PUSH`가 읽혀야 한다. 일반 강화·첫 위험 강화·실패 유지·실패 손상·성공·이정표 진입 상태를 검토 가능해야 한다.

### `BS-VIS-20260820-02` · 강화 DDD Feedback Ladder

**Approval:** `USER_APPROVED_FOR_GENERATION`

안전 강화와 고위험 강화의 anticipation·impact·result feedback scale 차이를 설명하는 storyboard/system diagram을 만든다. 모든 단계에 같은 대형 연출을 적용하지 않는다.

### `BS-VIS-20260820-05` · 첫 10분 DDD Storyboard

**Approval:** `USER_APPROVED_FOR_GENERATION`

`New Game → 짧은 첫 작품 → +1/+2 LEARN → +3~+9 BUILD → +10 정밀강화/checkpoint → +11 위험 Preview → STOP/PUSH → 실제 결과 → NADIA_VENN 작품 인계 → 지연 결과 → 같은 UID 다음 행동` 흐름을 시각화한다. scripted failure·hidden success boost·강제 +11은 금지한다.

### `BS-VIS-20260820-06` · CURRENT/MAX 이중 내구도 상태

**Approval:** `USER_APPROVED_FOR_GENERATION`

`CURRENT NN% / MAX MM%`를 동시에 읽게 하고, `STABLE / STRESSED / DAMAGED / FRACTURED / CRITICAL / DESTROYED` 구조 상태를 비색상 신호와 함께 표현한다. 수리가 MAX 자체를 복구한다고 오해시키지 않는다.

### `BS-VIS-20260820-09` · 수리 판단 카드

**Approval:** `USER_APPROVED_FOR_GENERATION`

`CURRENT → MAX / MAX 유지 / 필수 골드 / 필수 일반 구조재료 / 공방 부담 2 / 수리하지 않고 계속 강화`를 2~3초 안에 비교할 수 있어야 한다. 부분수리·자동수리 기본 ON·MAX 완전복구 암시는 금지한다.

### `BS-VIS-20260824-10` · 정밀강화 → 고객 Context 판단 카드

**Approval:** `USER_APPROVED_FOR_GENERATION`

Nadia context에서 `직접 도움 / Gate 변화 / trade-off / 직접 관련 없음`을 종합점수 없이 읽게 한다. `Best`, 0~100 적합도, 정확 레시피 정답 강조, 촉매 자체의 고객 보너스, 미래 탐사 결과 스포일러는 금지한다.

## Explicitly not approved

다음은 이번 사용자 승인으로 열리지 않는다.

- 실제 이미지 생성 실행
- 생성 이미지의 최종 승인
- Asset Library의 `Approved=true`
- 제품 UI/Scene/Resource 구현
- Android/device/accessibility/Human validation PASS
- balance 수치의 최종 제품값 확정
- `BS-VIS-20260820-03`, `04`, `07`, `08` 또는 기타 Visual brief의 자동 승인

따라서 현재 상태는 다음과 같다.

```text
VISUAL_STYLE = STYLIZED_DARK_FORGE_CURRENT
SELECTED_VISUAL_BRIEFS = USER_APPROVED_FOR_GENERATION
APPROVED_REPRESENTATIVE_VISUAL = NOT_AVAILABLE
IMAGE_GENERATION = NOT_RUN
FINAL_ASSET_APPROVAL = NOT_RUN
PRODUCT_IMPLEMENTATION = BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION
```

## Pre-work research disposition

이번 작업은 기존 디자인의 신규 비교·변경이 아니라 사용자가 직전에 확인한 **기존 6개 브리프의 approval gate만 변경**하는 좁은 상태 전환이다. 따라서 새로운 외부 benchmark 수치나 사례를 유입하지 않는다.

- `ADOPT`: 현재 6개 brief와 `STYLIZED_DARK_FORGE`를 그대로 승인 단계로 전진
- `ADAPT`: 없음
- `REJECT`: 예시 이미지를 승인 asset으로 승격, brief approval을 final asset approval로 해석, 제품 구현 Gate 자동 개방
- `DIFFERENTIATOR`: 강화 STOP/PUSH와 같은 UID 생애 인과가 시각 판단의 중심이라는 기존 Blacksmith 차별점을 유지
- `BENCHMARK_NOT_APPLICABLE`: design delta 없음 / approval-state-only change

## Destination contract

- GitHub: 이 문서가 approval gate의 repository canon이다.
- Notion Visual Bible: 동일 6개 Decision ID의 상태를 `USER_APPROVED_FOR_GENERATION`으로 갱신한다.
- Google Sheet: migration compatibility/same-ID mirror로 동일 6개 Decision ID를 기록한다.
- Asset Library approved gallery는 실제 이미지 review가 완료될 때까지 0건이어도 정상이다.
