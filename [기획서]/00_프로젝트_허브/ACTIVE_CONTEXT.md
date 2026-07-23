# Active Context

## 현재 목표

POC v0.6.4 강화 실패 정책의 단일 정본과 데이터 의미 검증을 완료했다. Issue #29 기준선 시뮬레이터와 15개 분포 실행을 완료했으며, 다음 제품 작업은 한 변수군 후보안 비교와 자동 반복·실제 플레이 검증이다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: 강화 실패 정책 Integration·Completion PASS / 밸런스 시뮬레이션 기준선 실행 완료
- 버전 표시: `POC v0.6.4 · main · 2026.07.23.1`
- 제작: 광클·자동 작업·피버·선택적 정밀 마감 구현
- 제작 품질: 철검 원본 20 기준 보통 20/가치 ×1.00, 좋음 21/×1.05, 완벽 22/×1.12
- 제작 피버 결과: 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 추가 발동 비중첩
- 합산 결과: 피버 적용 보통/좋음/완벽 공격력 21/22/23, 제작 가치 ×1.03/×1.08/×1.15
- 제작 전달: 원본 공격력·마감·피버·합산 제작 배율을 강화와 보관까지 유지
- 자동 반복 제작: 새 철검은 보통 마감·피버 미적용으로 시작
- 강화: +0~+100, 일반 강화와 +10 단위 특수 강화 분리
- 성장: 현재 공격력 기준 점진적 증가, 고단계 효과·가격·비용 가속
- 위험: +11부터 단계 하락 가능, +30부터 파괴 가능, 실패 보정 유지
- 실패 정책 정본: 성공률·보정·하락·파괴·실패 처리 수치는 `data/crafting/enhancement_balance.json`만 소유
- 이정표 정본: `data/crafting/enhancement_milestones.json`은 +10 단위 수식어·특수 강화 구조만 소유하며 실패 정책을 포함하지 않음
- 실패 처리: 선택 재료는 시도 시작 시 소비, 성공 시 보정 초기화, 유지·하락 시 보정 누적, 파괴 시 세션 종료
- 데이터 의미 검증: 성공률 패턴·보정 범위·위험 단조성·도달 가능 decade 0~9·이정표·재료·숨은 레시피 참조를 검사
- 단조 방식: 균형·안정·폭주
- 폭주 단조: 성공 시 소량 확률로 총 2단계 상승, 특수 강화와 +9 끝자리 구간 사용 불가
- 보관함: 최대 6개, 강화 종료 후 저장·상세 확인
- 공유 경제: 수동 강화와 자동 단조가 동일 `WorkshopResources`의 골드·재료 재고와 거래 명령을 사용
- 수동 강화: 실제 비용과 선택 재료를 차감하며, 골드·보조재료 부족 시 무차감·무판정 차단
- 수동 촉매: `사용하지 않음` 허용, 선택 촉매 재고 부족 시 차단
- 자동 단조: 목표 단계·반복·단조 방식·특수 강화 재료 지정 후 자동 진행·보관
- 자동 fallback: 지정 보조재료·촉매가 소진되면 빈 슬롯으로 동일 거래 경로를 사용
- 재료 선택 동기화: 정밀 판정 중 사용 재료 기록을 보존하고, 다음 특수 강화 진입 시 가용 재료로 UI·세션을 함께 갱신
- 자동 중지: 골드 부족·보관함 가득 참·수동 중지. 파괴 시 반복 설정에 따라 재시작 또는 종료
- 공유 경제 자동 검증: 단위 7건·실제 강화 UI 통합 2건 PASS 이력
- 제작 결과 자동 검증: 제작 모델 7건·제작→강화·보관 통합 6건·정적 계약 검사 PASS 이력
- 강화 실패 정책 검증: 데이터 의미·정적 계약·운영체계 참조 감사·고정 Base 전체 회귀 PASS
- Godot 자동 검증: 4.7.1 import·parse, 강화·전체 흐름 Scene, 제작 모델 7건·강화 12건·공유 자원 7건·수동 경제 2건·제작 결과 통합 6건 PASS
- 공식 Workflow 증거: Data validation #352 PASS, Godot validation #310 PASS
- Godot 프로세스 종료코드: `forging=0 enhancement=0 workshop=0 manual_economy=0 forging_quality=0`
- Base 운영체계: 고정 Base의 25개 ACTIVE Skill 기능을 프로젝트 운영 문서와 Skill 3개로 통합
- Base 최신 기준: `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`; 최신 전체 회귀는 PR #32 Workflow 결과로 판정
- 통합 완료: PR #18 공유 경제, PR #20 제작 품질, PR #21 품질 정수·CI, PR #24 제작 피버, PR #25 상태 동기화, PR #26 강화 실패 정책 정합성 main 병합
- PR #26 squash main 커밋: `cce45542f0203d6c0b8dcf13826a5441275e4df5`
- Godot AI 개발 연동: `addons/godot_ai/` 벤더 소스, 에디터 플러그인, `_mcp_game_helper` 오토로드가 최신 main에 포함
- Godot AI 검증: 필수 진입점·`project.godot` 선언·Godot 파싱은 자동 검증, 로컬 MCP 서버·클라이언트 실제 연결은 NOT_RUN
- 밸런스 시뮬레이션: `tools/simulate_enhancement_balance.py`가 런타임 규칙을 고정 roll 반례로 검증하고, 15개 기준선 조합 × 1,000회 결과는 `docs/BALANCE_SIMULATION_REPORT.md`에 기록
- 밸런스 판정: +70 이후 균형·폭주 단일 무기 도달률과 +100 안정 단조 비용은 `TUNE 후보`; 현재 게임 수치·런타임은 변경하지 않음
- 추적 이슈: GitHub Issue #29 `POC: 위험·가격 곡선 기준선 시뮬레이터와 판정 보고서`
- Android 실기기·AAB·사람 시각·접근성·성능·Branch protection 강제: NOT_RUN 또는 UNVERIFIED

