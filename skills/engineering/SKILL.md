---
name: blacksmith-engineering
description: Use when a verified Blacksmith engineering route authorizes Godot code, data, save compatibility, or runtime diagnosis.
---

# Blacksmith Engineering

## 상태·진입

이 패키지의 존재는 실행 권한이 아니다. `skills/PROJECT_SKILL_SNAPSHOT.json`의 route가 HOLD이면 활성화하지 않는다.
AGENTS.md → `docs/operations/BLACKSMITH_BASE_CURRENT_ADAPTATION_WORK_CONTRACT_20260901.md` → 승인된 product owner와 실제 대상·consumer·tests를 읽는다.
엔진/툴 pin은 프로젝트 채택 기록·project.godot·CI에서 확인한다. 이 스킬에 버전을 중복 고정하지 않는다.

## 승인 실행의 원칙

- 코드·기계 계약은 실제 실패 반례부터 확인하고 최소 구현 후 회귀를 검증한다.
- 규칙과 거래는 domain/data가 소유하고 UI·모션은 확정 결과를 표현한다. 표시 callback에서 비용·보상·저장을 재계산하지 않는다.
- 저장·UID·schema·id·기본값 변경은 기존 호환 계약과 원자성·복구·재시작을 함께 검증한다. legacy 저장을 새 규칙으로 재해석하지 않는다.
- Scene·Resource·project 설정과 제품 저작은 채택된 HiGodot 경계, GDScript 테스트는 GUT 경계를 지킨다. Hera를 persistent writer로 쓰지 않는다.
- 새 기능/리팩터링을 섞지 않는다. 반복·취소·중단·대상 소멸과 실패 복구는 실제 consumer가 요구하는 범위에서 확인한다.
- 플레이어-facing 효과/UI 변경이면 기획·QA의 재미 가설과 요구 ID를 소비한다. 미구현 연결은 PLANNED, 사람 증거는 별도다.
- 원인 불명 runtime 문제는 실제 로그·재현·버전·프로젝트 경로를 먼저 확인한다.
- 기존 저장·사용자 작업·승인 자산·다른 프로세스·secret은 보호한다. 새 비용·보안·기획 의미는 사용자 결정이다.

## 검증·산출물

관련 데이터 검사·GUT·실제 Godot 실행과 필요한 화면/기기 검사를 수행한다. 문서만 수정할 때 엔진 실행을 강제하지 않는다.
CI의 실제 debug/디렉터리 옵션을 맞추고 경고를 숨기지 않는다. 미실행은 NOT_RUN이며 machine PASS는 사람/출시 승인이 아니다.
기존 작업 계약에 영향 파일·입출력·상태·실패 복구·검증·롤백을 남긴다. 새 추적 문서를 만들지 않는다.
