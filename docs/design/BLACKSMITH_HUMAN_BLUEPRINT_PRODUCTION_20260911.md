# 모루의 서약 통합 블루프린트 제작 계약

최신 사용자 요청(2026-09-11): 타 프로젝트의 사람용 PDF는 구조만 참고하고, 상세 기획·조사·SWOT 보완·실제 게임용 후보 자산·아틀라스·데이터·구현 인수인계를 완성해 최종 검토로 제출한다. IMAGE_PRODUCTION_RESUMED_BY_USER. 제품 구현은 최종 승인 전 금지한다.

## 범위와 책임

- PLAN / NONCODING_BUILD / REVIEW. 게임 디자인·brainstorming·PDF·imagegen·Aseprite 패키징을 사용한다.
- 기존21쪽 보충편은 보존한다. 새 통합 편집본은 기존 규칙의 읽기 뷰와 신규 상세 권장안을 구분한다. 기존 게임·저장·승인 binary는 변경하지 않는다.
- 이전 이미지 보류 문구는 과거 체크포인트이며 이번 후보 제작에는 적용하지 않는다. 후보 생성은 최종 그림체 승인·runtime 승격이 아니다.
- PR371은 현재 작업의 직접 후속이다. PR359/196은 읽기 전용. 프로젝트 v9.4.4 잠금을 유지하며 Base current는 관찰만 한다.
- 예시 PDF의92쪽·아틀라스·6부 구조를 확인했다. 게임 규칙·캐릭터·이미지·수치는 가져오지 않는다.
- 대안: 보충편 누적(중복·탐색 불리), 축약본(상세 손실), 통합 편집(선택; coverage 검증 필요).
- 제작 체크: 정본/consumer 확인 → 조사 → 상세 규칙/수치/예외 → 실제 사용처 이미지 → 아틀라스/모션 계약 → PDF → 전 페이지 렌더/누락 검사 → 원격 검증. 완료 체크는 증거 후만 갱신한다.

## 신규 후보 Visual Requirement

공통 스타일: 중간 밀도 판타지 픽셀, 강철 청회색/청동/갈색 가죽/청록 직물, 명확한 실루엣, 원작 캐릭터·로고 복제 금지. 그림 안 글자·UI·설명문 금지. 원본은 보존하며 최종 표시 크기에서 검수한다. 실제 게임에서 소비할 영역을 문서가 미리 보여 주는 것이며 장식 전용 출력이 아니다.

| consumer_id | surface / implementation owner | 역할 / primary_use | 목표 규격 | 상태군 / fallback |
|---|---|---|---|---|
| BP11-ITEM-ATLAS | vs_workshop_screen.gd / equipment catalog의 신규 픽셀 표시 | 인벤토리·강화·인계의5종 장비+2촉매+주괴+보강재 아이콘 | 3x3 동일 정사각형 셀, PNG RGBA; 생산 셀128 목표 | 기본만, 등급 불변; 태그/손상은 별도 상태/텍스트. 미채택은 기존 게임 유지 |
| BP11-FORGE | vs_workshop_screen.gd 상단 배경 | 공방 고정 작업 공간 | 3:2, 정수 스케일 후보,360x248/136 crop 시험 | 인물·모루 없는 작업 바닥; 동작용 소품 분리. 미채택은 기존 배경 |
| BP11-ADVENTURE | planned WorldEventPanel ADVENTURE | 수로 사건 재현의 배경 | 3:2 가로 환경, 하단 이동 바닥 | 정적 배경, 텍스트 요약 fallback |
| BP11-DUEL | planned WorldEventPanel DUEL | 콜로세움 재현 배경 | 3:2, 옆면 바닥 | 정적 배경, 텍스트 요약 fallback |
| BP11-ARMY | planned WorldEventPanel ARMY | 전선 대표 병력의 배경 | 3:2, 옆면 바닥 | 정적 배경, 텍스트 요약 fallback |
| BP11-SMITH-MOTION | workshop smith AnimatedSprite2D 계획 | 망치 준비/내리침/접촉/복귀 | 4x2 동일 셀 RGBA; 각셀128 목표 | 8프레임 연결 후보, 발/모루/그립 고정; 불연속 시 생산 준비 미완료 |
| BP11-WORLD-ACTOR | world actor AnimatedSprite2D 계획 | 준비/이동/사용/방어/피격/성공/실패 | 4x2 동일 셀 RGBA; 각셀128 목표 | 8키포즈 후보, 키포즈만으로 전체 모션 완료 주장 금지 |

