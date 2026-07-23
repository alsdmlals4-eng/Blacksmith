---
name: blacksmith-game-design
description: Blacksmith의 제작·강화·경제·벤치마크·플레이테스트·PoC·Vertical Slice를 하나의 게임 디자인 책임으로 다룬다.
---

# Blacksmith Game Design

## Modes

- `frame`: 핵심 행동·감정·제약·결정 질문을 고정한다.
- `update-system`: 승인된 제작·강화·판매 규칙을 정본과 데이터 계약에 반영한다.
- `balance-review`: 성장·성공률·위험·가격·재료 선택과 악용 가능성을 검토한다.
- `balance-simulation`: 강화·제작·판매의 확률·비용·재료·파괴·복원 곡선을 재현 가능한 가설과 시뮬레이션으로 검증한다.
- `benchmark-and-player-research`: 제품 사실·플레이어 반응·행동 근거를 분리하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정한다.
- `playtest-and-experiment`: 빌드·대상·과제·행동 이벤트·성공 기준을 고정한다.
- `poc-check`: 가장 위험한 가설과 최소 검증·중단 기준을 정한다.
- `vertical-slice-gate`: 대표 플레이 구간의 목표 품질·접근성·성능·제작 파이프라인·실제 플레이 증거를 판정한다.
- `art-brief`: 승인된 아트 방향을 생성·편집 프롬프트와 기술 제약으로 변환한다.

## Read

`ACTIVE_CONTEXT.md` → `BLACKSMITH_GAME_BIBLE.md` → 관련 MVP Scope 또는 `docs/BALANCE_SIMULATION_SCOPE.md` → 관련 JSON → 실제 구현·테스트.

## Rules

- 광클→즉시 피드백→피버→성장 선택이 핵심이다.
- Base의 `DDD`는 `Digital Dopamine Design`이다. 첫 의미 있는 보상, 피드백 지연, Micro→Session→Meta 보상, 다음 행동, 피로·인플레이션을 검토한다.
- 일반 강화와 +10 단위 특수 강화를 분리한다.
- 보조재료·촉매·정밀 강화는 특수 강화에서만 적용한다.
- 고단계 보상은 위험·비용·복구 선택과 함께 증가시킨다.
- 직원·무기 수리는 승인 없이 추가하지 않는다.
- 수치의 정본은 JSON, 구현 사실은 Script·Scene·Test다.
- 벤치마크와 리뷰는 요구사항 정본이 아니라 개선 가설의 근거다.
- 승인 이미지가 있으면 임의로 교체하지 않는다.

## Balance simulation

- 먼저 결정 질문을 하나로 고정한다. 예: 특정 목표 강화까지의 기대 비용, 파괴 뒤 회복 가능성, 피버 보상이 정상 제작 선택을 압도하는지, 판매 보상이 재료·골드 순환을 무너뜨리는지.
- JSON 정본, 코드의 실제 판정 순서, 초기 자원, 반복 정책, 중지 조건을 입력으로 기록한다. 문서 수치나 임시 화면 문구를 입력값으로 쓰지 않는다.
- 평균만 보고 결론내리지 않는다. 중앙값, 하위·상위 분위, 실패·하락·파괴 빈도, 재료 병목, 보관함·자동 중지, 선택별 분산을 함께 본다.
- 성공률·비용·보정·피버·판매가를 한 실험에서 동시에 바꾸지 않는다. 변경 전 가설·가드레일·중단 조건을 선언한다.
- 결과는 `KEEP / TUNE / REJECT / TEST_IN_PLAY`로 판정하고, 실제 플레이 체감이 필요한 결론은 시뮬레이션 PASS로 확정하지 않는다.
- 범위·입력·지표·산출물·완료 기준은 `docs/BALANCE_SIMULATION_SCOPE.md`를 따른다.

## Output

- 유지·변경·제외 범위
- 책임 원본과 데이터 필드
- 정상·실패·경계 플레이 결과
- 검증 가능한 가설·지표·게이트
- 시뮬레이션 입력 스냅샷·시드·분포·판정
- 미확정과 다음 결정

## Failure

- 부가 시스템이 광클 핵심 경험을 가린다.
- 특수 강화 경계나 재료 효과가 일반 강화로 누출된다.
- 외부 인기 기능을 검증 없이 복사한다.
- 평균만 보고 고위험 곡선을 확정한다.
- 여러 실험 변수를 동시에 바꾸거나 결과 후 성공 기준을 바꾼다.
- 실제 플레이 증거 없이 Production·Vertical Slice 통과를 선언한다.

## Learning

실패·중요 결정·반복 가능한 교훈·실제 플레이 증거만 `skills/SKILL_LEARNING_LOG.md`에 기록한다.
