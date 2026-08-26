# Decision31 수리 경제 결정론 감도분석

- Decision: `BS-REPAIR-20260826-31`
- 상태: `TEMP_TEST_BUDGET_NOT_FINAL_PRODUCT_BALANCE`
- 실행 범위: planning-only deterministic analysis
- 실행 입력: `R_BAND = 100` 정규화 기준, 동일 UID `BS-REPAIR-SENS-001`
- 비교: `b = 0.50 / 0.65 / 0.80`

## 입력 및 경계

`R_BAND = 100`은 곡선의 상대 차이를 읽기 위한 고정 측정 단위다. 판매가,
다음 강화비, MAX 흉터 배율, 실제 확보 강화구간 가격이 아니다. 보강재는 각
수리마다 `common_reinforcement_material x1`로 별도 소비하며, Decision18의
50G shadow value는 Gold에 합산하지 않았다.

모든 비교는 같은 UID, 같은 다섯 실제 손상 뒤 repair-job, 같은 quality/scar
stream을 사용한다. 따라서 아래 Gold 차이의 유일한 원인은 `b`다.

## 결과

| Event | OLD CURRENT / MAX / BASE | Quality · candidate MAX | b=.50 Gold | b=.65 Gold | b=.80 Gold | POST MAX · NEW CURRENT | 회복 | Scar | 수리권 |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| E1 | 4 / 5 / 5 | 1.00 · 5 | 15 | 18 | 21 | 5 · 5 | 1 | 없음 | 시작 시 소비, 재시도 차단 |
| E2 | 3 / 5 / 5 | 0.50 · 5 | 25 | 31 | 37 | 5 · 4 | 1 | 없음 | 시작 시 소비, 재시도 차단 |
| E3 | 2 / 5 / 5 | 0.75 · 4 | 35 | 44 | 53 | 4 · 3 | 1 | 적용 | 시작 시 소비, 재시도 차단 |
| E4 | 1 / 5 / 5 | 1.00 · 4 | 45 | 57 | 69 | 4 · 4 | 3 | 적용 | 시작 시 소비, 재시도 차단 |
| E5 | 4 / 5 / 5 | 0.50 · 4 | 15 | 18 | 21 | 5 · 5 | 1 | **skip** | 시작 시 소비, 재시도 차단 |

Gold 묶음은 Current 4/3/2/1 순서로 각각 `15 / 18 / 21`, `25 / 31 / 37`,
`35 / 44 / 53`, `45 / 57 / 69`이다. 각 표 행은 세 `b` 결과를 함께 표시한
것이며, 기계 산출물은 총 15개 행을 유지한다.

## 기계 검증

- 15/15 수리 행에서 `NEW_CURRENT > OLD_CURRENT`.
- E5는 `candidate_post_scar_max <= OLD_CURRENT`이므로 scar를 skip했고,
  quality/scar reroll 없이 1 Current를 회복했다.
- 15/15 수리 행에서 repair job은 시작 즉시 소비되고, 즉시 재수리 결과는
  `BLOCKED_NO_REPAIR_JOB`이다. 다음 resolved actual damage만 새 job을 연다.
- 보강재는 15/15 행에서 1개이며 Gold에 포함되지 않았다.
- 세 곡선에서 recovery, scar 처리, 재료 수량, repair-job 결과는 같고 Gold만
  `b`에 따라 변한다.

## 판정

| 항목 | 판정 | 이유 |
| --- | --- | --- |
| Repair job 1회 제한 | KEEP | 나쁜 quality 뒤의 반복 뽑기를 기계적으로 차단한다. |
| 0회복 scar guard | KEEP | 5칸 기준에서 paid repair의 양의 회복을 보장한다. |
| 보강재 1개 분리 소비 | KEEP | Gold 할인·흉터 이중 과금 없이 공통 자원 의미를 유지한다. |
| b=.50 / .65 / .80 | TEST_IN_PLAY | 산술은 단조·판독 가능하지만, 나쁜 결과의 답답함과 비용 압력은 실제 플레이가 필요하다. |
| R_BAND 실제 입력 근거 | NOT_DECIDED | 실구간 가격과 Gold 목표는 이 분석의 범위 밖이다. |

## 미실행·다음 Gate

Runtime, Android, 접근성, 성능, 사람 플레이는 모두 `NOT_RUN`이다. 이 결과는
제품 가격이나 구현 허가가 아니다. 다음 결정은 사람 체감 검증 설계와, 그 뒤
사용자 승인에 따른 실제 `R_BAND` 근거/목표 범위 검토다.
