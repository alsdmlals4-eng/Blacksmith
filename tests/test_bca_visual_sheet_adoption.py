from __future__ import annotations
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE_SHA="7072b9e2742a60d7548fd39df3328ad76a8dbad1"
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
