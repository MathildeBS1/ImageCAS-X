#!/usr/bin/env python3
"""Generate thesis/refs_clean.bib from thesis/refs.bib and the thesis .tex fragments.

refs.bib is the working bibliography: it carries provenance comments and per-entry
`note` markers ([VERIFIED], [BOOK], [PARTIAL], [BIBLIOGRAPHY VERIFIED]) that say how far
each reference has been checked. refs_clean.bib is the same bibliography with that
apparatus removed -- the file a compiled thesis reads.

Two rules define it, both taken from the file as it already stood:

  1. Only entries actually cited by a thesis .tex fragment are carried over.
  2. Everything else about an entry is kept verbatim, minus its `note` field.

Entries keep the order they have in refs.bib, so the sectioning of the working file
still shows through in the generated one.

    python scripts/make_refs_clean.py            # write thesis/refs_clean.bib
    python scripts/make_refs_clean.py --check    # verify only, non-zero exit on a problem

--check reports a citation with no refs.bib entry (which would compile to a bare `?`)
and a refs_clean.bib that has drifted from what refs.bib plus the .tex files imply.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "thesis" / "refs.bib"
OUT = ROOT / "thesis" / "refs_clean.bib"

ENTRY_START = re.compile(r"^@(\w+)\{([^,\s]+)\s*,", re.M)
CITE = re.compile(r"\\(?:cite|citep|citet|autocite|textcite)\w*(?:\[[^\]]*\])*\{([^}]*)\}")
COMMENT = re.compile(r"(?<!\\)%.*$", re.M)


def tex_files():
    """Every thesis .tex fragment, in a stable order."""
    return sorted((ROOT / "thesis").rglob("*.tex"))


def cited_keys():
    """Citation keys used anywhere in the thesis, mapped to the files that use them.

    This deliberately includes the working-reference and draft fragments as well as the
    body text: a key cited only there is still a reference the thesis has taken a view
    on, and dropping it from refs_clean.bib would lose it on the next rewrite.
    """
    keys = {}
    for path in tex_files():
        text = COMMENT.sub("", path.read_text())
        for match in CITE.finditer(text):
            for key in match.group(1).split(","):
                key = key.strip()
                if key:
                    keys.setdefault(key, []).append(path)
    return keys


def parse_entries(text):
    """Return [(key, raw entry text)] in source order, brace-matched."""
    entries = []
    position = 0
    while True:
        match = ENTRY_START.search(text, position)
        if match is None:
            return entries
        opening = text.index("{", match.start())
        depth = 0
        for index in range(opening, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    break
        else:
            raise ValueError(f"unbalanced braces in entry {match.group(2)}")
        entries.append((match.group(2), text[match.start() : index + 1]))
        position = index + 1


def split_fields(entry):
    """Split an entry into its header line and its top-level `field = {...}` chunks."""
    body = entry[entry.index("{") + 1 : entry.rindex("}")]
    header, _, rest = body.partition(",")
    fields = []
    depth = 0
    current = ""
    for char in rest:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        if char == "," and depth == 0:
            fields.append(current)
            current = ""
        else:
            current += char
    if current.strip():
        fields.append(current)
    return entry[: entry.index("{") + 1], header, fields


def strip_note(entry):
    """The entry with its `note` field dropped and its remaining fields left untouched."""
    prefix, header, fields = split_fields(entry)
    kept = [f for f in fields if not f.strip().lower().startswith("note")]
    if len(kept) == len(fields):
        return entry
    return prefix + header.strip() + "," + ",".join(kept).rstrip() + "\n}"


def render(entries, cited):
    """The generated file: cited entries only, source order, notes removed."""
    return "\n\n".join(strip_note(raw) for key, raw in entries if key in cited) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify only, write nothing")
    args = parser.parse_args()

    entries = parse_entries(SOURCE.read_text())
    known = {key for key, _ in entries}
    cited = cited_keys()

    missing = sorted(set(cited) - known)
    if missing:
        for key in missing:
            where = ", ".join(sorted({str(p.relative_to(ROOT)) for p in cited[key]}))
            print(f"error: {key} is cited in {where} but has no refs.bib entry", file=sys.stderr)
        return 1

    text = render(entries, cited)
    uncited = len(known) - len(cited)

    if args.check:
        if OUT.read_text() != text:
            print(f"error: {OUT.relative_to(ROOT)} is out of date -- re-run without --check",
                  file=sys.stderr)
            return 1
        print(f"{len(cited)} cited entries up to date ({uncited} in refs.bib cited nowhere)")
        return 0

    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)} with {len(cited)} cited entries "
          f"({uncited} in refs.bib cited nowhere)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
