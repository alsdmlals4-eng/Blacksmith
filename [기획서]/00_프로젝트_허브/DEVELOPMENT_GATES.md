# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준 |
|---|---|---|
| Intake·Context | PASS | 저장소·플랫폼·핵심 방향·Base 기준 커밋 확인 |
| Definition of Ready | PASS | 강화 실패 정책 단일 정본·의미 검증·기능 보존 범위와 완료 기준 기록 |
| Planning·Approval | PASS | 사용자의 순차 개선·적대적 검토·기획서 동기화·병합 요청 확인 |
| Implementation | PASS | 중복 실패 정책·도달 불가능 위험 데이터 제거, Schema 갱신, 의미·정적 계약 검사 구현 |
| Verification | PASS | Data #352·Godot #310, 데이터 의미·정적 계약·참조 감사·고정 Base 회귀·Godot 파싱·Scene·모델 테스트 통과 이력 |
| Documentation | PASS | Game Bible 재검토, Decision Log·Active Context·Roadmap·Scope·플레이테스트·README 동기화 |
| Integration·Completion | PASS | PR #26 변경 파일 전수 검토·squash 병합·main 커밋 `cce45542f0203d6c0b8dcf13826a5441275e4df5` 재확인 |
| Operating canonical recovery | PASS | PR #31 충돌 정본 복구, 제품 코드·데이터 비변경, Data #362·Godot #316 성공 |
| Base 25-skill resync | IN_REVIEW | 최신 Base 고정·25개 기능 매핑·Skill/Registry/문서 동기화·전체 회귀 결과 확인 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | PASS | 핵심 약속·플랫폼·시스템 경계 유지 |
| Prototype | CURRENT | 위험·가격 곡선 후보 비교→실제 Godot·Android 확인→첫 판매 구현 |
| Graybox | NOT_STARTED | 고객·상인 판매, 재화·재료 획득, 저장·복귀 연결 |
| First Playable | NOT_STARTED | 20~30분 초기 성장 세션과 실패·복구 흐름 완주 |
| Vertical Slice | NOT_STARTED | 출시 목표 UI 품질·접근성·성능·외부 플레이·AAB 파이프라인 증명 |

## 위험·가격 곡선 시뮬레이션 게이트

| 단계 | 상태 | 종료 기준 |
|---|---|---|
| Scope·Routing | PASS | `balance-simulation` Mode·trigger·Work Mode·Base profile·Design Registry·Scope 일치 |
| Simulator implementation | PASS | JSON 정본과 `EnhancementSession` 판정 순서를 재현하고 고정 반례 통과 |
| Baseline distribution | PASS | +10·+30·+50·+70·+100 × 균형·안정·폭주 15개 조합 × 1,000회 결과 생성 |
| Candidate tuning | NOT_STARTED | 한 변수군만 변경하고 동일 시드 기준선과 비교해 `KEEP / TUNE / REJECT / TEST_IN_PLAY` 판정 |
| Automatic repeat·bottleneck | NOT_RUN | 자동 반복·재료 부족·골드 부족·보관함 중지·파괴 후 재시작 분포 생성 |
| Runtime parity | NOT_RUN | 실제 Godot 난수 시퀀스와 시뮬레이터 결정 순서 대조 |
| Regression | PARTIAL | 기준선 시뮬레이터 계약은 검증됐으며 최신 Base 25개 회귀는 PR #32 실행 결과 대기 |
| Human play evidence | NOT_RUN | +100 손실 피로·수동/자동 효율·보상 체감을 실제 플레이에서 확인 |

기준선 실행 완료는 후보 수치 승인, 실제 손맛, Android 성능 PASS를 의미하지 않는다.

## 제작 검증

