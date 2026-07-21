# Active Context

## 현재 목표

Godot에서 직접 실행 가능한 강화 테스트를 통해 일반 단계의 원클릭 진행과 +5·+10·+15·+20 이정표 정밀 강화가 자연스럽게 이어지는지 검증한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 구현 상태: 철검 제작과 +20 강화·수식어 이정표 테스트 구현
- 자동 검증: JSON PASS, Godot 프로젝트 파싱 PASS, 제작 모델 4건 PASS, 강화 모델 7건 PASS
- 모바일 검증: 실제 화면 렌더·Android 실기기 미실행

## 구현된 범위

### MVP-001 제작

- `scripts/forging/forging_session.gd`: 제작·피버·마감 상태 계산
- `scripts/ui/forging_screen.gd`: 모바일 중심 제작 UI와 입력
- `data/crafting/forging_balance.json`: 제작 수치
- `tests/unit/test_forging_session.gd`: 제작 모델 테스트

### 강화 이정표 테스트

- `scripts/enhancement/enhancement_session.gd`: +0~+20 강화, 원클릭·정밀 이정표, 실패 보정, 재료 누적, 수식어 추가·강화
- `scripts/ui/enhancement_screen.gd`: 재료·촉매 선택과 이정표 중심 모바일 UI
- `scripts/ui/enhancement_test_runner.gd`: 테스트용 철검으로 강화 화면을 바로 실행
- `scenes/test/enhancement_test.tscn`: Godot 전용 강화 테스트 Scene
- `scripts/ui/game_flow_screen.gd`: 제작 완료 후 강화 진입과 새 제작 복귀
- `data/crafting/enhancement_balance.json`: +1~+20 단계별 성공률
- `data/crafting/enhancement_milestones.json`: +5·+10·+15·+20 정밀 강화와 수식어 변화
- `tests/unit/test_enhancement_session.gd`: 강화 모델 7개 테스트
- `docs/GODOT_PLAYTEST.md`: 직접 실행 안내

### 강화 조작 주기

- +1~+4, +6~+9, +11~+14, +16~+19: 버튼 한 번으로 즉시 성공·실패 판정
- +5: 정밀 강화 후 첫 수식어 1티어 추가
- +10: 정밀 강화 후 첫 수식어 2티어 강화
- +15: 정밀 강화 후 두 번째 수식어 1티어 추가
- +20: 정밀 강화 후 두 번째 수식어 2티어 강화

## 보호 결정

- 광클은 피로·과열 불이익이 아니라 피버 보상으로 이어진다.
- 제작 정밀 마감은 ON/OFF 가능하다.
- 강화 정밀작업은 수식어가 변화하는 +5·+10·+15·+20에서만 필수다.
- 일반 강화는 타이밍 게임 없이 한 번의 클릭으로 즉시 판정한다.
- 기본 제작품인 철검에는 수식어가 붙지 않는다.
- 강화 실패 시 단계 유지, 무기 파괴·수리 없음, 재료 소모와 성공률 보정만 발생한다.
- 직원과 무기 수리는 초기 범위에서 제외한다.

## 직접 테스트

1. Godot 4.7.1에서 `project.godot`을 연다.
2. `scenes/test/enhancement_test.tscn`을 연다.
3. `F6`을 눌러 +0부터 +20까지 강화한다.
4. 전체 제작 흐름은 `scenes/main/main.tscn`에서 확인한다.

## 다음 우선순위

1. 강화 테스트 Scene을 실제 렌더해 버튼·스크롤·정밀 게이지를 시각 검수한다.
2. 플레이 감각에 따라 단계별 성공률과 정밀 구간을 조정한다.
3. Android 기기에서 터치·스크롤·세로 비율·안전 영역을 확인한다.
4. 무기 인벤토리와 최소 골드·재료 경제를 구현한다.
5. 방문 검투사 판매와 상인 납품 의뢰를 구현한다.

## 확인된 검증

- `python tools/validate_game_data.py`: PASS
- Godot 4.7.1 `--headless --editor --path . --quit`: PASS
- `tests/unit/test_forging_session.gd`: PASS — 제작 모델 4건
- `tests/unit/test_enhancement_session.gd`: PASS — 강화 모델 7건
- 일반 단계 원클릭 즉시 판정 확인
- +5·+10·+15·+20 정밀 강화 전환 확인
- +5·+15 수식어 추가와 +10·+20 티어 강화 확인

## 미검증

- 실제 화면 렌더와 광클·강화 플레이 감각
- Android SDK/JDK 및 export template
- API 36 대상 APK·AAB 생성
- 실제 Android 기기 터치·스크롤·화면 안전 영역
- 장시간 방치 저장·복귀
- 기획서 PDF/DOCX 발행과 사람 시각 검수
