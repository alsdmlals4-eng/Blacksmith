# GUT 9.7.1 제거 절차

```text
SEPARATE_REVIEWED_CHANGE_ONLY
```

GUT 제거는 독립 Draft PR에서 수행한다. 테스트 실패를 숨기기 위한 즉시 삭제나 같은 PR의 무단 대체는 허용하지 않는다.

## 1. 선행 증거

- `addons/gut`의 source tag·commit·MIT license를 확인한다.
- `.gutconfig.json`, `tests/gut`, `.github/workflows/gut-validation.yml`의 consumer search를 수행한다.
- 프로젝트 문서·CI·스크립트에 남은 `gut_cmdln.gd`, `GutTest`, JUnit 참조를 목록화한다.
- 대체 테스트 권위와 Decision ID가 없다면 제거를 중단한다.

## 2. 테스트 이관

- `tests/gut/unit`과 `tests/gut/integration`의 각 계약을 대체 프레임워크 또는 승인된 직접 runner로 RED→GREEN 이관한다.
- zero test, skipped test, missing result를 성공으로 바꾸지 않는다.
- 과거 JUnit evidence, exact-head workflow run, RED/GREEN commit은 역사 증거로 보존한다.

## 3. 제거 순서

1. GUT 전용 workflow를 비활성화하거나 대체 workflow로 전환한다.
2. `.gutconfig.json` consumer를 제거한다.
3. `tests/gut` 테스트의 이관 readback을 확인한다.
4. `addons/gut` vendor를 삭제한다.
5. dependency·license·adoption registry를 갱신한다.
6. `project.godot` 변경이 필요하다면 HiGodot 저작 권위로만 수행한다.

현재 정식 채택은 editor plugin을 활성화하지 않으므로 `project.godot`의 GUT Plugin 제거는 기본적으로 필요하지 않다. 실제 상태를 다시 읽지 않고 추정 삭제하지 않는다.

## 4. 제거 후 검증

- consumer search 결과 0건 또는 승인된 역사 문서 참조만 남아야 한다.
- Godot 4.7.1 clean import와 parse를 수행한다.
- 기존 Python·직접 GDScript·Scene smoke 회귀를 수행한다.
- 추적 Scene·Resource·`project.godot` hash가 승인 범위 밖에서 바뀌지 않았는지 확인한다.
- clean import 뒤 working tree와 untracked 파일을 분류한다.
- JUnit evidence 보존 위치를 readback한다.

## 5. 실패 조건

- 테스트 이관 없이 `addons/gut` 삭제
- GUT 실패를 없애기 위해 workflow만 삭제
- HiGodot 외 도구가 `project.godot` Plugin 설정을 임의 수정
- 과거 JUnit evidence 삭제
- clean import 미실행
- 남은 consumer search 미실행

하나라도 발생하면 `GUT_REMOVAL_BLOCKED`다.