## 강화 분류

### 일반 강화

- +10 단위가 아닌 단계
- 원클릭 즉시 판정
- 보조재료·촉매·정밀 판정 미사용
- 실제 보유 골드에서 시도 비용 차감
- 이전 특수 강화 선택 효과가 누출되지 않음

### 특수 강화

- +10·+20·…·+100
- 수동 보조재료 선택 필수
- 촉매는 선택 또는 사용하지 않음
- 정밀 판정
- 수식어 추가·성장
- 수동 시 골드·선택 재료 부족이면 무차감 차단
- 자동 단조에서는 지정 재료 재고가 있을 때만 소비하고, 없으면 명시적 fallback으로 빈 슬롯 진행

## 수식어 성장

- +10: 첫 수식어 1티어
- +20: 첫 수식어 2티어
- +30: 두 번째 수식어 1티어
- +40: 두 번째 수식어 2티어
- +50: 세 번째 수식어 1티어
- +60: 세 번째 수식어 2티어
- +70·+80·+90: 각 수식어 3티어
- +100: 모든 수식어 4티어

## Base 통합 구조

- 작업 자세: `PLAN / BUILD / REVIEW`
- 프로젝트 Skill: `blacksmith-game-design`, `blacksmith-engineering`, `blacksmith-qa`
- 밸런스 분석 Mode: `blacksmith-game-design: balance-simulation`
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 감사 증거: `docs/BASE_ADOPTION_AUDIT.md`, `tools/audit_project_operating_system.py`
- 경기 관람·게임 내 재화 베팅: 삭제하지 않고 MVP-003 이후 별도 PoC 대상으로 보존

## 주요 책임 경로

- 운영 규칙: `AGENTS.md`, `docs/BASE_RULES_VERSION.md`, `docs/BASE_ADOPTION_AUDIT.md`
- 현재 라우팅: `WORK_MODE_AND_SKILL_ROUTING.md`, `SKILL_REGISTRY.json`
- 게임 전체: `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- 밸런스 시뮬레이션: `../../docs/BALANCE_SIMULATION_SCOPE.md`, `../../docs/BALANCE_SIMULATION_REPORT.md`, `../../tools/simulate_enhancement_balance.py`
- 테스트 진입: `scenes/test/enhancement_test.tscn`, `scenes/main/main.tscn`
- 강화 모델: `scripts/enhancement/enhancement_session.gd`
- 공유 경제: `scripts/economy/workshop_resources.gd`
- 강화 UI: `scripts/ui/enhancement_screen.gd`, `scripts/ui/enhancement_test_runner.gd`, `scripts/ui/game_flow_screen.gd`
- 제작 데이터: `data/crafting/forging_balance.json`
- 강화 실패·확률·위험 정본: `data/crafting/enhancement_balance.json`
- 수식어 이정표 정본: `data/crafting/enhancement_milestones.json`
- 재료·수식어: `data/crafting/materials.json`, `data/crafting/affixes.json`
- 모델·통합 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_forging_session.gd`, `tests/unit/test_workshop_resources.gd`, `tests/integration/test_manual_enhancement_economy.gd`, `tests/integration/test_forging_quality_enhancement.gd`
- 정적 계약: `tests/check_forging_quality_contract.py`, `tests/check_enhancement_failure_contract.py`, `tests/check_no_merge_conflicts.py`
- 데이터 의미 검증: `tools/validate_game_data.py`
- Godot AI 연동: `project.godot`, `addons/godot_ai/plugin.cfg`, `addons/godot_ai/plugin.gd`, `addons/godot_ai/runtime/game_helper.gd`, `addons/godot_ai/README.md`

## 다음 우선순위

1. 후보안 하나에서 성공률·비용·하락·파괴 중 한 변수군만 조정해 기준선과 동일 시드 비교를 실행한다.
2. 자동 반복·자원 병목·파괴 후 재시작을 시뮬레이터에 추가하고 실제 플레이 검증 계획을 만든다.
3. 위험·가격 곡선 정합화 뒤 방문 검투사 판매를 구현한다.

## 미검증·위험

- 공유 경제 변경의 실제 사람 수동 화면 검수
- 제작 마감·피버 결과 효과의 실제 사람 화면·체감 검수
- +100 실제 수동 완주와 실패·하락·파괴 피로도
- 위험·가격 곡선 장기 밸런스
- 시뮬레이터와 `EnhancementSession`의 결정적 판정 순서 일치
- Android APK·AAB와 실제 기기 입력
- 저장·복귀·방치 보상
- 고객·상인 판매 루프
- 자동 단조 장시간 반복의 밸런스·성능
- 사람 시각·접근성·태블릿·폴더블·노치
- GitHub Required Check 강제 여부
- 로컬 `uv`·Godot AI MCP 서버·Codex 클라이언트 실제 연결

## 사용자 실행 경로

1. GitHub Desktop에서 Blacksmith `Fetch origin → Pull origin`
2. Godot에서 저장소의 `project.godot` 열기
3. F5 실행
