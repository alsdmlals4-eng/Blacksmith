---
name: blacksmith-game-design
description: Design and review Blacksmith crafting, enhancement, affix, economy, customer, reward, and POC rules while keeping runtime values in JSON.
---

# Blacksmith Game Design

## Modes

- `analyze`: 핵심 재미·루프·위험·보상 분석
- `design`: 새 규칙과 플레이어 선택 설계
- `update-spec`: Game Bible·MVP 책임 원본 갱신
- `poc-check`: 가장 위험한 가설과 관찰 결과 정의

## Read first

- Game Bible
- 관련 MVP Scope
- `data/crafting/` 또는 `data/sales/`
- 실제 모델·테스트

## Rules

- 간단한 모바일 광클 경험 우선
- 9회 빠른 일반 강화와 1회 특수 강화 리듬 보호
- 고위험은 성공 가치·손실·복구·표시를 함께 설계
- 직원·수리를 임의 추가하지 않음
- 설명 문서가 실제 JSON 수치를 독립 소유하지 않음
- 자동화가 수동 선택을 무의미하게 만들지 않게 함
- 판매 두 방식의 역할을 겹치지 않게 함

## Validation

- 행동 직후 피드백과 다음 행동 의도가 명확한가
- 고단계 성공 보상이 위험보다 체감되는가
- 안전·균형·도약 선택이 실질적으로 다른가
- 파괴 후 복귀가 과도하게 길지 않은가
- 가격·성장 인플레이션이 판매 판단을 무너뜨리지 않는가
