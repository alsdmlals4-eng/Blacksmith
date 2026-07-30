# Blacksmith v9 구형 정본·Google Sheet 전파 계획

> 상태: `PLANNED / BLOCKED_UNTIL_기획_완료`
>
> 기준일: `2026-07-31`
>
> Work Mode: `PLAN`
>
> 실행 권한: `NONE`
>
> 추적 Issue: #79

## 1. 목적

사용자 `기획 완료` 이후 현행 마스터 v9 결정을 구형 기획 문서, 문서 등록부, Google Sheet에 누락 없이 전파하기 위한 순서와 검증 기준을 정의한다.

현재 단계에서는 실제 문서·Sheet 동기화를 실행하지 않는다.

## 2. 실행 Gate

```text
현재 마스터 v9 상세 기획 완료
→ 사용자 "기획 완료"
→ 이 전파 계획 실행 승인
→ GitHub 구형 정본 정합화 PR
→ PR 검증·병합
→ 병합된 main 기준 Google Sheet 동기화
→ Sheet 재조회·오류 검사
→ 적대적 최종 검수
→ 사용자 "검수 완료"
→ 마지막 단계에서 Codex 구현
```

금지:

- 기획 완료 전 구형 정본을 현행인 것처럼 대량 수정
- 병합 전 Sheet를 미래 문서 상태로 먼저 변경
- 제품 코드·게임 데이터와 함께 섞어서 전파
- Codex 구현 Issue를 동시에 생성

## 3. 책임 원본

전파 기준:

1. `BLACKSMITH_VERTICAL_SLICE_MASTER_V9_DRAFT.md`
2. `BLACKSMITH_V9_USER_DECISION_PACKET.md`
3. `BLACKSMITH_P1_CONSISTENCY_AND_ADVERSARIAL_REVIEW_2026.md`
4. `BLACKSMITH_RESULT_AND_CONTENT_DATA_CONTRACT_2026.md`
5. `BLACKSMITH_FIRST_FIVE_MINUTES_AND_MASTERWORKS_UX_2026.md`
6. `BLACKSMITH_BENCHMARK_FIRST_WORKING_PRINCIPLE.md`

벤치마킹 근거 문서는 설계 판단의 출처지만 규칙 충돌 시 마스터와 정합성 문서가 우선한다.

## 4. GitHub 전파 대상

### 4.1 정밀강화

대상:

- `BLACKSMITH_PRECISION_ENHANCEMENT_BASELINE.md`
- 연결된 기계 판독 데이터
- 관련 Decision Ledger·Authority Index

변경:

- 구형 정밀 등급 제거
- 수식어 슬롯 A·B 2개 제거
- 계보 1개 + 보조 2개 구조 반영
- 10단위 성공 후 별도 정밀 실패 판정 제거
- 성공 후 공개 후보 보장 선택 반영
- +50 진화와 +60 이상 정체성 심화 반영

### 4.2 강화 위험·확률 공개

대상:

- `BLACKSMITH_ENHANCEMENT_RISK_CURVE_2026.md`
- `BLACKSMITH_ENHANCEMENT_PROBABILITY_DISCLOSURE_2026.md`
- 연결 데이터

변경:

- `정밀강화 실패는 재료만 손실` 구형 문구 제거
- 일반 정밀강화는 10단위 진입 시도 자체로 통일
- 진입 성공 후 정체성 결과 보장 선택 명시
- 일반 강화 최종 확률 공개·보호 결과 변환 계약 유지
- +49→+50 특수재료 확정 성공 경로와 일반 위험 경로 구분

### 4.3 경제·가격

대상:

- `BLACKSMITH_ENHANCEMENT_PROFIT_CURVE_2026.md`
- `BLACKSMITH_FULL_PROTECTION_ENDGAME_ECONOMY_2026.md`
- 관련 경제 데이터

변경:

