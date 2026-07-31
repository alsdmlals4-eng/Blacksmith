# Blacksmith 남은 기획 항목 판정

> 상태: `CURRENT_PLANNING_STATUS / MID_CHECK_PASS_1_FINDINGS_OPEN`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 추적 Issue: #79

## 1. 결론

고객 유형·개별 고객의 범위와 +50 강화 경로를 벤치마킹·적대적 검토한 결과, 게임 규칙 차원의 미해결 구조적 기획은 0건이다.

그러나 실제 Scene·Script·Resource·데이터를 기준으로 `BS-SCREEN-20260731-01` 중간점검 1차를 수행한 결과, 최신 기획을 실제 화면·상태 전환·저장 구조로 연결하기 위한 P0 Finding 6건과 P1 Finding 4건이 확인됐다.

```text
GAME_RULE_P0_BLOCKER: 0
GAME_RULE_P1_UNDECIDED: 0
SCREEN_FLOW_P0_FINDINGS: 6
SCREEN_FLOW_P1_FINDINGS: 4
USER_DECISIONS_REQUIRED: 2
REVIEW_GATE: MID_CHECK_PASS_1_FINDINGS_OPEN
```

중간점검 책임 원본은 `docs/planning/BLACKSMITH_SITUATION_SCREEN_MID_CHECK_2026.md`다. 현재는 사용자 `기획 완료` 선언 가능 후보가 아니다.

## 2. 완료된 구조적 기획

- 제품 정의·플랫폼·핵심 감정 곡선
- 단조→강화→완성/도전→판매→세계 환류
- +5/+10 일상 루프와 +50 장기 명작 루프
- 제작 등급 5단계
- 계보 1개 + 보조 최대 2개
- +10·20·30·40 정체성 이정표
- +49→+50 일반 정밀강화·고위 정밀강화 이원화
- 특수재료의 촉매·특수 보조재료 역할
- 일반 강화 확률·보호·저장 경계
- 고객 범주 자격·공개 적합도
- 고객 4유형: 수집가·모험가·검투사·군인
- 유형별 복수 이름 고객과 공통 파이프라인
- 카시아 대표 세트·에르사 재사용 증명 세트
- 장비 소유권·운명·연대기
- 첫 5분 화면 흐름·접근성
- 명작 전당 검증 랭킹·레거시 전시 경계
- 플레이테스트 Gate
- 벤치마킹 선행 원칙
- 승인 결정 즉시 정본 동기화 원칙

## 3. 중간점검 1차 완료 범위

- 실제 진입 Scene과 제품 후보 Scene 확인
- 필수 기준 화면 4종의 현재 구현·미구현 분리
- 현재 시각 방향과 UI 생성 방식 확인
- 대표 상황 12개 도출 및 P0~P3 우선순위 부여
- P0 상황 6개의 A~T 구현 명세 작성
- 전체 상황 전환도와 유지 데이터 정리
- 공통 UI·전용 UI·재사용 Scene 후보 분리
- Vertical Slice 화면 구현 순서 작성
- Base 승격 후보와 Blacksmith 전용 항목 분리

필수 기준 화면 대응:

1. 대장간 허브·복귀 화면
2. 단조·강화 핵심 작업대
3. 보관함·자원 관리
4. 제작·강화·고객 세계 결과·장비 연대기 결과

## 4. 열린 P0 Finding

1. `BS-SCR-F01` — F5 진입이 강화 테스트이며 제품 메인 허브가 없음
2. `BS-SCR-F02` — 최신 +50 두 경로와 구형 10단위 특수 강화·세 번째 수식어 슬롯이 충돌
3. `BS-SCR-F03` — 고객 요청·세계 결과가 카일·검투사에 하드코딩
4. `BS-SCR-F04` — 제작·강화·세계 결과가 공통 결과 계약 없이 분산
5. `BS-SCR-F05` — 앱 종료·복귀·미확인 결과를 책임지는 영속 Save Shell이 실제 화면 경로에서 미확인
6. `BS-SCR-F06` — 주요 UI가 런타임 GDScript 조립이라 Scene 재사용·시각 검수 경계가 불명확

이 Finding은 지금 제품 코드를 고치라는 뜻이 아니다. 기획 완료 전에 목표 화면 구조·상태 전환·데이터 계약·구현 경계를 명확히 확정해야 한다는 의미다.

## 5. 열린 P1 Finding

