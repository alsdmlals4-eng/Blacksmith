# Blacksmith 기존 프로젝트 감사 Addendum — 제작 등급 4단계

> Audit Addendum ID: `BS-REPO-AUDIT-20260801-01-GRADE-A1`
>
> 관련 Finding: `BS-AUD-F04`, `BS-AUD-F20`
>
> 관련 결정: `BS-GRADE-20260801-01`
>
> 상태: `PLANNING_TARGET_RESOLVED / RUNTIME_MIGRATION_OPEN`
>
> 구현 권한: `NONE`

## 1. 변경된 목표 정본

기존 감사 보고서의 `BS-AUD-F04`에서 비교 대상으로 사용한 5단계 기획은 다음 4단계 최신 결정으로 대체한다.

```text
보통 → 우수 → 명품 → 걸작
```

`양질`은 현행 제작 등급에서 제거한다.

## 2. Finding 판정

```text
BS-AUD-F04_RULE_TARGET: RESOLVED_BY_BS-GRADE-20260801-01
BS-AUD-F04_RUNTIME_CONFLICT: OPEN
BS-AUD-F20_TEST_MIGRATION: OPEN
```

Finding 수를 줄이지 않는다. 실제 main은 여전히 다음 구형 5개 ID를 사용한다.

```text
APPRENTICE / STANDARD / REFINED / MASTERWORK / PERFECT
```

따라서 해결해야 할 범위는 오히려 명확해졌다.

- 5개 구형 ID → 4개 신규 ID 변환
- 기존 저장 장비의 등급 보존
- 제작 분포 변환
- 공격력·가치 배율 변환
- 고객 적합도 점수 변환
- fixture·validator·단위·통합 테스트 변환

## 3. 금지되는 임시 해결

- `양질` 텍스트만 삭제하고 배열 인덱스를 그대로 사용
- 구형 `MASTERWORK`를 새 걸작과 같은 의미로 간주
- 기존 장비 등급 재추첨
- 저장 스키마 버전 없이 묵시적 변환
- 고객 점수와 테스트는 구형 ID를 사용하면서 UI만 4단계 표시
- 구형 등급을 알 수 없다는 이유로 전부 보통으로 변환

## 4. 다음 승인 필요 항목

다음은 아직 사용자 승인 전이다.

1. 신규 내부 등급 ID 4개
2. 구형 5개 ID의 결정론적 변환표
3. 기존 저장 작품의 경계 사례 처리
4. 확률·공격력·가치 배율의 초기값

이 항목은 P0-2 마이그레이션 설계에서 대안 비교 후 승인한다.
