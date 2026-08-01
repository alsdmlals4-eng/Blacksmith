#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_VERSION = '9.4.0'
BASE_PAYLOAD = 'a728712cb776ec98f4875914a580fcf7d0156593'
BASE_EVIDENCE = 'ef1fba11167e4da0b298123b0c85ebd268191a42'
BASE_FINALIZATION = '87a0b54c2847ce4b685879209205957c170cc1cd'
BASE_REGISTRY_SHA = '693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59'
BASELINE = '500a5a7960146ef229ae172cf9e127306d23f073'
NEW_SKILL = 'optimizing-ai-model-and-prompt-costs'


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def save(path: str, data: dict) -> None:
    (ROOT / path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def route() -> dict:
    return {'route_id': NEW_SKILL, 'skill_id': NEW_SKILL, 'status': 'ACTIVE'}


def append_once(path: str, marker: str, block: str) -> None:
    file = ROOT / path
    text = file.read_text(encoding='utf-8') if file.exists() else ''
    if marker not in text:
        text = text.rstrip() + ('\n\n' if text.strip() else '') + block.strip() + '\n'
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding='utf-8')


def migrate_adapters() -> None:
    adapter_path = 'skills/PROJECT_BASE_ADAPTER.json'
    adapter = load(adapter_path)
    adapter['base_release'] = {
        'release_commit': BASE_PAYLOAD,
        'release_evidence_commit': BASE_EVIDENCE,
        'repository': 'alsdmlals4-eng/Base',
        'version': BASE_VERSION,
    }
    adapter['protected_baseline']['commit'] = BASELINE
    adapter['skill_registry']['base']['sha256'] = BASE_REGISTRY_SHA
    routes = adapter['routing']['base_routes']
    if NEW_SKILL not in {item['route_id'] for item in routes}:
        routes.append(route())
    routes.sort(key=lambda item: item['route_id'])
    adapter['shared_overrides'].setdefault(NEW_SKILL, {
        'modes': ['route-model-and-effort', 'design-cacheable-prefix', 'estimate-cost', 'measure-actual-usage', 'recalibrate'],
        'provider_measurement_status': 'NOT_RUN',
    })
    save(adapter_path, adapter)
    adapter_sha = hashlib.sha256((ROOT / adapter_path).read_bytes()).hexdigest()

    snapshot_path = 'skills/PROJECT_SKILL_SNAPSHOT.json'
    snapshot = load(snapshot_path)
    snapshot['base_registry']['sha256'] = BASE_REGISTRY_SHA
    if NEW_SKILL not in {item['route_id'] for item in snapshot['base_routes']}:
        snapshot['base_routes'].append(route())
    snapshot['base_routes'].sort(key=lambda item: item['route_id'])
    snapshot['effective_routes'][NEW_SKILL] = {
        'route_id': NEW_SKILL,
        'skill_id': NEW_SKILL,
        'source': 'BASE_SHARED',
        'status': 'ACTIVE',
        'target_route_id': NEW_SKILL,
    }
    snapshot['source_registry']['sha256'] = adapter_sha
    save(snapshot_path, snapshot)

    for view_path in ('skills/BASE_V9_ADAPTER.json', 'skills/PROJECT_BASE_SKILL_ADAPTER.json'):
        view = load(view_path)
        view['base_release'] = {
            'release_commit': BASE_PAYLOAD,
            'release_evidence_commit': BASE_EVIDENCE,
            'repository': 'alsdmlals4-eng/Base',
            'version': BASE_VERSION,
        }
        view['canonical_source_sha256'] = adapter_sha
        if view_path.endswith('PROJECT_BASE_SKILL_ADAPTER.json'):
            view.setdefault('shared_skill_overrides', {}).setdefault(NEW_SKILL, {})
        save(view_path, view)


