# 모루의 서약 — 남은 작업 설계·구현 명세

작성일 2026-09-14 · BS-SPEC-20260914-01 · 상태 SPECIFIED_WITH_EXPLICIT_GATES

## 0. 범위·읽는 법·현재 증거

최신 사용자 요청 BS-REPLAN-20260914-08은 이 명세 순서대로 조사·구체화·구현·검증·개선을 계속 진행하는 것이다. 아래 최초 준비 시점의 수치와 증거는 역사 기준선이며 현재 실행 경계는 제작 계약 최상단을 따른다. 기존 승인 방향을 실행 가능한 작업으로 분해하는 책임 원본이며, 새 경제·달력의 시험값을 최종 균형이나 제품 구현 완료로 선언하지 않는다. 사람용 블루프린트65~72절은 이 명세의 요약·체크리스트다. 별도 HTML PM은 만들지 않는다.

- 현재 main: `f30baaa60e1fb95905c47d5a8303cd069895ce96` (local/origin 일치 확인).
- 보존한 작업 HEAD: `d73e391e7f81c3f0e349d92505cdeb80fe7063a9`, PR381 Draft. 다른 PR359/196은 읽기 전용.
- Base adopted v9.4.4 / validator43b3 유지. 최신 Base remote d830c0f는 드리프트 참고이며 잠금 교체 권한이 아니다.
- MAIN_VERIFIED: 이전 전달 범위에서 제작·강화·정밀 태그·수리·회복 의뢰·수동 하루 마감·촉매 교환·기존 세계 사용의 기계/일부 데스크톱 증거가 있다. 모든 기능·기기 PASS를 의미하지 않는다.
- BRANCH_MACHINE_VERIFIED: AR 5종 허용과 목록 표시. 해당 HEAD의 GUT315/3278, Python511/3skip 통과. 활 실제 제작→+10→AR 준비 캡처는 있으나 재시작 후 결과까지의 새 전달 검증은 미완료다.
- NOT_RUN: 이번 명세의 신규 시스템 실행, Android 실기기, 사람 플레이 균형, 최종 미술·동작·출시 검수. 현재 보고서 패널을 움직이는 전투 구현으로 세지 않는다.

읽는 순서: 전체 의존관계 → R01~R04 플레이 순환 → R05~R08 성장·시각 연결 → R09~R12 사용성·내구성·완성 검수. 아래 신규 식별자·파일명은 제안이며 실제 파일 존재 주장과 구분한다. 새 영속 필드는 SaveEnvelope 허용 스키마/마이그레이션을 함께 통과해야 한다.

## 1. 정본 차이와 유지할 핵심

| 항목 | 확인한 현재 상태 | 이번 판단·후속 작업 |
|---|---|---|
| 신규 슬롯 지급 | `vs_save_envelope.gd` new replan initializer: Gold20000, 보강재/불의 심장/대지의 결정 = 30 / 64 / 64 | 런타임 사실. 기존 저장을 감액하지 않는다 |
| 블루프린트39 시험 예산 | Gold20000, 보강재/두 촉매 = 60 / 5 / 5 | 경제 비교용 설계값. R04 별도 profile로 검증; 런타임과 동일하다고 쓰지 않는다 |
| 일반 의뢰 | 회복 의뢰의 전용 재료·400Gold/보강재2 보상만 실제 연결 | 일반 선금·납품·회수는 별도 버전/원장. 기존 보상에 가산 금지 |
| 세계 사용 | main AQ방패, DU/AR검·방패; branch AR5종 | R01 검증·전달 전 main 완료로 표시 금지 |
| 모닥 달력 | review JSON120일/년, 3년 차 LATER; 계산 모형만 존재 | RECOMMENDED_NOT_LOCKED. 수동 마감 구현과 성장 구현은 별개 |
| 그림 | 젊은 대장장이1번 및 모닥 EARLY/LATER 외형 승인 | 알파·분리·모션·인게임 검수는 미완료. 승인 외형 보존 |

유지: 정밀강화는 +9→10, +19→20 등 10단위 경계; 촉매는 실제 아이템 자원; 태그 추가/강화와 최대3슬롯; 등급만 달라져도 같은 장비 외형 유지, 강화 단계·태그가 외형 변화 원인. 일반 성공+1, 단계 하락 없음. CURRENT/MAX/BASE_MAX 내구도와 작품UID·흉터·연대기 보존. 세계 결과와 실제 사용 손상은 독립 판정. 모닥은 순진한 어린 불의 정령 조수이며 성장해도 강제 손실·자동 확률 보너스를 만들지 않는다. 픽셀 기본 방향과 모닥의 승인된 비픽셀 예외를 분리한다.

## 2. 조사·선택·독창성

2026-09-14 공식 소개/기술 문서를 확인했다. 아래는 직접 플레이·개발팀 인터뷰 결과가 아니라 공개 1차 자료에서 추출한 설계 패턴이다. 수치·이미지·캐릭터·진영 시스템을 복사하지 않는다.

