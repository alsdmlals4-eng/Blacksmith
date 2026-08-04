# [현재 정본] Blacksmith 체크포인트 003 이후 정본 적대적 검토

- 운영 Decision ID: `BS-OPS-20260804-02`
- Audit ID: `BS-ADV-20260804-01`
- 상태: `COMPLETED_WITH_OPEN_USER_DECISIONS`
- 기준 main: `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`
- R2 체크포인트 003: PR `#103/#104`
- 제품 구현: `BLOCKED`

## 1. 감사 목적

- 승인·병합된 기획을 현재 정본으로 확정
- 핵심 재미와 실제 구성의 정합성 적대적 재검토
- 충돌·누락·구형 반대 서술 차단
- 구형 문서에 `[부분 대체됨]`, `[대체됨]`, `[보류]`, `[폐기]`, `[역사 증거]` 표시
- 새로운 게임 규칙은 사용자 승인 전 `PROPOSED_ONLY`로 격리

## 2. 현재 정본 구조

```text
직접 제작
→ 제작 등급과 고정 등급 수식어
→ 일반 강화의 성공·실패와 멈춤·추가 도전
→ +10/+20/+30/+40/+50 정밀강화
→ 강화 방식으로 세부 수치 방향 선택
→ 촉매 이력으로 촉매 수식어 생성·성장·분기·변형
→ 고객·사건·손상·복원·소유 이력으로 연대기 수식어 생성·진화
→ [등급] 촉매 수식어 기본 작품명 - 연대기 수식어
→ 작품을 고객과 세계에 보냄
→ 같은 UID 작품의 결과·재방문·복원·계승
→ 다음 강화·복원·제작 판단
```

현재 수식어 슬롯:

```text
GRADE_AFFIX / CATALYST_AFFIX / CHRONICLE_AFFIX
```

구형 `일반 수식어 A·B + 사건 수식어`, 보조재료 슬롯, 제작 시 모든 수식어가 비어 있다는 해석은 현재 정본이 아니다.

## 3. 근본 원인

### RC-01 — 자기 자신의 미래 main SHA를 예측하는 Registry

PR #104 병합 전 Registry가 `current_main`과 `closure pending`을 저장했다. PR #104 병합 자체가 main을 이동시키므로 문서가 즉시 오래된 상태가 됐다.

해결:

- 변동하는 `current_main` 필드 제거
- 불변 증거인 PR 번호·exact HEAD·merge SHA·readback 상태 분리
- 브랜치 문서가 자기 자신의 미래 merge SHA를 예측하지 않음

### RC-02 — R1→R2 supersession 전파 누락

R2에서 세 수식어·보조재료 제거·일정 유형 분리를 승인했지만 Game Bible·Roadmap·Development Gates·R1 Registry·Authority Index에 구형 구조가 남았다.

해결:

- 현행 R2 Game Bible 신규 생성
- 기존 R1 Game Bible은 `[부분 대체됨]` 진입점으로 전환
- Roadmap·Gates·R1/R2 Registry·Authority Index 동기화
- 구형 고위험 문서 직접 상태 표시

### RC-03 — PR #81의 참고 자산과 현재 정본 경계 부족

PR #81은 181개 커밋·88개 파일의 고유 자료를 보존하지만 최신 정본과 충돌하는 규칙도 포함한다.

해결:

```text
전체 병합 단위: [폐기]
브랜치·원 승인 원문: [역사 증거]
분야별 선별 이관: [보류]
```

제목과 본문에 `REFERENCE ONLY / DO NOT MERGE`를 직접 표시했다.

## 4. 감사 결과

```text
CORE_FUN_DIRECTION: VALID
STRUCTURAL_ALIGNMENT: VALID_AFTER_AUTHORITY_REPAIR
P0: 0
P1_FOUND: 7
P1_DOCUMENT_AUTHORITY_RESOLVED: 6
P1_USER_DECISION_OPEN: 1
P2_OPEN: 7
PRODUCT_IMPLEMENTATION: BLOCKED
```

### P0

`0건`.

- 제품 코드·Scene·runtime data·asset 변경 없음
- 승인된 3수식어 구조 자체의 차단 모순 없음
- PR #103/#104 exact-head 검증 뒤 squash 병합 완료

### 해결된 P1 — 6건

1. R2 Registry의 closure 대기·이전 main SHA 드리프트
2. Game Bible의 A/B 수식어·보조재료·구형 정밀강화
3. Roadmap의 R3/R6/R7 구형 행동 증거
4. Development Gates의 A/B·구형 일정 Gate
5. R1 Registry의 현재 R2 계약 오인 가능성
6. Authority Index의 `수식어 2개` 최신 안내

### 열린 P1 — 사용자 Decision 필요

**제작 등급 수식어와 예술성 시각 단계의 한국어 명칭 충돌**.

장비명 예시의 `[명품]`과 예술성 시각 단계의 `명품 6~8`이 같은 단어를 다른 축에 사용한다. 구조는 분리돼 있지만 플레이어는 혼동할 수 있으므로 별도 Decision이 필요하다.

### 열린 P2 — 7건

1. 연대기 수식어 효과 책임 경계
2. 작품 판매·증여·복원·상속 소유권 상태 머신
3. 모바일 긴 조합 장비명 표시
4. 첫 작품의 촉매·연대기 정체성 보상 시점
5. 완전 파괴와 작품 애착의 정합성
6. 성공률 공개가 수치 최적화로 수렴하는 위험
7. PR #81 분야별 선별 이관

## 5. 핵심 재미 정합성

### 강점

