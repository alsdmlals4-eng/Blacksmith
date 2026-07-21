---
name: blacksmith-qa
description: Blacksmith 변경의 계약·참조·정적·런타임·회귀·Android 증거를 적대적으로 검수한다.
---

# Blacksmith QA Skill

## Skill Modes

- `contract-check`: 사용자 요구·보호 대상·완료 기준과 실제 diff를 대조한다.
- `static`: JSON·GDScript·Scene·참조·Registry를 검사한다.
- `runtime`: Godot 프로젝트와 관련 Scene·상태 전환을 실행한다.
- `reference-freshness`: 경로·ID·Schema·정본 변경이 모든 소비자에 전파됐는지 확인한다.
- `regression`: 인접 제작·강화·보관·자동 단조 흐름의 정상·실패·경계를 재검증한다.
- `evidence-report`: PASS·PARTIAL·FAIL·NOT_RUN과 증거·롤백을 기록한다.

## Read first

- 승인된 사용자 요청 또는 PR 계약
- `AGENTS.md`
- `ACTIVE_CONTEXT.md`, `DEVELOPMENT_GATES.md`, 관련 책임 원본
- 실제 changed files와 변경됐어야 하지만 untouched인 소비자
- 관련 Workflow·테스트 로그

## Minimum checks

- JSON 구문·Schema·ID·참조 무결성
- 프로젝트 Registry 경로와 Skill 패키지 1:1
- 제작 진행도·피버 경계값
- 일반 강화와 +10 단위 특수 강화 분리
- 보조재료·촉매·정밀 강화의 일반 단계 누출 방지
- 수식어 이정표 +10~+100
- 실패 유지·하락·파괴·보정 확률 합계와 경계
- 폭주 단조 2단계 도약 제한
- 자동 단조 목표·비용·재료 fallback·자동 보관·보관함 반복·중지 조건
- 고객 방문과 상인 납품 역할 분리
- 저장·복귀·방치 보상은 구현 시 검증
- 세로 화면·스크롤·터치·노치·태블릿·폴더블 비율

## Validation order

```text
계약·diff 대조
→ reference-freshness
→ JSON·문법·정적 검사
→ 자동 모델 테스트
→ Godot 프로젝트 파싱
→ 관련 Scene 스모크
→ 정상·실패·경계·회귀
→ 적용 시 Android·접근성·성능
→ 문서·Registry·게이트 동기화
```

## PR review checklist

- 모든 changed file의 patch를 읽었는가?
- 요구사항별 구현 파일과 검증 증거가 연결되는가?
- 삭제·이동 파일의 활성 참조와 복구 경로를 확인했는가?
- 변경됐어야 하지만 untouched인 문서·데이터·테스트가 없는가?
- Workflow 존재와 실제 실행, Required Check 강제를 구분했는가?
- 자동 테스트가 성공 결과만 강제하지 않고 실패·하락·파괴·재료 부족·보관함 가득 참을 다루는가?
- 실제 Android·시각·접근성·성능 미실행을 명확히 남겼는가?

## Status language

- `PASS`: 요구된 검증을 실제 실행하고 증거가 일치함
- `PARTIAL`: 일부 검증만 실행하거나 비차단 미확인이 남음
- `FAIL`: 차단 결함 또는 계약 불일치
- `NOT_RUN`: 환경·입력·권한 부족으로 실행하지 않음

실행하지 않은 검증을 PASS로 표시하지 않는다.

## Failure conditions

- 변경 파일 일부만 읽고 PR 전체 검토를 주장한다.
- 문서의 오래된 상태를 실제 구현보다 우선한다.
- 정상 경로만 테스트한다.
- Godot·Android·접근성·성능을 실행하지 않고 통과로 보고한다.
- stale reference 또는 untouched 소비자 finding을 무시한다.

## Learning

회귀·누락·거짓 양성·검증 파이프라인 실패가 재사용 가능한 교훈이면 `skills/SKILL_LEARNING_LOG.md`에 기록한다.
