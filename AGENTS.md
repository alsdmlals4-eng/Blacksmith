# Blacksmith AI 작업 규칙

Blacksmith는 Android 세로형 Godot 제작 게임 프로젝트다. 현재 일반 제품 구현은 `BLOCKED`이며, `R2_BATCH_006_APPROVED_MAIN_CANON`이 승인한 버티컬 슬라이스 namespace만 제한적으로 구현할 수 있다.

## 1. 권위 순서

1. 사용자의 최신 지시와 승인
2. `AGENTS.md`
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
6. Active Context·Roadmap·Development Gates
7. 실제 코드·data·Scene·tests
8. Google Sheet와 파생 문서
9. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 정본이다. Google Sheet는 같은 Decision ID·경로·Commit·검증 상태를 연결한다.

## 2. 필수 작업 순서

```text
현재 권위·변경 경계 확인
→ PRE_WORK_RESEARCH_GATE: 벤치마킹·현업/공식/1차 자료 조사
→ ADOPT / ADAPT / REJECT / DIFFERENTIATOR + 정본 충돌 + 적대 pre-check
→ brainstorming·적대적 검토
→ RED: 실패 계약 테스트 작성·의도한 실패 관측
→ GREEN: 최소 정본·구현 변경
→ REFACTOR: 중복·구형 참조 정리
→ exact-head 전체 검증
→ GitHub·Sheet readback
→ 같은 승인 범위는 재승인 없이 병합 / 새 planning conflict·scope expansion만 사용자 Decision
```

### PRE_WORK_RESEARCH_GATE — 벤치마킹·현업 비교·조사

Decision `BS-OPS-20260811-02`. 모든 의미 있는 작업은 fresh authority preflight 뒤 실제 설계·정본·구현·테스트·설정·자산 변경 전에 벤치마킹과 최신 현업/공식/1차 자료 조사를 수행한다. 이 Decision은 `BS-OPS-20260805-01`의 benchmark scope만 refine하며 기존 TDD·early checkpoint 권위는 유지한다.

- 게임 기획·콘텐츠·UX·경제·시장 포지셔닝: 직접/인접 유사작 2개 이상 + 현업/공식/1차 자료 2개 이상을 기본으로 한다. 핵심 시스템·경제·출시·권리·접근성 등 고위험 작업은 유사 사례 3개 이상 + 공식/1차 자료 2개 이상을 기본으로 한다.
- 기술·Godot·Android·GitHub·CI·tooling·performance: current 공식/1차 자료 1개 이상 + 유사 구현/추가 공식 자료 1개 이상과 프로젝트 버전 호환성을 확인한다.
- 저위험 maintenance·좁은 문서/metadata repair: 현재 정본·최근 PR·공식 책임 원본을 다시 읽고, 외부 비교가 실질적으로 무관하면 `BENCHMARK_NOT_APPLICABLE` 사유를 남긴다. 관련 공식/1차 자료가 존재하면 최소 1개 확인한다.
- 모든 경우 `ADOPT / ADAPT / REJECT / DIFFERENTIATOR / 남은 불확실성`과 정본 충돌·적대 pre-check를 기록한다.
- 유명 사례라도 프로젝트 코어와 충돌하면 `REJECT`한다.
- 출처와 확인 날짜를 PR·정본·Decision·감사 기록 중 하나에 남긴다.
- 벤치마크의 수치·확률·경제·보상은 Blacksmith 정본으로 자동 역수입하지 않는다.
- 검색 요약·과거 채팅·메모리·2차 블로그만으로 시간민감 정본 결론을 확정하지 않는다.

### 작업마다 TDD

모든 기능·규칙·계약·버그 수정은 TDD를 사용한다.

```text
RED → GREEN → REFACTOR
```

- 테스트를 먼저 작성한다.
- 의도한 이유로 실패하는 RED를 실제 관측한다.
- 최소 변경으로 GREEN을 만든다.
- GREEN 이후에만 정리한다.
- RED와 GREEN 증거 없이 PASS 또는 완료를 주장하지 않는다.
- 문서·기획 변경도 기계 판독 계약 테스트로 보호한다.

## 3. 승인 배치와 조기 체크포인트

- 승인 10건은 **최대 배치 크기**다.
- 기본적으로 Draft PR에 승인 Decision을 누적한다.
- 다음 조건이면 10건 전에도 조기 체크포인트를 허용한다.
  - `HIGH_RISK_CONFLICT`: 기존 핵심 규칙과 고위험 충돌
  - `SESSION_END`: 세션 종료로 정본 유실 위험
  - `LARGE_CANON_IMPACT`: 다수 권위 문서·Registry·후속 설계에 큰 영향
