# Blacksmith

Google Play 출시를 목표로 하는 Android 모바일용 방치형·클리커형 무기 제작·강화 게임입니다.

```text
재료 획득
→ 광클·자동 작업·피버로 기본 무기 제작
→ 빠른 일반 강화와 +10 단위 특수 강화
→ 성장한 무기를 보관
→ 고객 방문 또는 상인 납품으로 판매
→ 골드·명성·희귀 재료로 대장간 성장
```

## 현재 플레이 가능한 POC

### 제작

- 철검 한 사이클
- 터치·자동 작업 진행
- 연속 터치 피버
- 선택 가능한 정밀 마감
- 완벽·좋음·보통 마감
- 완성 철검을 강화 화면으로 전달

### +100 강화

- +10 단위가 아닌 단계: 원클릭 일반 강화
- +10·+20·…·+100: 보조재료·촉매·정밀 판정을 사용하는 특수 강화
- 강화 단계가 높아질수록 공격력 성장량·비용·판매가·위험 증가
- +11부터 단계 하락 가능
- +30부터 파괴 가능
- 실패당 성공률 +4%p, 최대 +24%p
- 안정 단조: 높은 비용으로 파괴 방지·하락 위험 감소
- 폭주 단조: 성공 시 8% 확률로 총 2단계 상승
- 폭주 단조는 특수 강화와 특수 강화를 건너뛸 수 있는 단계에서 사용 불가
- +10부터 수식어를 추가·성장시켜 +100에서 세 수식어 4티어 달성

### 보관함·자동 단조

- 메모리 기반 무기 보관함 6칸
- 현재 공격력·다음 강화 효과·가격·비용·위험 표시
- 목표 강화 단계까지 빠른 자동 진행
- 목표 도달 시 자동 보관
- 보관함이 찰 때까지 반복 생산
- 지정한 보조재료·촉매 재고가 없으면 해당 재료 없이 계속 진행
- 골드 부족·보관함 가득 참·수동 중지 시 종료
- 저장·복귀는 아직 구현되지 않음

## 바로 실행

1. GitHub Desktop에서 `Fetch origin → Pull origin`
2. Godot 4.7.1로 `project.godot` 열기
3. `F5`

`project.godot`의 기본 실행 Scene이 강화 테스트이므로 별도 Scene 파일을 만들거나 선택할 필요가 없습니다. 전체 제작→강화 흐름은 `scenes/main/main.tscn`을 현재 장면으로 실행해 확인합니다.

## 기술 기준

- Godot 4.7.1 / GDScript
- Android portrait 720×1280
- `canvas_items` + `expand`
- Google Play / AAB
- API 36 이상 준비

## 프로젝트 운영 시작점

```text
AGENTS.md
→ [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ SKILL_REGISTRY.json
→ 실제 코드·데이터·테스트
```

공용 운영 기준은 `docs/BASE_RULES_VERSION.md`, 적용 감사 결과는 `docs/BASE_SYNC_AUDIT.md`에서 확인합니다.

## 검증

```bash
python tools/validate_game_data.py
python tools/check_project_governance.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

자동 검증과 실제 화면·플레이 감각·Android 실기기·AAB 검증은 별개입니다.
