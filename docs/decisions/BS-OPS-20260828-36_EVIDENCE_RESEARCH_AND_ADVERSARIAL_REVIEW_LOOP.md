# BS-OPS-20260828-36 · 증거·조사·적대적 검토 루프

- 상태: `USER_APPROVED_CURRENT_OPERATIONAL_OVERRIDE`
- 날짜: `2026-08-28 KST`
- 범위: Blacksmith의 기획, 문서, 구현 계약, 코드 검토, 시각자료, 출시·권리 관련 **실질 작업**의 조사·검증 절차. 새 게임 기능, 권리 확보, 출시, runtime 통과를 자동 승인하지 않는다.

## 1. 사용자 승인 운영 규칙

사용자는 앞으로 필요한 승인 사항을 이 대화에서 승인한다고 밝혔고, 모든 작업에서 적대적 검토 루프·인터넷 조사·실제 구현 가능성 재확인을 요구했다. 이 규칙은 기존 current Canon을 대체하는 게임 규칙이 아니라, 정본을 다루는 작업 절차의 강화다.

```text
USER_APPROVED_CURRENT_OPERATIONAL_OVERRIDE
FRESH_CANONICAL_READ = REQUIRED
CURRENT_EXTERNAL_RESEARCH = REQUIRED_FOR_EVERY_SUBSTANTIVE_TASK
ADVERSARIAL_REVIEW_LOOP = REQUIRED
IMPLEMENTATION_FEASIBILITY_GATE = REQUIRED
EVIDENCE_CEILING = NO_AUTO_PASS
ADOPT / ADAPT / AVOID / REJECT / DIFFERENTIATION / REMAINING_UNCERTAINTY / TEST = REQUIRED
```

## 2. 작업마다 남길 증거

실질 작업을 시작하기 전과 완료 전, 담당자는 다음을 확인하고 해당 Project GitHub 정본에 남긴다.

1. **fresh canonical read:** 현재 main, 관련 current Decision/JSON, handoff, open/draft PR 경계, 실제 consumer와 테스트를 다시 읽는다.
2. **current external research:** 작업에 영향을 주는 게임 기획·UX·기술·Android·플랫폼·권리 자료를 최신 공식/1차 자료와 직접 관련 사례로 조사한다. 외부 자료가 정본을 자동 변경하지 않는다는 점을 함께 기록한다.
3. **ADOPT / ADAPT / AVOID / REJECT / DIFFERENTIATION / REMAINING_UNCERTAINTY / TEST:** 무엇을 채택·변형·회피·명시 거절·검증하는지, Blacksmith의 차별점과 남은 불확실성을 기록한다. 비슷한 색만 다른 허수 대안이나 타 작품의 표현 복사는 금지한다.
4. **adversarial review:** 핵심 재미의 단절, 승인 Decision 무시, 기능/이미지 발명, UX 가독성, scope 폭증, 기술·데이터·권리·성능 위험을 실패 가정으로 검토한다.
5. **implementation feasibility:** Godot Scene/Node/Resource/GDScript, 데이터 소유자, target Android/세로형 UI, 테스트와 runtime consumer를 대조한다. 가능한 경우 작은 재현 또는 공식 문서로 확인하되, 실행하지 않은 경로는 `NOT_RUN`으로 남긴다.
6. **correction and readback:** 유효 finding은 영향을 받은 정본/계약/테스트에만 교정하고 exact destination readback을 남긴다.

## 3. 증거 상태와 금지된 추론

```text
VERIFIED = named source and direct test/runtime/human evidence agree
PARTIAL = a source or implementation path exists, but the complete claim is not proven
INFERENCE = reasonable interpretation; not a current fact
NOT_RUN = required execution, device, visual, accessibility, performance, or human test was not observed
```

문서 존재, 코드 존재, CI 통과, 생성 이미지 존재는 각각 다른 층위의 증거다. 하나를 다른 층위의 PASS로 승격하지 않는다. 특히 사람이 읽기 쉬운가, 플레이가 재미있는가, Android 기기에서 문제없는가, 에셋 권리가 충분한가는 별도 증거 없이는 자동 PASS가 아니다.