- [x] 철검 제작 상태 모델
- [x] 터치·자동 작업
- [x] 연속 터치 피버와 작업 배율
- [x] 정밀 마감 ON/OFF
- [x] 완벽·좋음·보통 마감
- [x] 완성 철검 강화 전달
- [x] Godot 헤드리스 파싱·제작 모델 테스트
- [x] 성공 테스트 러너의 `quit(0)` 뒤 즉시 `return`, 실패 시 `quit(1)` 계약
- [x] 마감 품질의 실제 정수 공격력 20/21/22와 판매 가치 반영
- [x] 원본 공격력·마감·피버·합산 제작 배율의 강화·보관 전달
- [x] 반복 자동 단조의 새 철검 보통 마감·피버 미적용 고정
- [x] 제작 모델 7건·제작 결과 통합 6건·정적 제작 결과 계약 검사
- [x] 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03, 반복 발동 비중첩
- [ ] 실제 화면 전후 렌더 시각 검수
- [ ] Android 실제 기기 터치·세로 비율 검증

## 강화·보관 검증

- [x] 최대 +100
- [x] 일반 강화와 +10 단위 특수 강화 분리
- [x] 특수 강화에서만 보조재료·촉매·정밀 판정 적용
- [x] 일반 강화에 이전 재료·촉매 효과 비누출
- [x] 현재 공격력 기반 점진 성장
- [x] 다음 공격력·판매가·비용·확률 표시
- [x] +10~+100 수식어 추가·티어 성장
- [x] 실패 보정, +11 하락, +30 파괴
- [x] 균형·안정·폭주 단조와 폭주 이정표 차단
- [x] 최대 6개 무기 보관과 상세 표시
- [x] 실패·확률·위험 수치의 단일 정본 `enhancement_balance.json`
- [x] `enhancement_milestones.json`은 수식어 이정표만 유지
- [x] 도달 가능한 위험 decade 0~9와 데이터 의미 검증
- [x] Godot 파싱·Scene 스모크·강화 모델 테스트 PASS 이력
- [ ] +100 실제 수동 완주와 피로도 관찰
- [ ] 확률·효과·가격 곡선 장기 밸런스 검증
- [ ] Android 특수 강화 타이밍·스크롤 검증

## 공유 강화 경제 검증

- [x] 수동·자동 강화가 동일 `WorkshopResources` 사용
- [x] 일반 강화 골드 차감·재료 미소비
- [x] 수동 특수 강화 보조재료·선택 촉매 소비
- [x] 골드·선택 재료 부족 시 무차감·무판정
- [x] 정밀 판정 중 중복 결제 차단과 시작 실패 복구
- [x] 자동 단조 빈 보조재료 fallback
- [x] 다음 특수 강화 진입 시 소진 재료 UI·세션 동기화
- [x] 공유 경제 단위 7건·실제 UI 통합 2건 PASS 이력
- [ ] 실제 사람 입력의 골드·재료 표시 전후 검수

## 자동 단조 검증

- [x] 목표 단계·단조 방식·특수 재료 지정
- [x] 수동과 동일 거래 경로로 골드·재료 소비
- [x] 지정 재료 부족 시 빈 슬롯 fallback
- [x] 목표 도달 자동 보관과 보관함 반복
- [x] 골드 부족·보관함 가득 참·수동 중지
- [x] 파괴 시 반복 설정에 따른 재시작·종료
- [x] 폭주 도약의 특수 강화 이정표 차단
- [ ] 장시간 반복 중 무한 루프·프레임 정지·메모리 증가 실측
- [ ] 재화·재료 경제와 실제 획득 루프 연결
- [ ] 앱 중단·복귀 시 자동 작업 상태 저장 정책
- [ ] 자동 정밀 판정과 수동 플레이 효율 분리

## 위험·가격 곡선 시뮬레이션 검증

