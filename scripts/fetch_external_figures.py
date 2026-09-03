#!/usr/bin/env python
"""Fetch the externally-licensed figures used in the thesis, with their attribution.

Borrowed figures need an author and a licence in the caption, and typing those from memory is
how a licence gets misattributed. This script asks the Wikimedia Commons API for the file, and
takes the URL, licence and author out of the same response it downloads from -- so the credit
line in ``figures/external/CREDITS.md`` is correct by construction rather than by recollection.

SVGs are converted to PDF with rsvg-convert, which keeps them vector so they stay sharp at any
size in the thesis. Bitmaps are stored as delivered.

Usage:  python scripts/fetch_external_figures.py [--force]

Re-runnable: files already present are skipped unless --force. CREDITS.md is always rewritten,
and records the retrieval date so a later licence change is detectable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from topology import paths

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "ImageCAS-X-thesis/1.0 (DTU Compute; figure attribution fetcher)"

# Commons file title -> local basename (without extension) and what it illustrates.
FIGURES = {
    "File:Diagram of the human heart (cropped).svg": (
        "heart_chambers", "Chambers, valves and the direction of flow"),
    "File:2004 Heart Wall.jpg": (
        "heart_wall", "The three layers of the heart wall"),
    "File:Coronary arteries.svg": (
        "coronary_arteries", "The coronary arteries on the surface of the heart"),
}


def _strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", html.unescape(value or "")).strip()



# Commons "Artist" fields often carry template boilerplate and a source-file prefix alongside
# the real credits. Strip only those; never drop a contributor.
_BOILERPLATE = re.compile(
    r"(author\s*info|reusing\s*images|conflicts?\s*of\s*interest)", re.I)


def _clean_artist(raw: str) -> str:
    """Flatten a multi-line Artist field to one credit line.

    Split on lines only -- never on commas, which would tear "Lynch, medical illustrator" and
    "Haggstrom, M.D." apart. Boilerplate lines are dropped, and a line already contained in a
    kept credit is treated as a duplicate. Every distinct contributor survives.
    """
    parts: list[str] = []
    for line in raw.splitlines():
        line = re.sub(r"^\S+\.(pdf|svg|jpg|png)\s*:\s*", "", line.strip(), flags=re.I)
        line = line.strip(" .;-")
        if not line or _BOILERPLATE.search(line):
            continue
        if any(line in kept for kept in parts):
            continue
        parts = [kept for kept in parts if kept not in line]
        parts.append(line)
    return "; ".join(parts)


def query(title: str) -> dict:
    """imageinfo for one Commons file: download URL plus licence metadata."""
    params = {
        "action": "query", "prop": "imageinfo",
        "iiprop": "url|extmetadata|size", "format": "json", "titles": title,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as fh:
        pages = json.load(fh)["query"]["pages"]
    page = next(iter(pages.values()))
    if "imageinfo" not in page:
        raise SystemExit(f"not found on Commons: {title}")
    info = page["imageinfo"][0]
    meta = info.get("extmetadata", {})
    get = lambda key: _strip_html(meta.get(key, {}).get("value", ""))
    artist = _clean_artist(get("Artist"))
    return {
        "title": page["title"],
        "url": info["url"].split("?")[0],
        "width": info["width"],
        "height": info["height"],
        "license": get("LicenseShortName"),
        "usage_terms": get("UsageTerms"),
        "artist": artist,
        "descriptionurl": info.get("descriptionurl", ""),
    }


def download(url: str, dest: str) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as fh, open(dest, "wb") as out:
        shutil.copyfileobj(fh, out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download files already present")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()

    out_dir = args.out_dir or str(paths.REPO_ROOT / "figures" / "external")
    os.makedirs(out_dir, exist_ok=True)

    if not shutil.which("rsvg-convert"):
        print("warning: rsvg-convert not on PATH; SVG files cannot be converted to PDF")

    records = []
    for title, (stem, purpose) in FIGURES.items():
        meta = query(title)
        src_ext = os.path.splitext(meta["url"])[1].lower()
        raw = os.path.join(out_dir, stem + src_ext)

        if args.force or not os.path.exists(raw):
            download(meta["url"], raw)
            action = "downloaded"
        else:
            action = "cached"

        final = raw
        if src_ext == ".svg":
            pdf = os.path.join(out_dir, stem + ".pdf")
            if args.force or not os.path.exists(pdf):
                subprocess.run(["rsvg-convert", "-f", "pdf", "-o", pdf, raw], check=True)
            final = pdf

        meta.update(stem=stem, purpose=purpose, local=os.path.basename(final))
        records.append(meta)
        print(f"[{action:10s}] {stem:18s} {meta['license']:14s} {os.path.basename(final)}")

    today = dt.date.today().isoformat()
    lines = [
        "# External figure credits",
        "",
        "Generated by `scripts/fetch_external_figures.py` from the Wikimedia Commons API.",
        "Do not edit by hand -- re-run the script instead, so the credits stay tied to the",
        f"source. Retrieved {today}.",
        "",
    ]
    for r in records:
        lines += [
            f"## `{r['local']}`",
            "",
            f"- **Illustrates:** {r['purpose']}",
            f"- **Author:** {r['artist']}",
            f"- **Licence:** {r['license']} ({r['usage_terms']})",
            f"- **Source:** {r['descriptionurl'] or r['url']}",
            f"- **Original:** {r['title']}, {r['width']}x{r['height']}",
            "",
            "Caption credit line to use in the thesis:",
            "",
            f"> Figure by {r['artist']}, {r['license']}, via Wikimedia Commons.",
            "",
        ]
    credits = os.path.join(out_dir, "CREDITS.md")
    with open(credits, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"\nwrote {credits}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
