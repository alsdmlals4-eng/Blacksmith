---
name: blacksmith-game-design
description: Use when reviewing Blacksmith player experience, game rules, balance, feature design, visual intent, or playtest evidence.
---

# Blacksmith Game Design

## 읽기와 범위

Repository AGENTS.md → `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md`의 current-authority → production/fields → 해당 기능의 승인 원본·JSON·실제 사용처를 읽는다.
장르명·구형 Game Bible·스킬 본문으로 코어·그림체·강화 규칙을 정하지 않는다.
읽기 전용 설명은 사실과 미확인을 답하고 제품 수정·새 승인·새 보고서를 만들지 않는다.

## 필요한 작업만 선택

- frame / identify-project-core / classify-core-support: 현재 승인 경험과 실제 구현을 구분하고 핵심·지원·외피를 판단한다.
- update-system / balance-review / balance-simulation: 해당 Decision·데이터·판정 순서·저장 영향을 확인한다. 핵심/경제/저장 의미 변화는 새 결정이다.
- benchmark-and-player-research / playtest-and-experiment: 기존 유효 근거부터 사용하고 부족한 질문만 조사한다. 제품 사실·관찰·자기보고·해석을 구분한다.
- visual-brief / art-brief / visual-qa-and-approval: 현재 승인 방향과 실제 consumer·상태군·규격을 연결한다. 이미지 도구·크로마키/alpha·사후 승인·런타임 증거는 AGENTS의 경계를 따른다.
- 나머지 Registry mode는 위 같은 책임 안에서 필요한 경우만 적용한다. 자동 전체 체크리스트가 아니다.

## 재미 가설에서 구현까지

플레이어-facing 변경은 운영 계약의 재미 검증 절을 사용한다. Base #885의 방법을 현재 프로젝트에 맞추되 새 감독 스킬/점수표를 만들지 않는다.
기존 기능 원본에 요구 ID, 승인된 경험, 가설·반례, 대표 구간, 상태·선택·정보·피드백, 실제 consumer, 검증/다음 결정을 연결한다.
L1은 짧은 연결, 주요 기능은 기존 상세 명세를 사용한다. 미구현은 PLANNED다. 단순 내부/기계 수정은 영향이 없다는 이유를 기록하거나 기존 비퇴행 근거를 재사용한다.

- 강화: 위험·비용·태그 선택의 이해와 STOP OR PUSH 판단을 관찰한다. 오래 고민했다는 이유로 재미라고 단정하지 않는다.
- 의뢰/세계 결과: 같은 장비와 결과의 인과를 이해하는지 확인한다. 보상 수령률만으로 애착을 확정하지 않는다.
- 효과/비주얼/UI: 목적·필요 상태·정보 공개·시점/반복·중단/복귀·자산·consumer·확인 방법을 구체화한다. 규칙 효과와 표현 효과의 책임을 분리한다.

위 질문은 기존 경험을 검증하는 가설이지 새 게임 규칙이나 합격 수치가 아니다.
DOC/MACHINE/RUNTIME/HUMAN/USER_APPROVAL/RELEASE는 별개다. 자동 테스트·AI 평가는 HUMAN/FUN_PASS가 아니다.
첫 이해와 반복 피로, 행동과 자기보고, 반대 근거를 비교한다. 사람 미검증은 승인 구현을 순환 차단하지 않는다.
실패는 이해/선택·규칙/연출/리듬·콘텐츠/빌드 문제로 나누고 KEEP/CHANGE/DEFER/RETEST를 기존 Decision에 연결한다.

## 수치·산출물

수치는 해당 JSON과 실제 판정 순서가 소유한다. 임시값은 가설이며 평균뿐 아니라 분포·실패·병목·선택별 차이를 본다.
변수·가드레일·중단 기준을 먼저 정한다. 범위가 실제 밸런스 시뮬레이션이면 `docs/BALANCE_SIMULATION_SCOPE.md`의 해당 계약만 읽는다.
산출물은 기존 원본의 변경/보호·가설·consumer·검증·미확인·다음 판단이다. 승인 이미지와 저장 의미는 임의 교체하지 않는다.
재사용할 실패/교정 근거가 생겼을 때만 기존 `skills/SKILL_LEARNING_LOG.md`를 갱신한다. 일반 작업일지는 기존 날짜별 source에 누적한다.
