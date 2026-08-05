# [현재 정본] Blacksmith 시작 지점

## 프로젝트 약속

> 제한된 하루 작업량 안에서 작품을 만들고 강화 위험 앞에서 멈출지 더 도전할지 선택하며, 같은 UID 작품이 고객과 세계에서 겪은 생애 결과를 돌려받는 Android 세로형 제작 게임.

```yaml
WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R2_CORE_SESSION_META_LOOP
R2_CHECKPOINT_003: PR103 / CLOSURE_PR104 / CANON_AUDIT_PR105
R2_STATUS: BATCH_004_ACTIVE_2_OF_10
CURRENT_DECISIONS: BS-CRAFT-20260804-07 / BS-CRAFT-20260805-01 / BS-OPS-20260805-01
PRODUCT_IMPLEMENTATION: BLOCKED
```

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
10. 분야별 최신 정본
11. 실제 구현·data·tests — 역사 구현과 현재 제품 상태 구분

## 현재 규칙

```text
제작 등급: [보통] → [우수] → [명품] → [걸작] → [전설]
예술성: 0 이상의 정수 / 고정 설계 최대치 없음 / 예술성 27
수식어: GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

- 제작 등급은 최초 직접 단조 완료 시 확정하고 동일 UID에서 고정
- `전설`은 출생 극희귀 결과이며 후천 승격 없음
- 예술성은 다른 무기 능력치와 같은 원수치이며 분모·별점·백분율·단계명이 없음
- 예술성 0은 미완성품이 아니라 미적 투자가 거의 없는 정상 기능품
- 제작 등급은 예술성의 고정 상한을 만들지 않음
- 예술성은 전투력을 기본적으로 올리지 않고 범용 속성·수식어 배율이 아님
- 일반 강화는 한 입력에 한 결과
- 정밀강화는 주재료 맥락 + 강화 방식 + 촉매 한 개
- 연대기 수식어를 누르면 UID 기반 읽기 전용 상세
- 보조재료 슬롯과 일반 수식어 A·B는 현재 구조 아님

## 운영 규칙

- 질문·추천·설계 전 벤치마킹·현업 비교
- 승인 10건은 최대 배치 크기
- `HIGH_RISK_CONFLICT / SESSION_END / LARGE_CANON_IMPACT` 조기 체크포인트
- 작업마다 `RED → GREEN → REFACTOR` TDD
- 명시적 사용자 승인 전 병합 금지

## 이번 정제 검증

- RED commit: `3b08260dcfeeb1d97900949b04395f15a29d74d0`
- Planning-first run `65`: expected failure
- Base run `532`: PASS
- GREEN candidate Planning-first run `78`: PASS
- 최종 exact-head Python·Godot 검증: `PENDING`
- 현재 5등급·예술성 제품 구현: `NOT_STARTED / BLOCKED`
- runtime·Android·접근성·성능·사람 플레이: `NOT_RUN`

## 구형 문서

상태 원장: `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`.

- 이전 4등급 문서: `[대체됨]`
- 초기 bounded 예술성 모델과 named tier: `[대체됨]`
- 과거 3등급 runtime: `[역사 증거]`
- PR #81 전체 병합: `[폐기]`, 선별 이관: `[보류]`
