---
name: thesis-writing
description: Write or revise prose for the coronary topology master's thesis — chapters, weekly reports, abstracts, figure captions. Use whenever text is destined for the thesis document rather than for code comments or working notes.
---

# Writing the thesis

Write every draft at submission standard. There is no drafting tier — see below for why.

## Calibrate against the previous thesis

Korona & Baldachowski, *Tracing the coronary arteries in 3D computed tomography scans*
(DTU Compute, 2025), in `Former_students_work/` — same supervisor, same dataset lineage.
Read the comparable section before writing one.

**It sets the level; it is not a source.** Use it to judge depth, structure, citation density
and tone. Never cite it, and never cite any student work in `Former_students_work/`. Where it
makes a claim you want, follow its citation to the published work and cite that instead.

**Match:** clinical background before methods; abbreviations defined on first use and listed
in the front matter; one figure per concept with a real source line; one to three citations
per paragraph in background sections.

**Beat, on four points that are real defects in their submitted work:**

| Defect | Rule |
|---|---|
| Three `??` unresolved citations shipped in the week-2 report | Never write a placeholder key. |
| `vales` for "valves" survived from that report into the final thesis | See *Why no drafting tier*. |
| "in around 15% of the population [25]" | Give value, range, population, source. Where our cohort measures the same thing, give both and reconcile. |
| No section linking geometry to clinical risk | Every background section must license a later claim. If it licenses nothing, cut it. |

## Why no drafting tier

`myocardial infraction` (for *infarction*) appears in their week-2 report and was fixed by
submission. `vales` (for *valves*) appears in both and never was. Both are real English
words, so no spell checker flags either:

```
$ printf 'two types of vales\nmyocardial infraction\n' | hunspell -l -d en_US
myocardial      # false positive on domain vocabulary; neither real error is flagged
```

Later proofreading catches the alarming error and misses the ordinary one.

## Prose

- Topic sentence carries the claim. A reader skimming first sentences should get the argument.
- One claim per sentence, each with its citation.
- State the mechanism, not just the association.
- Quantify: number, range, population, source.
- Banned: `delve`, `it is important to note`, `plays a crucial role`, chains of
  `Moreover`/`Furthermore`, three-item lists for rhythm.
- Hedge once or not at all.
- American spelling (`-ize`, `-ization`) — matches their thesis (56 `-ization` vs 2
  `-isation`) and the cardiology literature. Watch `caliber`, `millimeters`, `labeled`.
- One sentence per source line, so diffs show which sentence changed.
- Captions state the takeaway, not the contents.

## Sourcing

- Every clinical claim carries a citation.
- Figures are ours or carry a licence and attribution line.
- Numbers from our cohort must be reproducible; name the script that produced them.
- When our cohort disagrees with a published value, report both and leave it open.

## Check before you call it done

```bash
# in your thesis folder, after a build
grep -c "Citation.*undefined"  main.log      # 0
grep -c "Reference.*undefined" main.log      # 0
pdftotext main.pdf - | grep '??'             # empty

# real-word errors no spell checker catches
grep -nE '\b(vales|infraction|profusion|arteriosclerosis|torturosity|pericardial)\b' *.tex
```

| Written | Probably meant |
|---|---|
| vales | valves |
| infraction | infarction |
| profusion | perfusion |
| arteriosclerosis | atherosclerosis (different condition) |
| pericardial | epicardial (different location) |
| torturosity | tortuosity |

Extend the table whenever a near-miss turns up. Then read the section aloud — it is the only
reliable way to catch a real-word error.
