# Base 적용·가지치기 감사

## 기준

- Base: `alsdmlals4-eng/Base@41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 대상: `alsdmlals4-eng/Blacksmith`
- 동기화일: 2026-07-23
- 최종 재검토: 2026-07-24
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 자동 감사: `tools/audit_project_operating_system.py`

## 적용 전략

Base 전체를 프로젝트에 복제하지 않는다. Base 25개 ACTIVE Skill의 기능을 Blacksmith 운영 문서와 다음 프로젝트 Skill 3개에 매핑한다.

- `blacksmith-game-design`
- `blacksmith-engineering`
- `blacksmith-qa`

Base 공용 규칙보다 사용자의 최신 지시, Blacksmith 책임 원본, 실제 구현·데이터·테스트가 우선한다.

## 현재 매핑 결과

| 구분 | 결과 |
|---|---|
| Base ACTIVE Skill | 25개 매핑 완료 |
| Blacksmith 프로젝트 Skill | 3개 유지 |
| 자동 라우팅 | `automatic-trigger-match` |
| Work Mode | PLAN / BUILD / REVIEW |
| 미해결 Git 충돌 검사 | 활성 |
| 정본·참조 감사 | 활성 |
| 제품 Script·Scene·게임 데이터 변경 | Base 운영 PR에서는 없음 |

## 최신 자동 검증

- Data validation #389 PASS
- 고정 Base checkout PASS
- Base Registry·25 Skill 경로·선택 로딩 감사 PASS
- Blacksmith Skill Mode·Registry·책임 원본·로컬 참조 감사 PASS
- Base 전체 운영체제 회귀 PASS
- Git 충돌 블록·JSON·강화 계약·시뮬레이터 계약 PASS

Data validation #391은 새 프로젝트 코어 정렬 검사에서 의도적으로 Red를 만들기 위해 실패했다. Base 적용 자체의 실패가 아니며, stale 시작 문서와 누락된 MVP-003 책임 전파를 검출했다.

최종 Green Workflow ID와 결과는 최종 보고서·Active Context에 기록한다.

## 흡수한 공용 기능

- 프로젝트 작업 계약과 Work Mode 선택
- 운영체계 감사·구형 파일 분류
- 기획 책임 원본과 정책 기반 PDF 발행
- 프로젝트 코어 식별·사용자 승인 확정
- 벤치마킹·PoC·플레이테스트·SWOT/VRIO
- 적대적 검토→비판 검증→최소 개선→회귀
- 정본·경로·ID·Schema reference-freshness
- 계약 보존 리팩터링
- Godot 런타임 진단·정적·회귀·접근성·성능 검증
- 장기 작업 context·handoff

## 정본 동기화 이력

- Base 13개 활성 기능 → 25개
- 구형 Base commit → `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 수동 Skill 선택 → trigger 기반 자동 선택
- Scope와 Report 책임 혼합 → 별도 정본
- 검투사 관전·베팅 삭제 오해 → 후속 보존
- 위험 시뮬레이션 준비 → 기준선 완료
- 프로젝트 코어 미확정 → `CORE_CONFIRMED / CORE_RECORDED`
- 다음 작업 → Issue #34 장비 한 점의 생애 PoC

## 구형·중복 자료 판정

- 과거 Changelog·닫힌 Issue·PR: `HISTORICAL_ARCHIVE`
- legacy `quality_*`: `ACTIVE_COMPATIBILITY`, 신규 schema와 별도 변환 필요
- MVP-001/002 Scope: `CURRENT_CANONICAL` for historical implemented slices
- Issue #29·#14: 완료 후 닫음
- `docs/MVP-003_SCOPE.md`: 새 현행 실행 책임 원본
- `final/latest/v2` 이름의 독립 활성 정본: 생성하지 않음

## 미검증

- 새 작업자의 실제 cold start
- Branch protection의 Required Check 강제 여부
- Android·AAB·실기기
- 사람 시각·접근성·성능
- 외부 플레이테스트
- 로컬 Godot AI MCP client 연결

## 현재 판정

Base 적용과 25 Skill 매핑은 자동 검증 증거가 있다. 다만 프로젝트 전체 완료는 Issue #34 구현과 플랫폼·사람 검증 전까지 선언하지 않는다.
