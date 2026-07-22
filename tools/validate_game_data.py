#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; ERR=[]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def num(v): return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))
def prob(v,label):
 if not num(v) or not 0<=float(v)<=1: ERR.append(f'{label}: 0..1 finite number required'); return None
 return float(v)
def enhancement():
 b=load(DATA/'crafting/enhancement_balance.json'); m=load(DATA/'crafting/enhancement_milestones.json'); mats=load(DATA/'crafting/materials.json')
 if b.get('schema_version')!=3: ERR.append('enhancement_balance schema must be 3')
 if m.get('schema_version')!=2: ERR.append('enhancement_milestones schema must be 2')
 if 'failure_policy' in m: ERR.append('milestones cannot own failure_policy')
 maxl=b.get('max_level'); interval=b.get('material_interval')
 if not isinstance(maxl,int) or maxl<=0 or not isinstance(interval,int) or interval<=0 or maxl%interval: ERR.append('invalid max_level/material_interval'); return
 if b.get('precision_interval')!=interval: ERR.append('precision/material intervals must match')
 pattern=b.get('base_success_pattern_by_cycle_position',{}); keys={str(i) for i in range(1,interval+1)}
 if set(pattern)!=keys: ERR.append(f'success pattern keys must be 1..{interval}')
 prev=1.0
 for i in range(1,interval+1):
  v=prob(pattern.get(str(i)),f'success pattern {i}')
  if v is not None and v>prev: ERR.append('success pattern must be nonincreasing')
  if v is not None: prev=v
 pity=b.get('pity',{}); step=prob(pity.get('bonus_per_failure'),'pity step'); cap=prob(pity.get('max_bonus'),'pity cap')
 if step is not None and cap is not None and step>cap: ERR.append('pity step cannot exceed cap')
 policy={'consume_materials_on_attempt_start':True,'pity_resets_on_success':True,'pity_survives_downgrade':True}
 if b.get('failure_policy')!=policy: ERR.append('canonical failure_policy mismatch')
 risk=b.get('risk',{}); safe=risk.get('safe_until_level'); destroy=risk.get('destroy_start_level')
 if not isinstance(safe,int) or not isinstance(destroy,int) or not 0<=safe<destroy<=maxl: ERR.append('invalid risk boundaries')
 decades={str(i) for i in range((maxl-1)//10+1)}; parsed={}
 for field in ('downgrade_ratio_by_decade','destroy_ratio_by_decade'):
  vals=risk.get(field,{})
  if set(vals)!=decades: ERR.append(f'{field} must cover only reachable decades'); continue
  prev=-1.0; parsed[field]={}
  for k in sorted(decades,key=int):
   v=prob(vals[k],f'{field}.{k}')
   if v is not None:
    parsed[field][k]=v
    if v<prev: ERR.append(f'{field} must be nondecreasing')
    prev=v
 steps=risk.get('downgrade_steps_by_decade',{})
 if set(steps)!=decades or any(not isinstance(v,int) or v<0 for v in steps.values()): ERR.append('downgrade steps must cover reachable decades')
 items=m.get('milestones',[]); levels=[x.get('level') for x in items if isinstance(x,dict)]; expected=list(range(interval,maxl+1,interval))
 if levels!=expected or not all(x.get('special_enhancement') is True for x in items): ERR.append('milestones must be ordered special levels 10..100')
 special=m.get('special_enhancement',{}); precision=b.get('precision',{})
 if special.get('interval')!=interval: ERR.append('special interval mismatch')
 for key in ('good_success_bonus','perfect_success_bonus'):
  if special.get(key)!=precision.get(key): ERR.append(f'{key} mismatch')
 ids=set()
 for item in mats.get('materials',[]):
  mid=item.get('id') if isinstance(item,dict) else None
  if not isinstance(mid,str) or mid in ids: ERR.append(f'invalid or duplicate material id: {mid}'); continue
  ids.add(mid)
  for key,val in item.get('effects',{}).items():
   if not num(val) or float(val)<0: ERR.append(f'{mid}.{key} must be nonnegative finite')
def main():
 files=sorted(DATA.rglob('*.json'))
 for p in files:
  try: d=load(p)
  except Exception as e: ERR.append(f'{p.relative_to(ROOT)}: {e}'); continue
  if not isinstance(d,dict) or d.get('schema_version') not in {1,2,3}: ERR.append(f'{p.relative_to(ROOT)}: invalid root/schema')
 mats=load(DATA/'crafting/materials.json'); ids={x.get('id') for x in mats.get('materials',[]) if isinstance(x,dict)}
 for r in load(DATA/'crafting/hidden_recipes.json').get('recipes',[]):
  for f in ('secondary_material','catalyst'):
   v=r.get('input',{}).get(f)
   if v and v not in ids: ERR.append(f'unknown {f}: {v}')
 enhancement()
 if ERR:
  print('Blacksmith data validation FAILED'); [print('-',e) for e in ERR]; return 1
 print(f'Blacksmith data validation PASSED ({len(files)} files; enhancement semantics verified)'); return 0
if __name__=='__main__': sys.exit(main())