모든 후보는 primary_use=PLANNED_GAME_SURFACE, runtime_asset_role은 위 표, source/PNG/metadata/alpha/사용영역은 후보 record에 남긴다. 이미지 모델로 창작하고 연결된 restricted Aseprite로 허용된 정리·내보내기만 한다. 도구 범위 밖의 임의 Lua/픽셀 그리기로 대체하지 않는다. UI 와이어프레임·흐름·관계는 text-native 도식이며 생성 그림으로 만들지 않는다.

## 위험 및 증거 상한

### 후속: 청년 대장장이 그림체 비교와 모닥

최신 사용자 요청은 젊고 잘생긴 애니메이션풍 대장장이 3개 그림체 비교와 불꽃 정령 1개 제작이다. 전면 픽셀 방향은 유지한다. 이전 수염 대장장이 시트는 새 주인공 방향의 최종 외형이 아니라 비교 이력이다. 기존 41쪽 PDF는 이번 선택 전 자동 교체하지 않는다.

| requirement_id | consumer / owner | primary_use / 규격 | 상태군과 미채택 fallback |
|---|---|---|---|
| BP11-SMITH-STYLE | BP11-SMITH-MOTION / planned workshop AnimatedSprite2D, `scripts/vertical_slice/ui/vs_workshop_screen.gd` 화면 | PLANNED_GAME_SURFACE, 청년 주인공 외형 소스, 세로 1024×1536 요청, 실제 출력은 record | 세 그림체에서 기본 정지 1포즈씩 비교. 선택 후 128셀 정리·준비/접촉/복귀 제작 필요. 미채택 후보는 참고만 유지, 기존 게임 불변 |
| BP11-MODAK-STYLE | planned workshop companion sprite, 위 화면 소속 예정 | PLANNED_GAME_SURFACE, 불꽃 정령 기본 외형, 정사각 1024 요청 | 기본 1포즈. idle/기쁨/걱정/집중 상태와 32~64px 판독성 후속 검수. 미채택은 미구현 유지 |

생성 전 실제 공방 후보 `candidates/blueprint-20260911/forge.png`를 확인해 팔레트/세계 참조로 첨부했다. 캐릭터 복제가 아니라 청회색·가죽·청록·화염의 조화를 유지한다. 대장장이는 20대 초반 성인, 수염 없음, 과장 근육 제외, 망치·앞치마를 공통으로 둔다. 세 그림체는 정통 JRPG/각진 셀 애니메이션/부드러운 청춘형을 비교한다. 기존 모닥 방향 기록의 밝은 노랑·주황, 차분한 감정 표현, 검은 숯 몸체 제외를 최신 픽셀 요청에 맞게 적용한다. 모닥의 새 능력·보상·자동 강화는 추가하지 않는다.

