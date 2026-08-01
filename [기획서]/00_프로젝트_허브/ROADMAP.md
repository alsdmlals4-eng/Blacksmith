# Blacksmith Roadmap

> 상태: `PLANNING_REMEDIATION_IN_PROGRESS`
>
> 갱신일: `2026-08-01`
>
> 제품 구현: `BLOCKED`

## 1. 보존 기준선

### 프로젝트 코어 — PASS / KEEP

- 한 명의 대장장이
- 직접 제작
- 작품의 영구 제작 등급
- 강화 위험과 장비 정체성 선택
- 판매·인계 후 장비 UID·소유권·연대기 보존
- 세계 결과·명성·다음 의뢰 환류
- 직원·직접 전투·작업 예약·일상적 수리 관리 제외

### 기존 PoC — HISTORICAL IMPLEMENTATION BASELINE

MVP-001~003에서 다음 구현과 자동 검증 이력을 보존한다.

- 제작·피버·정밀 마감
- 강화·실패 보정·하락·파괴
- 자원 거래 원자성
- 6칸 보관함·자동 단조
- 카일 검투사 납품·지연 결과·장비 Registry
- Python·Godot·E2E PASS 이력

이 기준선은 최신 제품 정본이 아니다. 최신 v9와 충돌하는 구형 등급·수식어·고객·자동화는 마이그레이션한다.

## 2. 완료된 현행 기획

### 방향·비주얼

- 별도 메인 화면
- 단일 `BlacksmithApp` + View·Overlay
- 스타일라이즈드 다크 포지
- 밝은 불 정령 모닥
- 비주얼 보드 `USER_ACCEPTED_WORKING_BASELINE`

### 게임 규칙

- 제작 등급: 보통→우수→명품→걸작→전설
- 계보 1개 + 보조 최대 2개
- +10·20·30·40 정체성 이정표
- +49→+50 일반 정밀강화 / 고위 정밀강화
- 고객 4유형 × 유형별 복수 이름 고객
- 장비 운명·소유권·연대기

### 저장·마이그레이션

- `BS-SAVE-20260801-01`: 단일 캠페인·자동 백업2·AttemptIntent·ResultEnvelope
- 저장 구현계획: 11개 TDD Task
- `BS-MIGRATION-20260801-01`: 구형 데이터 결정론적 이전
- 마이그레이션 구현계획: 7개 TDD Task

위 계획은 전체 기획·최종 검수 전 실행하지 않는다.

## 3. 운영체계 현재 상태

- Base current 구조 분석: 완료
- 적용 목표: released Base v9.3
- canonical adapter: v9.1 구형
- protected baseline·Sheet binding·provenance·Snapshot·Router·Health: 정합화 필요
- latest Base main·미출시 v9.4 직접 pin: 금지
- local Base generator·validator: NOT_RUN

## 4. 현재 단계 — Canonical Remediation

- [x] P0-1 세이브·이어하기·ResultEnvelope 기획
- [x] P0-2 제작 등급·수식어·+50 마이그레이션 기획
- [x] Base Skill·작업 구조 분석
- [x] GitHub·Sheet 적대적 검토 Pass 2
- [ ] 시작 문서·Design Registry·Sheet CURRENT/History 정리
- [ ] Base v9.3 adapter migration 실행 준비·검증
- [ ] P0-3 고객 공통 계약
- [ ] P0-4 자동 단조 정지 경계
- [ ] P0-5 비주얼 Placeholder·Asset/License 구조
- [ ] P1 Theme·안전 영역·설정·Android lifecycle
- [ ] 최신 validator·fixture·E2E·시각 회귀 계획
- [ ] 적대적 검토 Pass 3

## 5. P0-3 고객 공통 계약

필수 완료 기준:

- 수집가·모험가·검투사·군인 공통 데이터 구조
- 유형별 최소 2명 이름 고객
- 모험가·군인 대표 확정
- 범주 요청·공개 적합도·관계·소유권 이전
- 유형별 세계 결과 Resolver
- 카시아 대표·에르사 재사용·추가 고객 비하드코딩 fixture
- 공통 ResultEnvelope·CampaignSnapshot 연결

## 6. P0-4 자동 단조 경계

필수 완료 기준:

- +5 완성 판단 전 정지
- +10/+20/+30/+40 선택 전 정지
- +49→+50 경로 선택 전 정지
- 판매·고객 인계·비가역 결과 전 정지
- 정밀 게이지 임의 난수 자동 판정 금지
- 특수재료 빈 fallback으로 이정표 우회 금지
- 파괴 뒤 무제한 새 장비 반복의 기본값 금지

## 7. P0-5·P1

### 비주얼·자산

- 시안 Placeholder와 시스템 정본 분리
- 최종 화면 에셋 Manifest
- 외부 에셋·폰트·아이콘 License Ledger
- 모닥 실제 화면 크기·밝기·가림 검증
- 핵심 화면 Screenshot Baseline

### UI·플랫폼

- 공통 Theme Resource·재사용 UI Scene
- 720×1280 외 안전 영역·태블릿·폴더블 대응
- 음악·효과음·진동·모션 감소·텍스트 크기 설정 저장
- Android 뒤로가기·pause·process-death
- 접근성·성능·외부 플레이

## 8. 구현 Gate

다음이 모두 충족되기 전 Codex BUILD를 열지 않는다.

```text
P0 planning findings = 0
P1 implementation-contract findings = 0 또는 명시적 defer
Base adapter operating integrity = PASS
GitHub canon ↔ Sheet = CROSS_SOURCE_VERIFIED
User 기획 완료 = DECLARED
Adversarial final review = PASS
User 검수 완료 = DECLARED
```

## 9. Production Gate

- 최신 제품 자동 계약·Godot E2E Green
- Android 실제 빌드·기기 증거
- 안전 영역·뒤로가기·중단 복구 증거
- 접근성 사람 검토
- 대표·최악 장면 성능
- 신규 플레이어 최소 6명 행동 검증
- 자산·라이선스 원장 완료
- 스토어 QA와 사업 범위 승인
