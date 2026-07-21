# Blacksmith Work Mode·Skill 라우팅

## 핵심

- `Work Mode`: 현재 단계의 권한·증거 기준
  - `PLAN`: 조사·설계·정본·순서
  - `BUILD`: 승인 범위 구현
  - `REVIEW`: 적대적 검토·반례·검증
- `Skill`: 반복 책임 계약
- `Skill Mode`: Skill 내부 절차

```text
Prompt
→ Work Mode 하나
→ Registry trigger·do_not_use_when
→ 주 Skill 최대 하나 + 필요한 영향 Skill
→ 실행·검증
→ 사용 이유·결과·미검증 보고
```

사용자가 Skill을 선택할 필요는 없다. `load_by_default=false`는 trigger가 없을 때 읽지 않는다는 뜻이다.

## 프로젝트 Skill 3개

| Skill | 책임 | Modes |
|---|---|---|
| `blacksmith-game-design` | 핵심 재미·제작·강화·경제·조사·플레이테스트·PoC·Vertical Slice·아트 방향 | `frame`, `update-system`, `balance-review`, `benchmark-and-player-research`, `playtest-and-experiment`, `poc-check`, `vertical-slice-gate`, `art-brief` |
| `blacksmith-engineering` | Godot·데이터·Android·저장·자동화 구현 | `plan-change`, `implement`, `data-migration`, `runtime-check` |
| `blacksmith-qa` | 계약·외부 결과·참조·정적·런타임·접근성·성능·UI·회귀 | `contract-check`, `external-source-review`, `reference-freshness`, `static`, `runtime`, `accessibility-review`, `performance-profile`, `ui-art-review`, `regression`, `evidence-report` |

Base의 13개 활성 기능은 `docs/BASE_ADOPTION_PROFILE.json`에서 이 3개 Skill과 프로젝트 운영 문서로 전부 매핑한다. Base Skill 패키지를 중복 복사하지 않는다.

## Foundation 절차

큰 요청은 한 번만 다음 순서로 처리한다.

```text
route
→ 저장소 사실 조사
→ 필요한 경우 사용자 확인
→ contract
→ L2 이상·다중 의존성이면 decompose-and-sequence
→ BUILD
→ REVIEW
→ execution-report
```

운영체계 변경은 `audit → 필요한 경우 reconcile-legacy → 승인된 migrate → verify` 순서다. 사용자 승인 전 대량 삭제·이동·통합을 하지 않는다.

외부 AI 대량 작업은 `external-ai-worktree`로 별도 브랜치·작업 공간에 격리하며, 결과는 `blacksmith-qa: external-source-review`를 통과하기 전 정본으로 사용하지 않는다.

## 권한 전환

- PLAN: 읽기·조사·제안. 승인 전 범위 밖 제품 변경 금지.
- BUILD: 승인 범위만 수정하고 단계별 테스트·롤백 유지.
- REVIEW: finding·심각도·증거 우선. 승인된 수정만 BUILD 후 재검증.

## 실행 보고

L1 이상 작업은 다음을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | NOT_RUN
```

실행하지 않은 Skill·테스트·Android·시각·접근성·성능·브랜치 보호는 사용 또는 통과로 보고하지 않는다.
