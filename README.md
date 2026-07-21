# Blacksmith

Google Play 출시를 목표로 하는 Android 모바일용 방치형·클리커형 무기 제작·강화 게임 프로젝트입니다.

플레이어는 광클과 피버로 무기를 만들고, 일반 강화와 +10 단위 특수 강화를 반복합니다. 고단계에서는 효과·가격·비용과 함께 단계 하락·파괴 위험이 커지며, 완성 무기는 보관하거나 목표 단계까지 자동 단조할 수 있습니다.

## 현재 구현

### 제작

```text
철 고정 → 광클·자동 작업 → 피버 → 선택적 정밀 마감 → 철검 완성
```

- 터치·자동 작업 진행
- 연속 터치 피버와 작업 배율
- 정밀 마감 ON/OFF
- 완벽·좋음·보통 마감

### +100 강화·특수 강화

```text
철검 → 일반 강화 → +10 특수 강화 → 고단계 하락·파괴 → +100 수식어 완성
```

- 일반 강화: +10 단위를 제외한 단계, 원클릭 즉시 판정
- 특수 강화: +10·+20·…·+100
- 보조재료·촉매·정밀 판정은 특수 강화에서만 적용
- 현재 공격력 기준 점진 성장과 고단계 가격·비용 가속
- 다음 공격력·판매가·비용·성공/유지/하락/파괴 확률 표시
- +11부터 단계 하락, +30부터 파괴 가능
- 실패 보정과 안정 단조 보호
- +100에서 수식어 3개가 모두 4티어

### 폭주 단조

- 성공 시 낮은 확률로 총 2단계 상승
- 특수 강화에서는 사용 불가
- +9·+19·+29처럼 도약이 특수 강화 이정표를 건너뛸 구간에서 사용 불가

### 보관함·자동 단조

- 강화 무기 최대 6개 보관
- 공격력·판매가·누적 비용·수식어·촉매·마감 품질 확인
- 목표 강화 단계와 반복 여부 지정
- 자동 단조용 단조 방식·보조재료·촉매 지정
- 특수 강화 재료가 없으면 해당 재료 없이 계속 진행
- 목표 도달 자동 보관
- 반복 설정 시 보관함이 찰 때까지 새 철검 진행
- 골드 부족·보관함 가득 참·수동 중지·파괴 처리

## 실행

사용자가 할 일은 두 가지입니다.

1. GitHub Desktop에서 **Fetch origin → Pull origin**
2. Godot 4.7.1에서 저장소의 `project.godot`을 열고 **F5**

상세 안내: `docs/GODOT_PLAYTEST.md`

## 프로젝트 운영 시작 위치

1. `AGENTS.md`
2. `[기획서]/00_프로젝트_허브/START_HERE.md`
3. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`
4. `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`
5. `[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md`
6. `[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json`
7. `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`
8. `[기획서]/00_프로젝트_허브/WORK_MODE_AND_SKILL_ROUTING.md`

Base 적용 기준과 전수 대조:

- `docs/BASE_RULES_VERSION.md`
- `docs/BASE_ADOPTION_AUDIT.md`

## 기술 기준

- Engine: Godot 4.7.1 stable
- Language: GDScript
- Primary platform: Android mobile
- Distribution: Google Play
- Orientation: Portrait 720×1280
- Store package: Android App Bundle (`.aab`)
- Target preparation: Android 16 / API 36+

## 자동 검증

```bash
python tools/validate_game_data.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

자동 검증과 실제 화면·Android·접근성·성능 검증을 구분합니다. 실행하지 않은 검사는 `NOT_RUN` 또는 `UNVERIFIED`입니다.
