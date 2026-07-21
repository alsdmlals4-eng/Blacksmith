# Blacksmith Work Mode·Skill 라우팅

## 용어

- `Work Mode`: 현재 단계의 작업 자세·권한·증거 기준
  - `PLAN`: 조사·설계·정본·순서 확정
  - `BUILD`: 승인 범위 구현·갱신
  - `REVIEW`: 적대적 검토·반례·검증
- `Skill`: 반복 책임을 수행하는 프로젝트 전용 계약
- `Skill Mode`: Skill 내부의 세부 절차
- `Prompt`: 사용자의 현재 목표·제약·산출물

## 자동 선택 순서

```text
Prompt 의도·현재 단계·위험
→ 주 Work Mode 하나
→ SKILL_REGISTRY trigger·do_not_use_when 대조
→ 필요한 최소 프로젝트 Skill 자동 선택
→ 필요 시 Base Foundation Skill 기준 참조
→ 실행·검증
→ Work Mode·Skill·Skill Mode 사용 이유와 결과 보고
```

사용자가 Skill 이름을 선택할 필요가 없다. `load_by_default=false`는 자동 사용 금지가 아니라 trigger가 없을 때 읽지 않는다는 뜻이다.

## 프로젝트 Skill

| 주 책임 | Skill | 대표 Skill Mode |
|---|---|---|
| 제작·강화·수식어·고객·경제·PoC 방향 | `blacksmith-game-design` | `frame`, `update-system`, `balance-review`, `poc-check` |
| Godot·GDScript·Android·데이터·저장 구현 | `blacksmith-engineering` | `plan-change`, `implement`, `data-migration`, `runtime-check` |
| 계약·정적·런타임·회귀·Android 증거 | `blacksmith-qa` | `contract-check`, `static`, `runtime`, `regression`, `evidence-report` |

주 책임 분야 Skill은 최대 하나다. 복합 작업은 게임 디자인을 주 책임으로 두고 engineering·qa를 영향 분야로 실행하거나, 구현이 중심이면 engineering을 주 책임으로 둔다.

## Base Foundation 연결

다음 상황에서는 `docs/BASE_RULES_VERSION.md`에 고정된 Base 기준의 해당 계약을 선택적으로 적용한다.

- 새 요청·큰 범위·의존성 분해: `managing-project-intake-and-work-contract`
- 운영 구조 감사·마이그레이션·구형 정리: `managing-game-project-operating-system`
- 책임 문서·발행: `managing-design-documents`
- Active Context·Handoff: `maintaining-project-context-and-handoff`
- 정본·경로·ID·Schema 전파: `auditing-canonical-reference-freshness`
- 통합 변경 검증: `reviewing-and-validating-project-changes`

Base Skill을 프로젝트 폴더에 전부 복제하지 않는다.

## 권한 전환

```text
PLAN
- 읽기·조사·제안
- 사용자 승인 전 범위 밖 제품 변경 금지

BUILD
- 승인 범위만 수정
- 단계별 테스트·롤백 유지

REVIEW
- finding·심각도·증거 우선
- 수정이 승인된 범위면 BUILD로 전환
- 수정 뒤 REVIEW 재검증
```

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
status: PASS | PARTIAL | FAIL | UNVERIFIED
```

실행하지 않은 Skill·검사·Android 기기·접근성·성능·브랜치 보호는 사용 또는 통과로 보고하지 않는다.
