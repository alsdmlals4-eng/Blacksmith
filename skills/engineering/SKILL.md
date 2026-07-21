---
name: blacksmith-engineering
description: Implement and review Blacksmith Godot 4.7.1 GDScript, domain models, data contracts, save compatibility, Android builds, and target-platform performance.
---

# Blacksmith Engineering

## Modes

- `design-interface`
- `implement`
- `data-contract`
- `android-build`
- `profile`

## Baseline

- Godot 4.7.1 / GDScript
- Android portrait 720×1280
- `canvas_items` + `expand`
- AAB / API 36 준비

## Rules

- 게임 규칙은 UI가 아니라 모델·JSON이 소유
- UI는 표시·입력·흐름 담당
- JSON ID·수치를 여러 Script에 중복하지 않음
- 공개 함수·snapshot 필드 변경 시 모든 소비자·테스트 검색
- 저장 도입 시 schema version·migration·기본값·파괴 상태 검증
- 서명키·인증 정보 커밋 금지
- 실제 기기 미실행은 NOT_RUN

## Validation

- `python tools/validate_game_data.py`
- `python tools/check_project_governance.py`
- Godot import/parse
- Scene smoke
- 모델 테스트
- Android debug/AAB와 실제 기기는 환경이 있을 때 별도
