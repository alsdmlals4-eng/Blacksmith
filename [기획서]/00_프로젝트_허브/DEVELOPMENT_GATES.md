# Blacksmith Development Gates

> 갱신일: `2026-08-01`
>
> 현재 단계: `PLANNING_REMEDIATION_IN_PROGRESS`
>
> 제품 구현 권한: `NONE`

## 판정 원칙

- 승인 결정, 설계, 구현계획, 제품 구현, 자동 테스트, 실제 렌더, Android, 접근성, 성능, 외부 플레이는 독립 상태다.
- 미실행 검사는 `NOT_RUN` 또는 `UNVERIFIED`로 유지한다.
- 과거 PoC PASS는 최신 v9 정본의 회귀 PASS를 대신하지 않는다.
- GitHub 정본·계획 데이터·Sheet가 같은 ID로 재조회돼야 동기화 PASS다.
- Base 생성 파생물은 generator·validator 실행 없이 수동 PASS 처리하지 않는다.

## Gate Summary

| Gate | 현재 상태 | 증거 | 차단 조건 |
|---|---|---|---|
| Project core | `PASS / KEEP` | 코어 계약·사용자 승인 | 코어 불변 변경 |
| Current decision discovery | `PASS` | `CURRENT_CONFIRMED_DECISIONS.md` | 정본 인덱스 drift |
| Art·Modak·screen direction | `PASS / WORKING_BASELINE` | 승인 정본·비주얼 보드 | 최종 에셋·사람 검수는 별도 |
| Grade rule | `PASS` | `BS-GRADE-20260801-02` | 표시·순서 변경 |
| Save·ResultEnvelope design | `PASS / DESIGN_COMPLETE` | `BS-SAVE-20260801-01`, 11 Task plan | 런타임·테스트 없음 |
| v9 legacy migration design | `PASS / DESIGN_COMPLETE` | `BS-MIGRATION-20260801-01`, 7 Task plan | 데이터·SaveMigrator·fixture 없음 |
| Base structure analysis | `PASS / ANALYSIS_COMPLETE` | `BS-BASE-AUDIT-20260801-01` | local inventory·validator NOT_RUN |
| Base v9.3 project migration | `BLOCKED / REQUIRED` | adapter v9.1·baseline·Sheet drift | generator·validator·cold-start PASS 필요 |
| GitHub·Sheet review Pass2 | `PASS / REMEDIATION_IN_PROGRESS` | `BS-REPO-AUDIT-20260801-02` | safe fixes·P0/P1 open |
| Customer common contract | `PARTIAL` | 4유형 방향·카시아·에르사 | 모험가·군인·공통 Resolver 미정 |
| Auto-forge boundary | `OPEN` | 구형 runtime만 존재 | 핵심 선택 우회 |
| Theme·safe area·settings | `OPEN` | 방향 일부 | 공통 계약·실기기 없음 |
| Current v9 automated validation | `NOT_RUN` | 계획만 존재 | 최신 fixture·CI 실행 필요 |
| Android device | `NOT_RUN` | 없음 | 실제 빌드·기기 증거 |
| Accessibility human review | `NOT_RUN` | 코드·방향 일부 | 사람·기기 검증 |
| Performance | `NOT_RUN` | 없음 | 대표·최악 장면 측정 |
| External playtest | `NOT_RUN` | 계약 일부 | 신규 플레이어 행동 증거 |
| Planning complete | `BLOCKED` | P0 10·P1 10·Base drift | P0/P1 계약 종료 |
| Codex BUILD | `BLOCKED` | 사용자 기획·검수 미완료 | 모든 선행 Gate |
| Production greenlight | `BLOCKED` | 제품 증거 없음 | 구현·플랫폼·사람·사업 증거 |

## PoC 증거의 사용 범위

과거 PR #35와 validation #468의 Python·Godot·E2E PASS는 다음을 증명한다.

- 구형 제작·강화·자원 거래 모델이 당시 계약대로 동작
- 카일 검투사 장비 생애 PoC가 결정론적으로 완주
- 기존 원자 rollback·event ID 멱등성·장비 Registry 패턴 사용 가능

다음을 증명하지 않는다.

- 별도 메인·SaveCoordinator·App Shell
- 최신 제작 등급 ID
- 계보+보조2·+50 이원화
- 고객 4유형 공통 파이프라인
- 최신 자동 단조 경계
- Android 중단 복구
- 현재 v9 재미·가독성·성능

## 현재 P0 기획 Gate

| Finding | 기획 목표 | 런타임·검증 |
|---|---|---|
| F01 제품 진입 | 승인됨 | OPEN |
| F02 저장·이어하기 | `BS-SAVE-20260801-01` 해결 | OPEN |
| F03 단일 AppState | Shell·Save 설계 연결 | OPEN |
| F04 제작 등급 | `BS-MIGRATION-20260801-01` 해결 | OPEN |
| F05 수식어·+50 | migration target 해결 | OPEN |
| F06 자동 단조 | OPEN | OPEN |
| F07 고객 하드코딩 | PARTIAL | OPEN |
| F08 운명·관계·유형별 결과 | PARTIAL | OPEN |
| F09 ResultEnvelope | `BS-SAVE-20260801-01` 해결 | OPEN |
| F10 비주얼 Placeholder | REMEDIATION IN PROGRESS | 최종 에셋 NOT_RUN |

제품 구현 전 기획 목표가 모두 해결돼야 한다. 제품 구현 뒤에는 같은 Finding을 런타임·자동·플랫폼 증거로 다시 닫는다.

## Base Operating Gate

필수 순서:

```text
released Base v9.3 pin·evidence·Registry hash 검증
→ PROJECT_BASE_ADAPTER migration
→ Snapshot·Router·Health·compatibility views generator 재생성
→ configured Sheet·current decision entrypoint binding
→ operating-contract validator
→ reference freshness
→ cold-start recheck
```

latest Base main과 미출시 v9.4 제안을 직접 pin하지 않는다.

## Planning Complete Gate

다음이 모두 충족돼야 사용자 `기획 완료` 선언 후보가 된다.

- P0 기획 Finding 0
- P1 중 구현 전 필요한 계약 0
- Base operating integrity PASS
- CURRENT·SUPERSEDED·LEGACY·PLACEHOLDER 전파 정리
- Design Document Registry 최신화
- GitHub·Sheet cross-source verification PASS
- 적대적 검토 Pass 3에서 P0/P1 신규 발견 0

## Codex BUILD Gate

```text
User 기획 완료
→ adversarial final review PASS
→ User 검수 완료
→ approved implementation plan and exact branch
→ Codex PLAN read-only review
→ GPT package review
→ READY_FOR_BUILD
```

## Product Validation Gate

자동:

- 최신 v9 데이터 validator
- save/migration/customer/auto-forge contract tests
- Godot import·Scene smoke·E2E
- result reroll/double apply/resource loss 0
- legacy migration loss 0

외부:

- Android process death·safe area·back button
- 접근성 사람 검토
- 대표·최악 장면 성능
- 외부 최소 6명 행동 검증
- 최종 에셋·라이선스·화면 시각 검수

외부 검증은 실행 증거 전까지 `NOT_RUN`이다.
