# Active Context

## 현재 목표

Godot에서 `제작 → +100 강화 → 무기 보관 → 자동 단조 반복` 흐름을 검증하고, 다음 고객 판매 Vertical Slice로 넘어갈 준비를 한다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 버전 표시: `POC v0.6.0 · main · 2026.07.21.4`
- 제작: 광클·자동 작업·피버·선택적 정밀 마감 구현
- 강화: +0~+100, 일반 강화와 +10 단위 특수 강화 분리
- 성장: 현재 공격력 기준 점진적 증가, 고단계 효과·가격·비용 가속
- 위험: +11부터 단계 하락 가능, +30부터 파괴 가능, 실패 보정 유지
- 단조 방식: 균형·안정·폭주
- 폭주 단조: 성공 시 소량 확률로 총 2단계 상승, 특수 강화와 +9 끝자리 구간 사용 불가
- 보관함: 최대 6개, 강화 종료 후 저장·상세 확인
- 자동 단조: 목표 단계, 반복, 단조 방식, 특수 강화 보조재료·촉매 지정 후 빠른 자동 진행
- 자동 단조 fallback: 지정 보조재료·촉매 재고가 없으면 해당 재료 없이 계속 진행
- 자동 보관: 목표 도달 시 저장, 반복 설정 시 보관함이 찰 때까지 새 무기 진행
- 자동 중지: 골드 부족, 보관함 가득 참, 수동 중지. 파괴 시 반복 설정에 따라 새 무기 재시작 또는 종료
- 자동 검증: 기능 브랜치 기준 Godot 4.7.1 파싱·Scene·모델·JSON 검증 PASS 이력 있음
- Android 실기기·AAB·접근성·성능: NOT_RUN

## 강화 분류

### 일반 강화

- +10 단위가 아닌 단계
- 원클릭 즉시 판정
- 보조재료·촉매·정밀 판정 미사용
- 이전 특수 강화 선택 효과가 누출되지 않음

### 특수 강화

- +10·+20·…·+100
- 보조재료·촉매 선택
- 정밀 판정
- 수식어 추가·성장
- 자동 단조에서는 지정 재료 재고가 있을 때만 소비

## 수식어 성장

- +10: 첫 수식어 1티어
- +20: 첫 수식어 2티어
- +30: 두 번째 수식어 1티어
- +40: 두 번째 수식어 2티어
- +50: 세 번째 수식어 1티어
- +60: 세 번째 수식어 2티어
- +70·+80·+90: 각 수식어 3티어
- +100: 모든 수식어 4티어

## 주요 책임 경로

- 운영 규칙: `AGENTS.md`, `docs/BASE_RULES_VERSION.md`, `docs/BASE_ADOPTION_AUDIT.md`
- 현재 라우팅: `WORK_MODE_AND_SKILL_ROUTING.md`, `SKILL_REGISTRY.json`
- 게임 전체: `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- 테스트 진입: `scenes/test/enhancement_test.tscn`, `scenes/main/main.tscn`
- 강화 모델: `scripts/enhancement/enhancement_session.gd`
- 강화 UI: `scripts/ui/enhancement_screen.gd`, `scripts/ui/enhancement_test_runner.gd`, `scripts/ui/game_flow_screen.gd`
- 데이터: `data/crafting/enhancement_balance.json`, `enhancement_milestones.json`, `materials.json`, `affixes.json`
- 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_forging_session.gd`

## 다음 우선순위

1. Godot에서 폭주 2단계 도약 제한과 자동 단조 목표·반복·재료 fallback을 수동 검수한다.
2. +100 완주 피로도, 가격·효과·위험 곡선을 플레이 관찰로 조정한다.
3. Android 실제 기기에서 세로 화면·스크롤·터치·안전 영역을 검증한다.
4. 무기 보관함과 재화·재료 재고를 고객 판매 루프에 연결한다.
5. MVP-003 방문 검투사 판매를 구현한다.

## 미검증·위험

- Android APK·AAB와 실제 기기 입력
- 저장·복귀·방치 보상
- 고객·상인 판매 루프
- 자동 단조 장시간 반복의 밸런스·성능
- 접근성·태블릿·폴더블·노치
- GitHub Required Check 강제 여부

## 사용자 실행 경로

1. GitHub Desktop에서 Blacksmith `Fetch origin → Pull origin`
2. Godot에서 저장소의 `project.godot` 열기
3. F5 실행
