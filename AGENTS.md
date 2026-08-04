# Blacksmith AI 작업 규칙

Blacksmith는 Android 세로형 Godot 제작 게임 프로젝트다. 현재 단계는 제품 구현이 아니라 `TOTAL_PLANNING / R2_BATCH_004`이며 제품 구현은 `BLOCKED`다.

## 1. 권위 순서

1. 사용자의 최신 지시와 승인
2. `AGENTS.md`
3. `CURRENT_CONFIRMED_DECISIONS.md`
4. `docs/planning/CURRENT_R2_CANON_REGISTRY.json`
5. `docs/planning/BLACKSMITH_CURRENT_GAME_BIBLE_R2_2026.md`
6. Active Context·Roadmap·Development Gates
7. 실제 코드·data·Scene·tests
8. Google Sheet와 파생 문서
9. 외부 벤치마크·과거 대화·AI 추론

GitHub가 기획 정본이다. Google Sheet는 같은 Decision ID·경로·Commit·검증 상태를 연결한다.

## 2. 필수 작업 순서

```text
현재 권위·변경 경계 확인
→ 벤치마킹·현업 비교
→ brainstorming·적대적 검토
→ RED: 실패 계약 테스트 작성·의도한 실패 관측
→ GREEN: 최소 정본·구현 변경
→ REFACTOR: 중복·구형 참조 정리
→ exact-head 전체 검증
→ GitHub·Sheet readback
→ 명시적 사용자 승인 뒤 병합
```

### 벤치마킹·현업 비교

질문·추천·새 시스템 설계 전에 관련 현업 사례와 유사 게임을 비교한다.

- `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`을 기록한다.
- 유명 사례라도 프로젝트 코어와 충돌하면 비채택한다.
- 출처와 확인 날짜를 PR 또는 정본에 남긴다.
- 표면 기능이 아니라 플레이어 판단·정보 구조·제작 비용을 비교한다.

### 작업마다 TDD

모든 기능·규칙·계약·버그 수정은 TDD를 사용한다.

```text
RED → GREEN → REFACTOR
```

- 테스트를 먼저 작성한다.
- 의도한 이유로 실패하는 RED를 실제 관측한다.
- 최소 변경으로 GREEN을 만든다.
- GREEN 이후에만 정리한다.
- RED와 GREEN 증거 없이 PASS 또는 완료를 주장하지 않는다.
- 문서·기획 변경도 기계 판독 계약 테스트로 보호한다.

## 3. 승인 배치와 조기 체크포인트

- 승인 10건은 **최대 배치 크기**다.
- 기본적으로 Draft PR에 승인 Decision을 누적한다.
- 다음 조건이면 10건 전에도 조기 체크포인트를 허용한다.
  - `HIGH_RISK_CONFLICT`: 기존 핵심 규칙과 고위험 충돌
  - `SESSION_END`: 세션 종료로 정본 유실 위험
  - `LARGE_CANON_IMPACT`: 다수 권위 문서·Registry·후속 설계에 큰 영향
- 조기 체크포인트도 적대적 감사·changed files·리뷰·CI·Sheet readback을 생략하지 않는다.
- 병합에는 명시적 사용자 승인이 필요하다.
- 병합 뒤 main SHA와 Sheet를 다시 읽어 최종 동기화한다.

## 4. 현재 코어 보호

- 강화 성공·실패와 멈춤·추가 도전이 즉각 반복 재미다.
- 작품은 UID·소유·손상·복원·사건·연대기를 유지한다.
- 일반 강화는 한 입력에 한 결과다.
- 정밀강화는 주재료 맥락 + 강화 방식 + 촉매 한 개다.
- 수식어는 `GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX` 세 슬롯이다.
- 제작 등급은 `보통 / 우수 / 명품 / 걸작 / 전설` 다섯 단계의 출생 완성도다.
- 예술성은 단계명이 없는 `1~10` 숫자형 무기·작품 능력치다.
- 예술성은 전투력을 기본적으로 올리지 않는다.
- 보조재료 슬롯과 일반 수식어 A·B는 재도입하지 않는다.

## 5. 보호 경로

기획 승인 전 변경 금지:

```text
data/
scripts/
scenes/
assets/
addons/
project.godot
```

제품 구현은 R1~R8와 최종 사용자 검수 및 별도 Codex Gate 전까지 `BLOCKED`다.

## 6. 정본·구형 문서

- 한 질문에는 활성 책임 원본 하나만 둔다.
- `[대체됨] / [부분 대체됨] / [보류] / [폐기] / [역사 증거]`를 직접 표시한다.
- 과거 PASS는 해당 과거 HEAD의 증거일 뿐 현재 제품 PASS가 아니다.
- PR #81은 `REFERENCE_ONLY / DO_NOT_MERGE_AS_UNIT`이다.

## 7. 완료 증거

- expected/exact HEAD 고정
- Base adoption
- Python contracts
- Godot headless
- 변경 파일·보호 경로
- PR 댓글·인라인 스레드
- Google Sheet same-ID readback
- 미실행 runtime·Android·접근성·성능·사람 플레이는 `NOT_RUN`