- 조기 체크포인트도 적대적 감사·changed files·리뷰·CI·Sheet readback을 생략하지 않는다.
- 같은 승인 범위는 exact technical validation 뒤 병합 재승인을 요구하지 않는다. 새 기획 충돌·범위 확장만 별도 사용자 Decision이 필요하다.
- 병합 뒤 main SHA와 Sheet를 다시 읽어 최종 동기화한다.

## 4. 현재 코어 보호

- 강화 성공·실패와 멈춤·추가 도전이 즉각 반복 재미다.
- 작품은 UID·소유·손상·복원·사건·연대기를 유지한다.
- 일반 강화는 한 입력에 한 결과다.
- 정밀강화는 주재료 맥락 + 강화 방식 + 촉매 한 개다.
- 수식어는 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 슬롯이다.
- 제작 등급은 `보통 / 우수 / 명품 / 걸작 / 전설` 다섯 단계의 출생 완성도다.
- 예술성은 단계명이 없는 `1~10` 숫자형 무기·작품 능력치다.
- 예술성은 전투력을 기본적으로 올리지 않는다.
- 보조재료 슬롯과 일반 수식어 A·B는 재도입하지 않는다.

## 5. 보호 경로

기획 승인 전 변경 금지:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

일반 제품 구현은 R1~R8와 최종 사용자 검수 및 별도 Codex Gate 전까지 `BLOCKED`다. 버티컬 슬라이스는 승인된 namespace와 Task 범위를 넘어 확장하지 않는다.

## 6. 정본·구형 문서

- 한 질문에는 활성 책임 원본 하나만 둔다.
- `[대체됨] / [부분 대체됨] / [보류] / [폐기] / [역사 증거]`를 직접 표시한다.
- 과거 PASS는 해당 과거 HEAD의 증거일 뿐 현재 제품 PASS가 아니다.
- PR #81은 `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`이다.

## 7. 완료 증거

