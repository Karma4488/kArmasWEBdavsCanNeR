#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗  ██╗ █████╗ ██████╗███╗   ███╗ █████╗ ███████╗
██║ ██╔╝██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔════╝
█████╔╝ ███████║██████╔╝██╔████╔██║███████║███████╗
██╔═██╗ ██╔══██║██╔══██╗██║╚██╔╝██║██╔══██║╚════██║
██║  ██╗██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║███████║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝
██╗    ██╗███████╗██████╗ ██████╗  █████╗ ██╗   ██╗
██║    ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║   ██║
██║ █╗ ██║█████╗  ██████╔╝██║  ██║███████║██║   ██║
██║███╗██║██╔══╝  ██╔══██╗██║  ██║██╔══██║╚██╗ ██╔╝
╚███╔███╔╝███████╗██████╔╝██████╔╝██║  ██║ ╚████╔╝ 
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  
 ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
 ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
 ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
 ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
 ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝

        kArmasWEBdavsCanNeR v1.0 — WebDAV Upload Vulnerability Scanner
              We Are Legion. We Do Not Forget. We Do Not Forgive.
"""

import sys
import os
import time
import random
import socket
import threading
import urllib.request
import urllib.error
import urllib.parse
import http.client
import ssl
import base64
import json
import argparse
import datetime
from collections import defaultdict

# ─── ANSI COLOR CODES ─────────────────────────────────────────────────────────
class C:
    GREEN   = '\033[92m'
    RED     = '\033[91m'
    YELLOW  = '\033[93m'
    CYAN    = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE    = '\033[94m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'
    BLINK   = '\033[5m'

def c(color, text): return f"{color}{text}{C.RESET}"

# ─── MATRIX RAIN ──────────────────────────────────────────────────────────────
def matrix_rain(duration=2.5):
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ@#$%&"
    try:
        cols = os.get_terminal_size().columns
    except:
        cols = 80
    streams = [0] * cols
    end_time = time.time() + duration
    while time.time() < end_time:
        line = ""
        for i in range(cols):
            if random.random() < 0.04:
                streams[i] = random.randint(5, 20)
            if streams[i] > 0:
                ch = random.choice(chars)
                line += c(C.GREEN, ch) if random.random() > 0.1 else c(C.WHITE + C.BOLD, ch)
                streams[i] -= 1
            else:
                line += " "
        print(line[:cols], end="\r\n")
        time.sleep(0.04)
    print(C.RESET)

# ─── SKULL ────────────────────────────────────────────────────────────────────
SKULL = r"""
        ░░░░░░░░░░░░░░░░░░░░
      ░░  ░░░░░░░░░░░░░░  ░░
    ░░  ░░                ░░  ░░
   ░░  ░░   ████  ████    ░░  ░░
   ░░ ░░   ██░░██ ██░░██   ░░ ░░
   ░░ ░░   ██  ██ ██  ██   ░░ ░░
   ░░  ░░   ████   ████   ░░  ░░
    ░░   ░░░░░░░░░░░░░░░░░░   ░░
    ░░     ░░   ░░   ░░       ░░
     ░░░░  ░░░░░░░░░░░░  ░░░░░
          ░░░░░░░░░░░░░░░