1. `BS-SCR-F07` — 보관함이 무기 6칸·세션 메모리 구조로 최신 작품·소유권·고객 비교를 표현하지 못함
2. `BS-SCR-F08` — 접근성 Overlay의 실기기·포커스·노치 검증 미실행
3. `BS-SCR-F09` — 4개 정보를 수평 배치한 Workshop HUD의 작은 폭·텍스트 확대 과밀 위험
4. `BS-SCR-F10` — 구형 제작 등급·수식어·강화 데이터가 최신 정본과 다름

## 6. 사용자 결정이 필요한 항목

### DECISION-NEEDED-01 — 앱 시작 방식

- A안 권장: 저장 복구 후 별도 타이틀 메뉴 없이 대장간 허브로 즉시 진입
- B안: 타이틀·이어하기·설정 화면을 거쳐 대장간 진입

### DECISION-NEEDED-02 — 제품 Shell과 화면 전환

- A안 권장: 하나의 App Shell 아래 허브·작업대 상태 전환, 보관함·결과 Overlay 혼합
- B안: 기능마다 완전히 별도 Scene으로 교체

두 결정이 확정되면 같은 Decision ID 체계로 GitHub·계획 JSON·Sheet에 즉시 동기화한다.

## 7. 남아 있지만 중간점검 Finding 해소를 막지 않는 항목

### 밸런스 조정값

- 제작 등급별 발생 분포·가치 배율
- 계보·보조·특수 수식어의 정확한 효과량
- 일반 +49→+50 성공·유지·하락·파괴 확률
- 고위 정밀강화 특수재료 비용·요구 수량
- 후보 생성 가중치
- 고객 가격·관계 변화 수치
- 초기 제공 자원량
- 플레이테스트 합격선 재조정

### 콘텐츠 제작값

- 모험가·군인 대표 고객 이름·성격·외형
- 각 유형의 두 번째 이상 이름 고객 프로필
- 유형별 개인 야망·재방문 사건·대사
- 최종 대사와 현지화 템플릿
- 특수재료 이름·획득 서사
- 대표 특수 수식어 명칭·외형 세부안
- 모닥·카시아·에르사 최종 아트 시트
- 장비 연대기 문장 전체 풀

### 플랫폼·운영값

- 실제 확보 가능한 Android 물리 기기 모델
- 최소 Android 버전·메모리·패키지·발열 목표
- 미래 명작 전당 시즌 길이
- 서버·DB·API·인증 기술
- 개인정보·신고·법무 운영 검토

## 8. 다음 절차

```text
사용자 DECISION-NEEDED-01·02 확정
→ P0 Finding 대응 기획 정본 갱신
→ 화면 보드·상황 상세 명세 최종화
→ 적대적 검토 Pass 2
→ 화면 흐름 P0 Finding 0건 확인
→ 사용자 기획 완료 선언 가능 후보 복귀
→ 사용자 기획 완료
→ 구형 정본 전체 전파·PR 병합
→ 적대적 최종 검수
→ 사용자 검수 완료
→ 별도 Codex Goal·구현 Issue
```

## 9. 재개방 조건

다음이 발생하면 구조적 기획을 다시 연다.

- 프로젝트 코어 변경
- 새 핵심 시스템 추가
- 고객 유형 수·유형별 공통 세계 환류 변경
- 한 세션에서 처리하는 요청 수 변경
- +50 일반·고위 정밀강화의 성공·정체성 책임 변경
- 장비 정체성·강화·고객 결과 구조 변경
- 주요 UX 흐름 변경
- 서버·경제·저장 경계 변경
- 화면 중간점검에서 추가 핵심 흐름 단절 발견
- 플레이테스트에서 구조적 실패 발견

재개방 시 `BS-SYNC-20260731-01` 계약과 벤치마킹 선행 원칙을 적용한다.

## 10. 현재 판정

```text
STRUCTURAL_GAME_PLANNING_REMAINING: NONE
SITUATION_SCREEN_MID_CHECK: PASS_1_FINDINGS_OPEN
P0_SCREEN_FINDINGS: 6
P1_SCREEN_FINDINGS: 4
USER_DECISIONS_REQUIRED: 2
TUNABLES_REMAINING: YES_WITH_DEFINED_BOUNDARIES
CONTENT_PRODUCTION_REMAINING: YES
CUSTOMER_PROFILE_PRODUCTION_REMAINING: YES
PLATFORM_VALIDATION_REMAINING: YES
CANONICAL_PROPAGATION_REMAINING: YES
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```
