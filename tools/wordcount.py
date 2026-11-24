#!/usr/bin/env python3
"""Count visible words in <main> of a built page (QA helper). Usage: python3 tools/wordcount.py index.html"""
import re, sys
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.m = 0; s.skip = 0; s.w = []
    def handle_starttag(s, t, a):
        if t == "main": s.m = 1
        if t in ("script", "style", "title", "desc"): s.skip += 1
    def handle_endtag(s, t):
        if t == "main": s.m = 0
        if t in ("script", "style", "title", "desc"): s.skip -= 1
    def handle_data(s, d):
        if s.m and not s.skip: s.w += re.findall(r"\w[\w'’.-]*", d)
for f in sys.argv[1:]:
    p = P(); p.feed(open(f, encoding="utf-8").read()); print(len(p.w), f)
