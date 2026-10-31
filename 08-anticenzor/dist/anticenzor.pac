// ============================================================
// Anticenzor -- selective-routing PAC script (GENERATED FILE).
// DO NOT EDIT BY HAND: rebuild with src/build.py.
//   source list: data/domains.txt + data/sources.d/*.txt
//   config:      data/config.json (proxy chain + fallback)
//
// Principle (repo: 07-prototypes/pid1-manifest.md): the human is
// PID 1 -- the human writes the rules; the corporation serves;
// the default route is DIRECT. No telemetry: this file is plain
// local JS, readable, revocable in one click.
//
// Practices applied (MDN "Proxy Auto-Configuration (PAC) file",
// Wikipedia "Proxy auto-config", Chromium "Secure Web Proxy"):
//   * no dnsResolve / isResolvable / isInNet / myIpAddress:
//     those call DNS per request and can stall the whole
//     browser; matching is done on the host name only;
//   * no shExpMatch: glob support differs between engines;
//   * top-level FindProxyForURL plus FindProxyForURLEx wrapper
//     for extended-PAC stacks (no async extensions used);
//   * host param carries no port per MDN; defensive port strip
//     kept for legacy engines; trailing FQDN dot handled;
//   * single-label hosts and private/literal IPs go DIRECT;
//   * return chain order = preference order; last item = fallback;
//   * pure ASCII body: works on every engine (UTF-8 PAC files
//     are Firefox 66+ only).
// ============================================================

// --- Configuration (injected by build.py) ---
var AC_PROXY_CHAIN = ["PROXY ac-proxy.example.org:3128", "SOCKS5 127.0.0.1:1080"];
var AC_FALLBACK = "DIRECT";

// --- Suffix map (injected by build.py) ---
// "example.org"      -> domain and all subdomains via the chain
// "!img.example.org" -> exception: that suffix goes DIRECT
// Longest match wins: the LAST (most specific) key hit decides.
var AC_SUFFIX = {"!img.example.org":1,"example.net":1,"example.org":1,"xn--e1afmkfd.xn--p1ai":1};

function acCleanHost(host) {
  var h = String(host).toLowerCase();
  var p = h.indexOf(':');
  if (p !== -1) {
    var rest = h.substring(p + 1);
    var singleColon = h.indexOf(':', p + 1) === -1;
    var allDigits = /^\d+$/.test(rest);
    if (singleColon && allDigits) {
      h = h.substring(0, p); // legacy "host:port"; IPv6 literals untouched
    }
  }
  if (h.length > 0 && h.charAt(h.length - 1) === '.') {
    h = h.substring(0, h.length - 1); // FQDN trailing dot
  }
  return h;
}

function acIsLiteralIp(h) {
  return /^(\d{1,3}\.){3}\d{1,3}$/.test(h) || h.indexOf(':') !== -1;
}

function acIsPrivateIp(h) {
  var m = /^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/.exec(h);
  if (m) {
    var a = +m[1], b = +m[2];
    if (a > 255 || b > 255) return true;                 // malformed literal
    if (a === 0 || a === 10 || a === 127) return true;   // 0/8, 10/8, 127/8
    if (a === 172 && b >= 16 && b <= 31) return true;    // 172.16/12
    if (a === 192 && b === 168) return true;             // 192.168/16
    if (a === 169 && b === 254) return true;             // link-local 169.254/16
    if (a === 100 && b >= 64 && b <= 127) return true;   // CGNAT 100.64/10
    return false;
  }
  if (h.indexOf(':') !== -1) {                           // IPv6
    var t = h.toLowerCase();
    if (t === '::' || t === '::1') return true;
    if (t.substring(0, 5) === 'fe80:') return true;      // link-local fe80::/10
    if (t.charAt(0) === 'f' && (t.charAt(1) === 'c' || t.charAt(1) === 'd')) return true; // ULA fc00::/7
    return false;
  }
  return false;
}

// Right-to-left longest match over dot labels.
function acInSuffixSet(h) {
  var labels = h.split('.');
  var probe = '';
  var decision = false;
  for (var i = labels.length - 1; i >= 0; i--) {
    probe = labels[i] + (probe ? '.' + probe : '');
    if (AC_SUFFIX.hasOwnProperty(probe)) decision = true;
    if (AC_SUFFIX.hasOwnProperty('!' + probe)) decision = false;
  }
  return decision;
}

function acChain() {
  return AC_PROXY_CHAIN.join('; ') + '; ' + AC_FALLBACK;
}

function FindProxyForURL(url, host) {
  var h = acCleanHost(host);
  if (!h) return 'DIRECT';
  if (h.indexOf('.') === -1 && h.indexOf(':') === -1) return 'DIRECT'; // single label
  if (acIsLiteralIp(h)) {
    if (acIsPrivateIp(h)) return 'DIRECT';
    // public literal IPs: the full string is the last probe of the walk,
    // so listing e.g. "203.0.113.7" in the map routes it via the chain
  }
  if (acInSuffixSet(h)) return acChain();
  return AC_FALLBACK;
}

// Extended-PAC stacks (WinHTTP-era entry point) get an identical wrapper.
// dnsResolveEx is deliberately NOT used -- see header practices.
function FindProxyForURLEx(url, host) {
  return FindProxyForURL(url, host);
}
