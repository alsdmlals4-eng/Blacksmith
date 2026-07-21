# Development Gates

## 작업 게이트

| 게이트 | 상태 | 종료 기준·현재 증거 |
|---|---|---|
| Intake·Context | PASS | 저장소·플랫폼·핵심 방향·Base 기준·보호 범위 확인 |
| Definition of Ready | PASS | 제작·강화 POC 범위와 Issue #14 운영 계약 |
| Planning·Approval | PASS | 사용자 직접 지시와 분리된 작업 브랜치 |
| Implementation | PASS | 제작, +100 강화, 위험·가격, 단조 기술, 보관함, 자동 단조 |
| Verification | CURRENT | 자동 검증은 통과 이력, 최신 PR 재실행과 실제 화면·Android 확인 필요 |
| Documentation | CURRENT | POC v0.6.0과 Base 운영체계로 정본 동기화 중 |
| Integration·Completion | NOT_STARTED | PR 전수 검수·CI·사용자 Fetch/Pull/F5 확인 |

## 제품 게이트

| 단계 | 상태 | 다음 Greenlight |
|---|---|---|
| Concept | PASS | 핵심 약속·플랫폼·시스템 경계 확정 |
| Prototype | CURRENT | 제작→강화→보관 자동화의 실제 화면·Android 검증과 방문 판매 1건 |
| Graybox | NOT_STARTED | 판매 2종, 고객 3종 최소 루프, 저장·복귀 |
| First Playable | NOT_STARTED | 20~30분 초기 성장 세션과 경제 |
| Vertical Slice | NOT_STARTED | 출시 목표 UI·대표 고객 루프·AAB 내부 테스트 |

## 제작 POC

- [x] 철검 제작 상태 모델
- [x] 터치·자동 작업
- [x] 연속 터치 피버·작업 배율
- [x] 선택적 정밀 마감
- [x] 완성 철검의 강화 화면 전달
- [x] 제작 모델 4건
- [ ] 실제 화면·손맛 검수
- [ ] Android 터치 검증

## 강화·보관·자동 단조 POC

- [x] +100 일반/특수 강화
- [x] 특수 강화 전용 재료·촉매·정밀 판정
- [x] 복리형 성장·가격·비용
- [x] +11 하락·+30 파괴
- [x] 실패 보정 +4%p·최대 +24%p
- [x] 균형·안정·폭주 단조
- [x] 폭주 8% 총 2단계 도약과 특수 강화 건너뛰기 방지
- [x] +100 수식어 3개 4티어
- [x] 6칸 보관함
- [x] 목표 단계 자동 단조·자동 보관·반복
- [x] 재료 소진 시 빈 슬롯 진행
- [x] 강화 모델 12건
- [ ] 실제 +100 수동 완주·피로 검수
- [ ] 실제 하락·파괴·보호 선택 체감 검수
- [ ] Android 정밀 판정·스크롤 검증

## 운영체계·문서 게이트

- [x] Base 기준 커밋 고정
- [x] 자동 Work Mode·Skill 라우팅 계약
- [x] Design Document Registry·Skill Registry
- [x] 문서 갱신 매트릭스·Handoff·Health Report
- [x] PR 체크리스트·Project Governance
- [ ] Skill Map PDF·Manifest 발행
- [ ] Game Bible PDF 발행
- [ ] Branch protection Required Check 강제 확인

## 모바일 출시 게이트

- [ ] Android export template
- [ ] OpenJDK·Android SDK 경로
- [ ] 패키지 ID
- [ ] API 36 이상
- [ ] 저장소 밖 release keystore
- [ ] AAB·ARM64
- [ ] 휴대전화·태블릿·폴더블
- [ ] 안전 영역·터치 대상·접근성
- [ ] Google Play 내부 테스트
- [ ] 데이터 안전·콘텐츠 등급·스토어 메타데이터
