---
name: blacksmith-mobile-ux
description: Review and improve the implemented Blacksmith portrait mobile flow, touch targets, scrolling, precision input, information hierarchy, and accessibility barriers with real render evidence.
---

# Blacksmith Mobile UX

## Modes

- `flow-review`
- `touch-review`
- `accessibility-review`
- `visual-runtime-check`

## Scope

- 720×1280 portrait
- 작은 PC 미리보기 창
- 한 손 엄지 도달
- 일반/특수 강화 전환
- 확률·가격·위험 정보
- 정밀 게이지
- 보관함·자동 단조 설정

## Checks

- 핵심 버튼이 충분히 크고 겹치지 않는가
- 현재 상태와 다음 결과가 한눈에 구분되는가
- 하락·파괴를 색만으로 전달하지 않는가
- 스크롤 중 주요 실행 버튼을 잃지 않는가
- 연타·정밀 입력에 자동 대안이 있는가
- 위험 행동의 확인·복구가 명확한가
- 버전 배지가 콘텐츠를 가리지 않는가
- 작은 화면과 안전 영역에서 잘리지 않는가

실제 Godot 렌더나 Android 기기 없이 시각·터치 PASS를 선언하지 않는다.
