# Scenes

현재 구현:

```text
scenes/
├─ main/main.tscn                 # 제작→강화 전체 흐름
└─ test/enhancement_test.tscn     # F5 기본 진입·강화·보관·자동 단조 테스트
```

원칙:

- `project.godot`은 현재 Prototype 검증을 위해 강화 테스트 Scene을 기본 실행한다.
- 새 기능은 기존 흐름에 통합할 수 없을 때만 Scene을 추가한다.
- 상인·고객·저장·방치 Scene은 실제 구현 범위가 승인된 뒤 생성한다.
- 빈 디렉터리와 미래 구조를 현재 구현처럼 문서화하지 않는다.
