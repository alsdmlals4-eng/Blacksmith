# Tests

현재 자동 검증은 프로젝트 운영체계·JSON 데이터·Godot 4.7.1 파싱·Scene smoke·제작/강화 모델을 실행한다.

## 명령

```bash
python tools/check_project_governance.py
python tools/validate_game_data.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
```

## 제작 모델 — 4 cases

- 제작 진행도와 자동 작업
- 피버 게이지·배율
- 정밀 마감 ON/OFF와 완벽 판정
- 제작 세션 초기화

## 강화 모델 — 12 cases

- 일반/특수 강화 분리
- 현재 공격력 기반 점진 성장
- 고단계 비용·판매가 가속
- 촉매 가격·가치 효과
- +10 이하 유지와 실패 보정 +4%p
- +11 단계 하락
- +30 무기 파괴
- 안정 단조·수호 가루 보호
- 폭주 단조 8% 총 2단계 도약
- 폭주의 특수 강화 건너뛰기 차단
- +10 첫 수식어
- +100 세 수식어 4티어

## Project Governance

- Base 기준 커밋
- 필수 시작 문서·Registry·Skill 경로
- automatic-trigger-match와 Work Mode
- 활성 문서의 과거 규칙 표현
- 강화 JSON 핵심 계약
- F5 Main Scene
- 임시 Workflow 제거
- 모든 JSON 구문

## 후속 테스트

- 보관함 6칸 초과·파괴 무기 보관 방지
- 자동 단조 골드 부족·재료 0·목표 초과·반복 종료
- 고객 방문 인센티브
- 상인 납품 가격
- 저장·방치 복귀와 migration
- Android 터치·화면 비율·안전 영역
- 실제 UI 렌더·접근성·성능

자동 PASS는 실제 화면·Android 기기 PASS가 아니다.
