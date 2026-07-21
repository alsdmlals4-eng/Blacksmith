# Base 적용 감사표

## 기준

- Base 저장소: `alsdmlals4-eng/Base`
- 기준 브랜치: `main`
- 기준 커밋: `ee265576da7f67d3278f8099dd97d4e714ef0651`
- 감사일: 2026-07-22
- 대상 저장소: `alsdmlals4-eng/Blacksmith`
- 적용 원칙: Base 전체 복제가 아니라 책임 원본·라우팅·검증 계약을 Blacksmith의 실제 Godot 프로젝트에 분화한다.

## 읽은 Base 책임 원본

- `README.md`
- `START_HERE.md`
- `AGENTS.md`
- `docs/OPERATING_MODEL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/DOCUMENTATION_MAP.md`
- `skills/SKILL_REGISTRY.json`
- `skills/managing-game-project-operating-system/SKILL.md`
- 위 문서가 현재 요청에 연결한 운영체계·문서·검증·참조 최신성·Active Context 계약

Base 자체 규칙에 따라 모든 Skill을 무작정 로드하지 않고, 이번 요청의 trigger인 기존 프로젝트 운영체계 감사·마이그레이션·검증과 정본 최신성에 필요한 책임 원본을 전부 추적했다.

## 적용 대조표

| Base 영역 | Blacksmith 상태 | 처리 | 결과·경로 |
|---|---|---|---|
| 최상위 AI 규칙 | 부분 적용, 구형 라우팅 | UPDATE_IN_PLACE | `AGENTS.md`에 우선순위·Work Mode·자동 Skill·검증·완료 계약 반영 |
| 프로젝트 시작 라우터 | 존재하나 구현 상태가 +5 기준으로 오래됨 | UPDATE_IN_PLACE | `[기획서]/00_프로젝트_허브/START_HERE.md` 최신화 |
| Base 버전 고정 | 커밋 미확정 | UPDATE_IN_PLACE | `docs/BASE_RULES_VERSION.md`에 기준 SHA·동기화 범위 기록 |
| Work Mode·Skill 라우팅 | 프로젝트 문서 없음, Registry가 수동 `none` | ADD + UPDATE | `WORK_MODE_AND_SKILL_ROUTING.md`, `SKILL_REGISTRY.json` |
| Active Context | 자동 단조·위험 강화·보관함 이전 상태 | UPDATE_IN_PLACE | `ACTIVE_CONTEXT.md`를 v0.6.0 기준으로 갱신 |
| Documentation Map | 기본 지도만 존재 | UPDATE_IN_PLACE | 운영 문서·감사·검증·실제 기능 경로 추가 |
| Development Gates | +5·파괴 없음·5개 테스트 기준 | UPDATE_IN_PLACE | +100·파괴/하락·자동 단조·보관함 기준 갱신 |
| Roadmap | MVP-002가 +5 기준 | UPDATE_IN_PLACE | 현재 Prototype 증거와 다음 Greenlight 재정렬 |
| Design Document Registry | 단일 Bible 등록, 발행 정책 명칭이 Base 최신 정책과 다름 | UPDATE_IN_PLACE | `source_only / milestone_sync / always_sync` 계약에 맞춤 |
| 프로젝트 Skill Registry | trigger는 있으나 자동 선택·비사용 조건·검수 trigger 없음 | UPDATE_IN_PLACE | Base Registry 계약의 프로젝트 전용 필드 반영 |
| 프로젝트 Skill 패키지 | front matter·입력·출력·실패 조건·실행 보고 부족 | UPDATE_IN_PLACE | game-design·engineering·qa Skill 계약 보강 |
| Learning Log | 존재 경로만 등록 | KEEP + 연결 강화 | Registry와 Skill에서 실행 증거 기록 조건 연결 |
| 책임 원본 단일성 | Bible·MVP scope·JSON 역할 구분은 양호 | KEEP | Markdown 설명 / JSON 실제 값 / Script 구현 사실 유지 |
| 문서 발행 | PDF 경로는 있으나 도구·사람 검수 미실행 | KEEP_UNRESOLVED | `NOT_RUN`, 자동으로 CURRENT 처리하지 않음 |
| Visual Source·Asset Manifest | 아직 승인 아트 파이프라인 없음 | DEFER | 실제 승인 이미지 도입 시 설치. 현재 결함으로 판정하지 않음 |
| 접근성 | 모바일 가독성 원칙만 있고 실기기 증거 없음 | PARTIAL | Gate와 QA Skill에 터치·스크롤·안전 영역 검증 유지 |
| 성능 | 목표 플랫폼 프로파일 없음 | NOT_RUN | 대표/최악 장면이 생긴 뒤 Android frame time·메모리 측정 |
| 자동 검증 | Godot·JSON CI 존재 | KEEP + 검토 | 프로젝트 파싱·Scene·모델·데이터 검증을 Required evidence로 연결 |
| 브랜치 보호 | Workflow 존재와 강제 여부 불명 | UNVERIFIED | GitHub 설정 확인 전 Required Check 강제 완료로 표시하지 않음 |
| 콜드 스타트 | 문서 간 상태 불일치로 실패 가능 | FIX | START_HERE→Context→Map→Gates→Registry→실제 파일 경로 통일 |
| Legacy 정리 | 일회성 `materialize-auto-forge.yml` 잔존 | DELETE_APPROVED | 기능 병합 완료 후 사용처 없음. 본 PR에서 삭제 |
| Base 환류 | Blacksmith 고유 구현을 Base에 직접 복사하지 않음 | KEEP | 반복 검증된 공용 교훈만 별도 제안 대상으로 남김 |

