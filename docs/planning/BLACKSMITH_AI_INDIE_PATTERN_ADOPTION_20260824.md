# Blacksmith · AI Indie Pattern Adoption — 2026-08-24

```yaml
status: USER_DIRECTED_ADAPTATION
work_mode: PLAN
runtime_mutation: NONE
balance_mutation: NONE
source_base_merge: dff09d83c3892a70ba5fee86a59d36086889a6c5
current_core_owner: CURRENT_CONFIRMED_DECISIONS.md
current_balance_owner: docs/planning/BLACKSMITH_ENHANCEMENT_BALANCE_CURVE_CANON_20260820.md
human_playtest: NOT_RUN
```

## 1. 결론

Blacksmith는 새 `RNG recovery` 시스템을 추가할 필요가 없다. 현재 강화 정본은 이미 실패를 단순 꽝으로 처리하지 않고 `CURRENT damage / CRITICAL / MAX scar / DOWNGRADE / repair / recraft / per-UID recovery / hard guarantee / 작품 연대기`로 다음 판단에 연결한다.

따라서 이번 흡수의 핵심은 **새 메커니즘이 아니라 기존 강화 선택의 정보 품질과 실패 후 의사결정 가시성을 강화하는 것**이다.

## 2. 판정표

| Base pattern | 판정 | Blacksmith 적용 |
|---|---|---|
| HUMAN_DIRECTED_AI_BUILD_LOOP | ADOPT | AI 수치/콘텐츠 생성 뒤 simulation + 사람 판단 필수 |
| SILENT_OMISSION_GATE | ADOPT | enhancement/item UID/customer/result consumer 누락 검사 |
| CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET | ADOPT | enhancement, durability, economy, customer lifecycle owner 분리 |
| BREADTH_AFTER_CORE_IDENTITY_LOCK | ADOPT | 강화 긴장감 Human 검증 전 고객/아이템/촉매 breadth 과확장 금지 |
| PLAYER_FEEDBACK_REBUILD_LOOP | ADOPT | 강화가 긴장보다 피로/억울함이면 수치만이 아니라 정보·구조 재검토 |
| AI_VISIBLE_OUTPUT_QUALITY_GATE | ADOPT | 생성 시각물/아이콘도 작품 UID와 상태를 정확히 표현해야 함 |
| RNG_AGENCY_AND_RECOVERY | ADOPT_EXISTING | 현재 per-UID recovery/repair/recraft가 이미 구현할 설계 계약을 충족 |
| runtime generative AI | REJECT_CURRENT | 강화 판단에 불필요 |

## 3. 기존 Recovery 정본을 보존

현재 승인 테스트 Budget:

```text
RECOVERY_SUCCESS_BONUS_PER_FAILURE = +6%p
RECOVERY_SOFT_CAP = 95%
owner = ITEM_UID + TARGET_LEVEL
cross_item_transfer = FORBIDDEN
```

Band별 hard guarantee도 유지한다. 이 구조를 새 pity currency나 계정 공용 실패 보너스로 바꾸지 않는다.

Blacksmith의 핵심은 실패를 없애는 것이 아니라:

```text
이 작품을 여기서 멈출까?
→ 더 강화할까?
→ 손상을 수리할까?
→ MAX scar를 감수할까?
→ downgrade를 복구할까?
→ 파괴 위험을 감수할 가치가 있는가?
```

를 작품 UID의 생애와 함께 누적시키는 것이다.

## 4. 새 적용 계약 · STOP_DECISION_READABILITY_GATE

강화 버튼을 누르기 전에 플레이어가 최소 다음을 이해할 수 있어야 한다.

```text
현재 강화 → 목표 강화
현재 성공 기대
이번 시도 Gold/재료 비용
현재 실패 recovery 보너스
hard guarantee까지 남은 실패 수
일반 실패에서 가능한 CURRENT 손상
CRITICAL에서 가능한 CURRENT / MAX scar 위험
현재 CURRENT / MAX 내구도
이 작품에 이미 누적된 가치/연대기 중 위험에 노출되는 것
```

정확한 수치가 아직 provisional이면 provisional임을 표시하고 확정 수치처럼 꾸미지 않는다.

### 정보 제공 ≠ 정답 추천

UI는 다음을 말할 수 있다.

- 위험이 이전 단계보다 커졌다.
- 이번 실패는 recovery를 누적한다.
- 현재 MAX가 낮아 성공 기대가 감소했다.
- 수리 가능한 CURRENT 손상과 복구 불가능한 MAX scar는 다르다.

하지만 다음을 자동으로 말하지 않는다.

- “지금 강화가 최적입니다.”
- “여기서 판매하세요.”
- 고객/시장/Chronicle까지 합친 단일 최적 점수.

## 5. 실패 결과를 다음 선택으로 연결

```text
강화 실패
→ failure family와 실제 손상 표시
→ recovery progression 갱신
→ 작품 UID history 기록
→ repair / retry / stop / sell / customer-use 후보를 현재 정본 범위에서 비교
→ 다음 결정
```

파괴도 단순 save-reload 유도 실패가 아니라 작품 생애의 끝과 재제작 비용/기억으로 연결되어야 한다. 다만 Human evidence가 파괴를 의미 있는 긴장보다 반복 노동으로 느낀다면 severity/cost/supply를 먼저 재조정한다.

## 6. Player Feedback Rebuild

Human QA에서 다음을 분리한다.

```text
GOOD_TENSION
= 성공 가능성과 잃을 것을 이해하고 스스로 더 누름

BAD_OPACITY
= 무엇을 잃을지 몰라서 불안함

BAD_GRIND
= 결과는 이해하지만 회복을 위해 같은 행동을 과도하게 반복
```

조정 우선순위:

```text
정보/피드백
→ 비용/손상/재료 공급
→ recovery/hard-guarantee pacing
→ 성공률
→ 마지막에만 core 구조 재검토
```

극저확률로 긴장감을 만드는 과거 방향은 되살리지 않는다.

## 7. 다음 Codex 구현 후보

향후 승인된 제품 Task에서:

1. 강화 확인 화면의 위 정보 필드 coverage test.
2. failure result packet에 damage/recovery/guarantee/UID history가 함께 연결되는지 검사.
3. same-seed/Monte Carlo로 stop points, destruction, repair frequency 분포 측정.
4. UI는 static expected-value table과 actual player spend를 혼동하지 않도록 테스트.
5. Human play에서 “왜 멈췄는가/왜 한 번 더 눌렀는가”를 설명할 수 있는지 검증.

## 8. Implementation Reality Gate

현재 주장 가능:
- Base RNG recovery 패턴이 이미 존재하는 Blacksmith 설계와 중복됨을 확인하고 새 시스템 생성을 피함.
- 강화 선택 정보 Gate를 프로젝트용으로 정의함.

현재 주장 불가:
- 강화가 실제로 더 긴장감 있음.
- +0~+100 최종 제품 밸런스 확정.
- 파괴/repair pacing Human PASS.
- Android/device UX PASS.

## 9. 적대적 검토 5회

1. **중복 시스템** — 기존 recovery/hard guarantee 재사용, 새 pity 시스템 없음: PASS.
2. **긴장감 훼손** — recovery가 위험을 삭제하지 않고 decision support로만 작동: PASS.
3. **정답 UI** — 정보 제공과 최적 추천을 분리: PASS.
4. **경제 왜곡** — actual spend와 static market anchor를 혼동하지 않음: PASS.
5. **증거 과장** — simulation과 Human evidence를 분리: PASS.

`CLEAN_REVIEW_EXIT`.
