# Blacksmith BCA v8 적용 적대적 검토

```yaml
base_commit: 7072b9e2742a60d7548fd39df3328ad76a8dbad1
project_sheet_status: NOT_CONFIGURED
product_paths_changed: false
final_status: CONFLICT_FIXED
```

- `MUST_FIX`: Base SHA·v8 실행문·Sheet·이미지 승인 adapter 부재 → 설치.
- `MUST_FIX`: 사용자의 과거 명시 요청 조건이 새 승인된 기획 이미지 workflow를 막음 → 단계·브리프·검수 조건으로 교체.
- `MUST_FIX`: Android 실제 화면과 최종 자산 상태 분리 부족 → lifecycle·QA 추가.
- `ALLOWED_LEGACY`: 기존 PoC·Prototype 구현 사실은 역사·현재 구현 상태로 보존하며 별도 제품 Gate 권한으로 사용하지 않음.
- `BLOCKED_UNVERIFIED`: 실제 Sheet, 생성 이미지, Android 실기기·AAB·런타임 검수.
