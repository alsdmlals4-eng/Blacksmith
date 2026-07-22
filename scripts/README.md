# Scripts

현재 구현:

```text
scripts/
├─ forging/       # 제작 진행도·터치·피버·마감 상태
├─ enhancement/  # 강화 확률·성장·위험·수식어 상태
├─ economy/      # 수동·자동 강화가 공유하는 골드·재료 거래
└─ ui/           # 입력·표시·Scene 전환·보관함·자동 단조 연결
```

책임 원칙:

- 게임 규칙은 `forging/`과 `enhancement/`의 상태 모델이 소유한다.
- 골드·재료 차감과 강화 시작 거래는 `economy/workshop_resources.gd`가 단일 책임으로 처리한다.
- `ui/`는 선택과 표시를 연결하며 성공률·가격·파괴 결과를 독립 결정하지 않는다.
- 데이터 값은 `data/**/*.json`이 책임진다.
- 수동·자동 UI는 자원을 직접 차감하지 않고 동일 `WorkshopResources.try_begin_attempt()`를 호출한다.
- 저장·판매·고객·방치 시스템은 실제 구현할 때만 새 책임으로 확장한다.