- 제작 완성도 기준명 `평범한` → 제작 등급 `보통`
- 정밀 등급 가치 보정 제거
- 수식어 일반 가치·진화·운명·연대기·고객 적합 순서 반영
- `DAMAGED` 감액 제거
- 전투 흔적은 고객·채널에 따라 가치 방향이 달라지는 서사 상태로 처리
- +5 최초 평균 흑자 구조 유지
- +60 이상 신규 수식어 슬롯 없음 명시

### 4.4 고객·장비 파괴

대상:

- `BLACKSMITH_CUSTOMER_EQUIPMENT_DESTRUCTION_2026.md`
- 고객·장비 생애주기 문서
- 연결 데이터

변경:

- 무보호 파괴 시 장비 객체 영구 소멸 유지
- 고객·관계 데이터 유지
- 파괴 장비 연대기 종료 기록 유지
- 명작 전당 `DESTROYED_HISTORY`는 아이템 복구가 아닌 공개 기록임을 명시
- 현재 사용 작품 랭킹 제외

### 4.5 고객·세계 결과

대상:

- 고객·관계·세계 게시판·검투사 관련 정본
- 콘텐츠 제작 파이프라인 문서

변경:

- 카시아·에르사 공통 결과 데이터 계약 반영
- 고객 이름 하드코딩 금지
- 장비 기여와 외부 원인 분리
- 승리·패배·전시 결과 모두 유효한 연대기 생성
- 배팅은 Vertical Slice 필수 완료 조건에서 제외

### 4.6 UX·접근성·성능

대상:

- UX 흐름
- 접근성 계약
- Android 패키지·성능 계획
- 플레이테스트 문서

변경:

- 첫 5분 화면 흐름
- 최소 48dp 터치 대상
- 초기 +1~+5 숨은 성공 보정 금지
- +5 완성·+10 도전 비교 화면
- 첫 강화 중앙값 60초 후보
- 검증 랭킹·레거시 전시 설명 UX

## 5. 문서 등록부·진입점

대상:

- `docs/DESIGN_DOCUMENT_REGISTRY.json`
- `docs/DOCUMENTATION_MAP.md`
- `docs/START_HERE.md`
- `docs/ACTIVE_CONTEXT.md`
- `docs/DEVELOPMENT_GATES.md`
- README의 기획 상태 안내

변경 원칙:

- 마스터 v9를 Vertical Slice 현행 기획 진입점으로 등록
- PR #61 v6 Draft·Addendum은 `LEGACY_REQUIREMENT_TRACEABILITY`로 이동
- 새 벤치마킹 원칙과 결과·UX 계약 등록
- `PR #35 Draft` 같은 구형 상태 제거
- 실제 main SHA와 기획 Gate 표시
- 구현 가능 상태를 과장하지 않음

## 6. Google Sheet 전파 대상

### 우선 동기화 탭

1. `00_프로젝트_허브`
2. `01_작업순서`
3. `02_현재_확정결정`
4. `04_누락_충돌_감사`
5. `05_GDD_요약`
6. `10_제품방향`
7. `12_핵심루프`
8. `13_주요인물`
9. `20_코어경험_데모목표`
10. `30_데모범위_품질기준_제작기반`
11. `40_핵심시스템_메인콘텐츠`
12. `41_성장_경제`
13. `50_메인콘텐츠`
14. `60_UX_UI_접근성`
15. `70_아트_오디오_에셋`
16. `80_데모_버티컬슬라이스_플레이테스트`
17. `90_본제작_출시_사업`
18. `99_변경이력`

### 핵심 변경

- Base v9.3 기준선과 병합 main SHA
- 고객 4종 동시 완주 제거
- 일상 +5/+10과 장기 +50 두 시간 지평
- 제작 등급 5단계
- 계보 1 + 보조 2
- 10단위 보장 선택 이정표
- 카시아 대표 세트·에르사 증명 세트
- 모닥
- 첫 5분 UX
- 명작 전당 미래 정책
- 구현·검수 Gate

## 7. Sheet 수식 오류 처리

