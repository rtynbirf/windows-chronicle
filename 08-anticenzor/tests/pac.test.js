'use strict';
// Anticenzor PAC vectors. Run: node tests/pac.test.js
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const src = fs.readFileSync(path.join(ROOT, 'dist', 'anticenzor.pac'), 'utf8');
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'config.json'), 'utf8'));
const CHAIN = cfg.proxy_chain.join('; ') + '; ' + cfg.fallback;
const DIRECT = 'DIRECT';

const api = new Function(src + '\n;return { f: FindProxyForURL, x: FindProxyForURLEx };')();
const FindProxyForURL = api.f;
if (typeof api.x !== 'function') throw new Error('FindProxyForURLEx missing');

const cases = [
  ['http://example.org/', 'example.org', CHAIN],
  ['http://www.example.org/', 'www.example.org', CHAIN],
  ['http://a.b.example.org/', 'a.b.example.org', CHAIN],
  ['http://EXAMPLE.ORG/', 'EXAMPLE.ORG', CHAIN],            // case-insensitive
  ['http://example.org./', 'example.org.', CHAIN],          // FQDN trailing dot
  ['http://example.org:8080/', 'example.org:8080', CHAIN],  // legacy engine sends port
  ['http://example.net/', 'example.net', CHAIN],
  ['http://xn--e1afmkfd.xn--p1ai/', 'xn--e1afmkfd.xn--p1ai', CHAIN], // пример.рф
  ['http://img.example.org/', 'img.example.org', DIRECT],   // exception wins
  ['http://other.test/', 'other.test', DIRECT],
  ['http://sub.other.test/', 'sub.other.test', DIRECT],
  ['http://192.168.1.1/', '192.168.1.1', DIRECT],
  ['http://10.0.0.5/', '10.0.0.5', DIRECT],
  ['http://172.16.0.9/', '172.16.0.9', DIRECT],
  ['http://169.254.3.3/', '169.254.3.3', DIRECT],           // link-local
  ['http://100.100.1.1/', '100.100.1.1', DIRECT],           // CGNAT
  ['http://8.8.8.8/', '8.8.8.8', DIRECT],                   // public literal, not listed
  ['http://intranet/', 'intranet', DIRECT],                 // single label
  ['http://[::1]/', '::1', DIRECT],
  ['http://[fe80::1]/', 'fe80::1', DIRECT],
  ['http://[2001:db8::1]/', '2001:db8::1', DIRECT],         // public IPv6, not listed
];

let failed = 0;
for (const [url, host, want] of cases) {
  const got = FindProxyForURL(url, host);
  const ok = got === want;
  if (!ok) failed += 1;
  console.log((ok ? 'PASS' : 'FAIL') + ' | ' + host.padEnd(26) + ' -> ' + got +
              (ok ? '' : '  (want: ' + want + ')'));
}

const ex = api.x('http://example.org/', 'example.org');
if (ex !== CHAIN) {
  failed += 1;
  console.log('FAIL | FindProxyForURLEx mismatch: ' + ex);
} else {
  console.log('PASS | FindProxyForURLEx agrees with FindProxyForURL');
}

console.log(failed === 0
  ? 'ALL ' + (cases.length + 1) + ' CHECKS PASSED'
  : failed + ' CHECK(S) FAILED');
process.exit(failed === 0 ? 0 : 1);