def migrate_docs() -> None:
    rules = ROOT / 'docs/BASE_RULES_VERSION.md'
    rules.write_text(f'''# Base 적용 기준

```yaml
base: alsdmlals4-eng/Base
base_version: {BASE_VERSION}
base_payload_commit: {BASE_PAYLOAD}
base_trusted_evidence_commit: {BASE_EVIDENCE}
base_pin_finalization_commit: {BASE_FINALIZATION}
base_registry_sha256: {BASE_REGISTRY_SHA}
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
''', encoding='utf-8')

    ai = f'''# Blacksmith AI·GitHub 작업 흐름

## Base v9.4 계약

- `[모델 추천]`은 난도·실패 비용·재작업 위험을 기준으로 모델과 추론 단계를 제안한다. 실제 모델 설정 변경은 사용자가 수행하며 다음 checkpoint부터 적용한다.
- 보안·권한·데이터 무결성·저장 호환성·불가역 변경은 `HARD_CONSTRAINT`다.
- 일반 기술 구조는 `RECOMMENDED_DEFAULT`, 비파괴 표현 초안은 `JUDGMENT_SPACE`다.
- Prompt는 `problem / player_or_user_value / inputs / authority_and_source / output_contract / invariants / failure_conditions / validation`의 Interface-first 계약으로 작성한다.
- `Example-as-Fixture`: 예시는 정답 권위가 아니라 정상·실패·경계·회귀 Fixture 또는 Golden Set이다.
- Context는 `decision_question / include_criteria / exclude_criteria / authority_level / freshness / known_conflicts / progressive_load_trigger / refresh_trigger`를 기록한다.
- 화면·Schema·Fixture는 실제 Android 런타임·사람 이해·성능을 자동 증명하지 않는다.

## Blacksmith 보호

제작·강화·경제·저장·승인 아트는 프로젝트 정본과 실제 파일이 소유한다. Base 기본값으로 수치나 제품 의미를 덮어쓰지 않는다.

Base identity: payload `{BASE_PAYLOAD}`, evidence `{BASE_EVIDENCE}`, Registry `{BASE_REGISTRY_SHA}`.
'''
    path = ROOT / '[기획서]/00_프로젝트_허브/AI_WORKFLOW.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ai, encoding='utf-8')

    ux_path = ROOT / 'docs/UX_UI_SYSTEM.md'
    ux = ux_path.read_text(encoding='utf-8').replace('Base content commit: `0fd95f4513343e77fd664af2763a01b02f52545b`', f'Base content commit: `{BASE_PAYLOAD}`')
    if '## 7A. UI 모션·중단·반복 계약' not in ux:
        block = '''## 7A. UI 모션·중단·반복 계약

```text
입력 접수 → 처리 중 → 도메인 결과 확정 → 결과 표현
```

- 반복 클릭·제작·강화·보상 수령은 중복 지급·중복 소비·transform drift 없이 재진입해야 한다.
- 모션은 중단과 즉시 완료 경로를 가지며, 취소·건너뛰기 후에도 도메인 상태와 결과 카드가 동일해야 한다.
- `AnimationPlayer`·`Tween` 완료 signal은 제작 성공·재료 소비·보상·저장 권위 시점이 아니다.
- `Reduced Motion`, `mute`, `haptic-off`에서도 결과·위험·다음 행동을 텍스트·아이콘으로 보존한다.
- Android 반복 피로·기기 성능·사람 이해는 `NOT_RUN` 또는 `HUMAN_NOT_RUN`으로 유지한다.

'''
        ux = ux.replace('## 8. 검증 매트릭스', block + '## 8. 검증 매트릭스', 1)
    ux_path.write_text(ux, encoding='utf-8')

    active = ROOT / '[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md'
    text = active.read_text(encoding='utf-8')
    marker = '## Base v9.4 운영 계약'
    if marker not in text:
        text = text.rstrip() + f'''\n\n{marker}\n\n- Base `{BASE_VERSION}` payload/evidence를 adapter에 적용했다.\n- 범위는 운영 계약과 UI 검증 계약이며 제품 코드·데이터·Scene·자산·저장은 변경하지 않는다.\n- Godot·Android·사람·provider 비용 증거는 `NOT_RUN` 또는 `HUMAN_NOT_RUN`이다.\n'''
    active.write_text(text, encoding='utf-8')

    docmap = ROOT / '[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md'
    text = docmap.read_text(encoding='utf-8')
    rows = '| AI 모델·지시·Context 작업 흐름은 무엇인가 | `AI_WORKFLOW.md` | Base v9.4 모델 추천·지시 권위·Context·증거 상한 |\n| Base v9.4 적용·보호 감사는 무엇인가 | `docs/reviews/2026-08-01_BASE_V9_4_ADOPTION_AUDIT.md` | payload·evidence·route·제품 보호 경계 |'
    if 'AI_WORKFLOW.md` | Base v9.4' not in text:
        anchor = '| Base 기준은 무엇인가 | `docs/BASE_RULES_VERSION.md` | 고정 commit과 적용 정책 |'
        text = text.replace(anchor, anchor + '\n' + rows, 1)
    docmap.write_text(text, encoding='utf-8')

    audit = ROOT / 'docs/reviews/2026-08-01_BASE_V9_4_ADOPTION_AUDIT.md'
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(f'''# Base v9.4 적용 감사 — Blacksmith

```yaml
decision_id: DEC-2026-08-01-001
issue: 82
baseline_commit: {BASELINE}
base_version: {BASE_VERSION}
base_payload: {BASE_PAYLOAD}
base_evidence: {BASE_EVIDENCE}
base_finalization: {BASE_FINALIZATION}
base_registry_sha256: {BASE_REGISTRY_SHA}
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
''', encoding='utf-8')


