# Base 적용 기준

- Base 저장소: `alsdmlals4-eng/Base`
- Base 기준 브랜치: `main`
- Base 기준 커밋: `ee265576da7f67d3278f8099dd97d4e714ef0651`
- 동기화일: 2026-07-22
- 대상 프로젝트: `alsdmlals4-eng/Blacksmith`
- 적용 방식: 공용 저장소 전체 복제가 아니라 현재 프로젝트에 필요한 책임 원본·라우팅·검증 계약을 분화
- 상세 대조: `docs/BASE_ADOPTION_AUDIT.md`

## 적용한 공용 계약

- 사용자 지시·프로젝트 정본·실제 구현 우선순위
- `PLAN / BUILD / REVIEW` Work Mode
- trigger 기반 최소 Skill 자동 선택
- 한 질문당 단일 책임 원본
- Markdown 설명 / JSON 구조·수치 / Script·Scene 구현 사실 분리
- Active Context·Documentation Map·Development Gates·Registry 연결
- 구형 파일 보존·참조·복구 기반 처리
- 정본·경로·ID·Schema 변경의 untouched 소비자 감사
- 정적·런타임·회귀·증거 보고
- 실행하지 않은 검증을 `NOT_RUN` 또는 `UNVERIFIED`로 표시

## 프로젝트 전용 차이

- Godot 4.7.1 + GDScript + Android 세로형 720×1280을 기술 기준으로 사용한다.
- 프로젝트 전용 Skill은 game-design·engineering·qa 세 개만 유지하고 Base 공용 Skill 13개를 복제하지 않는다.
- 기획 책임 원본은 현재 `BLACKSMITH_GAME_BIBLE.md` 한 권을 중심으로 하며 실제 게임 값은 `data/**/*.json`이 책임진다.
- PDF·DOCX·다이어그램 발행은 현재 `NOT_RUN`이며 사람 검수 없이 `CURRENT`로 표시하지 않는다.
- 승인 이미지 파이프라인이 생기기 전까지 빈 Asset Manifest를 강제 설치하지 않는다.
- Android 실기기·AAB·접근성·성능은 실제 증거가 생길 때까지 미검증 상태로 유지한다.

## 다음 동기화 조건

다음 중 하나가 발생하면 Base 최신 커밋을 다시 감사한다.

- Base Operating Model·Skill Registry·프로젝트 운영체계 Skill 변경
- Blacksmith 문서 구조·Registry·Skill·발행 정책 변경
- 주요 제품 게이트 진입
- 콜드 스타트 실패 또는 오래된 활성 참조 발견
