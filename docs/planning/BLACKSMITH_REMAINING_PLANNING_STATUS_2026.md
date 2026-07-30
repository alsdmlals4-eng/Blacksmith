# Blacksmith 남은 기획 항목 판정

> 상태: `CURRENT_PLANNING_STATUS`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 구현 권한: `NONE`
>
> 추적 Issue: #79

## 1. 결론

Blacksmith Vertical Slice v9에는 현재 **미해결 구조적 기획안이 없다.**

```text
P0 구조적 차단: 0
P1 핵심 구조 미결정: 0
P2 조정값: 경계가 정의된 상태로 후속 단계 이관
```

따라서 현재 상태는 `사용자 기획 완료 선언 가능 후보`다. 이 문서는 사용자 선언을 대신하지 않는다.

## 2. 완료된 구조적 기획

- 제품 정의·플랫폼·핵심 감정 곡선
- 단조→강화→완성/도전→판매→세계 환류
- +5/+10 일상 루프와 +50 장기 명작 루프
- 제작 등급 5단계
- 계보 1개 + 보조 최대 2개
- 10단위 진입 성공 후 보장 선택
- 일반 강화 확률·보호·저장 경계
- 고객 범주 자격·공개 적합도
- 카시아 대표 세트·에르사 재사용 증명 세트
- 장비 소유권·운명·연대기
- 첫 5분 화면 흐름·접근성
- 명작 전당 검증 랭킹·레거시 전시 경계
- 플레이테스트 Gate
- 벤치마킹 선행 원칙
- 승인 결정 즉시 정본 동기화 원칙

## 3. 남아 있지만 기획 완료를 막지 않는 항목

### 밸런스 조정값

- 제작 등급별 발생 분포·가치 배율
- 계보·보조 수식어의 정확한 효과량
- 후보 생성 가중치
- 고객 가격·관계 변화 수치
- +50 진화별 세부 수치 예산
- 초기 제공 자원량
- 플레이테스트 합격선 재조정

### 콘텐츠 제작값

- 최종 대사와 현지화 템플릿
- +50 특수재료 이름·획득 서사
- 최종 장비명·외형 세부안
- 모닥·카시아·에르사 최종 아트 시트
- 장비 연대기 문장 전체 풀

### 플랫폼·운영값

- 실제 확보 가능한 Android 물리 기기 모델
- 최소 Android 버전·메모리·패키지·발열 목표
- 미래 명작 전당 시즌 길이
- 서버·DB·API·인증 기술
- 개인정보·신고·법무 운영 검토

## 4. 기획이 아니라 남은 절차

- 사용자 `기획 완료` 선언
- 구형 정본 전체 전파와 등록부 정리
- PR #81 병합
- 병합 commit 기준 Sheet `SYNCED_TO_MAIN` 갱신
- 적대적 최종 검수
- 사용자 `검수 완료`
- 별도 Codex Goal·구현 Issue
- 사람·Android·접근성·성능 검증

## 5. 재개방 조건

다음이 발생하면 구조적 기획을 다시 연다.

- 프로젝트 코어 변경
- 새 핵심 시스템 추가
- 장비 정체성·강화·고객 결과 구조 변경
- 주요 UX 흐름 변경
- 서버·경제·저장 경계 변경
- 플레이테스트에서 구조적 실패 발견

재개방 시 `BS-SYNC-20260731-01` 계약과 벤치마킹 선행 원칙을 적용한다.

## 6. 현재 판정

```text
STRUCTURAL_PLANNING_REMAINING: NONE
TUNABLES_REMAINING: YES_WITH_DEFINED_BOUNDARIES
CONTENT_PRODUCTION_REMAINING: YES
PLATFORM_VALIDATION_REMAINING: YES
CANONICAL_PROPAGATION_REMAINING: YES
READY_FOR_USER_기획_완료_DECLARATION: YES
USER_기획_완료: NOT_DECLARED
USER_검수_완료: NOT_DECLARED
CODEX_IMPLEMENTATION: BLOCKED
```