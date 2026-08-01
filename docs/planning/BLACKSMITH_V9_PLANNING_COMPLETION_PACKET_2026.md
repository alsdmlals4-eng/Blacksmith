# Blacksmith v9 기획 완료 후보 패킷

> 상태: `READY_FOR_USER_기획_완료_DECLARATION`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 구현 권한: `NONE`
>
> 추적 Issue: #79
>
> Draft PR: #81

## 1. 판정 목적

Blacksmith Vertical Slice v9의 구조적 기획이 사용자 `기획 완료` 선언을 요청할 수 있는 수준인지 판정한다.

이 문서는 사용자 선언을 대신하지 않는다.

```text
현재 판정
→ 기획 완료 선언 가능 후보

아직 아님
→ 사용자 기획 완료 선언
→ Google Sheet·구형 정본 동기화
→ 적대적 최종 검수
→ 사용자 검수 완료
→ Codex 구현
```

## 2. 책임 문서

| 책임 | 문서 |
|---|---|
| 현행 통합 기획 | `BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md` |
| 사용자 승인 결정 | `BLACKSMITH_V9_USER_DECISION_PACKET.md` |
| 프로젝트 작업 원칙 | `BLACKSMITH_BENCHMARK_FIRST_WORKING_PRINCIPLE.md` |
| 벤치마킹 근거 | `BLACKSMITH_P1_CONTENT_UX_BENCHMARK_AND_DESIGN_2026.md` |
| 구형 정본 정합성 | `BLACKSMITH_P1_CONSISTENCY_AND_ADVERSARIAL_REVIEW_2026.md` |
| 고객·세계 결과 데이터 | `BLACKSMITH_RESULT_AND_CONTENT_DATA_CONTRACT_2026.md` |
| 첫 5분·명작 전당 UX | `BLACKSMITH_FIRST_FIVE_MINUTES_AND_MASTERWORKS_UX_2026.md` |
| 기획 완료 후 전파 | `BLACKSMITH_V9_LEGACY_AND_SHEET_PROPAGATION_PLAN.md` |
| 감사·상태 복원 | `BLACKSMITH_V9_PLANNING_AUDIT_AND_DIRECTION.md` |

## 3. 완료 범위 점검

### 프로젝트 코어

- [x] 한 문장 제품 정의
- [x] 핵심 판매 문장
- [x] 플레이어 약속과 감정 곡선
- [x] 코어·지원·확장·제외 범위 구분
- [x] Android 세로형·오프라인 우선 경계

### 핵심 루프

- [x] 단조 → 강화 → 완성/도전 → 판매 → 세계 환류
- [x] 일상 +5/+10과 장기 +50의 두 시간 지평
- [x] +5 최초 평균 흑자 역할
- [x] +50 진화와 명작 목표
- [x] 15~25분 대표 플레이 순서

### 강화·작품 정체성

- [x] 제작 등급 5단계
- [x] 계보 1개 + 보조 최대 2개
- [x] 10단위 보장 선택 이정표
- [x] +50 진화 후보 3개
- [x] 구형 정밀 등급·A/B 슬롯 대체 판정
- [x] 성공 후 두 번째 실패 판정 금지
- [x] 보호·완전 보호·파괴 책임 경계
- [x] 일반 확률 공개와 원자적 저장

### 고객·세계 환류

- [x] 범주 거래 자격과 공개 적합 신호 분리
- [x] 일반 판매·방문 상인·이름 있는 고객 차이
- [x] 대표 검투사 카시아 벨란
- [x] 수집가 에르사 로엔 증명 세트
- [x] 공통 고객·판매·결과 데이터 계약
- [x] 승리·패배·전시 결과 구조
- [x] 장비 기여 원인과 외부 원인 분리
- [x] 고객 이름 하드코딩 금지

### 장비 생애주기

- [x] 장비 ID·제작자·소유자·운명·연대기
- [x] 판매는 삭제가 아닌 소유권 이전
- [x] 정상·전투 흔적·분실·회수·영구 파괴
- [x] 수치형 내구도·반복 수리 제거
- [x] 파괴 장비 객체와 역사 기록 분리
- [x] 앱 중단·복귀·중복 적용 방지

### 모바일 UX

- [x] 첫 5분 S00~S07 화면 흐름
- [x] 첫 망치·첫 강화 시간 목표
- [x] +5 완성·+10 도전 비교 화면
- [x] 장비 카드·고객 비교·연대기 정보 위계
- [x] 48dp 터치 기준
- [x] 색상·소리·진동·모션 단일 의존 금지
- [x] 길게 누르기 대체 입력
- [x] 숨은 튜토리얼 성공 보정 금지

### 콘텐츠·아트·카피

- [x] 비성장형 불씨 정령 모닥
- [x] 대표 대사·성격·외형 방향
- [x] 카시아·에르사 역할과 가치관
- [x] +50 진화 3종의 시각·가치 방향
- [x] 초기 계보·보조 수식어 풀
- [x] 장비가 화면의 주인공이라는 아트 위계

### 검증·플랫폼

- [x] 결정론적 기능 검증 Gate
- [x] 최소 6명 비유도 테스트
- [x] 수집가 두 번째 파이프라인 검증
- [x] 양방향 회귀
- [x] 저·중·상 Android 기기군 후보
- [x] 성능 저하 시 장식 효과 우선 축소
- [x] 차단 결함 정의

