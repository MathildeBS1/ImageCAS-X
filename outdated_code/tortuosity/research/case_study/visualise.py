"""Side-by-side 3D view of the two case-study RCAs (scans 662 and 518) with their numbers.

Reads only the precomputed case-study outputs (no metric is recomputed):
  easy_metrics.json, easy_pointwise.npz          (easy.py)
  advanced_metrics.json, advanced_pointwise.npz  (advanced.py)
Writes, next to them:
  rca_tortuosity_comparison.html  (plotly.js from jsdelivr, data inline)
  rca_tortuosity_comparison.png   (matplotlib, 300 dpi)

Both views use one mm scale (each curve centred on its own bounding-box centre, same
half-range R) and one orthographic camera: LAO 30, cranial 0, view direction
d = (sin a, -cos a, 0) in LPS, the same convention as compute_simple.view_dir.
Line colour = |psi| = sqrt(k1^2 + k2^2) on the delivered curve (no extra smoothing), shared scale
clipped at KMAX. Bend markers (>= 45 deg) come from easy.py (1 mm chords).
Run: source env.sh && python tortuosity/research/case_study/visualise.py
"""
import json
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Line3DCollection  # noqa: E402

OUT = "/work3/s254124/imagecasx_results/tortuosity_research/case_study"
IDS = ["662", "518"]
KMAX = 0.20  # mm^-1 (radius 5 mm); 662's ostial kink (0.56) saturates
STOPS = [(0.0, "#6f86a0"), (0.35, "#d9b84a"), (0.7, "#e2702e"), (1.0, "#c7304f")]
CASE_COL = {"662": "#2f6fb0", "518": "#b0487a"}


def view_dir(a):
    a = np.radians(a)
    return [float(np.sin(a)), float(-np.cos(a)), 0.0]


def load():
    em = json.load(open(f"{OUT}/easy_metrics.json"))
    am = json.load(open(f"{OUT}/advanced_metrics.json"))
    ep = np.load(f"{OUT}/easy_pointwise.npz")
    ap = np.load(f"{OUT}/advanced_pointwise.npz")
    E = {c: {m["name"]: m for m in em[c]} for c in IDS}
    A = {c: {m["name"]: m for m in am[c]} for c in IDS}
    return E, A, ep, ap


def rows(c, E, A):
    """(group, label, value text, percentile or None, one-line meaning) for the numbers panel."""
    e, a = E[c], A[c]
    ta = lambda k: a[k]["value"]  # noqa: E731
    return [
        ("Easy", "Arc / chord", f"{e['DM']['value']:.2f}", e["DM"]["percentile"],
         "Path length over the straight ostium to end distance. Mostly the RCA's overall C."),
        ("Easy", "Arc / chord, LAO 30 shadow", f"{e['DM2_LAO30']['value']:.2f}", e["DM2_LAO30"]["percentile"],
         "The same ratio on the 2D projection an angiographer sees in LAO 30."),
        ("Easy", "κa at 5 mm chord", f"{e['kappa_a5']['value']:.3f} rad/mm", e["kappa_a5"]["percentile"],
         "Mean turning per mm between successive 5 mm chords. Local bendiness."),
        ("Easy", "Total turning", f"{e['total_turning_deg']['value']:.0f}°", e["total_turning_deg"]["percentile"],
         "All 5 mm chord turns added up. 180° is a half circle, 360° a full loop."),
        ("Easy", "Bends ≥45° / ≥90°", f"{e['n_bends_ge45']['value']:.0f} / {e['n_bends_ge90']['value']:.0f}",
         e["n_bends_ge45"]["percentile"],
         "Discrete bends on 1 mm chords, by cumulative angle. Percentile is for ≥45°."),
        ("Easy", "Largest bend", f"{e['max_bend_deg']['value']:.0f}° at {e['max_bend_at_mm']['value']:.1f} mm",
         e["max_bend_deg"]["percentile"], "One tight turn, blind to the rest of the vessel."),
        ("Advanced", "Bending energy kB", f"{ta('BCS kB'):.3f} /mm", a["BCS kB"]["percentile"],
         "RMS curvature, the square root of bending energy per mm. Driven by the sharpest turn."),
        ("Advanced", "Wiggle share", f"{ta('BCS f_wiggle'):.2f}", a["BCS f_wiggle"]["percentile"],
         "Share of bending energy in bends shorter than 20 mm rather than the course."),
        ("Advanced", "Out-of-plane share f_twist", f"{ta('BCS f_twist (W 5 mm)'):.2f}",
         a["BCS f_twist (W 5 mm)"]["percentile"],
         "Share of bending energy outside the local bending plane. Low means planar."),
        ("Advanced", "Average crossing number", f"{ta('average crossing number (ACN)'):.2f}", None,
         "How often the vessel overlaps itself, averaged over all projection directions."),
        ("Advanced", "Direction sphere coverage", f"{ta('tangent sphere coverage within 10 deg'):.3f}", None,
         "Tangent indicatrix spread: share of all 3D directions visited (within 10°)."),
        ("Advanced", "Tangent out-of-plane variance",
         f"{ta('tangent out-of-plane variance (smallest eigenvalue of <T T^T>)'):.3f}", None,
         "0 when every direction lies in one plane, 1/3 when spread evenly."),
        ("Advanced", "Turns ≥90° (barcode)",
         f"{ta('turn barcode: turns >= 90 deg'):.0f}, largest {ta('turn barcode: largest turn'):.0f}°", None,
         "Constant-sign turns along the local bending axis."),
        ("Advanced", "SRVF distance to the other RCA",
         f"{ta('SRVF elastic distance 662 vs 518 (rotation + warping)'):.2f} rad", None,
         "Elastic shape distance after best rotation and reparametrisation. Shared by both."),
    ]


