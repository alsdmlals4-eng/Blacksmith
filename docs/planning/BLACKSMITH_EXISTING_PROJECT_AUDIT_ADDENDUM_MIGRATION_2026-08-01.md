# Blacksmith 기존 프로젝트 감사 보완 — v9 데이터 마이그레이션

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A5`
>
> Decision ID: `BS-MIGRATION-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_OPEN`
>
> 기준일: `2026-08-01`

## 1. 직접 충돌 증거

현행 main의 제작 등급 데이터는 다음 구형 5단계를 사용한다.

```text
APPRENTICE / 미숙한
STANDARD / 평범한
REFINED / 정교한
MASTERWORK / 명품
PERFECT / 완벽한
```

현행 main의 강화 이정표는 +10 slot1 추가, +20 slot1 강화, +30 slot2 추가, +40 slot2 강화, +50 slot3 추가 후 +100까지 세 슬롯을 반복 강화한다.

최신 정본은 다음과 다르다.

```text
NORMAL / 보통
SUPERIOR / 우수
EXQUISITE / 명품
MASTERPIECE / 걸작
LEGENDARY / 전설

계보 1개 + 보조 최대 2개
+49→+50 일반 정밀 / 고위 정밀
```

## 2. 해결된 기획 목표

`BS-MIGRATION-20260801-01`로 다음을 확정했다.

- 제작 등급의 순위 보존 1:1 ID 변환
- 기존 score·공격·가치 배율과 확률 분포의 호환 보존
- 마감 판정과 제작 등급 필드 분리
- 구형 slot1→계보, slot2→보조1, slot3→보조2
- +50 이상 구형 장비에 `LEGACY_GENERAL_PRECISION` provenance 부여
- 고위 정밀 특수 수식어·진화 소급 지급 금지
- 장비 UID·강화 단계·소유권·연대기 보존
- 캠페인 전체 원자 마이그레이션과 실패 시 원본 보존
- 마이그레이션 멱등성·fixture·0허용오차 지표

## 3. Finding 판정

| Finding | 기획 목표 | 런타임·데이터 |
|---|---|---|
| `BS-AUD-F04` | RESOLVED | OPEN |
| `BS-AUD-F05` | MIGRATION TARGET RESOLVED | OPEN |
| `BS-AUD-F20` | MIGRATION TEST TARGET RESOLVED | OPEN |

P0·P1 Finding 수는 실제 JSON·GDScript·fixture·validator·SaveMigrator 변경과 자동 검증 전까지 줄이지 않는다.

## 4. 적대적 실패 조건

```text
등급 순위 변경
저장된 배율·점수 변경
수식어 삭제·재추첨
구형 +50에 고위 정밀 보상 소급 지급
장비 UID 변경
동일 migration 두 번 적용
일부 장비만 변환된 캠페인 저장
실패 시 원본 덮어쓰기
```

하나라도 발생하면 마이그레이션 실패다.

## 5. 직접 영향 파일

- `data/crafting/craftsmanship_grades.json`
- `data/crafting/enhancement_milestones.json`
- `data/crafting/affixes.json`
- `scripts/forging/craftsmanship_grade_resolver.gd`
- `scripts/enhancement/enhancement_session.gd`
- 장비 생성·보관·고객 적합도·세계 Registry
- 제작·강화·장비 생애 테스트와 fixture
- `BS-SAVE-20260801-01`의 SaveMigrator

## 6. 상태

```text
MIGRATION_DESIGN: COMPLETE
CROSS_SOURCE_SYNC: PENDING
PRODUCT_DATA_CHANGE: NOT_RUN
SAVE_MIGRATOR: NOT_RUN
AUTOMATED_TESTS: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
