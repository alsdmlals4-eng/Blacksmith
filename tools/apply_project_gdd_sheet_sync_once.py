from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE_SHA="c987647d01ad2baa028a16e03d85ddfc1572a727"
SHEET_ID="1DGNgLmn6nV3BwK795Y_GjS4wu8pbnIVdkLa8xzQRNWg"
SHEET_URL=f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
TABS=["00_프로젝트_허브","01_작업순서","02_현재_확정결정","03_근거_라이브러리","04_누락_충돌_감사","05_GDD_요약","10_제품방향","11_세계관","12_핵심루프","13_주요인물","14_조연_세력_관계","15_조작_게임규칙","20_코어경험_데모목표","30_데모범위_품질기준_제작기반","40_핵심시스템_메인콘텐츠","41_성장_경제","50_메인콘텐츠","60_UX_UI_접근성","70_아트_오디오_에셋","71_이미지기획_생성목록","72_이미지검수_승인로그","80_데모_버티컬슬라이스_플레이테스트","90_본제작_출시_사업","98_Base_반영후보","99_변경이력"]
for p in ["README.md","AGENTS.md","docs/BASE_RULES_VERSION.md","docs/BCA_VISUAL_SHEET_ADOPTION_AUDIT.md","docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md"]:
 f=ROOT/p
 if f.exists():
  t=f.read_text(encoding="utf-8")
  t=t.replace("7072b9e2742a60d7548fd39df3328ad76a8dbad1",BASE_SHA).replace("NOT_CONFIGURED","PROJECT_SHEET_CONFIGURED")
  t=t.replace("정확한 URL·권한을 확인하기 전에는 새 Sheet를 추정 생성하지 않는다.","검증된 URL·ID·탭을 사용하고 사용자 Sheet 수정은 `PROPOSED_SHEET_CHANGE`로 보존한다.")
  t=t.replace("실제 Google Sheet URL·권한과 실제 생성 이미지·런타임 검수","실제 생성 이미지·런타임·사용자 시각 검수")
  f.write_text(t,encoding="utf-8")
lines=["# 블랙스미스 프로젝트 Google Sheets Workbook","","```yaml","project: Blacksmith","sheet_status: PROJECT_SHEET_CONFIGURED",f"spreadsheet_url: {SHEET_URL}",f"spreadsheet_id: {SHEET_ID}","workbook_role: USER_FACING_GDD_WORKSPACE","sheet_edit_policy: PROPOSED_SHEET_CHANGE",f"base_commit: {BASE_SHA}","last_verified_at: 2026-07-29","```","","Google Sheets는 제작·강화·장비 연대기·고객·경제의 전체 흐름을 사용자가 확인·수정하고 AI가 GitHub 정본·실제 구현과 함께 읽는 GDD 작업면이다.","","## 검증된 탭"]
lines += [f"- `{x}`" for x in TABS]
lines += ["","## 프로젝트 책임 매핑","","| 의미 구조 | 프로젝트 책임 원본 |","|---|---|","| 핵심루프 | 단조→강화→+5 납품/+10 도전→고객·시장 환류 |","| 핵심시스템 | `BLACKSMITH_GAME_BIBLE.md`, 강화·보호·장비 생애주기 결정 정본 |","| 성장·경제 | 골드·보호석·완충 충전·고강화 시장 정본 |","| 주요인물·관계 | 대장장이·고객4종·상인·검투사 기획 정본 |","| 이미지 계획·검수 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_WORKFLOW.md` |","","GitHub에 없는 사용자 수정은 `PROPOSED_SHEET_CHANGE`로 보존하고 승인 후 양쪽을 재조회한다."]
(ROOT/"docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
rp=ROOT/"skills/SKILL_REGISTRY.json"; r=json.loads(rp.read_text(encoding="utf-8")); b=r["base_source"]; b["commit"]=BASE_SHA; b.update({"project_sheet_status":"PROJECT_SHEET_CONFIGURED","project_sheet_url":SHEET_URL,"project_sheet_id":SHEET_ID,"project_sheet_role":"USER_FACING_GDD_WORKSPACE","project_sheet_edit_policy":"PROPOSED_SHEET_CHANGE","project_sheet_last_verified_at":"2026-07-29"}); v=r["bca_visual_sheet"]; v.update({"sheet_status":"PROJECT_SHEET_CONFIGURED","spreadsheet_url":SHEET_URL,"spreadsheet_id":SHEET_ID,"workbook_role":"USER_FACING_GDD_WORKSPACE","sheet_edit_policy":"PROPOSED_SHEET_CHANGE","last_verified_at":"2026-07-29","required_tabs":TABS}); rp.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
test=f'''from __future__ import annotations
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE_SHA="{BASE_SHA}"; SHEET_ID="{SHEET_ID}"
class BCAAdoptionTests(unittest.TestCase):
 def test_contract(self):
  for p in ("README.md","AGENTS.md","docs/BASE_RULES_VERSION.md"): self.assertIn(BASE_SHA,(ROOT/p).read_text(encoding="utf-8"),p)
  s=(ROOT/"docs/PROJECT_GOOGLE_SHEET_WORKBOOK.md").read_text(encoding="utf-8")
  for x in ("PROJECT_SHEET_CONFIGURED",SHEET_ID,"USER_FACING_GDD_WORKSPACE","PROPOSED_SHEET_CHANGE","05_GDD_요약","15_조작_게임규칙"): self.assertIn(x,s)
 def test_registry(self):
  r=json.loads((ROOT/"skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")); self.assertEqual(r["base_source"]["commit"],BASE_SHA); self.assertEqual(r["bca_visual_sheet"]["spreadsheet_id"],SHEET_ID); self.assertIn("05_GDD_요약",r["bca_visual_sheet"]["required_tabs"])
if __name__=="__main__": unittest.main()
'''; (ROOT/"tests/test_bca_visual_sheet_adoption.py").write_text(test,encoding="utf-8")
