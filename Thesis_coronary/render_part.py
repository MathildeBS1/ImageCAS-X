"""Render one part of the thesis to its own PDF.

Usage (from anywhere):
    python Thesis_coronary/render_part.py technical
    python Thesis_coronary/render_part.py methodology --notes
    python Thesis_coronary/render_part.py content/methodology/03_features.tex

The part is compiled with the preamble of main.tex (pdfLaTeX + biber) and keeps its chapter
number from the full thesis. The PDF lands in Thesis_coronary/build/<part>.pdf. References to
labels outside the part show as ??.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"

# part name -> (chapter number in the full thesis, files to input, in order)
PARTS = {
    "introduction": (1, ["content/introduction"]),
    "literature": (2, ["content/litterature_review"]),
    "clinical": (3, [
        "content/background/chapter_intro",
        "content/background/heart_anatomy",
        "content/background/disease_and_risk",
        "content/background/wall_shear_stress",
        "content/background/ccta",
    ]),
    "technical": (4, [
        "content/technical/00_chapter_intro",
        "content/technical/01_glm",
        "content/technical/02_glmm",
        "content/technical/03_fpca",
    ]),
    "data": (5, ["content/data"]),
    "methodology": (6, ["content/methods"]),
    "results": (7, ["content/results"]),
    "discussion": (8, ["content/discussion"]),
    "conclusion": (9, ["content/conclusion"]),
    "appendix": (None, [
        "content/appendix/bifurcation_point",
        "content/appendix/link_choice",
        "content/appendix/mixed_model_details",
        "content/appendix/score2_recalibration",
    ]),
}


def preamble() -> str:
    """Everything in main.tex before \\begin{document}."""
    text = (ROOT / "main.tex").read_text()
    return text.split(r"\begin{document}")[0]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("part", help=f"one of {', '.join(PARTS)}, or a .tex path relative to Thesis_coronary/")
    ap.add_argument("--notes", action="store_true", help="show \\todonote draft notes")
    ap.add_argument("--open", action="store_true", help="open the PDF when done")
    args = ap.parse_args()

    if args.part in PARTS:
        name = args.part
        chapter, files = PARTS[name]
    else:
        path = Path(args.part)
        if not (ROOT / path).exists():
            sys.exit(f"Unknown part '{args.part}'. Choose from: {', '.join(PARTS)}, or give a .tex path.")
        name, chapter, files = path.stem, None, [path.with_suffix("").as_posix()]

    body = []
    if name == "appendix":
        body.append(r"\appendix")
    elif chapter is not None:
        body.append(rf"\setcounter{{chapter}}{{{chapter - 1}}}")
    body += [rf"\input{{{f}}}" for f in files]

    head = preamble()
    if args.notes:
        head = head.replace(r"\draftnotesfalse", r"\draftnotestrue")
    # A missing \input file is shown in red instead of stopping the build.
    guard = (r"\let\partorigInput\input" "\n"
             r"\renewcommand{\input}[1]{\IfFileExists{#1}{\partorigInput{#1}}"
             r"{\textcolor{red}{\textbf{[Missing file: \detokenize{#1}]}}}}" "\n")
    tex = head + guard + "\\begin{document}\n\\mainmatter\n\\pagestyle{fancy}\n" + "\n".join(body) + \
        "\n\\printbibliography[heading=bibintoc]\n\\end{document}\n"

    # The root file sits next to main.tex so that \input, figure and refs.bib paths resolve.
    BUILD.mkdir(exist_ok=True)
    job = f"part_{name}"
    src = ROOT / f"{job}.tex"
    src.write_text(tex)
    try:
        # -f: keep going past errors (e.g. a missing figure) so a draft PDF is still made;
        # -g: always rebuild, since the root file is recreated each run.
        cmd = ["latexmk", "-pdf", "-f", "-g", "-interaction=nonstopmode", f"-outdir={BUILD}", src.name]
        result = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, errors="replace")
    finally:
        src.unlink()

    pdf = BUILD / f"{job}.pdf"
    log = BUILD / f"{job}.log"
    if not pdf.exists():
        print(result.stdout[-3000:])
        sys.exit(f"Build failed, see {log}")
    if result.returncode != 0:
        errors = [l for l in log.read_text(errors="replace").splitlines() if l.startswith("!")]
        print(f"Built with {len(errors)} LaTeX error(s), see {log}:")
        for line in dict.fromkeys(errors):
            print("  " + line)
    out = BUILD / f"{name}.pdf"
    shutil.move(pdf, out)
    print(out)
    if args.open:
        subprocess.run(["open", out])


if __name__ == "__main__":
    main()
