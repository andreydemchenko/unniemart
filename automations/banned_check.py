#!/usr/bin/env python3
"""Banned-phrase checker for captions, scripts and shot lists (strategy/PLAYBOOK.md "Banned", slop gate rules 3-5).

BLOCK = the draft can't go to the owner until it's fixed. WARN = a human should look.
Only catches wording. It can't tell whether a fact is true: facts still need a source and a human tick.

Usage:
  python3 automations/banned_check.py FILE [FILE...]        # or pipe text on stdin
  python3 automations/banned_check.py --stock-checked FILE  # scarcity lines were checked against the stock list
Exit code 1 if anything is BLOCK.

In .md files the markdown-stars rule is skipped (bold is normal there); run it on the caption text itself.
"""
import argparse
import re
import sys
from dataclasses import dataclass

MONTH = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?'
DATE = re.compile(rf'\b{MONTH}\s*\d{{1,2}}\b|\b\d{{1,2}}\s*{MONTH}\b|\b\d{{1,2}}/\d{{1,2}}\b|\b20\d\d-\d\d-\d\d\b', re.I)

# (rule, pattern, message). Case-insensitive.
BLOCK = [
    ('slop phrase', r'this (might|will|could) change your life', 'generic hook'),
    ('slop phrase', r'\bhear me out\b', 'generic hook'),
    ('slop phrase', r"\b(stay|wait|watch) (till|until|'til|til) the end\b", 'generic hook'),
    ('slop phrase', r'\bgame[- ]?changer\b', 'generic hype'),
    ('slop phrase', r"\byou won'?t believe\b", 'generic hook'),
    ('slop phrase', r'\bmust[- ]have\b', 'generic hype'),
    ('AI leftover', r'suggested (title|hashtags|caption)', 'AI tool output pasted into the caption'),
    ('AI leftover', r"\bas an ai\b|\bhere'?s (a|your) (caption|script)\b", 'AI tool output pasted into the caption'),
    ('legit claim', r'100\s*% legit|100 percent legit|sure ?ball legit', 'show proof instead of claiming it'),
    ('AI or stock visual', r'\bai[- ](voice|voiceover|avatar|face|idol|generated|image|photo|render)s?\b',
     'no AI voices, faces or product photos'),
    ('AI or stock visual', r'\bstock (footage|render|video|photo)s?\b', 'film the real item'),
    ('AI or stock visual', r'\bfancam\b|\bsomeone else.s (video|footage)\b', "don't use other people's footage"),
]

SCARCITY = re.compile(
    r'\blast \d+\s*(pcs?|pieces?|slots?|units?|stocks?)\b|\b\d+\s*(pcs?|pieces?|slots?|units?)\s*(left|na lang|nalang)\b'
    r'|\bhuling \d+\b|\b(few|limited) (slots?|stocks?|pieces?)( left)?\b|\bpaubos na\b|\bselling fast\b|\bubos na\b'
    r'|\bonly \d+ left\b|\balmost sold out\b', re.I)
MISS_OUT = re.compile(r"\bdon'?t miss( out)?\b|\bwag (nyo |niyo )?palampasin\b|\bhuwag palampasin\b", re.I)

WARN = [
    ('fear selling', r'\buseless\b|wala ?nang silbi|sayang lang (pera|bili)|\bobsolete\b',
     'help, not "your old one is useless"'),
    ('hashtag', r'#(fyp|foryou|foryoupage|viral)\b', 'skip #fyp; use 3 to 5 exact hashtags with the model name'),
    ('AI tell', r'\b(elevate|delve|look no further|whether you.re a|ultimate guide|in today.s video)\b',
     'reads like AI; say it the way the owner talks'),
    ('AI tell', '—', 'em dash reads like AI in a Taglish caption'),
]
MD_STARS = re.compile(r'\*\*[^*\n]+\*\*')
PRICE = re.compile(r"(?<!\w)(₱|php|p)\s?\d{1,3}(,\d{3})+|(?<!\w)(₱|php)\s?\d{4,}", re.I)


@dataclass
class Finding:
    level: str      # BLOCK or WARN
    rule: str
    match: str
    message: str
    line: int

    def __str__(self):
        return f'{self.level:5} line {self.line}: {self.rule}: "{self.match}" ({self.message})'


def check(text, stock_checked=False, markdown=False):
    """Return a list of Findings for one caption, script or document."""
    out = []
    text = (text or '').replace('’', "'").replace('‘', "'")
    lines = text.splitlines() or ['']
    for n, line in enumerate(lines, 1):
        for rule, pat, msg in BLOCK:
            for m in re.finditer(pat, line, re.I):
                out.append(Finding('BLOCK', rule, m.group(0), msg, n))
        if not stock_checked:
            for m in SCARCITY.finditer(line):
                out.append(Finding('BLOCK', 'scarcity', m.group(0),
                                   "needs the real count from the owner's stock list (then use --stock-checked)", n))
        for m in MISS_OUT.finditer(line):
            if not DATE.search(line):
                out.append(Finding('BLOCK', 'miss out', m.group(0), 'only with a real date on the same line', n))
        if not markdown:
            for m in MD_STARS.finditer(line):
                out.append(Finding('BLOCK', 'AI leftover', m.group(0), 'markdown stars show up as ** on TikTok', n))
        for rule, pat, msg in WARN:
            for m in re.finditer(pat, line, re.I):
                out.append(Finding('WARN', rule, m.group(0), msg, n))
    tags = re.findall(r'(?<!\w)#\w+', text)
    if not markdown and len(tags) > 5:
        out.append(Finding('WARN', 'hashtag', f'{len(tags)} hashtags', 'use 3 to 5', 1))
    first = next((ln for ln in lines if ln.strip()), '')
    m = PRICE.search(first)
    if not markdown and m and not re.search(r'\bdp\b|down ?payment', first, re.I):
        out.append(Finding('WARN', 'price first', m.group(0),
                           'lead with help, or the small number first ("₱300 DP · total ₱2,750")', 1))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Banned-phrase checker for Unnie Mart drafts')
    ap.add_argument('files', nargs='*')
    ap.add_argument('--stock-checked', action='store_true', help='scarcity lines were checked against the stock list')
    a = ap.parse_args(argv)
    inputs = [(f, open(f, encoding='utf-8').read()) for f in a.files] or [('stdin', sys.stdin.read())]
    blocked = False
    for name, text in inputs:
        found = check(text, a.stock_checked, markdown=name.endswith('.md'))
        blocked |= any(f.level == 'BLOCK' for f in found)
        print(f'{name}: ' + ('OK' if not found else f'{len(found)} finding(s)'))
        for f in found:
            print('  ' + str(f))
    return 1 if blocked else 0


if __name__ == '__main__':
    sys.exit(main())
