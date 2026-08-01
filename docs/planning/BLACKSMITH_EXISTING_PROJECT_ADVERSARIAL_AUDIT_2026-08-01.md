# Blacksmith 기존 프로젝트 적대적 감사 보고서

> Audit ID: `BS-REPO-AUDIT-20260801-01`
>
> 상태: `AUDIT_COMPLETE / FINDINGS_OPEN`
>
> 기준일: `2026-08-01`
>
> Work Mode: `REVIEW`
>
> 구현 권한: `NONE`
>
> 기준 main: `500a5a7960146ef229ae172cf9e127306d23f073`
>
> 계획 브랜치: `docs/blacksmith-v9-planning-audit`
>
> 추적: Issue #79 / Draft PR #81

## 1. 감사 목적

현재 승인된 Blacksmith v9 기획과 비주얼 기준이 기존 Prototype·장비 생애 PoC 위에 안전하게 통합될 수 있는지 확인한다.

감사 대상:

- 운영 시작 문서와 권위 지도
- `project.godot`과 실제 기본 실행 Scene
- 제작·강화·보관함·고객·세계 결과 UI
- 강화·제작 등급·수식어·재료·고객·세계 데이터
- 세션 상태·저장·복구·접근성·Android 경계
- 기존 테스트가 보호하는 구형 계약
- 승인된 비주얼 보드가 암시하는 신규 시스템

이번 감사는 코드 수정이 아니라 **누락·충돌·보완·유지 항목을 확정하는 기획 감사**다.

## 2. 감사 기준

권한 순서:

```text
사용자 최신 승인
→ BS-MAIN-20260801-01 / BS-SHELL-20260801-01
→ BS-ART-20260731-01 / BS-MODAK-20260731-01
→ BS-CUST-20260731-01 / BS-ENH-20260731-01
→ Blacksmith Vertical Slice v9 기획
→ main의 실제 Scene·Script·Data·Test
→ 구형 PoC 문서와 역사 기록
```

판정 태그:

- `KEEP`: 기존 강점이며 보존
- `MISSING`: 최신 제품 계약에 필요하지만 없음
- `CONFLICT`: 실제 구현·데이터와 승인 기획이 직접 충돌
- `STALE`: 현재 사실과 맞지 않는 활성 문서·메타데이터
- `IMPLIED_NOT_APPROVED`: 시안에 보이지만 시스템 승인 없음
- `NOT_RUN`: 실행 증거 없음

## 3. 적대적 검토 루프

### Pass 1 — 진입·상태 소유권

질문:

- F5가 제품 메인 화면으로 진입하는가?
- 메인·허브·PoC·강화가 하나의 캠페인 상태를 공유하는가?
- 앱 종료 후 이어하기가 가능한가?

판정: `FAIL`

### Pass 2 — 핵심 규칙·데이터 정합성

질문:

- 제작 등급·계보·보조·+50 두 경로가 실제 데이터와 일치하는가?
- 자동화가 플레이어의 핵심 선택을 건너뛰지 않는가?

판정: `FAIL`

### Pass 3 — 고객·세계 환류 재사용성

질문:

- 4개 고객 유형과 유형별 복수 고객을 같은 파이프라인으로 표현할 수 있는가?
- 거래 자격·공개 적합도·소유권·운명·연대기가 분리돼 있는가?

판정: `FAIL`

### Pass 4 — 비주얼·UX 구현 가능성

질문:

- 승인된 스타일을 공통 Theme·Scene으로 적용할 경계가 있는가?
- 세로형·안전 영역·텍스트 확대·설정 유지가 가능한가?

판정: `FAIL`

### Pass 5 — 검증·운영 정본

질문:

- 현재 시작 문서와 Base 버전이 실제 상태와 일치하는가?
- 테스트가 최신 스키마와 제품 진입·저장 구조를 보호하는가?

판정: `FAIL`

감사 자체는 완료됐으나 Finding이 열려 있으므로 제품 구현 또는 `기획 완료` 상태로 전환하지 않는다.

---

# 4. P0 Finding — 제품 구조와 핵심 규칙 차단

## BS-AUD-F01 — 기본 실행 Scene이 제품 메인 화면이 아님

