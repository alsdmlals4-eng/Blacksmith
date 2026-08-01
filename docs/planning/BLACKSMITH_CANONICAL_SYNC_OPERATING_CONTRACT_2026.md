# Blacksmith 기획 정본 즉시 동기화 운영 계약

> Decision ID: `BS-SYNC-20260731-01`
>
> 상태: `USER_APPROVED / CURRENT_OPERATING_CONTRACT`
>
> 승인일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 구현 권한: `NONE`

## 1. 사용자 승인 규칙

앞으로 주요 변경사항과 사용자 승인 내용은 대화에만 남기지 않는다.

승인 직후 다음 대상을 함께 찾아 같은 Decision ID로 반영한다.

```text
GitHub 권위 Markdown
+ GitHub 계획 데이터 JSON
+ 문서 권위 지도
+ 연결 Google Sheet 결정 인덱스
+ 직접 영향 GDD 탭
+ 감사 기록
+ 변경이력
```

## 2. 즉시 동기화 대상

- 프로젝트 코어·제품 정의·범위
- 새 시스템과 핵심 규칙
- 콘텐츠 구조와 대표 Vertical Slice
- 주요 UX 흐름·정보 위계·접근성
- 강화·경제·확률·보호·저장·장비 생애주기
- 플랫폼·출시·서버·랭킹·개인정보·운영 정책
- 사용자가 명시적으로 승인한 권장안

## 3. Decision ID 규칙

- 서로 독립적인 결정은 서로 다른 ID를 사용한다.
- 같은 결정의 Markdown·JSON·Sheet·감사·변경이력에는 같은 ID를 사용한다.
- ID는 결정 의미가 바뀌지 않는 한 변경하지 않는다.
- 기존 결정을 대체하면 새 ID를 만들고 이전 ID를 `supersedes`로 연결한다.

권장 형식:

```text
BS-<DOMAIN>-YYYYMMDD-NN
```

## 4. 동기화 상태

| 상태 | 의미 |
|---|---|
| `GITHUB_DRAFT_COMMITTED` | GitHub 계획 브랜치에 정본과 데이터가 커밋됨 |
| `SYNCED_TO_DRAFT` | Sheet가 PR·브랜치 커밋을 명시해 동기화됨 |
| `SYNCED_TO_MAIN` | 병합 커밋 기준으로 Sheet가 재확인됨 |
| `PARTIAL_SYNC_BLOCKED` | 일부 대상이 실패했고 누락 위치가 기록됨 |
| `CROSS_SOURCE_VERIFIED` | GitHub와 Sheet를 재조회해 일치 확인함 |

Draft 상태를 main 병합 상태로 표시하지 않는다.

## 5. 실행 순서

```text
승인 결정 확인
→ 영향 문서·데이터·Sheet 범위 재조회
→ Decision ID 할당
→ GitHub 권위 문서·계획 데이터 커밋
→ 같은 ID로 Sheet 결정·영향 탭·감사·이력 갱신
→ GitHub·Sheet 재조회
→ 변경 위치·커밋·검증 결과 보고
```

## 6. 기록 의무

각 동기화에는 최소 다음을 남긴다.

- Decision ID
- 승인일과 승인 주체
- 결정 요약
- GitHub 파일 경로
- 계획 데이터 경로
- PR·브랜치·커밋
- Sheet 문서와 정확한 범위
- 동기화 상태
- 재검증 결과
- 대체하거나 충돌한 이전 결정

## 7. 기존 일괄 전파 계획과의 관계

기존 `기획 완료 후 Google Sheet 전체 동기화` 규칙은 **구형 정본 전체 정리와 대규모 탭 재작성**에 적용한다.

새 승인 결정의 인덱스와 직접 영향 범위는 이 계약에 따라 즉시 동기화한다.

따라서:

- 승인 결정을 Sheet에서 장기간 누락하는 것은 금지한다.
- 아직 병합되지 않은 내용은 `SYNCED_TO_DRAFT`로 명시한다.
- 역사 문서 전체를 즉시 재작성할 필요는 없다.
- 병합 후 같은 ID의 커밋·상태를 `SYNCED_TO_MAIN`으로 갱신한다.

## 8. 오류 처리

- Sheet 쓰기 전 현재 셀을 다시 읽는다.
- 텍스트가 `+`로 시작하면 문자열로 기록해 수식 해석을 막는다.
- 실패한 범위만 재시도한다.
- 일부 실패를 전체 성공으로 보고하지 않는다.
- 제품 코드·Scene·게임 데이터·에셋 변경과 섞지 않는다.

## 9. 현재 적용

이 계약은 다음 결정 묶음에 최초 적용한다.

- `BS-V9-20260731-01` 제작 등급
- `BS-V9-20260731-02` 수식어 구조
- `BS-V9-20260731-03` 10단위 이정표
- `BS-V9-20260731-04` 고객 거래 자격·공개 적합도
- `BS-V9-20260731-05` 장비 운명 상태
- `BS-V9-20260731-06` 수집가 증명 세트
- `BS-V9-20260731-07` 명작 전당
- `BS-V9-20260731-08` 벤치마킹 선행 원칙
- `BS-SYNC-20260731-01` 본 즉시 동기화 계약

## 10. 계약 상태

```text
IMMEDIATE_CANONICAL_SYNC: REQUIRED
SAME_DECISION_ID_ACROSS_SOURCES: REQUIRED
CHANGE_LOCATION_AND_COMMIT_LOG: REQUIRED
SHEET_DRAFT_STATE_DISCLOSURE: REQUIRED
BULK_LEGACY_REWRITE: SEPARATE_GATED_OPERATION
PRODUCT_IMPLEMENTATION: NOT_AUTHORIZED
```