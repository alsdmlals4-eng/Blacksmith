# Blacksmith Current Confirmed Decisions

> R1 정본 기준 병합: PR `#94`
>
> R1 정본 기준 SHA: `8a0956d6c8b4cf3db545a17d0bd002ba8354d568`
>
> Sheet 최종 동기화 기준: `BS-OPS-20260803-04 / READBACK_PASS`
>
> R1 최종 사용자 승인: `BS-OPS-20260803-05 / USER_APPROVED`
>
> R2 첫 승인 Decision: `BS-WORLD-20260803-02 / USER_APPROVED / BASELINE_TEST_PRESET`
>
> R2 체크포인트: `BS-OPS-20260803-06 / EARLY_CHECKPOINT_1_OF_10 / MERGED_PR99`
>
> R2 체크포인트 main SHA: `534ac05596573ae4055fa97a4e6888f4e8966b05`
>
> 현재 단계: `R2_CORE_SESSION_META_LOOP / PLANNING_ACTIVE`
>
> 상태: `R1_USER_APPROVED / R2_CHECKPOINT_001_CANON / NEXT_GRILL_ME_COUNTER_0_OF_10 / PRODUCT_BLOCKED`

## 1. 권위 규칙

1. 최신 사용자 승인 Decision과 병합된 최종 정본
2. `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
3. `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
4. 현재 Hub·Roadmap 문서
5. 과거 Prototype·PoC·연구·Draft 문서

과거 문서가 최신 Decision과 충돌하면 최신 Decision이 우선한다. 미검증 정확한 수치·주기·확률·경제값은 제품 확정값이 아니라 버전형 테스트 프리셋이다.

## 2. 운영 Decision

- `BS-OPS-20260802-01`: 총기획·정본 복구를 제품 구현보다 우선
- `BS-OPS-20260802-02`: 승인 배치·적대적 감사·squash 병합 정책
- `BS-OPS-20260802-03~05`: 배치 002~004 감사·병합
- `BS-OPS-20260802-06`: 주요 Grill Me·작업에 공식 벤치마킹과 현업 비교 적용
- `BS-OPS-20260803-01`: Game Bible·Hub·Roadmap·MVP·Registry·Sheet 정렬
- `BS-OPS-20260803-02`: PR #94 적대적 감사·병합, P0/P1 0
- `BS-OPS-20260803-03~04`: PR #96·#97 post-merge 상태와 Sheet 동기화 Gate 최종화
- `BS-OPS-20260803-05`: 사용자 R1 정본 최종 승인, R2 기획 Gate 개방
- `BS-OPS-20260803-06`: R2 승인 1/10 조기 체크포인트와 프로젝트 Base 어댑터 권위 드리프트 봉합

제품 구현은 R1~R8 전체 기획과 최종 사용자 검수 전까지 `BLOCKED`다.

## 3. R1·R2 승인 결정

- `BS-CORE-20260802-03`: 현재 검증 상한 `+50`, 매 `+10` 이정표, 최종 상한 `DEFERRED`
- `BS-CORE-20260802-04`: 일반 수식어 A·B 두 개, 세계일정 성질은 별도 계층
- `BS-CORE-20260803-01`: 활성 사건·연대기 수식어 한 개와 진화 이력
- `BS-CORE-20260803-02`: 한 작품 `+50` 생애 왕복 버티컬 슬라이스
- `BS-CORE-20260803-03`: 구조는 정본, 정확한 숫자는 버전형 테스트 프리셋
- `BS-CORE-20260803-04`: 행동 증거+중립적 회상 인터뷰 검증 Gate
- `BS-WORLD-20260803-01`: 세계일정은 날짜마다 단계적으로 진행하며 규모가 클수록 더 오래 걸림
- `BS-WORLD-20260803-02`: 첫 코어 슬라이스는 납품 당일 준비, 1일차 초기 사용, 2일차 변수·전환점, 3일차 최종 결과, 4일차 같은 UID 재방문을 기준 프리셋으로 사용

통합 정본:

- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `docs/planning/BLACKSMITH_R2_WORLD_SCHEDULE_BASELINE_CHECKPOINT_001_2026.md`
- `docs/planning/BLACKSMITH_R1_FINAL_APPROVAL_AND_WORLD_SCHEDULE_PROGRESS_2026.md`
- `docs/planning/BLACKSMITH_R1_CANON_ALIGNMENT_AND_PR94_AUDIT_2026.md`

