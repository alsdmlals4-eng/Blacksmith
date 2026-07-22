#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; ERR=[]
def t(p): return (ROOT/p).read_text(encoding='utf-8')
def req(c,m):
 if not c: ERR.append(m)
b=json.loads(t('data/crafting/enhancement_balance.json')); m=json.loads(t('data/crafting/enhancement_milestones.json'))
req(b.get('schema_version')==3,'balance schema must be 3'); req(m.get('schema_version')==2,'milestone schema must be 2'); req('failure_policy' not in m,'milestones cannot own failure policy')
req(b.get('failure_policy')=={'consume_materials_on_attempt_start':True,'pity_resets_on_success':True,'pity_survives_downgrade':True},'failure policy mismatch')
for f in ('downgrade_ratio_by_decade','destroy_ratio_by_decade','downgrade_steps_by_decade'): req('10' not in b.get('risk',{}).get(f,{}),f'unreachable decade 10: {f}')
s=t('scripts/enhancement/enhancement_session.gd'); r=t('scripts/economy/workshop_resources.gd')
req('failure_streak = 0' in s,'success reset missing'); req(s.count('failure_streak += 1')>=2,'hold/down pity missing'); req('destroyed = true' in s and 'state = State.COMPLETE' in s,'destroy termination missing')
req('_consume_material(secondary_id)' in r and '_consume_material(catalyst_id)' in r,'material consume missing'); req(r.index('_consume_material(secondary_id)')<r.index('session.begin_attempt'),'materials must be consumed before attempt'); req('_restore_material(secondary_id)' in r,'failed start restore missing')
for p in ('README.md','docs/MVP-002_SCOPE.md','docs/GODOT_PLAYTEST.md','tests/README.md','tests/SPECIAL_ENHANCEMENT_VALIDATION.md'):
 x=t(p); req('enhancement_balance.json' in x,f'balance owner missing: {p}'); req('enhancement_milestones.json' in x,f'milestone owner missing: {p}')
req('tests/check_enhancement_failure_contract.py' in t('.github/workflows/data-validation.yml'),'workflow checker missing')
if ERR:
 print('Enhancement failure contract FAILED'); [print('ERROR:',e) for e in ERR]; raise SystemExit(1)
print('Enhancement failure contract PASSED')
