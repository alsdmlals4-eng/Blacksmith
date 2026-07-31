# Blacksmith 남은 기획 항목 판정

> 상태: `CURRENT_PLANNING_STATUS / REPOSITORY_AUDIT_COMPLETE / FINDINGS_OPEN`
>
> 기준일: `2026-08-01`
>
> Work Mode: `PLAN / REVIEW`
>
> 구현 권한: `NONE`
>
> 추적: Issue #79 / Draft PR #81

## 1. 현재 결론

게임의 핵심 방향과 주요 사용자 결정은 확정됐지만, 실제 프로젝트와 최신 v9 정본 사이의 통합 설계 Finding이 열려 있다.

```text
GAME_RULE_P0_BLOCKER: 0
GAME_RULE_P1_UNDECIDED: 0
REPOSITORY_AUDIT: COMPLETE
P0_FINDINGS: 10
P1_FINDINGS: 10
P2_FINDINGS: 6
TOTAL_FINDINGS: 26

VISUAL_BOARD: USER_ACCEPTED_WORKING_BASELINE
ART_STYLE_DECISION: APPROVED
MODAK_VISUAL_DECISION: APPROVED
SEPARATE_MAIN_MENU: APPROVED
APP_SHELL_VIEW_OVERLAY_MIX: APPROVED
OPEN_VISUAL_DECISIONS: 0

CODEX_IMPLEMENTATION: BLOCKED
```

현행 책임 원본:

- 메인·제품 Shell: `docs/planning/BLACKSMITH_MAIN_MENU_AND_APP_SHELL_CANON_2026.md`
- 그림체·모닥: `docs/planning/BLACKSMITH_ART_STYLE_AND_MODAK_CANON_2026.md`
- 저장소 적대적 감사: `docs/planning/BLACKSMITH_EXISTING_PROJECT_ADVERSARIAL_AUDIT_2026-08-01.md`
- 기계 판독 감사: `docs/planning/data/blacksmith_existing_project_adversarial_audit_2026-08-01.json`
- 비주얼 작업 기준: `docs/planning/data/blacksmith_visual_situation_board_design_v1_2026.json`

## 2. 완료된 주요 기획

- Android 세로형 대장간 제작·강화·장비 생애 RPG
- 단조→강화→멈춤/도전→고객 인계→세계 결과→연대기
- +5/+10 일상 작품 루프와 +50 장기 명작 루프
- 제작 등급 5단계
- 계보 1개 + 보조 최대 2개
- +10·20·30·40 정체성 이정표
- +49→+50 일반 정밀강화·고위 정밀강화 이원화
- 특수재료의 촉매·특수 보조재료 역할
- 고객 4유형과 유형별 복수 이름 고객
- 고객 거래 자격과 공개 적합도 분리
- 장비 소유권·운명·연대기
- 스타일라이즈드 다크 포지
- C안 표정 기반 밝은 불 정령 모닥
- 별도 메인 화면
- 단일 `BlacksmithApp` Shell + View·Overlay 혼합
- 첫 5분 UX·접근성 경계
- 미래 명작 전당 경계
- 벤치마킹 선행 및 승인 결정 즉시 동기화 원칙

## 3. 현재 비주얼 기준안 상태

`BS-VISUAL-20260731-01`은 `USER_ACCEPTED_WORKING_BASELINE`이다.

채택:

- 별도 메인 화면
- 대장간 허브·단조·강화·보관함·결과 화면 구조
- 장비 중심 정보 위계
- 철·황동 UI와 따뜻한 불빛
- 밝은 모닥
- 제품 Shell의 View·Overlay 혼합

최종 시스템으로 승인되지 않은 시안 요소:

- 플레이어 레벨
- 청색 보석·프리미엄 재화
- 업적·상점
- 상세 도감·가이드
- 별도 `특수 제작` 시스템
- 보관함 128/150 수치
- 시장·경기장 직접 탐색
- 시안의 확률·골드·재료 수치

위 요소는 `PLACEHOLDER / NOT_CANON`이며 최종 제품 에셋 제작도 `NOT_RUN`이다.

## 4. 열린 P0 Finding

