# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준 |
|---|---|---|
| Intake·Context | PASS | 저장소, 플랫폼, 핵심 방향 확인 |
| Definition of Ready | PARTIAL | 초기 구조 범위는 준비됐으나 MVP 수치 미확정 |
| Planning·Approval | CURRENT | 모바일 구조와 책임 원본 설치 |
| Implementation | NOT_STARTED | 실제 핵심 루프 미구현 |
| Verification | NOT_STARTED | Godot·Android 실행 미검증 |
| Documentation | IN_PROGRESS | Markdown·JSON 설치 중 |
| Integration·Completion | NOT_STARTED | PR 검토·병합 필요 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | CURRENT | 핵심 수직 프로토타입 범위 승인 |
| Prototype | NOT_STARTED | 제작·피버·마감·+5 수식어·판매 1건 동작 |
| Graybox | NOT_STARTED | 3개 고객 루프와 저장·복귀 |
| First Playable | NOT_STARTED | 초기 성장 세션 완주 |
| Vertical Slice | NOT_STARTED | Google Play 내부 테스트 AAB |

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
