# Scripts

GDScript는 상태 책임에 따라 나눈다.

```text
scripts/
├─ autoload/      # 게임 상태, 데이터 Registry, 저장
├─ forging/       # 제작 진행도, 터치, 피버, 마감
├─ enhancement/  # 강화 확률, 이정표, 수식어
├─ inventory/    # 무기와 재료 보유 상태
├─ sales/        # 고객 방문, 상인 납품, 가격
├─ customers/    # 검투사·군대·모험가 결과
├─ simulation/   # 방치 진행과 결과 계산
└─ ui/           # 표시와 입력 연결만 소유
```

UI 애니메이션이나 연출이 보상·강화·저장 결과를 직접 변경하지 않게 한다.
