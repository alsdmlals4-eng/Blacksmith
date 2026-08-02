# Blacksmith Roadmap

## 현재 운영 상태

```yaml
CURRENT_OPERATING_DECISIONS:
  - BS-OPS-20260802-01
  - BS-OPS-20260802-02
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
CURRENT_STAGE_STATUS: IN_PROGRESS / GRILL_BATCH_01_PREMERGE_AUDIT
CURRENT_DRAFT_PR: 84
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_ACTIVITY: MERGE_BATCH_01_THEN_CONTINUE_R1
```

문서 병합은 승인 기획을 main에 보존하는 작업이며 제품 구현 승인과 다르다.

## R0 — 운영·정본 복구

상태: `PASS_FOR_DRAFT_PR`.

- current main 기준 진입 문서·Decision 원장·Base Adapter 복구
- PR #81 전체 병합 대신 승인 기획 선별 승격
- GitHub·Sheet 동일 Decision ID 동기화
- Issue·PR 권위 관계 정리
- 보호 제품 경로 변경 0 확인

local validator는 container DNS 제한으로 `BLOCKED_UNVERIFIED`였으며 Godot·Android·접근성·성능·사람 플레이는 최신 기획 기준 `NOT_RUN`이다.

## R1 — 프로젝트 코어·플레이어 약속

상태: `IN_PROGRESS / APPROVED_BATCH_01`.

승인 배치:

- `BS-CORE-20260802-01`: 피로도·날짜 진행 핵심 불변
- `BS-CORE-20260802-02`: 강화 메인 + 고객·세계 역사 환류
- `BS-SET-20260802-01`: 다양한 작품 제작 동기와 세트
- `BS-SET-20260802-02`: 사건 연대기 기반 동적 세트
- `BS-SET-20260802-03`: 범용 보정 + 상황 태그 + 역사 기록
- `BS-SET-20260802-04`: 실패 사건도 실제 기여 시 세트 성립

```text
직접 제작
→ 강화 성공·실패와 멈춤·추가 도전
→ 피로도에 따른 하루 우선순위
→ 고객 판매·납품
→ 짧은 세계 사건 결과
→ 작품의 소유·운명·연대기·세트
→ 새로운 작품과 더 높은 강화
```

남은 R1:

- 타깃·비타깃 플레이어
- 플레이 상황과 세션 약속
- 세일즈포인트 최대 3개
- 비타협 조건·변경 가능한 외피·제외 범위
- 성공·반증·실패 기준
- +50 대표 경험 위치
- 즉시 세계 결과와 지연 기록 경계

PR #84 병합 후에도 R1은 계속 진행한다.

## Grill Me 병합 운영

```text
새 승인 누적
→ 10/10
→ GitHub·Sheet Decision 동기화
→ changed files·리뷰·CI·충돌·금지 경로 감사
→ P0/P1 0 확인
→ squash 병합
→ main SHA·Sheet 재동기화
→ 카운터 0/10
```

이번 최초 배치는 사용자 지시에 따라 승인 질문 5건으로 병합한다.

## Historical PoC alignment

### 장비 한 점의 생애 PoC — CURRENT

이 문자열은 기존 CI 정렬 계약의 역사 토큰이다. 현행 권위 분류는 `REFERENCE_IMPLEMENTATION`이며 최신 R1 기획 정본을 덮어쓰지 않는다.

- 과거 상태: `IMPLEMENTATION_VALIDATED / HUMAN_VALIDATION_PENDING`
- 과거 CI 증거: `PR validation #468`
- CI 운영 계약: `docs/CI_EXECUTION_POLICY.md`
- 현재 최신 R1 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## R2 — Core·Session·Meta Loop

시작 조건: `R1_APPROVED`.

범위:

- 제작→강화→멈춤/도전→피로도→판매·납품→사건→성장
- 즉시·세션·장기 보상
- 실패·재도전·복귀
- +5/+10 일상 루프와 +50 장기 하이라이트
- 온보딩과 정보 공개

