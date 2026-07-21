# 변경 요약

- 목표:
- 사용자·플레이어 가치:
- Work Mode:
- 주 책임 분야:
- 영향 분야:
- 관련 Issue·승인 요청:
- 기준 Base 커밋:
- 기준 Blacksmith 커밋:
- 버전 표시 영향:

## 범위·보호

- 포함:
- 제외:
- 보호한 결정·코드·데이터·경로:
- 삭제·이동·Schema 변경:
- 롤백:

## 작업 게이트

- [ ] Intake·Context
- [ ] Definition of Ready
- [ ] Planning·Approval
- [ ] Implementation
- [ ] Verification
- [ ] Documentation
- [ ] Integration·Completion

## 파일별 전수 확인

| 파일 | 변경 이유 | 책임 원본/소비자 | 검증 | 판정 |
|---|---|---|---|---|
|  |  |  |  |  |

- [ ] 변경 파일 목록을 GitHub API로 전부 확인
- [ ] 각 patch를 읽고 범위 밖 변경 없음
- [ ] 삭제 파일의 대체 경로·참조·Git 복구 확인
- [ ] 변경됐어야 하지만 untouched인 소비자 확인
- [ ] 과거 History/Legacy와 활성 stale reference 구분

## 책임 원본·Registry

- [ ] START_HERE·Active Context·Documentation Map·Gate 일치
- [ ] Design Document Registry의 모든 ACTIVE source 경로 존재
- [ ] 한 질문당 현행 Markdown/JSON 원본 하나
- [ ] 실제 수치는 `data/**/*.json`, 구현 사실은 Scene·Script·테스트와 일치
- [ ] Skill Registry schema v3·automatic-trigger-match
- [ ] 주 책임 분야 Skill 최대 하나·Foundation 최소 호출
- [ ] Skill 변경 시 Learning Log 갱신
- [ ] Base 기준 커밋과 프로젝트 차이 기록

## 강화·게임 회귀

- [ ] 일반 강화에 보조재료·촉매·정밀 효과 누출 없음
- [ ] +10 단위에서만 특수 강화
- [ ] +11부터 하락, +30부터 파괴
- [ ] 실패 보정 +4%p·최대 +24%p
- [ ] 안정 단조 보호
- [ ] 폭주 8% 총 2단계·특수 강화 건너뛰기 차단
- [ ] +100 수식어 3개 4티어
- [ ] 보관함 6칸
- [ ] 자동 단조 목표·자동 보관·반복·골드·재료 소진
- [ ] `project.godot` F5 기본 진입 유지

## 검증

| 검증 | 결과 | 증거 |
|---|---|---|
| `python tools/check_project_governance.py` |  |  |
| `python tools/validate_game_data.py` |  |  |
| Godot import/parse |  |  |
| Enhancement Scene smoke |  |  |
| ForgingSession 4 cases |  |  |
| EnhancementSession 12 cases |  |  |
| 정본·참조 최신성 검색 |  |  |
| 실제 Godot 화면 |  |  |
| Android 실기기·AAB |  |  |
| PDF·Skill Map |  |  |

## 상태 분리

- 자동 검증:
- 실제 구현:
- 수동 플레이:
- 시각·접근성:
- Android·성능:
- 발행본:
- 미검증:
- 후속:

## Acceptance

- [ ] 승인 범위 충족
- [ ] 보호 범위 침범 없음
- [ ] 문서·Registry·데이터·코드·테스트 일치
- [ ] 차단 finding 0
- [ ] 사용자 확인 절차: Fetch origin → Pull origin → Godot F5
