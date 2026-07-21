# Document Update Matrix

| 변경 유형 | 반드시 확인·갱신 | 실제 증거·검증 |
|---|---|---|
| 핵심 게임 약속·루프 | Game Bible, START_HERE, Decision Log, Roadmap | 플레이 흐름·사용자 확인 |
| 강화 수치·위험·단조 기술 | `data/crafting/enhancement_balance.json`, MVP-002, Game Bible, Decision Log | EnhancementSession 테스트·Governance |
| 재료·촉매·수식어 | `data/crafting/materials.json`, `affixes.json`, MVP-002 | JSON 검사·모델 테스트 |
| UI·입력·화면 흐름 | Game Bible UX, Godot Playtest, Active Context | Scene smoke·실제 렌더·기기 |
| 보관함·자동 단조 | MVP-002, Roadmap, Active Context, 관련 UI Script | 모델/통합 테스트·수동 경계 |
| 고객·판매 | Game Bible, Roadmap, `data/sales/`, 신규 범위 문서 | 결과 계산 테스트 |
| 저장·복귀 | Game Bible, Roadmap, Engineering Skill, 데이터 Schema | 마이그레이션·로드 회귀 |
| 파일·경로·ID·Schema | START_HERE, Documentation Map, Registry, Workflow, 테스트 | Project Governance·reference freshness |
| Skill 추가·변경 | Skill Registry, Skill 파일, Learning Log, 필요 시 Skill Map Manifest | Governance |
| 제품 단계·게이트 | START_HERE, Active Context, Development Gates, Roadmap | Health Review |
| Base 동기화 | Base Rules Version, Base Sync Audit, Changelog, Health Report | 기준 커밋·PR |
| 발행 원본 변경 | Design Registry와 Manifest | 정책별 build·렌더·사람 검수 |
| Android 출시 기준 | AGENTS, Game Bible, Development Gates, Engineering Skill | 실제 SDK·AAB·기기 |

모든 행은 변경 필요 후보를 뜻한다. 영향이 없으면 PR에서 이유를 기록하고 억지로 수정하지 않는다.