- 유형: `CONFLICT`
- 증거: `project.godot`의 `run/main_scene`이 `scenes/test/enhancement_test.tscn`
- 실제 상태: F5 실행 시 테스트용 철검 강화 화면으로 진입
- 승인 상태: `BS-MAIN-20260801-01` 별도 메인 화면
- 영향: 신규 사용자 진입, 이어하기, 설정, 캠페인 복구를 검증할 제품 경로가 없음
- 권장 조치: 제품 Boot·MainMenu Scene을 별도 책임 원본으로 만들고 테스트 Scene은 명시적 개발 경로로 격리

## BS-AUD-F02 — 영속 세이브·이어하기·미확인 결과 복구가 없음

- 유형: `MISSING`
- 저장소 검색에서 프로젝트 게임 상태를 `user://`에 저장하는 Save Manager·Save Coordinator를 확인하지 못함
- 현재 `snapshot()`은 메모리 Dictionary와 테스트 롤백에 한정
- 메인 화면의 이어하기 버튼을 활성화할 저장 메타데이터 계약이 없음
- 강화·납품·세계 결과 도중 앱 종료 후 같은 결과를 복구할 수 없음
- 권장 조치: 캠페인 세이브, 설정 세이브, 원자 저장, 미확인 `ResultEnvelope` ID, 손상 복구 계약을 별도 정본화

## BS-AUD-F03 — 세 개의 런타임 흐름이 서로 다른 상태를 소유

- 유형: `CONFLICT`
- 흐름 A: `enhancement_test_runner.gd`의 테스트 강화·보관함
- 흐름 B: `game_flow_screen.gd`의 제작·강화·6칸 보관함·자동 단조
- 흐름 C: `equipment_lifecycle_poc_screen.gd`의 카일 계약·별도 자원·별도 Registry
- 각 흐름이 골드·재료·보관함·장비 목록을 독립 생성
- 화면 이동이 동일 캠페인의 연속이 아니라 별도 데모 재시작에 가까움
- 권장 조치: `BS-SHELL-20260801-01`에 따라 도메인 상태 소유자를 App Shell·Save Coordinator로 단일화

## BS-AUD-F04 — 제작 등급 이름·ID가 승인 정본과 충돌

- 유형: `CONFLICT`
- 실제 데이터: `APPRENTICE / STANDARD / REFINED / MASTERWORK / PERFECT`
- 실제 표시: `미숙한 / 평범한 / 정교한 / 명품 / 완벽한`
- 승인 정본: `보통 / 양질 / 우수 / 명품 / 걸작`
- 고객 점수·fixture·resolver·테스트가 구형 ID를 직접 참조
- 권장 조치: 표시명만 교체하지 말고 스키마 버전·호환 변환·고객 점수·fixture·테스트를 함께 마이그레이션

## BS-AUD-F05 — 수식어·이정표·+50 구조가 승인 정본과 충돌

- 유형: `CONFLICT`
- 실제 데이터: +10 슬롯 1 추가, +20 슬롯 1 강화, +30 슬롯 2 추가, +50 슬롯 3 추가
- 실제 코드: +50 이상 수식어 슬롯 3개 허용
- 승인 정본: 계보 1개 + 보조 최대 2개, +50은 새 슬롯이 아니라 일반 또는 고위 정밀강화 경로
- 실제 모든 10단위가 재료·정밀 타격·추가 성공 확률을 사용
- 승인 정본은 10단위 진입 성공 후 정체성 선택에 두 번째 실패 판정을 두지 않음
- 권장 조치: `lineage_affix_id`, `secondary_affix_ids`, `enhancement_route_at_50`, `special_affix_id`, `evolution_id` 중심의 신규 스키마와 legacy 변환 계약 필요

## BS-AUD-F06 — 자동 단조가 핵심 판단을 건너뜀

- 유형: `CONFLICT`
- 실제 자동 단조는 목표 단계까지 반복하고 정밀 위치를 난수로 완료
- 특수재료가 부족하면 재료 없이 계속 진행할 수 있다는 UI 안내가 존재
- 고위험·이정표·+50 경로를 플레이어가 직접 판단해야 한다는 핵심 경험과 충돌
- 자동 흐름이 장비 파괴 후 새 장비로 반복할 수 있어 작품 애착과 비가역 선택을 약화
- 권장 조치: 자동 단조는 일반 구간에만 사용하고 +5 완성 판단, +10 단위 선택, +49→+50 경로, 판매·인계 전에 반드시 정지하도록 기획 경계 확정

## BS-AUD-F07 — 고객 구조가 카일·철검에 하드코딩

