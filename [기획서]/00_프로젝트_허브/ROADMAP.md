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

현재 목표는 승인 결정·기존 기획·실제 구현·Google Sheet의 권위를 유지하면서 전체 기획을 분야별로 완성하는 것이다. 문서 병합은 제품 구현 승인과 다르다.

## R0 — 운영·정본 복구

상태: `PASS_FOR_DRAFT_PR`.

완료:

- current main 기준 진입 문서·Decision 원장·Registry·Base Adapter 복구
- PR #81 전체 병합 대신 승인 기획 선별 승격 구조
- GitHub·Google Sheet 동일 Decision ID 동기화
- Issue·PR 권위 관계 정리
- 보호 제품 경로 변경 0 확인

제한:

- local validator: `BLOCKED_UNVERIFIED` — container GitHub DNS 실패
- Godot·Android·접근성·성능·사람 플레이: `NOT_RUN`

## R1 — 프로젝트 코어·플레이어 약속

상태: `IN_PROGRESS / APPROVED_BATCH_01`.

### 승인 배치 01

- `BS-CORE-20260802-01`: 피로도·날짜 진행 핵심 불변
- `BS-CORE-20260802-02`: 강화 메인 + 고객·세계 역사 환류
- `BS-SET-20260802-01`: 다양한 작품 제작 동기와 세트 시스템
- `BS-SET-20260802-02`: 사건 연대기 기반 동적 세트
- `BS-SET-20260802-03`: 범용 보정 + 상황 태그 + 역사 기록
- `BS-SET-20260802-04`: 실패 사건도 실제 기여 시 세트 성립

### 현재 코어

```text
직접 제작
→ 강화 성공·실패와 멈춤·추가 도전
→ 피로도에 따른 하루 우선순위
→ 고객 판매·납품
→ 짧은 세계 사건 결과
→ 작품의 소유·운명·연대기·세트
→ 새로운 작품과 더 높은 강화
```

### 남은 R1 범위

- 타깃·비타깃 플레이어
- 플레이 상황과 세션 약속
- 세일즈포인트 최대 3개
- 비타협 조건과 변경 가능한 외피
- 명시적 제외 범위
- 성공 기준과 반증·실패 기준
- +50 대표 경험의 위치
- 세계 환류의 즉시 결과와 지연 기록 경계

### 현재 Gate

`GRILL_BATCH_01_PREMERGE_AUDIT`.

PR #84 병합 후 R1 전체를 완료 처리하지 않고 남은 범위를 계속한다.

## Grill Me 병합 운영

`BS-OPS-20260802-02`:

```text
새 승인 누적
→ 10/10
→ GitHub·Sheet Decision 동기화
→ PR changed files·리뷰·CI·충돌·금지 경로 감사
→ P0/P1 0 확인
→ squash 병합
→ main SHA·Sheet 재동기화
→ 카운터 0/10
```

이번 최초 배치는 사용자의 즉시 지시에 따라 승인 5건으로 병합한다.

## R2 — Core·Session·Meta Loop

시작 조건: `R1_APPROVED`.

범위:

- 첫 행동부터 세션 종료까지 반복 구조
- 제작→강화→멈춤/도전→피로도 배분→판매·납품→사건→성장
- 즉시·세션·장기 보상
- 실패·재도전·복귀
- +5/+10 일상 루프와 +50 장기 하이라이트
- 온보딩과 정보 공개

중요 검토:

- 피로도와 날짜 넘기기가 대기벽 또는 최적 스킵 전략이 되지 않는가
- 세계 결과가 강화 코어를 강화하는가
- 자동화가 핵심 판단을 우회하지 않는가

## R3 — 제작·강화·작품 정체성·실패·저장

시작 조건: `R2_APPROVED`.

범위:

- 제작 입력과 완성도
- 일반·특수·정밀 강화의 책임 분리
- 제작 등급·계보·수식어
- 하락·파괴·보호·완충
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
- 판매·납품 뒤 소유권과 사건 연대기
- 예정 세트→기여 작품→연대기 세트 파이프라인
- 성공·부분 성공·실패·참패 결과 장면
- 상황 태그 기반 추가 정보·선택지·전용 장면
- 재방문·관계·명성·복원·계승 의뢰

