"""Read candidate binaries; emit factual provenance, never edit image pixels."""
import hashlib,json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/'docs/design/candidates/blueprint-20260911'
CONSUMERS={'items':'Inventory/Enhancement/Customer item icon regions','forge':'Workshop background layer','adventure':'WorldWindow adventure background','duel':'WorldWindow duel background','army':'WorldWindow army background','smith':'Workshop smith action layer','actor':'WorldWindow actor animation layer'}
SOURCES={'items':'exec-7bb45ee6-0ee1-4856-acd6-c243e9fcf5a5.png','forge':'exec-f47698fc-52be-48e2-9de2-6e698fb7606d.png','adventure':'exec-e7228800-abd5-4e35-8936-7f4acd270ee9.png','duel':'exec-b78a643c-d53b-42d3-990d-83d7f4b81dd4.png','army':'exec-9b1e7f8b-1b0c-4d81-ab37-cd8bc00b42ac.png','smith':'exec-4c2543cd-4d13-4474-849d-a1f67c055d4e.png','actor':'exec-86db1055-ec37-4146-9659-63dda4cd15b5.png'}
def main():
    assets=[]
    for key,consumer in CONSUMERS.items():
        path=FOLDER/(key+'.png')
        with Image.open(path) as im:
            hist=im.convert('RGBA').getchannel('A').histogram()
            item={'id':'BS-BP11-'+key.upper(),'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'width':im.width,'height':im.height,'alpha_zero':hist[0],'alpha_opaque':hist[255],'alpha_partial':sum(hist[1:255]),'consumer':consumer,'status':'REVIEWED_CANDIDATE_NOT_ASSET_READY','source_filename':SOURCES[key],'generator':'image_gen; exact model not exposed','runtime_promoted':False,'user_approved':False}
        if key=='items':
            item['processing']='Restricted Aseprite MCP nearest resize 1254 to 384; copy_sprite to items.aseprite; export roundtrip verified separately'
            item['regions']=[{'id':name,'rect':[i%3*128,i//3*128,128,128]} for i,name in enumerate(['iron_sword','iron_shield','iron_bow','iron_armor','iron_helmet','fire_heart','earth_crystal','iron_ingot','reinforcement'])]
            item['qa_remaining']=['partial alpha interior review','64px readability','tag/damage overlays','engine import']
        elif key in ('smith','actor'):
            item['qa_remaining']=['equal cell boundaries','foot and grip alignment','all required states','true alpha/background','motion continuity','engine import']
            if key=='actor':
                item['status']='REJECTED_RUNTIME_INPUT_BAKED_CHECKERBOARD'
                item['primary_use_disposition']='Failed planned game-surface candidate; retained in review only to explain blocking defect, not an explanatory commissioned asset'
                item['failed_correction']={'source_filename':'exec-6ae584ec-ea59-4013-bd3f-84e34aad94cd.png','sha256':'1a25aad11450435fd77570071d2a732923f0d99fc528425e23a87b03a2e6d4b9','mode':'RGB','alpha_zero':0,'result':'REJECTED; no background removal achieved; not copied into repository'}
        else:item['qa_remaining']=['base pixel-grid normalization','representative actor composition','small-screen contrast','engine import']
        assets.append(item)
    record={'schema_version':1,'user_instruction':'2026-09-11 implementation-ready planning and actual-consumer images; final approval pending','brief':'docs/design/BLACKSMITH_HUMAN_BLUEPRINT_PRODUCTION_20260911.md','assets':assets,'evidence_ceiling':'No runtime, Android, human, rights or release PASS'}
    (FOLDER/'record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps([{'id':a['id'],'size':[a['width'],a['height']],'transparent':a['alpha_zero'],'partial':a['alpha_partial']} for a in assets]))
if __name__=='__main__':main()
