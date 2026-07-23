# Roadmap

## Concept — PASS

- 프로젝트 코어: `CORE_CONFIRMED / CORE_RECORDED`
- 한 명의 대장장이, 직접 제작, 영구 완성도, 강화 선택, 세계 장비 이력과 명성 환류
- 직원·직접 전투·작업 예약·일상적 수리 관리 제외
- 정확한 `+100`은 현재 제품 목표이며 코어 불변값은 아님

책임 원본: `docs/superpowers/specs/2026-07-23-project-core-design.md`

## Prototype 구현 기준선 — 유지

### MVP-001 제작

- 철검 제작, 광클·자동 작업, 피버, 제작 정밀 마감
- 제작 결과가 강화·보관으로 전달됨
- 자동 검증 PASS 이력
- 실제 화면·Android: `NOT_RUN`

### MVP-002 강화·보관·자동 단조

- 일반/특수 강화, +11 하락, +30 파괴, 실패 보정
- 균형·안정·폭주 단조
- +100 수식어 성장 목표
- 공유 골드·재료 거래, 보관함, 자동 단조
- 자동 검증 PASS 이력
- 장기 플레이·성능·Android: `NOT_RUN`

### 위험·가격 기준선 시뮬레이션

- Issue #29 기준선 15개 조합 × 1,000회 실행 완료
- Scope·Report·Registry·CI 증거 보존
- 추가 수치 조정은 장비 생애 PoC의 경제 입력이 확인될 때 재개
- 상태: `DEFERRED / TEST_IN_PLAY`

## 장비 한 점의 생애 PoC — CURRENT

- Issue: #34
- Draft PR: #35
- Scope: `docs/MVP-003_SCOPE.md`
- Spec: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- Plan: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- CI policy: `docs/CI_EXECUTION_POLICY.md`
- 상태: `IMPLEMENTATION_CANDIDATE / VALIDATION_DEFERRED`

```text
검투사 의뢰
→ 철검 제작·영구 완성도
→ +5 납품 또는 +10 추가 도전
→ 수동 하루 종료
→ 지연 경기 결과
→ 영구 장비 이력·명성·관계
→ 같은 검투사 재방문
```

### 구현 후보 완료

1. lifecycle 데이터 계약·검증기
2. 날짜·피로도와 50% 이월
3. 정밀 결과·영구 완성도 분리와 legacy 호환
4. 고객 의뢰·납품 적합도
5. 세계 기록·결정적 결과 판정
6. 원자 거래·생애 컨트롤러
7. 로컬 행동 로그
8. 세로 UI·접근성 보조·기존 Prototype 진입점
9. 전체 생애 E2E·CI 구조·정본 동기화

### 현재 검증 게이트

- GitHub Actions 자동 실행: `DEFERRED_UNTIL_ACTIONS_AVAILABLE`
- 신규 head Godot import·main/PoC Scene smoke: `NOT_RUN`
- 신규·기존 Godot 전체 회귀: `NOT_RUN`
- Ubuntu·Windows Python 매트릭스: `NOT_RUN`
- Android·접근성·성능·외부 플레이: `NOT_RUN`

### 종료 기준

- 제작부터 재방문까지 E2E 완주 PASS
- +5 납품과 +10 추가 도전이 모두 유효
- DEFEAT/WIN/DECISIVE_WIN 반례가 모두 도달
- 골드·재료·피로도 거래 원자성
- 납품 후 장비 기록 보존과 결과 인과 설명
- 신규 테스트와 기존 Godot 회귀 PASS
- Android·접근성·성능·외부 플레이 미실행은 PASS로 표기하지 않음

## Actions 재사용 가능 후 즉시 작업

1. PR validation `pull_request` 트리거 복원
2. 코드 범위 Ubuntu Python·Godot 실행
3. 실패 수정 후 최신 head 전체 재실행
4. `main`/nightly full validation 활성화
5. Ubuntu·Windows × Python 매트릭스 실행
6. 실제 check 이름으로 Branch protection 갱신
7. PR #35 코드 리뷰와 병합 판정

## 다음 게이트

장비 생애 PoC 행동 증거가 통과한 뒤에만 다음을 순서대로 검토한다.

1. +30 위험 강화 PoC
2. 흉갑·반지 공통 문법 전이
3. 제한된 세계 활동 장비 파이프라인
4. 토너먼트 일정과 선택적 관전
5. 전쟁·대표작·선택형 복원
6. 최종 강화 상한과 +100 유지·감량 판정
7. SWOT·VRIO 기반 Production Greenlight

## 현재 보류

- MVP-004 상인 납품
- 방어구·악세서리 수량 확정
- 다수 고객·세력·시장
- 전쟁·관전·베팅
- 대표작·복원 구현
- 저장·방치 복귀
- 범용 이벤트 버스·퀘스트 프레임워크

## Production 진입 차단 조건

다음 증거 없이는 Production 또는 MVP 전체 완료로 표시하지 않는다.

- 최신 head 전체 회귀
- 실제 Android 빌드·기기 증거
- 저장·복귀 계약
- 외부 플레이 행동 증거
- 접근성 장벽 검수
- 대표·최악 장면 성능 측정
- PR Required Check 강제 상태 확인
