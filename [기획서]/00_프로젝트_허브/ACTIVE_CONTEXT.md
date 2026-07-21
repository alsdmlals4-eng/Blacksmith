# Active Context

## 현재 목표

Godot에서 철검 제작 후 +100까지 강화하는 모바일 조작 흐름을 검증한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 제작: 광클·자동 작업·피버·정밀 마감 구현
- 최대 강화: +100
- 일반 단계: 원클릭 즉시 판정
- +5 단위: 정밀 강화
- +10 단위: 보조재료·촉매 표시 및 적용 + 정밀 강화
- 자동 검증: JSON PASS, Godot 파싱 PASS, 테스트 Scene PASS
- 모델 테스트: 제작 4건 PASS, 강화 8건 PASS
- Android 실기기 검증: 미실행

## 수식어 성장

- +10/+20: 첫 수식어 추가·강화
- +30/+40: 두 번째 수식어 추가·강화
- +50/+60: 세 번째 수식어 추가·강화
- +70/+80/+90: 각 수식어 3티어
- +100: 모든 수식어 4티어

## 주요 경로

- `scenes/test/enhancement_test.tscn`
- `scripts/enhancement/enhancement_session.gd`
- `scripts/ui/enhancement_screen.gd`
- `data/crafting/enhancement_balance.json`
- `data/crafting/enhancement_milestones.json`
- `tests/unit/test_enhancement_session.gd`
- `docs/GODOT_PLAYTEST.md`

## 보호 결정

- 강화 실패 시 단계 유지, 무기 파괴·수리 없음
- 보조재료와 촉매는 +10 단위에서만 표시·적용
- 최대 강화는 +100
- 직원과 무기 수리는 초기 범위에서 제외

## 다음 우선순위

1. Godot 창에서 +5와 +10 UI 차이 검수
2. +100까지 수동 플레이 피로도·성공률 검수
3. Android 터치·스크롤·안전 영역 검증
4. 무기 인벤토리와 최소 경제 구현
5. 방문 검투사 판매와 상인 납품 구현

## 미검증

- 실제 Godot 창에서 +100 완주
- Android APK·AAB
- 저장·복귀
- 판매·인벤토리·경제
