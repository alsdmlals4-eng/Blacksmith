# Base → Blacksmith 운영체계 적용 감사

## 기준선

- Base: `ee265576da7f67d3278f8099dd97d4e714ef0651`
- Blacksmith: `4ab49d32788cf3ccbf50ed078e6dae1d346ad2e5`
- 작업 계약: GitHub Issue #14
- 적용 방식: 기존 프로젝트 `audit → reconcile-legacy → migrate → verify`
- 보호 대상: 현재 Godot 동작, 게임 데이터, 사용자 확정 결정, Git 이력

## Base 범위별 조사·적용 판정

| Base 영역 | 확인한 책임 | Blacksmith 적용 |
|---|---|---|
| 루트 시작 규칙 | `START_HERE.md`, `AGENTS.md`, `README.md` | 프로젝트 읽기 순서·우선순위·금지 규칙 갱신 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | Prompt→Work Mode→Skill→계약→구현→검증→동기화 흐름 적용 |
| 자동 라우팅 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | `PLAN/BUILD/REVIEW`, trigger 기반 최소 선택, 실행 보고 적용 |
| 문서 지도 | `docs/DOCUMENTATION_MAP.md` | 질문별 책임 원본·실제 증거·검증 경로 확장 |
| Skill Registry | `skills/SKILL_REGISTRY.json` | 프로젝트 Registry schema v3와 자동 선택 정책으로 마이그레이션 |
| 요청·계약 Skill | `managing-project-intake-and-work-contract` | 프로젝트 Foundation Skill의 route/contract/report mode에 분화 |
| 운영체계 Skill | `managing-game-project-operating-system` | audit/migrate/verify·보존표·Health Report 적용 |
| 변경 검증 Skill | `reviewing-and-validating-project-changes` | 계약·정적·런타임·회귀·증거 보고 적용 |
| 정본 최신성 Skill | `auditing-canonical-reference-freshness` | stale token·경로·Registry·데이터 drift 자동 검사 적용 |
| 프로젝트 템플릿 | `templates/project-operations/` | START_HERE, Handoff, Update Matrix, AI Workflow, Health Report를 프로젝트 전용으로 작성 |
| GitHub 템플릿 | PR·Governance 예시 | Blacksmith PR 체크리스트와 `project-governance.yml` 설치 |
| 발행 체계 | source_only/milestone_sync/always_sync | Game Bible은 milestone_sync, 운영·MVP 문서는 source_only |
| 지식 methods·research·cases | Documentation Map을 통해 카탈로그 확인 | 현재 운영 마이그레이션과 직접 관련 없는 사례·아트·서사 자료는 복사하지 않음 |
| 외부 AI·아트·UI 전문 Skill | 조건부 활성 Skill | 현재 trigger가 없어 설치·실행하지 않음 |
| Base 변경 제안 | 프로젝트 교훈 환류 절차 | 후속 후보로만 유지, 이번 PR과 혼합하지 않음 |

`전부 확인`은 Base 자체 규칙에 따라 모든 파일을 무작정 복제하는 것이 아니라, Documentation Map·Registry에서 이 작업에 영향을 주는 책임 원본·Skill·Template·검사와 그 소비자를 빠짐없이 추적하는 것으로 판정했다.

## 발견한 활성 drift

| 현재 파일 | 발견 | 처리 |
|---|---|---|
| 프로젝트 START_HERE | +5 강화·파괴 없음·테스트 5건 | 실제 POC v0.6.0 기준으로 UPDATE_IN_PLACE |
| ACTIVE_CONTEXT | 실패 유지·인벤토리 미구현 | 하락·파괴·보관함·자동 단조 기준으로 UPDATE_IN_PLACE |
| Game Bible | +5 이정표와 이전 확률 | +100·위험·경제·자동 단조를 포함하도록 UPDATE_IN_PLACE |
| MVP-002 Scope | 이전 확률·파괴 없음·F6 | 데이터·테스트·F5 기준으로 UPDATE_IN_PLACE |
| Development Gates·Roadmap | +5 완료 기준 | 현재 구현·미검증을 재분류 |
| Decision Log | 이전 결정과 현재 구현 충돌 | 과거 결정은 `대체됨`으로 보존하고 새 결정 추가 |
| Skill Registry | `default_selection=none`, schema 1 | schema 3 자동 라우팅으로 마이그레이션 |
| Base Rules Version | 기준 커밋 미기록 | 현재 Base 커밋 고정 |
| 임시 Actions | 특정 과거 브랜치 전용 materializer | 대체 기능이 병합됐으므로 DELETE_APPROVED |
| `project.godot` | 임시 검증 주석 | 기능 영향 없이 제거 |

## 삭제·이동 판정

- 삭제 승인: `.github/workflows/materialize-auto-forge.yml`
  - 과거 한 PR의 압축 패치 적용 전용이며 대상 브랜치가 이미 병합됐다.
  - 현재 게임 빌드·검증·문서가 참조하지 않는다.
  - Git 이력에서 복구 가능하다.
- 이동 없음: 기존 `[기획서]`, Game Bible, Skill 경로는 안정 경로를 유지한다.
- 기존 문서 삭제 없음: 고유 결정과 역사 정보는 현재 파일 또는 Git 이력에 보존한다.

## 미적용·미검증

- PDF/DOCX/Skill Map 생성: NOT_RUN
- Android 실기기·AAB: NOT_RUN
- UI 실제 렌더 사람 검수: NOT_RUN
- 접근성 실제 기기 검수: NOT_RUN
- 성능 프로파일: NOT_RUN
- Branch protection Required Check 강제: NOT_RUN

## 최종 검증 계약

```text
project governance
→ JSON game data
→ Godot import/parse
→ enhancement Scene smoke
→ ForgingSession 4 cases
→ EnhancementSession 12 cases
→ PR changed files 전수 검토
→ stale reference·untouched consumer 재검색
```