- [x] 범위·입력·지표·판정 계약 등록
- [x] 고정 roll 반례: 유지·보정·하락·파괴·폭주 차단·특수 비용·판매가
- [x] 15개 기준선 조합 × 1,000회 실행
- [x] 입력 커밋·JSON SHA-256·시드·난수 방식 기록
- [x] 기준선 결과를 `KEEP / TUNE 후보 / TEST_IN_PLAY`으로 분리
- [ ] 한 변수군 후보안의 동일 시드 비교
- [ ] 자동 반복·자원 병목·보관함 중지·파괴 후 재시작 분포
- [ ] 실제 Godot 난수 시퀀스 대조
- [ ] 실제 +100 손실 피로·Android·장시간 자동 단조 체감

## 개발 도구 연동 검증

- [x] `addons/godot_ai/` 벤더 소스 포함
- [x] Godot AI 에디터 플러그인과 `_mcp_game_helper` 등록
- [x] 운영 감사가 필수 진입점과 프로젝트 선언 확인
- [x] 벤더 upstream 참조와 프로젝트 로컬 참조 경계 분리
- [ ] 로컬 `uv`와 Godot AI MCP 서버 실제 기동
- [ ] Codex 등 MCP 클라이언트 실제 연결·도구 호출

## 운영체계·문서 검증

- [x] Base 기준 커밋 `41a20584dd2ee51d917e5c9d7cab6838e1ceba7e` 고정
- [x] Base ACTIVE Skill 25개 Profile 매핑
- [x] 프로젝트 Skill 3개 유지와 Registry Mode 일치
- [x] Work Mode·Skill 자동 라우팅 문서
- [x] Active Context·START_HERE·Documentation Map 연결
- [x] Design Document Registry에서 분석 Scope·Report 책임 분리
- [x] 문서 로컬 참조·stale 활성 설명 감사 계약
- [x] 미해결 Git 충돌 블록 전수 검사와 회귀 테스트
- [x] 프로젝트 문서와 벤더 upstream 참조 감사 경계 분리
- [x] 강화 실패 정책·밸런스 시뮬레이터 정적 계약과 Workflow 연결
- [ ] 최신 Base 25개 전체 회귀 Workflow 최종 결과
- [ ] 새 작업자 또는 별도 AI의 실제 콜드 스타트 재현
- [ ] Branch protection에서 Required Check 강제 여부 확인

## 기능 보존 검증

- [x] 강화 성공률·성장·하락·파괴·수식어 플레이 수치 미변경
- [x] 자동 단조 재료 소진 fallback 유지
- [x] 직원·무기 수리 제외 결정 유지
- [x] 숨은 무기·강화 피버 후속 기능 보존
- [x] 검투사 경기 관람·게임 내 재화 베팅 후속 기능 보존
- [x] 과거 Changelog·Learning Log 보존
- [x] Base 기능 삭제 없이 ADOPT·ADAPT·CONSOLIDATE·ROUTE_ON_DEMAND로 매핑

## 모바일 출시 게이트

- [ ] Godot Android export template 설치
- [ ] OpenJDK 17 및 Android SDK 경로 확인
- [ ] 패키지 ID 확정
- [ ] API 36 이상 AAB·64비트 ARM 빌드
- [ ] release keystore 저장소 외부 관리
- [ ] 휴대전화·태블릿·폴더블·노치·안전 영역 검증
- [ ] 터치 대상·텍스트·대비·시간 제한 대안 검수
- [ ] 대표·최악 화면 frame time·메모리·로딩 baseline
- [ ] Google Play 내부 테스트·데이터 안전·콘텐츠 등급·스토어 메타데이터 검토

## 상태 판정

- `PASS`: 요구된 검증을 실제 실행하고 증거가 있음
- `PARTIAL`: 일부만 실행 또는 비차단 미확인 존재
- `FAIL`: 차단 결함·계약 불일치
- `NOT_RUN`: 환경·입력·권한이 없어 실행하지 않음
- `READY`: 범위·입력·종료 기준은 준비됐으나 실행 증거는 아직 없음
- `IN_REVIEW`: 변경은 반영됐으나 PR 검증·검토가 완료되지 않음

문서 존재와 실제 실행, Workflow 존재와 실행 성공, Required Check 강제를 각각 구분한다.