def case_data(c, E, A, ep, ap):
    xyz0, s0 = ep[f"{c}_xyz"], ep[f"{c}_s"]
    ctr = (xyz0.min(0) + xyz0.max(0)) / 2
    xyz = ap[f"{c}_xyz"] - ctr
    s = ap[f"{c}_s"]
    psi = np.hypot(ap[f"{c}_k1"], ap[f"{c}_k2"])
    at = lambda q: (np.array([np.interp(q, s0, xyz0[:, i]) for i in range(3)]).T - ctr)  # noqa: E731
    b = ep[f"{c}_bends45"]
    turns = ap[f"{c}_turns"]
    rnd = lambda v, n=3: [None if not np.isfinite(x) else round(float(x), n) for x in np.ravel(v)]  # noqa: E731
    return {
        "id": c,
        "x": rnd(xyz[:, 0], 2), "y": rnd(xyz[:, 1], 2), "z": rnd(xyz[:, 2], 2),
        "s": rnd(s, 2), "psi": rnd(psi, 4),
        "s5": rnd(s0, 2), "turn5": rnd(ep[f"{c}_turn5"], 4),
        "ends": at(np.array([0.0, s0[-1]])).round(2).tolist(),
        "bends": [{"s": round(float(q), 1), "deg": round(float(d)), "p": p}
                  for q, d, p in zip(b, ep[f"{c}_bends45_deg"], at(b).round(2).tolist())],
        "turns45": [[float(t[0]), float(t[1]), round(float(t[2]))] for t in turns if t[2] >= 45],
        "L": round(float(s0[-1]), 1), "D": round(float(E[c]["D"]["value"]), 1),
        "rows": rows(c, E, A),
    }


def half_range(cases):
    ext = [np.abs(np.array([d["x"], d["y"], d["z"]], float)).max() for d in cases]
    return float(np.ceil(max(ext) * 1.08 / 5) * 5)


# ---------------------------------------------------------------- PNG (matplotlib)

