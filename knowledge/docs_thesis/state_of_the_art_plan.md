# State of the art (objective 4) — structure and direction

## Context

`06_geometry_risk.tex` moves out of the clinical background into this new chapter, so the clinical
background ends at hemodynamics. Everything below is already researched: `docs_thesis/literature.md`
(Axes 1–5, methods) and `docs_thesis/find_research.md` (Stages 1–6, evidence). **Nothing here needs a
new search.** Neither file's claims are full-text verified yet — see the queue at the bottom.

## The direction, in three sentences

The field's cohorts, machine learning and outcome data are all at **lesion scale** — plaque shape
and radiomics. **Tree-scale** geometry is studied in cohorts one to two orders of magnitude smaller,
against softer endpoints. This thesis goes up-scale: measure tree topology across thousands, describe
its distribution, and ask which individuals fall outside it — which no study in either research pass
has done.

## Structure

Open on the scale argument, with the evidence matrix as the central table. Then:

| § | Claim | Source |
|---|---|---|
| Opening | The field went to the lesion; tree scale is thin | `find_research.md` §6 evidence matrix — reproduce as a table, empty cells and all |
| 4.1 Getting the tree | Segmentation is solved well enough to build on; connectivity is the failure mode that matters | `literature.md` Axis 1 — `bransby2026imagecasx`, `qiu2025topology` |
| 4.2 Describing the tree | Normative atlases and automated geometric characterization exist, at n = 281–300 | `literature.md` Axis 2 — `medranogracia2016atlas`, `nannini2024characterization` |
| 4.3 Does tree geometry predict disease? | Feature by feature, ranked by evidence | `find_research.md` Stage 1 + its ranked feature table in §6; absorbs §6's Han/Juan/Wang/Zebić/Veltman |
| 4.4 Why shape is enough | Shear is recoverable from geometry, prognostic content intact — no CFD needed | `find_research.md` Stage 3 — `griffo2026wss` |
| 4.5 The nearest competitors | What exists and how this differs | `find_research.md` Stage 4 — `sun2026angiographcad`, `shen2026geometry` |
| 4.6 The gap | Nobody joins population scale to tree geometry to distribution | `find_research.md` §6 "The gap, stated for §4" — near-verbatim |

Order features in 4.3 by the ranking already done in `find_research.md` §6: bifurcation angle,
dominance, tortuosity, ramus intermedius; then the two empty cells — ostial take-off angle and branch
count — which is where objectives 8 and 9 live.

## What supports the direction

- Two tree-scale cells in the matrix are **empty**: progression and ischemia. `ThesisPlan.md` weeks
  11–14 propose exactly the first.
- **No cell anywhere** holds a population-distribution study. Two independent passes, on disjoint
  queries, reached this separately (`literature.md` Axis 4, `find_research.md` §6).
- The outcome cohort exists and is the one this project moves to — Fuchs, CGPS CCTA, n = 9533 with
  adjudicated MI (`find_research.md` Stage 2).
- `griffo2026wss` removes the CFD objection: shape carries the hemodynamic signal.
- `shen2026geometry` closes on mechanism "in individuals representative of large populations" — the
  field naming objective 8.

## Two corrections the merge forces

Both are in `find_research.md`'s repairs list and both currently make §6 wrong or incomplete:

1. **Dominance.** §6 cites `veltman2012dominance` alone (HR 3.20, n = 1425). The larger evidence
   contradicts it — `gebhard2015dominance` null at n = 6382, `khan2016dominance` OR 1.27 at
   n = 255,718. Restate as conditional. This also clears the single-source flag.
2. **Tortuosity.** §6 gives only the positive association with *non-obstructive* disease
   (`zebicmihic2023tortuosity`, OR 7.96). `groves2009tortuosity` (n = 1221) finds the **inverse**
   with obstructive disease. Not wrong as written, but incomplete in a way that reads as cherry-picked.

## Mechanics

- New `thesis/state_of_the_art/`, numbered files, same convention as `clinical_background/`.
- Move `06_geometry_risk.tex` content there; delete it from `clinical_background/`. Keep
  `\label{sec:geometry}` alive — referenced from `00_chapter_intro.tex`, `03_cad.tex` and
  `05_hemodynamics.tex`.
- `00_chapter_intro.tex` currently promises six sections including geometry; update it.
- The bifurcation-angle figure moves with the text.
- Run the `thesis-writing` skill over every new file.

## Verification

```bash
cd thesis
grep -rn 'ref{sec:geometry}' --include=*.tex .        # all resolve after the move
grep -rn 'sec:hemodynamics' --include=*.tex .         # still resolves
cd state_of_the_art
hunspell -l -t -d en_US -p ../wordlist.txt *.tex | sort -u          # empty
grep -nE 'has been reported|have been reported' *.tex               # empty
for f in *.tex; do keys=$(grep -o '\\cite{[^}]*}' $f | sed 's/\\cite{//;s/}//' | tr ',' '\n')
  t=$(printf '%s\n' "$keys" | grep -c .); [ "$t" -gt 2 ] || continue
  printf '%s\n' "$keys" | sort | uniq -c | sort -rn | head -1 |
    awk -v f="$f" -v t="$t" '{if ($1*3>t) print f": "$2" "$1"/"t" OVER"}'; done
```

Plus: every `n` in 4.3 traces to a cell in the matrix, and every empty cell in the matrix is one the
search record can account for.

## Before this carries weight

Every claim in both research files is **abstract-level**. Four papers do the heavy lifting here and
none is read: `griffo2026wss` (4.4), `shen2026geometry` (opening and 4.5), `sun2026angiographcad`
(4.5, the novelty claim is written against it), `gebhard2015dominance` (the correction above). Use
`/paper-review`, one at a time. Griffo needs DTU library access — ScienceDirect 403s.
