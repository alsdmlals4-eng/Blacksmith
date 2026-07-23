# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준 |
|---|---|---|
| Intake·Context | PASS | 저장소·플랫폼·핵심 방향·Base 기준 커밋 확인 |
| Definition of Ready | PASS | 강화 실패 정책 단일 정본·의미 검증·기능 보존 범위와 완료 기준 기록 |
| Planning·Approval | PASS | 사용자의 순차 개선·적대적 검토·기획서 동기화·병합 요청 확인 |
| Implementation | PASS | 중복 실패 정책·도달 불가능 위험 데이터 제거, Schema 갱신, 의미·정적 계약 검사 구현 |
| Verification | PASS | Data #352·Godot #310, 데이터 의미·정적 계약·참조 감사·고정 Base 전체 회귀·Godot 파싱·Scene·모델 테스트 통과 |
| Documentation | PASS | Game Bible 재검토, Decision Log·Active Context·Roadmap·Scope·플레이테스트·README 동기화 |
| Integration·Completion | PASS | PR #26 변경 파일 전수 검토·squash 병합·main 커밋 `cce45542f0203d6c0b8dcf13826a5441275e4df5` 재확인 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | PASS | 핵심 약속·플랫폼·시스템 경계 유지 |
| Prototype | CURRENT | 위험·가격 곡선 조정→실제 Godot·Android 확인→첫 판매 구현 |
| Graybox | NOT_STARTED | 고객·상인 판매, 재화·재료 획득, 저장·복귀 연결 |
| First Playable | NOT_STARTED | 20~30분 초기 성장 세션과 실패·복구 흐름 완주 |
| Vertical Slice | NOT_STARTED | 출시 목표 UI 품질·접근성·성능·외부 플레이·AAB 파이프라인 증명 |

## 제작 검증

- [x] 철검 제작 상태 모델
- [x] 터치·자동 작업
- [x] 연속 터치 피버와 작업 배율
- [x] 정밀 마감 ON/OFF
- [x] 완벽·좋음·보통 마감
- [x] 완성 철검 강화 전달
- [x] Godot 헤드리스 파싱·제작 모델 테스트
- [x] 성공한 테스트 러너의 `quit(0)` 뒤 즉시 `return`, 실패 시 `quit(1)` 계약
- [x] 마감 품질의 실제 정수 공격력 20/21/22와 판매 가치 반영
- [x] 원본 공격력·마감·피버·합산 제작 배율의 강화·보관 전달
- [x] 반복 자동 단조의 새 철검 보통 마감·피버 미적용 고정
- [x] 제작 모델 7건·제작 결과 통합 6건·정적 제작 결과 계약 검사
- [x] 피버 1회 이상 공격력 ×1.05·제작 가치 ×1.03
- [x] 반복 발동 비중첩·자동 반복 미적용·강화/보관 전달
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
- [x] 실패 보정
- [x] +11부터 단계 하락 가능
- [x] +30부터 파괴 가능
- [x] 균형·안정·폭주 단조
- [x] 폭주 성공 시 소량 확률 총 2단계 상승
- [x] 폭주 단조의 특수 강화·+9 끝자리 사용 제한
- [x] 최대 6개 무기 보관과 상세 표시
- [x] 실패·확률·위험 수치의 단일 정본을 `enhancement_balance.json`으로 통합
- [x] `enhancement_milestones.json`에서 구형 실패 정책 제거, 수식어 이정표만 유지
- [x] 도달 가능한 위험 decade 0~9만 허용하고 decade 10 제거
- [x] 성공률 패턴·보정·위험 단조성·이정표·재료 효과 의미 검증
- [x] 기존 런타임의 시도 시작 재료 소비·성공 보정 초기화·유지/하락 보정 누적·파괴 종료 정적 계약
- [x] Godot 파싱·Scene 스모크·강화 모델 테스트 PASS 이력
- [ ] +100 실제 수동 완주와 피로도 관찰
- [ ] 확률·효과·가격 곡선 장기 밸런스 검증
- [ ] Android 특수 강화 타이밍·스크롤 검증

## 공유 강화 경제 검증

- [x] 수동·자동 강화가 동일 `WorkshopResources` 인스턴스를 사용
- [x] 일반 강화 시 실제 골드 차감, 재료 미소비
- [x] 수동 특수 강화 시 보조재료·선택 촉매 각각 1개 소비
- [x] 수동 특수 강화의 보조재료 필수 정책
- [x] 촉매 `사용하지 않음` 허용
- [x] 골드 부족 시 무차감·무판정·시도 횟수 불변
- [x] 선택 재료 부족 시 무차감·무판정
- [x] 정밀 판정 중 중복 결제 차단
- [x] 강화 시작 실패 시 골드·재료 복구
- [x] 자동 단조의 빈 보조재료 fallback을 명시적 플래그로 허용
- [x] 정밀 판정 중 사용 재료 기록 보존
- [x] 다음 특수 강화 진입 시 소진 재료를 가용 재료로 UI·세션 동기화
- [x] 공유 경제 단위 테스트 7건 PASS 이력
- [x] 실제 `EnhancementScreen` UI 통합 테스트 2건 PASS 이력
- [x] PR #18 squash 병합 `53cf5edacd5701ec5d412e233d45b35c6e3feb87`와 main 코드 재확인
- [ ] 실제 사람 입력으로 골드·재료 표시 전후 수동 검수

