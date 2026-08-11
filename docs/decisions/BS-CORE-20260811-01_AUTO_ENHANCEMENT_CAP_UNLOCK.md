# BS-CORE-20260811-01 — Auto Enhancement Cap Unlock

- Decision ID: `BS-CORE-20260811-01`
- Title: `AUTO_ENHANCEMENT_CAP_UNLOCK`
- Date: `2026-08-11 KST`
- Status: `USER_APPROVED_DIRECTION / PLANNING_ONLY`
- Product implementation: `BLOCKED`
- Task3 implementation: `NOT_APPROVED`

## User-approved direction

중·후반으로 갈수록 과거 저강화 구간의 반복 가치는 낮아지므로, 플레이어가 목표 강화 수치를 지정해 자동 강화할 수 있게 하고 진행에 따라 자동 강화 최대치를 해금한다.

## Canonical interpretation

이 Decision은 기존 `저위험 연속 강화`를 폐기하지 않고 성장형 상한을 추가한다.

```text
BS-CORE-20260811-01
AUTO_ENHANCEMENT_CAP_UNLOCK
15 manual attempts → AUTO_CAP +20
+40 breakthrough complete → AUTO_CAP +30
+50 breakthrough complete → AUTO_CAP +40
+60 breakthrough complete → AUTO_CAP +50
AUTO_CAP = highest completed category breakthrough - 10
CATEGORY_SPECIFIC_AUTO_CAP
PLAYER_SELECTED_TARGET_REQUIRED
TARGET_ENHANCEMENT <= AUTO_CAP
```

초기 `+20`은 기존 승인된 early-game exception이다. 이후 상한은 해당 장비 분야에서 플레이어가 직접 완료한 기술 돌파보다 한 10강 밴드 뒤에서 따라간다.

## Preserved authorities

```text
BREAKTHROUGH_AUTHORITY: BLACKSMITH_GROWTH_SYSTEM_ADDENDUM_02
RISK_PROBABILITY_AUTHORITY: BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026
CONTINUOUS_ENHANCEMENT_AUTHORITY: BLACKSMITH_DECISION_LEDGER_ADDENDUM_07
```

이 문서는 새 성공률, 새 강화 결과표, 새 돌파 비용, 새 pity/보장 게이지를 소유하지 않는다.

## Automatic attempt contract

- 자동화는 정상 강화 시도를 순차 실행한다.
- 각 시도는 수동과 같은 확률·비용·재료·보호·작업 기회비용을 사용한다.
- 각 시도는 동일 UID에 독립 이력을 남긴다.
- 자동이라는 이유로 성공률 보너스·할인·무료 보호를 주지 않는다.
- `HIGH / VERY_HIGH` 위험, 정밀강화, 기술 돌파, 특수/영구 위험 선택은 수동 전용이다.
- 무보호 파괴 가능 시도는 자동으로 시작하지 않는다.
- 실제 단계 하락 또는 보호 파괴가 발생하면 그 시도 결과를 적용한 뒤 즉시 자동을 멈춘다.

```text
NO_HIDDEN_SUCCESS_RATE_BONUS
NO_RESOURCE_OR_FATIGUE_BYPASS
PER_ATTEMPT_UID_HISTORY_PRESERVED
NO_UNPROTECTED_AUTO_DESTRUCTION
AUTO_PRECISION_ENHANCEMENT: false
AUTO_TECHNICAL_BREAKTHROUGH: false
```

## Marek integration boundary

`BS-CONTENT-20260811-03 / SOLDIER_01 / MAREK_OLDEN`은 이미 해금된 자동 범위를 편의 기능으로 사용할 수 있지만 자동 상한의 해금·성장 권한을 소유하지 않는다. 여러 작품에 같은 목표를 지정해도 각 UID의 비용·판정·이력은 독립한다.

## Research judgment

- V4 official guide: `ADAPT` target-level automation and visible danger boundaries; `REJECT` industrial-scale identity loss.
- Uncharted Waters Origin July 2026 Director's Letter: `ADAPT` target-level auto-enhance as mature progression QoL.
- Black Desert Mobile Ancient Anvil: `ADAPT` friction-relief problem framing; `REJECT` a new pity/guaranteed-success economy.
- Google Play quality guidance: `ADOPT` intuitive, seamless UX that recognizes player progress.
- `DIFFERENTIATOR`: manual mastery first, automation one band behind, per-UID history preserved.

## Adversarial decision

- `MUST_FIX`: automatic cap never reaches or exceeds the currently manually proven category frontier.
- `MUST_FIX`: category ownership is preserved.
- `MUST_FIX`: no high/very-high auto, auto precision, auto breakthrough, unprotected auto destruction, or probability/resource bypass.
- `MUST_FIX`: batch convenience must not merge item identities.
- `REJECTED_IMPORT`: no Ancient Anvil/pity gauge is introduced.

## Authority links

- Detailed canon: `docs/planning/BLACKSMITH_AUTO_ENHANCEMENT_CAP_UNLOCK_CANON_2026.md`
- Design spec: `docs/superpowers/specs/2026-08-11-auto-enhancement-cap-unlock-design.md`
- Planning implementation plan: `docs/superpowers/plans/2026-08-11-auto-enhancement-cap-unlock.md`

This Decision does **not** increment the R3–R7 content approval counter. The content counter is advanced to `3/10` by `BS-CONTENT-20260811-03`, not by this core/system refinement.
