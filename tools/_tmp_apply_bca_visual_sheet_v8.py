from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "7072b9e2742a60d7548fd39df3328ad76a8dbad1"
TABS = ["00_프로젝트_허브","01_작업순서","02_현재_확정결정","03_근거_라이브러리","04_누락_충돌_감사","10_제품방향","11_세계관","12_핵심루프","13_주요인물","14_조연_세력_관계","20_코어경험_데모목표","30_데모범위_품질기준_제작기반","40_핵심시스템_메인콘텐츠","41_성장_경제","50_메인콘텐츠","60_UX_UI_접근성","70_아트_오디오_에셋","71_이미지기획_생성목록","72_이미지검수_승인로그","80_데모_버티컬슬라이스_플레이테스트","90_본제작_출시_사업","98_Base_반영후보","99_변경이력"]

def write(path, content):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content.rstrip()+"\n",encoding="utf-8")
def append_once(path, marker, content):
    p=ROOT/path; t=p.read_text(encoding="utf-8")
    if marker not in t: p.write_text(t.rstrip()+"\n\n"+content.strip()+"\n",encoding="utf-8")

def docs():
    tabs="\n".join(f"- `{x}`" for x in TABS)
    write("docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md",f"""# Blacksmith 프로젝트 Google Sheets Workbook

```yaml
project: Blacksmith
sheet_status: NOT_CONFIGURED
spreadsheet_url:
base_commit: {BASE_SHA}
```

정확한 기존 Sheet URL·ID·권한을 확인하지 못했으므로 신규 Sheet를 만들지 않는다. 연결 시 기존 tab·수식·검증·사용자 편집을 보존하며 아래 의미 구조를 설치·병합한다.

{tabs}

| 의미 구조 | 프로젝트 책임 원본 |
|---|---|
| 세계관·주요인물·조연 | `BLACKSMITH_GAME_BIBLE.md`의 대장간·고객·상인·검투사·장비 소유자 |
| 핵심루프 | 광클 단조 → 즉시 피드백 → 피버 → 성장·판매 선택 |
| 핵심시스템·메인콘텐츠 | 제작·일반 강화·특수 강화·수식어·재료·촉매·판매·장비 생애주기 |
| 이미지 계획·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md` |

Sheet는 독립 정본이 아니라 Decision ID·GitHub 경로·상태를 연결한다.
""")
    write("docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md",f"""# Blacksmith GPT 이미지 생성·검수 워크플로

- Base: `alsdmlals4-eng/Base@{BASE_SHA}`
- Mode: `planning-visualization`, `final-visual-candidate`, `visual-qa-and-approval`
- Sheet: `NOT_CONFIGURED`

## 기획 중 우선 이미지

1. 세로형 720×1280 단조·강화·피버 UI 목업.
2. 장비 생애주기, 소유자·제작자·강화 이력·수식어 정보 카드.
3. 일반 강화와 +10 특수 강화의 위험·보상·복구 선택 비교 화면.
4. 재료·촉매·보조재료·정밀 강화의 선택 관계 시각화.
5. 고객·상인·검투사와 판매·의뢰 흐름 장면.

## 기획 종료 후보

1. Google Play 세로 스크린샷·키아트·아이콘·피처 그래픽 후보.
2. 실제 모바일 HUD·버튼·확률·비용·파괴 위험 고도화 목업.
3. 대표 장비·대장장이·고객 캐릭터 시트.
4. 장비 역사·강화 결과·판매 가치 카드 체계.

상태는 `PLANNED → GENERATED_EXPLORATION → IN_REVIEW → REVISION_REQUIRED/REJECTED/APPROVED_CANDIDATE → PROJECT_ASSET_APPROVED → APPLIED_AND_RUNTIME_VERIFIED`다. 실제 모바일 크기·터치·한글·수치·손·망치·무기·광원·특정 IP 유사성·원출처·라이선스를 검수한다. 생성 이미지는 자동 최종 자산이 아니다.
""")
    write("docs/BCA_VISUAL_SHEET_ADOPTION_AUDIT.md",f"""# Blacksmith BCA v8 적용 적대적 검토

```yaml
base_commit: {BASE_SHA}
project_sheet_status: NOT_CONFIGURED
product_paths_changed: false
final_status: CONFLICT_FIXED
```

- `MUST_FIX`: Base SHA·v8 실행문·Sheet·이미지 승인 adapter 부재 → 설치.
- `MUST_FIX`: 사용자의 과거 명시 요청 조건이 새 승인된 기획 이미지 workflow를 막음 → 단계·브리프·검수 조건으로 교체.
- `MUST_FIX`: Android 실제 화면과 최종 자산 상태 분리 부족 → lifecycle·QA 추가.
- `ALLOWED_LEGACY`: 기존 PoC·Prototype 구현 사실은 역사·현재 구현 상태로 보존하며 별도 제품 Gate 권한으로 사용하지 않음.
- `BLOCKED_UNVERIFIED`: 실제 Sheet, 생성 이미지, Android 실기기·AAB·런타임 검수.
""")

