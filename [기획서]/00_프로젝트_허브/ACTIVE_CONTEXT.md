# Active Context

## 현재 목표

Godot에서 철검 제작 후 +100까지 강화하는 모바일 조작 흐름을 검증한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 제작: 광클·자동 작업·피버·정밀 마감 구현
- 최대 강화: +100
- 일반 강화: +10 단위가 아닌 모든 단계, 원클릭 즉시 판정
- 특수 강화: +10·+20·…·+100
- 특수 강화 구성: 보조재료·촉매 선택 + 정밀 판정 + 수식어 성장
- 자동 검증: 최신 `main` GitHub Actions 확인 필요
- Android 실기기 검증: 미실행

## 강화 분류

### 일반 강화

- +1~+9, +11~+19처럼 +10 단위를 제외한 모든 단계
- 원클릭으로 즉시 성공·실패 판정
- 보조재료·촉매·정밀 판정 미사용
- 이전 특수 강화에서 선택한 촉매 효과가 적용되지 않음

### 특수 강화

- +10·+20·+30·…·+100
- 보조재료와 촉매 선택 영역 표시
- 정밀 판정 필수
- 수식어 추가 또는 티어 성장

## 수식어 성장

- +10: 첫 수식어 1티어
- +20: 첫 수식어 2티어
- +30: 두 번째 수식어 1티어
- +40: 두 번째 수식어 2티어
- +50: 세 번째 수식어 1티어
- +60: 세 번째 수식어 2티어
- +70·+80·+90: 각 수식어 3티어
- +100: 모든 수식어 4티어

## 성공률과 실패

- 10단계 성공률 패턴 반복
- 높은 강화 구간일수록 기본 성공률 점진 감소
- 실패 시 강화 단계 유지
- 무기 파괴·수리 없음
- 실패당 다음 성공률 +5%p, 최대 +20%p
- 성공 시 실패 보정 초기화

## 주요 경로

- `scenes/test/enhancement_test.tscn`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/ui/special_enhancement_screen.gd`
- `data/crafting/enhancement_balance.json`
- `data/crafting/enhancement_milestones.json`
- `tests/unit/test_enhancement_session.gd`
- `docs/GODOT_PLAYTEST.md`

## 사용자가 할 일

1. GitHub Desktop에서 Blacksmith 저장소의 `Fetch origin`과 `Pull origin`을 누른다.
2. Godot에서 `project.godot`을 열고 테스트 Scene을 실행한다.

## 다음 우선순위

1. Godot 창에서 +5 일반 강화와 +10 특수 강화의 UI 차이를 검수한다.
2. +100까지 수동 플레이 피로도·성공률을 검수한다.
3. Android 터치·스크롤·안전 영역을 검증한다.
4. 무기 인벤토리와 최소 경제를 구현한다.
5. 방문 검투사 판매와 상인 납품을 구현한다.

## 미검증

- 실제 Godot 창에서 +100 완주
- Android APK·AAB
- 저장·복귀
- 판매·인벤토리·경제