def png(cases, R, path):
    cmap = LinearSegmentedColormap.from_list("k", STOPS)
    fig = plt.figure(figsize=(16, 10.5))
    gs = fig.add_gridspec(2, 4, width_ratios=[1.25, 1, 1, 1.25], height_ratios=[1.9, 1],
                          wspace=0.08, hspace=0.2, left=0.05, right=0.98, top=0.86, bottom=0.06)
    fig.suptitle("RCA tortuosity comparison: scan 662 (smooth) vs scan 518 (tortuous), LAO 30 orthographic, "
                 "same mm scale", fontsize=14, fontweight="bold", x=0.02, ha="left", y=0.985)
    fig.text(0.02, 0.935, f"Colour = |ψ| curvature (mm⁻¹), shared scale clipped at {KMAX} (radius 5 mm). "
             "Dots: ostium (O), distal end (E), bends ≥45° with angle. Dashed: chord. "
             "Grid 10 mm, superior up. Percentiles among 560 training RCAs in brackets.", fontsize=9.5, color="#44505c")
    d = view_dir(30)
    azim = np.degrees(np.arctan2(d[1], d[0]))
    for k, (c, col3d, colt) in enumerate(zip(cases, (0, 3), (1, 2))):
        ax = fig.add_subplot(gs[0, col3d], projection="3d")
        ax.set_proj_type("ortho")
        ax.view_init(elev=0, azim=azim)
        P = np.array([c["x"], c["y"], c["z"]], float).T
        seg = np.stack([P[:-1], P[1:]], 1)
        kk = np.clip(np.array(c["psi"], float), 0, KMAX) / KMAX
        lc = Line3DCollection(seg, colors=cmap((kk[:-1] + kk[1:]) / 2), linewidths=3.2)
        ax.add_collection(lc)
        if c["id"] == "662":
            t0, t1 = c["turns45"][0][:2]
            m = (np.array(c["s"]) >= t0) & (np.array(c["s"]) <= t1)
            ax.plot(*P[m].T, color="#c7304f", alpha=0.18, lw=14, solid_capstyle="round")
            ax.text(*P[m][-1] + [-4, 0, -2], "ostial kink", fontsize=8, color="#8a1c35", ha="right")
        (o, e) = np.array(c["ends"])
        ax.plot(*np.stack([o, e]).T, ls=(0, (4, 3)), color="#44505c", lw=1)
        ax.scatter(*o, s=46, color="#17212b", depthshade=False)
        ax.scatter(*e, s=46, facecolor="white", edgecolor="#17212b", depthshade=False)
        ax.text(*o + [0, 0, 2.5], "O", fontsize=10, fontweight="bold")
        ax.text(*e + [0, 0, 2.5], "E", fontsize=10, fontweight="bold")
        for b in c["bends"]:
            p = np.array(b["p"])
            ax.scatter(*p, s=26, color="#17212b", marker="D", depthshade=False)
            ax.text(*p + [0, 0, -5 if b["s"] < 5 else 2.5], f"{b['deg']}° @{b['s']:.0f}", fontsize=8)
        for set_, lab in ((ax.set_xlim, "x  L (mm)"), (ax.set_ylim, "y  P (mm)"), (ax.set_zlim, "z  S (mm)")):
            set_(-R, R)
        ax.set_box_aspect((1, 1, 1), zoom=1.3)
        ax.set_xlabel("x  L (mm)", fontsize=8)
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.tick_params(labelsize=7)
        ax.set_title(f"Scan {c['id']}   L {c['L']} mm, D {c['D']} mm", fontsize=12,
                     color=CASE_COL[c["id"]], fontweight="bold")
        # numbers panel
        axt = fig.add_subplot(gs[0, colt])
        axt.axis("off")
        y, grp = 0.98, None
        axt.text(0.0, 1.03, f"Scan {c['id']}", fontsize=12, fontweight="bold", color=CASE_COL[c["id"]],
                 transform=axt.transAxes)
        for g, lab, val, pct, _ in c["rows"]:
            if g != grp:
                y -= 0.02
                axt.text(0.0, y, g.upper(), fontsize=8.5,
                         color="#5b6b7a", fontweight="bold", transform=axt.transAxes)
                y -= 0.055
                grp = g
            axt.text(0.0, y, lab, fontsize=9, transform=axt.transAxes)
            axt.text(1.0, y, val + (f"  [{pct:.0f}]" if pct is not None else ""), fontsize=9, ha="right",
                     family="monospace", transform=axt.transAxes)
            y -= 0.058
    fig.colorbar(plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, KMAX)),
                 cax=fig.add_axes([0.44, 0.39, 0.12, 0.012]), orientation="horizontal",
                 label="|ψ| (mm⁻¹), clipped")
    # curvature vs arc length, one row per case, shared axes
    ymax = KMAX * 1.5
    for k, c in enumerate(cases):
        ax = fig.add_subplot(gs[1, 0:2] if k == 0 else gs[1, 2:4])
        for t0, t1, deg in c["turns45"]:
            ax.axvspan(t0, t1, color=CASE_COL[c["id"]], alpha=0.08)
            ax.text((t0 + t1) / 2, ymax * 0.93, f"turn {deg}°", ha="center", fontsize=7.5, color="#44505c")
        s, p = np.array(c["s"], float), np.array(c["psi"], float)
        ax.plot(s, np.minimum(p, ymax), color=CASE_COL[c["id"]], lw=1.6, label="|ψ|")
        ax.plot(np.array(c["s5"], float), np.array(c["turn5"], float), color=CASE_COL[c["id"]], lw=1,
                ls=":", label="turn5 (5 mm chords)")
        for b in c["bends"]:
            ax.axvline(b["s"], color="#17212b", lw=0.6, ls="--")
            ax.text(b["s"] + 0.8, ymax * 0.8, f"{b['deg']}°", fontsize=7.5)
        if c["id"] == "662":
            ax.text(7.5, ymax * 0.62, f"|ψ| peak {np.nanmax(p):.2f} (clipped)", fontsize=7.5, color="#8a1c35")
        ax.set_xlim(0, 110)
        ax.set_ylim(0, ymax)
        ax.set_xlabel("arc length from ostium (mm)", fontsize=9)
        ax.set_ylabel("curvature (mm⁻¹)", fontsize=9)
        ax.set_title(f"Scan {c['id']}: curvature along the vessel (shaded: barcode turns ≥45°, dashed: bends ≥45°)",
                     fontsize=9.5, loc="left", color=CASE_COL[c["id"]])
        ax.tick_params(labelsize=8)
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7.5, loc="upper right", bbox_to_anchor=(1, 0.75), frameon=False)
    fig.savefig(path, dpi=300)
    plt.close(fig)


