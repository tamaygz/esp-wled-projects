#!/usr/bin/env python
"""
upload_spiffs.py — Upload firmware/spiffs/ files to a WLED device over HTTP.

Works with any WLED installation method, including the web installer
(install.wled.me).  WLED's built-in /upload endpoint stores each uploaded
file in the device's LittleFS filesystem, making it accessible at
http://<device>/<filename>.

After uploading, visit http://<device>/ha-import.html to start the
Home Assistant import wizard.

Usage
-----
    python tools/upload_spiffs.py --project reefs
    python tools/upload_spiffs.py --project reefs --device 192.168.1.42
    python tools/upload_spiffs.py --project reefs --device reefs.local

Requirements
------------
    Python 3.8+  (stdlib only, no pip packages needed)
    WLED device reachable on the local network (WiFi configured)
"""

from __future__ import annotations
import argparse
import os
import sys
import uuid
import urllib.request
import urllib.error

# ── Paths ──────────────────────────────────────────────────────────────────────
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(TOOLS_DIR)

# ── ANSI colours (disabled automatically on Windows without ANSI support) ─────
def _ansi(code: str, text: str) -> str:
    if sys.stdout.isatty() and os.name != "nt" or _win_ansi():
        return f"\033[{code}m{text}\033[0m"
    return text

def _win_ansi() -> bool:
    """Return True if the Windows console supports ANSI sequences."""
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        return bool(kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(ctypes.c_ulong())))
    except Exception:
        return False

green  = lambda t: _ansi("32", t)
red    = lambda t: _ansi("31", t)
yellow = lambda t: _ansi("33", t)
bold   = lambda t: _ansi("1",  t)


# ── Multipart upload (stdlib, no requests) ─────────────────────────────────────
def upload_file(url: str, filepath: str, timeout: int = 30) -> tuple[int, str]:
    """
    POST a single file to WLED's /upload endpoint using multipart/form-data.

    WLED expects the field name ``data`` and stores the file in LittleFS
    under the uploaded filename (with a leading / prepended if absent).

    Returns (http_status_code, response_body_text).
    """
    boundary = "----WLEDUpload" + uuid.uuid4().hex
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as fh:
        file_bytes = fh.read()

    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="data"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n"
        f"\r\n"
    ).encode()
    tail = f"\r\n--{boundary}--\r\n".encode()

    body = head + file_bytes + tail

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    req.add_header("Content-Length", str(len(body)))

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode(errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode(errors="replace")


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload firmware/spiffs/ files to a WLED device over HTTP."
    )
    parser.add_argument(
        "--project", "-p",
        required=True,
        help="Project folder name (e.g. reefs)",
    )
    parser.add_argument(
        "--device", "-d",
        default="",
        help="Device IP or hostname (default: <project>.local)",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Per-file upload timeout in seconds (default: 30)",
    )
    args = parser.parse_args()

    device = args.device or f"{args.project}.local"
    spiffs_dir = os.path.join(REPO_ROOT, args.project, "firmware", "spiffs")

    if not os.path.isdir(spiffs_dir):
        print(red(f"Error: spiffs folder not found: {spiffs_dir}"), file=sys.stderr)
        return 1

    files = sorted(
        f for f in os.listdir(spiffs_dir)
        if os.path.isfile(os.path.join(spiffs_dir, f))
    )

    if not files:
        print(yellow(f"No files found in {spiffs_dir} — nothing to upload."))
        return 0

    upload_url = f"http://{device}/upload"
    print()
    print(bold(f"Uploading {len(files)} file(s) to {upload_url}"))
    print()

    ok = fail = 0
    for filename in files:
        filepath = os.path.join(spiffs_dir, filename)
        size_kb  = os.path.getsize(filepath) / 1024
        print(f"  {filename:<40} ({size_kb:.1f} KB)  ", end="", flush=True)
        try:
            status, body = upload_file(upload_url, filepath, timeout=args.timeout)
            if 200 <= status < 300:
                print(green(f"OK ({status})"))
                ok += 1
            else:
                print(red(f"FAILED ({status})  {body[:80].strip()}"))
                fail += 1
        except OSError as exc:
            print(red(f"ERROR  {exc}"))
            fail += 1

    print()
    if fail == 0:
        print(green(f"All {ok} file(s) uploaded successfully."))
        print()
        print(f"  Open in browser:  http://{device}/ha-import.html")
        print(f"  Check filesystem: http://{device}/edit")
        print()
        return 0
    else:
        print(yellow(f"{ok} uploaded, {fail} failed."))
        print(f"  Is the device reachable?  Try: ping {device}")
        print(f"  Or specify the IP:  --device 192.168.x.x")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
