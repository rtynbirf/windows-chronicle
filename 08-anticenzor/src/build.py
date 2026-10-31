#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Anticenzor PAC builder.

Input:  data/domains.txt + data/sources.d/*.txt + data/config.json
Output: dist/anticenzor.pac (pure ASCII, deterministic) + sha256 sidecar

Rules:
  example.org        -> domain and all subdomains via the proxy chain
  !img.example.org   -> exception: that suffix goes DIRECT (longest match wins)
  203.0.113.7        -> literal IPv4 is allowed too
  пример.рф          -> IDN converted to punycode automatically
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN_RE = re.compile(r'^(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))*$')
IPV4_RE = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')


def to_ascii(domain: str) -> str:
    if IPV4_RE.match(domain):
        return domain
    try:
        return domain.encode('idna').decode('ascii').lower()
    except UnicodeError as exc:
        sys.exit(f'BUILD ERROR (IDN): {domain!r}: {exc}')


def collect_entries() -> dict:
    files = sorted((ROOT / 'data').glob('*.txt')) + \
            sorted((ROOT / 'data' / 'sources.d').glob('*.txt'))
    entries: dict = {}
    for f in files:
        for n, raw in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            neg = line.startswith('!')
            dom = to_ascii((line[1:] if neg else line).lower().lstrip('.'))
            if not DOMAIN_RE.match(dom):
                sys.exit(f'BUILD ERROR: bad domain {line!r} ({f.name}:{n})')
            entries[('!' + dom) if neg else dom] = 1
    return entries


def main() -> None:
    cfg = json.loads((ROOT / 'data' / 'config.json').read_text(encoding='utf-8'))
    chain = [str(p) for p in cfg['proxy_chain']]
    fallback = str(cfg.get('fallback', 'DIRECT'))
    for p in chain + [fallback]:
        if ';' in p:
            sys.exit(f'BUILD ERROR: semicolon forbidden in proxy entry {p!r}')
    entries = collect_entries()
    if not entries:
        sys.exit('BUILD ERROR: empty domain set')

    tpl = (ROOT / 'src' / 'template.pac.js').read_text(encoding='utf-8')
    out = (tpl
           .replace('/*@PROXY_CHAIN@*/', json.dumps(chain, ensure_ascii=True))
           .replace('/*@FALLBACK@*/', json.dumps(fallback, ensure_ascii=True))
           .replace('/*@SUFFIX_SET@*/', json.dumps(entries, ensure_ascii=True,
                                                   sort_keys=True,
                                                   separators=(',', ':'))))
    if not out.isascii():
        sys.exit('BUILD ERROR: generated PAC must be pure ASCII (engine compat)')

    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    target = dist / 'anticenzor.pac'
    target.write_text(out, encoding='ascii')
    sha = hashlib.sha256(out.encode('ascii')).hexdigest()
    (dist / 'anticenzor.pac.sha256').write_text(sha + '  anticenzor.pac\n',
                                                encoding='ascii')
    print(f'OK: {len(entries)} entries, {len(out)} bytes')
    print(f'sha256: {sha}')
    print(f'cache-buster: ?v={sha[:12]}')


if __name__ == '__main__':
    main()