- **즉각 재미:** 강화 성공·실패와 멈춤·추가 도전이 짧은 주기로 반복된다.
- **제작자 선택:** 강화 방식과 촉매 이력이 작품에 플레이어 의도를 남긴다.
- **작품 정체성:** 등급·촉매·연대기가 출생, 제작자 선택, 실제 생애를 각각 설명한다.
- **장기 의미:** 고객과 세계에 보낸 동일 UID 작품이 결과와 다음 제작 이유를 돌려준다.
- **모바일 적합성:** 일반 강화는 한 입력 한 결과이고 정밀강화만 고밀도 선택을 요구한다.
- **콘텐츠 확장성:** 검투사·모험가·군인·귀족이 같은 작품 생애 파이프라인을 공유한다.

### 위험

- 세 수식어가 실제 다음 판단을 만들지 못하면 설명용 장식이 된다.
- 성공률 공개가 너무 정확하면 작품 생애보다 수치 최적화가 우선한다.
- 일정·연대기 알림이 강화 리듬을 자주 끊으면 메인 반복 재미가 분산된다.
- 예술성·제작 등급·세 수식어를 같은 화면에 위계 없이 노출하면 인지 부하가 커진다.
- 첫 작품에서 촉매·연대기 보상이 너무 늦으면 장기 정체성의 매력을 체감하기 전에 이탈할 수 있다.

판정: **핵심 재미 방향은 유효하다.** 다만 열린 P1/P2는 R2~R6에서 검증·승인해야 한다.

## 6. 개선 제안 — 아직 정본 아님

`PROPOSED_ONLY / USER_REVIEW_REQUIRED`.

### 제안 A — 표시 어휘 분리

- 제작 등급 수식어: `[표준] / [우수] / [완벽]` 계열
- 예술성 시각 단계: `기본 / 세련 / 거장 / 걸작` 계열

같은 `명품`을 두 축에 중복 사용하지 않는다. 정확한 라벨은 후속 Decision에서 확정한다.

### 제안 B — 연대기 효과 책임 제한

기본 영향 범위 권장:

- 고객·세력 선호와 대화
- 감정 가치·감정가·전시·선물·상속 가치
- 관련 사건의 추가 선택지

기본 전투 수치 직접 상승은 예외 콘텐츠 Gate로 제한해 촉매 수식어의 실용 성능 책임을 보호한다.

### 제안 C — 작품 소유권 상태 머신

```text
PLAYER_OWNED
→ SOLD_OR_GIFTED
→ TEMPORARILY_RETURNED_FOR_SERVICE
→ RETURNED_TO_OWNER
→ INHERITED_OR_LOST
```

복원 의뢰의 임시 회수와 영구 재소유를 분리해 중복 판매·소유권 복제·UID 충돌을 방지한다.

### 제안 D — 첫 작품 정체성 보상 시점

- 제작 완료: 등급 수식어 즉시 획득
- 첫 정밀강화: 촉매 계보 방향 체감
- 첫 고객 결과: 연대기 수식어 형성 가능성 예고

실제 생성 보장·확률은 사람 플레이 뒤 결정한다.

## 7. 문서 상태 정책

| 표시 | 의미 |
|---|---|
| `[현재 정본]` | 현재 구현·후속 기획의 직접 기준 |
| `[부분 대체됨]` | 일부 원칙은 유지되나 명시 범위는 최신 정본 우선 |
| `[대체됨]` | 최신 정본이 같은 책임을 완전히 인수 |
| `[보류]` | 승인·채택 전 참고만 가능 |
| `[폐기]` | 재사용 금지 |
| `[역사 증거]` | 당시 구현·검증·승인 과정 보존용 |

기계 판독 원장:

- `docs/planning/BLACKSMITH_LEGACY_DOCUMENT_STATUS_REGISTRY_2026.json`

## 8. 직접 표시 완료 문서

- R1 Game Bible — `[부분 대체됨]`
- Precision Enhancement Baseline — `[대체됨]`
- Core Resolution 02 — `[대체됨]`
- Core Resolution 03 — `[부분 대체됨]`
- Master Game Design Planning — `[부분 대체됨]`
- Growth System Planning — `[부분 대체됨]`
- MVP-003 Scope — `[역사 증거] [보류]`
- Final Adversarial Review Report — `[대체됨]`
- Project Core Review Report — `[대체됨]`
- Equipment Lifecycle PoC Spec — `[역사 증거] [보류]`

원문은 기준 main `d6fd9fc8ce6177c0b4ea0c41e1d9f4213c5726a9`의 Git 이력으로 보존된다.

## 9. PR #81 처리

- 제목: `[REFERENCE ONLY · DO NOT MERGE]`
- 전체 병합: `[폐기]`
- 원 승인·고유 자료: `[역사 증거]`
- Save·migration·자동화·고객·UI·검증·비주얼 선별 이관: `[보류]`

최신 main에서 시작한 소형 분야별 PR만 허용한다.

## 10. 검증 계약

- Current Decisions·R2 Registry·R2 Game Bible에서 A/B 수식어·보조재료·2슬롯을 현재형으로 서술하지 않음
- 구형 파일은 첫 화면에 상태와 대체 문서를 표시
- R1 Registry는 역사적 승인 증거로 분류
- PR #81 전체 병합 금지
- 역사 PoC PASS를 최신 제품 PASS로 해석 금지
- 제품 경로 변경 `0`
- 자동 검증 결과는 PR exact-head 증거로 기록하며 문서가 미래 merge SHA를 예측하지 않음

## 11. 다음 Decision 후보

1. 제작 등급 수식어와 예술성 단계 명칭 분리
2. 연대기 수식어 효과 책임
3. 작품 소유권 상태 머신
4. 모바일 장비명 표시 계약
5. 첫 작품 정체성 보상 시점
6. 완전 파괴와 작품 애착 검증
7. PR #81 선별 이관 순서

제품 구현은 계속 `BLOCKED`다.