현재 `+`로 시작하는 텍스트가 수식으로 해석된 셀이 존재한다.

처리 원칙:

- 텍스트 값은 문자열로 입력
- 필요한 경우 앞에 작은따옴표를 사용하거나 셀 형식을 일반 텍스트로 지정
- `#ERROR!`를 표시값만 덮어쓰지 않고 원래 의도 문구를 복원

확인 대상 예:

- `12_핵심루프`의 `+5 완성` 관련 셀
- `30_데모범위_품질기준_제작기반`의 `+60~+100` 관련 셀
- `40_핵심시스템_메인콘텐츠`의 고강화 관련 셀
- `50_메인콘텐츠`의 엔드게임 관련 셀
- `60_UX_UI_접근성`의 `+5/+10` 관련 셀
- `02_현재_확정결정`의 고강화 경제 셀

전체 Sheet에서 `effectiveValue.errorValue`를 재검색해 누락을 확인한다.

## 8. 동기화 순서

```text
1. 기획 완료 선언 확인
2. main 최신 SHA 확인
3. 구형 정본·등록부 정합화 브랜치 생성
4. 문서·기계 판독 데이터 변경
5. 정적 계약·링크·JSON 검증
6. PR 검토·병합
7. 병합 main SHA 재확인
8. Google Sheet 백업·변경 대상 범위 재조회
9. 탭별 일괄 동기화
10. #ERROR! 수정
11. 변경 탭 재조회
12. GitHub·Sheet 상호 대조
13. 04_누락_충돌_감사·99_변경이력 기록
14. 적대적 최종 검수
```

## 9. 검증 체크리스트

### GitHub

- [ ] 마스터 v9가 등록부의 현행 진입점
- [ ] 구형 정밀 등급 참조 제거 또는 LEGACY 표시
- [ ] 구형 슬롯 A·B 참조 제거 또는 LEGACY 표시
- [ ] 10단위 별도 실패 판정 제거
- [ ] 경제 가치 보정 순서 일치
- [ ] DAMAGED 반복 수리 참조 없음
- [ ] 배팅이 대표 완료 조건에 없음
- [ ] 파괴 역사 기록이 아이템 복구 권한을 만들지 않음
- [ ] JSON·문서 링크 유효

### Google Sheet

- [ ] Base v9.3·main SHA 일치
- [ ] 고객 4종 동시 완주 현행 표시 없음
- [ ] +5/+10/+50 역할 구분
- [ ] 제작 등급·수식어 구조 일치
- [ ] 카시아·에르사·모닥 반영
- [ ] 명작 전당은 FUTURE/NOT_IMPLEMENTED
- [ ] 모든 `#ERROR!` 제거
- [ ] 변경이력 기록

### Gate

- [ ] 제품 코드·Scene·데이터·에셋 변경 없음
- [ ] Codex Goal 생성 없음
- [ ] 구현 가능 상태 과장 없음
- [ ] 사용자 검수 완료 전 구현 차단 유지

## 10. 롤백·실패 처리

- GitHub PR 병합 전 Sheet 동기화 금지
- Sheet 동기화 중 오류가 나면 성공한 범위를 기록하고 실패 범위를 재조회
- 일부 탭만 미래 정본으로 남기는 상태를 장기 유지하지 않음
- Sheet 변경이 잘못됐다고 구형 GitHub 문서를 다시 현행으로 승격하지 않음
- 동기화 실패는 기획 실패나 제품 데이터 손상으로 처리하지 않음

## 11. 현재 판정

```text
LEGACY_PROPAGATION_PLAN: DEFINED
SHEET_PROPAGATION_PLAN: DEFINED
SHEET_ERROR_REPAIR_PLAN: DEFINED
EXECUTION_GATE: BLOCKED_UNTIL_기획_완료
PRODUCT_FILES_CHANGED: NO
SHEET_WRITE: NOT_RUN
CODEX_IMPLEMENTATION: BLOCKED
```
