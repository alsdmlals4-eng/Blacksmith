# Tests

## 자동 검증

```bash
python tools/validate_game_data.py
python tools/audit_project_operating_system.py --base-root <Base checkout>
python tests/check_forging_quality_contract.py
python tests/check_enhancement_failure_contract.py
godot --headless --editor --path . --quit
godot --headless --path . res://scenes/test/enhancement_test.tscn --quit-after 2
godot --headless --path . --script res://tests/unit/test_forging_session.gd
godot --headless --path . --script res://tests/unit/test_enhancement_session.gd
godot --headless --path . --script res://tests/unit/test_workshop_resources.gd
godot --headless --path . --script res://tests/integration/test_manual_enhancement_economy.gd
godot --headless --path . --script res://tests/integration/test_forging_quality_enhancement.gd
```

## 현재 범위

- 제작 진행도·피버·정밀 마감·초기화
- 피버 1회 이상 결과 보너스와 반복 발동 비중첩 경계
- 보통·좋음·완벽 마감 및 마감+피버의 공격력·가치 배율과 제작→강화→보관 전달
- 구형 단일 품질 배율·기본 공격력 덮어쓰기·옛 버전 재등장 차단
- 일반 강화와 +10 단위 특수 강화 분리
- 재료·촉매·정밀 효과의 일반 단계 누출 방지
- +10~+100 수식어 성장
- 공격력·가격·비용의 점진 성장
- 실패 유지·단계 하락·파괴·실패 보정
- 실패 정책 단일 정본, 도달 가능한 decade, 이정표/위험표 의미 검증
- 안정·균형·폭주 단조
- 폭주 성공 시 낮은 확률 총 2단계 상승과 이정표 차단
- 촉매 비용·보호·위험 효과
- 보관함 최대 6개와 파괴 무기 보관 차단
- 자동 단조 목표·재료 fallback·자동 보관·반복·중지
- 수동·자동 강화의 동일 골드 차감·재료 소비·부족 차단·중복 결제 방지
- Base 13개 기능 매핑·Registry·로컬 참조·stale 정본 감사

## 별도 검증

자동 테스트만으로 다음을 통과 처리하지 않는다.

- 실제 화면·스크롤·시각 품질
- Android 터치·안전 영역·태블릿·폴더블
- AAB·Google Play
- 접근성 사람 검수
- 대표·최악 장면 성능 프로파일
- 저장·복귀·방치 보상
- 고객·상인 판매

강화 실패 정책·확률·위험표의 유일한 정본은 `data/crafting/enhancement_balance.json`이며, `data/crafting/enhancement_milestones.json`은 수식어 이정표만 소유합니다.
