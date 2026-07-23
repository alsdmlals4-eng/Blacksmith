# Blacksmith

Android 모바일과 Google Play 출시를 목표로 하는 Godot 대장장이 게임 프로젝트입니다.

> **장비를 대량 생산하는 게임이 아니라, 장비의 출생·성장·소유·사건 기록을 제작하는 대장장이 게임.**

플레이어는 한 명의 대장장이로서 장비 한 점을 직접 만들고, 강화 버튼을 누를 때마다 멈출지 더 도전할지 판단합니다. `+10` 이정표에서 수식어와 성장 방향을 선택하며, 판매·납품한 장비는 세계에서 이력을 쌓아 명성과 다음 의뢰로 돌아옵니다.

## 상태 구분

### 현재 구현

현재 Prototype은 다음을 실제 코드·데이터·테스트로 지원합니다.

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

### 확정 설계·다음 구현

프로젝트 코어는 `CORE_CONFIRMED / CORE_RECORDED`이며, 다음 구현은 **장비 한 점의 생애 PoC**입니다.

```text
검투사 의뢰
→ 철검 제작과 영구 완성도
→ +5 납품 또는 +10 추가 도전
→ 수동 하루 종료
→ 지연된 경기 결과
→ 장비 이력·명성·관계
→ 같은 검투사의 재방문
```

- 피로도는 하루 작업량을 제한합니다.
- 날짜는 플레이어가 직접 하루를 마칠 때만 진행됩니다.
- 남은 피로도의 50%를 다음 날로 이월합니다.
- 작업 예약은 사용하지 않습니다.
- 직원·직접 전투·일상 수리 관리는 제외합니다.
- 중요한 역사 장비의 선택형 복원은 후속 범위입니다.
- 정확한 `+100`은 현재 제품 목표지만 코어 불변값은 아닙니다.

제품 구현은 아직 시작되지 않았습니다. Android 실기기, 접근성, 성능과 외부 플레이테스트도 `NOT_RUN` 또는 `UNVERIFIED`입니다.

## 현행 작업

- Issue: #34 `MVP-003: 장비 한 점의 생애 PoC 구현 및 플레이 검증`
- Core: `docs/superpowers/specs/2026-07-23-project-core-design.md`
- Integrated spec: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- MVP Scope: `docs/MVP-003_SCOPE.md`
- Implementation plan: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`

## 실행

1. GitHub Desktop에서 **Fetch origin → Pull origin**
2. Godot 4.7.1에서 `project.godot`을 열고 **F5**

상세 안내: `docs/GODOT_PLAYTEST.md`

## 프로젝트 운영 시작 위치

1. `AGENTS.md`
2. `[기획서]/00_프로젝트_허브/START_HERE.md`
3. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
4. `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
5. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
6. `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
7. `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`

Base 적용 기준:

- `docs/BASE_RULES_VERSION.md`
- `docs/BASE_ADOPTION_AUDIT.md`

## 기술 기준

- Engine: Godot 4.7.1 stable
- Language: GDScript
- Primary platform: Android mobile
- Distribution: Google Play
- Orientation: Portrait 720×1280
- Package: Android App Bundle (`.aab`)
- Target preparation: Android 16 / API 36+

## 자동 검증

```bash
python tests/check_no_merge_conflicts.py .
python tools/validate_game_data.py
python tests/check_enhancement_failure_contract.py
python tests/check_project_core_alignment.py
```

Godot 코드 변경은 `.github/workflows/godot-validation.yml`의 import, Scene smoke, 모델·통합 테스트를 실행합니다. 실행하지 않은 화면·Android·접근성·성능 검증을 통과로 표시하지 않습니다.
