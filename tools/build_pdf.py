#!/usr/bin/env python3
"""Generate the executive-brief PDFs from the HTML presentations (single source of truth).

Usage:  python3 tools/build.py && python3 tools/build_pdf.py

Serves the built site on a local port, prints each language version with headless Chrome
(print CSS in assets/css/brief.css: one 13.333 × 7.5 in page per slide, no margins, backgrounds kept),
then adds document metadata (title, author, subject, keywords, language) with an incremental PDF update.
Text stays selectable, diagrams stay vector and links stay clickable. Requires Google Chrome or Chromium.
"""
import functools
import http.server
import os
import re
import shutil
import subprocess
import sys
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sitegen.pages_brief import DIR, PDF, URL, T  # noqa: E402

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "", shutil.which("chromium") or "", shutil.which("chromium-browser") or "",
]
META = {
    "en": {"subject": "Executive business overview: enterprise intelligence across distributed data",
           "keywords": "GroundTruth AI, enterprise AI, distributed data, industrial AI, predictive maintenance, AI training efficiency",
           "lang": "en-US"},
    "es": {"subject": "Resumen comercial: inteligencia empresarial sobre datos distribuidos",
           "keywords": "GroundTruth AI, IA empresarial, datos distribuidos, IA industrial, mantenimiento predictivo, eficiencia de IA",
           "lang": "es-ES"},
}


def pdf_str(s):
    """PDF text string: UTF-16BE with BOM, hex encoded (safe for any character)."""
    return "<FEFF" + s.encode("utf-16-be").hex().upper() + ">"


def add_metadata(path, title, subject, keywords, lang):
    data = open(path, "rb").read()
    startxref = int(re.findall(rb"startxref\s+(\d+)", data)[-1])
    trailer = re.findall(rb"trailer\s*<<(.*?)>>\s*startxref", data, re.S)
    if not trailer:
        print("  (cross-reference stream PDF: metadata step skipped)")
        return
    tr = trailer[-1]
    size = int(re.search(rb"/Size\s+(\d+)", tr).group(1))
    root = re.search(rb"/Root\s+(\d+)\s+(\d+)\s+R", tr)
    rnum, rgen = int(root.group(1)), int(root.group(2))
    m = list(re.finditer(rb"(?<!\d)%d %d obj\s*<<(.*?)>>\s*endobj" % (rnum, rgen), data, re.S))[-1]
    catalog = re.sub(rb"/Lang\s*\([^)]*\)|/Lang\s*<[^>]*>", b"", m.group(1))
    out = bytearray(data)
    if not out.endswith(b"\n"):
        out += b"\n"
    offs = {}
    offs[rnum] = len(out)
    out += b"%d %d obj\n<<%s /Lang (%s)>>\nendobj\n" % (rnum, rgen, catalog, lang.encode())
    info = size
    offs[info] = len(out)
    out += ("%d 0 obj\n<< /Title %s /Author %s /Subject %s /Keywords %s /Creator %s >>\nendobj\n" % (
        info, pdf_str(title), pdf_str("GroundTruth AI"), pdf_str(subject), pdf_str(keywords), pdf_str("GroundTruth AI website build"))).encode()
    xref = len(out)
    out += b"xref\n"
    for num in sorted(offs):
        out += b"%d 1\n%010d %05d n \n" % (num, offs[num], rgen if num == rnum else 0)
    out += b"trailer\n<< /Size %d /Root %d %d R /Info %d 0 R /Prev %d >>\nstartxref\n%d\n%%%%EOF\n" % (size + 1, rnum, rgen, info, startxref, xref)
    open(path, "wb").write(out)


def main():
    chrome = next((c for c in CHROME_CANDIDATES if c and os.path.exists(c)), None)
    if not chrome:
        sys.exit("Chrome/Chromium not found; set CHROME=/path/to/chrome")
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=ROOT)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    port = srv.server_address[1]
    try:
        for lang in ("en", "es"):
            out = os.path.join(ROOT, DIR.strip("/"), PDF[lang])
            url = f"http://127.0.0.1:{port}{URL[lang]}"
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--hide-scrollbars",
                            "--run-all-compositor-stages-before-draw", "--virtual-time-budget=8000",
                            f"--print-to-pdf={out}", url], check=True, capture_output=True)
            add_metadata(out, T[lang]["title"], META[lang]["subject"], META[lang]["keywords"], META[lang]["lang"])
            print(f"Wrote {os.path.relpath(out, ROOT)} ({os.path.getsize(out) // 1024} KB)")
    finally:
        srv.shutdown()


if __name__ == "__main__":
    main()
