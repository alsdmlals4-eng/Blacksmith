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

PM_TOOLING_COMMIT = 'f27fe4b993e8ffc24db235cda05d0782f6a1308c'
REQUIRED_TOOLS = ('tools/validate_work_contract_receipt.py', 'tools/project_work_tracking.py')
SHA = re.compile(r'[0-9a-f]{40}\Z')


def check_tooling(base: Path, expected_commit: str = PM_TOOLING_COMMIT) -> list[str]:
    """Read-only check of exact source and executable file cleanliness."""
    if not base.is_dir() or base.is_symlink():
        return ['Base PM checkout is missing or a symlink']
    if any(not (base / path).is_file() or (base / path).is_symlink() for path in REQUIRED_TOOLS):
        return ['Base PM executable files are missing or symlinks']
    try:
        def git(*args: str) -> subprocess.CompletedProcess[str]:
            return subprocess.run(['git', '-C', str(base), *args], text=True,
                                  capture_output=True, check=False, timeout=15)
        top = git('rev-parse', '--show-toplevel')
        head = git('rev-parse', 'HEAD')
        if top.returncode or Path(top.stdout.strip()).resolve() != base.resolve():
            return ['Base PM path is not the repository root']
        if head.returncode or head.stdout.strip() != expected_commit:
            return ['Base PM checkout does not match the selected operational tooling commit']
        tracked = git('ls-files', '--error-unmatch', '--', *REQUIRED_TOOLS)
        clean = git('diff', '--quiet', 'HEAD', '--', *REQUIRED_TOOLS)
        if tracked.returncode or clean.returncode:
            return ['Base PM executable files differ from the exact tracked commit']
        # Index flags may hide edits from git diff; compare actual executable bytes.
        for path in REQUIRED_TOOLS:
            source = subprocess.run(['git', '-C', str(base), 'show', f'{expected_commit}:{path}'], capture_output=True, check=False, timeout=15)
            actual = (base / path).read_bytes().replace(b'\r\n', b'\n')
            if source.returncode or actual != source.stdout.replace(b'\r\n', b'\n'):
                return ['Base PM executable bytes differ from the selected commit']
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return [f'Base PM identity check unavailable: {type(exc).__name__}']
    return []


def command(base: Path, receipt: Path, phase: str, source_sha: str) -> list[str]:
    if phase not in ('start', 'resume', 'closeout'):
        raise ValueError('phase must be start, resume or closeout')
    if not isinstance(source_sha, str) or SHA.fullmatch(source_sha) is None:
        raise ValueError('expected source must be a fresh-read 40-character project SHA')
    return [sys.executable, str(base / REQUIRED_TOOLS[0]), '--receipt', str(receipt),
            '--phase', phase, '--expected-source-sha', source_sha, '--render-markdown']


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-root', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--expected-source-sha', required=True)
    parser.add_argument('--phase', choices=('start', 'resume', 'closeout'), default='start')
    args = parser.parse_args()
    errors = check_tooling(args.base_root)
    if errors:
        print('BLACKSMITH PM: BLOCKED_UNVERIFIED')
        for error in errors:
            print(f'- {error}')
        return 1
    try:
        return subprocess.run(command(args.base_root, args.receipt, args.phase, args.expected_source_sha),
                              check=False, timeout=120).returncode
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'BLACKSMITH PM: BLOCKED_UNVERIFIED — {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