## 보존한 Blacksmith 고유 결정

- Godot 4.7.1 / GDScript / Android 세로형 720×1280
- 광클은 피버 보상으로 연결
- 직원·수리 시스템 제외
- 일반 강화와 +10 단위 특수 강화 분리
- 보조재료·촉매·정밀 강화는 특수 강화에서만 적용
- +100 수식어 성장
- 고단계 하락·파괴·실패 보정
- 폭주 단조의 2단계 도약 제한
- 목표 단계·자동 보관·보관함 반복 자동 단조
- 실제 게임 값은 `data/**/*.json`, 구현 사실은 GDScript·Scene·테스트가 책임

## 확인된 주요 stale 항목

1. START_HERE·ROADMAP·DEVELOPMENT_GATES가 +5 강화 기준이다.
2. ACTIVE_CONTEXT가 실패 시 단계 유지·파괴 없음으로 남아 있다.
3. Skill Registry가 `default_selection: none`이라 Base 자동 라우팅 계약과 충돌한다.
4. Base 기준 커밋이 미확정이다.
5. 일회성 패치 적용 Workflow가 `main`에 남아 있다.
6. 프로젝트 Skill 문서가 실행 계약과 실패·검증 증거를 충분히 정의하지 않는다.

## 검증 계획

- JSON Registry 구문 검사
- 로컬 참조 경로 존재 여부 검사
- Skill Registry 경로와 Skill 파일 1:1 대조
- START_HERE·Documentation Map·Active Context·Gates 간 상태 용어 대조
- 실제 `data/`, `scripts/`, `scenes/`, `tests/`와 문서 주장 대조
- Godot 4.7.1 프로젝트 파싱·강화 Scene 스모크·모델 테스트
- 데이터 검증
- PR changed files 전수 패치 검토
- 변경됐어야 하지만 untouched인 소비자 검색

## 제외·보류 사유

- Base의 공용 Skill 13개를 프로젝트에 그대로 복제하지 않는다. Blacksmith는 프로젝트 전용 Skill 3개와 Base 기준 연결만 유지한다.
- PDF·DOCX·다이어그램은 현재 도구 실행과 사람 시각 검수가 없으므로 생성·CURRENT 판정을 하지 않는다.
- 승인 이미지가 없으므로 Visual Asset Manifest를 빈 형식으로 강제 설치하지 않는다.
- Android 실기기·AAB·접근성·성능 검증은 실행 환경과 실제 기기 증거가 없으므로 `NOT_RUN`이다.
