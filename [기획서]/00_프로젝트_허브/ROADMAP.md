# Blacksmith Roadmap

## 현재 운영 상태

```yaml
CURRENT_DECISION: BS-OPS-20260802-01
CURRENT_WORK_MODE: TOTAL_PLANNING
CURRENT_STAGE: R0_CANONICAL_RECOVERY
CURRENT_DRAFT_PR: 84
PRODUCT_IMPLEMENTATION: BLOCKED
NEXT_PLANNING_BUNDLE: R1_PROJECT_CORE_AND_PLAYER_PROMISE
```

현재 목표는 기능을 더 구현하는 것이 아니라, 승인 결정·기존 기획·실제 구현·Google Sheet의 권위를 복구한 뒤 전체 기획을 분야별로 완성하고 검수하는 것이다.

## R0 — 운영·정본 복구

### 목표

- current main 기준의 진입 문서·Decision 원장·Registry·Base Adapter 복구
- PR #81 전체 병합 대신 승인 기획 선별 승격 구조 확정
- GitHub·Google Sheet 동일 Decision ID 동기화
- Issue·PR 권위 관계 정리
- 적대적 검토·콜드 스타트·exact-HEAD 검증

### 현재 상태

| 항목 | 상태 |
|---|---|
| 승인 설계 | `PASS` |
| 실행 계획 | `PASS` |
| 기준선 Finding | `RECORDED` |
| Root Decision 원장 | `CREATED` |
| 핵심 진입 문서 | `RECOVERY_IN_PROGRESS` |
| Registry·Base Adapter·Health | `PENDING` |
| Google Sheet | `SYNC_PENDING` |
| Issue·PR 권위 | `PENDING` |
| 최종 적대적 검토 | `PENDING` |
| 보호 제품 경로 | `UNCHANGED_AT_LAST_CHECKPOINT` |

### 완료 조건

```yaml
CANONICAL_RECOVERY_GATE: PASS
DECISION_SYNC_GATE: PASS
PLANNING_COVERAGE_GATE: NOT_STARTED
CODEX_IMPLEMENTATION_GATE: BLOCKED
```

## R1 — 프로젝트 코어·플레이어 약속

### 핵심 질문

- 어떤 플레이어가 어떤 상황에서 이 게임을 켜는가?
- 한 문장 약속과 남길 감정은 무엇인가?
- 반복 행동 중 가장 중요한 고민과 선택은 무엇인가?
- 장비 한 점의 생애와 강화 위험 중 무엇이 코어이고 어떻게 결합되는가?
- 제거하면 정체성이 무너지는 요소와 변경 가능한 외피는 무엇인가?
- 세일즈포인트 최대 3개는 무엇인가?
- 모바일·1인 개발·Godot 제약에서 명시적 제외 범위는 무엇인가?

### 입력

- `CURRENT_CONFIRMED_DECISIONS.md`
- 기존 Project Core spec과 Game Bible
- 실제 Prototype/PoC 구현
- PR #81의 승인·제안 자료
- Google Sheet current/history
- 경쟁·유사 게임 Evidence와 반증

### 산출물

- 프로젝트 코어 정본
- 플레이어 약속
- 뾰족한 재미
- 비타협 조건·변경 가능한 외피·제외 범위
- 중요 충돌이 있을 경우 Grill Me Decision

### Gate

`USER_REVIEW_REQUIRED`.

## R2 — Core·Session·Meta Loop

### 범위

- 첫 행동부터 세션 종료까지의 반복 구조
- 제작→강화→멈춤/도전→판매·납품→결과→성장
- 즉시·세션·장기 보상
- 실패·재도전·복귀
- 일반 반복과 기억에 남는 하이라이트
- 온보딩과 정보 공개

### 중요 검토

- +5/+10 일상 루프와 +50 장기 목표가 서로를 약화하지 않는가
- 세계 결과가 핵심 루프를 강화하는가, 기다림만 늘리는가
- 자동화가 핵심 선택을 우회하지 않는가

### Gate

`R1_APPROVED` 후 시작.

## R3 — 제작·강화·작품 정체성·실패·저장

### 범위

- 제작 입력과 완성도
- 일반·특수·정밀 강화의 책임 분리
- 제작 등급·계보·보조 수식어
- 하락·파괴·보호·완충
- 장비 UID와 불변 정체성
- SaveStatus·AttemptIntent·ResultEnvelope
- Legacy migration과 호환성

### 기본값 정책

확률·비용·용량·시간·간격은 먼저 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 제안한다. 플레이어 애착·공정성·장기 경제를 근본적으로 바꾸는 경우만 Grill Me로 승격한다.

### Gate

`R2_APPROVED` 후 시작.

## R4 — 고객·판매·세계 환류·장비 연대기

### 범위

- 고객 직접 방문과 상인 납품
- 의뢰·적합도·선택·보상
- 판매·납품 뒤 소유권과 장비 연대기
- 지연 결과·재방문·관계·명성
- 대표 고객과 콘텐츠 제작 파이프라인
- 시장·경기장·전쟁의 표현 경계

### 중요 검토

- 고객 소유 장비의 파괴와 복구 경계
- 세계 환류가 결과 연출인지 플레이 가능한 외부 장소인지
- 직접 전투 범위 팽창 여부

