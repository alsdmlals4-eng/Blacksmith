---
name: blacksmith-change-validation
description: Review Blacksmith code, data, documents, configuration, and PRs against the approved contract with canonical-reference, static, runtime, boundary, and regression evidence.
---

# Blacksmith Change Validation

## Modes

- `contract-check`
- `reference-freshness`
- `static-validation`
- `runtime-validation`
- `regression`
- `evidence-report`

## Review order

```text
Issue·승인 범위
→ 실제 diff
→ 책임 원본과 소비자
→ stale·orphan·untouched consumer
→ JSON·GDScript·Scene·Workflow 정적 검사
→ Godot 실행
→ 정상·실패·경계·회귀
→ 자동/수동/기기/발행 상태 분리
```

## Blacksmith 필수 반례

- 일반 강화에 촉매·정밀 효과 누출
- +11 하락과 +30 파괴 경계
- 안정 단조 파괴 0
- 폭주가 +10 단위를 건너뜀
- 자동 단조가 목표 단계를 초과함
- 재료 0인데 재고가 음수가 됨
- 파괴 무기 보관
- 보관함 6칸 초과
- 문서가 이전 확률·테스트 수를 현행으로 주장
- `project.godot` F5 진입점 손상

## Decision

`ACCEPT / ACCEPT_WITH_FOLLOWUP / REVISE / REJECT / UNVERIFIED`
