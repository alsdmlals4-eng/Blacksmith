# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준 |
|---|---|---|
| Intake·Context | PASS | 저장소·플랫폼·핵심 방향·Base 기준 커밋 확인 |
| Definition of Ready | PASS | 제작·강화·보관·자동 단조의 목표·제외·완료 기준 기록 |
| Planning·Approval | PASS | 사용자의 직접 구현 승인과 영향 범위 확인 |
| Implementation | PASS | 제작, +100 강화, 위험 결과, 단조 방식, 보관함, 자동 단조 구현 |
| Verification | CURRENT | 자동 검증 PASS 이력, 최신 PR 검증과 실제 Godot·Android 수동 확인 필요 |
| Documentation | CURRENT | Base 운영체계·현재 상태·Roadmap·Registry 최신화 진행 |
| Integration·Completion | NOT_STARTED | PR 적대적 검토·Required Checks·병합·main 재확인 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | PASS | 핵심 약속·플랫폼·시스템 경계 유지 |
| Prototype | CURRENT | 제작→강화→보관→자동 반복을 실제 Godot·Android에서 확인하고 첫 판매 구현 |
| Graybox | NOT_STARTED | 고객·상인 판매, 재화·재료 재고, 저장·복귀 연결 |
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
- [x] Godot 파싱·Scene 스모크·강화 모델 테스트 PASS 이력
- [ ] +100 실제 수동 완주와 피로도 관찰
- [ ] 확률·효과·가격 곡선 장기 밸런스 검증
- [ ] Android 특수 강화 타이밍·스크롤 검증

## 자동 단조 검증

- [x] 목표 강화 단계 지정
- [x] 단조 방식 지정
- [x] 특수 강화 보조재료·촉매 지정
- [x] 골드·재료 소비
- [x] 지정 재료 부족 시 해당 재료 없이 진행
- [x] 목표 도달 자동 보관
- [x] 보관함이 찰 때까지 반복
- [x] 골드 부족·보관함 가득 참·수동 중지 처리
- [x] 파괴 시 반복 설정에 따른 재시작·종료
- [x] 폭주 도약이 특수 강화 이정표를 건너뛰지 않음
- [ ] 장시간 반복 중 무한 루프·프레임 정지·메모리 증가 실측
- [ ] 재화·재료 경제와 실제 재고 획득 루프 연결
- [ ] 앱 중단·복귀 시 자동 작업 상태 저장 정책

## 운영체계·문서 검증

- [x] Base 기준 커밋 고정
- [x] Work Mode·Skill 자동 라우팅 문서
- [x] Skill Registry 자동 trigger 정책
- [x] 프로젝트 Skill 입력·출력·실패·검증 계약
- [x] Active Context·START_HERE·Documentation Map 상태 동기화
- [x] Base 적용 감사표와 보존·제외 사유
- [ ] Design Document Registry Schema·발행 정책 검증
- [ ] 문서 로컬 참조 전수 검사
- [ ] 새 작업자 콜드 스타트 재현
- [ ] GitHub Workflow와 Required Check 강제 여부 확인

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