중요 검토:

- 직접 전투 범위 팽창 금지
- 사건 RNG가 제작·강화·역할 선택을 압도하지 않음
- 고객·이벤트가 강화보다 긴 필수 플레이가 되지 않음

## R5 — 경제·피로도·성장·장기 목표

시작 조건: `R4_APPROVED`.

범위:

- 골드·재료 Source/Sink
- 피로도 소비·회복·날짜 전환
- 장비·세트 가치·명성·관계
- 연대기 범용 보정·누적 상한·점감
- 실패 연대기 파밍 방지
- 보관함과 작품 관리
- +50 이후 성장 중심
- 악용·무한 루프·소프트락·복구

필수 검증: 수치 시뮬레이션과 경계 조합. 사람 플레이 전 불확실성을 숨기지 않는다.

## R6 — 모바일 UX·접근성·아트·오디오

시작 조건: `R5_APPROVED`.

범위:

- Main Menu와 단일 BlacksmithApp 정보 구조
- View·Overlay·뒤로가기·오류 복구
- Android portrait, safe area, one-hand flow
- 장비 중심 화면과 위험·확률·소유권 설명
- 예정 세트·기여 작품·상황 태그·3줄 역사 요약
- 스타일라이즈드 다크 포지와 밝은 모닥
- 색상 이외 정보 채널·텍스트·모션 감소

Android가 현재 출시 범위이며 PC는 데이터·입력 추상화만 고려한다.

## R7 — 버티컬 슬라이스·데이터·검증·제작 계획

시작 조건: `R6_APPROVED`.

범위:

- 15~25분 대표 세션
- 포함 시스템·대표 콘텐츠·명시적 제외
- 기존 구현 재사용·대체·삭제 금지 경계
- Schema·ID·저장·migration
- 자동 테스트·Godot·Android·접근성·성능·사람 플레이
- 반복 콘텐츠 제작 가능성
- Codex 실행 Packet 초안

모든 승인 기획은 버티컬 슬라이스에서 `구현·검증 대상` 또는 `Decision ID가 있는 명시적 제외`여야 한다.

## R8 — 최종 적대적 검수·사용자 검수

검토 축:

- 플레이어 약속 ↔ 반복 행동
- 강화 코어 ↔ 피로도·세계 일정·세트
- 보상·경제 ↔ 장기 성장
- 시스템 복잡도 ↔ 모바일 온보딩
- 작품 애착 ↔ 파괴·실패·복구·판매
- 세계 환류 ↔ 직접 전투·범위 팽창
- 데이터·저장 ↔ 비가역 결과
- Vertical Slice ↔ 대표 경험·제작량
- GitHub 정본 ↔ Sheet ↔ 실제 구현

미해결 `MUST_FIX`, 미동기화 Decision, 미확정 중요 선택이 있으면 완료하지 않는다.

## R9 — Codex 구현 인계

현재 `BLOCKED`.

필수 입력:

- 승인 Decision IDs
- exact canonical baseline commit
- 기능·콘텐츠·UI·data 범위와 제외
- 보호 동작·assets·interfaces
- 구현 순서와 TDD
- 저장·migration·호환성
- Android·접근성·성능 조건
- 자동·수동 테스트와 기대 결과
- GitHub·Sheet 갱신 위치
- Rollback

Codex는 기획 공백을 추측하거나 주요 기능을 임의 삭제·대체하지 않는다.

## Production Greenlight

다음이 실제 증거로 닫히기 전 Production·Demo Ready를 주장하지 않는다.

- 승인 전체 기획과 명시적 제외 Decision
- 제품 구현과 회귀 테스트
- 저장·복구·migration
- Android build·설치·기기 실행
- 접근성 사람 검토
- 대표·최악 장면 성능
- 외부 플레이 행동 증거
- GitHub·Sheet·실제 구현 일치
