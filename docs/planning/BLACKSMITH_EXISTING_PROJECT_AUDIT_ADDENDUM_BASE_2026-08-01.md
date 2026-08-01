# Blacksmith 기존 프로젝트 감사 보완 — Base 운영 무결성

> Addendum ID: `BS-REPO-AUDIT-20260801-01-A4`
>
> Audit ID: `BS-BASE-AUDIT-20260801-01`
>
> 상태: `BASE_ANALYSIS_COMPLETE / PROJECT_INTEGRITY_CONFLICTS_OPEN`
>
> 기준일: `2026-08-01`

## 1. 목적

기존 `BS-AUD-F12`의 “Base v8·v9.1·v9.3 표기가 동시에 활성” 문제를 실제 Base current main, 검증 릴리스, Blacksmith adapter·Snapshot·Router·Registry·Sheet binding과 대조해 세부 원인으로 분해한다.

## 2. Base 기준

```text
Base latest main observed:
90ec6f33953f80f607d4e79f58cc2174eb178f73

Latest released project line:
Base v9.3.0
release: 30ca6c7b5f93521f0eb0eed42d01437cd43c50ae
evidence: 462a86db192d23d0f386281a1eb54b0a8cbad62e
registry SHA-256: 9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1
```

Base latest main에 존재하는 v9.4 제안은 아직 검증 릴리스가 아니므로 Blacksmith 핀으로 사용하지 않는다.

## 3. Blacksmith 충돌

| ID | 문제 | 판정 |
|---|---|---|
| `BASE-F01` | canonical adapter는 v9.1인데 최신 기획은 v9.3 목표를 주장 | MUST_FIX |
| `BASE-F02` | protected baseline `4b465ae…`가 감사 main `500a5a7…`과 다름 | MUST_FIX / validator NOT_RUN |
| `BASE-F03` | adapter Sheet `NOT_CONFIGURED`와 실제 configured Sheet 충돌 | MUST_FIX |
| `BASE-F04` | Base Rules 문서의 commit·25개 기능·v8 Prompt가 구형 | MUST_FIX |
| `BASE-F05` | Adoption Profile에 별도 Base pin이 활성 상태로 남음 | MUST_FIX |
| `BASE-F06` | 로컬 Skill Registry provenance가 canonical adapter와 다름 | MUST_FIX |
| `BASE-F07` | generated Snapshot·Router가 v9.1 상태 | MUST_FIX / regenerate only |
| `BASE-F08` | 표준 CURRENT_CONFIRMED_DECISIONS 진입점 또는 명시 binding 부재 | SHOULD_FIX |
| `BASE-F09` | Operating Health PASS 파생본이 현재 drift를 반영하지 않음 | MUST_FIX |
| `BASE-F10` | Sheet CURRENT 원장에 SUPERSEDED 결정이 혼재 | SHOULD_FIX |
| `BASE-F11` | 최신 Base main을 release pin처럼 사용하면 안 됨 | KEEP_GUARDRAIL |

## 4. 기존 Finding 연결

```text
BS-AUD-F12
└─ BASE-F01~F09
```

새 게임 기획 Finding 수를 추가하지 않는다. 다만 다음 작업 전 해결해야 하는 운영 무결성 차단으로 관리한다.

- Base shared Skill route 실행
- Codex 구현 패키지 인계
- 운영체계 PASS 주장
- 기획 완료 Gate 종료

## 5. 권장 처리

```text
v9.3 release/evidence/hash 검증
→ adapter migration 입력 생성
→ Base generator로 canonical adapter 갱신
→ Snapshot·Router·Health·호환 뷰 재생성
→ Base Rules·Adoption Profile·local Registry provenance 정리
→ configured Sheet와 결정 복원 진입점 binding
→ operating validator·reference freshness·회귀 검사
→ 적대적 콜드 스타트 재검토
```

호환 뷰·Snapshot·Router·Health를 수동 편집하지 않는다. Base generator가 생성해야 한다.

## 6. 이번 단계의 제한

- GitHub 연결로 권위 파일을 조사했다.
- 로컬 Base clone은 DNS 제한으로 실패했다.
- 전체 tracked inventory는 확보하지 못했다.
- `tools/project_operating_contract.py`는 읽었지만 실제 실행하지 않았다.
- Blacksmith 제품 코드·Scene·데이터·에셋은 변경하지 않았다.

## 7. 상태

```text
BASE_ANALYSIS: COMPLETE
BASE_TARGET: V9_3_RELEASED_PIN
PROJECT_ADAPTER_MIGRATION: REQUIRED
PROJECT_OPERATING_INTEGRITY: BLOCKED
LOCAL_VALIDATOR: NOT_RUN
COLD_START_RECHECK: NOT_RUN
PRODUCT_CHANGE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