"""

def print_banner():
    matrix_rain(2.0)
    print(c(C.GREEN + C.BOLD, SKULL))
    lines = __doc__.split('\n')
    for line in lines[1:]:
        print(c(C.GREEN, line))
    time.sleep(0.3)

# ─── LOGGING ──────────────────────────────────────────────────────────────────
LOG_LOCK = threading.Lock()
findings = []

def log(level, msg, indent=0):
    prefix = "  " * indent
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    ts_str = c(C.DIM, f"[{ts}]")
    if level == "INFO":
        tag = c(C.CYAN + C.BOLD, "[*]")
    elif level == "OK":
        tag = c(C.GREEN + C.BOLD, "[+]")
    elif level == "WARN":
        tag = c(C.YELLOW + C.BOLD, "[!]")
    elif level == "VULN":
        tag = c(C.RED + C.BOLD + C.BLINK, "[VULN]")
    elif level == "ERR":
        tag = c(C.RED, "[-]")
    elif level == "SECTION":
        print()
        print(c(C.MAGENTA + C.BOLD, f"  ┌─── {msg} ───"))
        return
    elif level == "END":
        print(c(C.MAGENTA + C.BOLD, f"  └─────────────────────────────────"))
        return
    else:
        tag = c(C.WHITE, "[?]")
    with LOG_LOCK:
        print(f"{ts_str} {prefix}{tag} {msg}")

def add_finding(severity, title, detail, url=""):
    findings.append({"severity": severity, "title": title, "detail": detail, "url": url})
    if severity == "CRITICAL":
        log("VULN", f"{c(C.RED+C.BOLD, 'CRITICAL')} — {c(C.WHITE+C.BOLD, title)}")
    elif severity == "HIGH":
        log("VULN", f"{c(C.YELLOW+C.BOLD, 'HIGH')} — {c(C.WHITE, title)}")
    elif severity == "MEDIUM":
        log("WARN", f"{c(C.YELLOW, 'MEDIUM')} — {title}")
    else:
        log("OK", f"{c(C.CYAN, 'LOW/INFO')} — {title}")

# ─── HTTP HELPER ──────────────────────────────────────────────────────────────
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE

class WebDAVClient:
    def __init__(self, base_url, timeout=10, auth=None, user_agent=None, proxy=None):
        parsed = urllib.parse.urlparse(base_url)
        self.scheme   = parsed.scheme.lower()
        self.host     = parsed.hostname
        self.port     = parsed.port or (443 if self.scheme == "https" else 80)
        self.base_path = parsed.path.rstrip("/") or ""
        self.base_url  = base_url.rstrip("/")
        self.timeout   = timeout
        self.auth      = auth   # (user, pass) or None
        self.user_agent = user_agent or "Mozilla/5.0 (kArmasWEBdavsCanNeR/1.0)"
        self.proxy     = proxy

    def _conn(self):
        if self.scheme == "https":
            return http.client.HTTPSConnection(self.host, self.port, timeout=self.timeout, context=CTX)
        else:
            return http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)

    def _headers(self, extra=None):
        h = {"User-Agent": self.user_agent, "Connection": "close"}
        if self.auth:
            creds = base64.b64encode(f"{self.auth[0]}:{self.auth[1]}".encode()).decode()
            h["Authorization"] = f"Basic {creds}"
        if extra:
            h.update(extra)
        return h

    def request(self, method, path, body=None, extra_headers=None):
        """Returns (status, headers_dict, body_bytes) or raises."""
        conn = self._conn()
        try:
            headers = self._headers(extra_headers)
            if body is not None and "Content-Length" not in headers:
                headers["Content-Length"] = str(len(body) if body else 0)
            conn.request(method, path, body=body, headers=headers)
            resp = conn.getresponse()
            resp_body = resp.read(8192)
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            return resp.status, resp_headers, resp_body
        finally:
            conn.close()

    def full_path(self, suffix=""):
        return self.base_path + "/" + suffix.lstrip("/") if suffix else self.base_path or "/"

# ─── TEST MODULES ─────────────────────────────────────────────────────────────

def test_options(client, path="/"):
    """Check OPTIONS response for DAV headers and allowed methods."""
    log("SECTION", "OPTIONS / DAV Capability Check")
    fpath = client.full_path(path)
    try:
        status, headers, body = client.request("OPTIONS", fpath)
        log("INFO", f"OPTIONS {fpath} → HTTP {status}", 1)
        dav_header = headers.get("dav", "")
        allow_header = headers.get("allow", "")
        ms_author = headers.get("ms-author-via", "")
        server = headers.get("server", "unknown")

        log("INFO", f"Server: {c(C.WHITE, server)}", 1)

        if dav_header:
            log("OK", f"DAV header present: {c(C.WHITE, dav_header)}", 1)
            add_finding("LOW", "WebDAV Enabled", f"DAV: {dav_header}", client.base_url)
        else:
            log("INFO", "No DAV header found — may not be WebDAV", 1)

        if allow_header:
            log("INFO", f"Allowed methods: {c(C.CYAN, allow_header)}", 1)

        dangerous = []
        for m in ["PUT", "DELETE", "MOVE", "COPY", "MKCOL", "PROPPATCH", "LOCK", "UNLOCK"]:
            if m in allow_header.upper():
                dangerous.append(m)

        if dangerous:
            log("WARN", f"Dangerous methods advertised: {c(C.YELLOW+C.BOLD, ', '.join(dangerous))}", 1)
            add_finding("MEDIUM", "Dangerous HTTP Methods Advertised",
                        f"Methods: {', '.join(dangerous)}", client.base_url)

        if "PUT" in allow_header.upper():
            add_finding("HIGH", "HTTP PUT Advertised in OPTIONS",
                        "Server explicitly allows PUT uploads via OPTIONS", client.base_url)

        if ms_author:
            log("INFO", f"MS-Author-Via: {ms_author}", 1)

        return status, dav_header, allow_header
    except Exception as e:
        log("ERR", f"OPTIONS failed: {e}", 1)
        return None, "", ""
    finally:
        log("END", "")


def test_propfind(client, path="/"):
    """PROPFIND to enumerate directory listings."""
    log("SECTION", "PROPFIND Directory Enumeration")
    fpath = client.full_path(path)
    body = b'<?xml version="1.0" encoding="utf-8"?><D:propfind xmlns:D="DAV:"><D:allprop/></D:propfind>'
    try:
        status, headers, resp_body = client.request(
            "PROPFIND", fpath, body=body,
            extra_headers={"Depth": "1", "Content-Type": "application/xml"}
        )
        log("INFO", f"PROPFIND {fpath} → HTTP {status}", 1)
        if status in (207, 200):
            log("OK" if status == 207 else "WARN",
                f"Server responded to PROPFIND (status={status})", 1)
            decoded = resp_body.decode("utf-8", errors="replace")
            # Count <D:response> elements as a proxy for listed resources
            entries = decoded.count("<D:response") + decoded.count("<d:response")
            if entries > 1:
                log("WARN", f"Directory listing returned ~{entries} entries", 1)
                add_finding("MEDIUM", "PROPFIND Directory Listing Enabled",
                            f"PROPFIND returned {entries} resource entries — directory browsing possible",
                            client.base_url + fpath)
            else:
                log("INFO", "PROPFIND returned minimal data", 1)
        elif status == 401:
            log("WARN", "PROPFIND requires authentication (401)", 1)
        elif status == 403:
            log("INFO", "PROPFIND forbidden (403)", 1)
        elif status == 405:
            log("INFO", "PROPFIND not allowed (405) — WebDAV may be disabled", 1)
        else:
            log("INFO", f"PROPFIND returned {status}", 1)
        return status
    except Exception as e:
        log("ERR", f"PROPFIND failed: {e}", 1)
        return None
    finally:
        log("END", "")


def test_put_upload(client, path="/"):
    """Attempt to PUT a harmless text file."""
    log("SECTION", "PUT Upload Test (Unauthenticated)")
    filename = f"kArmas_test_{int(time.time())}.txt"
    fpath = client.full_path(path + "/" + filename)
    payload = b"kArmasWEBdavsCanNeR - authorized security scan probe. Safe to delete."
    try:
        status, headers, _ = client.request(
            "PUT", fpath, body=payload,
            extra_headers={"Content-Type": "text/plain"}
        )
        log("INFO", f"PUT {fpath} → HTTP {status}", 1)
        if status in (200, 201, 204):
            log("VULN", f"File uploaded successfully! HTTP {status}", 1)
            add_finding("CRITICAL", "Unauthenticated File Upload via PUT",
                        f"Successfully uploaded {filename} (HTTP {status}). "
                        "Arbitrary file upload possible without credentials.",
                        client.base_url + fpath)
            # Attempt cleanup
            _cleanup_put(client, fpath)
        elif status == 401:
            log("INFO", "PUT requires authentication (401) — good", 1)
        elif status == 403:
            log("INFO", "PUT forbidden (403) — access denied", 1)
        elif status == 405:
            log("INFO", "PUT method not allowed (405)", 1)
        elif status == 409:
            log("WARN", "PUT returned 409 Conflict — parent collection may not exist", 1)
        elif status == 423:
            log("WARN", "PUT returned 423 Locked — resource is locked", 1)
        else:
            log("INFO", f"PUT returned {status}", 1)
        return status
    except Exception as e:
        log("ERR", f"PUT upload test failed: {e}", 1)
        return None
    finally:
        log("END", "")


def _cleanup_put(client, fpath):
    """Try to DELETE the probe file we just uploaded."""
    try:
        status, _, _ = client.request("DELETE", fpath)
        if status in (200, 204):
            log("OK", f"Probe file deleted (HTTP {status})", 2)
        else:
            log("WARN", f"Could not delete probe file (HTTP {status}) — manual cleanup needed: {fpath}", 2)
    except Exception:
        log("WARN", "Could not clean up probe file — delete manually", 2)


def test_put_dangerous_extensions(client, path="/"):
    """Try uploading files with dangerous extensions (non-executing, content is benign)."""
    log("SECTION", "Dangerous Extension Upload Test")
    exts = [
        (".php",   b"<?php echo 'kArmas probe'; // NOT executing", "PHP script"),
        (".asp",   b"<% Response.Write(\"kArmas\") ' NOT executing %>", "ASP script"),
        (".aspx",  b"<%@ Page Language=\"C#\" %> <!-- kArmas probe -->", "ASPX page"),
        (".jsp",   b"<% out.print(\"kArmas\"); // NOT executing %>", "JSP script"),
        (".shtml", b"<!--#echo var=\"DATE\" --> kArmas probe", "SSI file"),
        (".htaccess", b"# kArmas probe\nOptions -Indexes", ".htaccess config"),
    ]
    found_any = False
    for ext, content, desc in exts:
        filename = f"kArmas_probe_{int(time.time())}{ext}"
        fpath = client.full_path(path + "/" + filename)
        try:
            status, _, _ = client.request(
                "PUT", fpath, body=content,
                extra_headers={"Content-Type": "text/plain"}
            )
            if status in (200, 201, 204):
                log("VULN", f"Uploaded {desc} ({ext}) → HTTP {status}", 1)
                add_finding("CRITICAL", f"Dangerous Extension Upload: {ext}",
                            f"Server accepted upload of {desc} file ({filename}). "
                            "May allow remote code execution if served.",
                            client.base_url + fpath)
                found_any = True
                _cleanup_put(client, fpath)
            elif status in (401, 403, 405):
                log("INFO", f"{ext}: blocked (HTTP {status})", 1)
            else:
                log("INFO", f"{ext}: HTTP {status}", 1)
        except Exception as e:
            log("ERR", f"{ext}: {e}", 1)
        time.sleep(0.2)

    if not found_any:
        log("OK", "No dangerous extension uploads accepted", 1)
    log("END", "")


def test_mkcol(client, path="/"):
    """Test unauthenticated directory creation via MKCOL."""
    log("SECTION", "MKCOL Directory Creation Test")
    dirname = f"kArmas_dir_{int(time.time())}"
    fpath = client.full_path(path + "/" + dirname)
    try:
        status, _, _ = client.request("MKCOL", fpath)
        log("INFO", f"MKCOL {fpath} → HTTP {status}", 1)
        if status in (200, 201):
            log("WARN", f"Directory created (HTTP {status})", 1)
            add_finding("MEDIUM", "Unauthenticated Directory Creation (MKCOL)",
                        f"Created directory '{dirname}' without authentication.",
                        client.base_url + fpath)
            # cleanup
            try:
                client.request("DELETE", fpath)
                log("OK", "Probe directory deleted", 2)
            except:
                pass
        elif status in (401, 403, 405):
            log("INFO", f"MKCOL blocked (HTTP {status})", 1)
        else:
            log("INFO", f"MKCOL returned {status}", 1)
        return status
    except Exception as e:
        log("ERR", f"MKCOL failed: {e}", 1)
        return None
    finally:
        log("END", "")


def test_copy_move(client, path="/"):
    """Test COPY and MOVE method abuse."""
    log("SECTION", "COPY / MOVE Method Test")
    for method in ["COPY", "MOVE"]:
        src = client.full_path(path + "/robots.txt")
        dst = client.full_path(path + f"/kArmas_copymove_test_{int(time.time())}.txt")
        dest_url = f"{client.scheme}://{client.host}:{client.port}{dst}"
        try:
            status, _, _ = client.request(
                method, src,
                extra_headers={"Destination": dest_url, "Overwrite": "T"}
            )
            log("INFO", f"{method} → HTTP {status}", 1)
            if status in (200, 201, 204):
                log("WARN", f"{method} succeeded — file manipulation possible", 1)
                add_finding("MEDIUM", f"Unauthenticated {method} Method Allowed",
                            f"{method} returned HTTP {status}. Attackers may overwrite files.",
                            client.base_url + src)
                try:
                    client.request("DELETE", dst)
                except:
                    pass
            elif status in (401, 403, 405):
                log("INFO", f"{method} blocked (HTTP {status})", 1)
            else:
                log("INFO", f"{method} returned {status}", 1)
        except Exception as e:
            log("ERR", f"{method}: {e}", 1)
        time.sleep(0.1)
    log("END", "")


def test_lock_unlock(client, path="/"):
    """Test LOCK/UNLOCK (can indicate writable WebDAV)."""
    log("SECTION", "LOCK / UNLOCK Method Test")
    fpath = client.full_path(path + f"/kArmas_lock_{int(time.time())}.txt")
    lock_body = b'''<?xml version="1.0" encoding="utf-8"?>
<D:lockinfo xmlns:D="DAV:">
  <D:lockscope><D:exclusive/></D:lockscope>
  <D:locktype><D:write/></D:locktype>
  <D:owner><D:href>kArmasWEBdavsCanNeR</D:href></D:owner>
</D:lockinfo>'''
    try:
        status, headers, _ = client.request(
            "LOCK", fpath, body=lock_body,
            extra_headers={"Content-Type": "application/xml", "Timeout": "Second-60", "Depth": "0"}
        )
        log("INFO", f"LOCK → HTTP {status}", 1)
        if status in (200, 201):
            lock_token = headers.get("lock-token", "")
            log("WARN", f"LOCK succeeded (token: {lock_token})", 1)
            add_finding("LOW", "LOCK Method Allowed",
                        f"Server accepted LOCK request. Lock token: {lock_token}",
                        client.base_url + fpath)
            # UNLOCK
            if lock_token:
                try:
                    u_status, _, _ = client.request(
                        "UNLOCK", fpath,
                        extra_headers={"Lock-Token": lock_token}
                    )
                    log("INFO", f"UNLOCK → HTTP {u_status}", 1)
                except:
                    pass
        elif status in (401, 403, 405):
            log("INFO", f"LOCK blocked (HTTP {status})", 1)
        else:
            log("INFO", f"LOCK returned {status}", 1)
    except Exception as e:
        log("ERR", f"LOCK: {e}", 1)
    log("END", "")


def test_large_file_dos(client, path="/", size_kb=512):
    """Test if server is vulnerable to large file upload (DoS probe — benign)."""
    log("SECTION", f"Large Upload Probe ({size_kb} KB)")
    filename = f"kArmas_large_{int(time.time())}.bin"
    fpath = client.full_path(path + "/" + filename)
    payload = b"\x00" * (size_kb * 1024)
    try:
        start = time.time()
        status, _, _ = client.request(
            "PUT", fpath, body=payload,
            extra_headers={"Content-Type": "application/octet-stream"}
        )
        elapsed = time.time() - start
        log("INFO", f"Large PUT ({size_kb}KB) → HTTP {status} in {elapsed:.2f}s", 1)
        if status in (200, 201, 204):
            log("WARN", f"Large file accepted ({size_kb}KB) — no size restriction", 1)
            add_finding("LOW", "No Upload Size Restriction Detected",
                        f"Server accepted {size_kb}KB upload. May allow storage exhaustion.",
                        client.base_url + fpath)
            _cleanup_put(client, fpath)
        elif status in (401, 403, 405, 413):
            log("INFO", f"Blocked (HTTP {status})", 1)
        else:
            log("INFO", f"HTTP {status}", 1)
    except Exception as e:
        log("ERR", f"Large file probe: {e}", 1)
    log("END", "")


def test_auth_bypass(client, path="/"):
    """Test common WebDAV authentication bypass techniques."""
    log("SECTION", "Authentication Bypass Probes")
    filename = f"kArmas_authbypass_{int(time.time())}.txt"
    fpath = client.full_path(path + "/" + filename)
    payload = b"kArmas auth bypass probe"

    bypass_headers = [
        ("No extra headers", {}),
        ("X-Original-URL bypass", {"X-Original-URL": "/"}),
        ("X-Rewrite-URL bypass", {"X-Rewrite-URL": "/"}),
        ("X-Forwarded-For localhost", {"X-Forwarded-For": "127.0.0.1"}),
        ("X-Custom-IP-Authorization", {"X-Custom-IP-Authorization": "127.0.0.1"}),
        ("Content-Type multipart bypass", {"Content-Type": "multipart/form-data"}),
        ("Translate: f (IIS)", {"Translate": "f"}),
        ("If: <*> (lock bypass)", {"If": "<*>", "Content-Type": "text/plain"}),
    ]

    for label, extra in bypass_headers:
        try:
            merged_extra = {"Content-Type": "text/plain"}
            merged_extra.update(extra)
            status, _, _ = client.request("PUT", fpath, body=payload, extra_headers=merged_extra)
            marker = c(C.GREEN + C.BOLD, f"HTTP {status}") if status in (200, 201, 204) else c(C.DIM, f"HTTP {status}")
            log("INFO", f"[{label}] → {marker}", 1)
            if status in (200, 201, 204):
                add_finding("CRITICAL", f"Auth Bypass via Header: {label}",
                            f"PUT succeeded with bypass technique: {label}",
                            client.base_url + fpath)
                _cleanup_put(client, fpath)
        except Exception as e:
            log("ERR", f"[{label}]: {e}", 1)
        time.sleep(0.1)
    log("END", "")


def test_xml_injection(client, path="/"):
    """Send malformed XML in PROPFIND to test for XXE / XML injection."""
    log("SECTION", "XML Injection / XXE Probe (PROPFIND)")
    fpath = client.full_path(path)
    xxe_payloads = [
        ("Basic XXE", b'''<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<D:propfind xmlns:D="DAV:"><D:prop><D:getcontentlength>&xxe;</D:getcontentlength></D:prop></D:propfind>'''),
        ("Blind SSRF XXE", b'''<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">]>
<D:propfind xmlns:D="DAV:"><D:allprop/></D:propfind>'''),
    ]
    for label, payload in xxe_payloads:
        try:
            status, headers, body = client.request(
                "PROPFIND", fpath, body=payload,
                extra_headers={"Depth": "0", "Content-Type": "application/xml"}
            )
            resp_text = body.decode("utf-8", errors="replace")
            log("INFO", f"[{label}] PROPFIND → HTTP {status}", 1)
            indicators = ["root:", "/bin/bash", "daemon:", "nobody:"]
            if any(ind in resp_text for ind in indicators):
                log("VULN", f"Possible XXE — /etc/passwd content in response!", 1)
                add_finding("CRITICAL", "XXE via WebDAV PROPFIND",
                            f"Response appears to contain /etc/passwd content. XXE exploitation possible.",
                            client.base_url + fpath)
            elif status in (500, 400):
                log("INFO", f"Server error {status} — may reject XXE (good) or be vulnerable", 1)
            else:
                log("INFO", f"No obvious XXE indicators in response", 1)
        except Exception as e:
            log("ERR", f"[{label}]: {e}", 1)
        time.sleep(0.2)
    log("END", "")


def test_path_traversal(client, path="/"):
    """Test path traversal via WebDAV MOVE/COPY destinations."""
    log("SECTION", "Path Traversal via WebDAV Destination")
    src_file = f"kArmas_trav_src_{int(time.time())}.txt"
    src_path = client.full_path(path + "/" + src_file)

    # First, try to PUT a source file
    try:
        status, _, _ = client.request("PUT", src_path, body=b"kArmas traversal probe",
                                       extra_headers={"Content-Type": "text/plain"})
        if status not in (200, 201, 204):
            log("INFO", "Cannot PUT source file — skipping traversal test", 1)
            log("END", "")
            return
    except:
        log("INFO", "Cannot reach source — skipping traversal test", 1)
        log("END", "")
        return

    traversal_paths = [
        "/../../../tmp/kArmas_traversal.txt",
        "/%2e%2e/%2e%2e/tmp/kArmas_traversal.txt",
        "/..%2f..%2ftmp%2fkArmas_traversal.txt",
    ]
    for tpath in traversal_paths:
        dst_url = f"{client.scheme}://{client.host}:{client.port}{tpath}"
        try:
            status, _, _ = client.request(
                "COPY", src_path,
                extra_headers={"Destination": dst_url, "Overwrite": "T"}
            )
            log("INFO", f"COPY to {tpath} → HTTP {status}", 1)
            if status in (200, 201, 204):
                log("WARN", f"Path traversal COPY succeeded!", 1)
                add_finding("CRITICAL", "Path Traversal via WebDAV COPY",
                            f"COPY to traversal path '{tpath}' succeeded (HTTP {status}). "
                            "File write outside webroot may be possible.",
                            client.base_url + tpath)
        except Exception as e:
            log("ERR", f"{tpath}: {e}", 1)
        time.sleep(0.1)

    _cleanup_put(client, src_path)
    log("END", "")


def test_http_verb_tampering(client, path="/"):
    """Try uncommon verbs and tunneled methods."""
    log("SECTION", "HTTP Verb Tampering / Tunneling")
    fpath = client.full_path(path + f"/kArmas_verb_{int(time.time())}.txt")
    payload = b"kArmas verb tamper probe"

    tests = [
        ("X-HTTP-Method-Override: PUT", "POST",
         {"X-HTTP-Method-Override": "PUT", "Content-Type": "text/plain"}),
        ("X-Method-Override: PUT", "POST",
         {"X-Method-Override": "PUT", "Content-Type": "text/plain"}),
        ("X-HTTP-Method: PUT", "POST",
         {"X-HTTP-Method": "PUT", "Content-Type": "text/plain"}),
    ]
    for label, method, headers in tests:
        try:
            status, _, _ = client.request(method, fpath, body=payload, extra_headers=headers)
            marker = c(C.YELLOW + C.BOLD, f"HTTP {status}") if status in (200, 201, 204) else c(C.DIM, f"HTTP {status}")
            log("INFO", f"[{label}] {method} → {marker}", 1)
            if status in (200, 201, 204):
                add_finding("HIGH", f"HTTP Method Override Bypass: {label}",
                            f"Server processed overridden PUT via {method} + header '{label}'",
                            client.base_url + fpath)
                _cleanup_put(client, fpath)
        except Exception as e:
            log("ERR", f"[{label}]: {e}", 1)
        time.sleep(0.1)
    log("END", "")


def test_webdav_paths(client):
    """Probe common WebDAV endpoint paths."""
    log("SECTION", "Common WebDAV Path Discovery")
    paths = [
        "/webdav", "/dav", "/files", "/upload", "/uploads", "/data",
        "/remote.php/dav", "/remote.php/webdav",      # Nextcloud / ownCloud
        "/servlet/webdav.infostore",                   # OX App Suite
        "/_dav", "/caldav", "/carddav",
        "/public", "/www", "/htdocs", "/web",
    ]
    discovered = []
    for p in paths:
        try:
            status, headers, _ = client.request("OPTIONS", p)
            dav = headers.get("dav", "")
            allow = headers.get("allow", "").upper()
            if status in (200, 207) or "PUT" in allow or dav:
                log("OK", f"{p} → HTTP {status}  DAV:{c(C.CYAN, dav or 'none')}  Allow:{allow[:60]}", 1)
                discovered.append(p)
                if dav or "PUT" in allow:
                    add_finding("LOW", f"WebDAV Endpoint Found: {p}",
                                f"Path '{p}' responded with DAV/PUT capabilities (HTTP {status})",
                                client.base_url + p)
            else:
                log("DIM", f"{p} → HTTP {status}", 1)
        except Exception:
            pass
        time.sleep(0.05)
    log("END", "")
    return discovered


def test_authentication_defaults(client, path="/"):
    """Try common default credential pairs."""
    log("SECTION", "Default Credential Brute-Force (Limited)")
    creds = [
        ("admin", "admin"), ("admin", "password"), ("admin", "1234"),
        ("root", "root"), ("root", "toor"), ("user", "user"),
        ("webdav", "webdav"), ("dav", "dav"), ("guest", "guest"),
        ("administrator", "administrator"), ("test", "test"),
    ]
    fpath = client.full_path(path)
    for user, passwd in creds:
        try:
            cred_b64 = base64.b64encode(f"{user}:{passwd}".encode()).decode()
            status, _, _ = client.request(
                "OPTIONS", fpath,
                extra_headers={"Authorization": f"Basic {cred_b64}"}
            )
            if status not in (401, 403):
                log("VULN", f"Credential works: {c(C.WHITE+C.BOLD, user+':'+passwd)} → HTTP {status}", 1)
                add_finding("CRITICAL", f"Default Credentials Valid: {user}:{passwd}",
                            f"Authentication succeeded with '{user}:{passwd}' (HTTP {status})",
                            client.base_url)
            else:
                log("DIM", f"{user}:{passwd} → HTTP {status}", 1)
        except Exception as e:
            log("ERR", f"{user}:{passwd}: {e}", 1)
        time.sleep(0.15)
    log("END", "")


# ─── REPORT ───────────────────────────────────────────────────────────────────

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}

def print_report(target, scan_time):
    print()
    print(c(C.MAGENTA + C.BOLD, "═" * 60))
    print(c(C.GREEN + C.BOLD,   "   kArmasWEBdavsCanNeR — SCAN REPORT"))
    print(c(C.MAGENTA + C.BOLD, "═" * 60))
    print(c(C.CYAN,  f"  Target : {target}"))
    print(c(C.CYAN,  f"  Time   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
    print(c(C.CYAN,  f"  Elapsed: {scan_time:.1f}s"))
    print()

    if not findings:
        print(c(C.GREEN + C.BOLD, "  [✓] No vulnerabilities detected."))
    else:
        sorted_findings = sorted(findings, key=lambda x: SEVERITY_ORDER.get(x["severity"], 99))
        counts = defaultdict(int)
        for f in sorted_findings:
            counts[f["severity"]] += 1

        sev_colors = {
            "CRITICAL": C.RED + C.BOLD,
            "HIGH":     C.YELLOW + C.BOLD,
            "MEDIUM":   C.YELLOW,
            "LOW":      C.CYAN,
            "INFO":     C.WHITE,
        }
        summary_parts = []
        for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if counts[sev]:
                summary_parts.append(c(sev_colors[sev], f"{counts[sev]} {sev}"))
        print(c(C.WHITE + C.BOLD, f"  Findings: ") + "  ".join(summary_parts))
        print()

        for i, f in enumerate(sorted_findings, 1):
            sev_col = sev_colors.get(f["severity"], C.WHITE)
            print(c(sev_col, f"  [{i:02d}] [{f['severity']}] {f['title']}"))
            print(c(C.DIM,  f"       Detail : {f['detail'][:100]}"))
            if f["url"]:
                print(c(C.DIM, f"       URL    : {f['url'][:80]}"))
            print()

    print(c(C.MAGENTA + C.BOLD, "═" * 60))
    print(c(C.GREEN + C.BOLD,
        "  We Are Legion. We Do Not Forget. We Do Not Forgive."))
    print(c(C.MAGENTA + C.BOLD, "═" * 60))
    print()


def save_report(target, scan_time, outfile):
    report = {
        "tool": "kArmasWEBdavsCanNeR",
        "target": target,
        "scan_time_seconds": round(scan_time, 2),
        "timestamp": datetime.datetime.now().isoformat(),
        "findings_count": len(findings),
        "findings": findings
    }
    with open(outfile, "w") as f:
        json.dump(report, f, indent=2)
    log("OK", f"Report saved → {c(C.WHITE, outfile)}")


# ─── AUTH GATE ────────────────────────────────────────────────────────────────

def authorization_gate(target):
    print()
    print(c(C.YELLOW + C.BOLD, "  ╔══════════════════════════════════════════════╗"))
    print(c(C.YELLOW + C.BOLD, "  ║         ⚠  AUTHORIZATION REQUIRED  ⚠        ║"))
    print(c(C.YELLOW + C.BOLD, "  ╚══════════════════════════════════════════════╝"))
    print()
    print(c(C.WHITE,  f"  Target: {c(C.CYAN, target)}"))
    print()
    print(c(C.WHITE,  "  This tool actively tests for WebDAV vulnerabilities."))
    print(c(C.WHITE,  "  Unauthorized scanning is ILLEGAL and unethical."))
    print()
    print(c(C.YELLOW, "  Only scan systems you OWN or have WRITTEN AUTHORIZATION to test."))
    print()
    confirm = input(c(C.GREEN + C.BOLD, '  Type "I HAVE AUTHORIZATION" to proceed: ')).strip()
    if confirm != "I HAVE AUTHORIZATION":
        print(c(C.RED + C.BOLD, "\n  ✗ Aborted. Authorization not confirmed."))
        sys.exit(0)
    print(c(C.GREEN + C.BOLD, "\n  ✓ Authorization confirmed. Initiating scan...\n"))
    time.sleep(0.5)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="kArmasWEBdavsCanNeR — WebDAV Upload Vulnerability Scanner",
        formatter_class=argparse.RawTextHelpFormatter
    )
    p.add_argument("target", help="Target URL (e.g. http://192.168.1.1 or https://target.local/dav)")
    p.add_argument("-p", "--path", default="/", help="WebDAV base path (default: /)")
    p.add_argument("-u", "--user", default=None, help="Username for Basic auth")
    p.add_argument("-P", "--password", default=None, help="Password for Basic auth")
    p.add_argument("-t", "--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    p.add_argument("-o", "--output", default=None, help="Save JSON report to file")
    p.add_argument("--ua", default=None, help="Custom User-Agent string")
    p.add_argument("--no-defaults", action="store_true", help="Skip default credential brute-force")
    p.add_argument("--no-paths", action="store_true", help="Skip WebDAV path discovery")
    p.add_argument("--skip-banner", action="store_true", help="Skip matrix rain intro")
    p.add_argument("--large-kb", type=int, default=512, help="Size for large upload probe in KB (default: 512)")
    p.add_argument("-y", "--yes", action="store_true", help="Skip authorization prompt (use if you're certain)")
    return p.parse_args()


def main():
    args = parse_args()

    if not args.skip_banner:
        print_banner()

    if not args.yes:
        authorization_gate(args.target)

    auth = (args.user, args.password) if args.user else None
    client = WebDAVClient(
        args.target,
        timeout=args.timeout,
        auth=auth,
        user_agent=args.ua
    )

    print(c(C.GREEN + C.BOLD, f"\n  Scanning: {c(C.WHITE, args.target)}"))
    print(c(C.GREEN,           f"  Path    : {args.path}"))
    if auth:
        print(c(C.CYAN,        f"  Auth    : {args.user}:{'*' * len(args.password)}"))
    print()

    start = time.time()

    # ── Run all test modules ──────────────────────────────────────────────────
    test_options(client, args.path)
    test_propfind(client, args.path)
    test_put_upload(client, args.path)
    test_put_dangerous_extensions(client, args.path)
    test_mkcol(client, args.path)
    test_copy_move(client, args.path)
    test_lock_unlock(client, args.path)
    test_xml_injection(client, args.path)
    test_path_traversal(client, args.path)
    test_http_verb_tampering(client, args.path)
    test_auth_bypass(client, args.path)
    test_large_file_dos(client, args.path, size_kb=args.large_kb)

    if not args.no_paths:
        discovered = test_webdav_paths(client)
        if discovered:
            print(c(C.CYAN, f"\n  Discovered WebDAV paths: {', '.join(discovered)}"))

    if not args.no_defaults:
        test_authentication_defaults(client, args.path)

    elapsed = time.time() - start
    print_report(args.target, elapsed)

    if args.output:
        save_report(args.target, elapsed, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(c(C.RED + C.BOLD, "\n\n  [!] Scan interrupted by user."))
        elapsed = 0
        if findings:
            print_report("(interrupted)", elapsed)
        sys.exit(0)