### Gate

`R3_APPROVED` 후 시작.

## R5 — 경제·성장·장기 목표

### 범위

- 골드·재료 Source/Sink
- 장비 가치·판매·명성·관계
- 보호·실패 완충·인플레이션
- 보관함과 작품 관리
- +50 이후 성장 중심
- Hall of Masterpieces·랭킹 등 미래 온라인 경계
- 악용·무한 루프·소프트락·복구

### 검증

- 수치 시뮬레이션
- 경계 조합
- 세션과 장기 피로
- 실제 플레이 이전의 불확실성 명시

### Gate

`R4_APPROVED` 후 시작.

## R6 — 모바일 UX·접근성·아트·오디오·피드백

### 범위

- 별도 Main Menu와 단일 BlacksmithApp 정보 구조
- View·Overlay·뒤로가기·오류 복구
- Android portrait, safe area, one-hand flow
- 장비 중심 화면과 비교 정보량
- 위험·확률·소유권·결과 설명
- 스타일라이즈드 다크 포지
- 밝은 불 정령 모닥
- 애니메이션·이펙트·사운드 정보 전달
- 색상 이외 정보 채널·텍스트 크기·모션 감소

### 플랫폼 경계

- Android 모바일이 현재 출시 범위다.
- PC는 데이터·입력 추상화 고려만 하며 동시 UI 품질 요구로 확장하지 않는다.

### Gate

`R5_APPROVED` 후 시작.

## R7 — 버티컬 슬라이스·데이터·마이그레이션·검증·제작 계획

### 범위

- 15~25분 대표 세션과 데모 종료 지점
- 포함 시스템·대표 콘텐츠·명시적 제외
- 기존 구현 재사용·대체·삭제 금지 경계
- Schema·ID·저장·migration
- 자동 테스트·Godot·Android·접근성·성능·사람 플레이
- 반복 콘텐츠 제작 가능성
- Build·패키징·배포 준비
- Codex 실행 Packet 초안

### 완료 기준

모든 승인 기획은 버티컬 슬라이스 범위에서 다음 중 하나다.

```text
IMPLEMENTED_AND_VALIDATED
또는
EXPLICITLY_EXCLUDED_WITH_DECISION_ID
```

기획 단계에서는 구현 위치·검증 계약·제외 Decision까지 정의하며 실제 구현 완료는 주장하지 않는다.

### Gate

`R6_APPROVED` 후 시작.

## R8 — 최종 적대적 검수·사용자 검수

### 적대적 검토

- 플레이어 약속 ↔ 실제 반복 행동
- Core Loop ↔ 보상·경제·장기 성장
- 시스템 복잡도 ↔ 모바일 온보딩·가독성
- 콘텐츠 구조 ↔ 1인 제작량
- 장비 애착 ↔ 파괴·복구·판매
- 세계 환류 ↔ 직접 전투·범위 팽창
- UX·아트·사운드 ↔ 정보 전달
- 데이터·저장 ↔ 비가역 결과
- Vertical Slice ↔ 대표 경험·제작 파이프라인
- GitHub 정본 ↔ 실제 구현 ↔ Sheet

### Gate 순서

```text
사용자 기획 완료
→ 전체 적대적 검수
→ validated finding 수정
→ 사용자 검수 완료
```

미해결 `MUST_FIX`, 미동기화 Decision, 미확정 중요 선택이 있으면 완료하지 않는다.

## R9 — Codex 구현 인계

R9는 현재 `BLOCKED`다.

필수 입력:

- 승인 Decision IDs
- exact canonical baseline commit
- 기능·콘텐츠·UI·데이터의 정확한 범위
- 보호할 동작·에셋·인터페이스
- 실제 파일·Scene·Resource·Schema
- 구현 순서와 TDD
- 저장·migration·호환성
- Android·접근성·성능 조건
- 자동·수동 테스트와 기대 결과
- GitHub·Sheet 갱신 위치
- Rollback

Codex는 기획 공백을 추측하거나 주요 기능을 임의 삭제·대체하지 않는다.

## Historical Implementation Baseline

기존 MVP-001·002·003 구현과 과거 자동 검증은 보존한다.

- 역할: actual implementation facts and regression baseline
- 현재 총기획 권위: `REFERENCE_IMPLEMENTATION`
- Android·접근성·성능·외부 플레이: `NOT_RUN`
- 별도 Main/Shell/Save 최신 계약: `NOT_IMPLEMENTED`

과거 순서와 상태는 Git history, 기존 Scope·Status·Issue·PR이 보존한다. 이 Roadmap의 현재 실행 순서는 R0~R9다.

## Production Greenlight

다음이 모두 실제 증거로 닫히기 전 Production 또는 Demo Ready를 주장하지 않는다.

- 승인 전체 기획과 명시적 제외 Decision
- 제품 구현과 회귀 테스트
- 저장·복구·migration
- 실제 Android 빌드·기기
- 접근성 사람 검토
- 대표·최악 장면 성능
- 외부 플레이 행동 증거
- Build·패키징·설치·실행
- GitHub·Sheet·실제 구현 일치
