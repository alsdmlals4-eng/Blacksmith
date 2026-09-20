# Blacksmith Current Base Adaptation Work Contract

이 문서는 운영·Base 적용·스킬 연결만 소유한다. 게임 의미·저장·엔진·자산 승인을 소유하지 않는다.

## 현재 승인·계획 · 2026-09-20

사용자 승인: #883 비교 적용안에 `승인할게`, 이후 #885 재미 검증 기준의 추가 적용을 직접 요청했다. 범위는 지침·스킬·참조·관련 검사 교정과 현재 작업 정상 PR 병합/main readback이다. R05 게임 구현은 시작하지 않는다.
방식: PLAN → NONCODING_BUILD → REVIEW. GODOT_PRODUCT_BUILD는 이번 범위 밖이다.
원래 checkout의 Godot AI3.2.0→4.1.0 표기/미커밋 변경은 미확인 사용자 작업으로 보존한다. main17fa19195fbb78faaef0bdde88b986e3e1d9100d에서 분리한 깨끗한 작업 폴더의 기존 보호 gate는 PASS다.

- [x] 현재 정본·실제 소비처·main·Base #883/#885·열린 PR 확인과 사용자 승인.
- [x] 보호 gate baseline PASS, 실제 owner 검사7개 RED, 독립 스킬 행동 baseline.
- [x] AGENTS·스킬·Registry·경로 교정, 생성물 재생성.
- [ ] 영향/전체 관련 검사, 독립 행동 검증, 전체 검토2회.
- [ ] 현재 작업 PR exact HEAD 검증·정상 병합·main 확인.

계획·체크리스트·메모는 이 기존 owner에 통합한다. 설치 스킬의 계획/검토 단계를 같은 계약에서 중복 초기화하지 않는다. 승인·필수 검사·독립 검토는 생략하지 않는다.
작업일지/PDF는 기존 날짜별 누적 정책을 유지한다. 이 운영 교정으로 새 월간 판본·게임 Blueprint·HTML PM을 만들지 않는다.

## Current-authority 경로

다음 JSON은 이 문서의 경로 표이지 새 상태 원장이 아니다. AGENTS → 이 표 → context/production → 관련 분야와 실제 소비처 → 최신 main/PR → 채택 Base/최신 Base 차이 → 필요한 스킬 순으로 읽는다.

<!-- current-authority -->
```json
{
  "schema_version": 1,
  "base_observation": {
    "repository": "alsdmlals4-eng/Base",
    "ref": "refs/heads/main",
    "commit": "23ecad5a3084f97c4e5d1e39a9a6d70d1eeb37ef",
    "observed_at": "2026-09-20",
    "merged_prs": [883, 885],
    "role": "OBSERVATION_NOT_RELEASE_LOCK"
  },
  "owners": {
    "context": "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
    "production": "docs/design/BLACKSMITH_HUMAN_BLUEPRINT_PRODUCTION_20260911.md",
    "decisions": "CURRENT_CONFIRMED_DECISIONS_20260820_OVERLAY.md",
    "fields": "docs/planning/BLACKSMITH_PLANNING_AUTHORITY_INDEX.md",
    "blueprint": "docs/design/BLACKSMITH_HUMAN_BLUEPRINT_20260911.md",
    "remaining": "docs/design/BLACKSMITH_REMAINING_IMPLEMENTATION_SPEC_20260914.md",
    "handoff": "docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md",
    "history": "CURRENT_CONFIRMED_DECISIONS.md",
    "design_skill": "skills/game-design/SKILL.md",
    "qa_skill": "skills/qa/SKILL.md",
    "engineering_skill": "skills/engineering/SKILL.md"
  }
}
```
<!-- /current-authority -->

history와 날짜별 이전 상태는 provenance이며 현재 실행 승인이 아니다. v4.8-r5.4 파일명 참조는 실제 추적 파일이 없어 활성 경로에서 제외했다. 과거 선언을 새 파일로 재구성하지 않는다.
최근 replan은 production·통합 Blueprint와 실제 `scripts/vertical_slice/domain/vs_replan_tag_rules.gd`/save/UI를 대조한다. 구형 코어/Decision은 대체되지 않은 필드에서만 원본이다. 이번 작업은 제품 값을 바꾸지 않는다.

## 채택·관찰·적용 구분