- 유형: `CONFLICT`
- 실제 계약은 `equipment_id = iron_sword`, `customer = 카일`, 기한 3일
- 화면도 검투사·철검·카일 재방문 문구를 직접 보유
- 승인 정본은 수집가·모험가·검투사·군인 4유형, 유형별 복수 이름 고객, 범주 요청, 동시 요청 최대 2개, 기본 2영업일
- 거래 자격이 정확한 아이템 ID와 강화 단계에 묶여 있고 소유·판매 가능 상태가 분리되지 않음
- 권장 조치: `CustomerType`, `CustomerProfile`, `CustomerRequest`, `EligibilityRules`, `PublicFitRules`, `WorldOutcomeTable` 공통 데이터 계약으로 분리

## BS-AUD-F08 — 장비 운명·관계·세계 결과가 최신 모델을 표현하지 못함

- 유형: `CONFLICT`
- 실제 운명 상태는 `BROKEN_OR_LOST`처럼 분실과 파괴가 결합
- 승인 정본은 정상·전투 흔적·분실·회수·영구 파괴를 분리
- 실제 관계는 Controller의 단일 정수이며 고객별 관계가 아님
- 실제 결과는 검투사 경기의 `DEFEAT / WIN / DECISIVE_WIN` 한 종류
- 권장 조치: 고객별 관계, 장비별 운명, 콘텐츠 세트별 결과 어휘, 공통 원인·상태 변화 계약 필요

## BS-AUD-F09 — 결과 UI와 비가역 결과 저장 계약이 분산

- 유형: `MISSING`
- 제작 결과는 작업대 상태 문구, 강화 결과는 강화 화면, 거래 결과는 작업대 문구, 세계 결과는 별도 경기 보고 UI
- 공통 이전·이후 Snapshot, 원인, 자원·관계·소유권 변화, 연대기 형식이 없음
- 결과를 디스크에 먼저 저장한 뒤 표시한다는 제품 계약이 구현되지 않음
- 권장 조치: `ResultEnvelope`와 `ResultType` 공통 스키마, 원자 저장 완료 후 확인 버튼 활성, 재진입 멱등성 테스트 필요

## BS-AUD-F10 — 승인된 시각 보드가 미승인 시스템을 암시

- 유형: `IMPLIED_NOT_APPROVED`
- 시안에 플레이어 레벨, 청색 보석, 에너지, 업적, 상점, 도감, 특수 제작, 보관함 128/150 등이 표시
- 이 항목들은 화면 구성 예시이며 승인된 시스템 정본이 아님
- 결제·광고·프리미엄 재화는 범위 승인 없이 추가 금지
- 시장 거리·경기장은 현재 직접 탐색 공간이 아니라 결과·배경 표현 후보
- 권장 조치: 비주얼 보드와 모든 파생 프롬프트에서 해당 요소를 `PLACEHOLDER / NOT_CANON`으로 고정

---

# 5. P1 Finding — UX·운영·검증 보완

## BS-AUD-F11 — 활성 시작 문서가 실제 병합 상태보다 오래됨

- 유형: `STALE`
- `START_HERE.md`, `ACTIVE_CONTEXT.md`, `DEVELOPMENT_GATES.md`, README 일부가 PR #35 Draft·병합 대기 상태를 유지
- 실제 PR #35는 2026-07-24 병합 완료
- 신규 작업자가 현재 Issue·PR·브랜치를 잘못 판단할 위험
- 권장 조치: 기획 PR 병합 시 main의 시작 문서·Gates·Roadmap·README를 일괄 갱신

## BS-AUD-F12 — Base v8·v9.1·v9.3 기준이 동시에 활성

- 유형: `CONFLICT / STALE`
- `AGENTS.md`와 `BASE_RULES_VERSION.md` 일부는 Base v8 pin을 표시
- main에는 Base v9.1 운영 어댑터가 병합됨
- Draft v9 기획은 Base v9.3을 목표로 함
- 권장 조치: 제품 규칙과 운영 어댑터를 구분해 현재 적용 버전·목표 버전·마이그레이션 Gate를 한 문서에서 명시

## BS-AUD-F13 — UI가 런타임 GDScript 조립에 과도하게 집중

- 유형: `MISSING`
- 주요 Panel·Label·Button·Overlay가 Script에서 직접 생성
- 승인된 철·황동 Theme, 고객 카드, 장비 카드, ResultEnvelope를 에디터에서 시각 검수하기 어려움
- 화면별 스타일 drift와 아트 교체 비용이 커짐
- 권장 조치: 공통 Theme Resource와 재사용 UI Scene을 만들고 Controller Script는 상태·데이터 연결만 담당

