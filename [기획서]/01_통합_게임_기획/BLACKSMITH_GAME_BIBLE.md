# [부분 대체됨] Blacksmith 통합 게임 기획서 — R1 역사 진입점

> 현재 구현·후속 기획의 직접 기준으로 사용하지 마십시오.
>
> 이 경로의 이전 본문은 Git 이력 `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`에 역사 증거로 보존됩니다.

## 현재 정본

1. `CURRENT_CONFIRMED_DECISIONS.md`
2. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
3. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
4. `[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md`

## 대체된 범위

다음 R1 서술은 현재 정본이 아닙니다.

- `일반 수식어 A·B`
- 일반 수식어 슬롯 두 개
- 보조재료 슬롯
- 정밀 등급 1개와 일반 수식어 두 개 구조
- 모든 일정의 고정 3일 결과·4일 재방문
- 제작 완료 시 촉매·연대기뿐 아니라 모든 수식어가 비어 있다는 해석

현재 작품 수식어는 정확히 다음 세 슬롯입니다.

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

현재 장비명:

```text
[등급 수식어] 촉매 수식어 기본 작품명 - 연대기 수식어
```

현재 책임 문서:

- `docs/planning/BLACKSMITH_R2_PRECISION_ENHANCEMENT_METHOD_AND_CATALYST_STRUCTURE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CATALYST_AFFIX_SEED_EVOLUTION_AND_MUTATION_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_THREE_AFFIX_SLOT_ARCHITECTURE_CANON_2026.md`
- `docs/planning/BLACKSMITH_R2_CHRONICLE_AFFIX_DETAIL_INTERACTION_CANON_2026.md`

## 유지되는 R1 원칙

- 강화의 성공·실패와 멈춤·추가 도전이 즉각 반복 재미다.
- 작품은 UID와 생애를 가진다.
- 고객과 세계 결과는 다음 강화·복원·제작 이유를 돌려준다.
- 피로도는 제한된 하루의 작업 우선순위 자원이다.
- 일반 실패는 작품 역사를 자동 삭제하지 않는다.
- 제품 구현은 R1~R8와 최종 사용자 검수 전까지 `BLOCKED`다.

문서 상태의 기계 판독 기준은 `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`을 사용합니다.