- expected/exact HEAD 고정
- Base adoption
- Python contracts
- Godot headless
- 변경 파일·보호 경로
- PR 댓글·인라인 스레드
- Google Sheet same-ID readback
- 미실행 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`

## 8. 플랫폼 출시·에셋 권리

출시·외부 자산·AI·외주·참조 기반 독립 제작 작업은 다음 프로젝트 증거를 읽는다.

- `docs/PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE.md`
- `docs/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- `docs/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

Android·Google Play 출시에서는 콘텐츠 등급과 target audience를 분리하고 Families, 광고 SDK, 데이터·개인정보, ads/IAP, build·store·questionnaire 일치를 함께 검토한다. 원본을 조금 수정하거나 AI로 변환했다는 이유만으로 독립 자산으로 보지 않으며 `reference_brief`, `forbidden_expression`, 별도 `final_asset_record`, 유사성 검토를 요구한다.

필수 권리·계약·약관 버전·플랫폼 답변이 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다. 제품 구현 BLOCKED 상태와 실제 제출·법률 검토·최종 등급 미실행 상태를 바꾸지 않는다.

## 9. HiGodot·GUT·Hera 권위와 필수 진입 Gate

- `HIGODOT_SOLE_AUTHORING_AUTHORITY`: `BS-HIGODOT-20260808-01` 사용자 승인으로 HiGodot은 Production Scene·Node·Resource·`project.godot` 설정의 단일 저작 권위로 활성화됐다.
- `GUT_SOLE_TEST_AUTHORITY`: GUT 9.7.1은 `BS-TEST-20260806-01` 및 postmerge closure에 따라 `FORMALLY_ADOPTED_ACTIVE`이며 GDScript 단위·통합 테스트 프레임워크의 단일 권위다.
- `ENTRY_GATE_FAIL_CLOSED`: 결정 원장·미확정/감사·이미지 목록/검수·열린 PR exact HEAD 중 하나라도 누락·stale·schema drift이면 작업 진입을 차단한다.

현재 HiGodot 권위는 `FORMALLY_ACTIVATED_PRODUCTION_AUTHORING_AUTHORITY`이고 production activation은 `USER_APPROVED_ACTIVE`다. 단, 현재 승인은 `TASK2_SCOPED_AUTHORING_ONLY`이며 일반 제품 Gate를 열지 않는다. 또한 실제 `.tscn`/Resource/`project.godot` 변경은 HiGodot production-authoring 실행 경로가 직접 생성한 저작 provenance가 있어야 하며, 일반 코드 편집기·GitHub Contents API·직접 텍스트 치환으로 Godot 직렬화 surface를 우회해서는 안 된다. 현재 저장소의 Live-Editor Pilot은 scratch-only/source-mutation-forbidden이므로 production 실행 경로로 간주하지 않는다.

`BS-HIGODOT-20260808-01`: HiGodot production authoring 권위를 활성화하되, 현재 Task 2에서 허용되는 Godot 저작 범위는 승인된 MainMenu / BlacksmithApp / Workshop scene과 `application/run/main_scene` 전환뿐이다. mixed-surface PR에는 `FILE_AUTHORITY_MANIFEST_REQUIRED_FOR_MIXED_SURFACE_PR`가 적용된다. 현재 production 실행 경로가 노출되지 않았거나 검증되지 않았으면 Scene/`project.godot` GREEN은 fail-closed로 중지한다.

`BS-HERA-20260808-01`: Hera Agent Godot 1.0.0 vendor tree의 main 존재와 당시 비활성 상태를 확정한 역사적 reconciliation Decision이다. 당시 상태 `VENDORED_PRESENT_DISABLED_NON_AUTHORITATIVE`는 보존한다.

`BS-TOOLCHAIN-20260809-01`: 사용자가 Godot AI 3.1.3 전환과 GUT·Hera editor plugin 활성화를 승인했다. 현재 GitHub 상태는 Godot AI `3.1.3`, GUT editor plugin enabled, Hera editor plugin enabled이며 Hera의 현재 상태는 `VENDORED_PRESENT_ENABLED_NON_AUTHORITATIVE`다. 이 활성화는 권위 확장이 아니다. HiGodot은 계속 `TASK2_SCOPED_AUTHORING_ONLY` Godot 직렬화 저작 권위이고, GUT은 계속 `SOLE_GDSCRIPT_TEST_FRAMEWORK_AUTHORITY`, Hera authoring/mutation authority는 계속 `NONE`이다. Hera가 별도 범위 승인을 받기 전에는 `.tscn`·Resource·`project.godot` 또는 기타 추적 제품 surface를 저작·수정할 수 없다.

`BS-TOOLCHAIN-20260811-02`: 사용자의 최신 3.1.4 업데이트 승인을 current version authority로 적용한다. 현재 `addons/godot_ai`는 공식 `v3.1.4` exact upstream vendor이며, `BS-TOOLCHAIN-20260809-01`의 3.1.3은 GUT/Hera 활성화와 Task2 실행의 역사 baseline으로 남는다. 완료된 Task2 전용 `set_main_scene` vendor overlay는 current vendor에 재포크하지 않으며 미래 영속 main-scene 변경은 새 범위 Decision이 필요하다. GUT 9.7.1 sole test authority, Hera authority `NONE`, 제품/Task3 차단은 그대로다.

GUT runtime은 Git 추적 파일을 수정할 수 없고, HiGodot은 `tests/gut/**`, `.gutconfig.json`, `addons/gut/**`, JUnit 성공 결과를 수정할 수 없다. 같은 파일의 이중 권위와 출처 미상 변경은 실패 처리한다. Hera 또한 별도 범위 승인 전에는 Git 추적 제품·저작 surface를 수정할 권위가 없다.

`READY`·`AWAITING`·`IN_REVIEW`·`APPROVED` 같은 일반 상태 문자열만으로는 진입할 수 없다. 범위, current main SHA, Sheet range, 열린 PR 상태, 미실행 검증과 차단 이유가 기계 판독 가능한 상태로 함께 기록되어야 한다.

## 10. 현재 프로젝트 총 작업지시문

- 작업지시문 정본: `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION.md` (`v4.5 r2`)
- 프로젝트 바인딩 override Decision: `BS-OPS-20260811-01`
- 선행 조사 Gate Decision: `BS-OPS-20260811-02 / PRE_WORK_RESEARCH_GATE`
- 첨부 source의 Switchy-Express 경로는 원문 보존 역사값이며, 현재 Blacksmith 실행 경로는 `BS-OPS-20260811-01`의 사용자 최신 바인딩을 따른다.
- 같은 승인 범위는 기술 재검증 후 병합 재승인을 요구하지 않는다. 새 기획 충돌·범위 확대만 별도 사용자 Decision이 필요하다.
- `PRODUCT_IMPLEMENTATION: BLOCKED`, `TASK3_IMPLEMENTATION: NOT_APPROVED`를 유지한다.
