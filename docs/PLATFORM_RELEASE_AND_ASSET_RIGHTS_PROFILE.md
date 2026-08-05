# Blacksmith 플랫폼 출시·에셋 권리 Profile

> Base 정본: `alsdmlals4-eng/Base/docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`  
> 기준 main: `476ddc380079dd61d67cda4c065a80819355292f`  
> 실제 제품 구현·자산 감사·제출은 아직 수행하지 않았다.

## 전략

```yaml
rating_strategy: LOWEST_VIABLE_RATING
adult_only_avoidance: AVOID_ADULTS_ONLY
content_rating_target: UNASSIGNED_PENDING_REPRESENTATIVE_BUILD
rating_candidate_range: ALL_OR_12_CANDIDATE
target_audience: GENERAL_AND_TEEN_CRAFTING_PLAYERS_PENDING_VALIDATION
children_in_target_audience: UNDECIDED
families_policy_applicable: UNDECIDED
platforms:
  Android: PRIMARY
  Google_Play: PRIMARY_RELEASE_CANDIDATE
  Steam: NOT_CURRENT_SCOPE
  STOVE: NOT_CURRENT_SCOPE
```

전체이용가는 후보지만 강제하지 않는다. 무기 제작·강화, 실패·손상, 검투·전투 결과 표현을 실제 빌드 기준으로 공개하며 청소년이용불가·18+를 기본적으로 피한다.

## 콘텐츠 위험 초안

| Risk | 현재 상태 | 출시 전 확인 |
|---|---|---|
| violence | 무기·검투·전투 결과 맥락 존재 가능 | 유혈·상처·사망·고통 묘사 강도 |
| sexual content / horror / language / drugs / crime | 정본만으로 전수 판정 불가 | 전체 대사·이벤트·상점 이미지 |
| gambling/simulated gambling | 강화 확률과 실패는 사행성 설문과 별도 검토 필요 | 실제 확률·유료 재화·현금성 보상 관계 |
| ads/IAP | 미확정 | 광고 SDK, 보상형 광고, IAP, 확률 공개, 환불 |
| UGC/online interaction | 미확정 | 실제 출시 기능 |
| AI-generated/live-generated content | 자산별 증빙 필요 | 모델·서비스·버전·입력 권리·약관 날짜·Google Play 공개 |

`content_rating_target`과 `target_audience`를 분리한다. 낮은 등급을 받기 위해 아동 대상으로 자동 선언하지 않는다.

## 자산·참조 제작

음악·효과음, 폰트, 캐릭터·일러스트·UI, 3D·애니메이션, 플러그인·에셋, OSS, AI 출력·약관, 외주, 성우·작곡·번역 계약을 자산별 Record로 관리한다.

```text
합법적 reference source
→ 기능·구조·정보 위계·일반 제작 원리
→ forbidden_expression
→ Blacksmith 고유 reference_brief
→ 별도 작업 파일·final_asset_record
→ similarity and rights review
```

원본을 조금 수정하거나 AI로 재생성했다는 이유만으로 독립 자산으로 보지 않는다.

## Release Gate

권리·조건 이행·Google Play 설문·target audience·Families·광고 SDK·데이터·개인정보·build/store 일치 중 하나라도 미확인이면 `RELEASE_BLOCKED_UNVERIFIED`다.

```text
STATIC_EVIDENCE_PROFILE_CREATED
RUNTIME_ASSET_USE_CHECKED: NOT_RUN
BUILD_STORE_CONSISTENCY_CHECKED: NOT_RUN
GOOGLE_PLAY_SUBMISSION: PLATFORM_SUBMISSION_NOT_RUN
FINAL_RATING: NOT_ASSIGNED
LEGAL_REVIEW: LEGAL_REVIEW_NOT_PERFORMED
```
