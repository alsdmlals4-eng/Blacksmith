# Blacksmith Decision Ledger Addendum 22

> Decision ID: `BS-GRADE-20260801-02`
>
> 기준일: `2026-08-01`
>
> 상태: `USER_APPROVED / SYNCED_TO_DRAFT / CROSS_SOURCE_VERIFIED`
>
> 추적: Issue #79 / Draft PR #81

## 결정

제작 등급을 다음 5단계로 고정한다.

```text
보통 → 우수 → 명품 → 걸작 → 전설
```

## 적용 범위

- 제작 등급 축만 변경한다.
- `양질`은 제거한다.
- `전설`은 최상위 제작 등급으로 추가한다.
- 강화 단계·계보·보조·+50 경로·운명 상태는 변경하지 않는다.
- 전설 제작 등급만으로 다른 시스템을 자동 해금하지 않는다.

## 대체 관계

```text
BS-GRADE-20260801-01: SUPERSEDED
BS-GRADE-20260801-02: CURRENT
```

`BS-V9-20260731-01`의 `보통→양질→우수→명품→걸작` 결정도 계속 역사 상태로 보존한다.

## 구현 경계

이번 결정은 기획 정본화이며 제품 코드·Scene·런타임 데이터는 변경하지 않는다.

다음은 P0-2에서 별도 승인한다.

- 내부 ID 5개
- 구형 ID 5개 변환표
- 분포·배율
- 고객 적합도 점수
- 저장 마이그레이션
- fixture·validator·회귀 테스트

## 동기화 위치

```text
02_현재_확정결정!A24:H24
04_누락_충돌_감사!A18:H18
05_GDD_요약!A4:H4
40_핵심시스템_메인콘텐츠!A8:H8
99_변경이력!A20:H20
CROSS_SOURCE_VERIFICATION: PASS
```
