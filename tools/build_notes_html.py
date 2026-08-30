#!/usr/bin/env python3
"""Build the HTML reading edition of a study-notes markdown file.

With no arguments this rebuilds the secure-boot notes exactly as before.
Pass --src/--out/--template to build a different notes file, e.g.

    python3 tools/build_notes_html.py \
        --src crypto-course-notes.md \
        --out crypto-course-notes.html \
        --template tools/crypto_notes_template.html
"""
import argparse
import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent

ap = argparse.ArgumentParser(description=__doc__,
                             formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--src", type=Path, default=REPO / "linux-secure-boot-notes.md",
                help="markdown source (default: linux-secure-boot-notes.md)")
ap.add_argument("--out", type=Path, default=None,
                help="html output (default: <src> with .html suffix)")
ap.add_argument("--template", type=Path, default=TOOLS / "notes_template.html",
                help="html template (default: tools/notes_template.html)")
args = ap.parse_args()

SRC = args.src
OUT = args.out if args.out else SRC.with_suffix(".html")
TEMPLATE_PATH = args.template

if not SRC.exists():
    raise SystemExit(f"source not found: {SRC}")
if not TEMPLATE_PATH.exists():
    raise SystemExit(f"template not found: {TEMPLATE_PATH}")

md_text = SRC.read_text(encoding="utf-8")

# --- strip the front-matter block (title h1 + intro blockquote + goal line) ---
lines = md_text.split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("---"))
body_md = "\n".join(lines[start + 1:]).lstrip("\n")

# adjacent blockquotes get merged by python-markdown, which loses their
# individual glyph classification -- keep them apart with an HTML comment
def split_adjacent_quotes(text):
    src, out, i, n = text.split("\n"), [], 0, len(text.split("\n"))
    while i < n:
        out.append(src[i])
        # the preceding quote may be indented (nested in a list); the following
        # one must be top-level, or the two are part of the same list structure
        if src[i].lstrip().startswith(">"):
            j = i + 1
            while j < n and src[j].strip() == "":
                j += 1
            if j > i + 1 and j < n and src[j].startswith(">"):
                out += ["", "<!-- -->"] + [""] * (j - i - 2)
                i = j
                continue
        i += 1
    return "\n".join(out)

body_md = split_adjacent_quotes(body_md)

import markdown
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "nl2br"])
# nl2br is wrong for prose; rebuild without it
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
body = md.convert(body_md)

# --- assign ids to h1/h2, collect nav entries ---
nav = []
counter = {"n": 0}

def head_repl(m):
    tag, inner = m.group(1), m.group(2)
    counter["n"] += 1
    hid = f"s{counter['n']}"
    text = re.sub(r"<[^>]+>", "", inner)
    # split "§7 信任鏈的破口：rootfs" into marker + label
    sec = re.match(r"^(§\d+)\s+(.*)$", text)
    if tag == "h2" and sec:
        marker, label = sec.group(1), sec.group(2)
        nav.append(("sec", hid, marker, label))
        inner = (f'<span class="sec-mark">{html.escape(marker)}</span>'
                 f'<span class="sec-label">{html.escape(label)}</span>')
    elif tag == "h1":
        nav.append(("part", hid, "", text))
    else:
        nav.append(("sec", hid, "", text))
    cls = ' class="part"' if tag == "h1" else ""
    return f'<{tag} id="{hid}"{cls}>{inner}</{tag}>'

body = re.sub(r"<(h1|h2)>(.*?)</\1>", head_repl, body, flags=re.S)

# --- tag callout blockquotes by their leading glyph ---
KINDS = [("⚠️", "warn"), ("🎯", "key"), ("📌", "gap"),
         ("🔒", "key"), ("💡", "tip"), ("ℹ️", "note"), ("📄", "src")]

def quote_repl(m):
    inner = m.group(1)
    plain = re.sub(r"<[^>]+>", "", inner).lstrip()
    for glyph, kind in KINDS:
        if plain.startswith(glyph):
            return f'<blockquote class="cal cal-{kind}">{inner}</blockquote>'
    return f'<blockquote class="cal cal-plain">{inner}</blockquote>'

body = re.sub(r"<blockquote>(.*?)</blockquote>", quote_repl, body, flags=re.S)

# --- h3 that carry a 🎯 get the key treatment ---
body = re.sub(r"<h3>(\s*🎯.*?)</h3>", r'<h3 class="h3-key">\1</h3>', body, flags=re.S)

# --- wrap tables so wide ones scroll inside themselves ---
body = re.sub(r"<table>(.*?)</table>",
              r'<div class="table-wrap"><table>\1</table></div>', body, flags=re.S)

# --- page-ref lines ("📖 書頁 1–5") become a footer chip ---
body = re.sub(r"<p>📖\s*(.*?)</p>", r'<p class="pageref"><span>📖</span>\1</p>', body)

# --- nav markup ---
nav_html = []
for kind, hid, marker, label in nav:
    if kind == "part":
        nav_html.append(f'<div class="nav-part">{html.escape(label)}</div>')
    else:
        m = f'<span class="nav-mark">{html.escape(marker)}</span>' if marker else ""
        nav_html.append(
            f'<a class="nav-link" href="#{hid}">{m}'
            f'<span class="nav-text">{html.escape(label)}</span></a>')
nav_html = "\n".join(nav_html)

TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8")
OUT.write_text(TEMPLATE.replace("<!--NAV-->", nav_html).replace("<!--BODY-->", body),
               encoding="utf-8")
print(f"wrote {OUT}  ({OUT.stat().st_size/1024:.0f} KB, {len(nav)} nav entries)")