| 자료 | 관찰 | 적용 판정 |
|---|---|---|
| [Anvil Saga](https://store.steampowered.com/app/1587540/) | 의뢰 선택이 공방 밖 결과와 연결 | ADAPT: 주문 목적을 고정하고 작품 연대기로 결과 회수; 진영 정치 전체는 REJECT |
| [Weapon Shop Fantasy](https://store.steampowered.com/app/599460/) | 제작과 원정의 재료 순환 | ADAPT: 의뢰→제작→사용→재료→재투자; 직원 자동사냥 게임으로 변경은 REJECT |
| [Gladiator Guild Manager](https://store.steampowered.com/app/1043260/) | 장비·준비의 효과를 자동 전투로 관찰 | ADAPT: 준비의 결과를 간단 재현; 실시간 전투 지휘·팀 육성 전체는 REJECT |
| [Godot 저장](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html) | 영속 대상 선별, 설정은 ConfigFile 가능 | ADOPT: 기존 SaveService/Envelope 유지, 설정과 캠페인 분리. 예제 저장 코드를 새 원장으로 이식하지 않음 |
| [Godot 스프라이트](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) | SpriteFrames/AnimationPlayer로 프레임 재생 | ADAPT: 승인 아틀라스·pivot·이벤트를 기존 엔진에 연결. 판정을 애니메이션 콜백에 맡기지 않음 |
| [Android 접근성](https://developer.android.com/guide/topics/ui/accessibility/views/apps-views) | 최소48dp 터치 영역 권장 | ADOPT: 물리 기기 밀도 환산·검사; Godot48px를48dp라고 주장하지 않음 |

차별점: 강한 물건을 많이 파는 것보다, 같은 UID의 작품이 태그·손상·수리 흔적을 지닌 채 고객의 사건을 겪고 돌아오는 연결을 강화한다. 성공/손상을 별도로 보여 주면 ‘임무는 성공했지만 내 작품을 손볼 때’라는 다음 선택이 생긴다. 모닥의 작은 실수는 이 반복에 정서를 더하되 경제 벌칙을 더하지 않는다.

| SWOT | 위험·가능성 | 강화·보완 방법 | 확인할 증거 |
|---|---|---|---|
| 강점 | 태그 목적과 UID 연대기가 연결될 수 있음 | 주문에 목적·적합도 이유를 먼저 공개, 결과에 선택한 태그의 관련성 표시 | 플레이어가 선택 이유와 결과를 설명할 수 있는지 |
| 약점 | 회복·교환 외 일반 경제가 끊기고 화면에 글이 많음 | R02~04 원장 연결, R08 재현과 한 줄 요약/펼침 | 최초 재투자까지 길 잃음·정보 누락 관찰 |
| 기회 | 모바일 짧은 관찰과 공방 애착 결합 | 세계창 접기/펼치기, 모닥 세대별 반응, 의미 사건 연대기 | 세계창을 열지 않아도 진행·정산 동일 |
| 위협 | 강화 피로, 파산, 벤치마크와 유사성 | 회복 경로 고정, 무작위 광고 구제 제외, 작품 일생에 집중 | 자원0에서 회복, 반복감/중단 의향 실플레이 |
| 제작 위험 | 승인 그림을 바로 모션 자산으로 오인 | 상태별 알파·pivot·consumer 명세와 검수 분리 | 실제 프레임·장착·기기 캡처; 후보만으로 PASS 금지 |

## 3. 구현 순서·범위

| 단계 | 작업 | 병행 가능·착수 조건 | 결과 |
|---|---|---|---|
| A | R01 현 브랜치 전달 마감 | 새 기획 구현 없이 기존 코드 검증부터 | 5종 모두 실제 사용 가능한 기준선 |
| B | R02 의뢰 정의 → R03 재료·취소 → R04 납품·경제 | 스키마·소유권 계약 공동 검토 후 순서 구현 | 회복을 넘어 일반 재투자 순환 |
| C | R05 성장 규칙; R06 인물 자산; R07 장비 상태 | R06/07 후보·규격 준비는 B와 독립; runtime 승격은 자산 lock 후 | 성장·행동·외형의 실제 소비처 |
| D | R08 세계 재현; R09 안내·설정 | R08은 R01+승인 배우/장비, R09 구조 준비는 B와 병행 | 보고서 이상의 관찰과 사용성 |
| E | R10 중단 복구는 모든 단계의 수직 테스트 | 새 원장마다 실패점 추가, 끝으로 미루지 않음 | 중복 차감·중복 보상 방지 |
| F | R11 콘텐츠·균형 → R12 기기·최종 검수 | R02~10 연결 플레이가 선행 | 완성 판정과 배포 가능성 분리 |

모든 단계 공통: fresh authority/consumer → 해당 범위 조사 → exact 보호 경로 등록 → RED → 최소 구현 → GREEN → 두 차례 적대 검토 → 실제 실행 → 블루프린트 체크리스트 → 정상 PR/정확 HEAD CI/main readback. 명세 준비 이후 최신 요청으로 구현을 재개했다. R01 native 검증부터 진행하며 R02 이후를 선행 완료로 표시하지 않는다.

## R01 — 5종 장비 세계 사용 전달 마감

**현재 상태:** BRANCH_MACHINE_VERIFIED. 기존 변경은 rules의 WORLD_EQUIPMENT와 workshop 목록 소비. AR검/방패/활/갑옷/투구, AQ방패, DU검/방패. PR381은 Draft이며 runtime 일부만 확인했다.

**선행 조건:** branch exactHEAD 및 활성2경로 승인/PR metadata 재확인. 진행 중 QA 저장과 unrelated imports 보존.

**설계·흐름:** 장비 선택 → AR 목적 선택 → +10·태그·내구도·예약 상태 검사 → PREPARED 저장 → 재시작 → 결과 확정 → 동일UID 귀환·독립 손상·연대기. UI에서 허용5종이 잘리지 않게 표시한다.

**데이터·구현:** 기존 `vs_replan_tag_rules.gd`, `vs_save_envelope.gd`, `vs_customer_actual_use_action_service.gd`, `vs_workshop_screen.gd`. 신규 필드 없음. family whitelist이며 향후 카탈로그 추가가 자동 허용되지 않음. 이벤트별 snapshot/draws 유지.

**실패·복구:** PREPARED 이후 닫아도 같은 두 난수로 복원. 잘못된 장비/낡은 저장 거부 시 원본 보존. 기존 버전으로 되돌릴 때 신규 AR 장비 snapshot이 들어 있는 저장을 옛 빌드에 열지 않는다.

**완료 증거:** 활·갑옷·투구의 실제 준비/확정 저장 회귀, 활부터 신규게임·재시작·결과 캡처 완주, 남은 두 장비 native 흐름, AQ/DU 제한 회귀, 두 번째 전체 리뷰, exact CI/main readback. 현재315/3278 통과만으로 완료 체크하지 않는다.

**제외:** 새 전투 모션·보상·확률 조정·새 세계 family.

## R02 — 일반 의뢰 제시·수락·작품 비교

**현재 상태:** 설계 기반만 있음. 실제 회복 의뢰 서비스는 존재하지만 일반 의뢰 정책의 대체물이 아니다.

**선행 조건:** R01 기준선, R03~04 소유/정산 스키마 합의. 후보 숫자는 RECOMMENDED_NOT_LOCKED 시험 profile로 격리한다.

**설계·흐름:** 제시 카드(목적/장비/최소단계/추천태그/위험/보상/반환) → 상세·UID 비교 → 수락 확인 → 예약 상태. requirements는 offer 생성 시 확정하며 보유 태그·재접속·미수락 날짜 넘김으로 다시 뽑지 않는다. 단계 미달은 이유와 제작/강화 이동 버튼을 표시한다. 기본 의뢰 +0 제작 경로와 정밀 태그 의뢰 +10 경로를 분리한다.

**데이터·구현:** 제안 신규 `vs_commission_service.gd`와 `commission_catalog_v1.json` (아직 없음). 정의: definition_id/version, equipment_id, min_level, recommended_level, purpose_axis, purpose_rhythm, risk_profile, ownership_mode, reward_policy_id, return_policy. instance: order_id, definition_snapshot, offered_day, accepted_day 또는 null, state, reserved_item_uid 또는 null, transaction_ids. validate_definition / preview_offer / accept / reserve_item API는 순수 검증과 저장 command 분리. 실제 workshop 및 기존 EquipmentCatalog/SaveEnvelope를 연결한다.

**실패·복구:** OFFERED→ACCEPTED→CRAFT_READY→HANDED_OFF→SETTLED; CANCELLED는 R03 규칙에서만. 수락 연타 동일 order_id 무효 재적용. 준비 중 COMMISSION_RESERVED 작품은 해당 의뢰를 위한 강화·수리만 허용하고 다른 의뢰·판매·독립 세계 사용은 차단한다. HANDED_OFF/PREPARED 이후 편집은 전면 차단한다. 납품 전 비교만으로 소유권 변하지 않는다. 초기안 기한 없음; 숨은 만료 금지. 전용 제작+0→예약→+10강화→납품을 반드시 연결 시험한다.

**완료 증거:** 고정 제안 재접속 동일, 지원5종 카탈로그 lint, 미달/빈선택/예약충돌 비용0, offer/accept 저장 왕복, 실제 목록→비교→수락 화면. 새 정의 버전 추가 후 기존 수락 snapshot 불변.

**제외:** 진영 평판·일일 랜덤 새로고침·자동 기한·동시 의뢰 슬롯 수 최종 확정.

## R03 — 의뢰 전용 재료·선금·취소 원장

**현재 상태:** 회복 의뢰의 전용 재료1개 소비는 존재. 일반 선금/재료 반환은 새 명세다.

**선행 조건:** R02 인스턴스, R04 시험 경제 profile. `advance`는 자유 지갑 Gold가 아닌 의뢰 귀속 제작 크레딧을 권장한다.

**설계·흐름:** 수락에서 크레딧/재료를 escrow에 배정 → 기본 제작 시 해당 order_id에서만 차감 → 완성 UID 예약 → 납품. 강화·촉매·수리는 개인 지갑으로 명확히 분리하고 위험 선택 비용을 선금으로 보전하지 않는다. UI에 ‘의뢰 전용 / 거래·다른 제작 불가’를 표시한다.

**데이터·구현:** R02 service 내부/작은 원장 helper 제안. escrow {order_id, allocated_credit, consumed_credit, material_id, allocated_qty, consumed_qty, produced_item_uid, reclaimed}; 금액·수량만 비음수 정수이며 consumed≤allocated. ID는 string, produced_item_uid는 제작 전 null, reclaimed는 boolean이다. command_id=order_id+단계+sequence, existing SaveService 원자 저장. 기본 제작 재시도에 무제한 새 전용 재료를 발급하지 않는다.

**실패·복구:** 제작 시작 전 취소는 escrow 전량 회수. 제작 완료·납품 전 취소는 잔여 escrow와 의뢰 재료로 만든 예약 작품을 함께 고객 반납 처리하고 개인 환급0을 먼저 고지한다. 진행 중 제작/세계 PREPARED에는 취소 불가. 개인 강화 비용은 환급하지 않는다. commit 이전 실패만 이전 상태 유지; commit 이후 readback 실패는 COMMIT_UNCERTAIN으로 안내하고 동일 command_id 재읽기로 조정한다. 확인 전 재회수/재지급·성공/무변경 단정 금지. 수락→취소→반복 순이익0.

**완료 증거:** 선금으로 개인 장비 제작/교환 불가, 초과소비·다른 order_id 거부, 취소 전후 자산 합계, 연타·저장실패·재시작 시험, 완성품 부정 보유 방지. 데이터 commit 이전 성공 토스트 없음.

**제외:** 사용자의 기존 자유 제작 아이템을 취소로 몰수, 대출·이자·빚 시스템, 회복 보상 공식을 일반 의뢰로 복사.

## R04 — 납품·반환·정산·일반 재투자

**현재 상태:** 회복400Gold+보강재2와1000Gold→선택촉매1은 별도 시험 정책으로 구현. 일반 납품 및 세계 수익은 아직 연결 전이다.

**선행 조건:** R02/03, R10의 원자 저장. 먼저 버전별 economic_profile과 신규 슬롯 적용 범위를 등록한다.

**설계·흐름:** 납품 확인에서 판매(SALE) / 대여(LOAN), 고정 보수·결과 보너스·반환 조건을 보여 준다. SALE은 소유권 고객 이전 후 작업 잠금. LOAN은 실제사용 PREPARED→결과→같은UID 반환. handoff 자체 손상0. 고정 보수는 commit 단계 하나에서만 지급; 결과 보너스도 별도 once-only 지급. 회복 보상과 일반 보상이 같은 납품에 중복 적용되지 않는다.

**데이터·구현:** 제안 policy `COMMISSION_ECONOMY_TRIAL_V1`; order settlement {order_id, settlement_id, phase, reward_policy_snapshot, gold_delta, material_delta, selected_catalyst, paid, returned_item_uid}. 보너스 초기 시험값0; 기본 재료 제공 + 기본 납품400Gold/보강재2 + 선택 촉매1은 비교 후보일 뿐 RECOMMENDED_NOT_LOCKED. 위험 강화 비용 환급0. 초기 profile A=현재30/64/64, B=블루프린트60/5/5; Gold20000 동일. B 신규 테스트 슬롯에서만 적용, 기존 캠페인 값/회복정책 불변.

소유권 시험 계약: funding_origin=COMMISSION_ESCROW이면 SALE만 허용, 생성 CUSTOMER_COMMISSION_RESERVED→인계 CUSTOMER→종료 CUSTOMER. funding_origin=PLAYER이면 LOAN에서 PLAYER_COMMISSION_RESERVED→CUSTOMER_BORROWED→PLAYER, SALE에서 PLAYER_COMMISSION_RESERVED→CUSTOMER→CUSTOMER. 고객 지원 LOAN은 초기안 거부한다. escrow 재료로 만든 작품이 개인 소유/판매 가능한 재고로 바뀌지 않는 불변식을 검증한다. PLAYER 취소는 본인 예약만 해제하며 작품 회수/몰수 없음.

보고 일정도 남은 작업이다: 기존51절 DU1/AQ2/AR3일 지연은 RECOMMENDED_NOT_LOCKED. handed_off_day와 schedule_policy_id, report_due_day, event_id, 당시 item/requirement/ruleset snapshot, 독립 mission/damage 두 draw를 인계 commit에서 함께 영속 고정한다. 기존 즉시 PREPARED를 날짜 대기 상태로 재사용하지 않고 durable IN_TRANSIT와 일시적 transaction-lock을 구분한다. IN_TRANSIT는 마감 가능하지만 해당 작품 편집은 잠긴다. close_day는 저장된 snapshot/draw만 소비하며 하루 증가와 도래 event_id의 결과/보상 최대1회 확정을 하나의 저장 command로 처리한다. 창 열기가 도래 판정 시계가 아니다. 현재 즉시 처리 trial은 유지하고 새 scheduled policy만 이 분기를 사용한다. 저장 실패/불확실성은 R10과 같은 방식으로 복구한다. due-day cutpoint 실패/재시작 전후 snapshot·draw·result 동일성과 난수 추가소비0을 검증한다.

**실패·복구:** 납품과 지급이 하나의 저장 commit, 조회/세계창 닫기/재실행은 지급 명령이 아니다. 보수 선택 누락 시 저장 전 차단. 이미 판매한 UID를 다시 반환하지 않음. profile 미상은 지급 거부+원본 보존, 임의 fallback 금지.

**완료 증거:** 실제 수락→제작→납품→촉매 선택→다음 정밀강화, 자원0 회복 가능, 실패/손상4조합과 보수 독립, 30회 반복 장부 대조. R11에서 단가·지급량 비교 후 시험/최종 상태 분리.

**제외:** 기존20000Gold 저장 일괄 감액, 최종 가격 확정, 원정/회복/일반 보상 모두 더하기.

## R05 — 모닥 합류·게임 연차·성장 이벤트

**현재 상태:** EARLY/LATER 외형 승인, 달력 JSON의 계산 fixture만 있음. 120일/년·3년 차 전환은 RECOMMENDED_NOT_LOCKED; 빈날240회로 즉시 성장 가능성이 있다.

**선행 조건:** 수동 날짜 commit owner 유지, R02~04 의미 있는 하루/작업 기록, 최종 달력 정책을 기존 저장에 소급하지 않는 버전 설계.

**설계·흐름:** 합류 기록 → EARLY의 서툰 도움 → 같은 외형의 익숙한 조수 반응 → 성장 자격 → 공방 idle에서 LATER 전환 장면 → 스킵/다시 보기. OS시간·오프라인 시간 금지. 권장 비교안 A=달력 연차만, B=달력 연차+서로 다른 실제 납품일30일. B의30은 시험값이며 최종 의미 변경 승인 전 제품 성장 발동을 잠근다. 두 안 모두 세이브 삭제/매년 초기화 없음.

**데이터·구현:** 제안 `vs_modak_growth_service.gd`; modak {joined_day, calendar_policy_id, productive_day_ids, eligible_stage, committed_stage, growth_event_id, presentation_ack}. joined_day 없는 기존 저장은 NOT_JOINED로 해석하고 명시적 합류 흐름으로 연결; 당일 자동 성장 금지. year=floor((day-joined_day)/days_per_year)+1. 성장 판정은 저장 command, 장면은 읽기 전용.

**실패·복구:** 잘못된 음수/소수 날짜·unknown policy 거부. 강화·수리·납품 중 성장 장면 대기. stage commit 후 종료되어도 중복 보상 없음, presentation_ack 미완료만 재생/스킵 가능. actor 준비 전 fallback EARLY + 성장 안내, 후보를 몰래 승격하지 않는다.

**완료 증거:** day1/120/121/240/241 경계, 늦은 합류, 빈날 넘김240회 비교, 저장실패·중복 장면·스킵·재시작, 신규/기존 슬롯 분리. 정책 확정 전 계산기/시험 장면만 준비 가능.

**제외:** 성공확률 버프, 강제 실수 손실, 전투 조작, 달력 길이·성장 자격 최종 lock 대행.

## R06 — 젊은 대장장이·모닥 실제 인게임 자산과 동작

**현재 상태:** smith01/Modak EARLY·LATER 승인 외형은 존재; 후보 이미지=ASSET_READY가 아니다. 기존 후보를 먼저 참조하고 불필요한 다른 얼굴을 새로 만들지 않는다.

**선행 조건:** 최신 Asset Catalog/Visual Requirement, 실제 actor·dialog consumer 확인. 이미지 생성은 모델, 생산 포장/프레임은 채택 Aseprite 선택 지침 확인 후 수행.

**설계·흐름:** smith idle→도구 준비→windup→contact→recover; 모닥 idle/말하기/놀람/머쓱함/도움/기쁨/걱정. EARLY는 작은 실수 후 바로 수습, LATER는 침착해져도 호기심 유지. 강화 결과를 모션이 결정하지 않는다. contact 효과는 attempt_id당1회만, 스킵은 이미 저장한 결과를 즉시 보여 준다.

**데이터·구현:** smith 픽셀 후보128cell의8프레임을 초기 규격으로 검토; 모닥은 승인 비픽셀 portrait와 필요 분리 레이어, 둘을 하나 필터로 처리하지 않음. manifest {asset_id, revision, appearance_lock, sha256, alpha, frame_rects, durations_ms, pivot, attachment_points, state_family, consumer, fallback}. 실제 .aseprite/PNG/frames JSON과 Godot SpriteFrames/AnimationPlayer 리소스. 저작은 승인 HiGodot 경로로; 구체 resource 경로는 자산 등록 시 고정.

**실패·복구:** 불투명 체크보드/흰 테두리/팔다리 연속성 실패는 후보 반려, runtime 기존 승인 자산 유지. 미승인 리소스 이름을 fallback으로 참조 금지. 애니메이션 누락이면 정적 승인 pose+텍스트 결과, 다시 굴림 없음.

**완료 증거:** 밝은/어두운 배경 alpha 검사, 모든 상태·pivot·도구 접점, 64/128 실사용 축소 확인, 양 성장 외형 실제 표시, 같은 transaction의 스킵/저속/재시작 결과 동일. 최종 자산 lock과 runtime 캡처 별도.

**제외:** 모닥 외형 재투표, nonpixel 예외를 공방 전체 그림체 변경으로 확대, 설명용 가짜 게임 스크린샷.

## R07 — 5종 장비 외형·장착·태그 상태군

**현재 상태:** 장비 카드/카탈로그는 실제 소비 중. 새 승인 방향의 단계별 장착/사용 모션 상태군은 미완료다.

**선행 조건:** R06 배우 pivot 규격, 현재 태그/강화/손상 consumer. 같은 종류는 등급만으로 외형 변경 금지.

**설계·흐름:** 기본 실루엣 + 강화 milestone 디테일 + 관련 태그 효과 + 손상/흉터 표식. 권장 시험 milestone +0/+10/+30/+60/+100, 그 사이 단계는 같은 형태와 수치 표시. 세 태그가 공존하면 모두 거대한 이펙트를 겹치지 않고 슬롯별 작은 표식 및 활성 사용 시 관련 효과만 보여 준다.

**데이터·구현:** equipment_id→base_asset; stage_band/tag_state/durability_view→overlay; wield_attachment hand/body/head; 방향별 pivot/손잡이 좌표. 아이콘128cell, 장착용 별도 art role. 5종×기본/손상/주요 단계의 필요한 조합을 카탈로그 검증. 기존 수치 owner를 읽고 별도 damage 상태를 저장하지 않는다. renderer 제안은 순수 조회 `appearance_for(item_snapshot, pose)`; grade 입력은 외형 선택에 사용하지 않음.

**실패·복구:** 알 수 없는 태그 revision은 승인 기본 장비+텍스트 설명, 잘못된 장비로 대체 금지. 활은 당김/놓음, 방패는 막음, 갑옷·투구는 착용 흔들림/피격; 검 휘두르기 reskin으로 대체하지 않는다. 아틀라스 교체 실패 시 이전 revision 복귀.

**완료 증거:** 같은 종류·다른등급의 외형 동일 테스트, +9/10·19/20 경계, 3태그 동시/빈태그, 5/5/5·4/4/5·2/2/5 상태, 양방향 장착·피격 캡처, 무배경 실제alpha. 숫자 보너스와 시각상 강화 효과 중복 적용0.

**제외:** 5종 외 장비 신규 확장, 등급별5벌 자동 생성, 모든 레벨별 별도 이미지100장.

## R08 — 선택형 세계 분할창·사건 모션 재현

**현재 상태:** COLLAPSED/SPLIT/FOCUS 및 보고서 텍스트 표시 있음. 움직이는 콜로세움·모험·군대 장면 전체 구현은 아니다.

**선행 조건:** R01 저장 결과, R06/07 승인 장착·배우 자산. 재현 도중 결과를 다시 계산하지 않는 계약을 먼저 테스트한다.

**설계·흐름:** 공방 집중(접힘) ↔ 세계 위/공방 아래(분할, 기존50절 유지) ↔ 세계 집중. 접힘은 CPU/효과음 정지, 결과 알림 배지 유지. 준비→이동→사용/방어→성공/실패→손상 여부→귀환의 핵심 몇 장면. 닫아도 대기/완료 상태 보존, 플레이어 전투 조작 불필요. 기본 방향은 3개 모드이며 분할 비율 드래그 기능은 후순위다.

**데이터·구현:** 제안 `vs_world_presentation.gd`: read-only projection {event_id, snapshot_revision, asset_revision, beats, cursor}; cursor는 재생용이며 mission/damage authority 아님. 기존 workshop `_refresh_world_viewer`에 자식 presentation scene/SubViewport 1개만 연결. 한 번에 활성 사건1개, 다른 사건은 목록/배지. AQ/DU/AR별 palette/background/actor state를 명시하고 공용 actor 재사용 여부 공개.

**실패·복구:** 저장 outcome 없는 PREPARED는 준비만 표시, 성공 장면 미리 재생 금지. 애셋 누락은 기존 상세 보고서 fallback. 모션중 재실행 시 저장 결과 재현, 보상/손상/연대기 추가0. split의 focus/input이 제작 버튼을 잘못 누르지 않도록 분리.

**완료 증거:** 성공+무손상/성공+손상/실패+무손상/실패+손상4개 분기, 접기/펼치기/스킵/재시작 outcome hash동일, 숨김 processing/audio0, 공방 입력 유지, 실제 화면 전후 아틀라스.

**제외:** 실시간 전투 판정·멀티플레이·새 세계 보상·가짜 generated screenshot을 runtime 증거로 사용.

## R09 — 첫 순환 안내·설정·접근성·사운드

**현재 상태:** 개별 기존 안내/UI는 있으나 새 의뢰·성장·세계 재현을 잇는 통합 검수는 NOT_RUN. 이름 검색만으로 프로젝트 전체 설정 기능 부재를 단정하지 않는다.

**선행 조건:** R02~04 화면 구조, R06/08 효과음 지점. 착수 시 existing settings/audio owner 전수 대조 후 중복 구현 대신 확장한다.

**설계·흐름:** 첫 제작→첫 태그→용도 맞는 의뢰→귀환/수리→재투자 안내. 완료한 단계는 save기반 표시, 스킵해도 기능 잠금 없음. 실패 이유 옆에 다음 행동: 재료 부족→획득, 예약→해당 의뢰, 파손→허용 경로. 설정은 BGM/SFX, 진동, 저동작, 섬광 완화, 큰 글씨; 무음에서도 수치/아이콘/문구만으로 결과 판독.

**데이터·구현:** settings는 ConfigFile 또는 기존 owner 재사용, 범위값 검증·기본값 유지. tutorial checkpoint는 캠페인 실제 완료 이벤트에서 파생/저장; 버튼 클릭만으로 지급하지 않음. 기본 UI의 컨트롤 간격·폰트 계층을 재사용, 모달 focus/뒤로가기 경로 정의. bus별효과음은 재현과 gameplay side effect 분리.

**실패·복구:** 설정 파일 손상은 캠페인에 영향 없이 기본설정+알림. 시스템 back은 확인창 닫기→세계 접기→메뉴 순서 제안, 저장중 exit 유예. muted/lowmotion 모드가 타이밍·확률을 바꾸지 않음.

**완료 증거:** 작은 세로 화면·노치·긴 한국어·200%글자, 48dp 밀도환산 터치 영역, 무음/색약 판독, 터치/키보드 포커스, 배경/복귀. 접근성 자동검사와 장애 사용자 사용성을 별도로 기록.

**제외:** 번역 언어 확대·유료 음원 구입·운영체제 읽기 지원을 Godot Label 존재만으로 PASS.

## R10 — 저장·중단·중복 입력 통합 내구성

**현재 상태:** 기존 SaveService 원자 저장/개별 재시작 검증 있음. 신규 일반 의뢰·성장·시각 cursor를 포함한 전체 crash matrix는 미완료.

**선행 조건:** 각 R02~09 변경과 함께 적용. 마지막 한 번의 QA로 미루지 않는다.

**설계·흐름:** validate → 기존 revision 대조 → immutable command/snapshot → 저장/재읽기 → UI 성공 통지. 거래 중 뒤로가기·중복 터치는 command_id로 차단. PREPARED의 고정 난수와 결과 commit을 기존 actual-use service에서 재사용한다.

**데이터·구현:** SaveEnvelope의 known version/optional schema를 확장하되 기존 parser가 조용히 필드를 버리지 않게 fixture 검증. 신규 order/escrow/growth 각각 source_version, policy_id, transaction_id. migration은 복사본→검증→선택 슬롯, 원본 삭제 금지. UI/presentation은 저장 truth를 읽는다.

**실패·복구:** 저장전/쓰기중/commit후표시전/결과확정후재접속 cutpoint마다 이전 완전 상태 또는 다음 완전 상태 하나만. 부족 디스크·malformed·다른run_id·unknown policy는 실패 설명 및 원본보존. 무조건 새게임 생성 fallback 금지.

**완료 증거:** accept/craft/cancel/handoff/settle/dayclose/exchange/growth별 cutpoint×연타×재시작 표; 돈·재료 합계, 한UID 한소유자, 사건당 손상최대1, 지급최대1. IN_TRANSIT 중 마감 가능, 도래일 경계/중복 마감/다중 사건 동시 도래/재접속에서도 due결과1회, transient PREPARED와의 교착 없음. 실제 OS강제종료/모바일 background는 단위 테스트와 구분.

**제외:** 클라우드 저장·동시기기 병합·범용 event-sourcing 프레임워크 신설.

## R11 — 콘텐츠 변주·경제·재미 개선 루프

**현재 상태:** 기존 목적 조합·12세계 콘텐츠 기반과 시험 수치가 있다. 사람 플레이로 입증된 최종 경제/장기 재미는 아직 없다.

**선행 조건:** R02~04 완주, R08 읽을 수 있는 결과, R10 자산 보전. 모닥 장기 성장 시험은 R05 정책 별도.

**설계·흐름:** ‘왜 이 장비를 만드는가’가 다른 의뢰를 제공하되 매번 규칙 추가로 해결하지 않는다. 같은 위험에서도 태그 목적·반환·수리 사연을 달리한다. 복구용/일반제작/태그목적/고위험의4역할이 플레이를 잇게 배치. 태그 이름만 바꾼 동일 의뢰는 변주 완료로 세지 않는다.

**데이터·구현:** R02 catalog에 역할·고객대사·결과요약·chronicle template 연결. 초기 fixture 최소5종×일반1·목적1=10정의, 기존AQ/DU/AR 목적12개와 적합성 검사. 보상수치는 R04 profile만 소유. 로컬 QA telemetry는 총소요시간/강화시도/순자원/회복횟수/중단지점, 개인식별정보 없음. 일반성공 반복로그를 작품 연대기에 추가하지 않는다.

**실패·복구:** trialprofile 0.75/1.00/1.25 비용·보수 감도 비교하되 한 번에 하나만 변경. 결과보고서에는 RNGseed/초기자원/profile 함께 기록. 최고평균수익만 최적화하면 위험 선택이 사라지는지 확인한다. 새 밸런스는 신규 시험 슬롯 또는 명시적 migration으로만.

**완료 증거:** 자원0→복구, 기본→정밀→세계→수리→재투자 연속3순환, 선택촉매 막힘없음, 빈날/취소무한이득0. 사람 검수 질문: 다음 행동 이해, 태그 선택 이유, 멈춤/추가강화 고민, 모닥 애착, 반복 피로. 수치 PASS와 재미 승인은 별개.

**제외:** 새장르·직원수십명·경쟁랭킹·광고구제·미승인 엔딩/플레이기간을 필수완성 범위로 추가.

## R12 — Android·최종 자산·사용자 테스트 전달

**현재 상태:** 데스크톱 부분 증거는 있으나 Android/최종미술/사람/권리/출시 전체 PASS 아님.

**선행 조건:** R01~11의 승인 제품 범위가 연결되고 알려진 P1/P2 정리. `PLATFORM_RELEASE_AND_ASSET_RIGHTS_PROFILE`, `ASSET_RIGHTS_AND_PROVENANCE_RECORD`, `GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK` fresh-read.

**설계·흐름:** exact build/revision 표시 → 신규 슬롯/이어하기 → 핵심3순환 → 종료/복귀 → 문제 보고. 사용자 테스트 패키지와 스토어 출시 패키지를 별도로 판정한다. 로컬 설치형 빌드는 외부 배포 승인 대체 아님.

**데이터·구현:** export preset/engine pin/asset manifest/build hash 기록. portrait safe area, 화면밀도, pause/resume, 저장 경로, 소리/진동 확인. 목표 성능은 시험30fps 기본·60fps 선택을 제안하되 기준기기 명시 전 보장값으로 쓰지 않는다. 세계창 접힘/펼침 CPU/GPU/메모리 비교.

**실패·복구:** 앱중단·OS회수·낮은저장공간에서 R10 보전. 버전다운그레이드 보호 및 테스트 저장 export/복구 안내. 출처·사용허락 불명 asset은 출시 후보 제외하되 원본을 지우지 않는다.

**완료 증거:** 최소 저성능/일반 실제기기 기록, 화면 캡처·정확빌드·재현순서·오류목록, 최종 자산 권리/승인 목록, 사용자 플레이 피드백 반영, required CI/main readback. 스토어 정책/등급/법률 확인이 없으면 RELEASE_BLOCKED_UNVERIFIED 유지.

**제외:** 출시 승인 대행, 유료도구 자동구매, 테스트 성공을 공개배포 권한으로 해석.

## 4. 착수 가능한 부분과 남은 결정

즉시 기술 착수 가능: R01 남은 검증; R02/03 순수 schema·상태·중복차단 테스트; R06/07 consumer brief·기존 승인 자산 점검; R10 실패행렬. 실제 product authoring 전 exact경로/정본 Gate는 여전히 필요하다.

시험안으로 구현 가능: R04 분리된 경제 profile, R05 비교 계산기, R07 milestone 표, R11 테스트 콘텐츠. 이는 최종 게임값 확정이 아니다. 최종 성장을 발동하려면 달력/실작업 조건, 최종 경제라 부르려면 플레이 균형 검수, 새로운 자산 runtime 승격에는 외형 lock이 필요하다. 본 문서는 그 승인을 얻었다고 기록하지 않는다.

권장 폐기/정리: 중복 HTML PM 만들지 않음; 체크보드 RGB 후보는 runtime 사용 금지; routine 강화 로그의 연대기 확대 금지; old표를 새 경제에 fallback하지 않음. 기존 파일은 이번 작업에서 삭제/이동하지 않았다. unused consumer·hash·복구목록을 확인한 파일만 추후 사용자 삭제용 폴더로 옮긴다.

공용화 판단: transaction별 검증·기계/실행/사람 상태 분리는 기존 Base 규칙 재사용. 이번12개 게임 명세나 후보 밸런스는 Base에 승격하지 않는다. 실제 반복 실패와 재사용 소비처가 확인된 자동 검사만 후속 공용 후보로 기록한다.
