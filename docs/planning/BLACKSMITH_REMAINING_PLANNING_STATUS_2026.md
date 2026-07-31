# Blacksmith 남은 기획 항목 판정

> 상태: `CURRENT_PLANNING_STATUS / VISUAL_BOARD_DRAFT_COMPLETE / FINDINGS_OPEN`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 추적: Issue #79 / Draft PR #81

## 1. 현재 결론

게임 규칙 차원의 구조적 미결정은 없다.

```text
GAME_RULE_P0_BLOCKER: 0
GAME_RULE_P1_UNDECIDED: 0
SCREEN_FLOW_P0_FINDINGS: 6
SCREEN_FLOW_P1_FINDINGS: 4
VISUAL_BOARD_DESIGN_DRAFT: COMPLETE
VISUAL_DECISIONS_REQUIRED: 3
CODEX_IMPLEMENTATION: BLOCKED
```

`BS-SCREEN-20260731-02`에 따라 비주얼 중심 화면 설계를 수행했고, 결과는 다음 문서가 책임진다.

- `docs/planning/BLACKSMITH_VISUAL_SITUATION_BOARD_DESIGN_V1_2026.md`
- `docs/planning/data/blacksmith_visual_situation_board_design_v1_2026.json`

현재는 화면 설계 초안과 적대적 자체 검토가 완료된 상태이며, 사용자 시각 결정 3건이 열려 있으므로 `기획 완료` 선언 가능 후보가 아니다.

## 2. 완료된 구조적 게임 기획

- Android 세로형 대장간 제작·강화·장비 생애 RPG
- 단조→강화→멈춤/도전→고객 인계→세계 결과→연대기
- +5/+10 일상 작품 루프와 +50 장기 명작 루프
- 제작 등급 5단계
- 계보 1개 + 보조 최대 2개
- +10·20·30·40 정체성 이정표
- +49→+50 일반 정밀강화·고위 정밀강화 이원화
- 특수재료의 촉매·특수 보조재료 역할
- 강화 확률·보호·원자 저장 경계
- 고객 4유형: 수집가·모험가·검투사·군인
- 각 유형별 복수 이름 고객과 공통 요청·거래·소유권·세계 결과 파이프라인
- 고객 거래 자격과 공개 적합도 분리
- 장비 소유권·운명·연대기
- 첫 5분 UX·접근성 경계
- 미래 명작 전당 경계
- 벤치마킹 선행 원칙
- 승인 결정·공유 Finding의 즉시 정본 동기화 원칙

## 3. 완료된 화면·비주얼 기획 범위

### 실제 파일 중간점검

- 실제 진입 Scene·제품 후보 Scene·테스트 Scene 확인
- 필수 기준 화면 4종의 현재 구현·미구현 분리
- 대표 상황 12개와 P0~P3 우선순위 도출
- P0 상황 6개의 A~T 기술 명세
- 실제 UI 색·패널·입력·PoC 제약 확인

### 비주얼 보드 설계

- `BOARD-A`: 프로젝트 비주얼 기준
- `BOARD-B1`: 대장간 허브·복귀
- `BOARD-B2`: 단조·강화 작업대
- `BOARD-B3`: 보관함·자원 관리
- `BOARD-B4`: 결과·장비 연대기
- `BOARD-C1`: 첫 작품 단조 시퀀스
- `BOARD-C2`: 일반 강화 판단 시퀀스
- `BOARD-C3`: +49→+50 경로 선택 시퀀스
- `BOARD-C4`: 이름 고객 거래 시퀀스
- `BOARD-C5`: 세계 결과·연대기 귀환 시퀀스
- `BOARD-D`: 최소 구현 명세 부록

모든 화면과 요소는 `CURRENT / INFERRED / PROPOSED / PLACEHOLDER`로 구분한다.

## 4. 열린 P0 Finding

1. `BS-SCR-F01` — F5 진입이 강화 테스트이며 제품 메인 허브가 없음
2. `BS-SCR-F02` — 최신 +50 두 경로와 구형 10단위 특수 강화·세 번째 수식어 슬롯 충돌
3. `BS-SCR-F03` — 고객 요청·세계 결과가 카일·검투사에 하드코딩
4. `BS-SCR-F04` — 제작·강화·세계 결과가 공통 결과 계약 없이 분산
5. `BS-SCR-F05` — 앱 종료·복귀·미확인 결과를 책임지는 영속 Save Shell이 실제 화면 경로에서 미확인
6. `BS-SCR-F06` — 주요 UI가 런타임 GDScript 조립이라 Scene 재사용·시각 검수 경계가 불명확

