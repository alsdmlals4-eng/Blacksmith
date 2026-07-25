# Base 공용 Skill 연결 기준

`Blacksmith`는 Base 공용 Skill 본문을 복제하지 않고 route Registry와 프로젝트 어댑터로 사용하며, 제작·강화·고객·경제처럼 Blacksmith 고유 책임만 프로젝트 Skill로 관리한다.

## 기준과 경로

- 공용 Skill 기준: `alsdmlals4-eng/Base@6a224e450f9420223c00921f3c56e051612f92ad`
- 공용 route: `skills/BASE_SHARED_SKILL_ROUTES.json`
- 프로젝트 어댑터: `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- 아카이브 어댑터: `docs/archive/ARCHIVE_RETENTION_ADAPTER.json`
- 프로젝트 Skill Registry: `[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json`

`docs/BASE_RULES_VERSION.md`의 전체 운영체계 기준과 이 공용 Skill 기준은 별도 책임이다. 공용 Skill pin 갱신으로 다른 Base 정책을 자동 강제하지 않는다.

## 라우팅

```text
작업 요청
→ Base 메인 skills/SKILL_REGISTRY.json 자동 trigger 선택
→ skills/PROJECT_BASE_SKILL_ADAPTER.json으로 프로젝트 경로·정본·검증기 주입
→ 필요할 때만 Blacksmith 고유 Skill 선택
```

- 레거시·아카이브: `governing-legacy-retention-and-archives`.
- Godot 직접 생성 전 자산 탐색: `evaluating-godot-assets-and-plugins-before-creation`.

## 직접 생성 전 조사

```text
Godot 기본 기능 → 공식 Asset Store → 기존 Asset Library
→ 제작자 GitHub 안정 Release·tag → itch.io → 공식 판매처·상용 마켓
→ ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM
```

모바일 UI, Safe Area, 인벤토리, 제작 데이터 보조, Android 빌드와 터치 피드백을 우선 조사한다. 제작 판정, 고객 반응과 핵심 경제 루프는 외부 플러그인에 맡기지 않는다.

## 기록·검증

- 채택 자산: `docs/technical/ADOPTED_ASSETS.md`
- 라이선스: `docs/technical/THIRD_PARTY_LICENSES.md`
- 아카이브: `docs/archive/README.md`, `docs/archive/MANIFEST.json`
- 정적 검사: `python tests/test_base_shared_skill_adapter.py`
- Godot·Android 실기기·AAB·Safe Area는 실행 전까지 `NOT_RUN`이다.