검토:

- 피로도·날짜 넘기기가 대기벽이나 최적 스킵이 되지 않는가
- 세계 결과가 강화 코어를 강화하는가
- 자동화가 핵심 판단을 우회하지 않는가

## R3 — 제작·강화·작품 정체성·실패·저장

시작 조건: `R2_APPROVED`.

범위:

- 제작 입력·완성도·등급·수식어
- 강화 하락·파괴·보호·완충
- 장비 UID와 불변 정체성
- EventChronicle·ChronicleSet·ChronicleModifier·SituationTag
- 실패·부분 성공·성공 기여 판정
- SaveStatus·AttemptIntent·ResultEnvelope
- migration·호환성

확률·비용·용량·시간·태그 유사도는 `RECOMMENDED_DEFAULT / TEST_VALUE`로 시작한다.

## R4 — 고객·세계 일정·사건·장비 연대기

시작 조건: `R3_APPROVED`.

범위:

- 고객 직접 방문과 상인 납품
- 세계 일정·마감·필요 역할
- 예정 세트→기여 작품→연대기 세트
- 성공·부분 성공·실패·참패 결과 장면
- 상황 태그 기반 추가 정보·선택지·전용 장면
- 재방문·관계·명성·복원·계승 의뢰

직접 전투 범위 팽창, 사건 RNG 우위, 과도한 필수 대화·이벤트를 차단한다.

## R5 — 경제·피로도·성장·장기 목표

시작 조건: `R4_APPROVED`.

범위:

- 골드·재료 Source/Sink
- 피로도 소비·회복·날짜 전환
- 장비·세트 가치·명성·관계
- 연대기 보정·누적 상한·점감
- 실패 연대기 파밍 방지
- +50 이후 성장
- 악용·무한 루프·소프트락·복구

## R6 — 모바일 UX·접근성·아트·오디오

시작 조건: `R5_APPROVED`.

범위:

- Main Menu와 BlacksmithApp 정보 구조
- Android portrait·safe area·one-hand flow
- 위험·확률·소유권·결과 설명
- 예정 세트·기여 작품·상황 태그·3줄 역사 요약
- 스타일라이즈드 다크 포지와 밝은 모닥
- 비색상 정보·텍스트·모션 감소

## R7 — 버티컬 슬라이스·데이터·검증·제작 계획

시작 조건: `R6_APPROVED`.

- 15~25분 대표 세션
- 포함 시스템·대표 콘텐츠·명시적 제외
- 기존 구현 보호·재사용 경계
- Schema·ID·저장·migration
- 자동 테스트·Godot·Android·접근성·성능·사람 플레이
- Codex 실행 Packet 초안

## R8 — 최종 적대적 검수·사용자 검수

- 플레이어 약속 ↔ 반복 행동
- 강화 코어 ↔ 피로도·세계 일정·세트
- 경제·성장 ↔ 장기 동기
- 복잡도 ↔ 모바일 온보딩
- 작품 애착 ↔ 파괴·실패·복구·판매
- 세계 환류 ↔ 직접 전투·범위 팽창
- GitHub 정본 ↔ Sheet ↔ 실제 구현

미해결 MUST_FIX, 미동기화 Decision, 미확정 중요 선택이 있으면 완료하지 않는다.

## R9 — Codex 구현 인계

현재 `BLOCKED`.

승인 Decision, exact baseline, 범위·제외, 보호 동작, TDD, 저장·migration, Android·접근성·성능, 테스트, 동기화 위치와 rollback이 필요하다.

## Production Greenlight

승인 전체 기획, 제품 구현, 회귀 테스트, 저장·복구, Android, 접근성, 성능, 외부 플레이, GitHub·Sheet·실제 구현 일치 전에는 Production·Demo Ready를 주장하지 않는다.
