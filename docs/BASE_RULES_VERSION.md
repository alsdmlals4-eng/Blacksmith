# Base 적용 기준

- Base: `alsdmlals4-eng/Base`
- 기존 Base 기준 커밋: `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 신규 adapter-only 공용 route 커밋: `a8218b454bcfd9e72c792f4bb8ed614a385e22d6`
- 동기화일: 2026-07-25
- 대상: `alsdmlals4-eng/Blacksmith`
- 상세 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 감사 결과: `docs/BASE_ADOPTION_AUDIT.md`
- 공용 route Registry: `[기획서]/00_프로젝트_허브/BASE_SHARED_SKILL_ROUTES.json`
- 프로젝트 어댑터: `[기획서]/00_프로젝트_허브/BASE_SHARED_SKILL_ADAPTER.json`
- 제3자 자산·플러그인 기록: `[기획서]/00_프로젝트_허브/THIRD_PARTY_ASSET_AND_PLUGIN_INVENTORY.json`

## 적용 방식

Base 공용 Skill 본문을 프로젝트에 복제하지 않는다. 기존 공용 운영 기능은 현재 동기화 구조를 유지하고, 신규·갱신되는 Base 공용 Skill은 route Registry와 프로젝트 어댑터로 연결한다. 프로젝트 로컬 Skill은 Blacksmith 고유 규칙과 구현·검증 책임에만 만든다.

```text
기존 Base 25개 활성 기능 @ 41a20584...
→ 프로젝트 운영 문서와 기존 통합 구조

신규 adapter-only 공용 Skill @ a8218b45...
→ BASE_SHARED_SKILL_ROUTES.json
→ BASE_SHARED_SKILL_ADAPTER.json
→ Blacksmith 경로·정본·검증기

Blacksmith 고유 책임
→ blacksmith-game-design
→ blacksmith-engineering
→ blacksmith-qa
```

각 기능의 보존 위치·호출 조건·통합 상태는 Profile과 Registry가 책임지고, 신규 공용 route는 프로젝트 어댑터가 경로·정본·검증기를 제공한다.

## 신규 공용 route

- `governing-legacy-retention-and-archives`: 구형·중복 자료의 고유 정보·참조·복구·승인을 확인하고 통합·stub·아카이브·승인 삭제를 판정한다.
- `evaluating-godot-assets-and-plugins-before-creation`: 새 Godot 기능·도구·자산을 만들기 전에 기본 기능, 공식 Store, 기존 Asset Library, GitHub, itch.io와 상용 후보를 조사한다.

Godot 기능·에셋·플러그인은 검색과 평가를 먼저 수행한다. 구매·계정 연결·프로젝트 설치·Android 네이티브 플러그인 추가는 별도 사용자 승인 범위에서만 수행한다.

## 유지 계약

- 사용자 지시 → 프로젝트 정본·구현 → 동기화된 Base 기준 순서
- `PLAN / BUILD / REVIEW`
- trigger 기반 최소 Skill 자동 선택
- Base 공용 Skill은 adapter-only, 프로젝트 전용 Skill은 local-only
- 단일 책임 원본과 Markdown / JSON / 구현 사실 분리
- Active Context·Map·Gates·Registry 연결
- 구형 파일의 고유 정보·참조·복구·승인 보존
- 정본·경로·ID·Schema의 untouched 소비자 감사
- 프로젝트 코어 식별과 사용자 승인 기반 확정 분리
- 적대적 검토 → 비판 검증 → 최소 승인 개선 → 회귀 재검토
- 동작·인터페이스·데이터 호환성을 보존하는 리팩터링
- Skill 본문은 상시 계약만 유지하고 조건부 상세는 reference로 분리
- 죽은 자료·중복·오래된 참조는 기능과 복구 경계를 보존하며 정리
- 장기 작업은 checkpoint·부분 산출물·정확한 재개 지점을 유지
- 정적·런타임·회귀·증거 보고
- 미실행은 `NOT_RUN`

## 프로젝트 차이

- Godot 4.7.1 / GDScript / Android 세로형 720×1280
- 프로젝트 Skill은 3개만 유지하며 Blacksmith 고유 경험·데이터·구현·검증만 책임진다.
- 실제 수치는 `data/**/*.json`, 구현 사실은 Script·Scene·Test
- PDF·DOCX·다이어그램·Asset Manifest는 실제 발행·승인 파이프라인이 생길 때 활성화
- Android 실기기·AAB·접근성·성능은 증거 전까지 `NOT_RUN`
- 이미지 생성은 사용자가 명시적으로 요청한 작업에서만 활성화
- 기존 `godot_ai` 애드온은 출처·버전·라이선스가 확인되기 전 `EXISTING_REVIEW_REQUIRED`

## Base 환류

Blacksmith 교훈을 Base에 직접 덮어쓰지 않는다.

```text
extract → submit → review → 사용자 승인 → 별도 implement PR → verify
```

여러 작업에서 반복 검증된 공용 교훈만 제안한다. 프로젝트 전용 Skill에서 공용 절차가 확인되면 Base 승격 후 어댑터 route로 전환한다.

## 검증

```text
python -m json.tool "[기획서]/00_프로젝트_허브/BASE_SHARED_SKILL_ROUTES.json"
python -m json.tool "[기획서]/00_프로젝트_허브/BASE_SHARED_SKILL_ADAPTER.json"
python -m json.tool "[기획서]/00_프로젝트_허브/THIRD_PARTY_ASSET_AND_PLUGIN_INVENTORY.json"
python tools/validate_game_data.py
```

운영 JSON과 문서만 변경한 이번 범위에서는 Godot 런타임·Android 실기기·AAB 검증을 자동 PASS로 표시하지 않는다.

## 재동기화 조건

- Base Operating Model·Skill Registry·공용 route Registry·어댑터 계약 변경
- Blacksmith Registry·책임 구조·발행 정책 변경
- Godot 버전·목표 Android API·`addons/`·제3자 라이선스 변경
- 주요 제품 게이트 진입
- 콜드 스타트 실패·stale 참조·감사 CI 실패