def patch():
    p=ROOT/"docs/BASE_RULES_VERSION.md"; t=p.read_text(encoding="utf-8").replace("41a20584dd2ee51d917e5c9d7cab6838e1ceba7e",BASE_SHA).replace("동기화일: 2026-07-23","동기화일: 2026-07-28")
    if "## BCA v8 채택" not in t: t=t.rstrip()+f"\n\n## BCA v8 채택\n\n- 활성 통합 실행문: `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`.\n- Sheet: `NOT_CONFIGURED`; `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`.\n- GPT 이미지·목업: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md`.\n- 생성 이미지는 검수·승인·실제 적용 전 최종 자산이 아니다.\n"
    p.write_text(t,encoding="utf-8")
    append_once("README.md","## BCA v8 기획·이미지·Sheet 운영",f"""## BCA v8 기획·이미지·Sheet 운영

- Base: `alsdmlals4-eng/Base@{BASE_SHA}`
- 통합 실행문: `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`
- Sheet: `NOT_CONFIGURED`; `docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md`
- GPT 이미지·검수: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md`
- 적대적 검토: `docs/BCA_VISUAL_SHEET_ADOPTION_AUDIT.md`
""")
    append_once("AGENTS.md","## BCA Sheet·GPT 이미지 생성·검수",f"""## BCA Sheet·GPT 이미지 생성·검수

- Base 기준은 `alsdmlals4-eng/Base@{BASE_SHA}`와 v8 통합 실행문이다.
- 프로젝트 Sheet는 `NOT_CONFIGURED`; URL 확인 전 신규 Sheet를 추정 생성하지 않는다.
- 사용자가 승인한 BCA workflow 안에서 GPT가 기획 중 시각화와 기획 종료 후보 이미지를 생성할 수 있다.
- 생성 이미지는 자동 최종 자산이 아니며 모바일 실제 화면·구현 가능성·권리·오류·Asset Ledger 검수 뒤 승인한다.
- 각 단계 뒤 `repository-wide-audit`로 stale Prompt·untouched 소비자·승인 누락을 재검사한다.
""")
    reg=ROOT/"[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json"; data=json.loads(reg.read_text(encoding="utf-8"))
    data["base_integration"]={"repository":"alsdmlals4-eng/Base","commit":BASE_SHA,"integrated_execution_prompt":"templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md","project_sheet_status":"NOT_CONFIGURED","project_sheet_contract":"docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md","image_workflow":"docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md","copy_skill_bodies":False}
    data["bca_visual_sheet"]={"status":"ADOPTED","required_tabs":TABS,"image_modes":["planning-visualization","final-visual-candidate","visual-qa-and-approval"],"adversarial_mode":"repository-wide-audit"}
    by={x["skill_id"]:x for x in data["skills"]}
    gd=by["blacksmith-game-design"]
    for tag in ("worldbuilding","main-characters","supporting-characters","core-systems","main-content","planning-visualization","final-visual-candidate","image-mockup"):
        if tag not in gd["trigger_tags"]: gd["trigger_tags"].append(tag)
    for mode in ("planning-visualization","final-visual-candidate","visual-brief"):
        if mode not in gd["skill_modes"]: gd["skill_modes"].append(mode)
    gd["review_triggers"]=["이미지 단계·브리프·승인 로그 없는 생성" if x=="명시적 요청 없는 이미지 생성" else x for x in gd["review_triggers"]]
    qa=by["blacksmith-qa"]
    for tag in ("sheet-structure","image-approval","visual-qa","stale-prompt","bca-adoption"):
        if tag not in qa["trigger_tags"]: qa["trigger_tags"].append(tag)
    for mode in ("visual-qa-and-approval","repository-wide-audit","bca-adoption-audit"):
        if mode not in qa["skill_modes"]: qa["skill_modes"].append(mode)
    reg.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    skill=ROOT/"skills/game-design/SKILL.md"; t=skill.read_text(encoding="utf-8")
    if "`planning-visualization`" not in t: t=t.replace("- `art-brief`: 사용자가 명시적으로 요청하고 승인한 아트 방향만 생성·편집 프롬프트와 기술 제약으로 변환한다.","- `art-brief`: 승인된 아트 방향을 생성·편집 프롬프트와 기술 제약으로 변환한다.\n- `planning-visualization`: 기획 중 단조·강화·장비 생애주기·세로 UI 목업으로 구조와 모순을 비교한다.\n- `final-visual-candidate`: 기획 종료 후 Demo·Google Play·UI·캐릭터·장비 후보를 만든다.\n- `visual-qa-and-approval`: 실제 모바일 화면·구현·권리·오류·승인 상태를 검수한다.")
    t=t.replace("이미지 생성은 사용자의 명시적 요청 없이는 실행하지 않는다.","이미지 생성은 승인된 BCA workflow·브리프 안에서 실행하며 생성 결과를 자동 최종 자산으로 사용하지 않는다.")
    t=t.replace("- 사용자의 명시적 요청 없이 이미지를 생성한다.","- 이미지 단계·브리프·검수·승인 원장 없이 생성하거나 자동 최종 자산으로 사용한다.")
    skill.write_text(t,encoding="utf-8")

