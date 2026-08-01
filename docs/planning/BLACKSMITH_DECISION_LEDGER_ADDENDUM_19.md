# Blacksmith Decision Ledger Addendum 19

> Decision ID: `BS-SYNC-20260731-01`
>
> 상태: `USER_APPROVED / CURRENT`
>
> 승인일: `2026-07-31`
>
> 상위 계약: `BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md`

## 승인 결정

주요 변경사항과 승인된 내용은 즉시 기획 정본 동기화 대상으로 처리한다.

동일한 Decision ID를 다음에 사용한다.

- GitHub 권위 문서
- GitHub 계획 데이터
- 문서 권위 지도
- 연결 Google Sheet 결정 인덱스와 직접 영향 탭
- 감사 기록과 변경이력

각 동기화는 변경 위치, PR·브랜치·커밋, Sheet 범위, 재검증 상태를 남긴다.

## 권한 판정

이 결정은 기존의 `기획 완료 후에만 Sheet 전체 전파` 규칙을 다음처럼 좁혀 해석한다.

- 새 승인 결정의 인덱스·직접 영향 범위: 즉시 동기화
- 구형 문서 전체 재작성·Sheet 전체 정리: 별도 일괄 전파 Gate 유지

병합 전 Sheet에는 `SYNCED_TO_DRAFT`, 병합 후에는 같은 Decision ID로 `SYNCED_TO_MAIN`을 기록한다.

## 금지

- 승인 내용을 대화 또는 한 문서에만 남김
- GitHub와 Sheet에서 서로 다른 ID 사용
- Draft 커밋을 main 병합 커밋으로 표시
- 동기화 실패 위치를 기록하지 않음
- 제품 구현과 기획 정본 동기화를 같은 변경으로 처리

## 전파 대상

- `BLACKSMITH_CANONICAL_SYNC_OPERATING_CONTRACT_2026.md`
- `BLACKSMITH_V9_CANONICAL_DECISION_SET_2026.md`
- `docs/planning/data/blacksmith_v9_canonical_decision_set_2026.json`
- `DOCUMENTATION_MAP.md`
- `PROJECT_GOOGLE_SHEET_WORKBOOK.md`
- Google Sheet `00`, `01`, `02`, 직접 영향 GDD 탭, `04`, `05`, `99`

## 상태

```text
DECISION: ACCEPTED
CANONICAL_SYNC: REQUIRED
SHEET_STATUS_BEFORE_MERGE: SYNCED_TO_DRAFT
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```