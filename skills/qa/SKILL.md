---
name: blacksmith-qa
description: Blacksmith 변경의 계약·외부 결과·정본 참조·정적·런타임·접근성·성능·UI·회귀 증거를 적대적으로 검수한다.
---

# Blacksmith QA

## Modes

- `contract-check`: 요구·보호 대상·완료 기준과 실제 diff를 대조한다.
- `external-source-review`: 외부 AI·벤치마크·리뷰 결과를 정본이 아닌 검수 대기 입력으로 확인한다.
- `reference-freshness`: 경로·ID·Schema·정본·정책 변경이 untouched 소비자까지 전파됐는지 확인한다.
- `adversarial-review`: 작업물이 실패했다고 가정하고 코어 훼손·누락·모순·거짓 통과를 공격적으로 찾는다.
- `critique-validation`: 지적을 증거·재현성·계약 영향으로 재검증하고 취향·오탐을 분리한다.
- `approved-refinement`: 유효하고 승인된 문제만 최소 범위로 수정한다.
- `regression-recheck`: 개선 뒤 원래 계약·반례·주변 시스템을 다시 검토한다.
- `static`: JSON·GDScript·Scene·Registry·로컬 참조·미해결 Git 충돌 블록을 검사한다.
- `runtime`: Godot 프로젝트·Scene·상태 전환을 실행한다.
- `accessibility-review`: 텍스트·입력·탐색·시간·모션·오류 복구의 실제 장벽을 검수한다.
- `performance-profile`: Android 대표·최악 장면의 frame time·CPU·GPU·메모리·로딩을 baseline과 비교한다.
- `ui-art-review`: 구현된 Godot UI를 실제 전후 렌더로 비교한다.
- `regression`: 제작·강화·보관·자동 단조의 정상·실패·경계를 재검증한다.
- `evidence-report`: `PASS / PARTIAL / FAIL / NOT_RUN`과 증거·위험·롤백을 기록한다.

## Read

승인 요청·PR 계약 → `AGENTS.md` → Active Context·Gates·정본 → changed files → untouched 소비자 → Workflow·로그.

## Minimum checks

- JSON·Schema·ID·경로·Registry 무결성
- 저장소 텍스트의 완전한 `<<<<<<< / ======= / >>>>>>>` 충돌 블록 부재
- 일반 강화와 +10 단위 특수 강화 분리
- 재료·촉매·정밀 효과의 일반 단계 누출 방지
- +10~+100 수식어 성장
- 실패 유지·하락·파괴·보정 확률 경계
- 폭주 단조 2단계 도약과 이정표 차단
- 자동 단조 목표·비용·재료 fallback·자동 보관·반복·중지
- 저장 변경 시 저장·불러오기·구버전 호환성
- 세로 화면·스크롤·터치·안전 영역

## Review loop

```text
계약·diff
→ adversarial-review
→ critique-validation
→ reference-freshness
→ 정적 검사
→ 모델 테스트
→ Godot 파싱·Scene
→ 실패·경계·회귀
→ 필요 시 접근성·성능·UI 렌더
→ 문서·Registry·게이트
→ approved-refinement
→ regression-recheck
→ evidence-report
```

발견 사항은 먼저 심각도·증거·영향을 기록한다. 모든 지적을 자동 수용하지 않고, 승인 범위의 수정만 BUILD로 전환한 뒤 다시 REVIEW한다.

## PR gate

- 모든 changed file patch를 읽는다.
- 요구사항마다 구현 파일과 증거를 연결한다.
- 삭제·이동 파일의 활성 참조와 복구 경로를 확인한다.
- 변경됐어야 하지만 untouched인 소비자를 찾는다.
- Workflow 존재·실행·Required Check 강제를 구분한다.
- 정상 결과만이 아니라 실패·하락·파괴·재료 부족·보관함 가득 참을 확인한다.
- Android·시각·접근성·성능 미실행은 `NOT_RUN`으로 남긴다.

## Failure

- 일부 파일만 읽고 PR 전체 검토를 주장한다.
- 레드팀 지적을 검증 없이 전부 수용하거나 취향을 결함으로 판정한다.
- 문서 주장이나 외부 결과를 실제 구현보다 우선한다.
- 자동 테스트만으로 Android·시각·접근성·성능을 통과 처리한다.
- stale reference·untouched 소비자·원래 실패 반례를 무시한다.
- 보류·기각한 개선을 몰래 반영하거나 개선 뒤 회귀 검토를 생략한다.

## Learning

재사용 가능한 회귀·누락·거짓 양성·파이프라인 실패만 `skills/SKILL_LEARNING_LOG.md`에 기록한다.