비주얼 설계 초안은 각 Finding의 목표 화면·상태 전환·공통 UI 방향을 제안했지만, 사용자 승인 전에는 Finding을 닫지 않는다.

## 5. 열린 P1 Finding

1. `BS-SCR-F07` — 보관함이 무기 6칸·세션 메모리 구조로 최신 작품·소유권·고객 비교를 표현하지 못함
2. `BS-SCR-F08` — 접근성 Overlay의 실기기·포커스·노치 검증 미실행
3. `BS-SCR-F09` — 4개 정보를 수평 배치한 Workshop HUD의 작은 폭·텍스트 확대 과밀 위험
4. `BS-SCR-F10` — 구형 제작 등급·수식어·강화 데이터가 최신 정본과 다름

## 6. 사용자 확인이 필요한 시각 결정

### DEC-VIS-01 — 앱 시작 방식

**권장안**

```text
앱 실행
→ 저장 복구
→ 미확인 비가역 결과 우선 확인
→ 대장간 허브 즉시 진입
```

별도 타이틀 메뉴는 두지 않고 설정·크레딧은 허브에서 접근한다.

대안은 타이틀·이어하기·설정을 거쳐 허브에 진입하는 방식이다.

### DEC-VIS-02 — 제품 Shell과 화면 전환

**권장안**

하나의 `BlacksmithApp` Shell 아래 허브·단조·강화를 상태 View로 전환하고, 보관함·결과는 Overlay 또는 내부 Screen으로 사용한다.

대안은 기능마다 완전한 별도 Scene으로 교체하는 방식이다.

### DEC-VIS-03 — 최종 아트 렌더링 강도

**권장안**

- 배경·장비: 질감이 읽히는 스타일라이즈드 2D 일러스트
- 고객: 과도한 반실사보다 단순화된 게임 일러스트 반신
- 모닥: 작고 단순한 상징 마스코트
- UI: 철·황동 재질을 암시하되 실제 금속 텍스처 과다 사용 금지

실제 제품 아트가 없으므로 현재 상태는 `PROPOSED`다.

## 7. 남아 있으나 구조 결정을 막지 않는 조정값

### 밸런스

- 제작 등급 분포·가치 배율
- 계보·보조·특수 수식어 효과량
- 일반 +49→+50 결과 확률
- 고위 정밀강화 재료 비용·요구량
- 고객 가격·관계 변화 수치
- 초기 제공 자원량

### 콘텐츠

- 모험가·군인 대표 고객
- 유형별 두 번째 이상 이름 고객 프로필
- 특수재료 이름·획득 서사
- 최종 대사·연대기 문장 풀
- 모닥·카시아·에르사와 장비 최종 아트 시트

### 플랫폼·운영

- 실제 Android 기준 기기
- 최소 OS·메모리·발열 기준
- 미래 명작 전당 서버·시즌·신고·법무 정책

## 8. 다음 절차

```text
사용자 DEC-VIS-01·02·03 확인
→ 승인 Decision ID 발급·GitHub·계획 JSON·Sheet 즉시 동기화
→ 비주얼 화면 명세 v1 확정본 갱신
→ P0 Finding 대응 정본 연결
→ 적대적 검토 Pass 2
→ 화면 흐름 P0 Finding 0건 판정
→ 사용자 기획 완료 선언 가능 후보 복귀
→ 사용자 기획 완료
→ 구형 정본 전체 전파·PR 병합
→ 적대적 최종 검수
→ 사용자 검수 완료
→ 별도 Codex Goal·구현 Issue
```

## 9. 현재 Gate

```text
STRUCTURAL_GAME_PLANNING_REMAINING: NONE
SITUATION_SCREEN_MID_CHECK: PASS_1_FINDINGS_OPEN
VISUAL_BOARD_DESIGN_DRAFT: COMPLETE
VISUAL_BOARD_ADVERSARIAL_SELF_REVIEW: PASS
P0_SCREEN_FINDINGS: 6
P1_SCREEN_FINDINGS: 4
USER_VISUAL_DECISIONS_REQUIRED: 3
VISUAL_BOARD_IMAGE_PRODUCTION: NOT_RUN
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```