조사(2026-09-11): [Sea of Stars 공식 제작사 자료](https://sabotagestudio.com/presskits/sea-of-stars/)의 현대적인 2D 픽셀 표현을 ADAPT하고, [Potion Permit 공식 배급사 자료](https://pqube.co.uk/games/potion-permit/)의 직업 주인공·동반자 구성을 ADAPT한다. 이는 비교 원리이며 캐릭터/복장/능력 복제는 REJECT한다. 작은 공방 공간에서 얼굴과 망치가 서로 뭉개지는지, 멋진 인상이 노화·과장 근육으로 바뀌는지, 정령이 촉매 아이콘과 혼동되는지를 후속 반례 검수한다. 상업 성공·사용자 선호는 조사만으로 증명하지 않는다.

실제 출력·프롬프트·해시·알파·미완성 상태는 `candidates/young-smith-spirit-20260911/record.json`에 바인딩한다. imagegen 내장 도구 사용. 이번은 그림체 선택 단계라 Aseprite 전체 모션 패키징을 선행하지 않는다. 생성/정적 검수/사용자 선택/정본 승격/게임 적용은 별도 상태다.

출력 검수: 대장장이1/3은 RGBA지만 주변 halo/반투명 정리가 필요하고, 대장장이2/모닥은 RGB 바둑판이 포함돼 runtime 입력으로 반려한다. 4장 모두 요청한 그림체 비교용으로만 보존한다. 새 생성물로 ASSET_READY를 주장하지 않는다. 권장 선택은 대장장이1이며 최종 선택 뒤 선택본만 정리한다. 별도 거대 비교 PDF나 중복 대시보드는 만들지 않았고 기존41쪽 PDF/source binding은 유지한다.

생성기의 알파·셀 정렬·동작 연속성이 실패할 수 있다. 실제 출력으로 판단하고 재제작/미준비를 표시한다. 필요한 파일이 있다는 이유로 ASSET_READY를 선언하지 않는다. 수치의 계산 검증과 재미·Android·권리·출시 검증을 분리한다. 광고/IAP/온라인·직원 경영·새 전투 조작 시스템은 추가하지 않는다.

롤백은 새 문서/후보/검사 변경의 정상 revert. 기존 PDF·원본 자산·세이브 삭제 없음. Base 승격은 이 작업의 자동 결과가 아니다.

## 제작·검수 체크포인트

- 재개 체크: 직전915bc629 원격 검사15SUCCESS/1조건부SKIPPED, 작업 브랜치0/0 확인. 모닥 배경제거 편집1회는1254×1254 RGB로 바둑판이 남아 반려했다. 원본 후보4장은 불변, 실패 binary는 저장소에 중복 복사하지 않고 record의refinements에 출처/해시/프롬프트를 남겼다. [Aseprite 공식 알파 정의](https://www.aseprite.org/docs/color-mode/)를 재확인했으며 보이는 바둑판을 투명도 증거로 쓰지 않는다. 같은 편집 반복 대신 지원되는 배경 처리 경로 점검이 필요하다. 대장장이 최종 선택·모션·게임 적용은 여전히 미완료. AgentMemory 세션 도구가 이번 연결 목록에 없어 현재 저장소와 Git 검증으로 재개했으며 세션 조회 성공을 주장하지 않는다.

-41쪽/41절 통합 PDF 생성, 전체 페이지 렌더 검사. 표 머리글 대비 교정, 불가능한+10·태그II 예시를+20으로 수정, 사건 준비도 cap 예시와 수리비 확보구간 설명 교정 후 해당 페이지 재검수.
- 신규7가족 중 배경4·장비/재료 아틀라스·대장장이 후보 확보. 세계 인물 시트와 배경제거 편집은 둘 다RGB 바둑판으로 runtime 입력 반려. 두 번째 반려 binary는 저장소에 중복 복사하지 않고 hash/source locator만 기록.
- 장비 atlas는 restricted Aseprite의 최근접384출력·native원본·PNG내보내기 decoded RGBA 동일 확인. 마무리 픽셀·알파·전체 모션/장착/상태·engine import는 미완료.
- PDF/source/후보 해시 및41페이지 계약 검사. 기존21쪽 PDF와 게임 보호 경로는 변경하지 않았다.
- Base 검사는 jsonschema가 있는 기존 Python에서 실행. 문서 번들 Python에 jsonschema가 없어 실패한 검사는 환경 원인을 확인하고 기존 검증 런타임에서 다시 PASS를 확인했다. 불필요한 패키지 설치 없음.
- L1 resume 검사는 PASS. 전체 작업이IN_PROGRESS이고 자산·최종사용자검토가 남아 closeout은 정상적으로 거부된다. 이를 회피하기 위해 DONE으로 바꾸지 않는다.
- 학습 후보: PNG확장자/바둑판 표시를 투명도 증거로 쓰지 않기, 조건부 확률과 최종확률 분리, 태그단계 예시에 도달가능성 검사, 작업용 PDF를 모든 자산 준비 완료로 오인하지 않기. 프로젝트에 먼저 검증을 남기며 공용 Base는 이번에 수정하지 않았다.
- 원격 첫 검사에서 Active Context의 연속 상단 추가가 기존 priority/provenance 안내를2500자 밖으로 밀어낸 실패를 발견했다. 최신 안내 바로 위에서 현재 우선순위와 기존 결정 원장 연결을 명시해 수정한다. 역사 원장 내용을 최신 권한으로 승격하거나 검사 범위를 느슨하게 바꾸지 않는다.
