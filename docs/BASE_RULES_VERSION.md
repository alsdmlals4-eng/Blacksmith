# Base 적용 기준

```yaml
base: alsdmlals4-eng/Base
base_version: 9.4.0
base_payload_commit: a728712cb776ec98f4875914a580fcf7d0156593
base_trusted_evidence_commit: ef1fba11167e4da0b298123b0c85ebd268191a42
base_pin_finalization_commit: 87a0b54c2847ce4b685879209205957c170cc1cd
base_registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
release_state: BASE_RELEASED
project: alsdmlals4-eng/Blacksmith
adoption_scope: OPERATING_CONTRACT_ONLY
product_paths_changed: false
```

## 적용 방식

Base 본문 전체를 복제하지 않는다. `skills/PROJECT_BASE_ADAPTER.json`이 선택한 공용 route와 Blacksmith 프로젝트 Skill 3개를 결합한다. Base v9.4는 모델·추론 단계·Prompt caching·비용 측정, 지시 권위, Interface-first Prompt, Context 큐레이션, Artifact 주장 상한, Godot UI 모션 계약을 제공한다.

## 프로젝트 보호 경계

- 제작·강화·경제·광클 피버·+10 특수 강화 규칙과 수치를 변경하지 않는다.
- `data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`을 이 적용에서 수정하지 않는다.
- 저장·인벤토리·장비 호환성과 승인 시각 방향을 유지한다.
- Android 실기기·AAB·safe area·접근성·성능은 실제 증거 전까지 `NOT_RUN`이다.
- provider 실제 비용·cache hit·절감률과 사람 반복 피로는 `NOT_RUN` / `HUMAN_NOT_RUN`이다.

## 재동기화 조건

Base release·Registry·route·adapter Schema가 바뀌거나 Blacksmith 책임 구조와 주요 제품 게이트가 변경될 때 재감사한다.
