#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "usage: run_wsl_python_lane.sh <repo-linux-path> <expected-head> <output-linux-path>" >&2
  exit 2
fi

repo="$1"
expected_head="$2"
output="$3"

if ! command -v python3.12 >/dev/null 2>&1; then
  echo "python3.12 is required in WSL Ubuntu" >&2
  exit 3
fi
actual="$(python3.12 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$actual" != "3.12" ]]; then
  echo "expected Python 3.12, got $actual" >&2
  exit 4
fi

venv="/tmp/blacksmith-wsl-py312-${expected_head:0:12}"
rm -rf "$venv"
python3.12 -m venv "$venv"
trap 'rm -rf "$venv"' EXIT

"$venv/bin/python" -m pip install \
  --disable-pip-version-check \
  pytest==8.3.5

"$venv/bin/python" "$repo/tools/run_local_python_matrix_lane.py" \
  --repo-root "$repo" \
  --expected-head "$expected_head" \
  --lane-id wsl-ubuntu-py312 \
  --platform-kind wsl-ubuntu \
  --expected-python 3.12 \
  --scope code \
  --output "$output"