- 채택 릴리스는 `skills/PROJECT_BASE_ADAPTER.json`의 Base **v9.4.4**다. 이 파일이 편집 가능한 통합 원본이다.
- router, snapshot, 기존 호환 adapter, `docs/PROJECT_OPERATING_DASHBOARD.html`은 채택 pin의 생성물이다. 수동 수정하지 않는다. 생성 router는 adapter/snapshot으로 연결되며 adapter의 shared override가 이 운영 owner를 가리킨다. router의 stop은 미검증 route 실행에만 적용한다. 현재 권위·실패 원인의 읽기 전용 감사는 AGENTS의 상위 경계를 따른다.
- 보호 검증기는 `.github/workflows/validate-project-base-adapter.yml`의43b3ffb2c5b026e3d4a38dab2338585894d36f61을 유지한다. release/pins/protected_paths는 바꾸지 않는다.
- adapter 수정 CI의 기존 규칙에 따라 보호 baseline만 검증된 시작 main으로 정합화한다. 제품 승인 manifest는 만들거나 재사용하지 않는다.
- 관찰 main/#883/#885는 운영 적용 근거다. 다음 새 작업에서는 원격 main을 다시 확인하고 영향 drift를 판정한다. release lock을 자동 갱신하지 않는다.
- 공용 Skill 본문을 복사하지 않는다. 아래 승인된 project-local 운영/재미 검증 적용만 narrow override다. 공유 실행은 채택 snapshot/pin을 먼저 검증한다.

읽은 Base owner: AGENTS/START_HERE, `docs/GPT_CODEX_WORKFLOW_POLICY.md` §3, `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`, intake와 workspace/adapter 계약.
추가 #885 owner: `skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md#fun-verification-lifecycle`, `docs/knowledge/game-development/EXPERIENCE_TO_PRESENTATION_GUIDE.md`, `skills/auditing-and-refining-ui-art/references/project-adapter-contract.md` §11. Base 원격의 검증된 관찰 revision에서 읽으며 그 SHA를 릴리스나 게임 판정 기준으로 사용하지 않는다.
ADOPT: 조건부 로드·승인/검토 공유·근거 재사용·재미 가설의 생명주기. ADAPT: 프로젝트 실제 소비처·기획·이미지·월간 PDF·보호 gate. REJECT: 전체 Base 이식·새 감독/대시보드·엔진 업그레이드·보편 재미 점수.
게임 벤치마크 재조사는 이번 지침 연결의 근거가 아니다. Base 실제 원문·프로젝트 consumer·검사 반례를 비교했다. Base에 기재된 외부 연구의 신규 직접 조사를 했다고 주장하지 않는다.

## 재미 검증의 프로젝트 연결

플레이어 경험을 바꾸는 작업만 기존 생산계약/기능 명세에 **요구 ID → 승인 경험 원본 → 가설/반례 → 상태·선택·정보·피드백 → 실제 소비처 → 검증/다음 판단**을 연결한다. 작은 작업은 짧게, 큰 기능은 기존 상세 명세에 기록한다. 순수 운영 교정은 제품 재미 검증 NOT_APPLICABLE이며 아래 연결은 검토 질문이다.

| 기존 경험/원본 | 실제 소비처 | 다음 제품 작업의 반증·관찰 질문 |
|---|---|---|
| Blueprint의 STOP OR PUSH·10단위 태그/촉매 선택 | `scripts/vertical_slice/ui/vs_workshop_screen.gd`, `scripts/vertical_slice/domain/vs_replan_tag_rules.gd` | 비용·위험·추가/강화 차이를 이해해 선택하는가? 한 선택만 반복하거나 왜 실패했는지 설명하지 못하면 가설을 재검토 |
| 생산계약의 의뢰·같은 UID·결과/연대기 | `scripts/vertical_slice/services/vs_commission_service.gd`, `scripts/vertical_slice/ui/vs_item_chronicle_screen.gd` | 장비와 세계 결과의 인과를 이해하는가? 보상 수령만 기억하고 내 장비 결과를 구분 못하면 반증 |
| Blueprint의 선택형 세계창 | `scripts/vertical_slice/ui/vs_workshop_screen.gd` | 공방 판단을 방해하지 않으면서 원하는 결과를 볼 수 있는가? 전환 피로·중요 정보 가림을 관찰 |

위 질문은 HYPOTHESIS/사람 검증 NOT_RUN이며 새 게임 규칙·재미 PASS가 아니다. 사용자 경험을 임의로 점수화하거나 재도전율/플레이시간만으로 몰입을 확정하지 않는다.
규칙 효과는 기존 domain/data, 표현은 UI/모션이 소유한다. 표현은 확정 결과를 표시하며 비용·보상·저장을 다시 계산하지 않는다. 상태·정보 공개·발생 시점·반복·취소/중단/복귀·필요 자산·consumer·확인 방법을 같은 요구에 묶는다. 미구현 경로는 PLANNED다.
DOC/MACHINE/RUNTIME/HUMAN/USER_APPROVAL/RELEASE를 구분한다. 행동 관찰·자기보고·필요 로그와 반대 근거를 대조한다. 이해 문제/규칙·선택 문제/연출 문제/반복 피로/빌드 결함을 분리해 교정한다. 사람 증거가 없어도 승인된 구현은 계속하며 HUMAN 승격만 미검증으로 둔다.

