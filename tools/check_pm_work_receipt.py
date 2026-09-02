#!/usr/bin/env python3
"""Blacksmith PM entrypoint: reuse the explicitly selected Base tooling only.

This operational tooling pin is NOT the game's adopted Base release lock.
No receipts, project files, services or repository settings are mutated here.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

PM_TOOLING_COMMIT = '96bee2700c8931b9262ad5a24a0664a400858f20'
REQUIRED_TOOLS = ('tools/validate_work_contract_receipt.py', 'tools/project_work_tracking.py')
IMPORTABLE_SUFFIXES = frozenset({'.py', '.pyc', '.pyo', '.pyd', '.so'})
SHA = re.compile(r'[0-9a-f]{40}\Z')


def _git(base: Path, *args: str, text: bool = False) -> subprocess.CompletedProcess:
    environment = os.environ.copy()
    environment['GIT_NO_REPLACE_OBJECTS'] = '1'
    return subprocess.run(
        ['git', '-C', str(base), *args],
        text=text,
        capture_output=True,
        check=False,
        timeout=30,
        env=environment,
    )


def _decode_path(raw_path: bytes, *, subject: str) -> tuple[str | None, str | None]:
    try:
        return raw_path.decode('utf-8'), None
    except UnicodeDecodeError:
        return None, f'{subject} contains a non-UTF-8 path'


def _tracked_tool_entries(
    base: Path,
    expected_commit: str,
) -> tuple[dict[str, tuple[str, str]], str | None]:
    """Return path -> (mode, object ID) from the pinned commit tree."""
    listed = _git(base, 'ls-tree', '-r', '-z', expected_commit, '--', 'tools')
    if listed.returncode:
        return {}, 'Base PM tools tree cannot be read from the selected commit'
    entries: dict[str, tuple[str, str]] = {}
    for record in listed.stdout.split(b'\0'):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b'\t', 1)
            mode_raw, type_raw, object_raw = metadata.split()
            mode = mode_raw.decode('ascii')
            object_type = type_raw.decode('ascii')
            object_id = object_raw.decode('ascii')
        except (ValueError, UnicodeDecodeError):
            return {}, 'Base PM tools tree contains a malformed entry'
        path, error = _decode_path(raw_path, subject='Base PM tools tree')
        if error:
            return {}, error
        if object_type != 'blob' or SHA.fullmatch(object_id) is None:
            return {}, f'Base PM tools tree contains a non-blob or invalid object: {path}'
        if path in entries:
            return {}, f'Base PM tools tree contains a duplicate path: {path}'
        entries[path] = (mode, object_id)
    if not entries:
        return {}, 'Base PM selected commit has no tools tree'
    return entries, None


def _indexed_tool_entries(
    base: Path,
) -> tuple[dict[str, tuple[str, str]], str | None]:
    """Return exact stage-0 path -> (mode, object ID) from the current index."""
    listed = _git(base, 'ls-files', '--stage', '-z', '--', 'tools')
    if listed.returncode:
        return {}, 'Base PM current tools index cannot be read'
    entries: dict[str, tuple[str, str]] = {}
    for record in listed.stdout.split(b'\0'):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b'\t', 1)
            mode_raw, object_raw, stage_raw = metadata.split()
            mode = mode_raw.decode('ascii')
            object_id = object_raw.decode('ascii')
            stage = stage_raw.decode('ascii')
        except (ValueError, UnicodeDecodeError):
            return {}, 'Base PM current tools index contains a malformed entry'
        path, error = _decode_path(raw_path, subject='Base PM current tools index')
        if error:
            return {}, error
        if stage != '0':
            return {}, f'Base PM current tools index contains an unmerged stage for {path}'
        if SHA.fullmatch(object_id) is None:
            return {}, f'Base PM current tools index contains an invalid object for {path}'
        if path in entries:
            return {}, f'Base PM current tools index contains a duplicate path: {path}'
        entries[path] = (mode, object_id)
    return entries, None


def check_tooling(base: Path, expected_commit: str = PM_TOOLING_COMMIT) -> list[str]:
    """Read-only exact check of commit tree, stage-0 index and importable worktree."""
    if not base.is_dir() or base.is_symlink():
        return ['Base PM checkout is missing or a symlink']
    try:
        top = _git(base, 'rev-parse', '--show-toplevel', text=True)
        head = _git(base, 'rev-parse', 'HEAD', text=True)
        if top.returncode or Path(top.stdout.strip()).resolve() != base.resolve():
            return ['Base PM path is not the repository root']
        if head.returncode or head.stdout.strip() != expected_commit:
            return ['Base PM checkout does not match the selected operational tooling commit']

        tracked_entries, tree_error = _tracked_tool_entries(base, expected_commit)
        if tree_error:
            return [tree_error]
        if any(path not in tracked_entries for path in REQUIRED_TOOLS):
            return ['Base PM selected commit does not track every required executable file']

        indexed_entries, index_error = _indexed_tool_entries(base)
        if index_error:
            return [index_error]
        if indexed_entries != tracked_entries:
            return [
                'Base PM current tools index mode/object/path entries differ from '
                'the selected commit tree'
            ]

        # Verify every tracked tools file directly. Git index flags such as assume-unchanged
        # must not hide byte drift, including LF/CRLF conversion in executable sources.
        for relative, (_, object_id) in tracked_entries.items():
            actual_path = base / relative
            if not actual_path.is_file() or actual_path.is_symlink():
                return [f'Base PM tracked tools path is missing or a symlink: {relative}']
            source = _git(base, 'cat-file', 'blob', object_id)
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
            if relative not in tracked_entries and candidate.suffix.casefold() in IMPORTABLE_SUFFIXES:
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
