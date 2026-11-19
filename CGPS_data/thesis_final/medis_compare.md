```markdown
# Tracer against Medis: agreement of the geometric features (medis_compare.py)

Baseline. Differences are tracer - Medis. Limits of agreement = bias +- 1.96 SD; 95% intervals from 2000 bootstrap samples of participants. Alignment cut 2 mm, shared stretch at least 10 mm. Counts 1-4 shown as <5; statistics only from 5 pairs.

## Flow

| step | participants |
|---|---|
| Medis trees | 600 |
| with a tracer pair | 600 |
| both trees divided | 599 |
| tree not divided | <5 |

| artery | missing in Medis | missing in Medis and tracer | missing in tracer | offset > 2 mm | ok | shared stretch < 10 mm |
|---|---|---|---|---|---|---|
| LAD | 35 | 0 | 7 | 17 | 532 | 8 |
| LCx | 32 | <5 | 21 | 35 | 493 | 17 |
| RCA | 8 | <5 | <5 | 5 | 527 | 56 |

Median tracer-to-Medis distance over the shared stretch (mm), pairs kept: LAD 0.4, LCx 0.4, RCA 0.39

## Curvature (average over the shared stretch)

| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | unit |
|---|---|---|---|---|---|---|
| LAD | 532 | 0.00585 (0.0051 to 0.00657) | 0.00878 | -0.0113 (-0.0135 to -0.00912) | 0.0231 (0.0214 to 0.0247) | 1/mm |
| LCx | 493 | 0.00389 (0.00275 to 0.00504) | 0.013 | -0.0216 (-0.0264 to -0.0168) | 0.0294 (0.0248 to 0.0343) | 1/mm |
| RCA | 527 | 0.000609 (-0.000356 to 0.00149) | 0.011 | -0.0209 (-0.0279 to -0.0148) | 0.0221 (0.0171 to 0.0281) | 1/mm |
| all arteries | 1552 | 0.00345 (0.00288 to 0.00401) | 0.0112 | -0.0185 (-0.0218 to -0.0157) | 0.0254 (0.0229 to 0.0283) | 1/mm |

## Bifurcation angle

| | pairs | bias (95% CI) | SD of differences | lower limit (95% CI) | upper limit (95% CI) | unit |
|---|---|---|---|---|---|---|
| LAD-LCx angle | 461 | 3.91 (2.03 to 5.93) | 21.2 | -37.6 (-43.8 to -31) | 45.4 (36.5 to 53.8) | degrees |

Angle missing: tracer 105, Medis 54.

```