1. `BS-AUD-F01` — 기본 실행 Scene이 강화 테스트이며 별도 메인 화면이 없음
2. `BS-AUD-F02` — 영속 세이브·이어하기·미확인 결과 복구 없음
3. `BS-AUD-F03` — 강화 테스트·게임 흐름·장비 생애 PoC가 서로 다른 메모리 상태 소유
4. `BS-AUD-F04` — 구형 제작 등급 ID·표시명과 승인 5등급 충돌
5. `BS-AUD-F05` — 구형 3수식어 슬롯·10단위 특수 강화와 최신 계보·보조·+50 이원화 충돌
6. `BS-AUD-F06` — 자동 단조가 정밀·재료·이정표·고위험 선택을 건너뜀
7. `BS-AUD-F07` — 고객·요청·화면이 카일·철검에 하드코딩
8. `BS-AUD-F08` — 운명·관계·세계 결과가 단일 검투사 PoC 모델에 묶임
9. `BS-AUD-F09` — 공통 ResultEnvelope와 비가역 결과 영속 저장 없음
10. `BS-AUD-F10` — 비주얼 시안의 미승인 시스템이 CURRENT처럼 오해될 위험

## 5. 열린 P1 Finding

1. `BS-AUD-F11` — 활성 시작 문서가 PR #35 병합 전 상태를 일부 유지
2. `BS-AUD-F12` — Base v8·v9.1·v9.3 표기가 동시에 활성
3. `BS-AUD-F13` — 주요 UI가 런타임 GDScript 조립이며 공통 Theme·재사용 Scene 경계 없음
4. `BS-AUD-F14` — 고정 폭·오프셋 사용과 제품 안전 영역 처리 부재
5. `BS-AUD-F15` — 시안의 설정 화면과 설정 영속성 미구현
6. `BS-AUD-F16` — Android 일시중지·백그라운드·뒤로가기·중단 복구 미정
7. `BS-AUD-F17` — 6칸 세션 보관함과 최신 작품·소유권·연대기 모델 불일치
8. `BS-AUD-F18` — 일반 판매·방문 상인·이름 고객 채널 미분리
9. `BS-AUD-F19` — 장비별 연대기와 고객별 관계 UI 부족
10. `BS-AUD-F20` — 기존 validator·fixture·테스트가 구형 스키마를 강하게 보호

## 6. 열린 P2 Finding

1. `BS-AUD-F21` — Android 메인 화면의 게임 종료 버튼 정책
2. `BS-AUD-F22` — 시장·경기장 이미지가 직접 탐색·전투로 오해될 위험
3. `BS-AUD-F23` — 모닥의 실제 화면 밝기·크기·모션 검증 미실행
4. `BS-AUD-F24` — 최종 폰트·아이콘·아트 라이선스와 Asset Ledger 미정
5. `BS-AUD-F25` — 핵심 화면 시각 회귀·스크린샷 기준 없음
6. `BS-AUD-F26` — telemetry가 메인·복구·+50·고객 유형·결과 이해도를 포함하지 않음

## 7. 보존할 기존 강점

- 강화 버튼 입력당 결과 1회
- 비용·재료·피로도·납품 원자 거래와 롤백
- 거래·세계 사건 멱등성
- 수동 날짜 진행
- 망치 탭당 피로도 부과 금지
- 색상 외 문구·숫자·원인 표시
- 판매 후 장비 기록 보존
- 720×1280 세로형·Expand 기준
- 접근성 보조가 PERFECT를 자동 제공하지 않는 경계
- 미실행 검사를 PASS로 표시하지 않는 원칙

## 8. 다음 기획 작업

```text
P0-1 세이브·이어하기·ResultEnvelope 계약
→ P0-2 제작 등급·계보·보조·+50 데이터 마이그레이션 계약
→ P0-3 고객 4유형 공통 데이터·화면 계약
→ P0-4 자동 단조 정지 경계
→ P0-5 비주얼 시안 Placeholder 정리
→ P1 Theme·Scene·안전 영역·설정·Android 생명주기
→ 신규 validator·migration·E2E 테스트 계획
→ 적대적 검토 Pass 2
```

## 9. 현재 Gate

```text
STRUCTURAL_GAME_DIRECTION: COMPLETE
USER_VISUAL_DECISIONS_REQUIRED: 0
REPOSITORY_ADVERSARIAL_AUDIT: COMPLETE
AUDIT_FINDINGS: OPEN
P0_FINDINGS: 10
P1_FINDINGS: 10
P2_FINDINGS: 6
FINAL_PRODUCT_ART_ASSETS: NOT_RUN
RUNTIME_VERIFICATION: NOT_RUN
ANDROID_VERIFICATION: NOT_RUN
READY_FOR_USER_기획_완료_DECLARATION: NO_FINDINGS_OPEN
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```
