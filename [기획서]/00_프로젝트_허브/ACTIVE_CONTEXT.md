# Active Context

## 현재 목표

제작 마감 품질을 실제 무기 성능·가치에 연결하고 검증 중이며, 다음 단계는 제작 피버 결과 보너스다.

## 현재 상태

- 제품 단계: Prototype
- 작업 게이트: Verification
- 버전 표시: `POC v0.6.2 · main · 2026.07.22.2`
- 제작: 광클·자동 작업·피버·선택적 정밀 마감 구현
- 제작 품질: 보통 공격력/가치 ×1.00, 좋음 ×1.05/×1.05, 완벽 ×1.10/×1.12
- 품질 전달: 원본 공격력·품질 적용 공격력·가치 배율을 강화와 보관까지 유지
- 자동 반복 품질: 새 철검은 보통 마감으로 시작해 최초 수동 품질을 복제하지 않음
- 강화: +0~+100, 일반 강화와 +10 단위 특수 강화 분리
- 성장: 현재 공격력 기준 점진적 증가, 고단계 효과·가격·비용 가속
- 위험: +11부터 단계 하락 가능, +30부터 파괴 가능, 실패 보정 유지
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
- 공유 경제 자동 검증: 단위 7건·실제 강화 UI 통합 2건 PASS
- 제작 품질 자동 검증: 제작 모델 5건·제작→강화·보관 통합 3건·정적 계약 검사 PASS
- Godot 자동 검증: 4.7.1 import·parse, 강화·전체 흐름 Scene, 제작·강화·공유 경제·품질 모델, UI 통합, JSON PASS
- Base 운영체계: 고정 Base의 13개 기능을 프로젝트 운영 문서와 Skill 3개로 통합
- Base 자동 검증: 원본 감사와 공식 Linux 회귀 전체 PASS
- 통합 완료: PR #18 squash 병합 `53cf5edacd5701ec5d412e233d45b35c6e3feb87`, main 핵심 코드 재확인
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
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 감사 증거: `docs/BASE_ADOPTION_AUDIT.md`, `tools/audit_project_operating_system.py`
- 경기 관람·게임 내 재화 베팅: 삭제하지 않고 MVP-003 이후 별도 PoC 대상으로 보존

## 주요 책임 경로

- 운영 규칙: `AGENTS.md`, `docs/BASE_RULES_VERSION.md`, `docs/BASE_ADOPTION_AUDIT.md`
- 현재 라우팅: `WORK_MODE_AND_SKILL_ROUTING.md`, `SKILL_REGISTRY.json`
- 게임 전체: `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- 테스트 진입: `scenes/test/enhancement_test.tscn`, `scenes/main/main.tscn`
- 강화 모델: `scripts/enhancement/enhancement_session.gd`
- 공유 경제: `scripts/economy/workshop_resources.gd`
- 강화 UI: `scripts/ui/enhancement_screen.gd`, `scripts/ui/enhancement_test_runner.gd`, `scripts/ui/game_flow_screen.gd`
- 데이터: `data/crafting/enhancement_balance.json`, `enhancement_milestones.json`, `materials.json`, `affixes.json`
- 테스트: `tests/unit/test_enhancement_session.gd`, `tests/unit/test_forging_session.gd`, `tests/unit/test_workshop_resources.gd`, `tests/integration/test_manual_enhancement_economy.gd`, `tests/integration/test_forging_quality_enhancement.gd`, `tests/check_forging_quality_contract.py`

## 다음 우선순위

1. 제작 마감 품질의 공격력·가치 반영을 PR 검증·병합하고 main을 재확인한다.
2. 제작 피버가 무기 결과에 남기는 작은 보너스를 설계·검증한다.
3. 강화 데이터의 중복 실패 정책을 제거하고 의미 검증을 강화한다.
4. 위험·가격 곡선을 시뮬레이션으로 조정한다.
5. 방문 검투사 판매를 구현한다.

## 미검증·위험

- 공유 경제 변경의 실제 사람 수동 화면 검수
- 제작 품질 효과의 실제 사람 화면·체감 검수
- Android APK·AAB와 실제 기기 입력
- 저장·복귀·방치 보상
- 고객·상인 판매 루프
- 자동 단조 장시간 반복의 밸런스·성능
- 사람 시각·접근성·태블릿·폴더블·노치
- GitHub Required Check 강제 여부

## 사용자 실행 경로

1. GitHub Desktop에서 Blacksmith `Fetch origin → Pull origin`
2. Godot에서 저장소의 `project.godot` 열기
3. F5 실행
