from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "[기획서]" / "00_프로젝트_허브"
REGISTRY_PATH = ROOT / "docs" / "planning" / "CURRENT_R2_CANON_REGISTRY.json"

CLOSURE_HEAD = "51d4acf4fc31233b4b218a6f20589fdbf2557ee2"
CLOSURE_MERGE = "06f03323c1309d8da0e6f5b9f4680a20ce388126"
CURRENT_MAIN_AT_AUDIT = "e525b7ca5df0d40a4dd7411789b8a36228063e84"

ACTIVE_CONTEXT = """# [현재 정본] Active Context

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / MERGED_PR109_MAIN_CANON / CLOSURE_PR117_MERGED_MAIN_CANON`
>
> `R2_BATCH_006_NOT_STARTED_0_OF_10`

- 갱신: `2026-08-06 18:30 KST`
- Work Mode: `TOTAL_PLANNING`
- 현재 단계: `R2_CORE_SESSION_META_LOOP / R2_CHECKPOINT_005_CLOSED_MAIN_CANON`
- 제품 구현: `BLOCKED`
- 사람 플레이테스트: `NOT_RUN`

```yaml
R2_CHECKPOINT_005: CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: NOT_STARTED_0_OF_10
PRODUCT_IMPLEMENTATION: BLOCKED
HUMAN_PLAYTEST: NOT_RUN
```

## 현재 권위

1. `CURRENT_CONFIRMED_DECISIONS.md`
2. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
4. 이 문서와 `ROADMAP.md`, `DEVELOPMENT_GATES.md`

PR #109는 Batch 005 기획 정본, PR #117은 체크포인트 폐쇄 정본, PR #118은 BCA 워크플로 복구로 병합됐다.

## 현재 게임 코어

```text
직접 단조
→ 제작 등급·예술성·역할 수치 확정
→ 일반 강화 지속·중단 판단
→ 정밀강화 방식·촉매 선택
→ 고객·일정에 작품 전달
→ 같은 UID의 결과·연대기·손상·복원
→ 다음 제작 판단
```

## 현재 승인 계약

### 작품·제작

- 제작 등급: `[보통] → [우수] → [명품] → [걸작] → [전설]`
- 최초 직접 단조 완료 시 확정하고 동일 UID에서 고정한다.
- 예술성은 `0` 이상의 정수이며 고정 설계 최대치가 없다.
- 수식어 슬롯은 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 개다.
- 보조재료 슬롯은 없다.
- 주재료는 장비군별 명시적 역할 적합성을 가진다.
- 직접 단조 결과는 역할별 3구간 판정으로 결정한다.
- 최초 역할 수치 프리셋은 `5 / 10 / 15`다.
- 작품 기본 중량은 장비군별 `0 / 5 / 10 / 15 / 20 / 30 WEIGHT_POINT`다.
- 기능 레시피는 역할·주재료·중량·상황·기능 용량을 함께 사용한다.

### 강화

- 일반 강화는 한 입력에 한 결과만 낸다.
- 일반 강화가 역할 원수치나 예술성을 자동 증가시키지 않는다.
- 정밀강화 이정표는 `+10 / +20 / +30 / +40 / +50`이다.
- 정밀강화 수치 패키지와 기능 재작업은 같은 이정표에서 상호배타다.
- 촉매 계보는 `EMPTY → SEED → DEVELOPED → EVOLVED → MASTERED`다.

### 고객·일정·UX

- 고객 능력은 근력·기량·체력·판단력 `1~10`이다.
- 최대 중량은 `STRENGTH × 10 WEIGHT_POINT`; 초과 장비는 배정 불가다.
- 성공률의 주효과는 강화 단계이며 고객 능력·적성은 작은 보조 보정이다.
- 고객 카드는 기본 → 장비 선택 후 판단 → 상세 보기의 3단계 공개를 사용한다.
- 핵심 원인 2~4개를 설명하고 48dp·비색상 단독 신호 금지를 지킨다.
- 고객 개인 일정과 날짜 예고형 세계 일정을 분리한다.
- 작품 결과는 고객 결과, UID 상태·연대기, 다음 제작·복원 판단으로 환류한다.

## 현재 구현 현실

현재 Godot 코드는 `POC v0.6.4` 역사 구현이다. 실행·테스트 기반은 보존하지만 다음 요소는 현재 정본 구현으로 간주하지 않는다.

- `STANDARD / GOOD / PERFECT` 구형 품질
- 보조재료 입력
- 범용 `affixes` 배열
- 고정 3일 계약 중심 고객 판정
- 현재 기획과 다른 정확한 확률·배율

따라서 기존 POC를 그대로 확장하지 않고, 최신 정본을 소비하는 별도 버티컬 슬라이스 경로를 설계해야 한다.

## 다음 작업

1. Godot 버티컬 슬라이스 범위 승인
2. Batch 006에서 데모용 데이터 Schema·UID·저장 경계를 확정
3. 대표 콘텐츠 한 경로의 테스트 프리셋 작성
4. 별도 승인 후에만 제품 경로 구현
5. 내부 구조 테스트 후 외부 3~5명 사람 플레이테스트

과거 배치 진행 카운터와 PR 대기 문구는 역사 문서에서만 조회한다.
"""