## 4. 적용 경계

- 외부 조사는 current Canon보다 낮은 권위다. 조사 결과가 사용자 승인과 충돌하면 충돌을 기록하고 새 Decision 없이는 제품 의미를 바꾸지 않는다.
- 단순 철자 수정처럼 플레이어 경험·기술·권리·범위에 영향을 주지 않는 작업은 이 결정의 전체 조사 형식을 요구하지 않는다. 그러나 “조사를 생략했다”는 이유로 실질 기획·구현·시각·출시 작업을 가볍게 취급할 수는 없다.
- 생성 후보와 사용자 잠금, Project Asset, runtime evidence는 서로 다른 상태다. 이미지의 실제 consumer/권리/최종 lock 규칙은 Decision04와 Decision35를 계속 따른다.
- 유효 finding이 없으면 `NO_CORRECTION_AFTER_REVIEW`와 근거를 기록한다. 유효 finding이 있으면 국소 수정 후 해당 검증만 다시 실행한다.

## 5. 이번 적용 기록

`BLACKSMITH_HUMAN_FACING_GDD_20260828.md` 작성 시 current Canon, Decision34/35, handoff, vertical-slice Scene/GDScript와 기존 계약을 fresh-read했다. Godot Control의 UI anchor/offset 공식 문서와 Android export 공식 문서, 공방·고객 맥락의 인접 사례를 조사했다.

### 이번 조사 source identity · 2026-08-28 KST

- Godot 공식 UI 레이아웃: [Size and anchors](https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html), [Control class](https://docs.godotengine.org/en/stable/classes/class_control.html). `Control` anchor/offset이 부모·viewport 변화에 맞는 UI 레이아웃의 기반임을 확인했다.
- Godot 공식 Android export: [Exporting for Android](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html). Android SDK/JDK, release signing/AAB 등은 별도 실행·출시 검증 경로임을 확인했다.
- Android 공식 게임 품질/안정성: [Android game design overview](https://developer.android.com/games/design/overview?hl=en), [Android vitals for games](https://developer.android.com/games/optimize/vitals). 실제 기기 안정성·메모리·사용성은 문서나 코드 존재만으로 통과할 수 없음을 재확인했다.
- 인접 사례: [Shop Titans 공식 Steam 페이지](https://store.steampowered.com/app/1258080/Shop_Titans/), [Moonlighter 공식 Steam 페이지](https://store.steampowered.com/app/606150/Moonlighter/). 전자는 제작품과 고객/모험 맥락의 감정적 프레이밍, 후자는 상점·제작·강화의 역할 선명도만 제한적으로 참고했다. 시장·길드·타이쿤 관리, 던전 액션, 소매 가격 책정은 Blacksmith 요구사항으로 채택하지 않았다.

- `ADAPT`: 다양한 세로형 화면을 위해 Control 기반의 정보 우선순위·anchor/container 설계를 따른다.
- `AVOID`: 고객 생애를 폭넓은 시장/길드/타이쿤 관리로 확장하여 강화 메인을 가리는 일.
- `REJECT`: Moonlighter식 던전 액션/소매 상점 운영을 두 번째 메인 루프로 들여오는 일. Blacksmith의 차별점은 같은 무기 UID의 강화 판단이 실제 사용·손상·연대기로 이어지는 데 있다.
- `REMAINING_UNCERTAINTY`: 6~8분 Slice에서 생애 결과가 강화 메인을 강화하는지 Human/Player Experience로 확인되지 않았다.
- `VERIFY / PARTIAL`: current project Godot 4.7.1 headless GUT은 167 tests / 0 failures / 0 errors로 끝났다. live editor에는 Blacksmith project instance가 열려 있고 현재 error output은 없었으나, 이는 실제 화면·입력·Android 증명이 아니다.
- `TEST`: 실제 Godot client, Android 기기, 접근성, 성능, 6~8분 Human/Player Experience는 아직 `NOT_RUN`이다.
- `CORRECTION`: 영어 AI 생산 명세가 사람용 GDD를 겸하던 혼선을 한국어 사람용 GDD/PDF와 기술 추적용 명세로 분리했다.
