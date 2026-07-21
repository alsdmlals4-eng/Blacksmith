# AI Workflow

## 기본 흐름

```text
사용자 Prompt
→ 저장소 사실·현재 게이트 확인
→ PLAN / BUILD / REVIEW 자동 선택
→ SKILL_REGISTRY trigger로 최소 Skill·mode 선택
→ Issue 또는 승인된 직접 요청으로 작업 계약 고정
→ 필요 시 의존성 순서화
→ 별도 브랜치 구현
→ 정본·참조·정적·런타임·회귀 검증
→ PR 파일별 검수
→ 문서·Active Context·Learning Log 동기화
→ 병합
→ 사용자 Fetch/Pull/F5
```

## 도구 역할

- GPT: 요구·기획·정본·계약·문서·검수
- Codex/GitHub 작업자: 코드·데이터·테스트·CI 구현
- GitHub: Issue·브랜치·PR·Actions·이력
- Godot: 실제 실행·렌더·입력·Android export
- 외부 AI: 필요할 때만 격리된 초안 입력으로 사용하며 실제 diff·근거·테스트 전에는 정본이 아님

## PR 전 필수

- 기준 main·Base 커밋 고정
- 보호 범위 명시
- changed files 전수 목록
- 정본 변경의 소비자 지도
- JSON·Godot·Governance
- 자동/수동/기기/발행 상태 분리
- 미검증과 롤백
- 사용자 확인 절차

## 완료 보고

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | UNVERIFIED
```
