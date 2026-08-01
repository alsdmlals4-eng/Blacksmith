# Blacksmith 기존 프로젝트 감사 보완 — 자동 강화 경계

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A7`
>
> Decision ID: `BS-AUTOFORGE-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 기존 충돌

구형 `game_flow_screen.gd` 자동 단조는 다음을 수행한다.

- 보관함이 찰 때까지 반복
- 정밀 게이지 위치를 `rng.randf()`로 자동 지정
- `allow_empty_secondary=true`로 필수 재료 없이 진행
- 파괴 뒤 새 철검 template을 만들어 재시작
- 목표 단계까지 정체성·+50 경계 없이 반복

이는 최신 작품 완성·계보·보조·정밀·+50 경로·비가역 결과 선택과 충돌한다.

## 2. 해결된 기획 목표

`BS-AUTOFORGE-20260801-01`로 다음을 확정했다.

- 제품 명칭 `자동 강화`
- 한 기존 장비의 비결정 일반 강화만 반복
- +5/+10/+20/+30/+40/+50과 data-driven 선택 경계에서 필수 정지
- 정밀 입력 자동화·난수 위치 지정 금지
- 필수재료 빈 fallback과 최적 재료 자동 선택 금지
- 파괴 뒤 장비 자동 생성·재시작 금지
- 최대 시도와 지출/잔액 제한 필수
- 매 시도 AttemptIntent·ResultEnvelope·원자 저장 사용
- 실제 정지 이유와 다음 행동 표시

## 3. Finding 판정

| Finding | 기획 목표 | 런타임·테스트 |
|---|---|---|
| `BS-AUD-F06` | RESOLVED | OPEN |

P0 Finding 수는 제품 코드와 테스트가 변경되기 전까지 유지한다.

## 4. 적대적 실패 조건

```text
precision_position = rng.randf()
allow_empty_secondary = true
repeat_until_full
파괴 후 새 장비 자동 생성
계보·보조·+50 경계 자동 통과
판매·고객 인계 자동 수행
모든 시도·지출 제한 무제한
저장 실패 뒤 다음 시도 실행
결과 오류 뒤 RNG 재호출
```

## 5. 상태

```text
AUTO_ENHANCE_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
PRODUCT_CODE_UI: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
