# Blacksmith 시작 지점

> 사용자, 새 GPT, 새 Codex와 새 작업자가 프로젝트 목적·현재 상태·보호 범위·다음 작업을 가장 먼저 확인하는 대시보드다. 세부 기획은 Registry의 책임 원본을, 구현 사실은 실제 코드·데이터·테스트를 따른다.

## 한눈에 보기

| 항목 | 현재 기준 |
|---|---|
| 한 줄 약속 | 광클로 무기를 벼리고, 빠른 강화와 위험한 고단계 선택으로 가치가 폭증한 무기를 고객·상인에게 판매하는 모바일 대장간 게임 |
| 핵심 행동 | 터치 제작, 강화 선택, 위험 관리, 무기 보관·판매 판단 |
| 뾰족한 재미 가설 | 짧은 피드백과 10단계 이정표 사이에서 고위험 성공·2단계 도약·가격 폭증을 기대하는 것 |
| 장르·플랫폼 | 방치형 + 클리커형 + 무기 강화 / Android |
| 엔진 | Godot 4.7.1 / GDScript |
| 화면 | Portrait 720×1280, Expand |
| 현재 제품 단계 | Prototype |
| 현재 작업 게이트 | Verification |
| 현재 POC | 제작, +100 강화, 성장·가격·하락·파괴, 단조 기술, 보관함, 자동 단조 |
| 다음 Greenlight | 실제 화면·Android 터치 확인 후 MVP-003 방문 검투사 판매 |
| 가장 큰 위험 | 강화 정보·위험·자동화가 핵심 광클 재미보다 복잡해지는 것 |
| 기준 Git 커밋 | `4ab49d32788cf3ccbf50ed078e6dae1d346ad2e5` 이후 운영체계 동기화 |
| Base 기준 커밋 | `ee265576da7f67d3278f8099dd97d4e714ef0651` |
| 운영체계 감사 | `../../docs/BASE_SYNC_AUDIT.md` |

## 현재 상태

| 구분 | 요약 | 증거 |
|---|---|---|
| 확정 | Android, 광클 피버, 직원·수리 제외, 일반/특수 강화, +100 수식어, 고객/상인 판매 구분 | `DECISION_LOG.md`, Game Bible |
| 구현 | 제작, 강화 위험·성장·가격, 단조 기술, 보관함 6칸, 자동 단조 | `../../data/`, `../../scripts/`, `../../scenes/` |
| 자동 검증 | Godot 파싱·Scene smoke·제작 4건·강화 12건·JSON 검사 | `../../.github/workflows/` |
| 미검증 | 실제 화면 전체 완주, Android 터치·안전 영역, AAB, 성능 | `DEVELOPMENT_GATES.md` |
| 미구현 | 저장·복귀, 고객·상인 판매, 상점, 실제 방치 경제 | `ROADMAP.md` |
| 보류 | 결제, 광고, 서버, iOS, 직원, 무기 수리 | Game Bible |
| 불일치 | 이 운영체계 동기화에서 과거 +5 문서 drift를 현재 구현에 맞춤 | `../../docs/BASE_SYNC_AUDIT.md` |

## 핵심 플레이 경험

```text
광클·자동 작업
→ 즉각적인 피버와 제작 진행
→ 9회의 빠른 일반 강화
→ 1회의 선택·정밀 특수 강화
→ 공격력·가격 폭증 또는 하락·파괴
→ 안전 단조와 폭주 도약 사이 판단
→ 원하는 단계에서 보관
→ 판매처 선택
```

보호할 약속:

- 광클에 과열 불이익을 두지 않는다.
- 일반 강화에 특수 재료 효과가 새지 않는다.
- 고위험은 결과·확률·가격을 시도 전에 보여준다.
- 자동 단조가 수동 선택을 대체하되 자원과 위험을 무시하지 않는다.
- 작은 화면에서 한 번에 하나의 중요한 결정을 요구한다.

## 활성 책임 원본

| 질문 | 책임 원본 |
|---|---|
| 게임 전체 방향·시스템 | `../01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md` |
| 제작 POC | `../../docs/MVP-001_SCOPE.md` |
| 강화 POC | `../../docs/MVP-002_SCOPE.md` |
| 실제 수치·ID | `../../data/**/*.json` |
| 현재 상태 | `ACTIVE_CONTEXT.md` |
| 다음 순서 | `ROADMAP.md`, `DEVELOPMENT_GATES.md` |
| 결정과 대체 이력 | `DECISION_LOG.md` |
| 문서 책임·발행 | `DESIGN_DOCUMENT_REGISTRY.json` |
| Skill 라우팅 | `SKILL_REGISTRY.json` |
| Base 동기화 | `../../docs/BASE_RULES_VERSION.md`, `../../docs/BASE_SYNC_AUDIT.md` |

## 프로젝트 Skill 시작 경로

- 요청·운영: `blacksmith-project-operations`
- 변경 검증: `blacksmith-change-validation`
- 게임 디자인: `blacksmith-game-design`
- 모바일 UX: `blacksmith-mobile-ux`
- 엔지니어링: `blacksmith-engineering`
- QA: `blacksmith-qa`
- 이전 ID: `../../skills/LEGACY_SKILL_ALIASES.md`
- Learning Log: `../../skills/SKILL_LEARNING_LOG.md`

사용자는 Skill 이름이나 mode를 고를 필요가 없다. `SKILL_REGISTRY.json`의 trigger와 현재 Work Mode로 최소 집합을 자동 선택한다.

## 새 작업자의 읽기 순서

```text
AGENTS.md
→ 이 문서
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 책임 원본
→ SKILL_REGISTRY.json
→ 현재 Issue·승인 요청
→ 실제 코드·데이터·테스트
```

## 지금 하지 말아야 할 것

- 직원·무기 수리·결제·광고·서버를 범위 없이 추가하지 않는다.
- 실제 Android 검증 없이 모바일 완료로 표시하지 않는다.
- PDF/DOCX를 정본으로 수동 관리하지 않는다.
- 전체 Base나 전체 Skill을 복제하지 않는다.
- 자동 테스트 PASS를 손맛·가독성·실기기 PASS로 표현하지 않는다.
- 현재 강화 수치를 문서에서 중복 정본으로 만들지 않는다.
- 기존 안정 경로를 audit와 승인 없이 대량 이동·삭제하지 않는다.

## 다음 작업

1. POC v0.6.0 화면을 Godot에서 수동 완주하며 정보 밀도·스크롤·버튼을 검수한다.
2. Android 실제 기기에서 터치·안전 영역·연속 탭 피로를 검증한다.
3. 자동 단조의 목표·반복·재료 소진·파괴 복구 흐름을 플레이 검수한다.
4. MVP-003 방문 검투사 판매를 구현한다.
5. 저장·복귀와 실제 경제는 판매 루프 이후 별도 범위로 설계한다.