ROADMAP = """# [현재 정본] Blacksmith Roadmap

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / R2_BATCH_006_NOT_STARTED_0_OF_10`

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
CURRENT_STAGE_STATUS: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: NOT_STARTED_0_OF_10
PRODUCT_IMPLEMENTATION: BLOCKED
HUMAN_PLAYTEST: NOT_RUN
```

## R0–R2 — 완료된 기획 기반

- 프로젝트 코어와 권위 체계
- 직접 단조·제작 등급 5단계·예술성
- 등급·촉매·연대기 3수식어
- 일반 강화와 다섯 정밀강화 이정표
- 작품 역할·중량·기능 용량·재작업 레시피
- 고객 능력·장비 적합·모바일 정보 계층
- 개인 일정·세계 일정 분리와 작품 생애 환류

상태: `R2_CHECKPOINT_005_CLOSED_MAIN_CANON`.

## R2 Batch 006 — 다음 기획 배치

최대 10개 Decision으로 다음 순서를 권장한다.

1. 버티컬 슬라이스 대표 콘텐츠와 완료 조건
2. 작품 UID Schema·변동 장부·세이브 최소 계약
3. 제작 등급 5단계 데모 확률 프리셋
4. 예술성·역할 수치·중량 초기 프리셋
5. 일반 강화 데모 구간과 정밀강화 `+10` 대표 이정표
6. 촉매 씨앗·진화 대표 한 계보
7. 고객 3종과 설명 가능한 적합도 결과
8. 개인 일정 1개·세계 일정 1개
9. 손상·복원·연대기 대표 사건
10. 내부 테스트·사람 플레이테스트 프로토콜

정확한 값은 `BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED`로 유지한다.

## R3 — 버티컬 슬라이스 기반

- 최신 정본 전용 데이터 Schema
- 작품 UID와 저장·로드
- 단일 앱 셸과 화면 전환
- 대표 제작·강화·고객·일정·연대기 경로
- 원인 설명 로그와 로컬 검증 데이터

기존 POC의 구형 품질·보조재료·범용 수식어 구조는 재사용하지 않는다.

## R4 — 콘텐츠와 경제

- 장비군·주재료·기능·고객 확장
- 판매·증여·복원·상속 소유권 상태
- 가격·예술성·수요 점감
- 피로도·장기 성장·세계 일정

## R5–R6 — 모바일 제품화

- Android 세로형 UX
- 접근성·성능·저사양 검증
- 아트·오디오·피드백
- 세이브 migration과 복구

## R7 — 첫 코어 버티컬 슬라이스

```text
대표 작품 한 점 직접 단조
→ 제작 등급·예술성·역할·중량 확인
→ 일반 강화 지속·중단
→ 대표 정밀강화와 촉매 계보
→ 고객에게 배정하고 성공률·핵심 원인 확인
→ 결과·연대기·손상 또는 복원
→ 같은 UID로 재방문
→ 다음 제작 판단
```

필수 행동 증거:

- 플레이어가 강화 지속·중단을 고민한다.
- 등급·예술성·촉매·연대기의 원인을 구분한다.
- 고객 결과와 작품 선택의 인과를 설명한다.
- 같은 작품의 변화와 다음 행동을 기억한다.

## R8 — 적대적 최종 검토

- 핵심 재미와 모바일 복잡도
- 현재 정본·구형 문서·PR·데이터 충돌
- 저장·migration·접근성·성능
- 내부 테스트와 외부 사람 플레이테스트

## 구현 Gate

현재 상태:

```yaml
PRODUCT_IMPLEMENTATION: BLOCKED
HUMAN_PLAYTEST: NOT_RUN
VERTICAL_SLICE_PLAN: CONDITIONALLY_FEASIBLE
VERTICAL_SLICE_CODE: USER_APPROVAL_REQUIRED
```
"""