def migrate_tests() -> None:
    path = ROOT / 'tests/test_base_v94_ai_operations_adoption.py'
    path.write_text(f'''from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BaseV94BlacksmithAdoptionTests(unittest.TestCase):
    def test_identity_routes_and_project_skills(self) -> None:
        adapter = json.loads((ROOT / 'skills/PROJECT_BASE_ADAPTER.json').read_text(encoding='utf-8'))
        snapshot = json.loads((ROOT / 'skills/PROJECT_SKILL_SNAPSHOT.json').read_text(encoding='utf-8'))
        self.assertEqual('{BASE_VERSION}', adapter['base_release']['version'])
        self.assertEqual('{BASE_PAYLOAD}', adapter['base_release']['release_commit'])
        self.assertEqual('{BASE_EVIDENCE}', adapter['base_release']['release_evidence_commit'])
        self.assertEqual('{BASE_REGISTRY_SHA}', adapter['skill_registry']['base']['sha256'])
        self.assertIn('{NEW_SKILL}', {{item['route_id'] for item in adapter['routing']['base_routes']}})
        self.assertEqual({{'blacksmith-engineering', 'blacksmith-game-design', 'blacksmith-qa'}}, {{item['route_id'] for item in adapter['routing']['project_routes']}})
        self.assertEqual('BASE_SHARED', snapshot['effective_routes']['{NEW_SKILL}']['source'])
        self.assertEqual(['data/', 'scripts/', 'scenes/', 'assets/', 'addons/', 'project.godot'], adapter['protected_paths'])

    def test_generated_views_bind_to_adapter(self) -> None:
        sha = hashlib.sha256((ROOT / 'skills/PROJECT_BASE_ADAPTER.json').read_bytes()).hexdigest()
        snapshot = json.loads((ROOT / 'skills/PROJECT_SKILL_SNAPSHOT.json').read_text(encoding='utf-8'))
        self.assertEqual(sha, snapshot['source_registry']['sha256'])
        for file in ('skills/BASE_V9_ADAPTER.json', 'skills/PROJECT_BASE_SKILL_ADAPTER.json'):
            view = json.loads((ROOT / file).read_text(encoding='utf-8'))
            self.assertEqual(sha, view['canonical_source_sha256'])
            self.assertEqual('{BASE_VERSION}', view['base_release']['version'])

    def test_ai_ui_and_evidence_limits(self) -> None:
        ai = (ROOT / '[기획서]/00_프로젝트_허브/AI_WORKFLOW.md').read_text(encoding='utf-8')
        ux = (ROOT / 'docs/UX_UI_SYSTEM.md').read_text(encoding='utf-8')
        audit = (ROOT / 'docs/reviews/2026-08-01_BASE_V9_4_ADOPTION_AUDIT.md').read_text(encoding='utf-8')
        for token in ('[모델 추천]', 'HARD_CONSTRAINT', 'Interface-first', 'Example-as-Fixture', 'refresh_trigger', 'NOT_RUN'):
            self.assertIn(token, ai)
        for token in ('입력 접수', '처리 중', '중단', '즉시 완료', '재진입', 'Reduced Motion', 'mute', 'haptic-off', '권위 시점'):
            self.assertIn(token, ux)
        self.assertIn('product_paths_changed: false', audit)
        self.assertIn('HUMAN_NOT_RUN', audit)


if __name__ == '__main__':
    unittest.main()
''', encoding='utf-8')


def main() -> None:
    migrate_adapters()
    migrate_docs()
    migrate_tests()


if __name__ == '__main__':
    main()
