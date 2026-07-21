# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준 |
|---|---|---|
| Intake·Context | PASS | 저장소, 플랫폼, 핵심 방향 확인 |
| Definition of Ready | PASS | MVP-001·MVP-002 목표·범위·제외·완료 기준 기록 |
| Planning·Approval | PASS | 사용자의 진행 승인과 `docs/MVP-001_SCOPE.md`·`docs/MVP-002_SCOPE.md` |
| Implementation | PASS | 제작·강화 모델, 세로형 UI, 타이밍 게이지, 제작→강화 흐름 구현 |
| Verification | CURRENT | 자동 검증 PASS, 실제 화면·Android 실기기 확인 필요 |
| Documentation | PASS | 상태·Roadmap·통합 기획서·테스트 문서 갱신 |
| Integration·Completion | NOT_STARTED | PR 검토·시각/실기기 미검증 확인·병합 필요 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | PASS | 핵심 약속·플랫폼·시스템 경계 확정 |
| Prototype | CURRENT | 제작·+5 수식어·방문 판매 1건 동작과 Android 터치 확인 |
| Graybox | NOT_STARTED | 3개 고객 루프와 저장·복귀 |
| First Playable | NOT_STARTED | 초기 성장 세션 완주 |
| Vertical Slice | NOT_STARTED | Google Play 내부 테스트 AAB |

## MVP-001 제작 검증 체크

- [x] 철검 제작 상태 모델
- [x] 터치당 제작 진행
- [x] 자동 작업
- [x] 연속 터치 피버
- [x] 피버 작업 배율
- [x] 정밀 마감 ON/OFF
- [x] 완벽·좋음·보통 마감 판정
- [x] 다시 제작 초기화
- [x] Godot 프로젝트 헤드리스 파싱
- [x] 제작 모델 테스트 PASS
- [ ] 실제 화면 렌더 시각 검수
- [ ] Android 실기기 터치 검증

## MVP-002 강화 검증 체크

- [x] 철검 +0~+5 강화 상태 모델
- [x] 단계별 기본 성공률
- [x] 보조재료·촉매 선택
- [x] 촉매 성공률 가산
- [x] 정밀 강화 ON/OFF
- [x] GOOD·PERFECT 성공률 가산
- [x] 실패 시 단계 유지·파괴·수리 없음
- [x] 실패당 +5%p, 최대 +20%p 보정
- [x] 성공 시 실패 보정 초기화
- [x] 보조재료 성질 누적
- [x] +5 첫 수식어 생성
- [x] 제작 완료 후 강화 진입과 새 제작 복귀
- [x] 강화 모델 5건 PASS
- [x] Godot 4.7.1 Main Scene·참조 스크립트 파싱 PASS
- [ ] 실제 강화 화면·스크롤·상태 전환 시각 검수
- [ ] Android 실기기 정밀 강화 터치 검증

## 모바일 출시 게이트

- [ ] Godot Android export template 설치
- [ ] OpenJDK 17 및 Android SDK 경로 확인
- [ ] 패키지 ID 확정
- [ ] API 36 이상 대상으로 빌드
- [ ] release keystore를 저장소 밖에서 안전하게 관리
- [ ] AAB 생성
- [ ] 64비트 ARM 빌드 확인
- [ ] 휴대전화·태블릿·폴더블 비율 검증
- [ ] 터치 대상 크기와 안전 영역 검증
- [ ] Google Play 내부 테스트 통과
- [ ] 데이터 안전·콘텐츠 등급·스토어 메타데이터 검토
