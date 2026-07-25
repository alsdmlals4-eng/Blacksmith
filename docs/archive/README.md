# Blacksmith Archive

이 폴더는 역사 자료·호환 자료·검증 증거와 승인된 파생본을 복구 가능하게 보존한다.

- 이 폴더의 자료는 **현재 정본이 아니며 구현 권한이 없다**.
- 현재 정본은 `[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md`와 연결된 활성 문서에서 확인한다.
- 보존은 경로만 남기는 행위가 아니다. **원문을 비우지 않는다**.
- 비밀키·token·credential은 archive하지 않고 revoke·rotate·remove 절차로 처리한다.
- 모든 등록 항목은 `MANIFEST.json`에서 원래 경로, 현재 경로, 해시, 대체 정본, rollback 근거와 검증 상태를 기록한다.
- 이번 Base 공용 Skill 채택에서는 **기존 구형 자료를 이동·삭제·재작성하지 않는다**.
- archive를 기본 cold start, 현재 정본 라우팅 또는 직접 구현 지시의 근거로 사용하지 않는다.
