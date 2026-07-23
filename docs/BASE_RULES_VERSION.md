# Base 적용 기준

- Base: `alsdmlals4-eng/Base`
- 기준 커밋: `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`
- 동기화일: 2026-07-23
- 대상: `alsdmlals4-eng/Blacksmith`
- 상세 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 감사 결과: `docs/BASE_ADOPTION_AUDIT.md`

## 적용 방식

Base를 복제하지 않는다. 공용 기능은 Blacksmith의 실제 책임 원본과 프로젝트 Skill 3개에 통합한다.

```text
Base 25개 활성 기능
→ 프로젝트 운영 문서
→ blacksmith-game-design
→ blacksmith-engineering
→ blacksmith-qa
```

각 기능의 보존 위치·호출 조건·통합 상태는 Profile이 책임지고, CI가 Base 고정 커밋의 Registry·Skill 무결성과 Blacksmith의 경로·정본·stale 설명을 검사한다.

## 유지 계약

- 사용자 지시 → 프로젝트 정본·구현 → 동기화된 Base 기준 순서
- `PLAN / BUILD / REVIEW`
- trigger 기반 최소 Skill 자동 선택
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
- 프로젝트 Skill은 3개만 유지하되 Base 기능은 Mode와 운영 문서로 보존
- 실제 수치는 `data/**/*.json`, 구현 사실은 Script·Scene·Test
- PDF·DOCX·다이어그램·Asset Manifest는 실제 발행·승인 파이프라인이 생길 때 활성화
- Android 실기기·AAB·접근성·성능은 증거 전까지 `NOT_RUN`
- 이미지 생성은 사용자가 명시적으로 요청한 작업에서만 활성화

## Base 환류

Blacksmith 교훈을 Base에 직접 덮어쓰지 않는다.

```text
extract → submit → review → 사용자 승인 → 별도 implement PR → verify
```

여러 작업에서 반복 검증된 공용 교훈만 제안한다.

## 재동기화 조건

- Base Operating Model·Skill Registry·운영체계 Skill 변경
- Blacksmith Registry·책임 구조·발행 정책 변경
- 주요 제품 게이트 진입
- 콜드 스타트 실패·stale 참조·감사 CI 실패
