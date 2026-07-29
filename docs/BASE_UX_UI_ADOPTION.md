# Base UX/UI 채택 기록

- Base repository: `alsdmlals4-eng/Base`
- Base main commit: `0fd95f4513343e77fd664af2763a01b02f52545b`
- Shared Skill: `auditing-and-refining-ui-art`
- Project source of truth: `docs/UX_UI_SYSTEM.md`
- Project adapter: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Adopted at: `2026-07-29`

## 적용 범위

- Android 세로형 제작·강화 UX
- 실행 전 비용·위험·결과 예측
- 장비 비교, 터치, safe area, 오류 복구, 결과 복기
- Godot UI와 도메인 상태 소유권 분리

## 검증 상태

- 문서·JSON·PR 검증: 실행
- 제품 코드·Scene·data·asset 변경: 없음
- Godot runtime: `NOT_RUN`
- Android device: `NOT_RUN`
- Human understanding: `HUMAN_NOT_RUN`

공용 원리는 Base에 유지하고 실제 제작 수치·Scene·터치 배치·플레이테스트 결과는 Blacksmith에 유지한다.
