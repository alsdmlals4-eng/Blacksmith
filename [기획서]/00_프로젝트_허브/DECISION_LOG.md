# Decision Log

이 문서는 현행 결정과 재검토 조건을 기록한다. 과거 구현 수치와 상세 이력은 Git history·Changelog·MVP Scope가 보존한다.

## DEC-001 Android 모바일과 Google Play

- 상태: `CONFIRMED`
- Android 모바일·Google Play를 1차 목표로 한다.
- Godot 4.7.1, GDScript, 세로 720×1280, AAB, API 36 준비.
- 실제 기기 증거 전에는 모바일 완료로 표시하지 않는다.

## DEC-002 제작 입력

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- 빠른 연속 터치는 피버를 채우며 불이익을 주지 않는다.
- 제작 정밀 입력은 현재 Prototype에서 ON/OFF 가능하다.
- 장비 생애 PoC에서는 느린 게이지·넓은 판정·정밀 보조를 접근성 대안으로 검증한다.

## DEC-003 장비 성장 상한

- 상태: `LATEST_OVERRIDE`
- `+10` 단위 특수 강화와 점증 위험은 보호한다.
- 정확한 `+100`은 현재 구현·제품 목표이며 프로젝트 코어 불변값은 아니다.
- 최종 상한은 +30 PoC와 장기 피로·경제 증거 뒤 재검토한다.

## DEC-004 재료와 숨은 장비

- 상태: `CONFIRMED / DEFERRED_PARTIAL`
- 주재료·보조재료·촉매를 사용한다.
- 보조재료·촉매는 특수 강화에서만 적용한다.
- 숨은 장비 실제 변환은 First Playable 전 별도 범위다.

## DEC-005 판매 방식

- 상태: `CONFIRMED`
- 고객 직접 방문은 고정 대금과 지연 세계 결과를 제공한다.
- 상인 납품은 지정 조건과 즉시 정산 역할이다.
- 첫 장비 생애 PoC는 검투사 고객만 사용한다.

## DEC-006 단일 대장장이와 단순성

- 상태: `CONFIRMED`
- 직원·복수 대장장이를 사용하지 않는다.
- 자동 단조는 직원 시스템이 아니라 반복 입력 편의 기능이다.
- 일상적 수리 관리는 제외한다.
- 중요한 역사 장비의 선택형 복원은 후속 범위다.

## DEC-007 Prototype 수직 분할

- 상태: `LATEST_OVERRIDE`
- MVP-001: 제작
- MVP-002: 강화·보관·자동 단조
- MVP-003: 장비 한 점의 생애 PoC
- MVP-004: 상인 납품, MVP-003 행동 증거 뒤 재검토

## DEC-008 강화 실패·하락·파괴·보정

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- +1~+10 실패 시 기본 단계 유지.
- +11부터 하락, +30부터 파괴.
- 실패 보정은 실패에 누적하고 성공 시 초기화.
- 파괴 무기는 일상 수리하지 않는다.

## DEC-009 수식어 성장

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- +10 이정표에서 수식어를 추가·성장한다.
- 첫 PoC는 날카로움·화염 계열만 사용한다.
- 장기 +20~+100 티어 구조는 현재 제품 목표다.

## DEC-010 강화 조작 주기

- 상태: `CONFIRMED`
- 일반 강화 버튼 한 번당 판정 한 번.
- 일반 강화는 보조재료·촉매·정밀 판정을 사용하지 않는다.
- 특수 강화는 재료 선택과 정밀 판정을 사용한다.

## DEC-011 성장·가격 곡선

- 상태: `IMPLEMENTED_BASELINE / TEST_IN_PLAY`
- 공격력은 현재 강화 적용 공격력을 기준으로 성장한다.
- 고단계 가격·비용·위험을 가속한다.
- 기준선 시뮬레이션은 완료했으며 수치 조정은 장비 생애 경제 입력 뒤 재개한다.

## DEC-012 단조 방식

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- 균형·안정·폭주 단조를 사용한다.
- 폭주는 낮은 확률의 총 2단계 상승이며 특수 강화 이정표를 건너뛰지 않는다.

## DEC-013 장비 보관함

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- 현재 Prototype 보관 상한은 6개다.
- 보관 기록은 제작·강화·수식어·가치·비용을 유지한다.
- 장비 생애 PoC는 납품 뒤 보관함 제거와 세계 기록 생성을 원자적으로 처리한다.