## 자동 단조 검증

- [x] 목표 강화 단계 지정
- [x] 단조 방식 지정
- [x] 특수 강화 보조재료·촉매 지정
- [x] 수동과 동일 거래 경로로 골드·재료 소비
- [x] 지정 재료 부족 시 빈 슬롯 fallback
- [x] 목표 도달 자동 보관
- [x] 보관함이 찰 때까지 반복
- [x] 골드 부족·보관함 가득 참·수동 중지 처리
- [x] 파괴 시 반복 설정에 따른 재시작·종료
- [x] 폭주 도약이 특수 강화 이정표를 건너뛰지 않음
- [ ] 장시간 반복 중 무한 루프·프레임 정지·메모리 증가 실측
- [ ] 재화·재료 경제와 실제 재고 획득 루프 연결
- [ ] 앱 중단·복귀 시 자동 작업 상태 저장 정책
- [ ] 자동 정밀 판정과 수동 플레이 효율 분리

## 개발 도구 연동 검증

- [x] `addons/godot_ai/` 벤더 소스 포함
- [x] `project.godot`에서 Godot AI 에디터 플러그인 활성화
- [x] `_mcp_game_helper` 오토로드 등록
- [x] 운영 감사가 애드온 필수 진입점과 프로젝트 선언을 확인
- [x] 벤더 소스의 upstream 전용 문서·테스트 경로를 프로젝트 로컬 참조에서 분리
- [ ] 로컬 `uv` 설치와 Godot AI MCP 서버 실제 기동
- [ ] Codex 등 MCP 클라이언트 실제 연결·도구 호출

## 운영체계·문서 검증

- [x] Base 기준 커밋 고정
- [x] Base 공식 Linux 운영체계 회귀 테스트 전체 PASS 이력
- [x] Base 텍스트형 파일 223개 전수 스캔
- [x] Base ACTIVE Skill 13개 기능 매핑
- [x] 프로젝트 Skill 3개로 통합하고 Registry Mode 일치
- [x] Work Mode·Skill 자동 라우팅 문서
- [x] Active Context·START_HERE·Documentation Map 상태 동기화
- [x] Design Document Registry JSON·책임 경로·발행 상태 정적 검증
- [x] 문서 로컬 참조·stale 활성 설명 전수 검사
- [x] 프로젝트 문서와 벤더 애드온 upstream 참조의 감사 경계 분리
- [x] 변경 목록 밖의 tests·scripts·scenes 소비자 갱신
- [x] 일회성 Workflow 삭제와 활성 참조 부재 확인
- [x] 감사 보고서 오류 0·경고 0 이력
- [x] 시작 문서·책임 경로의 정적 콜드 스타트 검사
- [x] 운영 감사의 특정 POC 버전 번호 하드코딩 제거
- [x] JSON 파싱 검증을 강화 데이터 의미 검증으로 확대
- [x] 강화 실패 정책 전용 정적 계약 검사와 Data Workflow 연결
- [x] PR #26 GitHub Workflow 최종 실행 완료
- [ ] 새 작업자 또는 별도 AI의 실제 콜드 스타트 재현
- [ ] Branch protection에서 Required Check 강제 여부 확인

## 기능 보존 검증

- [x] 강화 성공률·성장·하락·파괴·수식어 플레이 수치 미변경
- [x] 자동 단조의 재료 소진 fallback 유지
- [x] 직원·무기 수리 제외 결정 유지
- [x] 숨은 무기 후속 기능 보존
- [x] 강화 피버 후속 기능 보존
- [x] 검투사 경기 관람·게임 내 재화 베팅을 후속 기능으로 보존
- [x] 과거 Changelog·Learning Log 보존
- [x] Base 기능 삭제 없이 ADOPT·ADAPT·CONSOLIDATE·ROUTE_ON_DEMAND로 매핑

## 모바일 출시 게이트

- [ ] Godot Android export template 설치
- [ ] OpenJDK 17 및 Android SDK 경로 확인
- [ ] 패키지 ID 확정
- [ ] API 36 이상 대상으로 빌드
- [ ] release keystore 저장소 외부 관리
- [ ] AAB 생성
- [ ] 64비트 ARM 빌드 확인
- [ ] 휴대전화·태블릿·폴더블·노치·안전 영역 검증
- [ ] 터치 대상 크기·텍스트·대비·시간 제한 대안 검수
- [ ] 대표·최악 화면 frame time·메모리·로딩 baseline 측정
- [ ] Google Play 내부 테스트 통과
- [ ] 데이터 안전·콘텐츠 등급·스토어 메타데이터 검토

## 상태 판정

- `PASS`: 요구된 검증을 실제 실행하고 증거가 있음
- `PARTIAL`: 일부만 실행 또는 비차단 미확인 존재
- `FAIL`: 차단 결함·계약 불일치
- `NOT_RUN`: 환경·입력·권한이 없어 실행하지 않음

문서 존재와 실제 실행, Workflow 존재와 Required Check 강제를 구분한다.
