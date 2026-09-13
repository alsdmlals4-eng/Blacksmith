# 모루의 서약 통합 블루프린트 제작 계약

## Manual Day / Repeated Recovery Implementation Plan — BS-REPLAN-20260913-05

Current implementation evidence (2026-09-13): PR377 exact2-path implementation is locally verified, final CI/merge pending. GUT309/3088 PASS after missing-service/native-control RED, actual48px touch-size RED, and malformed chronology/time RED. Actual day1 cancel preserved save SHA56365d15…; confirm advanced only to day2, no resources changed. Restart restored fresh order; pointer forging created distinct UID BSI-3ae976b62ae264fe9889fcd45a5b8206; restart READY→pointer delivery→restart DELIVERED. Gold17070→17470, reinforcement22→24, flame63/earth64 unchanged; original shield UID/level10/3-of-5 durability retained. Slot selection and scroll visibility were QA assists; no gameplay state or RNG injection. Native dialog96 logical pixels verified after layout. PDF61/62 adds actual captures/checklist; prior60 pages preserved. Whole-game, Android, human, final economy/art/motion remain incomplete.

Round1 adversarial findings and learning: invalid current_day1.5/string/bool was truncated, and acceptance after birth/delivery was accepted. Both reproduced RED then strict integer/time-order validation added within the same approved service path. No save migration or schema expansion. AcceptDialog internal layout resets custom minimum size from theme constants (https://raw.githubusercontent.com/godotengine/godot/master/scene/gui/dialogs.cpp); use buttons_min_height/width, confirmed in current4.7.1 runtime and 2-frame geometry regression. Project-local lesson only, no unproven Base promotion. Exact approval checker correctly rejects an approval with no protected diff; ordinary gate used before changes, exact approved checker passed after both paths changed. Transient MCP reload43 was not counted as PASS; fresh game runs and full GUT passed without startup errors.

Direction / Goal: 첫 재기 주문에서 끊긴 제작·납품 순환을, 직접 마감→다음 주문→다시 제작·납품으로 연결한다. 전체게임 구현의 다음 단계이며 이 묶음만으로 전체완료를 선언하지 않는다.

Architecture: 기존 recovery service가 원자 저장/readback과 주문 기록을 계속 소유한다. 기존 공방 VBox에 마감 버튼과 native 확인창을 연결하고 app의 campaign_saved 신호를 재사용한다. 새 Scene/자산/툴/전역 manager 없이 기존 두 script만 수정한다. Tech: Godot4.7.1 / GUT9.7.1 / HiGodot3.2.0; Base v9.4.4·validator43b3 유지.

Spec / approval: Blueprint17/39/51, BLACKSMITH_MODAK_CALENDAR_REVIEW_20260912.json의 manual-close recommendation, 최신 사용자 ‘게임 전체 완성,구현까지 계속진행’ 및 routine 재승인 생략. 상세 수치는 시험값; 성장/세계보고 지연/출시 승인으로 확장하지 않는다. 현재 main eb3a47cb1d33f5f942786de42acfbe15b46db1d0, 보호baseline4976ae2ca9d1eae11a5fc8fc44f1f8e9c23a047d. PR196/359 고유 변경과 경로 중첩 없음·read-only. 기존 import/후보/저장 보존. HiGodot 연결된 checkout의 codex branch에서 순차 저작하며 프로젝트 복사본을 추가하지 않는다.

Before→After: DELIVERED에서 후속 없음→명시 마감 확인 뒤 하루만 증가·완료기록 보존·새 주문 가능. 무료 마감으로 자원/보상/난수/주문 종류 재굴림 없음. 미수락 또는 ACCEPTED/READY는 그대로 유지. PREPARED 세계시험 또는 알 수 없는 nonempty schedule_state는 마감 차단. 뒤늦은 동일 source_day 요청은 추가 진행하지 않는다. 오래된 저장을 자동변환하거나 삭제하지 않는다.

Preflight (2026-09-13): 현 service/SaveEnvelope/UI/app/GUT와 공식 Anvil Saga(https://store.steampowered.com/app/1587540/), Weapon Shop Fantasy(https://store.steampowered.com/app/599460/), My Time at Sandrock(https://store.steampowered.com/app/1084600/) 설명을 재조회했다. 주문→공방 활동→재료/보상 재투자 ADAPT. Godot Saving games(https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html)·ConfirmationDialog(https://docs.godotengine.org/en/stable/classes/class_confirmationdialog.html) 직렬화 및 확인/취소 경계 ADOPT. 직원경제·외부 수치·단순 날짜클릭 보상 REJECT. 직접 경쟁작 플레이나 균형 검증 증거 아님.

Alternatives: (1) 기존 권장 명시마감 REUSE—선택 속도 유지·저장 경계 명확, 빈날 넘김 성장 악용은 성장 구현 전 별도 검토. (2) 실시간 자동날짜 REJECT—휴식/접속시간이 의뢰를 바꿈. (3) 강화횟수 자동날짜 REJECT—강화 코어와 달력을 불필요하게 결합. Base reuse handoff/profile의 공용 저장·지연엔진은 구현완료가 아닌 패턴/계획이므로 새 의존성으로 채택하지 않고 현 save service 재사용. No Base promotion now.

State / interface: service.close_day(envelope, source_day, save)→{status:APPLIED|ALREADY_APPLIED|BLOCKED,envelope? ,reason?}. 같은 campaign·정수 source_day·현재 저장 일치·미처리 거래 없음 검사→원본복제→current_day+1→DELIVERED만 recovery_order_history에 보존하고 active 제거→원자 저장→readback. optional recovery_calendar={schema_version:1,policy_id:MANUAL_CLOSE_V1,last_closed_day:N}; current_day=N+1. history는 순서대로 완료된 기존8필드 기록이며 UID 유일·아이템/원장 보존. 새 ID는 run_id-recovery-(history.size+1); 기록 부재인 기존 슬롯은 그대로 유효. 초기 정책 의미는 고정 호환경계이며 새 정책은 별도 이관 없이는 추측하지 않는다.

Compact flow: 오늘마감 버튼→확인창(취소는 무변경)→현재 source_day/저장/거래 검사→날짜 저장(+1, 완료주문만 보충)→공방 날짜·누적 납품 갱신→주문 수락/제작. 미완성은 같은 UID·재료·상태로 다음 날 계속. 날짜만 넘긴 결과는 Chronicle 보상 사건이 아니다.

Risk / rollback: 대량 주문기록 비용·빈날 성장 악용·고정 재기주문 반복의 지루함은 후속 플레이 검토 대상. 임의 cap/가격 변경 없음. 잘못된 기록은 저장을 거절하고 원본 유지. 정상 revert 가능하지만 새 calendar/history 저장은 구버전에서 열지 않으며 QA 전용 슬롯에서 먼저 검증; 사용자 파일을 구형으로 덮어쓰지 않는다. 이미 저장된 world trial 난수/결과/UID는 불변이다.

Execution uses TDD and inline execution per current user continuation; plan/spec remain in this existing owner instead of another dashboard.

- [x] DAY-01 RED: 기존 GUT 파일에서 close_day 부재/빈날 보상0·중복마감·미완성보존·3회 실제파일 제작납품·위조history/calendar/저장실패/PREPARED 차단을 검증한다. 예: close_day(original,1,save) 뒤 day=2, 같은 source1 재호출은 ALREADY_APPLIED/day2.
- [x] DAY-01 GREEN: scripts/vertical_slice/services/vs_recovery_order_service.gd의 validate/accept 확장과 close_day/close_block_reason. SaveEnvelope 기존 validate consumer 재사용; 승인 exact2경로 PR label readback 뒤 HiGodot 저작.
- [x] DAY-02 RED→GREEN: scripts/vertical_slice/ui/vs_workshop_screen.gd에 DayClose/DayCloseConfirmation. 확인 때 포착한 source_day 사용, 미표시/구형/진행중이면 호출 차단. 공방 화면 hidden 중 직접 handler 호출도 거절. tests/gut/unit/vertical_slice/test_vs_replan_tag_save.gd에서 native 버튼 취소/확인·실패 재시도·app 저장갱신 검증.
- [ ] DAY-03: 전체 GUT·Python·계약검사, 실제포인터 마감/재시작/두 번째 제작납품/캡처. Blueprint 기존60쪽 보존 및 반복플레이 화면/체크리스트 추가. 두 차례 전체 적대검토→필요 수정→exact CI·정상병합·main readback. Android/사람/최종경제/성장/모션은 NOT_RUN.

Fresh-read reconciliation: PR376은 eb3a47cb로 병합되어 consumed PR375 승인 회수와 baseline 교정까지 완료됐다. 아래 ‘정합화 진행’, ‘최종 검토 진행’, 기존 미체크 목록은 PR375 작업 중의 역사기록이며 현재 미완료는 위 DAY 항목과 전체게임 후속 큐다.

## Recovery Order Implementation Plan — BS-REPLAN-20260913-04

최신 전달: PR375/fbfde8f2 두 차례 전체 검토 후 추가 P1/P2없음, exact11SUCCESS/1조건부SKIPPED를 확인하고4976ae2c 정상병합. 로컬main=origin/main readback. CI 초기 외부 TLS/import 실패는 동일 head 실패작업 재실행으로 통과했고 gate는 완화하지 않았다. Python 전체506PASS/3SKIP, PDF9PASS, GUT304/2973PASS. 납품 뒤 재시작·완료버튼 재클릭은 저장SHA56365d15 불변. 아래 진행중 기록은 이전 checkpoint이다.

승인 회수 교정: consumed5경로 manifest를 내용그대로 archive에 보존하고 baseline만4976ae2c로 정합화. RED3→일반 gate/파생뷰/역사승인 회귀로 검증한다. Base v9.4.4·validator·보호경로/기존 사용자 import와 후보는 불변. 신규 실행범위는 다음 작업의 fresh PR metadata+exact 승인으로 등록한다. 운영 정리 자체를 제품 기능 향상으로 세지 않는다.

현재 결과: PR375의 exact5보호경로에 첫 재기 주문 수락→전용 재료 단조→예약 UID→납품 정산을 연결했다. 기존 작품/선택 UID 보존. 실제 파일 왕복에서 JSON 정수/소수 동일값 비교, 실패 후 단조 결과 재시도 latch, 복귀 버튼/스크롤 겹침, 필수 campaign 키 누락의 debugger break를 각각 RED로 재현·교정했다. GUT304/2973 PASS. HiGodot patch의 fallback43은 검사 PASS로 세지 않고 전체 엔진 실행과 재시작으로 확인했다.

실제 QA: 기존 자연성장 슬롯에서 포인터 수락→망치질28회→마감→새 철검 저장→게임 재시작 READY→납품. Gold16670→17070/보강20→22, 불63/대지64와 기존 철방패+10/3·5·5 불변. 슬롯 선택과 스크롤 가시성만 보조했고 결과/재화/단계/RNG 주입 없음. 중간 QA eval의 잘못된 변수/컴파일 오류로 미저장 단조가 중단돼 저장된 ACCEPTED에서 재시작했다. 이는 최종 게임 오류 없음 주장과 구분한다. 실제 캡처/PDF59절 추가; 최종 독립검토·exact-head CI·병합/readback은 진행 중이다.

다음 안전 제품 순서: 이 첫 주문 checkpoint를 보호경로로 전달한 뒤 영업일/주문 보충→반복 주문/재제작·재료순환→활/방어구 실제 사용 사건→달력/모닥 성장→승인 자산과 동작 연결 순으로 구체화·구현·실행 검수한다. 첫 주문1건/자동 검사만으로 전체게임 완료를 선언하지 않는다.

Goal: Blueprint17/39/51의 첫 재기 주문을 실제 단조→납품→400골드/보강재2 정산으로 연결한다. Architecture: 기존 SaveEnvelope에 optional recovery_order 단일 기록, 전용 서비스가 원본 복제·현재 저장 일치·원자 저장/readback을 소유한다. 기존 단조 화면/출생 변환기를 재사용하고 원래 선택 작품은 변경하지 않는다. Tech: Godot4.7.1/GUT9.7.1/HiGodot3.2.0, Base v9.4.4 유지. 이 기존 production owner에 계획을 통합하며 별도 dashboard/spec를 증식하지 않는다. 최신 사용자 routine 재승인 생략 지시로 inline 실행한다.

범위: 현재 main c5a81189·baseline76ad0bb0, 다른PR196/359 read-only. optional 기록 부재는 구형/기존 새 캠페인과 호환되며 legacy에 기능 노출 금지. 수락은 자원0에서도 가능, 주문 전용 제작권1회만 부여한다. 새 단조 결과의 UID를 주문에 고정하고 처음부터 CUSTOMER_RECOVERY_RESERVED 소유로 두어 다른 사용/강화로 유출하지 않는다. 납품은 CUSTOMER_RECOVERY로 이전하고 원장/정산을1회 저장한다. UID/원장 보존, 실제 파일 삭제 없음. 첫 주문만; 다음 날 보충/달력·촉매교환·대여 보상·경제최종확정은 이번 묶음 제외.

비교(2026-09-13 공식 소개 재조회): Weapon Shop Fantasy(https://store.steampowered.com/app/599460/) 제작·재료순환 ADAPT, Anvil Saga(https://store.steampowered.com/app/1587540/) 주문/공방 맥락 ADAPT, My Time at Sandrock(https://store.steampowered.com/app/1084600/) 의뢰 제작의 명확한 납품 목표 ADAPT. 직원경제/경쟁작가격/무료 클릭보상 REJECT. Godot Saving games 및 FileAccess 공식 문서의 직렬화 경계를 ADOPT하되 기존 save_service 재사용. 공개 소개/문서 조사이며 직접 경쟁작 플레이나 시장 밸런스 증거 아님.

파일: 신규 scripts/vertical_slice/services/vs_recovery_order_service.gd와 UID; 기존 domain/vs_save_envelope.gd(기록검증), ui/vs_workshop_screen.gd(주문카드/행동), ui/vs_app.gd(단조화면 왕복). tests/gut/unit/vertical_slice/test_vs_replan_tag_save.gd에 실제저장/실패/중복/UI 회귀 추가. 보호 exact5경로·신규 currentPR metadata 등록 후 제품저작. 새 이미지/씬/외부도구 없음. 기존 실제 단조·공방 소비처와 승인배경 재사용.

- [ ] RED: 서비스 부재 실패, accept(envelope,save)→forge(envelope,completed_result,save)→deliver(envelope,save)의 실제파일 왕복; 금0→400/보강0→2, 원작품불변, 중복납품0, 새UID/원장/선택유지. 잘못된기록·legacy·stale·저장실패 반례.
- [ ] GREEN: 서비스 validate(envelope)→오류문자열, accept/forge/deliver→{status,envelope,reason}; 수락ACCEPTED/item_uid빈값, 제작READY/전용UID, 납품DELIVERED/고정정산. JSON 검증은 exact key/type/phase/소유/작품존재를 확인한다. 재접속은 파일의 동일상태만 재사용한다.
- [ ] UI RED→GREEN: native RecoveryOrder/Action 수락→단조 열기→완료저장→납품→완료표시. 단조 중 공방 숨김, 저장실패는 결과를 보존해 재시도, 취소는 수락상태로 복귀. 최초·완료·legacy·연결오류 구분, 터치/스크롤은 기존 규격 유지.
- [ ] 전체 GUT/운영계약/실제포인터 제작·납품·재실행/캡처, 두 검토·수정, PDF 체크리스트와 receipt, exact CI/정상병합/main readback. Android/사람/최종밸런스는 별도.

## 2026-09-13 세계 시험 병합 후 다음 구현

PR373/278caffc는10SUCCESS·1조건부SKIPPED 및 미해결 검토스레드0 확인 뒤 정상 병합76ad0bb0. 로컬main/origin/main 동일 readback. 소진8경로 승인은 world-trials-pr373-20260913.json에 보존하고 활성경로에서 회수한다. Base v9.4.4와 보호목록/CI pin은 그대로 두고 프로젝트 baseline만 검증된 병합점으로 교정한다. 회수 계약 RED→일반 gate·파생뷰·역사PR 보존 회귀 GREEN을 요구한다. BENCHMARK_NOT_APPLICABLE: 제품 의미 변경 없는 기존 승인회수 절차이며 현재 병합/공식 Base 생성기와 검증기를 기준으로 한다.

다음 제품 작업은 Blueprint17/39/51의 주문 수락→주문 귀속 제작→인계·1회 정산→재제작/재료순환이다. 현재 새 캠페인의 초깃값 재화와 보상NONE 시험을 상용 경제로 착각하지 않는다. 기존 UID·실제 저장/readback 소비처를 재사용하고 구형 슬롯/기존 시험기록을 자동변환하지 않는다. 첫 묶음은 재기 주문을 실제 완성품 소비·중복 정산 차단·재료 부족 복구에 연결하는 계획부터 시작한다. 수치400골드/보강2는 시험값이며 확정 밸런스가 아니다. 날짜/성장/보고지연을 함께 무리하게 열지 않고 현재 정본·consumer와 공식 사례를 다시 읽어 exact 구현범위를 등록한다.

## 2026-09-13 세계 시험 연결 실행 계획 — BS-REPLAN-20260913-03

최종 전체 검토2회 완료: 두 번째의 P2(재시작 첫 native 목적지 카드가 AQ 잔류)를 DU/AR 실제 CardBody RED2로 재현했다. 전체 refresh를 앞당기면 기존 AQ 잠금을 덮는 회귀가 생겨 폐기하고, family 복원 뒤 목적지 요약만 다시 계산하도록 최소 교정. 최종 전체 GUT300/2914 PASS. 저장·미술·경제 변경 없으며 exact-head CI/readback 후 정상 병합한다. 세 번째 전체 검토 대신 지적 항목의 회귀를 확인했다.

현재 결과: PR373의8경로 구현, domain RED3→GREEN299, native 선택 부재RED1→GREEN300. 실제 자연성장 QA슬롯(철방패+10격발I)의 결투 출발→재시작→같은draw(83.754556533594/19.398580297557)→패배/손상5→4, 군대draw31.9656994722513/34.1941383041844→성공/손상4→3, 이후 재시작3종기록 복원. 재화16670/보강20/불63/대지64 불변. 입력은 포인터와 native 선택창 키보드; 슬롯 선택/스크롤 가시성만 QA 보조, 단계/재화/난수 주입 없음. 실제 다음목적지의 수로 고정 누락RED를 교정했고, 군대위험은 앞선 손상 여부에 따라40/50%여서 UI회귀도 해당 상태를 반영하도록 교정했다. 최종 GUT300/2912 PASS. 독립 코드검토1회 P1/P2없음, 최종diff/CI/readback 진행 중. PDF58쪽에 실제 결과2장/체크리스트 추가, 후보미술·모션·Android/사람/출시 완료 아님.

승인 근거: 최신 사용자의 전체 게임 구현 계속 지시와 Blueprint21~24. 이 절은 현재 작업 계획/체크리스트 owner이며 기존 상세 기획을 대체하지 않는다. main aaea8dd1, 보호 baseline df48dd06, Base v9.4.4와 현재 Base 관측 d830c0f6 유지. 다른 열린 PR196/359는 read-only, 사용자 import/후보 원본 보존. 연결된 HiGodot 작업 경로를 유지하기 위해 현재 checkout의 새 codex branch에서 작업하고 별도 프로젝트 복사본은 만들지 않는다.

- 설계: 기존 AQ API/저장 bucket/15필드 유지. DU/AR는 각각 duel_trials/army_trials에 동일 15필드 계약을 적용하되 record_type·event_id·검증 profile을 가족별 고정한다. 가족별 UID당 1회, 모든 가족을 통틀어 UID당 PREPARED 최대1개. 준비 저장→독립2draw 확정→손상/반환→readback→읽기전용 보고. 기존 슬롯 자동 전환/삭제, 보상/날짜 변경 없음.
- 종류: AQ 철방패, DU 검/방패; AR 초기 엄호 시험도 검/방패로 한정한다. 활/갑옷/투구의 전선별 실제 사용 맥락은 별도 후속 연결이며 근접 시험에 억지로 넣지 않는다. 최저/권장10, LOW/MEDIUM/HIGH는 해당 시험 정의에만 묶인 임시값. 임무 성공식은 기존 section21과 같고 내구 손상률은 기존 resolver 소유다.
- 비교: Weapon Shop Fantasy의 제작→사용 순환, Anvil Saga의 주문·선택 맥락, Gladiator Guild Manager의 준비/관전 분리를 ADAPT. 실시간전투·군대관리·HP·사상자 생성·타 작품 경제수치 복제를 REJECT. 공식 Godot RNG와 Saving games의 상태/저장 경계를 ADOPT하되 현재 원자적 저장/readback 서비스를 재사용한다. 공개 공식 소개 조사이지 직접 경쟁작 플레이/시장 검증이 아니다.
- 출처(2026-09-13 재조회): https://store.steampowered.com/app/599460/Weapon_Shop_Fantasy/ ; https://store.steampowered.com/app/1587540/Anvil_Saga/ ; https://store.steampowered.com/app/1043260/Gladiator_Guild_Manager/ ; https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html ; https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html
- 구현 책임: vs_replan_tag_rules.gd(12요구/미리보기), vs_save_envelope.gd(가족별기록/중복예약검증), vs_customer_actual_use_action_service.gd(공통거래/보고), vs_enhancement_action_service.gd·vs_workshop_maintenance_service.gd(예약잠금), vs_workshop_screen.gd(가족선택/보고), vs_item_chronicle_screen.gd·vs_app.gd(3기록 읽기 연결). 신규 Scene/자산/Base pin 변경 없음. 별도 exact8경로 승인과 현재PR metadata 필요, 소진PR371승인 재사용 금지.

- [x] RED: GUT 실파일 저장에서 DU/AR 준비→재시작→확정/재열람, 성공·손상 독립4조합, 잘못된종류/roll/중복예약/손상profile 위조 거절, AQ 원본 유지.
- [x] GREEN: 위8파일을 HiGodot로 수정. 기존 AQ API optional family 기본값 AQ 유지; 다른 family는 명시값만 허용. prepared는 저장된 item snapshot과 일치해야 한다.
- [x] UI: 공방 family+요구 선택, 준비 후 선택잠금, 세계창·연대기에서 저장된 기록 읽기. 화면은 저장된 사건 보고, 모션없는 상태를 LIVE로 표시하지 않는다.
- [ ] 검증: 전체 GUT·운영계약·exact경로·CI, 실제 격리 슬롯의 포인터 결투/군대→재실행→보고 캡처; 저장 실패·stale 재시도·보상/자원불변 회귀.
- [ ] 문서/PDF 체크리스트·readback·정상보호병합. 전체게임/Android/사람재미/최종미술/출시 완료 아님. 이후 주문·재제작·재료순환 이어가기.

## 2026-09-13 구현 checkpoint 병합과 다음 순서

- PR371 exact head dc2c8bbc974d4ea1248361abe15bd0298d487632의16SUCCESS/1조건부SKIPPED 확인 후 정상 보호 병합. merge df48dd06bffa1df11287029d2c7f43815f84ad23, 로컬main/origin/main 동일 readback. 사용자 import 변경·구형작업tree·후보원본 보존, direct main/force/admin 우회 없음.
- 소진 승인은 `docs/archive/protected-approvals/replan-pr371-20260913.json`에 내용 그대로 보존한다. 활성 승인 경로에서 제거하고 프로젝트 보호 baseline만 실제 병합점으로 정합화한다. 채택 Base v9.4.4/release SHA/보호목록/CI validator pin은 불변. 기존PR366 기록은 역사상태로 그대로 유지하고 현재 승인회수 증거는 기존pixel-world receipt의 remote_delivery가 소유한다.
- closure RED: archive부재/병합receipt누락3반례. 기준정합화와 공식 생성기로 파생뷰를 다시 만든 뒤 일반검사(외부 승인 false·manifest없음)로 통과해야 다음 제품 경로를 연다. 이 운영 정리는 새 제품 변경 승인을 대신하지 않으며 다음 구현은 별도 exact 범위/현재PR metadata로 검증한다.
- 후속 CI에서 장기PR 검사 한 곳의 c31e550f 고정 기대값 잔류를 확인하고 로컬 동일 RED를 재현했다. 현재 baseline 기대값은 기존 병합receipt의 책임 필드로 일원화하되, PR366/PR371의 역사 exact merge/source·보존 승인·소진 baseline 재사용 거부 시험은 유지한다. 실패 검사 제외/약화와 Base 업그레이드는 하지 않는다.
- 다음 제품 계획: Blueprint21~24의 공통 판정에 결투DU01~04·군대AR01~04를 연결한다. 기존AQ1회/UID 기록·구형저장 불변을 우선하며 종류/요구/공개위험을 출발 전에 선택·고정한다. 새 사건은 먼저 준비 저장→동일결과 확정→보고/연대기·세계창을 함께 소비하게 한다. 모션이 없는 동안 텍스트 보고라고 표시한다. 이후 주문·재제작·재료순환과 달력/모닥을 연결한다.
- 최신공식3작품 Weapon Shop Fantasy/Anvil Saga/Gladiator Guild Manager를 다시 읽었다(2026-09-13). 제작→실사용, 주문/선택→결과, 준비→관전 역할분리를 ADAPT; 미술/경제수치 복제와 새 실시간 전투게임 추가는 REJECT. 기존 Blueprint URL과 적용범위를 유지한다. 이것은 공개 소개 조사이며 직접 경쟁작 플레이/시장 검증이 아니다.

## 2026-09-13 병합 전 전체 검토와 정리 경계

- 제품16경로 및 비제품 문서/후보상태/검증 변경을 main ff1c935d→44582e57 기준으로 독립 검토했다. 후보 외형 승인과 runtime 준비를 분리했고 Base v9.4.4·baseline·workflow 변경 없음. 제품 추가 P1/P2는 없었으나 정리 도구 목적지 junction 조상 검사 누락 P2를 확인했다.
- 수정 계획/결과: 원본과 격리 목적지의 존재하는 모든 조상을 볼륨 root까지 검사하고, 디렉터리 생성과 이동 직전 재검사한다. guard 부재 RED→모의 경로 3반례/정상 경로 및 호출 위치 GREEN. 독립 재검토 P1/P2 없음. 실제 파일 이동/삭제와 실제 junction 파일시험은 수행하지 않았다. 동시 외부 프로세스가 검사 뒤 경로를 바꾸는 적대적 환경의 완전한 원자적 방어를 주장하지 않는다.
- BENCHMARK_NOT_APPLICABLE: 이번 보강은 사용자 승인된 로컬 정리 도구의 기존 경로 안전 계약 회복이며 게임 디자인/경제 변화가 아니다. 최신 코드·검토 지적·로컬 PowerShell guard 실행을 근거로 한다. 자동 삭제나 범위 확대 없음. 공용 Base 코드 변경 없이 프로젝트 도구와 회귀시험에 교훈을 반영한다.
- 병합은 현재 구현 묶음의 저장소 통합일 뿐 전체 게임/최종 미술/기기/사람 재미/출시 완료가 아니다. exact-head CI 확인→보호 PR 정상 병합→main readback→소진 승인 보존·기준 정합성 회복 후 다음 게임 구현을 이어간다.

## 2026-09-13 선택형 세계창 연결 계획

- Blueprint24/49/I4의 접힘·상단 세계/하단 공방 분할·확대 관람을 기존 WorkshopScreen 안에 연결한다. 현 I3 consumer는 같은 UID의 저장된 AQ 사건 보고이며 실제 전투 모션/배경 후보를 승인 자산인 것처럼 사용하지 않는다. 읽기전용 보고 단계와 최종 관전 연출 준비도를 분리한다.
- 구조/영향: 기존16보호경로 유지. native 모드 버튼·보고 ScrollContainer; 접힘은 공방 우선, 분할은 상단보고/하단공방, 확대는 공방 입력 영역을 숨기고 복귀를 항상 표시. 모드는 화면 전용이며 저장필드/RNG/보상/날짜 변경0. 사건없음·준비중·결과·불량기록/legacy는 별도 상태로 표시한다. 실제 이미지 자산 추가 없음.
- 비교: 기존 Weapon Shop Fantasy/Anvil Saga 제작→사용 결과·Gladiator Guild Manager 준비와 관전의 역할 구분을 ADAPT, Godot 공식 ScrollContainer의 follow_focus/다음프레임 레이아웃을 ADOPT. 경쟁작 실시간전투를 복제하거나 저장기록을 실시간 생중계로 표기하는 것은 REJECT. 결정용 강화/수리 입력은 공방 모드에서만 가능하며, 확대 중 숨겨진 공방에 포인터가 통과하지 않게 한다.
- 증거 기준: 세 모드 전환과 화면 경계·복귀, 반복열람 저장호출0·envelope불변, legacy 숨김, 실제720논리/360물리 세로 캡처. 장비 장착 배우·전투 모션·Android/human은 이 보고창 구현만으로 PASS가 아니다.
- 결과: 모드 missing-method RED→GREEN, pending/result 갱신·legacy복귀·비중첩·재열람 저장0까지 GUT296/296·2687asserts PASS. 실제 AQ01 저장에서 포인터 접힘→분할→확대→접힘, FOCUS 공방숨김/복귀 표시 확인. 저장 SHA8a43067f7b3e6a68bb484059f7980d8e3b0314f92f699fe1aa266aed5629801d 불변. `replan-world-report-split-20260913.png`와 `replan-world-report-focus-20260913.png`는 실제촬영. 독립 검토 추가 P1/P2없음.
- PDF56쪽:55절 실제+0·확률표시 전후,56절 세계보고 분할/확대 촬영 추가. 페이지구분 누락은 절당1쪽 검사로 RED 재현 후 구분선을 추가하고 재렌더 육안 확인했다. 상세설계·아틀라스는 삭제하지 않고 이전 캡처의 확률표시 오류를53절에서 역사상태로 명시했다. 소스/PDF해시 기존receipt 갱신.
- 다음 경험 격차: 보고는 연결됐지만 배우/장비장착/전투모션은 미연결이다. 주문·재제작·재료순환·12사건·시간성장은 여전히 구현 큐다. 기존16경로 검사·보호PR readback을 거쳐 이어가며 현재 상품 출시나 최종미술 승인을 주장하지 않는다.

## 2026-09-13 화면 확률 정본 교정 계획

- 실제+10 결과 화면에서 다음+11이 성공82/실패유지13/실패손상5로 표시됨을 관측했다. Decision32 JSON `FINAL_PER_ATTEMPT_SUCCESS_FAILED_HOLD_FAILED_DAMAGE`와 충돌한다. 실제 resolver는 실패 뒤5%로 손상 판정하므로 화면 손상은18%×5%=0.9%, 유지는17.1%여야 한다.
- 책임 원본은 `BLACKSMITH_DAMAGE_PROBABILITY_CURVE_20260826.json` failure_resolution/UI 정책이며, 오래된 GUT의79/6.3/14.7 기대값도 동일 오해였다. 정본 수치를 바꾸지 않고 표시 기대값을79/1.3/19.7로 교정하는 RED를 먼저 관측한다.
- 범위: 기존 exact16경로의 EnhancementResolver 안에서 조건부 손상/시도당 손상을 명시 분리. 기존 `final_damage_percent`는 호환용 조건부 alias로 유지하고 신규 명시 필드를 제공한다. 실제 손상 branch는 조건부 확률을 계속 사용한다. 신규 저장필드·경제·Base잠금 변경 없음. 정상/경상/중상·회복보너스·확정보장 및 경계4%/5% 판정으로 화면만 바뀌는지 검증한다.
- 결과:3실패 RED→GUT295/295·2653asserts PASS. 정밀 직후3연결, 첫 제작 읽기/선택/스크롤, 표시 확률을 함께 회귀했다. 실제+0 철방패를 +10격발I까지 올린 같은 슬롯에서 AQ01 PREPARED→RESOLVED 확인: 성공 draw46.0290874408245, 손상 draw10.6037638021102, 성공/무손상, 보상없음·자원불변. 재실행 후 동일 기록과82.0/17.1/0.9 표시 확인. `docs/testing/replan-from-zero-correct-risk-20260913.png`가 교정 후 실제 캡처, `replan-from-zero-aqueduct-result-20260913.png`는 교정 전 손상5% 표시의 결함 증거다. PDF53의 기존 캡처 역시 이전 checkpoint로 현재 확률 표시 증거가 아니다.
- 독립 코드 검토: 첫제작/JSON 비교 교정 추가 P1/P2 없음; 경미한 첫 망치 뒤 '제작 준비' 잔류는 RED→'제작 중'으로 교정했다. 신규 시도당 확률은 현재 정본과 손계산/실제화면에 대조했으며 전체 게임·Android·사람 재미 PASS는 아니다.

## 2026-09-13 실제 첫 제작 막힘 교정 계획

- 실제 새 슬롯 포인터 시작 후 아무 망치질 없이 진행39.3%, 방패 선택 거절/기본 검 고정을 관측했다. `_process`가 첫 입력 전 session.advance를 호출하고 select_equipment는 세션 config에 선택을 전달하지 않았다. 기존 검사는 같은 프레임 선택만 검사해 실제 읽기 시간을 놓쳤다.
- 수정 범위: ForgingScreen1경로를 exact manifest에 추가(총16). 첫 망치질 전 idle은 선택 대기, 이후 기존 자동작업/마감 수치는 유지. 선택한5종 identity는 세션 config와 결과 명칭에 그대로 전달. 기존 세로 레이아웃에 native ScrollContainer를 넣어 작업/마감/확정에 도달 가능하게 한다. 신규 장면·자산·저장필드·게임 수치 없음.
- 조사: Godot 공식 Idle and Physics Processing(https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html)의 매프레임 자동호출 설명과 ScrollContainer 공식 책임 원본을 확인했다. ADOPT 명시적 사용자 시작 경계·follow_focus 세로 스크롤; REJECT 자동 진행 숫자0 조정으로 원인을 숨기기. 기존 제작 세션 단위 API의 자동진행 계약은 유지한다.
- RED: 읽기30초 자동진행/선택거부, 비검4종이 모두 검으로 완성, 스크롤 부재를 실제 GUT 실패로 관측. GREEN 기준은 동일 실패 제거 및 전체 회귀, 별도슬롯의 실제 방패 선택→제작→공방+0 연결이다. UI 동작 수정이며 최종 제작 재미/미술 교체의 증거는 아니다.
- 첫 실제 결과: 선택 대기0% 유지→실제 방패 선택→망치질27회→마감→공방+0, 실제 강화10회 모두 성공해+10격발I. UID BSI-0d9808a2520ef5e96a8beb2c4d4f0423, Gold20000→16670, 보강재30→20, 불의심장64→63. 단계/재화/판정 주입 없음. 화면 스크롤만 가시성 보조 API를 사용했고 버튼은 포인터 입력했다. 검사 eval의 잘못된 들여쓰기/존재하지 않는 멤버 조회로 디버거가 중단된 경우는 도구 실수로 분리해 수정·재시작했고 사용자 저장은 건드리지 않았다.
- 이어진 실제 결함: 정밀 생성 ledger payload는 int, JSON readback은 float여서 같은 값이 Dictionary 비교에서 불일치. 실제 typeof2→3, 내용 동일·JSON 비교 true 확인. AQ 출발/다음 강화/수리가 모두 `SAVE_DIVERGED`로 막힐 수 있다. SaveEnvelope의 저장 의미 비교 한 함수를3서비스 및 예약 snapshot/readback에 공유하고 schema/type 검증을 선행 유지한다. 명시적 run/phase/자원/변경값 차이는 계속 거절한다. 실제 정밀 저장→live envelope 유지→3후속 분기 RED→GREEN, GUT293/2610 PASS. 입력 숫자·bool·문자열 차이 보존도 추가 검사한다.

## 2026-09-13 PDF 구현 증거 동기화

- 기존 상세 설계와15개 상태 아틀라스를 보존하고52~54절을 추가해54쪽으로 갱신했다. 현재 구현 체크리스트, 실제 게임 캡처2장, 게임 전체 완성까지 남은 순서를 구분했다. 준비전용 승인 문구는02/36절에서 역사 상태로 명시했다.
- PDF52~54와 변경02/36 페이지를1300px로 렌더해 표·본문·캡션·여백을 검수했다. PDF8계약 PASS; source/PDF SHA-256는 기존 receipt에 갱신. 별도 HTML/추적표와 신규 그림은 만들지 않았다. 문서 캡처는 자연+0 플레이나 Android 증거가 아니다.
- 구현 checkpoint a447cfeb의 원격16SUCCESS/1조건부SKIPPED 확인. 독립 검토에서 main ff1c935d 대비 제품15경로의 추가 P1/P2 미발견; 정적 코드 검토이며 사람/기기 PASS와 별개다. PR371은 아직 미병합이며 최신 문서 HEAD는 별도 원격 readback 대상.
- 다음 계획: 신규 캠페인의 실제 첫 제작/+0에서 정밀+10·모험 대여/복귀까지 자연 입력 흐름을 점검하고 발견한 막힘을 교정한다. 그다음 저장된 사건을 읽기만 하는 접힘/분할/확대 세계창을 연결한다. 보상·확률·날짜를 열람 동작에서 변경하지 않는 것을 완료 기준으로 한다.

## 2026-09-13 다음 구현 — 모험 목적·대여 상태·결과 근거

- 문제: 저장은 연결됐지만 공방이 '성능/취급' 추상축과 성공/손상만 보여줬다. Blueprint22의 AQ01~04 작업 목적,25의 당시 장비/태그 기여,20의 대여/반환 설명을 실제 보고에 연결한다.
- 계획: 기존 ruleset에4요구의 읽기 전용 목적/결과 어휘 매핑, 실제 saved snapshot에서만 보고 생성, 공방·연대기 동일 보고 소비. 준비 중에는 측량대가 사용하며 편집 잠금, 결과 뒤에는 반환/파괴 상태를 구별한다. 법적 소유 PLAYER를 바꾸는 판매가 아니라 대여 예약이며 별도 보상/소유권 저장필드/추첨을 추가하지 않는다. 기존 trial1회/보상NONE는 유지.
- 조사 비교: Gladiator Guild Manager 공식1043260의 준비→전투 관전/결과 맥락은 ADAPT, Shop Titans 공식15.3.1 보상 공지 검색 결과의 퀘스트 장비 상태 복구 사례는 경계 검토에만 참고(원문 open timeout, 직접 플레이 아님). Godot ScrollContainer 공식 문서의 다음프레임 배치 뒤 ensure_control_visible·follow_focus는 ADOPT. 경쟁작 전투 숫자·미술 복제와 실제HP/실시간 전투를 가장한 표시는 REJECT. 기존 Weapon Shop Fantasy/Anvil Saga 비교를 함께 사용한다.
- 영향/기준: 기존15경로 안에서 read model/UI만 변경. 4임무ID/목적·성공/실패어휘, 저장된+레벨/태그/기여 일치, 현재 장비 변경으로 과거 결과 재해석 금지, 보고 반복 시 저장/난수0. 실제세로화면 확인 후 증거 갱신한다. 달력2일 지연/세계모션/12사건은 이 read-model의 완료 범위가 아니다.
- 긴 기록 처리: 보고 상세와 정밀10회 기록이 늘면 고정 연대기에서 복귀 버튼이 화면 밖으로 밀린다. 기존 node path를 유지하고 ChronicleMargin의 화면 여백 영역을 세로 ScrollContainer로 전환한다. body28·버튼96 유지,40개 기록 fixture에서도 복귀 버튼에 도달하는지 검증한다. 독립 HTML/새 추적표를 만들지 않는다.
- 결과: AQ01~04 ID·작업어휘와 saved snapshot 보고를 공방/연대기에 연결했다. 현재 장비를99로 바꿔도 당시+19·태그/기여가 보존되는 회귀, 반복 보고 저장0,40기록 스크롤 복귀 검사 RED→GREEN. 전체 debug GUT289/289·2577asserts PASS. 기존 실제AQ04 성공 기록을 다시 열어 +10균형I·60+3=63%·5→5·반환 표시를 확인했다. `docs/testing/replan-aqueduct-detailed-report-20260913.png`, `replan-aqueduct-readable-chronicle-20260913.png`가 실제 framebuffer이며 현재 플레이어 자산·판정값 변경 없이 읽었다.

## 2026-09-13 연속 구현 — 수로 모험 저장 트랜잭션

- 최신 사용자: '게임 전체 완성,구현까지 계속진행'. 같은 Blueprint 구현 범위의 일상 승인을 반복하지 않고 실제 소비처까지 연결한다. 새 핵심 규칙/위험한 마이그레이션/최종 미술 승인과는 구분한다.
- 구현 계획: 신규 캠페인 철방패 AQ 시험의 PREPARED→RESOLVED를 기존 저장 서비스로 두 번 확정한다. 준비 단계에서 UID·규칙·장비 snapshot·성공/손상 독립 추첨값을 저장한다. 복구 시 저장값만 사용하고 동일 사건을 재추첨하거나 중복 손상하지 않는다. 보상NONE·LOW 손상·시험 성공식은 기존 Blueprint 유지.
- exact 영향: CustomerActualUseActionService와 SaveEnvelope 두 경로 추가(총12). 새 사건을 구형 Nadia ContentResult로 위장하지 않고 별도 typed payload로 검증한다. 기존 장비/자원/세이브는 준비·결과 저장 성공 전 수정하지 않는다.
- 조사: Godot 공식 RandomNumberGenerator 문서(https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html)는 내부 알고리즘을 구현 세부사항으로 명시한다. seed만 재생하지 않고 실제 두 판정값을 저장하는 방식을 ADOPT. 앞 절의 Weapon Shop Fantasy/Anvil Saga 제작→모험 연결 ADAPT, 경쟁작 수치 복사 REJECT.
- 증거 기준: 성공/실패 × 손상/무손상 4조합의 실제 파일 저장/재접속, 반복 확정 무변화, 저장 실패·잘못된 입력·snapshot 변경 거부, 전체 GUT와 실제 UI 연결. 현재 missing-method RED 1개 관측; 이후 결과를 별도 기록한다.
- 화면 연결 계획: 기존 공방에 AQ 용도 선택/시험 출발/저장된 결과 확인을 native control로 연결한다. 대기 중 강화/수리는 잠그고 결과 뒤 같은 UID 상태로 복귀한다. App의 campaign 저장 신호와 기존 연대기의 별도 AQ read model 두 경로 추가(총14); 기존 Nadia 사건은 유지하되 신규 캠페인 화면에서 구형 인계와 혼동하지 않게 분리한다. 배경·이미지 신규 저작 없음.
- 구현/검증: 실제 SaveService의 네 조합 저장/복구, 저장 실패 무변화, 비정상 roll/schema/probability 차단, 오래된 화면의 재추첨 반례, 대기 장비의 저장 경계 예약 RED→GREEN. 전체 debug GUT283/283·2500asserts PASS. 준비 중 UI 강화/수리 차단과 결과/연대기 native consumer를 연결했고 구형 '인계 가능' 문구도 신규 캠페인에서 교정했다.
- 런타임: 별도 `user://gut/blacksmith_aqueduct_runtime_20260913.json`에 이전 QA +10 균형I 철방패를 복제했다. 실제 게임 포인터로 출발→프로세스 재시작→동일 저장 판정값2.916994289/89.300411046 확인→포인터 결과 확정. 예상63%에서 성공·손상없음, CURRENT5유지, App/파일 RESOLVED 일치. 연대기 수로 기록 확인. +0부터 자연 진행/Android/플레이 재미 검증은 NOT_RUN.
- 캡처: `docs/testing/replan-aqueduct-prepared-20260913.png`, `replan-aqueduct-result-20260913.png`, `replan-aqueduct-chronicle-20260913.png`는 실제 game framebuffer. 준비/결과 캡처의 구형 다음목적지 문구는 이후 코드로 교정했으므로 최종 미술 증거가 아니다. PDF51쪽은 이 구현 증거를 아직 포함하지 않는다.
- 다음 개선: 연대기 태그명 한국어와 모바일 글자/버튼 크기, 결과 후 실제 수리의 저장 연결, 신규 캠페인의 첫 제작부터 연속 플레이 자원 흐름 점검. UI/코드 조각 완료를 게임 전체 완료로 축소하지 않는다.
- 독립 리뷰 P1 두 건: 다른 run의 유효 저장본을 오래된 AQ 요청으로 덮어쓰는 경계, 메모리 전용 수리 뒤 AQ 준비 시 디스크 상태로 되돌아가는 경계. 모두 현 묶음에서 수정한다. 수리는 기존 WorkshopScreen·MaintenanceService의 판정을 후보 envelope/자원에 적용→기존 SaveService 성공→live 채택으로 연결하며 기존 비용·확률·scar 규칙은 변경하지 않는다. 저장 실패는 비용/내구도 모두 무변화. 보호 경로 추가 없이 기존 공방14경로 범위.
- 위 구현 배치 조정: 저장 트랜잭션을 비대해진 화면에 넣지 않고 기존 MaintenanceService가 소유하도록 exact 경로1개 추가(총15). 화면은 서비스 호출/성공본 채택만 한다. 같은 승인된 수리 구현 범위이며 수리 비용·확률·회복/흉터 정본은 불변.
- 후속 검증: 다른 run 덮어쓰기 RED→차단, 실제 수리 저장 실패/재시작/AQ snapshot RED→GREEN. 독립 재검토에서 사건만 바뀐 stale envelope의 수리 기록삭제 P1을 추가 발견했다. disk active_run 비교로 교정하고 같은 반례를 강화에도 확대해 RED→GREEN. 최종 로컬 debug GUT286/286·2533asserts PASS. 수리/강화가 PREPARED와 무손상 RESOLVED 사건을 모두 보존한다.
- 실제 수리: 별도 `user://gut/blacksmith_repair_aqueduct_runtime_20260913.json`에서 +10 철방패 CURRENT3 QA 사전조건을 저장한 후 native 포인터 수리. CURRENT3→4, Gold19170→19131, 보강재9→8, 수리 job 소진, live/파일 자원 일치 확인. 손상 사전조건은 시험 주입이며 자연 모험 손상으로 주장하지 않는다.
- 화면 후속: 공방 기존 mobile body28/title44/최소터치96 규격을 연대기에 적용하고 신규 태그 한국어 이름은 rule module의 한 사전으로 공방·연대기가 공유한다. RED 글자20/터치48→GREEN. 구형 태그 의미/저장 ID는 바꾸지 않는다.
- 최종 리뷰 교정: 오래된 backup readback이 RESOLVED 저장을 PREPARED로 되돌려도 APPLIED를 보고하던 P2를 RED로 재현했다. readback의 run_id·record 존재·전체 사건 내용 일치를 요구하고 미일치/키없음은 `AQUEDUCT_READBACK_FAILED`로 차단한다. 최종 전체 debug GUT287/287·2537asserts PASS, 관련 Python7 PASS, exact15경로 gate PASS. 실제 새 검증 없이 Android/UX/밸런스/출시 PASS로 승격하지 않는다.

## 2026-09-13 연속 개선 — 수로 모험 예상치 consumer

- 계획/범위: 기존 신규 태그 rule module과 공방의 4요구 비교를 확장한다. Blueprint21/22의 철방패·권장10·최저10·보상NONE 시험식을 그대로 소비한다. 실제 사건 확정/보상/손상/저장 변경은 이 묶음에 포함하지 않는다. 보호10경로·Basev9.4.4 유지, PR371 실제 승인 label 확인 후 exact gate 사용.
- 조사 비교: Weapon Shop Fantasy 공식 소개(https://store.steampowered.com/app/599460/Weapon_Shop_Fantasy/)의 제작/마법부여/모험 연계 ADAPT, Anvil Saga 공식 소개(https://store.steampowered.com/app/1587540/Anvil_Saga/)의 주문과 결정 영향 ADAPT, Shop Titans 공식1.0.12(https://playshoptitans.com/zh-tw/news/version-1-0-12-release-notes)의 장비 enchantment와 착용자 효과 연결 ADAPT. 공개 원문 조사이며 직접 플레이 증거 아님. 수치/미술/직원 확장 복제 REJECT.
- 대안: 점수만 유지(사용 가치 불명확), 구형 고객 결과에 새 규칙 강제 주입(서로 다른 사건 정본 혼합), 기존 시험 모험의 예상 성공률을 먼저 연결(채택). 실제 구형 ContentResult와 App의 Nadia 사건은 고정된 별도 결과축을 가지므로 다음 사건 구현 때 신규 snapshot/result contract를 명시해야 한다.
- 구현: `aqueduct_preview`는 단계 준비도·raw 태그점수·cap 적용 기여·최종 예상치를 분리한다. +10 기민I 취급순간63%, +11은63.5%, +100 해당 축 두태그IV는 raw16이나 실제15%p·최종95%. 잘못된 종류/단계/태그 누적을 거부한다. 공방에서 성공 후 상태를 입력하며 '수로 모험 시험 예상'으로만 표시한다. 태그 선택 전 미산출 비용의0Gold 표시는 '태그 선택 후 확인'으로 교정했다.
- 검증: 계산 missing-method RED→GREEN, native 버튼 예상치 누락 RED→GREEN, 미선택0Gold RED→GREEN. 전체 debug GUT279/279·2433asserts PASS. 실제360×640 게임에서 줄바꿈 확인; +9는 격리 저장을 메모리에만 복제한 QA 사전조건이며 파일 저장/실제 모험 판정은 하지 않았다. 에디터reload43 fallback은 headless/실행 검증과 구분한다.
- 현재 main ff1c935d, Base 원격d830c0f6, 타PR359/196 read-only 유지. 생성된 import 파일은 UNKNOWN_UNVERIFIED로 보존, 신규 자산/도구/의존성 없음. 동일 소비처에는 기존 코드/시험/승인 이미지를 재사용했다. 다음: 신규AQ snapshot/결과 저장 계약→실제 사용/연대기 연결. 예상치 구현은 세계 사건 전체 구현이나 Human/Android/출시 PASS가 아니다. PDF 미재출력.

## 2026-09-13 공방 선택·저장 재실행 검수 결과

- 아래 서비스 연결 시점의 UI 미완료 기록은 역사 상태다. 현재 새 캠페인 시작/첫 제작 schema2/공방 4태그 선택/기존 강화 저장 트랜잭션까지 구현했다. 실제 고객 요구 및 세계 결과의 신규 적합도 소비는 다음 미완료 작업이다.
- 격리 시험 저장 `user://gut/blacksmith_replan_ui_20260913.json`에서 철방패를 +9 사전조건으로 준비한 뒤 실제 포인터로 균형 선택→강화 실행→성공→재실행 readback을 확인했다. 동일 UID `BSI-8b31f6beb9886a97826d22865415c851`, +10, SUSTAIN_HANDLING I 유지; 대지의 결정2→1, 보강재10→9, Gold20000→19170. +0부터 자연 플레이한 결과나 밸런스 검증은 아니다. 사용자 저장은 사용하지 않았다.
- 실제 화면에서 발견한 작은 글자/성공 후 태그 누락/영문 결과 문구/방패 아래 검 손상 그림을 교정했다. 신규 버튼 글자28, 높이112(720 논리 폭 기준); 장비별 승인 손상 이미지가 없는 비검 장비는 올바른 정체성 이미지와 숫자 상태를 유지한다. 신규 아트 제작/승격은 하지 않았다.
- 교정 전 캡처: `docs/testing/replan-restored-tag-20260913.png`. 교정 후 실제 framebuffer: `docs/testing/replan-restored-shield-tag-final-20260913.png`. 저장된 원본은180×320이며 MCP 게임 창 캡처360×640과 구분한다. 시안/가짜 화면이 아니다.
- 추가 반례: 구형 이어하기 후 새 게임 시작이 이전 서비스에 저장할 수 있었다. 새 캠페인 서비스 복원 계약 RED1→GREEN으로 교정하여 이전 슬롯 쓰기0회 보장. 전체 debug GUT278/278·2414asserts PASS. HiGodot의 기존 class_name reload43 fallback과 중간 패치의 미정의 함수 진단은 최종 실파일 headless 통과와 별도로 기록한다.
- 다음 순서: 실제 고객 요구/동일UID 사건의 신규 태그 적합도 소비 명세→RED→기존 사건/연대기 연결→실행 검수. 강화 전 미선택 비용 표시와 최초 시작 UX도 함께 검토한다. PDF51쪽은 이번 증거를 아직 재출력하지 않았으며 Android/사람 UX/출시 검증은 NOT_RUN이다.

## 2026-09-13 연속 구현 — 캠페인·공방 진입

- 최신 사용자가 반복 승인 없이 남은 기획 연결/구현/개선 루프를 계속하도록 명시 지시. 계획은 새 슬롯 시작→첫 제작 규칙→공방 native 선택→실제 실행 검수→고객 사건 후속. 원본 저장 자동변환과 후보 아트 승격은 제외한다.
- 보호 exact 범위: 기존6파일에 RunInitializer, ItemBirthService, MainMenu, WorkshopScreen의4파일만 추가. 기존 approved marker 및 Basev9.4.4/기준 SHA 유지. 신규 장면·이미지·자원 수치 변경 없음.
- 새 메인 메뉴 저장은 `user://blacksmith_replan_20260912.json`; 기존v5파일과 별도이며 legacy fallback 없음. 첫 제작은 명시된 active_run.tag_ruleset_id에만 schema2를 생성, 없는 구형 캠페인은 schema1 유지, 알 수 없는 규칙은 차단한다.
- 공방 native4태그 버튼과 용도4종 비교를 연결했다. 실제 고객 요구 미연결 상태에서 고객 이름에 임의 요구를 붙이지 않고 용도 비교로 표시한다. 96px 버튼·재고·성장 전후·재료 부족·선택 표시. 구형 촉매 계보 UI는 새 규칙에서 숨긴다. 기존 강화 버튼이 같은 저장 서비스로 실행한다.
- 조사: Anvil Saga/Weapon Shop Fantasy 공식 소개의 제작과 사용 동기 연결 ADAPT, Shop Titans 공식 enchantment의 이름 있는 재료 표현 ADAPT. 효과 비교→실행 분리 및 별도 저장 슬롯은 우리 구현 판단. 타작품 수치/미술/직원관리 복제 REJECT. 자동 테스트276/2399 PASS, 실제 화면 검수 진행 중이며 완료는 후속 증거로 기록한다.

## 2026-09-13 고객 선택·실제 강화 트랜잭션 연결 후속

- 사용자 `그래 진행해`로 이전 권장안의 연속 실행. 계획: 고객 적합도 비교 모델 RED→GREEN → 기존 강화 resolver의 명시적 ruleset 분기 → 기존 비용/저장 서비스 재사용 → 성공·실패·저장 실패·5종 자격·중복 성공 재시도 검증. 신규 화면이나 별도 게임을 만들지 않는다.
- 조사: 아래 Weapon Shop Fantasy/Anvil Saga/Shop Titans 공식 페이지를 다시 확인. 제작 선택과 실제 용도 연결은 ADAPT, 독립 이름의 촉매는 ADAPT, 인력/건물 확장·타작품 수치 복제는 REJECT. 재료 부족 선택지도 성공했을 때의 효과를 비교하되 실행 권한과 분리하는 것은 우리 UX 설계 판단이며 타작품의 실측 UI라고 주장하지 않는다.
- 구현: `customer_choices`가 현재 적합도·4태그 선택의 성공 시 적합도/증분·촉매 요구/재고·차단 이유를 반환한다. 부족한 촉매는 비교만 허용; IV·4번째 태그는 불가능한 성장 수치를 제시하지 않는다. 실제 UI 연결은 아직 미완료.
- 실제 consumer 연결: 기존 EnhancementResolver가 새 저장의 ruleset을 명시 판별하고 신규 precision adapter를 사용한다. 성공만 태그/이정표 성장, 기존 ActionService가 성공/판정 실패 모두 촉매1개와 기존 비용을 저장 후보에 적용한다. 저장 성공 이후에만 live 자원을 공개한다. 구형 schema1과 기존 강화/손상 확률은 유지한다. 새 태그는 기존 role_stat/weight에 구형 효과를 더하지 않는다.
- 자원 이름 드리프트 해결: 새 규칙의 의미 ID `fire_heart`는 실제 자원 consumer의 기존 `heart_of_flame`에 명시 매핑한다. 둘 다 불의 심장이며 새 재고통·무료 재고·사용자 save 변환을 만들지 않는다. `earth_crystal`은 동일. 고객 비교 모델에 재고를 전달할 UI도 이 매핑을 지켜야 한다.
- exact 보호 범위는 기존4경로 + `vs_enhancement_resolver.gd` + `vs_enhancement_action_service.gd`의6경로. 새 성공 연대기의 근거는 BS-REPLAN-20260913-02로 기록하고 과거 Decision40으로 오인시키지 않는다. 일반 보호 계약·Basev9.4.4·기준 SHA는 변경하지 않는다.
- 검증 중 테스트가 원장 키를 `decision_id`로 잘못 가정해 debugger 중단. 실제 `source_decision_id`를 읽고 시험 수정; 해당 headless PID28472/30036만 종료. 제품 세이브·다른 편집기는 건드리지 않았다. HiGodot은 이 작업의 기존 class_name 스크립트에 fallback reload43을 보고하므로 실제 플레이 증거와 구분한다.
- 남은 범위: 새 캠페인의 명시적 ruleset 시작, 고객 요구/태그 선택 UI, 동일UID 세계 사용 적합도, 실제 실행 캡처. 현재는 서비스까지 연결된 자동 시험 단계이며 사용자가 공방에서 이 새 선택을 누를 수 있다는 뜻은 아니다. PDF51쪽·이미지 불변.
- 완료 증거: 선택 비교 RED3→GREEN9/399, 신규 트랜잭션 RED2→GREEN 및 추가 경계 검증10/65. 전체 debug GUT273/273·2380asserts PASS, 관련 Python14 PASS,6경로 approval gate PASS. 트랜잭션 시험은 실제 도메인/자원/서비스와 JSON readback을 사용하되 저장 성공·실패 반환은 시험 대역이다. 실제 파일 I/O는 이전 SaveService 시험으로 별도 커버되며 이 조합의 사용자 플레이/Android 검증은 NOT_RUN. 최신 Base 원격d830c0f6·프로젝트 main ff1c935d·타PR359/196 읽기전용 확인; adoptedv9.4.4 유지.

## 제품 완성 개선 루프 / BS-REPLAN-20260913-02

- 최신 사용자 정의: 루프는 기술검사 반복이 아니라 유사 강화게임 조사→기획 구체화/시스템 연결→실제 구현→플레이 검토→개선이다. 테스트는 안전성 증거이지 제품 완성의 대체물이 아니다. 각 묶음은 플레이어에게 생기는 선택과 전후 경험을 먼저 정한다.
- 이번 질문: 고객의 용도에 맞춰 태그를 선택한 작품이 저장 후에도 같은 정체성으로 세계 결과와 연대기에 연결되는가?
- ADAPT: Weapon Shop Fantasy 공식 소개의 제작/마법부여→모험→재료 순환(https://store.steampowered.com/app/599460/Weapon_Shop_Fantasy/). Anvil Saga 공식 소개의 주문·결정과 이야기 연결(https://store.steampowered.com/app/1587540/Anvil_Saga/). Shop Titans 공식 Ember Element의 독립 enchantment 아이템 표현(https://playshoptitans.com/en/blueprints/enchantments/z/ember). 직원관리/방확장/수치·미술 복제는 REJECT. 공식 공개자료 조사이며 직접 플레이했다는 주장은 하지 않는다.
- 연결 설계: 현/예정 고객의 용도와 태그 전후 기여를 보여주기→불의 심장/대지의 결정 소비→같은 UID 인계→실사용 결과/흉터→연대기. 확률과 손상은 기존 독립축을 유지한다. 구체적인 실제 소비처 연결 전 임시 태그 화면이나 독립 게임을 추가하지 않는다.
- 첫 구현 계획: 기존 item schema4 내부 `catalyst_affix`에 별도 schema2(`ruleset_id`, `tags`)를 허용한다. schema1은 그대로 읽고 쓰며 자동변환하지 않는다. 구버전 reader는 이미 알 수 없는 catalyst schema를 차단하므로 기존 item/envelope 전체 버전을 불필요하게 올리지 않는다. 구형 precision resolver는 schema2에 효과를 적용하지 못하게 명시 차단한다.
- exact 변경: `vs_replan_tag_rules.gd` 검증, `vs_item.gd` 직렬화 소비, `vs_precision_resolver.gd` 경계, 관련 GUT. 최신 사용자의 저장 연결 권장안 실행 승인에 따라 보호 manifest는 이 네 경로(기존 UID 포함)만 기록한다. BS-OPS-20260913-01의 과거2파일 복구 범위를 소급 확대하는 것이 아닌 별도 승인 범위다.
- 완료 기준: 실제 Envelope→JSON→Envelope 왕복, schema1 불변, 알 수 없는 규칙/혼합ID/소수·bool단계/단계와 이정표 불일치 차단. 소비·선택 UI는 후속이며 이 단계만으로 플레이 루프 완성이라고 표시하지 않는다. 사용자 save 파일 변경 없음.
- 구현 결과: Item/Envelope JSON 왕복 및 기존 SaveService의 시험 파일 쓰기/읽기에 schema2가 보존된다. 잘못된 태그 저장은 임시파일 검증에서 거절되고 기존 정상 primary는 유지된다. 구형 resolver는 새 규칙에 명시 차단. mixed schema1/2·소수단계·중복/소수/bool이정표·알 수 없는ID를 차단. 소수 강화 단계19.5가19로 잘려 허용되는 반례도 RED→GREEN으로 교정했다.
- 검증: 첫 저장/guard RED2, 단계 소수 반례 RED1 → 전체 debug GUT267/267·2310asserts PASS, Python14 PASS, 정확한4파일 approval gate PASS. 전체 회귀 중 문자열 schema 비교가 debugger 중단을 일으켜 소유한 headless 시험20332/27428만 종료하고 타입 확인 후 비교하도록 수정; 재실행 정상종료. 실제 편집기 파일 수정 도구는 기존 class_name 파일에 fallback reload43을 보고하므로 라이브 편집기 검증 완료라고 주장하지 않는다. headless 실파일 파싱/시험은 통과했다. 사용자 게임 save·이미지 불변.
- 다음 플레이 묶음: 고객 요구→현재/선택후 태그 적합도→필요 촉매/보유량→강화 결과→저장된 동일UID 고객사용. 저장 경계만 완성한 현재 상태와 UI/소비/세계 결과 미연결을 구분한다.

## 2026-09-13 연속 교정 루프 / 저장 연결 준비

- 계획 우선: 원격 실패 재현 → 원인별 최소 수정 → 전체 debug GUT/관련 Python → 원격 exact-head 재검사 → 다음 저장 경계 작업. 검사 약화·새 게임 수치·구형 저장 변경은 제외한다.
- 발견1: 원격 GUT는 `-d`를 사용하지만 이전 로컬 실행은 생략했다. 신규 규칙의 정수 나눗셈 경고가 첫 시험에서 실패했다. 같은 명령으로 RED 재현 후 HiGodot `blacksmith@c857`/editor2352에서 명시적 `floori(float(level) / 10.0)`로 수정; 경고 억제나 GUT 오류 추적 비활성화는 하지 않았다.
- 발견2: 과거 승인 소진 시험이 재사용 가능한 승인 파일 경로의 영구 부재를 요구했다. c31e550f에 담겼던 소비된 승인 baseline1686f8f...의 재등장과 현 adapter 기준 불일치를 차단하도록 교정. 과거 병합 receipt와 호환 뷰 hash 검증 유지. 새 manifest 승인 유효성은 별도의 기존 Base gate가 계속 소유한다.
- 발견3: 전체 GUT에서 화면 임시 인스턴스12개가 남았다. 테스트가 생성한 미등록 main-menu 비교 인스턴스와 workshop 인스턴스를 `autofree`로 등록했다. 제품 화면 코드는 변경하지 않았다.
- 증거: 두 CI 실패 로컬 RED 재현 → 관련 Python14 PASS → debug GUT259/259,2285asserts PASS → 임시 객체 정리 후 같은259/2285 PASS 및 이번 출력의 orphan/종료 resource leak 경고 없음. 원격 CI는 PR exact-head 결과가 별도 책임 원본이다.
- 조사: Godot 공식 warning system과 GUT CLI 공식 예시의 debug 옵션을 확인. 웹 GUT 페이지는9.6.1 표기여서 실제9.7.1 vendor 및 현 CI 명령으로 호환 확인. https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/warning_system.html ; https://gut.readthedocs.io/en/latest/Command-Line.html . ADOPT: CI와 동일 debug 실행. REJECT: warning 무시/테스트 실패 추적 끄기.

### 다음 저장·비용 연결 계획 (미구현)

1. `vs_item.gd`의 현 item-schema4/catalyst-schema1과 `vs_save_envelope.gd` schema5를 기준으로 새 ruleset 식별/태그 저장 계약을 명세한다. 구형 TAG_*를 새 네 태그로 자동 치환하지 않는다. 구형 저장 보존 및 새 규칙의 명시적 선택 경계를 먼저 시험한다.
2. 현 `vs_enhancement_action_service.gd`의 copy→preview→candidate cost→save→live adopt 구조와 `vs_save_service.gd`의 temp 검증/backup/promote 복구를 재사용한다. 독립된 임시 게임·저장 시스템을 추가하지 않는다.
3. 필요한 실제 변경 파일과 보호 승인 목록을 대조한 뒤 RED 작성: save round-trip, 불명 ruleset 차단, 실패시 비용1회·태그불변, 저장실패 비용0·원본불변, 빈 선택/재료부족0회, 동일 확정 요청의 중복 반영 방지.
4. 위 경계가 통과하면 공방 선택 UI와 결과를 연결하고 격리된 시험 저장으로 +9→+10/실패/재접속을 확인한다. 현재 사용자 save 파일을 실험에 사용하지 않는다. UI·모션·이미지 상태는 실제 캡처 전 NOT_RUN 유지.

## 2026-09-13 보호 경로 복구 계획 — BS-OPS-20260913-01

- 사용자 승인: 이번 불일치에 한해 실패 후 읽기 전용 조사와 승인 범위의 검증 계약 교정을 허용. 일반적인 실패 시 중단 규칙을 삭제하거나 확대하지 않는다.
- 원인: 일반 검사만 실행했고, 이미 main CI가 채택한 `check_approved_project_operating_contract.py`와 외부 승인 표시를 사용하지 않았다. 아래 09-12의 일반 검사 PASS는 신규 규칙 파일 추가 전 기록이며 현재 상태를 뜻하지 않는다.
- 계획: 누락 승인 manifest RED → 기존 `docs/operations/PROJECT_PROTECTED_CHANGE_APPROVAL.json` 표준 경로에 정확한 2파일 등록 → 외부 PR 승인 표시 대조 → CI-pinned 검사 및 미승인 추가 파일/누락/승인 없음/기준 불일치/다른 오류 보존 시험 → 상태 갱신.
- 책임 원본: 승인 경로/기준은 위 JSON, 승인 근거와 작업계획은 이 절. BS-OPS-20260913-01은 신규 규칙 모듈과 UID에만 적용한다. UI/저장 연결 파일을 자동 허용하지 않는다.
- ADOPT: Base DEC-BASE-20260806-002의 exact approval gate와 main workflow의 검증기 pin `43b3ffb2c5b026e3d4a38dab2338585894d36f61`. GitHub 공식 label/event 문서와 실제 workflow를 대조했다. REJECT: protected_paths 제거, 기준 SHA 이동, self-attested approval만으로 통과, Base 버전 교체.
- 외부 근거: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request ; https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels . 게임 벤치마킹은 이번 승인 기록 복구에는 무관하며 새로운 게임 규칙을 추가하지 않는다.
- 구현 재개 전 순서: 승인 검사 통과 → 현재 작업 경로 fresh-read → I1 저장 분리 및 I2 원자적 비용/저장의 별도 세부계획. 파일 등록과 단위 시험은 플레이 가능 완성을 의미하지 않는다.
- 복구 증거: manifest 누락 회귀 RED 1건 관측 후 GREEN. CI pin checkout에서 승인 gate PASS, PR371 `approved-protected-change` 실제 readback 확인. 승인/문서 회귀 11 tests PASS; 신규 태그 GUT 6 tests / 376 asserts PASS (Godot4.7.1/GUT9.7.1). 태그 모듈은 계산/미리보기만 구현됐으며 촉매 실소비·저장·화면 연결은 미완료. 전체 GUT/실제 플레이/Android/UX는 이번 범위 NOT_RUN. 원격 CI 결과는 exact-head PR metadata로 별도 확인한다.
- 재사용 교훈: 일반 보호 오류를 보고 baseline을 이동하거나 승인 질문을 반복하기 전에, main workflow의 기존 승인 검사 및 실제 metadata를 확인한다. 이 복구는 기존 Base 기능 재사용이므로 공용 Base 코드 변경은 필요 없다. 이번 예외 외 오류는 계속 중단한다.

## 2026-09-12 구현·개선 연속작업 승인

최신 사용자 지시: Base를 fresh-read하고 조사·벤치마킹·개선·구현 루프를 별도 반복 승인 없이 계속 진행. `REPLAN_IMPLEMENTATION_AND_IMPROVEMENT_AUTHORIZED`. 아래 준비전용/최종 승인 전 구현금지는 이번 범위에서 역사 상태다. 새 비용·삭제·정본 파괴·보호 도구 우회는 승인으로 추정하지 않는다. 상세 시험값은 플레이 검증으로 교정하며 개별 후보를 사용자 승인했다고 표시하지 않는다.

- 현재 main ff1c935d, 작업 PR371/head3f4ecca9 직접 후속; 타PR359/196 read-only.
- Base current d830c0f6967678eed3c208ac6b24f9cd1b262ec3의 승인→사용자 시험가능 전달·연속작업 지침 적용; adoptedv9.4.4 변경 없음. 로컬 operating contract PASS.
- 구현 큐: I1 신규 네 태그 ruleset/5종 자격/구형 저장 분리 → I2 정밀강화 선택·원자적 비용/저장 → I3 고객 사건 적합도/결과 → I4 선택형 세계창 → I5 하루/주문·모닥 성장 → I6 자산·모션 연결 → I7 실제 플레이·Android·PDF 증거 갱신.
- 첫 점검: 현행 장비 catalog는 갑옷/투구 제외, resolver는 구형 촉매 효과를 소비한다. 자격 boolean만 바꾸면 새 기획과 다른 효과가 방어구에 적용될 수 있다. 따라서 새 ruleset의 순수 판정과 경계 시험부터 만든 뒤 UI/저장과 연결한다. 구형 저장에 신규 ID 자동 치환 금지.
- 대안: 기존 catalog 일괄치환(REJECT: 구형 save/effect 오염), UI만 임시 개방(REJECT: 판정 불일치), 신규 ruleset 경계부터 연결(ADOPT: 독립 검증 후 전환). I1 분리 모듈은 통합 완료 전 플레이 가능 완성이라고 보고하지 않는다.
- 조사: Weapon Shop Fantasy 공식 Steam599460의 제작/마법부여/모험 순환은 ADAPT, Anvil Saga1587540의 주문-세계 결과는 ADAPT, Gladiator Guild Manager1043260의 장비 준비-관전은 ADAPT. 직원급여/방확장/새 전투조작 복제는 REJECT. 공식 소개 desk research이며 실제 플레이나 비공개 구현을 조사했다고 주장하지 않는다. Godot Scene organization과 GUT command-line 책임 분리를 ADOPT.
- 검증: 각 작업 RED→GREEN, 두 차례 범위 검토/회귀, exact-head 보호 감사·CI·실제 Godot. 세이브·이미지·UX·출시 증거는 독립 상태. 이미지 품질 교정은 미완료로 큐 유지.

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

### BP12-SHIELD-STATES / 2026-09-12

- 재개 교정02: 이미지 모델의 배경 전용 편집으로 `shield-states-02.png` RGBA/1536×1024, 완전 투명827,038픽셀 확보. 다만 완전 불투명0픽셀, 반투명745,826픽셀로 방패 내부도 alpha253 수준이고 주변 잔여 halo·셀 경계 침범이 있다. `alpha_status=PASS`는 실제 투명 픽셀 존재만 뜻하며 clean-cutout/ASSET_READY는 아니다. 제한된 Aseprite MCP에서1프레임·1레이어 native 후보와 PNG 왕복의 decoded RGBA 동일을 확인했다. 6칸은 상태 비교 이미지이지6프레임 모션이 아니다. source01은 불변, 후속은 불투명 내부/가장자리 정리와128px 정렬·판독 검사. 최종 외형/제품 승격 미승인, PDF51쪽·게임 불변.
- 이번 조사·비교: Aseprite 공식 Color Mode/Sprite Sheet 문서의 실제 알파와 offset/cell 규격을 ADOPT. 이미지 모델 배경 전용 편집은 ADAPT(형태 유지 및 파일 측정 필수). RGB에 불투명 alpha를 붙이는 가짜 교정·임의 배경제거 코드·미지원 Aseprite CLI 우회는 REJECT. Base 최신 원격 관찰 `d830c0f6967678eed3c208ac6b24f9cd1b262ec3`은 참고이며 채택v9.4.4와 기존 보호 경계를 바꾸지 않는다. 전체 기획 최종 승인은 여전히 대기다.

- 검수 결과: `candidates/shield-states-20260912/record.json`에 6상태 후보·원본 hash·생성 전문·검수 기록. 기본→마감→각인I→II→균열→수리 흔적은 구분되지만 RGB 바둑판이 구워져 alpha gate FAIL. 원본 후보와 판 분할도 달라졌고 셀별 정합·128px 판독은 미검증. 외형 비교 후보로만 보존하며 ASSET_READY/사용자 승인/runtime 적용은 아니다. 51쪽 PDF는 이번 후보를 포함하지 않은 기존 검증본 그대로다. 후속은 실제 투명 배경 재생성과 동일 피벗·실루엣 정렬, 이후 Aseprite 패키징이다.

- consumer_id: BP12-SHIELD-STATES; consumer_surface: workshop item display / inventory / chronicle / planned world equipped shield; runtime_asset_role: same iron_shield appearance states; primary_use: PLANNED_GAME_SURFACE.
- implementation_owner_or_path: `scripts/vertical_slice/ui/vs_workshop_screen.gd`의 장비 표현 후속, 세계 장착은 planned consumer. 현재 runtime에 자동 연결하지 않는다.
- target_aspect_resolution: 3열2행,1536×1024 요청,512셀 생성 소스→선택 후128셀 pixel-grid 검수. 한 asset family 상태 시트이며 설명용 글자·화살표·가짜 UI 없음.
- state_family_requirement: plain base / enhanced finish / 기민I single flowing groove / 기민II paired groove / damaged 기민II / repaired scar 기민II. 강화는 마감만, 태그는각인만, 손상·수리 흔적은 같은 위치에서 연속. 등급별 외형 변경 금지. 동일 원형·구리테두리·중심돌기·리벳·카메라·스케일 유지.
- source: `candidates/blueprint-20260911/items.png` 상단중앙 iron_shield 후보. 다른8종은 이번 대상 아님. 기존 후보는 불변. 모델은 기존 픽셀 계열을 유지하며 모닥의 비픽셀 예외를 장비로 확대하지 않는다.
- fallback_if_unconsumed: generated candidate로 보존; 기존51쪽 도식/원본 유지. 실제 알파·셀 정렬·128px판독·각인 위치·runtime은 별도 확인. native 원본 패키징은 파일검수 후, 사용자 외형 승인 전 정본 승격 금지.

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

#### Current Modak amendment: humanoid weakened fire spirit

**최신 사용자 확정 — 두 외형 승인 및 연차 성장 방향:** `modak-human-02-younger.png`는 초기 어린 모습(EARLY), `modak-human-01.png`는 이후 자란 모습(LATER)으로 두 외형 모두 승인했다. 게임 속 연차가 흐르며 모닥도 함께 성장한다. 외형 승인과 연차 성장 방향 승인은 완료됐지만 정확한 전환 연차·시간 계산·저장 필드·능력 효과는 아직 미명세다. 두 이미지의 승인 해시와 파일은 각 record가 소유하며 기존 원본을 덮어쓰지 않는다. 이후 '검토 대기'라는 역사 문구는 이 두 외형 승인에 한해 대체된다.

권장 성장 표현: 초기에는 도구 이름을 혼동하고 도움을 주려다 머쓱해하는 어린 조수, 이후에는 작업 순서를 익히고 대장장이의 의도를 알아채는 동료로 변화한다. 외형뿐 아니라 말투·동작 숙련도·공방 추억의 반응이 함께 변하되 호기심과 귀여움은 유지한다. 해마다 새로운 전신 자산을 생산하기보다 승인된 두 단계와 단계 내 대사/동작 변화를 우선한다. 구체적 경계 연차, 정령의 힘 회복과 성장의 관계는 후속 기획에서 검토한다. 사용자에게 아직 승인받지 않은 수치 보너스·자동강화·강제 손해를 성장 보상으로 추가하지 않는다.

최신 성격·외형 보완: 사용자는 더 어린 느낌과 세상 물정을 몰라 실수하는 귀여운 정령을 요청했다. 동그란 얼굴·짧은 체구·큰 호기심 어린 눈·조금 큰 작업복으로 보완한다. 실수는 표정/도구 혼동 같은 가벼운 연출로 제안하며 플레이어 장비 파괴·자원 손실·강화 실패를 강제로 유발하는 시스템으로 확대하지 않는다. 금빛 머리·호박색 눈·인간형·공방 조수·약한 잔불·비픽셀 애니메이션풍은 유지한다. 정확한 나이와 성별은 별도 확정하지 않는다. 이전 전신 원본을 편집 입력으로 사용하며 새 외형은 다시 검토 대기다.

최신 사용자는 모닥을 **힘을 잃고 대장장이의 공방에 머무르며 조수로 돕는 의인화된 불의 정령**으로 지정했다. 이어 이번 제작에서는 픽셀을 제외해도 좋다고 승인했다. 이 예외는 우선 모닥 시안에 적용하며 전체 게임의 렌더링 방향을 자동 교체하지 않는다. 아래10개 불꽃 생물형은 이전 탐색 이력으로 전환한다. 대장장이1번 선택은 유지한다.

- BP11-MODAK-STYLE / planned workshop companion, 단일 전신 외형 후보. 금빛 머리·호박색 눈·작은 손끝 불씨·공방 조수 복장을 권장 디자인으로 적용한다.
- 피부와 사람형 얼굴/팔다리가 있는 애니메이션 일러스트. 전신 화염 대신 잔불로 쇠약함을 표현한다. 밝은 정령이라는 정체성은 유지하지만 과거의 '의상 없음/몸 전체가 불꽃' 조건은 이번 의인화 방향에서 대체된다.
- 사용자가 제공한 두 금빛 의인화 이미지의 따뜻함·신비로움만 참고한다. 고유 얼굴·하트 문양·현대 티셔츠·불꽃 뿔·UI를 복제하지 않는다. 참고 이미지 권리/배포 허가는 미확인이며 원본을 출시 자산으로 사용하지 않는다.
- 성별·정확한 나이는 확정하지 않는다. 중성적이고 작은 인간형을 이번 후보 기본값으로 사용한다. 구체적인 외형은 사용자 검토 대기다.
- 화로 살피기·도구 건네기·작업 결과에 반응하기는 연출 제안이다. 자동강화·성공확률·자원생성·전투능력 수치는 승인하지 않았다.
- 이번은 단색 배경의 외형 검토 원본1장이다. 투명화·레이어 분리·idle/도구 전달/집중/기쁨/걱정 모션과 runtime은 후속 작업이다. 비픽셀 일러스트에 Aseprite 픽셀격자 정리를 강제하지 않는다.

최신 선택: 사용자가 대장장이1번(`smith-01.png`, SHA256 970ea84a3db8d03227e4c408c4fd7a7b8155acb3d8d14fe00274fcc324ba60e3)의 외형을 선택했다. 선택은 픽셀 정리·모션·runtime 완료가 아니다. 모닥은 추가10외형 비교를 명시 요청했으므로 기존1안을 확정하지 않는다. BP11-MODAK-STYLE consumer와32~64px 후속 목표를 유지하며, 기본 정지 외형만10개 생성한다. 차이는 둥근 불씨/혜성꼬리/인간형/납작형/여우형/토끼형/불꽃꽃잎/소용돌이/튼튼한 사각형/긴꼬리형이다. 밝은 노랑·주황 불꽃, 검은 숯 몸체 제외를 유지하고 새로운 능력·보상은 만들지 않는다. 이번 비교 배경은 명시적인 단색이며 투명도를 가장하지 않는다. 최종 선택 후에만 실제 투명화·native-grid·모션 제작으로 진행한다.

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

- 2026-09-12 상태 아틀라스 갱신: 사용자가 반복 배경 카드의 무의미함을 지적했다. 첫 장을 실제 값·소유권·다음 페이지가 있는 흐름 지도로 바꾸고46~50절에15개 상태 도식을 추가했다.51절은 대표 하루·주문·시간 시험과 검수 과제를 통합한다. 기존45절은 보존하며 읽는 순서를6부로 확장했다. 후속 시간/주문 자료가 PDF 미반영이라는 아래 이력은 이 갱신으로 대체된다. 기존 raster 자산은 변경하지 않고 PDF에서 기존 방패 영역·배경을 배치한 text-native UI 도식이다. 물리 각인·균열·배우 모션은 여전히 미준비. 수리 예시는 추가 손상 후3/5/5→4/4/5로 현재+1 보호를 지켰다. UI 비활성 대비·절당1쪽·15상태 내구 불변식·원본/PDF 바인딩 검수. 임시 렌더는 별도 삭제 검토 폴더로 전달하며 자동 삭제하지 않는다.

### Remaining work audit 20260912

#### 주문 수·보고 지연 오프라인 시험 결과

사용자의 최신 ‘권장안대로 진행’은 수동 마감 권장안을 따라 상세 준비를 계속하는 승인으로 기록한다. 새 숫자와 전체 제품 구현의 최종 승인은 여전히 별도다. 이번에는 설명뿐 아니라 `tools/simulate_order_schedule_review.py`의 비런타임 일정 모형을 실행했다. 명세 수치는 기존 calendar review JSON의 order_schedule_trial에서 읽는다.

| 시험 구성 | 권장값 | 이유·한계 |
|---|---|---|
| 주문 표시/수락 공간 | 재기1 + 선택2 = 총3칸 | 어려운 주문/보고 대기만으로 재기 경로를 막지 않음. 모바일 가독성은 미검수 |
| 재기 주문 | +0 납품 후400골드·보강재2, 칸은 다음 날 보충 | PDF39절 기존 시험값 유지. 주문 전용 재료·완제품 소비가 정상이라는 전제 |
| 사건 보고 | 결투1일·모험2일·군대3일 후 | 인계한 게임 일차 기준, 수락일·현실 시간이 아님. 신규 시험 정의에만 적용 |
| 선택칸 점유 | 인계 후 결과 확정까지 유지 | 같은 UID 중복 인계 금지. 결과가 저장되면 반환/정산과 함께 칸 해제 |
| 미수락 주문 | 그대로 유지 | 빈 날 마감으로 재추첨 불가. 완수 불가 요구 생성은 producer 사전 검증 필요 |

조사(2026-09-12): [Potion Craft 공식](https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/)의 손님 문제 해결은 ADAPT, [Anvil Saga 공식](https://store.steampowered.com/app/1587540/Anvil_Saga/)의 공방과 주문 맥락은 ADAPT하되 방 확장·직원·세력 경영은 REJECT, [Gladiator Guild Manager 공식](https://store.steampowered.com/app/1043260/Gladiator_Guild_Manager/)의 대회 사이 준비 맥락은 비교하되 월간 대회 강제 일정은 REJECT한다.3칸·1/2/3일은 우리 시험 설계이지 사례에서 검증된 최적 수치가 아니다. 기존 EquipmentWorldRegistry의 result_due_day는 구현 참고일 뿐 현재 vertical_slice와 연결됐다고 간주하지 않는다.

**실행 결과:** 빈 날240회 마감→241일, 골드0, 기존 주문 ID 유지. 날짜만으로 성장시키면 EARLY를 거의 플레이하지 않고 LATER를 볼 수 있다는 반례는 그대로 남았다. 재기 주문30회 정상 완료 가정→12,000골드·보강재60. 무한 ‘중복 지급’과 정상 ‘반복 노동 수입’을 구분하며 제작 조작·소모·소요 시간을 생략했으므로 자원 회복 속도가 적당하다고 판정하지 않는다. 결과 모형은 게임 세이브를 읽거나 쓰지 않는다.

**시험 목록:** 빈 날 무보상/미재추첨, 재기 중복 완료 차단/다음 날 보충, 중복 마감/저장 실패 주입, 보고 시점/단발 확정/UID 중복 인계 차단, 선택칸2개 점유 중 재기 가능, 미지 사건 profile 거부, 늦은 인계일 기준1/2/3일 경계. 저장 실패는 모형에 주입한 boolean으로 검사하며 실제 파일 원자성의 증거가 아니다. 재기 +0 작품 생산·소비, 성공률·손상·보상, 정상 저장/종료·UI는 이 모형에서 제외된다.

**후속 판정:** 재기1칸 예약은 KEEP_FOR_TRIAL, 보고 지연/주문3칸은 TEST_IN_PLAY,120일/년 최종 잠금은 HOLD다. ‘관계 경험치’나 ‘필수 일일 노동’으로 성장 조건을 몰래 바꾸지 않는다. 먼저 대표1일에 주문 선택→제작/강화→인계→마감→보고를 연결할 화면/입력 명세와 플레이 과제를 마련한다. 경제 시험은 실제 제작 비용·시간과 함께 해야 한다. 이번 자료는 PDF45쪽 이후 통합 대상이며 PDF를 이미 갱신했다고 주장하지 않는다.

#### 영업일 진행·주문 주기 검토

2026-09-12 후속, RECOMMENDED_TEST_ONLY. 수치·기계 키는 기존 `BLACKSMITH_MODAK_CALENDAR_REVIEW_20260912.json`의 day_close_review가 단일 책임 원본이다. 아래는 사람용 설명이며 최종 규칙 승인 또는 게임 구현이 아니다.

| 방식 | 강화 코어 영향 | 판단 |
|---|---|---|
| 수동 영업 마감 | 작업 중 강제 정지 없이 자원·위험으로 STOP OR PUSH 판단 | 권장 시험안. 날짜 정체·빈 날 넘기기 검수 필요 |
| 행동 예산/피로도 소진 | 강화마다 추가 행동비용·강제 종료·회복 경제 필요 | 이번 재기획에 자동 도입하지 않음. 기존 구형 피로도 재활성화 금지 |
| 주요 주문 완료마다 하루 | 반복 리듬은 단순하지만 주문 처리와 세계 시간의 의미가 결합 | 비교안만 유지. 동시에 끝난 여러 주문의 날짜 중복과 강제 시간 경과 위험 |

조사: [Potion Craft 공식 상점](https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/)의 매일 찾아오는 손님과 문제 해결형 요청은 ADAPT한다. [Potionomics 공식 상점](https://store.steampowered.com/app/1874490/Potionomics/)의 제작·상점·경쟁을 연결한 구성은 비교하되, 카드 협상·경쟁 일정·관계 경영은 REJECT한다. [A Wonderful Life 공식 설명서](https://www.storyofseasons.com/awl/manuals/switch/06/)의 시간·계절 안내는 ADAPT하지만 현실 시간 압박과 농장 관리 체계를 가져오지 않는다. 수동 마감은 이 사례들에 대한 우리 설계 판단이며 해당 게임이 동일 규칙을 쓴다는 주장이나 직접 플레이 결과가 아니다.

**정상 흐름:** 공방 대기 → 오늘 마감 선택 → 미완 주문/다음 보고 안내 → 확정 → 같은 저장 후보에서 일차+1·도래 사건 정산·빈 완료 주문칸 보충·성장 표시 대기 등록 → 저장 성공 → 다음 날 표시. 미완 강화/수리/인계 거래 중에는 마감 불가이며 이유를 보여 준다. 취소·미리보기·세계창 시청은 날짜를 바꾸지 않는다. 전투/사건 모션의 종료를 저장 완료로 쓰지 않는다.

**마감 UI:** 제목 ‘오늘 작업을 마칠까요?’, 현재 날짜→다음 날짜, 진행 중 주문 수, 도착 예정 보고 수, ‘계속 작업’과 ‘다음 날로’ 두 선택을 표시한다. 진행 중 주문은 자동 실패하지 않으며, 별도 납기 계약을 앞으로 도입할 때만 수락 전 기한과 결과를 보여 준다. 마감의 의미를 연속 강화 중단과 혼동하지 않도록 강화 버튼 옆의 주 행동으로 배치하지 않는다.

**주문 주기:** 시험안은 수락한 주문을 완료/명시적 취소 정책이 확정될 때까지 유지한다. 미수락 주문은 마감만으로 재추첨되지 않는다. 완료로 빈 칸이 생겼을 때만 다음 날 새 정의를 순서대로 공급하고 그 순서를 저장한다. 무료 거절→대체 주문 생성은 아직 넣지 않는다. 초기 표시 개수와 보충 개수는 기존 주문 스키마/대표 플레이 검토 뒤 결정하며 숫자를 임의 승인값으로 추가하지 않는다. 재기 주문은 PDF39절의 별도 시험 규칙을 유지하며 날짜 넘김 자체에 골드·촉매·무료 장비를 지급하지 않는다.

**세계 사건:** 보고 지연이 명세된 사건만 확정된 날짜 도래 시 한 번 처리한다. 시청 여부와 결과·보상은 분리한다. 지연 정책이 없는 사건을 임의로 하루 후 완료시키지 않는다. 도래 처리와 해당 날짜 저장은 원자적이어야 하며 손상·반환·보상이 일부만 공개되는 상태는 금지한다. 같은 campaign/source_day 거래가 재시도되면 기존 결과를 반환하고 추가 날짜·보상·주문을 생성하지 않는다.

**미해결 위험을 숨기지 않는다:** 무료 빈 날 넘김은 자원 이익이 없어도 모닥 성장과 보고 대기를 쉽게 건너뛸 수 있다. 반대로 무제한 같은 날 작업은 달력을 정체시킬 수 있다. 이를 막으려고 승인 없이 관계 수치·필수 출석·강제 피로를 넣지 않는다. 후속 대표 플레이에서 마감 이유를 설명할 수 있는지, 성장만 보려고 빈 날을 반복하는지, 주문이 없어 진행이 막히는지 기록한다. 이러한 경우120일/년을 바로 최종값으로 잠그지 않고 연차 길이와 하루 의미를 함께 재검토한다.

**검증 범위:** 문서/JSON에 의도한 마감 경계·주문 유지·무보상 조건을 검사했다. 실제 게임의 날짜 변경·주문 보충·원자 저장은 미구현이며 해당 동작이 통과했다고 주장하지 않는다. 기존45쪽 PDF에는 이번 후속 검토가 아직 미반영이다. P1은 ‘아무 명세 없음’에서 ‘권장안·실패 조건 준비’로 진전됐고, P2 경제 시험 전에 주문 수와 사건 지연 정책 검토가 남는다.

현재 승인 범위는 최종 검토용 기획·자산 준비다. 기존 MVP 구현 허용 문구를 새 재기획 전체 구현 승인으로 확대하지 않는다. PR371은 이번 작업의 Draft, PR359/196은 read-only다. 작업 시작점 8b21ac9b의 원격 검사15개 통과·문서 전용 검사1개 조건부 skip을 확인했다. 이 결과가 새 설계 구현 또는 사람 검증을 증명하지 않는다.

| 순서 | 남은 작업 | 현재 상태·실제 근거 | 이번 조치 / 완료 조건 |
|---|---|---|---|
| P1 | 시간·캠페인·모닥 성장 | V5 active_run.current_day 존재, current vertical_slice 연차/일차 진행 consumer 미확인 | 아래 시험 정책과 경계 fixture 준비. 일차 진행·저장 지속 범위 최종 검토 필요 |
| P2 | 경제·주문 재기 | PDF39절 초기 시험 예산은 있지만 장기 수입/지출·고갈·무한이익은 미검증 | 날짜 진행과 주문 주기 연결 후 민감도 시험. 기존 가격 변경 금지 |
| P3 | 승인 캐릭터 생산 자산 | 청년1번·모닥2외형 승인, alpha/레이어/피벗/모션 미완 | 실제 공방 표시 크기와 제작 방식 검수 후 보정. 생성·승인·runtime 분리 |
| P4 | 세계창·장비 상태 자산 | 배경/장비 후보 확보, 세계 인물 RGB 바둑판 반려 | 투명 인물·5종 장착·태그/손상 상태군 준비; 실패 원본 출처 보존 |
| P5 | 최종 기획/PDF 승인 | 45쪽 통합 검토본, 큰 방향과 일부 외형만 승인 | P1~P4 미완료를 드러낸 최종 인수 기준 확인. 읽기 뷰 갱신 |
| I1~I7 | 신규 ruleset·판정·사건·화면·경제 | PDF35절 순서, 현재 소비자와 신규 계획 구분 | 최종 기획 승인 후 RED→GREEN→runtime 검수 |
| I8 | Android·성능·한글·접근성·사람 | 새 방향으로 NOT_RUN | 실제 빌드·캡처·입력·플레이 증거, 출시 권리 별도 |

**P1 조사와 채택 판단:** [A Wonderful Life 공식 설명서](https://www.storyofseasons.com/awl/manuals/switch/06/)는 계절·연말과 인물 성장을 연결한다. [공식 추억 소개](https://www.storyofseasons.com/awl/memories/)는 함께 지내는 관계의 변화를 보여 준다. [Wildermyth 공식](https://wildermyth.com/)은 나이와 개인 이력이 이어지는 인물을 설명한다. ADAPT: 연차와 관계 표현 연결. REJECT: 수명·은퇴·세대 계승을 기본 의무로 추가. 별도 계절 농사/날씨 보너스·시간제 에너지 제한은 추가하지 않는다. 조사만으로 최적 일수나 재미가 증명되지는 않는다.

**시간 권장 구조:** 동일 저장 캠페인 안에서 해가 바뀌어도 공방·작품 UID·사건·모닥은 유지한다. 새 캠페인은 별도 슬롯이며 기존 슬롯 삭제나 연말 초기화가 아니다. 실제 `vs_run_initializer_service.gd`는 run_id 생성과 current_day=1, 작품·고객·스케줄 초기화를 수행하므로 연도 변경에 이 서비스를 재사용하면 안 된다. `saved_at_utc`는 저장 시각 메타데이터이며 성장 입력이 아니다. current_day에 임의 더하기·구형 PoC 피로도 재사용도 금지한다.

**수치 책임 원본:** `docs/planning/BLACKSMITH_MODAK_CALENDAR_REVIEW_20260912.json`. 게임120일/년을 시험 기본값,30/365일을 비교값으로 둔다. 짧은 안은 성장 체감이 빠르지만 서사가 급할 수 있고, 긴 안은 애착 시간이 길지만 콘텐츠 반복 위험이 크다.120은 중간 비교 가설일 뿐 최종 균형이 아니다. 계절4개나 월별 시스템을 숫자에서 자동 도출하지 않는다. 하루의 진행 방식은 별도 미해결 의존성으로 남긴다. 다음 조사에서는 수동 영업 마감, 행동 예산 소진, 주요 주문 완료 방식이 STOP OR PUSH 판단에 주는 영향부터 비교한다.

**경계와 지속성:** 합류일을0일 경과로 세고 두 해가 완전히 지난 뒤3년 차에 들어간다. 시험 정책에서1일 합류→241일 성장,61일 합류→301일 성장이다. 성장 사건은 안전한 공방 대기 상태에서 한 번 표시하며, 날짜가 여러 해 건너뛰어도 회차별 보상/장면을 대량 발생시키지 않는다. 표현 단계 계산과 장면 완료 기록을 분리한다. 정책 버전은 캠페인에 묶어 이후120→30 같은 조정으로 기존 모닥이 갑자기 자라지 않게 한다. 음수 경과·누락·미지 버전은 자동 보정하지 않고 저장 원본을 보존한다.

**기계 검증 상한:**8개 정상/경계 fixture의 연차·외형 계산만 확인한다. 잘못된 입력6유형은 향후 실제 구현의 필수 실패 시험이며, 현재 게임에서 처리한다고 주장하지 않는다. 플레이 길이·경제·모션·세이브 원자성은 NOT_RUN. 새 데이터는 docs 아래의 비런타임 시험 명세이며 제품 data/scripts/scenes/assets는 변경하지 않는다. 이번 추가는45쪽 PDF에 아직 미반영이며 다음 통합 갱신 대상이다.

**학습/정리:** 오래된 readme/skill의 광클·피버 문구는 최신 STOP OR PUSH 정본을 덮어쓰지 않는다. 현재 구현을 확인하지 않은 달력 재사용, 초기화 서비스를 연말 처리로 재사용하는 설계 오류를 검토 항목에 추가했다. 검증은 `python -B`로 수행해 불필요한 캐시 생성을 줄인다. 삭제 검토 묶음은 사용자 전용으로 보존하며 자동 삭제하지 않는다. Base 공용 승격은 아직 하지 않는다.

- 2026-09-12 사용자 정리 지침: 앞으로 삭제 가능 파일은 직접 삭제하지 않고 별도 삭제 검토 폴더에 원래 경로·해시·이유와 함께 이동한 뒤 링크를 전달한다. 실제 삭제는 사용자가 한다. 이번 검토 묶음은 저장소 밖 `../Blacksmith-delete-review/2026-09-12`이며 PDF 검수 렌더와 Python 캐시만 포함한다. 승인 원본·기존 PDF·증거·출처 불명 자료·다른 프로젝트는 보존한다. `tools/collect_delete_review.ps1`은 기본 dry-run이며 제한된 파생파일만 취급한다. 기획의 다음 작업은 시간 책임 원본·게임 1년 길이·캠페인 지속 범위 검토로 유지한다.

- 2026-09-12 통합 PDF 갱신: 기존41절 유지,42~45절에 선택한 청년 대장장이·승인 모닥 EARLY/LATER·성장 체크리스트를 수록해45쪽으로 재발행했다. 아래 PDF 미반영 문구는 이 갱신으로 대체된다. 전45쪽 렌더 생성, 변경28/41절 및 신규42~45절 화면 검수, 절당1쪽·source/PDF 해시 검증. 새 이미지 생성·게임 구현·달력/세이브 변경 없음. 문서 번들에는 PyMuPDF가 없어 기존 시스템 Python에서 렌더했다. 추가 설치 없음.

### MODAK_GROWTH_PREPARATION — 연차 성장 상세 권장안

2026-09-11 후속 기획. 두 외형과 함께 성장하는 방향은 USER_APPROVED. 아래 시점·저장·연출 규칙은 RECOMMENDED / FINAL_USER_REVIEW_PENDING이며 제품 구현 승인이 아니다. 이미지 record의 `growth_schedule=UNSPECIFIED_REVIEW_REQUIRED`는 **최종 잠금 미완료**를 뜻하며 이 권장안을 승인값으로 오인하지 않는다.

**현재 증거와 의존성:** `scripts/progression/workshop_calendar.gd`에는 day/end_day가 있으나 참조는 `scripts/poc/equipment_lifecycle_poc_screen.gd`에서 확인된다. 현재 vertical_slice의 `vs_save_envelope.gd`와 `vs_run_initializer_service.gd`에는 current_day가 있지만 이를 연차로 환산하는 현재 consumer는 확인되지 않았다. 따라서 CALENDAR_INTEGRATION_REQUIRED. 구형 피로도·이월률 또는 365일을 새 시간 정본으로 역수입하지 않는다. Base v9.4.4 계약 검증 통과, 최신 Base main 관찰은 2f93e872이며 채택 잠금은 유지했다.

**조사·비교:** [STORY OF SEASONS: A Wonderful Life 공식](https://www.storyofseasons.com/awl/)의 오랜 시간에 걸친 가족·관계 이야기는 ADAPT: 공방의 일상과 함께 성장 체감을 만든다. [Wildermyth 공식](https://wildermyth.com/)의 나이·변화·개인 이력이 연결되는 인물 구성은 ADAPT: 예전의 실수를 이후의 능숙한 행동으로 회수한다. 죽음·은퇴·세대 교체는 REJECT: 모닥을 잃을 위험이나 별도 육성 의무를 만들지 않는다. 외형만 바꾸는 방식은 감정 연결이 약하고, 매년 새 외형을 만드는 방식은 자산 부담이 크므로 **두 외형 + 중간 대사/동작 변화**를 권장한다. 이는 사례를 바탕으로 한 설계 판단이며 재미 검증 결과가 아니다.

| 합류 이후 단계 | 외형 | 대사·행동 권장 예 | 플레이 역할 |
|---|---|---|---|
| 1년 차: 낯선 세상 | EARLY 승인본 | “집게가… 이거 맞지?” 도구를 확인하고 머쓱하게 웃음 | 호기심 많은 어린 조수; 입력을 가로막지 않는 짧은 반응 |
| 2년 차: 익숙해진 공방 | EARLY 유지 | “이번엔 제대로 가져왔어!” 먼저 도구를 준비하고 자랑함 | 같은 실수를 반복하는 대신 배운 것을 보여 줌 |
| 3년 차 이후: 믿음직한 동료 | LATER 승인본 | “이 집게지? 오늘은 내가 먼저 챙겼어.” 전달 자세와 불꽃 제어가 안정됨 | 능숙해져도 칭찬에 들뜨고 세상에 대한 질문은 유지 |

시점 상태는 YEAR_3_RECOMMENDED_NOT_LOCKED. JOIN_RELATIVE_GAME_YEARS: 세계의 절대 연도가 아니라 모닥과 함께 지낸 게임 연차를 기준으로 한다. NO_WALL_CLOCK_AGING: 현실 시간·접속 공백·기기 시계 변경으로 성장시키지 않는다. 게임 1년의 일수와 한 해의 실제 플레이 길이는 전체 시간 설계에서 먼저 지정하고 초반 플레이 검증으로 조절한다. 이 의존성이 풀리기 전에는 연차를 임의 계산하지 않고 EARLY를 유지한다. 정령의 힘 회복은 별도 서사이며 성장만으로 전투력·강화 성공률·자동 생산 보너스를 부여하지 않는다. NO_FORCED_RESOURCE_LOSS: 실수 때문에 장비 파괴·촉매 소비·강화 실패가 발생하지 않는다.

**연출 흐름:** 합류 → 일상 반응 축적 → 연차 경계 판정 → 현재 강화/수리 결과 처리 완료 → 공방의 안전한 대기 상태에서 짧은 성장 장면 → LATER 표현. 장면은 건너뛸 수 있고, 건너뛰어도 같은 결과와 추억 기록을 남긴다. 대사 중 저장/종료 후 재진입해도 보상이나 성장 사건을 중복 적용하지 않는다. 게임 진행보다 모닥 연출을 우선하지 않는다. 이전 어린 모습은 추억 화면에서만 회상하며 현재 외형을 임의로 되돌리는 기능은 이번 범위에 추가하지 않는다.

**저장·연결 명세 후보:** 현행 save envelope의 버전 관리·검증 경로를 확장하는 방식으로 준비한다. 합류한 게임 시점과 단발 성장 사건 완료 ID를 보관하고, 연차·표현 단계는 같은 시간 정책에서 파생한다. 저장할 age/year/stage 값을 중복 증식하지 않는다. 정확한 필드명과 run 종료 후 유지 여부는 캠페인/시간 책임 정본 검토 뒤 잠근다. 기존 저장에 모닥 합류 기록이 없으면 다음 안전한 공방 진입에서 합류를 시작하며, 오래된 current_day만 보고 성장 외형을 즉시 적용하지 않는다. 마이그레이션 전 원본 보존, 알려지지 않은 버전은 덮어쓰기 금지, 장면 완료 ID와 관련 상태는 동일 저장 단위로 처리한다. SAVE_MIGRATION_NOT_IMPLEMENTED.

**자산·모션 준비표:** 두 승인 원본을 유지한다. 각 단계에 투명 전신, 얼굴/머리/몸/팔/도구/불꽃 분리, 공통 발 기준점과 손잡이 기준점이 필요하다. idle·도구 확인/전달·집중·기쁨·걱정·머쓱함을 준비한다. 어린 단계는 짧고 조심스러운 전달, 성장 단계는 안정적인 전달로 차별화하며 불꽃이 버튼이나 작업 대상물을 가리지 않게 한다. 전신을 매년 새로 생성하지 않는다. 표시 크기·레이어 수·애니메이션 방식은 실제 공방 슬롯 검수 후 고정; 현재는 외형 승인만 완료, alpha/motion/engine/Android 검증은 NOT_RUN.

**구현 순서/완료 체크:** [ ] 현재 시간 책임 원본과 캠페인 지속 범위 잠금 → [ ] 연차 전환 경계 데이터 → [ ] 두 외형 투명 자산·공통 피벗 → [ ] 세이브 마이그레이션·성장 사건 중복 방지 → [ ] 공방 대기 상태 연결 → [ ] 실제 화면 검수. 제품 구현은 최종 기획 승인 뒤 진행한다. 필수 테스트는 경계 직전/정확한 경계/복수 연차 건너뜀, 장면 중 종료/스킵/재진입, 구형 저장, 시간 의존성 누락, 기기 시계 변경, 자원·확률 불변, 현재 run과 장기 기록 구분이다. 현재 문서 계약 검사는 이 표의 구현이나 재미를 증명하지 않는다.

**개선·학습:** 외형 승인과 시간·저장 승인 분리, 구형 PoC 달력을 현재 시스템으로 간주하지 않기, 강제 손해 없이 실수의 귀여움을 표현하기. 프로젝트 내 검토 기록이며 Base 공용 승격은 미실행. 기존41쪽 PDF에는 이번 성장 상세가 아직 반영되지 않았으므로 다음 통합 PDF 재발행 시 본 절과 승인 원본을 함께 수록하고 source binding을 다시 검증한다.

- 재개 체크: 직전915bc629 원격 검사15SUCCESS/1조건부SKIPPED, 작업 브랜치0/0 확인. 모닥 배경제거 편집1회는1254×1254 RGB로 바둑판이 남아 반려했다. 원본 후보4장은 불변, 실패 binary는 저장소에 중복 복사하지 않고 record의refinements에 출처/해시/프롬프트를 남겼다. [Aseprite 공식 알파 정의](https://www.aseprite.org/docs/color-mode/)를 재확인했으며 보이는 바둑판을 투명도 증거로 쓰지 않는다. 같은 편집 반복 대신 지원되는 배경 처리 경로 점검이 필요하다. 대장장이 최종 선택·모션·게임 적용은 여전히 미완료. AgentMemory 세션 도구가 이번 연결 목록에 없어 현재 저장소와 Git 검증으로 재개했으며 세션 조회 성공을 주장하지 않는다.

-41쪽/41절 통합 PDF 생성, 전체 페이지 렌더 검사. 표 머리글 대비 교정, 불가능한+10·태그II 예시를+20으로 수정, 사건 준비도 cap 예시와 수리비 확보구간 설명 교정 후 해당 페이지 재검수.
- 신규7가족 중 배경4·장비/재료 아틀라스·대장장이 후보 확보. 세계 인물 시트와 배경제거 편집은 둘 다RGB 바둑판으로 runtime 입력 반려. 두 번째 반려 binary는 저장소에 중복 복사하지 않고 hash/source locator만 기록.
- 장비 atlas는 restricted Aseprite의 최근접384출력·native원본·PNG내보내기 decoded RGBA 동일 확인. 마무리 픽셀·알파·전체 모션/장착/상태·engine import는 미완료.
- PDF/source/후보 해시 및41페이지 계약 검사. 기존21쪽 PDF와 게임 보호 경로는 변경하지 않았다.
- Base 검사는 jsonschema가 있는 기존 Python에서 실행. 문서 번들 Python에 jsonschema가 없어 실패한 검사는 환경 원인을 확인하고 기존 검증 런타임에서 다시 PASS를 확인했다. 불필요한 패키지 설치 없음.
- L1 resume 검사는 PASS. 전체 작업이IN_PROGRESS이고 자산·최종사용자검토가 남아 closeout은 정상적으로 거부된다. 이를 회피하기 위해 DONE으로 바꾸지 않는다.
- 학습 후보: PNG확장자/바둑판 표시를 투명도 증거로 쓰지 않기, 조건부 확률과 최종확률 분리, 태그단계 예시에 도달가능성 검사, 작업용 PDF를 모든 자산 준비 완료로 오인하지 않기. 프로젝트에 먼저 검증을 남기며 공용 Base는 이번에 수정하지 않았다.
- 원격 첫 검사에서 Active Context의 연속 상단 추가가 기존 priority/provenance 안내를2500자 밖으로 밀어낸 실패를 발견했다. 최신 안내 바로 위에서 현재 우선순위와 기존 결정 원장 연결을 명시해 수정한다. 역사 원장 내용을 최신 권한으로 승격하거나 검사 범위를 느슨하게 바꾸지 않는다.