## DEC-014 자동 단조

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE / POC_DEFERRED`
- 현재 Prototype에서 목표·반복·단조 방식·특수 재료를 설정한다.
- 첫 장비 생애 PoC에는 참여하지 않는다.
- 후속 통합 시 +10, 위험 개방 구간과 가치 기준에서 강제 정지한다.

## DEC-015 Base 운영체계 기준

- 상태: `LATEST_OVERRIDE / APPLIED`
- Base 기준 commit은 `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e`다.
- Base 25개 ACTIVE Skill을 프로젝트 Skill 3개와 운영 문서에 매핑한다.
- Work Mode는 PLAN·BUILD·REVIEW다.
- 현행 기준은 `docs/BASE_RULES_VERSION.md`가 책임진다.

## DEC-016 검투사 관전·베팅

- 상태: `DEFERRED`
- 기능 아이디어는 보존하되 MVP-003에서 구현하지 않는다.
- 판매 루프·경제·연령 등급·손실 압박을 검증하고 별도 승인 뒤 재개한다.

## DEC-017 제작 정밀 결과의 현재 구현 효과

- 상태: `IMPLEMENTED_BASELINE / SUPERSEDED_FOR_NEW_RECORDS`
- 현재 Prototype의 STANDARD/GOOD/PERFECT는 공격력·가치에 반영된다.
- 장비 생애 PoC에서는 정밀 결과와 영구 완성도를 분리한다.
- legacy `quality_*` 기록은 별도 호환 변환을 거친다.

## DEC-018 품질별 실제 정수 공격력과 검증 종료코드

- 상태: 확정·구현
- 철검 원본 공격력 20.
- 현재 Prototype 정밀 결과 기준 공격력 20/21/22.
- 피버 적용 실제 공격력 21/22/23.
- 테스트 PASS 문구, 프로세스 종료코드와 오류 로그를 모두 확인한다.

## DEC-019 Godot AI 벤더 연동

- 상태: `APPLIED / LOCAL_INTEGRATION_UNVERIFIED`
- `addons/godot_ai/` 벤더 경계를 유지한다.
- 필수 진입점과 Godot 파싱은 CI에서 검증한다.
- 로컬 MCP 서버·클라이언트 연결은 환경 증거 전 `UNVERIFIED`다.

## DEC-020 제작 피버 결과 보너스

- 상태: `IMPLEMENTED_BASELINE / REQUIRES_PLAYTEST`
- 피버 1회 이상 현재 공격력 ×1.05·가치 ×1.03 보너스를 적용하고 중첩하지 않는다.
- 수동 광클 의미와 입력 피로는 실제 플레이로 재검토한다.

## DEC-021 강화 실패 정책 단일 정본

- 상태: `CONFIRMED / IMPLEMENTED_BASELINE`
- 실패·보정·하락·파괴 수치는 `enhancement_balance.json`이 책임진다.
- `enhancement_milestones.json`은 특수 강화·수식어 이정표만 책임진다.

## DEC-022 위험·가격 기준선 시뮬레이션

- 상태: `BASELINE_COMPLETE / FOLLOW_UP_DEFERRED`
- Issue #29의 15개 조합 × 1,000회 기준선과 판정 보고가 완료됐다.
- 추가 후보 조정, 자동 반복 장기 성능과 실제 손실 피로는 장비 생애 PoC 이후 재개한다.
- 시뮬레이션은 손맛·Android·외부 플레이를 대신하지 않는다.

## DEC-023 프로젝트 코어 확정

- 상태: `CONFIRMED / RECORDED`
- 한 명의 대장장이가 장비 한 점의 출생·성장·소유·사건 기록을 만든다.
- 뾰족한 재미는 장비의 운명을 직접 결정하고 세계 결과를 돌려받는 것이다.
- 무기·방어구·악세서리 3계열을 장기 상위 범주로 사용한다.
- 첫 PoC는 철검만 사용한다.

## DEC-024 피로도·날짜 진행

- 상태: `CONFIRMED / IMPLEMENTATION_NOT_STARTED`
- 피로도는 하루 작업량이며 터치당 스태미나가 아니다.
- 날짜는 플레이어의 `하루 마치기` 입력으로만 진행한다.
- 남은 피로도의 50%를 소수점 버림으로 이월하고 별도 상한을 두지 않는다.
- 작업 예약은 사용하지 않는다.

## DEC-025 장비 생애 PoC

- 상태: `CONFIRMED / SPEC_READY / IMPLEMENTATION_NOT_STARTED`
- Issue #34와 `docs/MVP-003_SCOPE.md`가 실행 범위를 책임진다.
- +5는 기본 납품, +10은 선택적 욕심 구간이다.
- 결과는 최소 하루 지연되고 장비 이력·명성·관계·재방문으로 환류한다.
- DEFEAT/WIN/DECISIVE_WIN 대표 반례가 모두 도달 가능해야 한다.
- 골드·재료·피로도·납품은 원자 거래로 처리한다.
- Android·접근성·성능·외부 플레이는 증거 전까지 `NOT_RUN`이다.
