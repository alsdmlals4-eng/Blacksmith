#!/usr/bin/env python3
"""Blacksmith PM entrypoint: reuse the explicitly selected Base tooling only.

This operational tooling pin is NOT the game's adopted Base release lock.
No receipts, project files, services or repository settings are mutated here.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys

PM_TOOLING_COMMIT = '96bee2700c8931b9262ad5a24a0664a400858f20'
REQUIRED_TOOLS = ('tools/validate_work_contract_receipt.py', 'tools/project_work_tracking.py')
IMPORTABLE_SUFFIXES = frozenset({'.py', '.pyc', '.pyo', '.pyd', '.so'})
SHA = re.compile(r'[0-9a-f]{40}\Z')


def _git(base: Path, *args: str, text: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ['git', '-C', str(base), *args],
        text=text,
        capture_output=True,
        check=False,
        timeout=30,
    )


def _tracked_tool_paths(base: Path, expected_commit: str) -> tuple[list[str], str | None]:
    listed = _git(base, 'ls-tree', '-r', '--name-only', '-z', expected_commit, '--', 'tools')
    if listed.returncode:
        return [], 'Base PM tools tree cannot be read from the selected commit'
    try:
        paths = [raw.decode('utf-8') for raw in listed.stdout.split(b'\0') if raw]
    except UnicodeDecodeError:
        return [], 'Base PM tools tree contains a non-UTF-8 path'
    if not paths:
        return [], 'Base PM selected commit has no tools tree'
    return paths, None


def check_tooling(base: Path, expected_commit: str = PM_TOOLING_COMMIT) -> list[str]:
    """Read-only exact-byte check of the selected source and its importable tools tree."""
    if not base.is_dir() or base.is_symlink():
        return ['Base PM checkout is missing or a symlink']
    try:
        top = _git(base, 'rev-parse', '--show-toplevel', text=True)
        head = _git(base, 'rev-parse', 'HEAD', text=True)
        if top.returncode or Path(top.stdout.strip()).resolve() != base.resolve():
            return ['Base PM path is not the repository root']
        if head.returncode or head.stdout.strip() != expected_commit:
            return ['Base PM checkout does not match the selected operational tooling commit']

        tracked_paths, path_error = _tracked_tool_paths(base, expected_commit)
        if path_error:
            return [path_error]
        tracked = set(tracked_paths)
        if any(path not in tracked for path in REQUIRED_TOOLS):
            return ['Base PM selected commit does not track every required executable file']

        # Verify every tracked tools file directly. Git index flags such as assume-unchanged
        # must not hide byte drift, including LF/CRLF conversion in executable sources.
        for relative in tracked_paths:
            actual_path = base / relative
            if not actual_path.is_file() or actual_path.is_symlink():
                return [f'Base PM tracked tools path is missing or a symlink: {relative}']
            source = _git(base, 'show', f'{expected_commit}:{relative}')
            if source.returncode or actual_path.read_bytes() != source.stdout:
                return [f'Base PM tools bytes differ from the selected commit: {relative}']

        # A sibling module can shadow stdlib or provider imports because the verified
        # entrypoint runs from this directory. Reject untracked importable artifacts,
        # including ignored bytecode, before starting Python.
        tools_root = base / 'tools'
        for candidate in tools_root.rglob('*'):
            if candidate.is_symlink():
                return [f'Base PM tools tree contains a symlink: {candidate.relative_to(base).as_posix()}']
            if not candidate.is_file():
                continue
            relative = candidate.relative_to(base).as_posix()
            if relative not in tracked and candidate.suffix.casefold() in IMPORTABLE_SUFFIXES:
                return [f'Base PM tools tree contains an untracked importable file: {relative}']
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return [f'Base PM identity check unavailable: {type(exc).__name__}']
    return []


def command(
    base: Path,
    receipt: Path,
    phase: str,
    source_sha: str,
    expected_head_sha: str | None = None,
) -> list[str]:
    if phase not in ('start', 'resume', 'closeout'):
        raise ValueError('phase must be start, resume or closeout')
    if not isinstance(source_sha, str) or SHA.fullmatch(source_sha) is None:
        raise ValueError('expected source must be a fresh-read 40-character project SHA')
    argv = [
        sys.executable,
        '-E',
        '-s',
        '-B',
        str(base / REQUIRED_TOOLS[0]),
        '--receipt',
        str(receipt),
        '--phase',
        phase,
        '--expected-source-sha',
        source_sha,
    ]
    if phase == 'closeout':
        if not isinstance(expected_head_sha, str) or SHA.fullmatch(expected_head_sha) is None:
            raise ValueError('closeout requires a fresh-read 40-character verified subject HEAD')
        argv.extend(['--expected-head-sha', expected_head_sha])
    elif expected_head_sha is not None:
        raise ValueError('expected head is accepted only for closeout')
    argv.append('--render-markdown')
    return argv


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-root', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--expected-source-sha', required=True)
    parser.add_argument('--expected-head-sha')
    parser.add_argument('--phase', choices=('start', 'resume', 'closeout'), default='start')
    args = parser.parse_args()
    errors = check_tooling(args.base_root)
    if errors:
        print('BLACKSMITH PM: BLOCKED_UNVERIFIED')
        for error in errors:
            print(f'- {error}')
        return 1
    try:
        argv = command(
            args.base_root,
            args.receipt,
            args.phase,
            args.expected_source_sha,
            args.expected_head_sha,
        )
        return subprocess.run(argv, check=False, timeout=120).returncode
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'BLACKSMITH PM: BLOCKED_UNVERIFIED — {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
