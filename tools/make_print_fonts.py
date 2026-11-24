#!/usr/bin/env python3
"""Create static font instances for PDF printing (one-off; output is committed).

Chrome embeds variable web fonts in PDFs as Type 3 fonts, which some viewers render poorly and which break
text extraction. Static instances are embedded as regular TrueType fonts instead. Used only by the print
styles of the executive brief (assets/css/brief.css); the website itself keeps the variable fonts.

Requires: pip install fonttools brotli
Usage:    python3 tools/make_print_fonts.py
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "fonts")
OUT = os.path.join(SRC, "static")
JOBS = {"Inter-latin.woff2": ("Inter", (400, 500, 600, 700, 800)),
        "PlusJakartaSans-latin.woff2": ("PlusJakartaSans", (600, 700, 800))}

os.makedirs(OUT, exist_ok=True)
for src, (name, weights) in JOBS.items():
    for w in weights:
        font = TTFont(os.path.join(SRC, src))
        static = instancer.instantiateVariableFont(font, {"wght": w}, updateFontNames=False)
        static.flavor = "woff"
        path = os.path.join(OUT, f"{name}-{w}.woff")
        static.save(path)
        print(f"{os.path.relpath(path, ROOT)}  {os.path.getsize(path) // 1024} KB")