## BS-AUD-F14 — 고정 폭·고정 오프셋과 안전 영역 누락

- 유형: `MISSING`
- `custom_minimum_size = 672`, 좌우 24px, 여러 270px·305px 고정 배치가 존재
- 저장소에서 `DisplayServer.get_display_safe_area()` 또는 동등한 제품 안전 영역 처리를 확인하지 못함
- 18:9·20:9·노치·텍스트 확대에서 과밀 위험
- 권장 조치: SafeAreaContainer, 최소·최대 폭, 세로 스크롤, 폰트 스케일별 화면 계약과 실기기 검증 필요

## BS-AUD-F15 — 설정 화면과 설정 영속성이 없음

- 유형: `MISSING`
- 시안에는 음악·효과음·진동·텍스트 크기·접근성 설정이 있음
- 실제 PoC는 정밀 보조와 모션 감소 Toggle만 제공하며 세션을 나가면 유지되지 않음
- 오디오·진동·텍스트 크기 설정 구현을 확인하지 못함
- 권장 조치: 설정 Resource·로컬 저장·메인/게임 공통 Overlay·즉시 적용·재실행 복구 계약 필요

## BS-AUD-F16 — Android 생명주기·뒤로가기·중단 복구 계약 미정

- 유형: `MISSING`
- 앱 일시중지·백그라운드·프로세스 종료·Android 뒤로가기 처리 경로가 없음
- 정밀 타격·결과 표시·판매 확인 중 중단 시 행동이 정의되지 않음
- 권장 조치: 화면별 취소 가능 여부, pause notification, 뒤로가기 우선순위, 안전 체크포인트를 상태 머신에 포함

## BS-AUD-F17 — 보관함 데이터와 용량 정책이 최신 작품 모델에 부족

- 유형: `CONFLICT / MISSING`
- 기존 Prototype은 6칸 세션 메모리 보관함
- 시안의 128/150은 임시 수치이며 승인되지 않음
- 현재 카드에는 제작 등급·계보·보조·+50 경로·운명·소유권·연대기가 완전히 들어가지 않음
- 권장 조치: 용량 정책은 별도 밸런스 결정으로 두고 작품 목록·세계 기록·파괴 기록을 분리

## BS-AUD-F18 — 판매 채널의 역할 분리가 구현되지 않음

- 유형: `MISSING`
- 최신 기획의 일반 판매·방문 상인·이름 고객은 서로 다른 경제·세계 환류 역할을 가짐
- 실제 PoC는 카일 납품 한 경로만 존재
- 권장 조치: 공통 거래 서비스 위에서 채널별 가격·관계·세계 사건 여부를 분리

## BS-AUD-F19 — 연대기 UI가 장비별 역사와 고객별 관계를 충분히 보여주지 못함

- 유형: `MISSING`
- 실제 보고 화면은 이력 개수·소유자·보고 상태의 요약 중심
- 최근 사건, 원인, 소유권 전환, 운명 변화, 오래된 기록 접기 구조가 없음
- 권장 조치: 장비 단위 ChronicleEntry, 관계 단위 CustomerHistory, 결과 원인과 사건을 같은 묶음으로 표시

## BS-AUD-F20 — 자동 테스트가 구형 스키마를 강하게 보호

- 유형: `CONFLICT`
- lifecycle validator·fixture·단위·통합 테스트가 카일·철검·구형 제작 등급·구형 수식어를 계약으로 사용
- 최신 스키마로 파일만 교체하면 정상적인 기존 테스트가 대량 실패할 가능성이 높음
- 권장 조치: 호환 변환 테스트, schema version migration, 새 고객 재사용 fixture, +50 두 경로, 별도 메인·저장 복구 E2E를 먼저 설계

---

# 6. P2 Finding — 폴리싱·출시 전 검토

## BS-AUD-F21 — Android 메인 메뉴의 게임 종료 버튼

- 유형: `PROPOSED_REVIEW`
- Android에서는 OS의 앱 전환·종료 흐름이 기본이며 별도 종료 버튼이 필수 아님
- 메인 화면에서 제외하거나 플랫폼별 표시 정책을 정해야 함

## BS-AUD-F22 — 시장·경기장 이미지가 직접 플레이 공간으로 오해될 위험

- 유형: `PROPOSED_REVIEW`
- 현재 핵심 게임은 직접 전투·탐험을 포함하지 않음
- 장소 이미지는 고객 방문·결과 장면·연대기 배경임을 UI에서 명확히 해야 함

