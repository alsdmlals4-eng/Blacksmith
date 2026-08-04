# [현재 정본] Blacksmith 시작 지점

## 프로젝트 약속

> 한 명의 대장장이가 제한된 하루 작업량 안에서 작품을 만들고, 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 작품이 고객과 세계에서 겪은 생애와 결과를 돌려받는 Android 세로형 제작 게임.

## 현재 상태

```yaml
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R1_STATUS: USER_APPROVED / HISTORICAL_BASELINE / R2_REFINED
R2_STATUS: CHECKPOINT_003_CANON / CANON_AUDIT_COMPLETE_WITH_OPEN_USER_DECISIONS
R2_CHECKPOINT_003_PR: 103
R2_CHECKPOINT_003_MERGE: 674ee21013cb5d41f89a1a3f3b10ecfc31238295
R2_CHECKPOINT_003_CLOSURE_PR: 104
R2_CHECKPOINT_003_CLOSURE_MERGE: d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9
CANON_AUDIT: BS-OPS-20260804-02 / BS-ADV-20260804-01
NEXT_APPROVAL_COUNTER: 0/10
PRODUCT_IMPLEMENTATION: BLOCKED
```

위 SHA는 완료된 체크포인트의 불변 병합 증거이며 이 파일 자신의 현재 Git commit을 예측하지 않는다.

## 처음 읽을 순서

1. `AGENTS.md`
2. `CURRENT_CONFIRMED_DECISIONS.md`
3. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
4. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
5. `ACTIVE_CONTEXT.md`
6. `DEVELOPMENT_GATES.md`
7. `ROADMAP.md`
8. `DOCUMENTATION_MAP.md`
9. `DESIGN_DOCUMENT_REGISTRY.json`
10. 필요한 분야별 최신 R2 정본
11. 실제 구현·data·tests — 역사 구현과 현재 제품 상태를 구분

구형 파일의 상태는 `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`에서 확인한다.

## 현재 핵심 규칙

- 현재 검증 상한은 `+50`, 정밀 이정표는 `+10/+20/+30/+40/+50`이다.
- 장기 최종 강화 상한은 사람 플레이 이후 결정한다.
- 일반 강화는 한 입력에 한 결과다.
- 정밀강화는 `주재료 맥락 + 강화 방식 + 촉매 한 개`다.
- 보조재료 슬롯은 없다.
- 작품 수식어는 정확히 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 개다.
- 제작 완료 시 등급 수식어가 생성되고 촉매·연대기 수식어는 비어 있다.
- 등급 수식어는 동일 UID에서 고정된다.
- 촉매 수식어는 현재·누적 촉매 이력으로 확률적으로 성장한다.
- 연대기 수식어는 실제 작품 생애 기록으로 생성·진화한다.
- 세 수식어는 서로 생성·진화·덮어쓰기 하지 않는다.
- 장비명은 `[등급] 촉매 수식어 기본 작품명 - 연대기 수식어` 순서다.
- 연대기 수식어를 누르면 UID 기반 읽기 전용 상세를 확인한다.
- 작품은 UID·소유자·손상·복원·사건·계승·재방문 기록을 유지한다.
- 일반 실패와 대파는 작품 생애를 자동 삭제하지 않는다.
- 완전 파괴는 명시적이고 충분히 고지된 선택에서만 허용하며 역사 기록은 남긴다.
- 피로도·날짜는 작업 우선순위와 고객·세계 결과의 공통 축이다.
- 고객 개인 일정과 특정 날짜 예고형 세계 일정을 분리한다.
- 과거 고정 날짜 프리셋은 범용 상태 머신이 아니다.
- 정확한 경제·확률·기간 수치는 버전형 테스트 프리셋이다.
- 코어 재미는 행동 증거와 중립적 회상 인터뷰를 함께 사용해 검증한다.

## 첫 코어 버티컬 슬라이스 방향

```text
플레이어 선택 작품 한 점 제작
→ 제작 등급과 등급 수식어
→ 일반 강화와 멈춤·추가 도전
→ +10/+20/+30/+40/+50 정밀강화
→ 촉매 수식어 형성·성장
→ 고객 납품
→ 개인 일정 또는 세계 일정
→ 연대기 수식어 형성 가능성
→ 같은 UID 재방문
→ 손상·복원·재강화·후속 판단
```

현재는 기획 단계이며 버티컬 슬라이스 제품 구현은 승인되지 않았다.

## 역사 구현 기준선

- MVP-001·002·003은 과거 구현·자동 검증 증거다.
- MVP-003은 `REFERENCE_IMPLEMENTATION / HISTORICAL_EVIDENCE / HOLD`다.
- 과거 정확한 수치는 `LEGACY_IMPLEMENTED_VALUE`이며 최신 제품 확정값이 아니다.
- 과거 PASS는 최신 runtime·Android·접근성·성능·사람 플레이 PASS를 의미하지 않는다.
- 최신 제품 검증은 모두 별도 Gate에서 다시 수행한다.

## PR·감사 상태

- PR #103: `MERGED_R2_CHECKPOINT_003_CANON`
- PR #104: `MERGED_POSTMERGE_CLOSURE`
- PR #105: `CANON_ADVERSARIAL_AUDIT / VALIDATION_ACTIVE`
- PR #81: `[역사 증거] / 전체 병합 [폐기] / 선별 이관 [보류]`
- Audit: `BS-ADV-20260804-01`
- P0: `0`
- P1 총 발견: `9`
- P1 문서·권위 해결: `8`
- P1 사용자 Decision 필요: `1`
- 제품 경로 변경: `0`

## 열린 사용자 Decision

1. 제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 분리
2. 연대기 수식어 효과 책임
3. 작품 소유권 상태 머신
4. 긴 조합 장비명 표시
5. 첫 작품 정체성 보상 시점
6. 완전 파괴와 작품 애착 검증
7. PR #81 선별 이관 순서

첫 번째가 열린 P1이며 나머지는 P2 후속 기획 후보다.

## 다음 Gate

1. PR #105 exact-head 검증·Sheet 동기화·병합
2. 다음 R2 승인 배치를 `0/10`에서 재개
3. 제품 구현은 계속 `BLOCKED`