# ---------------------------------------------------------------- HTML (plotly.js)

HTML = r"""<title>RCA tortuosity comparison</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{
  --bg:#f3f6f8; --surface:#ffffff; --ink:#17212b; --muted:#5b6b7a; --rule:#d7dee5; --track:#e6ebf0;
  --c662:#2f6fb0; --c518:#b0487a; --accent:#0f7b83; --grid:#e3e8ed;
  --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0e141a; --surface:#151d25; --ink:#e3e9ef; --muted:#93a3b3; --rule:#2a3643; --track:#24303b;
    --c662:#72a9e6; --c518:#e384b3; --accent:#4fbcc4; --grid:#243039; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#0e141a; --surface:#151d25; --ink:#e3e9ef; --muted:#93a3b3; --rule:#2a3643; --track:#24303b;
  --c662:#72a9e6; --c518:#e384b3; --accent:#4fbcc4; --grid:#243039; color-scheme:dark;
}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:15px;line-height:1.5}
.wrap{max-width:1500px;margin:0 auto;padding-inline:16px;padding-block:24px 40px;display:flex;flex-direction:column;gap:20px}
h1{font-size:1.7rem;font-weight:600;margin:0;text-wrap:balance;letter-spacing:-.01em}
h2{font-size:1.05rem;font-weight:600;margin:0;text-wrap:balance}
p{margin:0;max-width:72ch}
.lede{color:var(--muted)}
.bar{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:6px;overflow:hidden}
.seg button{font:500 13px var(--sans);background:var(--surface);color:var(--ink);border:0;padding:6px 14px;cursor:pointer}
.seg button+button{border-left:1px solid var(--rule)}
.seg button[aria-pressed="true"]{background:var(--accent);color:var(--surface)}
button:focus-visible,input:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
label.chk{font-size:13px;display:inline-flex;gap:6px;align-items:center;color:var(--muted)}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;font-size:12.5px;color:var(--muted)}
.ramp{width:140px;height:9px;border-radius:2px;background:linear-gradient(90deg,__RAMP__)}
.key{display:inline-flex;align-items:center;gap:6px}
.dot{width:9px;height:9px;border-radius:50%;background:var(--ink);display:inline-block}
.dot.open{background:var(--surface);border:1.5px solid var(--ink);width:7px;height:7px}
.dia{width:8px;height:8px;background:var(--ink);transform:rotate(45deg);display:inline-block}
.dash{width:22px;border-top:1.5px dashed var(--muted);display:inline-block}
.grid{display:grid;gap:16px;grid-template-columns:minmax(0,1fr);grid-template-areas:"p1" "n1" "p2" "n2"}
@media (min-width:760px){.grid{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-areas:"p1 p2" "n1 n2"}}
@media (min-width:1280px){.grid{grid-template-columns:minmax(0,1.35fr) minmax(0,1fr) minmax(0,1fr) minmax(0,1.35fr);grid-template-areas:"p1 n1 n2 p2"}}
.panel{background:var(--surface);border:1px solid var(--rule);border-radius:8px;display:flex;flex-direction:column;min-width:0}
.panel header{padding:12px 14px 0;display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
.panel header span{font:12.5px var(--mono);color:var(--muted)}
.c662 h2{color:var(--c662)} .c518 h2{color:var(--c518)}
.plot3d{height:470px;width:100%}
@media (max-width:759px){.plot3d{height:380px}}
.nums{padding:12px 14px 14px;display:flex;flex-direction:column;gap:2px}
.grp{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding-top:10px;border-bottom:1px solid var(--rule);padding-bottom:4px;margin-bottom:2px}
.row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;padding:5px 0;border-bottom:1px solid var(--track)}
.row .lab{font-size:13.5px;font-weight:500}
.row .val{font:500 13.5px var(--mono);font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
.row .mean{grid-column:1/-1;font-size:12px;color:var(--muted);line-height:1.35}
.pct{grid-column:1/-1;display:flex;align-items:center;gap:8px;font:11.5px var(--mono);color:var(--muted)}
.pct .tr{position:relative;flex:1;height:4px;background:var(--track);border-radius:2px}
.pct .tr i{position:absolute;top:-3px;width:10px;height:10px;border-radius:50%;margin-left:-5px}
.c662 .pct i{background:var(--c662)} .c518 .pct i{background:var(--c518)}
.wide{background:var(--surface);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.plot2d{height:420px;width:100%}
.notes{display:grid;gap:16px;grid-template-columns:minmax(0,1fr)}
@media (min-width:900px){.notes{grid-template-columns:repeat(2,minmax(0,1fr))}}
.notes ul{margin:6px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:6px;max-width:75ch}
.foot{font-size:12.5px;color:var(--muted)}
code{font-family:var(--mono);font-size:.92em}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"></script>

<div class="wrap">
  <div style="display:flex;flex-direction:column;gap:8px">
    <h1>RCA tortuosity comparison</h1>
    <p class="lede">Two right coronary arteries from ImageCAS-X training scans, matched in length (109 and 104 mm).
    Scan 662 sits at the 10th percentile of local bendiness (κa at 5 mm), scan 518 at the 88th.
    Both views share one millimetre scale and one orthographic camera, so the shapes can be compared directly.
    Drag either view; the other follows.</p>
  </div>

  <div class="bar">
    <div class="seg" role="group" aria-label="Viewing angle">
      <button id="v-lao" aria-pressed="true">LAO 30</button>
      <button id="v-ap" aria-pressed="false">AP</button>
      <button id="v-rao" aria-pressed="false">RAO 30</button>
    </div>
    <label class="chk"><input type="checkbox" id="link" checked> Link cameras</label>
    <div class="legend">
      <span class="key">|ψ| curvature <span class="ramp"></span> 0 to __KMAX__ mm⁻¹ (clipped)</span>
      <span class="key"><span class="dot"></span> ostium</span>
      <span class="key"><span class="dot open"></span> distal end</span>
      <span class="key"><span class="dia"></span> bend ≥45°</span>
      <span class="key"><span class="dash"></span> chord</span>
    </div>
  </div>

  <div class="grid">
    <section class="panel c662" style="grid-area:p1"><header><h2>Scan 662</h2><span id="h662"></span></header><div id="p662" class="plot3d"></div></section>
    <section class="panel c662" style="grid-area:n1"><header><h2>Scan 662 numbers</h2><span>[percentile of 560 RCAs]</span></header><div id="n662" class="nums"></div></section>
    <section class="panel c518" style="grid-area:n2"><header><h2>Scan 518 numbers</h2><span>[percentile of 560 RCAs]</span></header><div id="n518" class="nums"></div></section>
    <section class="panel c518" style="grid-area:p2"><header><h2>Scan 518</h2><span id="h518"></span></header><div id="p518" class="plot3d"></div></section>
  </div>

  <section class="wide">
    <h2>Curvature along the vessel</h2>
    <p class="lede" style="font-size:13px">Solid: |ψ| on the delivered centerline (the 3D colour). Dotted: turn5 on 5 mm chords, undefined in the first and last 5 mm.
    Shaded: barcode turns ≥45°. Dashed lines: bends ≥45° marked in 3D. Hover a trace to place a cursor on the matching 3D curve.</p>
    <div id="k2d" class="plot2d"></div>
  </section>

  <section class="notes">
    <div class="wide">
      <h2>Where the eye agrees with the numbers</h2>
      <ul>
        <li>518 looks busier along its whole length: the proximal S within 20 mm, a kink near 34 mm and a double sweep at 66 to 77 mm near the crux. κa (0.068 vs 0.035 rad/mm), total turning (407° vs 218°) and bends ≥45° (5 vs 1) all say so.</li>
        <li>662 reads as one smooth C with a hook at the ostium. Its only bend ≥45° is that hook, and the curvature trace is flat after 6 mm except a gentle sweep at 60 to 80 mm.</li>
        <li>Rotating the views shows 518 leaving its plane (f_twist 0.46 vs 0.15, 95th vs 1st percentile). 662 stays nearly flat in every rotation.</li>
      </ul>
    </div>
    <div class="wide">
      <h2>Where the eye and the numbers part</h2>
      <ul>
        <li>Arc/chord differs by only 16 % (2.00 vs 1.73) although the shapes look very different: both are dominated by the C around the AV groove.</li>
        <li>In LAO 30 the 2D arc/chord gap shrinks to 5 %, and in RAO 30 the order flips. One angiographic view can hide 518's out-of-plane bends.</li>
        <li>Largest bend and bending energy kB are pulled up by 662's short ostial hook (127°, |ψ| peak 0.56 mm⁻¹), so kB ranks the two almost level (66th vs 79th percentile).</li>
      </ul>
    </div>
  </section>

  <p class="foot">Data: <code>easy_metrics.json</code>, <code>easy_pointwise.npz</code> and
  <code>advanced_metrics.json</code>, <code>advanced_pointwise.npz</code> from the case-study scripts; both on the delivered centerline resampled at 0.25 mm, no extra smoothing.
  Coordinates are LPS mm, each curve centred on its bounding box. View direction for LAO a: (sin a, −cos a, 0), up = superior.
  Percentiles are mid-rank among all 560 training RCAs.</p>
</div>

<script>
const DATA = __DATA__;
const R = DATA.R, KMAX = DATA.kmax, STOPS = DATA.stops;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const views = {lao: 30, ap: 0, rao: -30};
let cur = 'lao', linked = true, syncing = false;
function cam(a){ const r = a*Math.PI/180, k = 2.0;
  return {eye:{x:k*Math.sin(r), y:-k*Math.cos(r), z:0}, up:{x:0,y:0,z:1}, center:{x:0,y:0,z:0}, projection:{type:'orthographic'}}; }

function nums(c){
  const el = document.getElementById('n'+c.id); let g = null, h = '';
  for (const [grp, lab, val, pct, mean] of c.rows){
    if (grp !== g){ h += `<div class="grp">${grp}</div>`; g = grp; }
    h += `<div class="row" title="${mean}"><span class="lab">${lab}</span><span class="val">${val}${pct!=null?` <span style="color:var(--muted)">[${Math.round(pct)}]</span>`:''}</span>`;
    if (pct != null) h += `<div class="pct"><span class="tr"><i style="left:${pct}%"></i></span><span>${Math.round(pct)}th</span></div>`;
    h += `<span class="mean">${mean}</span></div>`;
  }
  el.innerHTML = h;
  document.getElementById('h'+c.id).textContent = `L ${c.L} mm · D ${c.D} mm`;
}

function axis(t){ return {title:{text:t, font:{size:11}}, range:[-R,R], dtick:20, gridcolor:css('--grid'), zerolinecolor:css('--rule'),
  color:css('--muted'), showbackground:false, showspikes:false}; }

function traces3d(c){
  const cs = STOPS.map(([v,col]) => [v,col]);
  const T = [];
  if (c.id === '662'){ const [t0,t1] = c.turns45[0]; const idx = c.s.map((v,i)=>v>=t0&&v<=t1?i:-1).filter(i=>i>=0);
    T.push({type:'scatter3d', mode:'lines', x:idx.map(i=>c.x[i]), y:idx.map(i=>c.y[i]), z:idx.map(i=>c.z[i]),
      line:{color:'#c7304f', width:22}, opacity:0.22, hoverinfo:'skip', name:'ostial kink'}); }
  T.push({type:'scatter3d', mode:'lines', x:c.x, y:c.y, z:c.z,
    line:{color:c.psi.map(v=>Math.min(v,KMAX)), colorscale:cs, cmin:0, cmax:KMAX, width:9},
    customdata:c.s.map((s,i)=>[s,c.psi[i]]), hovertemplate:'s %{customdata[0]:.1f} mm<br>|ψ| %{customdata[1]:.3f} mm⁻¹<extra></extra>', name:'centerline'});
  const [o,e] = c.ends;
  T.push({type:'scatter3d', mode:'lines', x:[o[0],e[0]], y:[o[1],e[1]], z:[o[2],e[2]], line:{color:css('--muted'), width:2, dash:'dash'},
    hovertemplate:`chord D ${c.D} mm<extra></extra>`, name:'chord'});
  T.push({type:'scatter3d', mode:'markers+text', x:[o[0],e[0]], y:[o[1],e[1]], z:[o[2],e[2]], text:['O','E'], textposition:'top center',
    textfont:{color:css('--ink'), size:13, family:'IBM Plex Sans'},
    marker:{size:6, color:[css('--ink'), css('--surface')], line:{color:css('--ink'), width:2}}, hovertemplate:['ostium','distal end'].map(t=>t+'<extra></extra>'), name:'ends'});
  T.push({type:'scatter3d', mode:'markers+text', x:c.bends.map(b=>b.p[0]), y:c.bends.map(b=>b.p[1]), z:c.bends.map(b=>b.p[2]),
    text:c.bends.map(b=>`${b.deg}°`), textposition:'middle right', textfont:{color:css('--ink'), size:12, family:'IBM Plex Mono'},
    marker:{size:5, symbol:'diamond', color:css('--ink')}, customdata:c.bends.map(b=>[b.s,b.deg]),
    hovertemplate:'bend %{customdata[1]}° at s %{customdata[0]} mm<extra></extra>', name:'bends'});
  T.push({type:'scatter3d', mode:'markers', x:[null], y:[null], z:[null], marker:{size:9, color:'rgba(0,0,0,0)', line:{color:css('--accent'), width:3}}, hoverinfo:'skip', name:'cursor'});
  return T;
}
function layout3d(){ return {margin:{l:0,r:0,t:0,b:0}, paper_bgcolor:'rgba(0,0,0,0)', showlegend:false, uirevision:'k',
  font:{family:'IBM Plex Sans', color:css('--muted')},
  scene:{xaxis:axis('x  L (mm)'), yaxis:axis('y  P (mm)'), zaxis:axis('z  S (mm)'), aspectmode:'cube', camera:cam(views[cur]), dragmode:'orbit'}}; }

function layout2d(){
  const ymax = KMAX*1.5, shapes = [], ann = [];
  DATA.cases.forEach((c,k) => { const ya = k ? 'y2' : 'y', xa = k ? 'x2' : 'x', col = css('--c'+c.id);
    for (const [t0,t1,deg] of c.turns45){ shapes.push({type:'rect', xref:xa, yref:ya, x0:t0, x1:t1, y0:0, y1:ymax, fillcolor:col, opacity:0.10, line:{width:0}});
      ann.push({xref:xa, yref:ya, x:(t0+t1)/2, y:ymax*0.95, text:`turn ${deg}°`, showarrow:false, font:{size:10.5, color:css('--muted')}}); }
    for (const b of c.bends){ shapes.push({type:'line', xref:xa, yref:ya, x0:b.s, x1:b.s, y0:0, y1:ymax*0.84, line:{color:css('--ink'), width:1, dash:'dash'}});
      ann.push({xref:xa, yref:ya, x:b.s, y:ymax*0.84, text:`${b.deg}°`, showarrow:false, xanchor:'left', yanchor:'bottom', font:{size:10.5, color:css('--ink'), family:'IBM Plex Mono'}}); }
    ann.push({xref:'paper', yref:ya+' domain', x:0, y:1.02, text:`<b>Scan ${c.id}</b>`, showarrow:false, xanchor:'left', yanchor:'bottom', font:{size:12.5, color:col}});
  });
  const ax = t => ({range:[0,110], gridcolor:css('--grid'), zeroline:false, color:css('--muted'), title:t?{text:t, font:{size:12}}:undefined});
  const ay = {range:[0,ymax], gridcolor:css('--grid'), zeroline:false, color:css('--muted'), title:{text:'mm⁻¹', font:{size:12}}};
  return {grid:{rows:2, columns:1, pattern:'independent', roworder:'top to bottom'}, margin:{l:52,r:12,t:22,b:44},
    paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)', font:{family:'IBM Plex Sans', color:css('--muted'), size:11.5},
    xaxis:ax(''), xaxis2:{...ax('arc length from ostium (mm)'), matches:'x'}, yaxis:ay, yaxis2:{...ay, matches:'y'},
    shapes, annotations:ann, showlegend:false, hovermode:'x unified', uirevision:'k'};
}
function traces2d(){
  const T = [];
  DATA.cases.forEach((c,k) => { const col = css('--c'+c.id), xa = k?'x2':'x', ya = k?'y2':'y';
    T.push({x:c.s, y:c.psi.map(v=>Math.min(v,KMAX*1.5)), customdata:c.psi, xaxis:xa, yaxis:ya, mode:'lines', line:{color:col, width:2},
      name:`${c.id} |ψ|`, hovertemplate:'|ψ| %{customdata:.3f}<extra></extra>'});
    T.push({x:c.s5, y:c.turn5, xaxis:xa, yaxis:ya, mode:'lines', line:{color:col, width:1.3, dash:'dot'}, name:`${c.id} turn5`,
      hovertemplate:'turn5 %{y:.3f}<extra></extra>', connectgaps:false}); });
  return T;
}

const ids = DATA.cases.map(c=>c.id);
function draw(){
  DATA.cases.forEach(c => Plotly.react('p'+c.id, traces3d(c), layout3d(), {displaylogo:false, responsive:true, modeBarButtons:[['resetCameraLastSave3d','toImage']]}));
  Plotly.react('k2d', traces2d(), layout2d(), {displaylogo:false, responsive:true, displayModeBar:false});
}
function setView(v){ cur = v;
  for (const k of Object.keys(views)) document.getElementById('v-'+k).setAttribute('aria-pressed', k===v);
  syncing = true; Promise.all(ids.map(id => Plotly.relayout('p'+id, {'scene.camera':cam(views[v])}))).then(()=>{syncing=false;}); }

DATA.cases.forEach(nums);
draw();
ids.forEach(id => {
  const src = document.getElementById('p'+id), other = 'p'+ids.find(x=>x!==id);
  const follow = ev => { if (!linked || syncing || !ev || !ev['scene.camera']) return;
    syncing = true; Plotly.relayout(other, {'scene.camera':ev['scene.camera']}).then(()=>{syncing=false;}); };
  src.on('plotly_relayouting', follow); src.on('plotly_relayout', follow);
});
document.getElementById('k2d').on('plotly_hover', ev => {
  const pt = ev.points[0], c = DATA.cases[pt.curveNumber < 2 ? 0 : 1];
  let i = 0, best = 1e9; c.s.forEach((s,j) => { const d = Math.abs(s-pt.x); if (d < best){ best = d; i = j; } });
  const div = 'p'+c.id, n = document.getElementById(div).data.length - 1;
  Plotly.restyle(div, {x:[[c.x[i]]], y:[[c.y[i]]], z:[[c.z[i]]]}, [n]);
});
for (const k of Object.keys(views)) document.getElementById('v-'+k).addEventListener('click', () => setView(k));
document.getElementById('link').addEventListener('change', e => { linked = e.target.checked; });
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
new MutationObserver(draw).observe(document.documentElement, {attributes:true, attributeFilter:['data-theme']});
</script>
"""


def html(cases, R, path):
    data = {"R": R, "kmax": KMAX, "stops": STOPS, "cases": cases}
    ramp = ",".join(f"{c} {int(v * 100)}%" for v, c in STOPS)
    page = (HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
            .replace("__RAMP__", ramp).replace("__KMAX__", f"{KMAX:.2f}"))
    open(path, "w").write(page)


def main():
    E, A, ep, ap = load()
    cases = [case_data(c, E, A, ep, ap) for c in IDS]
    R = half_range(cases)
    print(f"shared half-range R = {R} mm")
    png(cases, R, f"{OUT}/rca_tortuosity_comparison.png")
    html(cases, R, f"{OUT}/rca_tortuosity_comparison.html")
    print("wrote", f"{OUT}/rca_tortuosity_comparison.png", f"{OUT}/rca_tortuosity_comparison.html")


if __name__ == "__main__":
    main()