## BS-AUD-F23 — 모닥의 실제 화면 밝기·크기 검증 필요

- 유형: `NOT_RUN`
- 승인된 밝은 불꽃은 어두운 대장간에서 시선이 과도하게 집중될 수 있음
- 허브·강화·실패·연대기 화면별 최대 면적·휘도·애니메이션 빈도 검증 필요

## BS-AUD-F24 — 폰트·아이콘·아트 라이선스와 Asset Ledger 미정

- 유형: `MISSING`
- 생성 이미지는 콘셉트 레퍼런스이며 제품 에셋 아님
- 실제 폰트·아이콘·배경·인물·장비의 출처·수정권·상업 사용·버전 기록 필요

## BS-AUD-F25 — 시각 회귀·스크린샷 검증 없음

- 유형: `MISSING`
- 핵심 화면 4종과 상태 변형을 비교하는 기준 캡처·골든 이미지·사람 검토 체크가 없음
- 720×1280, 1080×2400, 텍스트 확대, 안전 영역 상태별 검증 계획 필요

## BS-AUD-F26 — telemetry가 단일 PoC 이벤트에 한정

- 유형: `MISSING`
- 메인 진입·이어하기·저장 복구·+50 경로·고객 유형·ResultEnvelope 이해도 측정 이벤트가 없음
- 개인정보 없이 로컬 플레이테스트 지표를 확장할 새 이벤트 스키마 필요

---

# 7. 보존해야 할 기존 강점

다음은 최신 제품 구조로 이관할 가치가 있는 `KEEP` 항목이다.

1. 강화 버튼 입력당 결과 1회
2. 비용·재료·피로도·납품의 원자 거래와 롤백
3. 같은 거래·세계 사건의 멱등성
4. 앱 실제 시간과 무관한 수동 날짜 진행
5. 망치 탭마다 피로도를 부과하지 않는 원칙
6. 색상 외 문구·숫자·원인 표시 방향
7. 판매 뒤에도 장비 기록을 보존하는 Registry 개념
8. Android 세로형 720×1280·Expand 기준
9. 정밀 보조가 PERFECT를 자동 제공하지 않는 접근성 경계
10. 사람·Android·성능·외부 플레이 미실행을 PASS로 표시하지 않는 운영 원칙

## 8. 수정 우선순위

### 기획·정본 P0

1. 별도 메인 화면과 App Shell 계약 반영
2. 세이브·이어하기·ResultEnvelope 계약 작성
3. 제작 등급·수식어·+50 신규 스키마와 legacy 변환 설계
4. 고객 4유형 재사용 데이터 계약과 대표 fixture 설계
5. 자동 단조의 정지 경계 확정
6. 비주얼 보드의 미승인 요소를 Placeholder로 정리

### 구현 전 설계 P1

7. Theme·재사용 UI Scene 경계
8. 안전 영역·설정·Android 생명주기
9. 보관함·판매 채널·연대기 정보 구조
10. 신규 validator·migration·E2E 테스트 계획

### 실기기·콘텐츠 P2

11. 최종 에셋·라이선스·Asset Ledger
12. Android·접근성·성능·시각 회귀·외부 플레이

## 9. 감사 판정

```text
AUDIT_ID: BS-REPO-AUDIT-20260801-01
AUDIT_SCOPE: MAIN_DOCUMENTS_SCENES_SCRIPTS_DATA_TESTS_VISUAL_BASELINE
P0_FINDINGS: 10
P1_FINDINGS: 10
P2_FINDINGS: 6
TOTAL_FINDINGS: 26
KEEP_ITEMS: 10

SEPARATE_MAIN_MENU: USER_APPROVED
APP_SHELL_VIEW_OVERLAY_MIX: USER_APPROVED
VISUAL_BOARD: USER_ACCEPTED_WORKING_BASELINE

PRODUCT_CODE_CHANGED: NO
PRODUCT_SCENES_CHANGED: NO
RUNTIME_DATA_CHANGED: NO
FINAL_ASSETS_CHANGED: NO
RUNTIME_VERIFICATION: NOT_RUN
ANDROID_VERIFICATION: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
```

## 10. 다음 Gate

```text
감사 Finding 정본·Sheet 동기화
→ P0 기획 보완안 작성
→ 적대적 검토 Pass 2
→ 사용자 결정이 필요한 항목만 분리
→ P0 기획 Finding 0건
→ 기획 완료 선언 가능 후보
```
