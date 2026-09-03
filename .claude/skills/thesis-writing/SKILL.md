---
name: thesis-writing
description: Write or revise prose for the coronary topology master's thesis — chapters, weekly reports, abstracts, figure captions. Use whenever text is destined for the thesis document rather than for code comments or working notes.
---

# Writing the thesis

Every draft at submission standard — there is no drafting tier (below). Beat the reference
documents on precision and on clarity to a non-expert, never on length.

## The two calibration documents

Both are in `Former_students_work/`, both from this supervisor group. They set the level and are
never sources: **never cite student work.** Where one makes a claim you want, follow its citation
to the published work and cite that.

| Document | Calibrates | Read before |
|---|---|---|
| Korona & Baldachowski, *Tracing the coronary arteries in 3D CT scans* (DTU Compute, 2025) | chapters: depth, structure, citation density | any chapter |
| Aïda Jiménez Ordoñez, *Weekly report 1* (January 2026) | weekly reports: what a good week 1 looks like | any weekly report |

Every defect quoted below was verified in the submitted PDF.

## Write to teach

The reader is a classmate on this MSc program: an engineer, not a cardiologist. They should be able
to follow a section without opening a second source. Writing that only an examiner who already knows
the field can follow has failed, however precise it is.

- Define a term in the sentence where it first appears, in plain words. Korona §3.1 is the register
  to match: "vena cava - human body's largest vein", "interventricular septum (a wall separating
  ventricles)".
- Expand every abbreviation at first use, captions included.
- Trace a process before summarizing it — the path blood takes, what happens across the cardiac
  cycle — then give the number.
- Order inside a paragraph: name the thing, say what it does, then say why it matters here.
- Never use a term before the sentence that defines it, and check that after every round of cutting.
- The test: hand the paragraph to a classmate. If they need another source to follow it, rewrite it,
  whatever its word count.

## Length is not the win

Korona's clinical background is 1,482 words over 6 pages. Aida's week 1 is 4,810 words. Our
clinical background is already 3,710 words — 2.5× Korona's — and that is a liability unless each
extra word is earned.

**Earned:** a number measured from our 800 cases; a sentence that licenses a later claim; a caveat
that changes how a result is read.
**Unearned:** explaining a standard method the reader knows (Aida wk1 §1.5.4 spends half a page on
CNN layers, ResNets and GANs, used nowhere later); summarizing a study the thesis never uses; a
second sentence restating the first.

Test a paragraph by deleting it and asking whether a later claim loses support. If none does, it
stays deleted. Prefer a number to an adjective, a table to a paragraph, one sentence to two.

This pulls against *Write to teach*, and the resolution is fixed: **explanation for a first-time
reader is earned length; the same fact stated twice is not.** Cut the restatement, never the
definition or the causal step. A short paragraph that only asserts is worse than the longer one that
explains — and a compression pass that leaves a term defined nowhere has broken the section, not
tightened it.

## Match these — they are done right

- Clinical background before methods; abbreviations on first use and in the front matter; one
  figure per concept with a real source line; 1–3 citations per paragraph in background (Korona).
- Korona §3.1 for the didactic register: it builds from nothing, names all four chambers, traces the
  blood path and glosses each term in place. Beat it on delivery — its sentences are choppy and
  list-like ("There are two types of vales"), it writes "where the PDA branches of", and its
  prevalence figure ("in around 15% of the population") has no population behind it.
- State of the art organized by sub-question, not chronologically, one paragraph per study; a
  project plan table with a per-activity risk column; a problem statement running from the
  clinical problem to the specific gap (Aida wk1 §1.6, §1.1, §1.3).

## The study paragraph

Aida's is the pattern, missing its last element. Give: (1) author and year, (2) the data with n,
(3) what they did, (4) the number they got, and (5) **what it licenses here** — the sentence that
makes it a citation rather than a summary.

> Taylor et al. pooled 1070 coronary trees and placed Murray's exponent at 2.39 (95% CI
> 2.24–2.54) rather than the cubic value \cite{taylor2024murray}.
> Any feature defined as a deviation from Murray's law therefore uses the coronary exponent
> (Section~\ref{sec:geometry}).

## Beat these — each one shipped

