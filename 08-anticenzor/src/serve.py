#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Anticenzor PAC local server.

Canonical MIME for PAC: application/x-ns-proxy-autoconfig
(default bind is 127.0.0.1 on purpose). For production put
dist/anticenzor.pac behind an HTTPS server (Caddy/nginx example
in README): a PAC fetched over plain HTTP can be MITM-replaced
and redirect ALL browser traffic.
"""
import argparse
import functools
import pathlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PAC_MIME = 'application/x-ns-proxy-autoconfig'


class PacHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if str(path).endswith('.pac'):
            return PAC_MIME
        return super().guess_type(path)

    def end_headers(self):
        self.send_header('Cache-Control', 'public, max-age=300')
        super().end_headers()


def main():
    ap = argparse.ArgumentParser(description='Serve the generated PAC file locally')
    ap.add_argument('--file', default='dist/anticenzor.pac')
    ap.add_argument('--port', type=int, default=8080)
    ap.add_argument('--bind', default='127.0.0.1')
    args = ap.parse_args()

    pac = pathlib.Path(args.file).resolve()
    if not pac.is_file():
        raise SystemExit(f'not found: {pac} (run: python3 src/build.py)')
    handler = functools.partial(PacHandler, directory=str(pac.parent))
    print(f'PAC URL: http://{args.bind}:{args.port}/{pac.name}')
    print(f'MIME:    {PAC_MIME}')
    ThreadingHTTPServer((args.bind, args.port), handler).serve_forever()


if __name__ == '__main__':
    main()
