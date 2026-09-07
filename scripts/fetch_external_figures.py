#!/usr/bin/env python3
"""Fetch externally-licensed figures and regenerate figures/external/CREDITS.md.

Every figure the thesis borrows must carry an attribution that traces to its source, and
that attribution must never be typed by hand into a caption -- it is generated here and
copied from CREDITS.md.  Re-run this script rather than editing CREDITS.md.

Two kinds of source are supported:

  wikimedia  Attribution is pulled live from the Commons API (extmetadata), so the credit
             cannot drift from the file page.
  plos       PLOS journals are uniformly CC BY 4.0 and expose no per-figure attribution
             API, so author and licence come from the manifest below.  Those fields are
             transcribed from the article's own licence statement and are marked in
             CREDITS.md as declared rather than API-derived, so a reader can tell the
             difference.

Usage:
    python scripts/fetch_external_figures.py            # fetch missing, rewrite CREDITS.md
    python scripts/fetch_external_figures.py --force    # re-download everything
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "figures" / "external"
CREDITS = OUT_DIR / "CREDITS.md"
UA = "ImageCAS-X-thesis/1.0 (DTU Compute; figure attribution fetcher)"

# --------------------------------------------------------------------------------------
# The manifest.  Order here is the order in CREDITS.md.
# --------------------------------------------------------------------------------------
FIGURES: list[dict] = [
    {
        "filename": "heart_chambers.pdf",
        "source": "wikimedia",
        "commons_file": "File:Diagram of the human heart (cropped).svg",
        "illustrates": "Chambers, valves and the direction of flow",
        "note": "converted to PDF after download",
    },
    {
        "filename": "heart_wall.jpg",
        "source": "wikimedia",
        "commons_file": "File:2004 Heart Wall.jpg",
        "illustrates": "The three layers of the heart wall",
    },
    {
        "filename": "coronary_arteries.pdf",
        "source": "wikimedia",
        "commons_file": "File:Coronary arteries.svg",
        "illustrates": "The coronary arteries on the surface of the heart",
        "note": "converted to PDF after download",
        # The Commons Artist field for this file carries editorial boilerplate
        # ("Author info - Reusing images- Conflicts of interest: None ...") around the
        # actual credit. Trimmed to the authors only; the untrimmed value is still
        # reachable at the Source URL below.
        "author_trimmed": (
            "Patrick J. Lynch, medical illustrator; derivative work: Fred the Oyster; "
            "Mikael H\u00e4ggstr\u00f6m, M.D"
        ),
    },
    {
        "filename": "bifurcation_angle.png",
        "source": "plos",
        "doi": "10.1371/journal.pone.0273157",
        "figure": "g002",
        "journal": "PLOS ONE",
        "year": 2022,
        # Transcribed from the article's licence statement; verified 2026-09-06.
        "author": "Murasato Y, Meno K, Mori T, Tanenaka K",
        "licence_short": "CC BY 4.0",
        "licence_long": "Creative Commons Attribution 4.0 International",
        "article_url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0273157",
        "illustrates": (
            "Two conventions for measuring bifurcation angle, and how curvature makes "
            "them disagree"
        ),
        "bibkey": "murasato2022bifurcation",
    },
]

# --------------------------------------------------------------------------------------


def _get(url: str, params: dict | None = None) -> bytes:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def _strip_html(s: str) -> str:
    """Commons `Artist` fields are HTML fragments; flatten to readable text."""
    out, depth = [], 0
    for ch in s:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0:
            out.append(ch)
    return " ".join("".join(out).split())


def resolve_wikimedia(entry: dict) -> dict:
    """Query the Commons API for download URL, author and licence."""
    raw = _get(
        "https://commons.wikimedia.org/w/api.php",
        {
            "action": "query",
            "format": "json",
            "titles": entry["commons_file"],
            "prop": "imageinfo",
            "iiprop": "url|size|extmetadata",
        },
    )
    pages = json.loads(raw)["query"]["pages"]
    info = next(iter(pages.values()))["imageinfo"][0]
    meta = info.get("extmetadata", {})

    def m(key: str, default: str = "") -> str:
        return _strip_html(meta.get(key, {}).get("value", default))

    return {
        "download_url": info["url"],
        "descriptionurl": info["descriptionurl"],
        "width": info.get("width"),
        "height": info.get("height"),
        "author": m("Artist", "unknown"),
        "licence_short": m("LicenseShortName", "unknown"),
        "licence_long": m("UsageTerms", "") or m("LicenseShortName", ""),
        "attribution_source": "Wikimedia Commons API",
    }


def _apply_trim(entry: dict, meta: dict) -> dict:
    """Honour a manifest `author_trimmed`, and disclose that the string was edited."""
    if entry.get("author_trimmed"):
        meta = dict(meta)
        meta["author"] = entry["author_trimmed"]
        meta["attribution_source"] += " (author string trimmed of boilerplate, see manifest)"
    return meta


def resolve_plos(entry: dict) -> dict:
    """PLOS exposes figures at a stable URL; licence and author come from the manifest."""
    return {
        "download_url": (
            "https://journals.plos.org/plosone/article/figure/image"
            f"?size=large&id={entry['doi']}.{entry['figure']}"
        ),
        "descriptionurl": entry["article_url"],
        "width": None,
        "height": None,
        "author": entry["author"],
        "licence_short": entry["licence_short"],
        "licence_long": entry["licence_long"],
        "attribution_source": "declared in manifest, verified against the article page",
    }


RESOLVERS = {"wikimedia": resolve_wikimedia, "plos": resolve_plos}


def credit_line(entry: dict, meta: dict) -> str:
    if entry["source"] == "wikimedia":
        return f"Figure by {meta['author']}, {meta['licence_short']}, via Wikimedia Commons."
    if entry["source"] == "plos":
        return (
            f"Figure from {meta['author']}, {entry['journal']} {entry['year']}, "
            f"doi:{entry['doi']}, {meta['licence_short']}."
        )
    raise ValueError(entry["source"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-download files already present")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    blocks: list[str] = []

    for entry in FIGURES:
        name = entry["filename"]
        dest = OUT_DIR / name
        meta = _apply_trim(entry, RESOLVERS[entry["source"]](entry))

        # Only fetch what we can write directly. The two PDFs in this manifest were
        # converted from SVG by hand after an earlier download; re-fetching would
        # overwrite a PDF with an SVG, so they are resolved for credit only.
        fetchable = dest.suffix.lower() == Path(meta["download_url"]).suffix.lower() or (
            entry["source"] == "plos"
        )
        if fetchable and (args.force or not dest.exists()):
            print(f"fetching {name} ...", file=sys.stderr)
            dest.write_bytes(_get(meta["download_url"]))
        elif not dest.exists():
            print(f"WARNING: {name} absent and not auto-fetchable ({entry.get('note','')})",
                  file=sys.stderr)
        else:
            print(f"present  {name}", file=sys.stderr)

        lines = [
            f"## `{name}`",
            "",
            f"- **Illustrates:** {entry['illustrates']}",
            f"- **Author:** {meta['author']}",
            f"- **Licence:** {meta['licence_short']} ({meta['licence_long']})",
            f"- **Source:** {meta['descriptionurl']}",
        ]
        if meta.get("width"):
            lines.append(
                f"- **Original:** {entry.get('commons_file', name)}, "
                f"{meta['width']}x{meta['height']}"
            )
        if entry.get("bibkey"):
            lines.append(f"- **Cite as:** `\\cite{{{entry['bibkey']}}}` (see `thesis/refs.bib`)")
        lines.append(f"- **Attribution from:** {meta['attribution_source']}")
        lines += ["", "Caption credit line to use in the thesis:", "",
                  f"> {credit_line(entry, meta)}"]
        blocks.append("\n".join(lines))

    today = _dt.date.today().isoformat()
    header = (
        "# External figure credits\n\n"
        "Generated by `scripts/fetch_external_figures.py`. Do not edit by hand -- re-run\n"
        "the script instead, so the credits stay tied to the source. Wikimedia entries are\n"
        "pulled live from the Commons API; entries marked *declared in manifest* have their\n"
        "author and licence transcribed from the source article and verified against it.\n"
        f"Retrieved {today}.\n"
    )
    CREDITS.write_text(header + "\n" + "\n\n".join(blocks) + "\n")
    print(f"wrote {CREDITS.relative_to(REPO)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
