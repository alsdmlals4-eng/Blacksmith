# GitHub Actions Public Standard Runner Policy

Decision: `BS-OPS-20260807-02`

## 목적

Blacksmith의 자동 검증을 public 저장소의 표준 GitHub-hosted runner에서 단순하고 반복 가능하게 실행한다. 검증 Gate는 유지하고 실행 장소만 기존 GitHub Actions로 복원한다.

## 허용 실행기

```text
ubuntu-latest
windows-latest
```

다음 실행기는 별도 Decision과 비용 검토 없이 사용할 수 없다.

```text
larger runner
GPU runner
custom image runner
self-hosted runner
```

## Pull Request 검증

1. PR을 생성하거나 새 commit을 push한다.
2. 기존 PR validation과 reusable workflow가 실행되는지 확인한다.
3. exact PR HEAD의 checks와 workflow run을 읽는다.
4. 실패 시 GitHub job log를 먼저 읽고 필요한 failure artifact만 확인한다.
5. 필수 Gate가 모두 PASS이기 전에는 Ready 또는 merge로 전환하지 않는다.

## 전체 수동 검증

1. GitHub 저장소에서 `Actions`를 연다.
2. `Full validation`을 선택한다.
3. `Run workflow`를 누른다.
4. 검증 대상 branch를 선택한다.
5. 실행 후 Ubuntu·Windows Python matrix, Base governance, Godot full suite 결과를 확인한다.

`Full validation`은 다음 matrix를 소유한다.

```text
Ubuntu Python 3.11 / 3.12 / 3.13
Windows Python 3.11 / 3.12 / 3.13
Ubuntu pinned Base governance
Ubuntu Godot 4.7.1 full suite
```

GUT 9.7.1 formal authority는 전용 `gut-validation.yml`과 기존 호출 경로를 유지한다.

## 비용 방어

- public 저장소의 표준 hosted runner만 사용한다.
- larger runner label을 추가하지 않는다.
- 모든 `actions/upload-artifact@v4` 호출은 `retention-days: 1`을 사용한다.
- failure artifact는 실패 원인 확인에 필요한 파일만 포함한다.
- `cancel-in-progress: true`를 유지해 같은 ref의 중복 실행을 취소한다.
- 로그로 충분한 증거는 artifact로 중복 업로드하지 않는다.

## 증거 규칙

검증 완료 판정에는 다음을 기록한다.

- workflow 이름
- run ID
- 검증 ref와 exact SHA
- 각 필수 job 결론
- 실패 시 첫 실패 step과 log 요약
- artifact가 있으면 이름과 만료 정책

## PR #127 처리

Windows+WSL2 로컬 검증팩 PR #127은 병합하지 않는다.

```text
SUPERSEDED_BY_BS_OPS_20260807_02
CLOSED_WITHOUT_MERGE
HISTORICAL_EXPERIMENT_ONLY
```

로컬 pack 재실행이나 manifest 완성은 더 이상 merge 전제조건이 아니다.

## 변경 관리

저장소가 private으로 전환되거나 standard runner 정책·비용 조건이 바뀌면 이 정책을 즉시 재검토한다. larger runner 또는 self-hosted runner 도입은 새로운 Decision ID가 필요하다.
