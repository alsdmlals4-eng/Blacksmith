# Skill Learning Log

## 2026-07-21 — 프로젝트 초기 설치

- 결과: 프로젝트 전용 게임 디자인·엔지니어링·QA 진입 스킬 골격 생성
- 검증: 데이터 정적 검증 통과
- 미검증: Godot 프로젝트 로드, Android 빌드, 실제 기기
- 관찰: 초기 프로젝트는 통합 기획서 한 권과 소수의 진입 스킬로 시작하는 것이 적합함
- 스킬 변경 트리거: 첫 수직 프로토타입 구현 중 반복 실패 또는 책임 충돌 발생

## 2026-07-21 — MVP-001 제작 터치

- 결과: 제작 상태 모델, 세로형 UI, 정밀 마감 게이지, Godot 헤드리스 테스트 추가
- 검증: Godot 4.7.1 프로젝트 파싱 PASS, 제작 모델 테스트 4건 PASS, JSON 검증 PASS
- 실패와 수정: 동적 객체 속성에서 지역 변수 타입 추론이 실패해 테스트가 파싱되지 않았으며 `var before: float`로 명시해 해결
- 교훈: GDScript 테스트에서는 동적 Script 인스턴스의 속성값을 받는 지역 변수 타입을 명시한다.
- 유지 결정: 상태 계산을 UI와 분리해 정밀작업 OFF, 피버 배율, 마감 판정, 초기화를 화면 없이 검증한다.
- 미검증: 실제 화면 렌더와 Android 실기기 터치
- 스킬 본문 변경: 한 번의 타입 추론 실패이므로 강제 규칙으로 승격하지 않고 Learning Log에만 기록

## 2026-07-21 — MVP-002 초기 강화

- 결과: 강화 상태 모델, 보조재료·촉매 선택 UI, 정밀 강화, 실패 보정과 제작→강화 화면 전환 추가
- 검증: Godot 4.7.1 프로젝트 파싱 PASS, 제작 모델 4건 PASS, 초기 강화 모델 5건 PASS, JSON 검증 PASS
- 유지 결정: 강화 확률·재료·수식어 판정은 `EnhancementSession`이 소유하고 UI는 선택과 표시만 담당한다.
- 교훈: 재료 성질로 결과 방향을 예측하게 하면 단순 UI에서도 선택 의미를 제공할 수 있다.
- 미검증: 실제 화면 배치, Android 실기기 정밀 타격

## 2026-07-22 — Base 운영체계 통합 감사

- 요청: Base를 상세히 적용하되 구조를 가지치기·통합하고 기능 손실 없이 적대적으로 검토한다.
- 결과: Base 13개 ACTIVE 기능을 운영 문서와 `blacksmith-game-design`, `blacksmith-engineering`, `blacksmith-qa` 세 Skill로 매핑했다.
- 통합: 벤치마크·DDD·플레이테스트·PoC·Vertical Slice·아트 방향은 game-design Mode로, 외부 결과·reference-freshness·접근성·성능·UI 감사는 qa Mode로 합쳤다.
- 자동화: Base 고정 commit 자체 테스트와 Blacksmith Registry·경로·stale 정본을 검사하는 `tools/audit_project_operating_system.py`를 CI에 연결했다.
- 교훈: 공용 Skill 패키지를 복제하지 않아도 기능별 owner·trigger·Mode·검증을 기계적으로 매핑하면 프로젝트 구조를 작게 유지하면서 기능 손실을 탐지할 수 있다.
- 보호: historical Changelog·Learning Log는 과거 증거로 유지하고 활성 정본만 stale 검사한다.
- 미검증: Android 실기기·AAB·사람 시각·접근성·성능 프로파일·Branch protection 강제 여부