| Where | What shipped | Rule |
|---|---|---|
| Korona wk2 (3×), Aida wk1 §1.8 | `??` and "Ansys Mechanical [?]" | never write a placeholder key; build and grep before sending |
| Korona wk2 → final thesis | `vales` for *valves* | see *Why no drafting tier* |
| Aida wk1 §1.4.1, §1.5.5 | "the responsable to transform"; "An scheme of the main FEM steps" | run hunspell, then read aloud; watch dropped articles and `a`/`an` |
| Aida wk1, all 14 pages | header reads "January 22, 2025", title page 2026 | never hand-type a date, version or count a command can compute |
| Aida wk1 Figs. 4, 5 | both captioned "Feedback scheme"; Fig. 5 is a CNN diagram | captions unique, and state that figure's takeaway |
| Aida wk1 refs [8], [9] | anatomy figures from a retailer's site and a blog, no licence | figures are ours, peer-reviewed, or licensed with attribution generated by `scripts/fetch_external_figures.py` |
| Aida wk1 §1.3 | "1.5 billion people worldwide [1]", cited to a segmentation paper | cite the origin of a number |
| Aida wk1 §1.5.4 | CNN/ResNet/GAN/XAI explainer, used nowhere later | every paragraph licenses a later claim, or is cut |
| Aida wk1 §1.6 | "impressive", "massive", "transformative", "famous for" | no praise borrowed from abstracts; give the number |
| Korona | "in around 15% of the population [25]" | value, range, population, source — and our cohort figure beside it, reconciled |
| Aida wk1 §1.7 | questions as fragments: "Frequency-dependent material properties?" | a question to a supervisor is a sentence naming the decision it unblocks |
| Aida wk1, whole report | no number from her own data | every weekly report carries a cohort number and names the script behind it |

## Why no drafting tier

```
$ printf 'the responsable part\nAn scheme of the steps\ntwo types of vales\n' | hunspell -l -d en_US
responsable
```

`responsable` is the only one a checker flags — and it shipped anyway, so no one ran it.
`An scheme` is grammar, and `vales` is a real word: both invisible. `vales` survived Korona's
week 2 into the submitted thesis, while `myocardial infraction` in the same report was fixed —
later proofreading catches the alarming error and misses the ordinary one. Run the checker, then
read aloud. Both, every draft.

## Prose

- Topic sentence carries the claim; a reader skimming first sentences gets the argument.
- One claim per sentence, each with its citation. Prefer sentences under 30 words.
- State the mechanism, not just the association. Quantify: number, range, population, source.
- Hedge once or not at all.
- Captions state the takeaway, not the contents, and no two are alike.
- One sentence per source line, so diffs show which sentence changed.
- American spelling (`-ize`, `-ization`) — matches Korona (56 `-ization` vs 2 `-isation`) and the
  cardiology literature. Watch `caliber`, `millimeters`, `labeled`.
- Banned: `delve`, `it is important to note`, `it is essential to`, `plays a crucial role`,
  `highlighting the urgent need`, `Moreover`/`Furthermore` chains, three-item lists for rhythm,
  and `impressive`/`massive`/`transformative`/`sophisticated`/`powerful` as praise.

## Sourcing

- Every clinical claim carries a citation, and the citation is the origin of the claim.
- Anatomy and physiology come from textbooks, reviews or primary literature — not vendor pages,
  blogs or course slides.
- Figure credits are copied from `figures/external/CREDITS.md`, never typed by hand.
- Cohort numbers name the script that produced them, and the script is re-run before submitting.
- When our cohort disagrees with a published value, report both and leave it open.

## Check before you call it done

```bash
# after a build, in the thesis folder
grep -c "Citation.*undefined"  main.log        # 0
grep -c "Reference.*undefined" main.log        # 0
pdftotext main.pdf - | grep -n '??\|\[?\]'     # empty -- Korona shipped ??, Aida shipped [?]

# stale dates: on Aida's week-1 PDF this prints "18 2025 / 3 2026" for a report written in
# January 2026 -- the stale running header, in one command
pdftotext main.pdf - | grep -o '20[0-9][0-9]' | sort | uniq -c | sort -rn | head

# every abbreviation expanded at first use: prints each one with the line it first appears on,
# so each can be checked against its expansion (this is what caught IQR, HU and LPS in §3.1)
grep -onE '\b[A-Z]{2,}[0-9]*\b' *.tex | sort -t: -k1,1n | awk -F: '!seen[$2]++'

# duplicate or contents-only captions
grep -h '\\caption' *.tex | sed 's/.*\\caption{//' | cut -c1-60 | sort | uniq -d   # empty

# spelling, with the project word list so domain vocabulary does not drown the signal
hunspell -l -t -d en_US -p wordlist.txt *.tex | sort -u                            # empty today

# real-word errors no checker catches, and borrowed praise
grep -nE '\b(vales|infraction|profusion|arteriosclerosis|torturosity|pericardial|sheer)\b' *.tex
grep -nEi '\b(impressive|massive|transformative|sophisticated|powerful|crucial|essential)\b' *.tex
```

| Written | Probably meant |
|---|---|
| vales | valves |
| infraction | infarction |
| profusion | perfusion |
| arteriosclerosis | atherosclerosis (different condition) |
| pericardial | epicardial (different location) |
| torturosity | tortuosity |
| ostium / ostia | singular / plural — check agreement after "two" |
| sheer | shear (as in wall shear stress) — both are real words, so nothing flags it |

Extend the table whenever a near-miss turns up, then read the section aloud; that is the only
reliable way to catch what nothing above flags.

`thesis/wordlist.txt` is the hunspell personal dictionary: 100 domain and LaTeX words, no prose
and no comments, because a misspelling added there is one the check can never catch again.
