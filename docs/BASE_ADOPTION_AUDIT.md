# Base 적용·가지치기 감사

## 기준

- Base: `alsdmlals4-eng/Base@ee265576da7f67d3278f8099dd97d4e714ef0651`
- 대상: `alsdmlals4-eng/Blacksmith`
- 전략: Base 기능을 복제하지 않고 프로젝트 운영 문서와 Skill 3개로 통합
- 기능 매핑: `docs/BASE_ADOPTION_PROFILE.json`
- 자동 감사: `tools/audit_project_operating_system.py`

## 읽기·검증 범위

CI가 Base 고정 커밋 전체를 checkout하고 다음을 실행한다.

1. Base의 모든 텍스트형 파일을 전수 스캔한다.
2. Base Skill Registry의 13개 ACTIVE Skill과 패키지 경로를 확인한다.
3. Base의 Skill 패키지·운영체계·프로젝트 Skill Map·통합 reference·freshness 테스트를 실행한다.
4. 13개 기능이 Blacksmith Profile에 빠짐없이 매핑됐는지 확인한다.
5. Blacksmith의 Registry·Skill Mode·책임 원본·로컬 경로·stale 활성 설명·런타임 필수 경로를 검사한다.

## 가지치기 결과

| 구분 | 결과 |
|---|---|
| 프로젝트 Skill 수 | 3개 유지 |
| 게임 디자인 | 조사·DDD·밸런스·플레이테스트·PoC·Vertical Slice·아트 방향 통합 |
| 엔지니어링 | Godot·데이터·Android·저장·자동화 통합 |
| QA | 계약·외부 결과·reference-freshness·정적·런타임·접근성·성능·UI·회귀 통합 |
| Foundation | Work Mode·작업 계약·문서·Context·운영 감사는 프로젝트 허브 문서가 담당 |
| 외부 AI | 필요할 때만 격리 작업 공간으로 라우팅하고 결과를 QA가 검수 |
| Base 환류 | 반복 검증된 공용 교훈만 별도 제안·승인·구현 PR로 처리 |

삭제한 기능은 없다. 독립 패키지가 불필요한 기능만 Mode 또는 운영 문서로 통합했다.

## 정본 동기화

다음 stale 상태를 현행 `POC v0.6.0` 기준으로 교정했다.

- +5 중심 강화 설명 → +100 일반·특수 강화
- 전 구간 파괴 없음 → +11 하락, +30 파괴
- 5개 테스트 기준 → 최신 강화 모델 검증
- 폭주 성장 증폭 → 낮은 확률 총 2단계 도약과 이정표 차단
- 자동 단조 없음 → 목표·자동 보관·반복·재료 fallback·중지 조건
- 수동 Skill 선택 → trigger 기반 자동 선택
- 미확정 Base 버전 → 고정 commit과 재동기화 조건

게임 코드·데이터·Scene 동작은 이 운영체계 PR에서 변경하지 않는다.

## 안전 정리

- 완료된 일회성 `.github/workflows/materialize-auto-forge.yml`: `DELETE_APPROVED`
- `project.godot`의 일회성 검증 주석: 제거
- PDF·DOCX·다이어그램·Asset Manifest: 파이프라인·승인 근거가 없으므로 `NOT_RUN`, 빈 구조를 강제하지 않음
- Android 실기기·AAB·사람 시각·접근성·성능: 증거 전까지 `NOT_RUN`

## PR 게이트

- [ ] Base 고정본 자체 테스트 PASS
- [ ] Base 13개 기능 매핑 1:1 PASS
- [ ] Blacksmith Skill 3개와 Registry Mode 일치 PASS
- [ ] 로컬 경로·책임 원본·stale 활성 설명 감사 PASS
- [ ] JSON 데이터 검증 PASS
- [ ] Godot 4.7.1 import·parse PASS
- [ ] 강화 Scene 스모크 PASS
- [ ] 제작·강화 모델 테스트 PASS
- [ ] changed files 전수 patch 검토 PASS
- [ ] untouched 소비자·삭제 참조 검토 PASS
- [ ] Android·AAB·시각·접근성·성능은 `NOT_RUN`으로 명시

차단 finding이 하나라도 있으면 병합하지 않는다.
