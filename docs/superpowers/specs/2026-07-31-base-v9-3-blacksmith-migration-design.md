# Base v9.3 Blacksmith 운영 계약 마이그레이션 설계

> 상태: `APPROVED_FOR_IMPLEMENTATION`
>
> 추적 Issue: #79
>
> 제품 구현 권한: `NONE`

## 1. 목표

블랙스미스(Blacksmith)의 운영 기준을 `Base v9.3.0`과 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`로 단일화한다. 기존 v6~v8 계약과 PR·Issue·기획 자료는 삭제하지 않고 요구사항 추적·호환 이력으로 보존한다.

이번 마이그레이션은 Android 모바일 제품을 변경하지 않는다. 향후 `+50` 이상 고등급 작품을 서버 랭킹에 등록해 등급과 수식어를 비교할 수 있도록, 데이터·권한·보안 경계만 미리 정의한다.

## 2. 프로젝트 바인딩

| 항목 | 값 |
|---|---|
| 프로젝트 | 블랙스미스(Blacksmith) |
| 저장소 | `alsdmlals4-eng/Blacksmith` |
| 기준 main | `500a5a7960146ef229ae172cf9e127306d23f073` |
| 플랫폼 | Android 모바일 / 세로형 720×1280 |
| 엔진 | Godot 4.7.1 / GDScript |
| Sheet | `1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg` |
| Base version | `9.3.0` |
| Base release | `30ca6c7b5f93521f0eb0eed42d01437cd43c50ae` |
| Base evidence | `462a86db192d23d0f386281a1eb54b0a8cbad62e` |
| Base Registry SHA-256 | `9847bb2b225c776ad7916930f0f48c490bc2a898bea8e02ea1fdd0e6caac60c1` |
| 실행문 | `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` |

## 3. 권한 모델

1. 사용자 최신 지시
2. `AGENTS.md`
3. Active Context·Decision·Documentation Map
4. 프로젝트 Adapter·Snapshot·Router와 프로젝트 Skill 3개
5. Base v9.3 release/evidence에 고정된 공용 계약
6. v6~v8 `LEGACY_REFERENCE_ALLOWED / SUPERSEDED_COMPATIBILITY`
7. 실제 제품 파일과 테스트

`skills/PROJECT_BASE_ADAPTER.json`을 Base 핀·라우팅·보호 경로의 기계 판독 정본으로 사용한다. `skills/BASE_V9_ADAPTER.json`, `skills/PROJECT_BASE_SKILL_ADAPTER.json`, `skills/PROJECT_SKILL_SNAPSHOT.json`, Dashboard와 router는 파생본이다.

## 4. 변경 범위

### 운영 계약

- Adapter를 Base v9.3 lock에 정렬
- 실제 Sheet를 `CURRENT`로 기록하고 저장소 Workbook 문서를 증거로 연결
- 프로젝트 Skill Registry의 Base 통합 메타데이터를 release/evidence/hash 기준으로 갱신
- v8 활성 문구와 구형 Base SHA 하드코딩 테스트 제거
- Blacksmith Vertical Slice v9 Application Binding과 Reconciliation Packet 추가
- v6 기반 Issue #60·#69는 v9 실행 권한으로 갱신하되 기존 기록은 보존

### 프로젝트 Skill

프로젝트 Skill은 다음 3개만 유지한다.

- `blacksmith-game-design`
- `blacksmith-engineering`
- `blacksmith-qa`

서버 관련 책임은 새 Skill을 만들지 않고 기존 3개에 다음 모드로 분담한다.

- 게임 디자인: 공개 비교 경험, 등록 조건, 시즌·보상 가설
- 엔지니어링: API·저장·오프라인 큐·idempotency·버전 경계
- QA: 서버 권위 검증·부정 등록·개인정보·삭제·호환성

## 5. 미래 고등급 작품 랭킹 계약

상태는 `FUTURE_SERVER_READY / NOT_IMPLEMENTED`다.

### 사용자 가치

플레이어는 어렵게 완성한 고강화 작품을 다른 플레이어의 작품과 비교하며 장비의 희소성·개성·성취를 확인한다. 단순 숫자 경쟁보다 `강화 단계 + 등급 + 수식어 조합`을 읽을 수 있어야 한다.

### 등록 조건

- 강화 단계 `+50` 이상
- 서버가 인정하는 완성 작품 상태
- 공개 등록에 대한 사용자의 명시적 동의
- 지원되는 게임·밸런스·데이터 Schema 버전

### 공개 데이터 최소 집합

- 공개용 작품 ID
- 공개 표시명 또는 익명 표시명
- 장비 종류와 작품 이름
- 강화 단계
- 등급
- 수식어 ID·표시명·표시 순서
- 밸런스 시즌·게임 버전
- 서버 검증 상태와 등록 시각

로컬 저장 전체, 장치 식별자, 원본 사용자 ID, 구매 정보, 비공개 장비 이력은 공개 랭킹 Payload에 포함하지 않는다.

### 권위와 무결성

- 클라이언트가 제출한 랭킹 점수나 등급을 그대로 신뢰하지 않는다.
- 서버는 작품 생성·강화 이력의 검증 가능한 스냅샷 또는 서명된 요약을 기준으로 정렬 키를 계산한다.
- 동일 작품의 중복 등록은 idempotency key로 방지한다.
- 조작 의심·지원 종료 버전·Schema 불일치는 `REJECTED / QUARANTINED`로 분리한다.
- 서버 실패가 로컬 작품이나 싱글플레이 진행을 훼손하지 않는다.

### 오프라인 우선

- 서버 미연결 상태에서도 제작·강화·저장·불러오기가 동작한다.
- 업로드 대기 큐는 별도 상태이며 작품 소유권·로컬 저장 성공과 분리한다.
- 재시도는 중복 안전하고 취소 가능해야 한다.
- 랭킹 조회 실패 시 마지막 캐시 또는 명확한 오프라인 상태를 표시한다.

### 후속 구현 전 필수 결정

- 인증 방식과 공개 표시명 정책
- 서버·DB·호스팅 선택
- 시즌제와 영구 명예 기록의 관계
- 동점 정렬 규칙
- 부정행위 탐지·이의제기·삭제 요청
- 미성년자·개인정보·지역 정책
- API 비용·장애·백업·운영 책임

## 6. 보호 경로

이번 PR에서는 다음 경로를 변경하지 않는다.

- `data/`
- `scripts/`
- `scenes/`
- `assets/`
- `addons/`
- `project.godot`

서버 랭킹 구현도 이 PR에서 시작하지 않는다.

## 7. 검증 설계

### 자동

- Base v9.3 release/evidence/Registry lock 일치
- Adapter·Registry·Snapshot·Compatibility view raw-byte hash 일치
- 프로젝트 Skill 3개와 Base shared route 존재
- v8 실행문·구형 Base SHA의 활성 참조 부재
- Sheet ID·25개 탭 계약 존재
- 미래 서버 계약에 `+50`, 등급, 수식어, 서버 권위, 오프라인 우선, `NOT_IMPLEMENTED` 존재
- 보호 경로 변경 부재

### 상태 분리

- 운영 정적 검증: CI 결과에 따라 판정
- Godot 제품 런타임: 제품 파일 무변경이므로 기존 증거를 보존하고 새 PASS를 주장하지 않음
- Android 실기기·사람 접근성·성능·외부 플레이: `NOT_RUN`
- 서버·API·DB·랭킹 UI: `NOT_IMPLEMENTED`

## 8. 병합과 Sheet 동기화

GitHub PR 검증과 병합을 먼저 완료한다. 병합된 `main`을 재조회한 뒤에만 다음 탭을 갱신한다.

- `00_프로젝트_허브`
- `01_작업순서`
- `04_누락_충돌_감사`
- `05_GDD_요약`
- `80_데모_버티컬슬라이스_플레이테스트`
- `90_본제작_출시_사업`
- `99_변경이력`

Sheet 변경은 GitHub 정본을 대체하지 않으며, 랭킹 서버 항목은 후속 계획 상태로 기록한다.
