# Active Context

- 갱신: `2026-08-03 09:25 KST`
- Work Mode: `TOTAL_PLANNING`
- 단계: `R1_PROJECT_CORE_AND_PLAYER_PROMISE / USER_FINAL_REVIEW_PENDING`
- R1 정본 기준 병합: PR `#94`
- R1 정본 기준 SHA: `8a0956d6c8b4cf3db545a17d0bd002ba8354d568`
- R1 감사: `BS-OPS-20260803-02 / P0=0 / P1=0`
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
→ 즉시 인과 결과
→ 날짜·세계일정
→ 같은 UID 생애·재방문
→ 복원·재강화·다음 목표
```

- 순간 동력: 강화 결과와 멈춤·도전 판단
- 장기 의미: 작품의 소유자·손상·복원·사건·계승·연대기가 돌아오는 것

## 현재 핵심 시스템

1. 직접 단조·영구 출생 품질
2. 일반 강화·한 입력 한 결과
3. `+10/+20/+30/+40/+50` 정밀강화
4. 일반 수식어 A·B
5. 활성 사건·연대기 수식어 한 개와 진화 이력
6. UID 기반 작품 생애주기
7. 방문 고객 인계·즉시 인과 결과
8. 지연된 세계 환류·재방문
9. 피로도·날짜 우선순위
10. 버전형 경제 테스트 프리셋

## 확정된 경계

- 현재 검증 상한은 `+50`; 최종 상한은 `DEFERRED`다.
- `+5/+10`은 역사 PoC 체크포인트이며 최신 데모 종료점이 아니다.
- 일반 수식어는 두 개이며 사건 수식어는 별도 한 개다.
- 손상·대파는 UID와 생애를 유지하고 복원 가능하다.
- 수식어는 삭제보다 잠금·복원을 따른다.
- 완전 파괴는 명시적 선택만 허용하며 역사 기록은 남긴다.
- 정확한 비용·확률·피로도·보상·간격은 테스트 프리셋이다.
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
→ 즉시 결과
→ 날짜·세계일정
→ 같은 UID 재방문
→ 손상·복원·재강화 판단
```

다른 작품군은 제한된 비플레이 미리보기로만 제공한다.

## 코어 재미 검증

행동 증거:

- 강화 지속·중단 고민
- 일반 수식어 A·B와 주요 선택 기억
- 결과 인과 설명
- 재방문 후 자발적 다음 행동
- 피로도·날짜 우선순위 사용
- 손상·복원의 생애 의미 이해

직후 중립적 회상 인터뷰가 행동과 충돌하면 통과를 보류하고 최소 수정 후 재검증한다.

## 역사 구현·보조 기능 추적

- `POC v0.6.4 · main · 2026.07.23.1`: 제작 품질 역사 구현 기준선
- 자동 검증 기록: `제작 모델 7건`, `통합 6건`
- MVP-001~003: `REFERENCE_IMPLEMENTATION / HISTORICAL_POC`
- 과거 `+11` 단계 하락·`+30` 파괴: `LEGACY_IMPLEMENTED_VALUE`
- `자동 단조`: 저위험 반복 편의 기능이며 중요 판단을 자동 통과하지 않음

## 정본·PR 상태

- `CURRENT_CONFIRMED_DECISIONS.md`
- `docs/planning/CURRENT_R1_CANON_REGISTRY.json`
- `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- `[기획서]/00_프로젝트_허브/ROADMAP.md`
- Core Resolution `01~06`
- PR #94: `MERGED_CANON_BASELINE`
- PR #81: `REFERENCE_ASSET / OPEN_DRAFT / DO_NOT_MERGE_AS_UNIT`
- PR #95·#86·#61: 종료 또는 역사 전용

## 실제 검증 상태

- PR #94 Base CI: `PASS`
- PR #94 PR validation: `PASS`
- 최신 R1 runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 다음 작업

1. Google Sheet를 PR #94 병합 SHA로 최종화
2. 사용자 R1 정본 최종 검수
3. 승인 후 R2 기획
4. 제품 구현은 계속 `BLOCKED`
