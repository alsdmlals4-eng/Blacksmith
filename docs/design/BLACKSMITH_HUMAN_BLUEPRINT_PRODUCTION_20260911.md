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

생성기의 알파·셀 정렬·동작 연속성이 실패할 수 있다. 실제 출력으로 판단하고 재제작/미준비를 표시한다. 필요한 파일이 있다는 이유로 ASSET_READY를 선언하지 않는다. 수치의 계산 검증과 재미·Android·권리·출시 검증을 분리한다. 광고/IAP/온라인·직원 경영·새 전투 조작 시스템은 추가하지 않는다.

롤백은 새 문서/후보/검사 변경의 정상 revert. 기존 PDF·원본 자산·세이브 삭제 없음. Base 승격은 이 작업의 자동 결과가 아니다.

## 제작·검수 체크포인트

-41쪽/41절 통합 PDF 생성, 전체 페이지 렌더 검사. 표 머리글 대비 교정, 불가능한+10·태그II 예시를+20으로 수정, 사건 준비도 cap 예시와 수리비 확보구간 설명 교정 후 해당 페이지 재검수.
- 신규7가족 중 배경4·장비/재료 아틀라스·대장장이 후보 확보. 세계 인물 시트와 배경제거 편집은 둘 다RGB 바둑판으로 runtime 입력 반려. 두 번째 반려 binary는 저장소에 중복 복사하지 않고 hash/source locator만 기록.
- 장비 atlas는 restricted Aseprite의 최근접384출력·native원본·PNG내보내기 decoded RGBA 동일 확인. 마무리 픽셀·알파·전체 모션/장착/상태·engine import는 미완료.
- PDF/source/후보 해시 및41페이지 계약 검사. 기존21쪽 PDF와 게임 보호 경로는 변경하지 않았다.
- Base 검사는 jsonschema가 있는 기존 Python에서 실행. 문서 번들 Python에 jsonschema가 없어 실패한 검사는 환경 원인을 확인하고 기존 검증 런타임에서 다시 PASS를 확인했다. 불필요한 패키지 설치 없음.
- L1 resume 검사는 PASS. 전체 작업이IN_PROGRESS이고 자산·최종사용자검토가 남아 closeout은 정상적으로 거부된다. 이를 회피하기 위해 DONE으로 바꾸지 않는다.
- 학습 후보: PNG확장자/바둑판 표시를 투명도 증거로 쓰지 않기, 조건부 확률과 최종확률 분리, 태그단계 예시에 도달가능성 검사, 작업용 PDF를 모든 자산 준비 완료로 오인하지 않기. 프로젝트에 먼저 검증을 남기며 공용 Base는 이번에 수정하지 않았다.
