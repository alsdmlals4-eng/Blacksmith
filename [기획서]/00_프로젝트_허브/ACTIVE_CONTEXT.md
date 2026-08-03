# Active Context

- 갱신: `2026-08-03 21:22 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R2_CORE_SESSION_META_LOOP / PLANNING_ACTIVE`
- R1 최종 승인: `BS-OPS-20260803-05 / USER_APPROVED / CANON_COMPLETE`
- R1 정본 기준 병합: PR `#94`
- R1 정본 기준 SHA: `8a0956d6c8b4cf3db545a17d0bd002ba8354d568`
- post-merge 상태 최종화: PR `#96/#97`
- Sheet 동기화 기준: `BS-OPS-20260803-04 / MAIN_CANON / READBACK_PASS`
- R1 감사: `BS-OPS-20260803-02 / P0=0 / P1=0`
- 세계일정: `BS-WORLD-20260803-01 / DAILY_STAGED_PROGRESS / SCALE_INCREASES_DURATION`
- 명예의 전당: `FUTURE_CONTENT_HOLD / NONCOMPETITIVE_ARCHIVE`
- 제품 구현: `BLOCKED`

## 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품 한 점을 직접 만들고, 강화의 위험 앞에서 멈출지 더 도전할지 선택하며, 그 작품이 다른 사람과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

```text
직접 제작
→ 한 결과씩 강화
→ 멈춤·추가 도전 판단
→ +10 단위 정밀강화
→ 방문 고객 인계
→ 즉시 사용 계획·초기 인과 피드백
→ 날짜마다 세계일정 한 단계 진행
→ 별도 날짜의 최종 결과
→ 같은 UID 생애·재방문
→ 복원·재강화·다음 목표
```

- 순간 동력: 강화 결과와 멈춤·도전 판단
- 장기 의미: 작품의 소유자·손상·복원·사건·계승·연대기가 날짜에 걸쳐 돌아오는 것

## 현재 핵심 시스템

1. 직접 단조·영구 출생 품질
2. 일반 강화·한 입력 한 결과
3. `+10/+20/+30/+40/+50` 정밀강화
4. 일반 수식어 A·B
5. 활성 사건·연대기 수식어 한 개와 진화 이력
6. UID 기반 작품 생애주기
7. 방문 고객 인계·즉시 사용 계획과 초기 인과 피드백
8. 날짜별 세계일정 중간 진행·최종 결과·재방문
9. 피로도·날짜 우선순위
10. 버전형 경제·세계일정 기간 테스트 프리셋

## 확정된 경계

- 현재 검증 상한은 `+50`; 최종 상한은 `DEFERRED`다.
- `+5/+10`은 역사 PoC 체크포인트이며 최신 데모 종료점이 아니다.
- 일반 수식어는 두 개이며 사건 수식어는 별도 한 개다.
- 손상·대파는 UID와 생애를 유지하고 복원 가능하다.
- 수식어는 삭제보다 잠금·복원을 따른다.
- 완전 파괴는 명시적 선택만 허용하며 역사 기록은 남긴다.
- 정확한 비용·확률·피로도·보상·세계일정 기간은 테스트 프리셋이다.
- 세계일정은 발생 당일 또는 첫 날짜 진행 한 번으로 최종 해결되지 않는다.
- 세계일정은 최소 하나의 중간 상태를 거치며 규모가 클수록 더 오래 걸린다.
- 날짜 경과만으로 사건 수식어가 자동 성장하지 않는다.
- 명예의 전당은 순위 없는 미래 아카이브다.

## 강화 데이터 권위

- `data/crafting/enhancement_balance.json`: 현재 구현의 비용·확률·실패·위험·단계 하락·파괴 비율과 소비 정책
- `data/crafting/enhancement_milestones.json`: 현재 구현의 정밀강화 이정표·보상 정의
- 기획 의미는 최신 Decision과 Game Bible이 소유하며, 정확한 구현값은 data·tests의 역사 증거 또는 테스트 프리셋으로 분류한다.

## 첫 코어 버티컬 슬라이스

```text
플레이어 선택 작품 한 점 제작
→ +10/+20/+30/+40/+50
→ 방문 고객 납품
→ 즉시 사용 계획·초기 피드백
→ 날짜 1: 준비·초기 진행
→ 날짜 2+: 중간 변화·전환점
→ 별도 날짜: 최종 결과
→ 같은 UID 재방문
→ 손상·복원·재강화 판단
```

다른 작품군은 제한된 비플레이 미리보기로만 제공한다.

## 세계일정 진행 계약

- 하루 종료 한 번당 최대 한 단계 또는 한 개의 명시적 진행 단위만 전진한다.
- 발생 상태·하나 이상의 중간 상태·별도 날짜의 최종 상태가 필수다.
- 상대 기간은 `LOCAL/PERSONAL < REGIONAL/FACTION < REALM/NATIONAL < WAR/CATASTROPHE`다.
- 날짜별 진행은 현재 단계·경과 날짜·다음 갱신·작품 기여·새 위험·대응 가능성을 보여준다.
- 빈 대기 로그·필수 장문 대화·날짜 넘기기 최적화를 금지한다.
- 정확한 기간·단계·동시 진행 수·분기는 R2~R4에서 확정한다.

## 코어 재미 검증

행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 결과 인과 설명
- 세계일정의 현재 단계와 다음 진행 이해
- 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

직후 중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류하고 최소 수정 후 재검증한다.

## 역사 구현·보조 기능 추적

- `POC v0.6.4 · main · 2026.07.23.1`: 제작 품질 역사 구현 기준선
- 자동 검증 기록: `제작 모델 7건`, `통합 6건`
- MVP-001~003: `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`
- 과거 `+11` 단계 하락·`+30` 파괴·단일 날짜 결과: `LEGACY_IMPLEMENTED_VALUE`
- `자동 단조`: 저위험 반복 편의 기능이며 중요 판단을 자동 통과하지 않음

## 정본·PR 상태

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `docs/planning/BLACKSMITH_R1_FINAL_APPROVAL_AND_WORLD_SCHEDULE_PROGRESS_2026.md`
- `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Core Resolution `01~06`
- PR #94: `MERGED_CANON_BASELINE`
- PR #96: `MERGED_POST_MERGE_FINALIZATION`
- PR #97: `MERGED_SHEET_SYNC_GATE_CLOSURE`
- PR #81: `REFERENCE_ASSET / OPEN_DRAFT / DO_NOT_MERGE_AS_UNIT`
- PR #95·#86·#61: 종료 또는 역사 전용

## 실제 검증 상태

- PR #94·#96·#97 Base CI: `PASS`
- PR #94·#96·#97 PR validation: `PASS`
- GitHub·Google Sheet 정본 동기화: `COMPLETE / READBACK_PASS`
- 최신 R2 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 다음 작업

1. R2 `Core·Session·Meta Loop` 기획
2. 첫 세계일정의 규모·기간·단계·날짜별 UI·개입 규칙 확정
3. 제품 구현은 계속 `BLOCKED`