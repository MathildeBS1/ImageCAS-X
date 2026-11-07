# Locating a partially annotated reference stretch on an automatic centerline (start/end + cross-section pairing)

Scope note: I read the primary text of Schaap et al. 2009 (NIH author manuscript, full text) and of several secondary/related papers. The full text of Kirisli et al. 2013 could not be retrieved (Elsevier 403, HAL bot wall, no PMC copy), so its exact clipping and pairing rules are **not verified** here and are listed as a gap.

## 1. How did the CAT08 (Schaap 2009) and Rotterdam lumen benchmark (Kirisli 2013) define the evaluated stretch and pair reference with test points?

### Takeaway
CAT08 clips only the **start** of the evaluated centerline with a disc at the reference start point (radius = 2 x annotated radius, normal = reference tangent there), then pairs points with a **monotone (order-preserving) minimum-total-Euclidean-length correspondence** found by Dijkstra on a distance matrix, which is the same idea as dynamic time warping. There is no distal clipping disc; the distal end is handled by the correspondence plus TP/FP labelling. Kirisli 2013's lumen evaluation details could not be verified.

### Cited Findings
- Schaap 2009 is "Standardized evaluation methodology and reference database for evaluating coronary artery centerline extraction algorithms", Med Image Anal 13(5):701–714, DOI 10.1016/j.media.2009.06.003; 32 CCTA datasets, 13 algorithms — [repub.eur.nl record](https://repub.eur.nl/pub/24468); full text read from the [NIH author manuscript (UNC repository copy)](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Reference definition: the centerline passes through the lumen centre of gravity in each cross-section; start = centre of the coronary ostium; end = "the most distal point where the artery is still distinguishable from the background" — [Schaap 2009 §4.2](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Reference start/end were themselves defined by agreement: "The points where for the first time the centerlines of two observers lie within the radius of the reference standard when traversing over this centerline from respectively the start to the end or vice versa were selected as the start- and end point of the reference standard" — [Schaap 2009 §4.2](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Resampling: both centerlines are "sampled equidistantly using a sampling distance of 0.03 mm" before correspondence — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- **Clipping disc (start only)**: "The evaluated centerline is then clipped with a disc that is positioned at the start of the reference standard centerline ... The radius of the disc is twice the annotated vessel radius and the disc normal is the tangential direction at the beginning of the reference standard centerline. Every point before the first intersection of a centerline and this disc is not taken into account during evaluation." Stated reason: many methods start their centerline inside the aorta — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- **Correspondence**: minimise the sum of Euclidean lengths of all point–point connections over all *valid* correspondences, where c0 = [p0, q0] (start points connected), the last connection joins the end points, and each step advances one index on one curve only ([pa+1, qb] or [pa, qb+1]); "These conditions guarantee that each point of centerline I is connected to at least one point of centerline II and vice versa." Solved with Dijkstra on the connection-length matrix — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- The same Dijkstra correspondence was used to transfer observer radii onto the consensus reference (radius = mean of all connected observer points) — [Schaap 2009 §4.2](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Labelling: a reference point is TP if at least one connected test point lies within the annotated radius, else FN; a test point is TP if at least one connected reference point is within that reference point's radius, else FP — [Schaap 2009 §4.4.1](https://cdr.lib.unc.edu/downloads/cn69mc016).
- First-error rule ignores FN points in the first 5 mm, because "the beginning of a coronary artery centerline is sometimes difficult to define"; 5 mm = mean annotated diameter at the start — [Schaap 2009 §4.4.2](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Distal limit for the clinically relevant overlap (OT): the point closest to the reference end with radius ≥ 0.75 mm is found; only reference points between start and that point, and test points connected to them, are used — [Schaap 2009 §4.4.2](https://cdr.lib.unc.edu/downloads/cn69mc016). (So a distal truncation is done on the *reference*, and the test stretch is inherited through the correspondence, not by a second disc.)
- Accuracy (AI) is averaged only over connections shorter than the annotated radius, i.e. only where tracking succeeded — [Schaap 2009 §4.4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Secondary paraphrase of the same rules (TP = within radius of closest reference point; OT uses radius ≥ 0.75 mm) in Wolterink et al. 2019 (Med Image Anal; arXiv version) — [arXiv 1810.03143](https://arxiv.org/pdf/1810.03143).
- Kirisli et al. 2013, Med Image Anal 17(8):859–876, DOI 10.1016/j.media.2013.05.007: 48 multicentre, multivendor CCTA datasets, 11 groups, stenosis detection/quantification and lumen segmentation — [Lancashire repository record](https://knowledge.lancashire.ac.uk/id/eprint/8978/). Downstream users report Dice, mean surface distance and Hausdorff separately for healthy and diseased segments (e.g. GCN mesh method Dice 0.75/0.73, MSD 0.25/0.28 mm) — [Wolterink et al. 2019, arXiv 1908.05343, preprint version of a MICCAI-workshop paper](https://arxiv.org/abs/1908.05343).
- In the Kirisli training set "reference surface meshes were annotated by three observers in a selection of segments in each data set, for a total of 78 coronary artery segments" — i.e. the lumen reference is itself partial (segments, not trees), which is the same situation as the Medis contours — [Wolterink 2019 arXiv 1908.05343](https://arxiv.org/abs/1908.05343).

### Inferences
- The CAT08 recipe transfers almost directly: (a) clip the tracer centerline proximally with a disc at the first Medis cross-section (centre = contour centroid, normal = Medis contour plane normal or local Medis tangent, radius ≈ 2 x equivalent lumen radius); (b) analogously clip distally with a disc at the last Medis cross-section (an extension; CAT08 did not do this because its reference ran to the vessel end); (c) pair cross-sections with an order-preserving min-sum-distance alignment between the Medis centroid sequence and the clipped tracer points.
- The disc radius limit (2r) is what stops the clip from firing on a neighbouring branch or on the aorta wall: only a crossing *within* the disc counts. Using an infinite plane instead would risk clipping at the wrong place where the vessel curves back across the plane.
- The monotone constraint removes the main failure of independent nearest-point matching (back-and-forth jumps), but by construction forces start-to-start and end-to-end connection, so it must be run *after* clipping; otherwise unmatched tails create long many-to-one connections that bias the measured distances.
- Schaap's own reference end points were defined by "first point within radius" traversal from each end — a simple, citable rule that can be reused: walk the tracer centerline from proximal to distal and take the first tracer point within r of the first Medis centroid (and symmetric from the distal side).

### Gaps
- Exact Kirisli 2013 rules for clipping test lumen surfaces to the reference segment (planes vs discs vs masks, how start/end markers were set) were not verified: full text unavailable via all routes tried (ScienceDirect 403, HAL bot challenge, no Europe PMC open copy). Should be checked in the PDF before citing any specific mechanism.
- Schaap 2009 does not report a failure analysis of the disc clip itself (e.g., how often the disc was missed).

## 2. How do CCTA-vs-IVUS/OCT and CCTA-vs-QCA studies match a lesion or stretch between modalities?

### Takeaway
Clinical validation studies almost always match stretches manually with **fiducial landmarks** (ostium, side branches, calcifications, stent edges), and then step along the centerline by **distance (arc length) from a landmark or ostium**, often with linear interpolation between two landmarks. Automatic methods add DTW/dynamic programming or learned registration. These are cross-modality problems; the Medis-vs-tracer case (same volume, same LPS mm space) is much easier, since no landmark is needed to put both in one coordinate frame.

### Cited Findings
- Leber et al. matched CTA and IVUS plaque using manually selected fiducial points ("side branches, calcified plaques and the origin of the stents"); Voros et al. and Brodoefel et al. followed the same rationale — as summarised by [Athanasiou et al. 2016, BMC Med Imaging (PMC4719213)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4719213/).
- Athanasiou et al. 2016: "Experts selected manually, segments of arteries which were assessed with both CTA and IVUS imaging. Side branches were used as fiducial points to define correspondence between CTA and IVUS." — [PMC4719213](https://pmc.ncbi.nlm.nih.gov/articles/PMC4719213/).
- van der Giessen et al.: user-defined landmarks give bifurcation correspondences and "the CCTA centerline is linearly interpolated between bifurcation correspondences"; Marquering et al. combined manual landmarks with automatic contour detection — as summarised by [van Herten et al., arXiv 2412.17100 (preprint, Dec 2024)](https://arxiv.org/html/2412.17100v1).
- van Herten et al. (preprint) register CCTA to IVUS automatically using detected bifurcations, calcifications and guidewire artefacts plus normalised mutual information; success judged with a Schaap-style centerline overlap (F1 at 2 mm threshold) and plane-normal cosine similarity; 40/48 successful; failures came from IVUS runs with few/no landmarks (multiple similar minima) and poor CCTA quality (failed centerline) — [arXiv 2412.17100](https://arxiv.org/html/2412.17100v1). Preprint; not peer reviewed as far as the text shows.
- For IVUS–IVUS: "linear fitting (distance normalization)" between landmarks assumes constant pullback speed, which is not always true; Zhang et al. instead solve location + rotation by dynamic programming on a 3D graph, mean location error 0.72–0.79 mm vs inter-observer 0.62–0.67 mm, worst cases 8.4 mm; failures at distal landmarks and frame "jumps" — [Zhang et al. 2015, IEEE TMI 34(12):2550 (PMC4700818)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4700818).
- Zhang et al. also find start/end pairs automatically with a minimum 25 mm required overlap — [PMC4700818](https://pmc.ncbi.nlm.nih.gov/articles/PMC4700818).
- Serial CCTA: one JACC Cardiovasc Imaging 2009 study coregistered cross-sections "by use of the distance from the right coronary ostium", stepping 1 mm along the centerline — reported in search summary of [JACC Cardiovasc Imaging 2009, doi 10.1016/j.jcmg.2009.07.007](https://www.jacc.org/doi/10.1016/j.jcmg.2009.07.007) (not read in full; verify).
- Serial CCTA nonlinear registration (Med Phys 2010) used coronary segmentation as landmarks for dense deformable registration; success 9/10 — [PubMed 20229898](https://pubmed.ncbi.nlm.nih.gov/20229898/) (abstract-level only).
- INVICTUS (Eur Radiol 2026): an IVUS core lab mapped ostium, side branches, calcifications and stenoses in both modalities to match segments; 26 vessels excluded for image quality or co-registration problems; 108 co-registered segments analysed — [Eur Radiol, doi 10.1007/s00330-026-12412-y](https://link.springer.com/article/10.1007/s00330-026-12412-y) (from search summary; not read in full).
- The 2024 SCCT standards for quantitative CCTA reportedly recommend co-registration using landmarks such as side branches and calcifications — [J Cardiovasc Comput Tomogr 2024](https://www.journalofcardiovascularct.com/article/S1934-5925(24)00341-1/fulltext) (403 on fetch; claim is from search summary only; verify before citing).

### Inferences
- Landmark + arc-length methods solve a problem the tracer-vs-Medis comparison does not have (different coordinate frames, pullback speed). Their useful lesson is the *1D parametrisation*: once the stretch ends are fixed, position along it can be expressed as arc length (or normalised arc length), and pairing can be done in 1D.
- Arc length from the ostium is fragile between two different centerlines: a small proximal offset (the start in the aorta or ostium definition) shifts every downstream position, and length differences from different smoothing/tortuosity accumulate distally ("distal drift"). Normalising arc length between two matched endpoints (linear interpolation between landmarks) limits that drift to within the stretch.
- Because Medis and tracer share one LPS mm space, the Medis contour centroids themselves are 3D landmarks on every cross-section; no side-branch fiducials are needed. Side branches only matter as a source of error (the tracer centerline or a nearest-point lookup crossing into a branch).

### Gaps
- Primary texts of Boogers, Voros, Brodoefel CCTA–IVUS papers were not read; their methods are cited only via the Athanasiou 2016 summary.
- No CCTA-vs-QCA paper was read that describes stretch matching in detail.

## 3. Nearest-point projection vs arc-length vs DTW-style correspondence: what is known, failure modes?

### Takeaway
The benchmark literature (CAT08) explicitly chose an **order-preserving, globally optimal** correspondence instead of independent nearest-point matching; the IVUS literature uses DTW/dynamic programming with smoothness penalties. Independent nearest-point projection is simple and accurate where curves are close, but has no ordering guarantee. I found no peer-reviewed paper that quantifies nearest-point failure rates for coronary centerlines; the failure modes below are partly inference.

### Cited Findings
- CAT08 correspondence is a monotone alignment (each step advances one index on one curve), minimising the summed Euclidean connection length, with both ends forced to connect — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016). This is structurally a DTW alignment with Euclidean local cost.
- CAT08 counts accuracy only on connections shorter than the reference radius, separating "tracking failure" (distance irrelevant) from "accuracy" — [Schaap 2009 §4.4.3](https://cdr.lib.unc.edu/downloads/cn69mc016). A useful guard: Medis–tracer pairs further apart than ~r should be flagged as mismatches, not averaged into lumen error.
- DTW for IVUS pullbacks: cost 1 − |NCC|; a regularisation term favours diagonal steps to reduce many-to-one mappings; authors note "a one-to-one image correspondence between the two sequences may not be always possible" and that error grows with pullback length; in vivo mean alignment error 4.3 ± 3.9 frames — [Tsiknakis et al. 2021, Diagnostics 11(8):1513 (PMC8394087)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8394087/).
- The same paper notes that first/last frames of two sequences can cover different vessel regions, so ends must be handled (partial overlap tested by removing 60–80% from the ends) — [PMC8394087](https://pmc.ncbi.nlm.nih.gov/articles/PMC8394087/).
- Linear distance normalisation between landmarks fails when the sampling rate along the vessel is not uniform (pullback speed) — [Zhang et al. 2015 (PMC4700818)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4700818).

### Inferences (not directly sourced; flag as reasoning)
- **Nearest-point projection of a Medis centroid onto the whole tracer tree**: failure 1, jumping to a neighbouring vessel or side branch where they pass within a few mm (LM bifurcation, LAD–diagonal, LCx–OM, RCA crossing near the right atrium); failure 2, non-monotone order at tight bends (consecutive Medis sections map back and forth); failure 3, at a stretch end that lies beyond the traced extent, every remaining Medis section snaps to the tracer's terminal point (pile-up). Mitigation: restrict projection to the correct tracer branch/path first, require distance < k·r, and check monotonicity of the projected arc-length.
- **Arc-length matching**: robust ordering, but sensitive to the start anchor and accumulates length differences distally (different smoothing, tortuosity, the tracer step size). Normalising between both matched ends limits this to a linear stretch.
- **DTW / Schaap-style monotone alignment**: guarantees ordering and gives a global optimum, but forces end-to-end matching (needs clipping first) and allows many-to-one plateaus; a diagonal-favouring penalty (as in Tsiknakis 2021) or open-end DTW variants address these.
- A practical hybrid consistent with the literature: (1) choose the tracer path (vessel) whose points are closest to the Medis centroids on average; (2) clip with discs at the first and last Medis sections (CAT08-style, 2r radius, contour normal); (3) monotone min-sum alignment on the clipped stretch; (4) discard pairs with distance > r as mismatches and report how many.

### Gaps
- No peer-reviewed study found that compares nearest-point vs arc-length vs DTW correspondence head-to-head for coronary CCTA centerlines, or that reports how often nearest-point projection jumps to a neighbouring vessel.
- VMTK documentation (vmtkcenterlineattributes abscissas, branch clipping) could not be fetched (403); not cited.

## 4. Published use of a clipping plane/disc from the reference start/end point and tangent

### Takeaway
Yes: CAT08 (Schaap 2009) is the canonical published example — a disc at the reference start point, radius = 2 x annotated radius, normal = reference tangent, discarding all test points before the first intersection. I found no equally explicit published distal disc; distal limits in CAT08 are imposed on the reference (end point, OT radius rule) and inherited by correspondence.

### Cited Findings
- Disc at reference start, radius 2r, normal = tangent at start; "Every point before the first intersection of a centerline and this disc is not taken into account during evaluation." — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- Reasoning given: ostium is the defined start, yet "for a variety of applications the centerline can start somewhere in the aorta" — [Schaap 2009 §4.3](https://cdr.lib.unc.edu/downloads/cn69mc016).
- The CAT08 framework and its metrics are reused by later CCTA-centerline papers (e.g. Wolterink 2019) and by a CCTA–IVUS registration preprint (overlap/F1 at 2 mm) — [arXiv 1810.03143](https://arxiv.org/pdf/1810.03143); [arXiv 2412.17100](https://arxiv.org/html/2412.17100v1).

### Inferences
- A distal disc built the same way (at the last Medis section, normal = its contour normal pointing distally, radius 2r) is a direct, defensible extension; it should be described as an adaptation of Schaap 2009, not as a published standard.
- For Medis contours, the contour plane normal is available directly from the contour points (fit a plane), which is likely a better disc normal than a finite-difference tangent of a few centroid points; this is a design choice, not a sourced finding.
- Failure modes of the disc clip: if the tracer stops before the last Medis section, the distal disc is never crossed (must fall back to the tracer end and record truncated coverage); if the tracer enters a side branch near the stretch end, it may cross the 2r disc off-centre or not at all; a too-large radius can be crossed by a parallel neighbouring vessel.

### Gaps
- Whether Kirisli 2013 used planes/discs to clip lumen surfaces to the annotated segments remains unverified (see §1 Gaps).