DEVELOPMENT_GATES = """# [현재 정본] Development Gates

<!-- R2_CHECKPOINT_005_CURRENT_AUTHORITY -->
> **R2_CHECKPOINT_005_CLOSED_MAIN_CANON**
>
> `R2_BATCH_005_CLOSED_10_OF_10 / R2_BATCH_006_NOT_STARTED_0_OF_10`

## Current Gate Summary

```yaml
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_STATUS: R2_CHECKPOINT_005_CLOSED_MAIN_CANON
R2_BATCH_005: CLOSED_10_OF_10
R2_BATCH_006: NOT_STARTED_0_OF_10
TDD_GATE: RED_GREEN_REFACTOR_REQUIRED
CODEX_IMPLEMENTATION_GATE: BLOCKED
VERTICAL_SLICE_PLAN_GATE: CONDITIONALLY_FEASIBLE
VERTICAL_SLICE_CODE_GATE: USER_APPROVAL_REQUIRED
LATEST_RUNTIME_VALIDATION_GATE: HISTORICAL_POC_ONLY
ANDROID_DEVICE_GATE: NOT_RUN
ACCESSIBILITY_GATE: NOT_RUN
PERFORMANCE_GATE: NOT_RUN
HUMAN_PLAYTEST: NOT_RUN
PRODUCT_IMPLEMENTATION: BLOCKED
```

## Canon Gate

버티컬 슬라이스를 포함한 모든 새 구현은 다음을 동시에 지켜야 한다.

- 제작 등급 5단계와 동일 UID 고정
- 예술성 비음수 정수·고정 설계 최대치 없음
- `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX`
- 보조재료 슬롯 없음
- 일반 강화 한 입력 한 결과
- 정밀강화 `+10/+20/+30/+40/+50`
- 장비군별 주재료·역할·기본 중량
- 역할 수치 프리셋 `5/10/15`
- 기능 용량과 명시적 재작업 레시피
- 고객 최대 중량 `STRENGTH × 10`
- 모바일 3단계 정보 공개와 설명 가능한 핵심 원인
- 개인 일정·세계 일정 분리
- 작품 UID 변동 장부와 연대기

판정: `REQUIRED`.

## Historical POC Gate

현재 Godot 프로젝트는 실행·파싱·씬 스모크·모델·통합 테스트가 통과하는 역사 POC다. 다음은 새 정본 구현으로 승격하지 않는다.

- 구형 `STANDARD / GOOD / PERFECT` 품질
- 보조재료 입력과 관련 재고
- 범용 수식어 배열
- 고정 계약 일수 중심 고객 평가
- 과거 정확한 확률·공격 배율·경제 수치

판정: `REFERENCE_ONLY / REUSE_BY_PORT_NOT_BY_AUTHORITY`.

## Vertical Slice Readiness Gate

판정: `CONDITIONALLY_FEASIBLE`.

필수 선행 조건:

1. 대표 콘텐츠 경로를 전체 콘텐츠와 구분한다.
2. 최신 정본 전용 Item UID·Save Schema를 확정한다.
3. 정확한 수치를 테스트 프리셋으로 격리한다.
4. 기존 POC 구형 모델을 새 Schema에 직접 혼합하지 않는다.
5. 앱 시작 씬을 테스트 씬과 분리한다.
6. 자동 검증과 사람 플레이테스트 결과를 별도로 기록한다.

제품 코드를 시작하려면 사용자의 별도 구현 승인이 필요하다.

## TDD Gate

모든 변경은 다음 순서를 따른다.

```text
RED → GREEN → REFACTOR → exact-head CI → review readback
```

현재 정본 폐쇄 보강 작업의 RED는 PR #119에서 관측한다.

## Save·UID Gate

버티컬 슬라이스 최소 저장 항목:

- 고유 작품 UID
- 주재료·장비군·역할 프로필
- 제작 등급·예술성·역할 원수치·중량
- 세 수식어 슬롯
- 강화 단계·정밀강화 사용 이정표
- 기능과 기능 용량
- 손상·복원·소유권·고객 결과
- 모든 변동 원인 장부

저장·로드 재추첨은 금지한다.

판정: `DESIGN_REQUIRED_BEFORE_CODE`.

## Human Playtest Gate

필수 검증:

- 강화 지속·중단 고민
- 등급·예술성·촉매·연대기 구분
- 고객 결과의 원인 설명
- 모바일 정보 과부하 여부
- 같은 UID에 대한 애착과 다음 행동

판정: `NOT_RUN`.

## Product Implementation Gate

R2 Batch 006의 버티컬 슬라이스 범위·Schema·테스트 프리셋과 사용자 구현 승인이 있기 전까지 `BLOCKED`다.
"""


def _write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _update_registry() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["stage_status"] = "R2_CHECKPOINT_005_CLOSED_MAIN_CANON"
    registry["next_approval_counter"] = "0/10"
    registry["product_implementation"] = "BLOCKED"
    registry["human_playtest"] = "NOT_RUN"
    registry["closed_batch"] = {
        "id": "R2_BATCH_005",
        "status": "CLOSED_MERGED_MAIN_CANON",
        "approved_count": 10,
        "maximum_count": 10,
    }
    registry["active_batch"] = {
        "id": "R2_BATCH_006",
        "status": "NOT_STARTED",
        "approved_count": 0,
        "maximum_count": 10,
    }
    checkpoint = registry["immutable_merge_evidence"]["checkpoint_005"]
    checkpoint["closure_exact_head"] = CLOSURE_HEAD
    checkpoint["closure_merge_sha"] = CLOSURE_MERGE
    checkpoint["closure_status"] = "MERGED_MAIN_CANON"
    checkpoint["closure_github_readback"] = "PASS"
    checkpoint["closure_sheet_readback"] = "PASS"
    checkpoint["current_main_at_finalization_audit"] = CURRENT_MAIN_AT_AUDIT
    registry.setdefault("validation_boundaries", {})["human_playtest"] = "NOT_RUN"
    REGISTRY_PATH.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    _write(HUB / "ACTIVE_CONTEXT.md", ACTIVE_CONTEXT)
    _write(HUB / "ROADMAP.md", ROADMAP)
    _write(HUB / "DEVELOPMENT_GATES.md", DEVELOPMENT_GATES)
    _update_registry()


if __name__ == "__main__":
    main()
