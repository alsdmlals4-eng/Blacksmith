---
name: blacksmith-project-operations
description: Automatically route Blacksmith requests into PLAN, BUILD, or REVIEW; create work contracts; audit and safely migrate project operating documents; update active context; and report execution evidence.
---

# Blacksmith Project Operations

## Modes

- `route`: 요청 의도·현재 단계·위험·주 책임 분야와 최소 Skill 선택
- `contract`: 범위·제외·보호·완료·검증·롤백 고정
- `audit`: 기존 책임 원본·참조·고유 정보·drift를 읽기 전용 조사
- `migrate`: 승인 범위만 보존형 갱신
- `verify`: 시작 경로·Registry·Skill·Gate·자동화·콜드 스타트 검수
- `handoff`: Active Context와 경계 스냅샷 갱신
- `execution-report`: 실제 Work Mode·Skill·증거·미검증 보고

## Read first

`AGENTS.md → START_HERE → ACTIVE_CONTEXT → DOCUMENTATION_MAP → DEVELOPMENT_GATES → Registry → Issue → 실제 파일`

## Rules

- 한 시점의 주 Work Mode는 하나
- 전체 Skill 기본 로드 금지
- 사용자 승인 전 대량 삭제·이동·통합 금지
- 기존 게임 결정·수치·코드·보류 보존
- 실행하지 않은 검증을 PASS로 보고하지 않음
- 경로·ID·Schema 변경 시 change-validation 호출

## Output

```yaml
work_mode:
skill_mode:
reason:
protected_scope:
changed_files:
validation:
result:
unverified:
rollback:
```
