# Side-by-side 3D visualisation of the two case-study RCAs (scans 662 and 518)

Population: two ImageCAS-X training scans, RCA only (label 9), the same curves as `easy_metrics.md` and `advanced_metrics.md`. No metric was recomputed; every number on the figure is read from `easy_metrics.json` (σ 0 entries only), `advanced_metrics.json`, `easy_pointwise.npz` and `advanced_pointwise.npz`. Percentiles are the mid-rank percentiles among the 560 training RCAs already stored in those files. The Disease column was not read.

Script: [visualise.py](file:///zhome/e2/6/224426/project/ImageCAS-X/tortuosity/research/case_study/visualise.py) (login node, CPU, a few seconds). Outputs: [rca_tortuosity_comparison.html](file:///work3/s254124/imagecasx_results/tortuosity_research/case_study/rca_tortuosity_comparison.html) (58 kB, plotly.js 2.35.2 from jsdelivr, data inline) and [rca_tortuosity_comparison.png](file:///work3/s254124/imagecasx_results/tortuosity_research/case_study/rca_tortuosity_comparison.png) (4800 × 3150 px, 300 dpi).

## How should two centerlines be shown so the eye can check the numbers?

### Takeaway
Treat the two RCAs as small multiples: one mm scale, one orthographic camera (LAO 30 by default, RAO 30 and AP on a toggle), linked rotation, one shared curvature colour scale, and a linked curvature-vs-arc-length strip so every bend marker in 3D has a peak underneath it. Numbers sit beside each view in identical row order so the two tables read across.

### Cited Findings
- Small multiples only work when every panel shares axes and scale; auto-scaling per panel encodes the same value differently and breaks the comparison ([Wikipedia, Small multiple](https://en.wikipedia.org/wiki/Small_multiple); [Forum One](https://www.forumone.com/insights/blog/good-data-visualization-practice-small-multiples/)).
- Plotly 3D cameras are set by `eye`, `up` and `center` in normalised domain coordinates ((0,0,0) is the centre of the domain regardless of data), and `projection.type` can be `orthographic` ([Plotly 3D camera controls](https://plotly.com/python/3d-camera-controls/); [Plotly camera reference](https://plotly.com/python-api-reference/generated/plotly.graph_objects.layout.scene.camera.html)). Orthographic projection preserves parallelism and is better suited to reading data than perspective ([plotly.js issue 2611](https://github.com/plotly/plotly.js/issues/2611)).
- Matplotlib 3D uses `view_init(elev, azim, roll)` and `set_proj_type('ortho')` for the same camera ([matplotlib view_init](https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.view_init.html)).
- LAO means the image intensifier sits over the patient's left chest, RAO over the right, with the angle from AP as suffix ([search summary of angiography patents and papers, e.g. Viewpoint Planning for QCA](https://arxiv.org/pdf/1808.00853)). The case-study code uses d = (sin a cos c, −cos a cos c, sin c) in LPS (`compute_simple.view_dir`), which puts the LAO 30 eye anterior and to the patient's left; with superior up this shows the patient's left on screen right, the usual angiographic display.
- Rainbow colour maps have perceptual kinks that create false features; perceptually ordered sequential maps are preferred ([HESS 2021](https://hess.copernicus.org/articles/25/4549/2021/); [matplotlib colormaps guide](https://matplotlib.org/stable/users/explain/colors/colormaps.html)).
- Colouring a centerline by a windowed curvature (angle between entry and exit direction over window length) is an established way to show where a vessel bends ([ScienceDirect topic summary, vessel centerline](https://www.sciencedirect.com/topics/computer-science/vessel-centerline)).

### Inferences
Design choices made in `visualise.py`, and why:
- **Same scale.** Each curve is translated to its own bounding-box centre (of the σ 0 curve) and both scenes get the same cube range ±R, R = 35 mm (the larger half-extent × 1.08, rounded up to 5 mm). Same x ticks in both PNG panels confirm this. Centring per curve (rather than a common LPS origin) is needed because the two scans sit in different scanner positions; it changes nothing about shape or size.
- **Same camera.** Orthographic, eye along view_dir(30), up = superior, identical eye norm in both scenes. Orthographic matches both angiography and the DM2 LAO 30 number on the panel, so the 2D arc/chord printed there is what the viewer is looking at. In the HTML, dragging one scene relays the camera to the other (`plotly_relayouting`), with a checkbox to unlink; buttons set LAO 30, AP or RAO 30 on both.
- **Colour.** |ψ| = √(k1² + k2²) on the σ0 1.25 mm curve, not turn5, because turn5 is undefined within 5 mm of each end and would hide 662's ostial kink, which is the single most important feature for reading kB and max bend. One shared scale 0 to 0.20 mm⁻¹ (radius 5 mm), clipped: 662's kink peaks at 0.56 and would otherwise flatten everything else. Custom sequential ramp slate grey → ochre → orange → crimson, monotone in lightness contrast from the low end, chosen so the low end stays visible on both light and dark backgrounds.
- **Markers.** Ostium filled dot "O", distal end open dot "E", bends ≥ 45° (easy.py, σ 0, centres) as diamonds with the angle; the chord O to E as a thin dashed line so arc/chord is visible as "path vs dashed line"; 662's first barcode turn (0 to 6.5 mm) as a translucent crimson halo labelled "ostial kink". Bend markers are placed on the σ 0 curve; the drawn line is the σ0 1.25 mm curve, which lies within 0.13 mm of it at the ends.
- **Numbers panel.** Easy (σ 0): arc/chord, LAO 30 shadow arc/chord, κa@5, total turning, bends ≥45°/≥90°, largest bend with position. Advanced (σ0 1.25 mm): kB, wiggle share, f_twist, ACN, direction sphere coverage and tangent out-of-plane variance (indicatrix spread), barcode turns ≥ 90° with largest turn, SRVF distance between the two. Percentile in brackets and, in the HTML, as a dot on a 0 to 100 track, so rank is visible without reading digits. Each row has a one-line meaning (small text, also as hover title). At ≥ 1280 px the layout is mirrored (3D | numbers | numbers | 3D) so the two tables sit next to each other; 760 to 1280 px puts both views on top and both tables below; narrow screens stack view, table, view, table.
- **Linked strip.** One row per case, shared x (0 to 110 mm) and y (0 to 0.30 mm⁻¹): solid |ψ|, dotted turn5, shaded barcode turns ≥ 45° with angles, dashed verticals at the bends ≥ 45° shown in 3D. Hovering the strip places a ring cursor on the matching point of the 3D curve.
- **Theme.** CSS tokens on `:root` with dark variants under `prefers-color-scheme` (guarded by `:root:not([data-theme="light"])`) and `:root[data-theme="dark"]`; plotly colours are read from the tokens and redrawn on a theme change.

### Gaps
- The HTML has not been opened in a browser here (no browser or node on the login node), so the JavaScript was not executed or syntax-checked. The PNG was inspected.
- Plotly's documentation found does not say whether eye distance sets zoom in orthographic mode; both scenes use the same eye norm, so they match either way.
- I found no source that prescribes a standard for displaying 3D coronary tortuosity; the design follows general small-multiple and colour-map guidance.

## Does the eye agree with the numbers?

### Takeaway
Mostly yes for local bendiness: 518 visibly carries more, sharper and more spread-out bends, as κa, total turning and bend count say. No for arc/chord: in LAO 30 both look like a C of similar openness, matching the small DM and DM2 gaps rather than the κa doubling. The ostial kink that drives 662's kB and max bend is nearly invisible in LAO 30 because it runs close to the view direction, so those two numbers disagree with what the eye sees in the standard view.

### Cited Findings
All from the PNG (LAO 30) and an extra inspection render of both curves in RAO 30, left lateral, AP and superior views made with the same scale (scratch only, not a deliverable), plus values in `easy_metrics.md` and `advanced_metrics.md`:
- 662 in LAO 30 is a clean C: a straight descent then a smooth turn into the distal limb, colour mostly slate to ochre. Its only bend ≥ 45° (127° at 2.4 mm) is a small hook at the ostium, a few mm across on screen. On the strip, |ψ| after 6 mm stays below about 0.13 mm⁻¹, with the broad 67° barcode turn at 59 to 79 mm as the only other structure.
- 518 in LAO 30 has a flat proximal segment turning sharply down (bends at 1.8 and 15 mm), a visible kink at 34 mm, and a tighter lower curve with bends at 66 and 77 mm. Its line shows more orange and crimson along the whole length. The strip shows five |ψ| peaks lining up with the five dashed bend lines and three shaded barcode turns of 157°, 131° and 110°.
- Chord: the dashed chord of 518 is visibly shorter relative to the path (D 52.2 vs 63.3 mm), but the overall C outline of the two looks similar in size, consistent with arc/chord 2.00 vs 1.73 and LAO 30 arc/chord 1.94 vs 1.85.
- Planarity: in the lateral and superior views 662 stays close to one plane (near-straight line in lateral view), while 518 shows an S in lateral view and a hook in superior view, matching f_twist 0.15 vs 0.46 and tangent out-of-plane variance 0.019 vs 0.126.
- 662's |ψ| trace carries many small ripples (0.05 to 0.10 mm⁻¹) that do not show as colour change in 3D; this is the fine-scale ripple that the advanced notes found collapses by σ 4 mm.

### Inferences
- Measures the eye confirms: κa@5, total turning, bends ≥ 45°, barcode turns ≥ 90°, f_twist (once the view is rotated). ACN (0.15 vs 0.41) is plausible from the shorter chord and the out-of-plane S of 518, but no single view shows a self-overlap, so the eye cannot really check it.
- Measures the eye does not support in LAO 30: largest bend (662 127° vs 518 109°) and the near-tie in kB. Both are driven by 662's ostial hook, which is short and partly along the LAO 30 view line. Rotating to AP or superior shows it; this supports the notes' recommendation of an ostial take-off rule before reporting energy-type metrics.
- Arc/chord matches the eye only in the sense that both look like "a C": the eye's impression of 518 as much more tortuous comes from bend count and sharpness, which arc/chord barely reflects.
- One view is not enough to judge 518: the out-of-plane part of its bending is visible only when rotating, which is why the linked cameras and the view buttons are part of the design.

### Gaps
- This is one observer's (the author's) reading of the rendered figures, not a blind or expert rating; criterion 7 in `tortuosity/CLAUDE.md` (Kendall τ against a blind expert ranking) remains the proper test.
- Only two vessels, so nothing here generalises.
