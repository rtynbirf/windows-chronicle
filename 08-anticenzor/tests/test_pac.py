#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anticenzor test runner: build + structural checks + JS vectors (node).

Run: python3 tests/test_pac.py
"""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def run(cmd):
    print('$', ' '.join(map(str, cmd)))
    return subprocess.run([str(c) for c in cmd], cwd=ROOT)


def main():
    r = run([sys.executable, 'src/build.py'])
    assert r.returncode == 0, 'build failed'

    pac = (ROOT / 'dist' / 'anticenzor.pac').read_text(encoding='ascii')
    assert pac.count('{') == pac.count('}'), 'unbalanced braces'
    for name in ('FindProxyForURL', 'FindProxyForURLEx', 'DIRECT'):
        assert name in pac, f'missing: {name}'
    for bad in ('NaN', 'undefined', '/*@'):
        assert bad not in pac, f'garbage in artifact: {bad}'

    node = shutil.which('node')
    if node:
        r = run([node, 'tests/pac.test.js'])
        assert r.returncode == 0, 'JS vectors failed'
    else:
        print('node not found -- JS vectors skipped (structural checks passed)')

    print('ALL CHECKS PASSED')


if __name__ == '__main__':
    main()
