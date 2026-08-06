# Blacksmith R2 Vertical Slice Benchmark — 2026-08-06

## 목적

R2 Batch 006의 Godot 버티컬 슬라이스가 유명 작품을 피상적으로 복제하지 않고, Blacksmith의 프로젝트 코어를 가장 짧은 경로로 검증하도록 비교한다.

```text
직접 제작의 손맛
→ 강화 지속·중단 판단
→ 고객과 세계에서 작품 결과 회수
→ 같은 UID 작품의 생애 기억
```

모든 비교 결과는 `채택 / 수정 채택 / 비채택 / 차별점 / 남은 불확실성`으로 기록한다.

## 비교 대상

### Potion Craft

공식 설명은 도구와 재료를 직접 조작하는 제작, 레시피 실험, 고객 대응, 상점 운영을 한 루프로 묶는다.

- 참고: https://www.playstation.com/en-us/games/potion-craft-alchemist-simulator/
- 참고: https://store.steampowered.com/app/1210320/Potion_Craft_Alchemist_Simulator/

**채택**

- 제작 행동이 고객 요구로 이어지는 짧고 읽기 쉬운 루프
- 제작 결과를 고객에게 제안하고 적합성을 판단하는 구조
- 직접 제작 과정이 단순 수치 선택보다 중요한 체험이어야 한다는 원칙

**수정 채택**

- 레시피 탐색 대신 `주재료 + 역할별 3구간 직접 단조`를 사용한다.
- 즉시 판매 중심이 아니라 작품 UID가 고객 결과·손상·복원·연대기로 되돌아오게 한다.

**비채택**

- 광범위한 레시피 맵과 재료 조합 퍼즐
- 버티컬 슬라이스에서 상점 평판·흥정·대규모 재고 경제를 동시에 구현하는 범위

**차별점**

Potion Craft가 제작 결과의 용도 적합성을 강조한다면 Blacksmith는 같은 작품이 강화 위험과 세계 사건을 거쳐 생애를 쌓는 점을 강조한다.

**남은 불확실성**

직접 단조 3구간 입력이 반복 세션에서도 충분히 의미 있는 차이를 만드는지는 사람 플레이테스트가 필요하다.

## While the Iron's Hot

공식 설명은 전투보다 제작과 자원, 퍼즐, 세계 연결을 중심으로 대장장이 여정을 구성한다.

- 참고: https://store.steampowered.com/app/1906830/While_the_Irons_Hot/
- 참고: https://www.nintendo.com/us/store/products/while-the-irons-hot-switch/

**채택**

- 제작한 물건이 세계의 문제와 관계를 해결하는 구조
- 전투를 직접 플레이하지 않아도 제작 결과가 사건과 이야기로 환류할 수 있다는 방향

**수정 채택**

- 탐험·퍼즐·마을 복구 대신 고객 일정과 날짜 예고형 세계 일정을 사용한다.
- 제작품의 결과를 일회성 퀘스트 완료가 아니라 동일 UID 연대기에 기록한다.

**비채택**

- 이동 가능한 탐험 맵
- 광범위한 스토리 퀘스트와 자원 채집
- 버티컬 슬라이스에서 제작 외 장르를 확장하는 방식

**차별점**

Blacksmith는 플레이어 캐릭터의 여행보다 작품 자체의 생애와 강화 선택을 주인공으로 둔다.

**남은 불확실성**

텍스트·카드 중심 결과 화면만으로 세계에 영향을 줬다는 감각이 충분한지 검증해야 한다.

## Blacksmith Master

공식 설명은 광산·벌목·제련·제작·판매를 포함하는 전체 생산 체인과 작업장 최적화를 강조한다.

- 참고: https://store.steampowered.com/app/2292800/Blacksmith_Master/
- 참고: https://wiki.hoodedhorse.com/Blacksmith_Master/Blacksmith_Master

**채택**

- 재료 선택과 제작 결과가 고객 수요와 연결되어야 한다는 원칙
- 제작품·고객·경제 사이에 명확한 원인 관계를 보여주는 정보 설계

**수정 채택**

- 생산 체인 전체가 아니라 대표 주재료 3종만 사용한다.
- 작업장 처리량 최적화 대신 한 작품을 더 강화할지 멈출지 판단하는 데 집중한다.

**비채택**

- 인력 배치
- 건물 배치와 생산 라인
- 광산·벌목·운송·대량 재고
- 대규모 경영 시뮬레이션

**차별점**

Blacksmith Master가 작업장 전체의 효율을 다룬다면 Blacksmith는 개별 작품의 출생·위험·고객 결과·연대기 기억을 다룬다.

**남은 불확실성**

대표 작품 한 점에 집중하는 구조가 충분한 장기 반복성을 제공하는지는 버티컬 슬라이스 이후 별도 검증이 필요하다.

## Godot 4.7 저장 구조

Godot 4.7 공식 문서는 `FileAccess`를 사용해 `user://` 경로에 저장 파일을 쓰고 JSON 또는 Dictionary 기반 데이터를 복원하는 방식을 제공한다.

- 참고: https://docs.godotengine.org/en/4.7/tutorials/io/saving_games.html
- 참고: https://docs.godotengine.org/en/stable/classes/class_fileaccess.html

**채택**

- `user://blacksmith_vertical_slice_v1.json`
- 명시적 `schema_version`과 `preset_version`
- JSON 호환 SaveEnvelope
- 저장 실패를 확인할 수 있는 반환값과 오류 처리

**수정 채택**

- 단순 노드 위치 저장이 아니라 작품 UID와 append-only 변동 장부를 중심으로 저장한다.
- 임시 파일 작성 후 교체해 중간 저장 실패가 기존 파일을 바로 손상시키지 않게 한다.
- RNG seed를 저장해 불러오기 재추첨을 금지한다.

**비채택**

- 역사 POC의 인메모리 작품 Dictionary를 그대로 직렬화
- 타입·버전 경계 없이 모든 런타임 객체를 저장
- 저장·불러오기로 제작 등급이나 고객 결과를 재추첨하는 구조

**차별점**

저장은 진행도 백업만이 아니라 같은 작품의 출생 사실과 변동 원인을 보존하는 정본 장치다.

**남은 불확실성**

Android 강제 종료·저장 공간 부족·파일 손상 복구는 데스크톱 headless 검증만으로 충분하지 않으므로 실제 Android 기기 검증이 필요하다.

## 적대적 검토 결론

### 가장 위험한 잘못된 방향

1. 기존 POC 화면이 있으므로 구형 `STANDARD / GOOD / PERFECT`와 보조재료 필드를 그대로 확장하는 것
2. 버티컬 슬라이스라는 이름으로 모든 장비군·재료·고객·이정표를 구현하는 것
3. 데모 수치를 최종 밸런스로 간주하는 것
4. 저장 파일에 결과만 넣고 변동 원인과 RNG seed를 누락하는 것
5. 자동 테스트 PASS를 사람 플레이테스트 PASS로 보고하는 것

### 최종 채택안

```text
ALL_APPROVED_CONTRACTS_REQUIRED
REPRESENTATIVE_CONTENT_ONLY
NEW_VERTICAL_SLICE_NAMESPACE
VERSIONED_UID_AND_SAVE_ENVELOPE
BASELINE_TEST_PRESET / USER_PLAYTEST_REQUIRED
```

판정: `R2_BATCH_006_RECOMMENDED_PENDING_USER_APPROVAL`.