### 미래 서버

- [x] 명작 전당 대상과 목적
- [x] 검증 랭킹·레거시 전시·내 작품 구분
- [x] 등록·실패·해제·신고 흐름
- [x] 공개·비공개 정보 경계
- [x] 파괴 작품 역사 기록 처리
- [x] 플랫폼 숫자 리더보드와 자체 작품 레코드 역할 분리
- [x] 오프라인 작품·로컬 저장 보호
- [x] 성능 보상 없는 명예·감상 중심 원칙

### 운영·전파

- [x] 벤치마킹 선행 원칙
- [x] LIGHT·STANDARD·DEEP 조사 깊이
- [x] 구형 정본 전파 대상
- [x] 문서 등록부·진입점 전파 대상
- [x] Google Sheet 탭별 전파 순서
- [x] Sheet `#ERROR!` 복구 계획
- [x] Codex 최종 단계 차단

## 4. 해결된 구조적 충돌

| 충돌 | 최종 판정 |
|---|---|
| 고객 4명 동시 완주 | 폐기, 카시아 대표 + 에르사 별도 증명 |
| +5/+10과 +50 경쟁 | 일상·장기 두 시간 지평으로 통합 |
| 제작 완성도와 정밀 등급 중복 | 제작 등급 하나로 통합 |
| 수식어 A/B와 계보·보조 중복 | 계보 1 + 보조 2로 대체 |
| 10단위 성공 후 별도 실패 | 금지, 공개 후보 보장 선택 |
| 내구도·DAMAGED·수리 | 제거, 비수치 운명 상태만 사용 |
| 배팅의 대표 흐름 팽창 | 선택적 변형, 필수 완료에서 제외 |
| 수집가 특정 아이템 요구 | 방어구 범주 요청 유지, 대표 작품은 픽스처 |
| 단일 점수 랭킹 | 금지, 작품 메타데이터 비교 |
| 파괴 작품 공개와 복구 혼동 | 아이템 소멸, 역사 기록만 유지 |

## 5. 남은 항목 분류

다음은 구조적 기획 차단 항목이 아니라 구현·밸런스·운영 단계의 조정값이다.

### 밸런스 조정값

- 제작 등급별 발생 분포·가치 배율
- 계보·보조 수식어의 정확한 효과량
- 후보 생성 가중치
- 고객 가격·관계 보정폭
- +50 진화별 정확한 수치 예산
- 초기 자원 수량
- 플레이테스트 합격선 세부 조정

### 콘텐츠 조정값

- +50 특수재료의 최종 이름·획득 서사
- 장비·인물의 최종 대사 문장
- 연대기 현지화 템플릿 전체 세트
- 최종 작품명·장비 외형 세부안
- 모닥·카시아·에르사의 최종 아트 시트

### 플랫폼·운영 조정값

- 실제 확보할 저·중·상 물리 기기 모델
- 최소 Android 버전 최종값
- 메모리·패키지·발열 목표
- 명작 전당 시즌 길이 후보 12주의 최종 채택
- 서버 공급자·DB·API·인증 기술
- 개인정보·신고·운영 정책의 출시 법무 검토

위 항목은 현재 구조를 바꾸지 않는 한 `기획 완료`를 막지 않는다. 새 시스템이나 핵심 규칙 변경이 발생하면 벤치마킹 선행 원칙에 따라 재검토한다.

## 6. 기획 완료 이후 실행 순서

```text
사용자 "기획 완료"
→ PR #81 기획 문서 상태 확정
→ 구형 정본·문서 등록부 정합화
→ main 병합
→ 병합 SHA 기준 Google Sheet 동기화·#ERROR! 수정
→ GitHub·Sheet 상호 검증
→ 적대적 최종 검수·수정
→ 사용자 "검수 완료"
→ 별도 Codex Goal·구현 Issue
```

현재 PR #81을 바로 제품 구현 PR로 사용하지 않는다.

## 7. 최종 Gate

```text
PROJECT_CORE: COMPLETE_FOR_PLANNING
VERTICAL_SLICE_FLOW: COMPLETE_FOR_PLANNING
ENHANCEMENT_AND_IDENTITY: COMPLETE_FOR_PLANNING
CUSTOMER_AND_WORLD_RESULTS: COMPLETE_FOR_PLANNING
FIRST_FIVE_MINUTES_UX: COMPLETE_FOR_PLANNING
ACCESSIBILITY_AND_PERFORMANCE: COMPLETE_FOR_PLANNING
FUTURE_MASTERWORKS_HALL: COMPLETE_FOR_FUTURE_PLANNING
BENCHMARK_FIRST_WORKING_PRINCIPLE: LOCKED
P0_OPEN_FINDINGS: 0
P1_STRUCTURAL_OPEN_FINDINGS: 0
P2_TUNABLES: DEFERRED_WITH_BOUNDARIES
PRODUCT_FILES_CHANGED: NO
GOOGLE_SHEET_SYNC: NOT_RUN
READY_FOR_기획_완료: YES_CANDIDATE_AWAITING_USER_DECLARATION
READY_FOR_검수_완료: NO
CODEX_IMPLEMENTATION: BLOCKED
```