def test_workflow():
    write("tests/test_bca_visual_sheet_adoption.py",f'''from __future__ import annotations
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE_SHA="{BASE_SHA}"
class TestBCA(unittest.TestCase):
 def test_pin(self):
  for p in ("README.md","AGENTS.md","docs/BASE_RULES_VERSION.md"): self.assertIn(BASE_SHA,(ROOT/p).read_text(encoding="utf-8"),p)
 def test_contracts(self):
  s=(ROOT/"docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md").read_text(encoding="utf-8"); v=(ROOT/"docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md").read_text(encoding="utf-8")
  for x in ("11_세계관","12_핵심루프","13_주요인물","14_조연_세력_관계","40_핵심시스템_메인콘텐츠","71_이미지기획_생성목록","72_이미지검수_승인로그","NOT_CONFIGURED"): self.assertIn(x,s)
  for x in ("planning-visualization","final-visual-candidate","visual-qa-and-approval","PROJECT_ASSET_APPROVED","자동 최종 자산"): self.assertIn(x,v)
 def test_registry(self):
  r=json.loads((ROOT/"[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json").read_text(encoding="utf-8")); self.assertEqual(r["base_integration"]["commit"],BASE_SHA); self.assertEqual(r["bca_visual_sheet"]["status"],"ADOPTED")
if __name__=="__main__": unittest.main()
''')
    write(".github/workflows/validate-bca-visual-sheet-adoption.yml",'''name: Validate Blacksmith BCA Adoption
on:
  pull_request:
    branches: [main]
    paths: ["README.md","AGENTS.md","docs/**","skills/**","[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json","tests/test_bca_visual_sheet_adoption.py",".github/workflows/validate-bca-visual-sheet-adoption.yml"]
permissions: {contents: read}
concurrency:
  group: blacksmith-bca-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
jobs:
  contract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: python -m unittest tests.test_bca_visual_sheet_adoption -v
      - run: git diff --check origin/main...HEAD
''')

def main(): docs(); patch(); test_workflow()
if __name__=="__main__": main()