## 최소 실행과 보호

동일 승인/가설/consumer/환경의 유효 근거는 재사용한다. 중요한 새 판단에만 실질 대안을 비교한다. 전체 검토는 동일 후보 계보2회, 이후 결함별 교정이다.
기계 계약/코드는 RED → GREEN → REFACTOR, 순수 문장은 사실·링크·diff 확인이다. 필수 CI·저장·보안을 비용 이유로 생략하지 않는다.
실패 gate는 의존 실행을 차단한다. 독립 읽기 전용 감사는 가능하다. 독립 수정은 승인·깨끗한 별도 범위·그 범위 gate 성공이 필요하다. root 실패를 PASS로 바꾸지 않는다.
GITHUB_REPOSITORY_ONLY_CURRENT_CANON = TRUE. NOTION_STATUS = HISTORICAL_REFERENCE_ONLY / NO_FUTURE_READ_WRITE_REQUIRED. GOOGLE_SHEET_STATUS = HISTORICAL_MIGRATION_ONLY / NO_FUTURE_WRITE_REQUIRED.
NO_AUTOMATIC_BASE_PIN_UPDATE = TRUE. NO_PRODUCT_PATH_CHANGE = TRUE는 이번 범위다. NO_DIRECT_MAIN_PUSH = TRUE. NO_FORCE_PUSH = TRUE.
OPEN_DRAFT_READ_ONLY_DO_NOT_TAKE_OVER: 이번 #359/#196은 읽기 전용이다. #359 PM wrapper/receipt 기능을 흡수·재구현하지 않는다. 같은 파일의 main 결함만 독립 교정한다.
상위 폴더/설치 스킬/전역 설정은 변경하지 않는다. 계획·체크리스트·메모는 이 owner를 재사용한다. 새 과금·권한·파괴적 작업은 별도 승인이다.

## 검증·기록

현재 경로: `python tests/check_current_authority_entrypoint_contract.py`와 `python -m unittest tests.test_lean_authority_routing -v`.
역사 증거: `python tests/check_base_current_adaptation_work_contract.py`는 기존9월3일 receipt와 CI고정 Base850204b3e5de81a4045111b4a050c46c5a292b59를 검증한다. 과거 SHA는 현재 관찰값/새 작업 승인이 아니다.
원본 pin의 `tools/check_project_operating_contract.py --project-root <current-worktree> --base-repository <verified-pinned-Base> --protected-base <trusted-baseline> --check`를 실행한다. 보호 실패를 우회하지 않는다.
구형 AGENTS 문구를 강제하던 검사는 해당 상세 원본과 실제 경로를 보도록 옮긴다. 제품 계약의 기대 의미는 유지한다.
마감: 보호 경로 무변경·generated check·관련 전체 검사·CI·전체 검토2회·thread·원격 HEAD·병합 main 확인. 보호 설정이 있다는 추정은 하지 않는다.
Godot/Android/사람 검수/최종 아트/출시는 NOT_RUN. 정상 revert가 롤백이며 기존 작업·승인 원문·PDF는 보존한다.

## 실행 증거

2026-09-20 baseline: 독립 행동 감사에서 문서 교정에 전체 이미지/Sheet 요구, 구형 광클/정밀 규칙 충돌, 보호 실패와 읽기 전용 감사 혼동을 확인했다. 참조 검사7개는 실제 owner 검증 부재로 RED. 원래 checkout의 실패를 보존하고 isolated main의 동일 gate는 PASS.
2026-09-20 교정 후보: 5가지 행동 시나리오의 직접 충돌 해소. 생성 router 수동 수정은 재생성으로 소실됨을 확인해 철회하고 상위 AGENTS/운영 계약과 adapter 연결로 처리했다. 저장소별 pin 검증 PASS, unittest403 대상/3skip, pytest539PASS/3skip. 현재 경로·코어·내구·수리경제·세계손상·Notion 이관·GDD 개별 검사 PASS. 이는 문서/자동 계약 증거이며 제품 실행·재미 검증이 아니다.
Windows Registry 경로의 대괄호가 Git 속성 패턴으로 해석되어 LF 고정이 적용되지 않던 결함을 실제 `git check-attr`로 확인·교정했다. 생성된 해시/승인 원문 바이트 검사는 유지했다. 로컬 임의 Base import를 제거하고 전체 스키마 검증은 CI 채택 pin이 소유한다.
이전 AGENTS·운영 계약의 역사 내용은 Git 이력으로 조회한다. 상시 지시로 재로드하지 않는다.
