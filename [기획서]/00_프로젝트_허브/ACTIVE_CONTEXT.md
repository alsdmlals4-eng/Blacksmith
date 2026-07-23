# Active Context

- 갱신일: 2026-07-24
- Work Mode: `REVIEW → PLAN`
- 현재 브랜치: `agent/propose-project-core-contract`
- 현재 PR: #33 Draft
- PR 스택: `#31 → #32 → #33`
- 현재 Issue·Goal: #34 `MVP-003: 장비 한 점의 생애 PoC 구현 및 플레이 검증`
- 장비 생애 PoC 통합 상태: `SPEC_READY / IMPLEMENTATION_NOT_STARTED`

## 1. 현재 판정

| 영역 | 상태 |
|---|---|
| 프로젝트 코어 | `CORE_CONFIRMED / CORE_RECORDED` |
| 장비 생애 PoC 통합 명세 | `SPEC_READY` |
| 장비 생애 PoC 구현 | `IMPLEMENTATION_NOT_STARTED` |
| 현재 Prototype 자동 검증 | Data #418 PASS, Godot #345 PASS |
| Android 실기기 | `NOT_RUN` |
| 접근성·성능 | `NOT_RUN` |
| 외부 플레이테스트 | `NOT_RUN` |
| Production | `NOT_GREENLIT` |

## 2. 프로젝트 코어

> 한 명의 대장장이가 제한된 하루 작업량으로 장비 한 점을 직접 만들고, 강화 위험과 `+10` 수식어 선택으로 운명을 정한 뒤, 그 장비가 다른 이의 손에서 쌓은 역사를 명성과 다음 의뢰로 돌려받는 모바일 제작 게임.

보호 대상:

- 직접 제작과 빠른 터치 피드백
- 영구 완성도
- 일반 강화 버튼 입력당 결과 1회
- `+10` 특수 강화와 수식어 선택
- 판매·납품 장비의 영구 기록과 세계 환류
- 한 명의 대장장이, 피로도 기반 일일 우선순위
- 수동 날짜 진행과 잔여 피로도 50% 이월

제외:

- 직원·복수 대장장이
- 직접 전투
- 작업 예약·생산 대기열
- 일상적 수리 관리
- 터치당 피로도
- 실시간 전체 세계 시뮬레이션

중요 장비의 선택형 복원은 승인된 후속 기획이며 첫 PoC에서는 제외한다.

## 3. 현재 구현 사실

현재 실행 배지: `POC v0.6.4 · main · 2026.07.23.1`

현재 코드·데이터·Scene·테스트가 지원하는 범위:

- 철검 제작, 자동 작업, 광클 피버, 제작 정밀 마감
- 일반 강화와 `+10` 단위 특수 강화
- 최대 +100 목표, 수식어 성장
- +11 하락, +30 파괴, 실패 보정
- 균형·안정·폭주 단조
- 공유 골드·재료 거래
- 보관함과 자동 단조

현재 제작 검증 기준:

- 제작 모델 7건
- 제작 결과 통합 6건
- 보통·좋음·완벽 기본 공격력 20·21·22
- 피버 적용 공격력 21·22·23
- 피버 공격력 ×1.05·제작 가치 ×1.03, 반복 비중첩

현재 실패·보정·위험 수치의 단일 책임 원본은 `data/crafting/enhancement_balance.json`이다. `data/crafting/enhancement_milestones.json`은 `+10` 단위 특수 강화·수식어 이정표만 책임진다.

아직 구현되지 않은 확정 설계:

- 영구 완성도 5등급과 기존 정밀 결과의 분리
- 피로도·날짜 진행
- 검투사 의뢰와 +5/+10 납품 판단
- 지연 경기 결과와 설명 가능한 기여 조건
- 영구 세계 장비 기록과 재방문
- PoC 행동 로그

## 4. 현행 책임 원본

- 코어: `docs/superpowers/specs/2026-07-23-project-core-design.md`
- 통합 명세: `docs/superpowers/specs/2026-07-23-equipment-lifecycle-poc-integrated-spec.md`
- MVP Scope: `docs/MVP-003_SCOPE.md`
- 구현계획: `docs/superpowers/plans/2026-07-23-equipment-lifecycle-poc-implementation.md`
- 최종 적대적 검토: `docs/FINAL_ADVERSARIAL_REVIEW_REPORT.md`
- 통합 게임 기획: `[기획서]/01_통합_게임_기획/BLACKSMITH_GAME_BIBLE.md`
- 상태·게이트: 이 문서, `ROADMAP.md`, `DEVELOPMENT_GATES.md`

## 5. 최근 검증

- Data validation #389: 기존 기준선 PASS
- 최종 검토 Red gate #391: 예상 실패. stale 시작 문서, 누락된 MVP Scope와 정본 전파 누락을 검출
- Green 후보 #406·#412: 기존 문서 계약과 계획 미래 경로 오분류를 추가 검출
- Data validation #418: Git conflict, JSON, 강화 실패, 시뮬레이터, core alignment, 계획 미래 경로 분류, Base adoption audit와 고정 Base 전체 회귀 PASS
- Godot validation #345: 제작 계약, Godot 4.7.1 import·parse, enhancement/main Scene smoke, 모델·통합 테스트, 패키징과 JSON 검증 PASS
- PR #31·#32·#33 review comment: 없음
- Issue #29 기준선 시뮬레이션: 완료 후 닫음
- Issue #14 구형 Base 마이그레이션: 현행 PR #31/#32로 대체 후 닫음
- PDF 자동 검수: 15페이지, 200 DPI 전 페이지 PASS
- PDF 사람 시각 검토: `NOT_RUN`

#418/#345는 최종 보고서 본문과 운영 정본을 포함한 substantive head `f161200613522d0b9ded5e951b3c404d93dce527`의 증거다. 이후 증거 문구만 동기화한 head도 동일 Workflow로 재확인한다.

## 6. 다음 작업

1. 최종 증거 동기화 head의 Data·Godot Workflow를 재확인한다.
2. PR #33 제목·본문·changed files·head 일치를 마감한다.
3. 선행 PR #31·#32를 정리한 뒤 #33을 검토한다.
4. Issue #34 구현은 별도 구현 PR에서 Task 1~9 순서로 수행한다.
5. Android·접근성·성능·외부 플레이 증거를 수집한다.

## 7. 완료 금지 조건

다음이 남아 있으면 프로젝트 구현 또는 MVP 완료로 선언하지 않는다.

- Issue #34 제품 코드 미구현
- Android·접근성·성능·외부 플레이 `NOT_RUN`
- Branch protection Required Check 강제 상태 `UNVERIFIED`
- PR #31·#32·#33 미병합
- 사람의 최종 PDF 시각 확인 `NOT_RUN`
- 저장소 PDF binary publication `NOT_RUN`
