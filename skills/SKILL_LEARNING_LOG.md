# Skill Learning Log

## 2026-07-21 — 프로젝트 초기 설치

- 결과: 게임 디자인·엔지니어링·QA 진입 Skill 골격
- 미검증: 실제 화면·Android

## 2026-07-21 — MVP-001 제작

- 결과: 제작 모델, 세로형 UI, 피버, 정밀 마감
- 검증: Godot 파싱, 제작 모델 4건, JSON
- 교훈: 동적 Script 속성을 받는 GDScript 테스트 지역 변수는 타입 추론 실패 가능성을 점검한다.
- 미검증: 실제 렌더·Android

## 2026-07-21 — 강화 POC 확장

- 결과: +100 일반/특수 강화, 수식어 성장, 성장·가격·하락·파괴, 단조 기술
- 검증: 강화 모델에서 성장·가격·촉매·유지·하락·파괴·보호·+100을 분리
- 교훈: 고단계 위험은 성공 가치와 시도 전 확률·가격 표시를 함께 제공해야 한다.
- 미검증: 실제 파괴 스트레스·경제 균형

## 2026-07-21 — 폭주 도약·자동 단조

- 결과: 폭주 8% 총 2단계, 특수 강화 건너뛰기 차단, 목표 자동 강화·보관·반복
- 검증: EnhancementSession 12건, Godot 파싱·Scene smoke·JSON
- 교훈: 도약 기능은 현재 목표뿐 아니라 도약 범위의 모든 이정표와 자동 목표 초과를 검사해야 한다.
- 교훈: 자동화가 선택 재료 부족을 오류로 멈추지 않고 명시된 빈 슬롯 정책으로 계속해야 한다.
- 미검증: 보관함 반복 생산의 실제 UX와 저장 호환성

## 2026-07-21 — Base 운영체계 감사

- 사용: `PLAN → BUILD → REVIEW`
- 결과: Base 기준 고정, 자동 Skill 라우팅, Registry schema v3, Handoff·Matrix·Health Report·Governance·PR 체크리스트
- 발견: 활성 문서가 +5·파괴 없음·과거 테스트 수를 주장해 실제 POC v0.6.0과 충돌
- 처리: 과거 결정은 삭제하지 않고 `대체됨`으로 보존, 현재 문서는 실제 데이터·테스트로 갱신
- 교훈: 기능 PR 완료 시 Active Context·Game Bible·MVP Scope·Gate·Roadmap·Decision Log의 untouched consumer를 반드시 검색한다.
- Skill 변경: 프로젝트 운영·변경 검증·모바일 UX mode를 명시
- 미검증: PDF·Skill Map·Android·Branch protection