## 4. 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
강화의 즉각 판단
→ 작품을 세상에 보냄
→ 작품의 생애와 세계 결과가 날짜마다 진행됨
→ 같은 UID의 변화와 결과가 돌아옴
→ 다음 강화·복원·제작 이유가 생김
```

강화는 반복 동력이고 작품 생애와 세계 환류는 의미·장기 보상이다.

## 5. 코어 구조

- 현재 검증 상한: `+50`
- 정밀 이정표: `+10 / +20 / +30 / +40 / +50`
- 장기 최종 상한: `DEFERRED`
- 일반 수식어: A·B 두 개
- 활성 사건·연대기 수식어: 한 개의 진화 계보
- 방문 고객에게 실제 인계한 뒤 작품 생애 활성화
- 같은 UID가 소유·사용·결과·손상·복원·계승·재방문 유지
- 일반 실패와 대파는 UID·역사를 삭제하지 않음
- 완전 파괴는 명시적이고 정보가 제공된 선택에서만 허용하며 역사 기록 보존
- 피로도는 오늘의 작업 우선순위 자원
- 날짜는 고객·세계일정·재방문의 공통 시간축
- 세계일정은 발생 당일 또는 첫 날짜 진행 한 번으로 최종 해결되지 않음
- 날짜마다 최대 한 단계씩 진행하고 최종 결과 전에 최소 하나의 중간 상태를 제공
- 규모가 클수록 필요한 단계와 게임 날짜가 늘어남

## 6. 첫 코어 버티컬 슬라이스

```text
플레이어가 선택한 작품 한 점 제작
→ +10/+20/+30/+40/+50 정밀 이정표
→ 방문 고객 납품
→ 납품 당일: 사용 계획·준비·예상 기여
→ 1일차: 출발·초기 사용·초기 접촉
→ 2일차: 변수·위험·기회·전환점
→ 3일차: 최종 세계 결과
→ 4일차: 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
→ 작품 생애가 다음 강화 이유로 환류
```

`+50` 도달만으로 완료하지 않는다. 세계일정은 최소 한 번의 중간 진행을 거치며 다른 작품군은 제한된 비플레이 미리보기로만 제시한다. 정확한 3일 결과·4일차 재방문은 `BASELINE_TEST_PRESET`이며 사람 플레이에 따라 조정한다.

## 7. 세계일정 진행 권위

- 납품 당일의 피드백은 사용 계획·초기 반응·예상 기여이며 최종 결과가 아니다.
- 하루 종료 한 번당 세계일정은 최대 한 단계 또는 한 개의 명시적 진행 단위만 전진한다.
- 모든 일정은 발생 상태, 하나 이상의 중간 상태, 별도 날짜의 최종 상태를 가진다.
- 첫 코어 슬라이스 기준 프리셋은 `납품 당일 준비 → 1일차 초기 사용 → 2일차 변수·전환점 → 3일차 최종 결과 → 4일차 재방문`이다.
- 기간 상대 관계는 `LOCAL/PERSONAL < REGIONAL/FACTION < REALM/NATIONAL < WAR/CATASTROPHE`를 따른다.
- 정확한 날짜·단계 수·분기 수는 `BASELINE_TEST_PRESET`이다.
- 날짜 경과만으로 사건 수식어가 자동 성장하지 않으며 실제 사용·기여·인과가 필요하다.
- 기간을 늘리기 위한 빈 대기 로그·필수 장문 대화·날짜 스킵 최적화를 금지한다.

## 8. 수치·검증 권위

정본은 자원 종류·소비 시점·반환 여부·정보 공개·상태 전이·피로도와 날짜 역할·세계일정 규모와 기간의 상대 관계를 소유한다. 정확한 비용·확률·소비량·보상량·세계일정 날짜·재방문 간격은 `LEGACY_IMPLEMENTED_VALUE / BASELINE_TEST_PRESET / EXPERIMENT_VARIANT / CURRENT_VALIDATED / DEPRECATED_PRESET`으로 관리한다.

코어 재미는 다음 행동 증거와 중립적 회상 인터뷰를 함께 사용해 검증한다.

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 결과 인과 설명
- 세계일정의 현재 단계와 다음 진행 이해
- 같은 UID 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

두 증거가 충돌하면 통과를 보류하고 원인을 수정한 뒤 재검증한다.

## 9. 콘텐츠·역사 상태

- 사건 연대기 세트·수집가: 승인된 장기 보조 시스템
- 명예의 전당: 비경쟁 작품 아카이브, `FUTURE_CONTENT_HOLD`
- 경쟁 랭킹·점수·시즌 보상: 폐기된 방향
- MVP-001·002·003: 과거 구현·자동 검증 기준선
- MVP-003: `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`
- `+5/+10` 판단과 단일 날짜 결과: 역사 연구 체크포인트이며 최신 데모 종료 구조가 아님
- 과거 PASS: 최신 R2 제품 PASS가 아님

## 10. 감사·동기화 상태

- PR #94: R1 canon baseline squash merged
- PR #96·#97: post-merge authority·Sheet sync state squash merged
- PR #98: R1 최종 승인·세계일정 구조 squash merged
- PR #99: R2 체크포인트 001·Base 어댑터 복구 squash merged
- R1 정본 감사: P0 `0`, P1 `0`
- R2 체크포인트 001 감사: P0 `0`, P1 어댑터 권위 드리프트 `RESOLVED`
- GitHub·Google Sheet 정본 정렬: `COMPLETE / MERGED_PR99 / MAIN_CANON / READBACK_PASS`
- 사용자 R1 최종 검수: `APPROVED / BS-OPS-20260803-05`
- R2 첫 기간 프리셋: `APPROVED / BS-WORLD-20260803-02`
- PR #99 자동 검증: `5 WORKFLOWS PASS`
- PR #99 리뷰 상태: `COMMENTS_0 / THREADS_0 / P0_0 / P1_0`
- 최신 제품 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`
- 제품 구현: `BLOCKED`

## 11. 다음 Gate

1. R2 Grill Me 2 — 날짜별 진행 화면에서 개입 가능일과 관찰일을 구분
2. 날짜별 정보량·작품 기여·위험·다음 갱신·대응 선택 계약 확정
3. 새 승인 카운터는 `0/10`에서 시작
4. 제품 구현은 R1~R8과 최종 사용자 검수 전까지 시작하지 않음
