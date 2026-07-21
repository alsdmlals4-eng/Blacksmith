# Base 적용 기준

## 동기화 기준

- Base 저장소: `alsdmlals4-eng/Base`
- Base 기준 브랜치: `main`
- Base 기준 커밋: `ee265576da7f67d3278f8099dd97d4e714ef0651`
- Blacksmith 기준 커밋: `4ab49d32788cf3ccbf50ed078e6dae1d346ad2e5`
- 동기화·감사일: 2026-07-21
- 적용 Issue: `#14 OPS-002 최신 Base 운영체계 전면 감사·보존형 마이그레이션`

프로젝트 작업 중에는 이 문서에 고정된 Base 기준을 우선한다. Base 원격 최신 상태를 매 작업에 암묵적으로 적용하지 않고, 별도 업데이트 감사에서만 비교한다.

## 적용 방식

Base 전체를 복제하지 않는다. Documentation Map과 Skill Registry에서 Blacksmith의 현재 작업에 필요한 공용 계약을 골라 프로젝트 경로·엔진·수치·상태에 맞게 분화했다.

적용한 핵심:

- `PLAN / BUILD / REVIEW` Work Mode
- trigger 기반 최소 Skill 자동 라우팅
- 실행 계약과 실행 증거 보고
- 기존 프로젝트 audit·보존형 migrate·verify
- 한 질문당 단일 Markdown/JSON 책임 원본
- Active Context·Roadmap·Development Gates·Decision Log 분리
- 정본·경로·ID·Schema 변경의 참조 최신성 검사
- PR 파일별 체크리스트와 자동 Governance
- 자동 검증·실제 렌더·Android 실기기·사람 검수 상태 분리

## Blacksmith 프로젝트 차이

- 기획 책임 원본은 소규모 프로젝트에 맞춰 통합 Game Bible과 MVP 범위 문서를 사용한다.
- 실제 강화 수치·재료·수식어는 `data/**/*.json`이 소유한다.
- 실제 구현 상태는 Godot Scene·GDScript·테스트가 소유한다.
- 선택 분야는 게임 디자인, UX·UI·접근성, 개발·엔지니어링, QA, 통합검수다.
- 프로젝트 Skill Map PDF와 Game Bible PDF는 현재 생성하지 않았으며 `NOT_BUILT/NOT_RUN`이다.
- DeepSeek worktree, 아트 생성, 사운드, Base 변경 제안은 현재 trigger가 없어 설치·실행하지 않았다.
- Android 실기기·AAB·성능 프로파일·사람 시각 검수는 미실행이다.

## 업데이트 절차

```text
Base 새 커밋 확인
→ START_HERE·AGENTS·OPERATING_MODEL·DOCUMENTATION_MAP·SKILL_REGISTRY 변경 비교
→ Blacksmith 영향 지도 작성
→ 별도 Issue·브랜치·PR
→ 보호 범위 확인
→ 필요한 최소 문서·Skill·검사만 갱신
→ 정본·참조 최신성·Godot·JSON 회귀 검증
→ 이 문서의 Base 커밋 갱신
```
