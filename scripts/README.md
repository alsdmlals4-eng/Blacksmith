# Scripts

현재 구현:

```text
scripts/
├─ forging/       # 제작 진행도·터치·피버·마감 품질·원본/적용 공격력 상태
├─ enhancement/  # 강화 확률·성장·위험·수식어 상태
├─ economy/      # 수동·자동 강화가 공유하는 골드·재료 거래
└─ ui/           # 입력·표시·Scene 전환·보관함·자동 단조 연결
```

책임 원칙:

- 게임 규칙은 `forging/`과 `enhancement/`의 상태 모델이 소유한다.
- 제작 품질은 `quality_attack_multiplier`와 `quality_value_multiplier`로 분리하며 구형 단일 배율을 사용하지 않는다.
- 원본 기본 공격력과 품질 적용 기본 공격력을 별도로 보존하고 강화·보관 소비자에 전달한다.
- 골드·재료 차감과 강화 시작 거래는 `economy/workshop_resources.gd`가 단일 책임으로 처리한다.
- `ui/`는 선택과 표시를 연결하며 성공률·가격·파괴 결과를 독립 결정하지 않는다.
- 데이터 값은 `data/**/*.json`이 책임진다.
- 수동·자동 UI는 자원을 직접 차감하지 않고 동일 `WorkshopResources.try_begin_attempt()`를 호출한다.
- 저장·판매·고객·방치 시스템은 실제 구현할 때만 새 책임으로 확장한다.

## 제작 결과 계약

- `forging/forging_session.gd`가 정밀 마감 품질과 피버 가치 보너스를 계산한다.
- 피버는 발동 1회당 제작 가치 +2%, 피버 중 제작 진행도 완료 +3%, 총 +5% 상한이다.
- 피버는 공격력과 정밀 마감 판정을 변경하지 않는다.
- `enhancement/`는 품질 가치와 피버 가치를 합산한 `crafting_value_multiplier`를 판매가 초기값으로 사용한다.
