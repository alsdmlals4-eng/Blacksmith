# Blacksmith

Android 모바일과 Google Play 출시를 목표로 하는 Godot 대장장이 게임 프로젝트입니다.

> **장비를 대량 생산하는 게임이 아니라, 장비의 출생·성장·소유·사건 기록을 제작하는 대장장이 게임.**

플레이어는 한 명의 대장장이로서 장비 한 점을 직접 만들고, 강화 버튼을 누를 때마다 멈출지 더 도전할지 판단합니다. `+10` 이정표에서 수식어와 성장 방향을 선택하며, 판매·납품한 장비는 세계에서 이력을 쌓아 명성과 다음 의뢰로 돌아옵니다.

## 현재 구현

### 기존 Prototype

```text
철검 제작
→ 광클·자동 작업·피버
→ 제작 정밀 마감
→ +100 일반/특수 강화
→ 단계 하락·파괴·실패 보정
→ 보관함
→ 자동 단조
```

- Godot 4.7.1 / GDScript
- 일반 강화 버튼 입력당 판정 1회
- `+10` 단위 특수 강화와 수식어 성장
- `+11` 단계 하락, `+30` 파괴 가능
- 균형·안정·폭주 단조
- 골드·재료 원자 거래
- 최대 6개 보관함과 자동 단조
- Godot AI 벤더 플러그인 진입점과 파싱 계약 유지

실패·보정·위험 수치의 단일 책임 원본은 `data/crafting/enhancement_balance.json`이며, `data/crafting/enhancement_milestones.json`은 +10 단위 특수 강화와 수식어 이정표를 책임집니다.

### 장비 한 점의 생애 PoC

```text
검투사 의뢰
→ 철검 제작과 영구 완성도
→ +5 납품 또는 +10 추가 도전
→ 수동 하루 종료
→ 지연된 경기 결과
→ 장비 이력·명성·관계
→ 같은 검투사의 재방문
```

구현·자동 검증 완료 범위:

- 피로도 20과 작업별 비용
- 수동 날짜 진행과 잔여 피로도 50% 이월
- 영구 완성도 5등급과 legacy 제작 품질 변환
- 검투사 계약, 납품 적합도와 세 결과 밴드
- 영구 세계 장비 기록과 결정적 경기 결과
- 제작·강화·납품 원자 거래
- 지연 보고, 명성·관계와 같은 고객 재방문
- 로컬 행동 telemetry
- 별도 세로 PoC Scene과 기존 Prototype 진입 버튼
- 정밀 보조 GOOD 경로와 모션 감소
- 전체 생애 E2E·경계 테스트

현재 상태는 `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`입니다. 코드 기준 head `03c90bb063103e1c92885e7e21228f963cfe2775`의 PR validation #468에서 Ubuntu Python 전체 계약, Godot import, `main.tscn`·PoC Scene smoke, 기존·신규 모델·통합·E2E가 통과했습니다. Android 실기기, 사람 접근성 검토, 성능과 외부 플레이테스트는 `NOT_RUN`입니다.

## 현행 작업

- Issue: #34 `MVP-003: 장비 한 점의 생애 PoC 구현 및 플레이 검증`
- PR: #35
- Core: `docs/superpowers/specs/2026-07-23-project-core-design.md`
- Integrated spec: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- MVP Scope: `docs/MVP-003_SCOPE.md`
- Implementation plan: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- Implementation status: `docs/MVP-003_IMPLEMENTATION_STATUS.md`
- CI policy: `docs/CI_EXECUTION_POLICY.md`

## 실행

1. GitHub Desktop에서 **Fetch origin → Pull origin**
2. Godot 4.7.1에서 `project.godot`을 열고 **F5**
3. 기존 화면 왼쪽 위의 **장비 생애 PoC** 버튼으로 PoC Scene에 진입

상세 안내: `docs/GODOT_PLAYTEST.md`

## 프로젝트 운영 시작 위치

1. `AGENTS.md`
2. `[기획서]/00_프로젝트_허브/START_HERE.md`
3. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
4. `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
5. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
6. `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
7. `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`

## 기술 기준

- Engine: Godot 4.7.1 stable
- Language: GDScript
- Primary platform: Android mobile
- Distribution: Google Play
- Orientation: Portrait 720×1280
- Package: Android App Bundle (`.aab`)
- Target preparation: Android 16 / API 36+

## 검증

GitHub Actions 자동 실행은 활성화돼 있습니다. 문서 전용 변경은 Ubuntu Python 문서 검사만, 코드 변경은 Ubuntu Python 전체 계약과 Godot 1회를 실행합니다. `main`/nightly는 Ubuntu·Windows Python 매트릭스, Godot, pinned Base 전체 회귀를 실행합니다.

```bash
python -m unittest tests/test_ci_workflow_structure.py
python tests/check_no_merge_conflicts.py .
python tools/validate_game_data.py
python tools/validate_lifecycle_data.py
python -m unittest tests/test_lifecycle_data_contract.py
python tests/check_enhancement_failure_contract.py
python tests/check_project_core_alignment.py
```

Android·접근성·성능·외부 플레이를 실행하지 않았다면 PASS로 표시하지 않습니다.
