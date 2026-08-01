# Base v9.4 적용 감사 — Blacksmith

```yaml
decision_id: DEC-2026-08-01-001
issue: 82
baseline_commit: 500a5a7960146ef229ae172cf9e127306d23f073
base_version: 9.4.0
base_payload: a728712cb776ec98f4875914a580fcf7d0156593
base_evidence: ef1fba11167e4da0b298123b0c85ebd268191a42
base_finalization: 87a0b54c2847ce4b685879209205957c170cc1cd
base_registry_sha256: 693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59
adoption_scope: OPERATING_CONTRACT_ONLY
product_paths_changed: false
gdd_sheet_written: false
runtime_validation: NOT_RUN
android_validation: NOT_RUN
human_validation: HUMAN_NOT_RUN
```

## 적용

- canonical adapter·snapshot·compatibility views에 v9.4 identity와 새 모델/비용 route를 기록했다.
- 프로젝트 고유 Skill `blacksmith-game-design`, `blacksmith-engineering`, `blacksmith-qa`를 유지했다.
- AI Workflow와 UX/UI 모션·중단·연타·접근성 폴백 계약을 연결했다.

## 보호

`data/`, `scripts/`, `scenes/`, `assets/`, `addons/`, `project.godot`, 제작·강화·경제·저장·승인 자산은 변경하지 않는다.

## 적대적 검토

- 반복 클릭과 제작/보상 연출이 결과를 중복시키는가.
- 모션 완료가 제작·재료·보상·저장 권위를 소유하는가.
- Context 큐레이션이 실패 사례·경제 위험·보호 규칙을 제거하는가.
- 문서만으로 Android·사람 이해·성능·비용 절감을 PASS 처리하는가.
