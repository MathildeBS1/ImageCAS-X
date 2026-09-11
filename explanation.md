Centerlines are the 1D reductions of the 3D coronorary arteries. Here 13 segments get centerlines. Centerlines keep where the vessel goes and roughly how big it is at each point, and discard the precise 3D shape of the vessel wall, in exchange for making downstream analysis (tapering, per-branch stats, stenosis severity along length) tractable to compute and easy to aggregat

Ostium: is the opening or origin point of a blood vessel. So functionally: ostium = the vessel's starting point at the aorta, and it's the reference point everything else (direction, arc-length distance, "how far downstream is this stenosis") gets measured from

Ground truth mask: The coronorary arteries was traced by human experts (radiologist), in ImageCas-X it was re-annotated with new labels. we have the 14 segments LM and so on, these ground truth masks are saved in 
segmentations/<scan_id>.coronary.nii.gz

Resolution: 0.5 mm — each voxel represents a 0.5 millimetre chunk of real-world space along that axis. Smaller number = finer resolution, more detail. Isotropic — the same spacing in all three directions (x, y, and z). So each voxel is a perfect little cube, 0.5 mm × 0.5 mm × 0.5 mm

resample: redrawing the image at a different resolution. Why it's needed here, tying back to what we covered earlier: different CT scans come with different native voxel spacing — recall the ImageCAS numbers, in-plane resolution 0.29–0.43 mm² and slice spacing 0.25–0.45 mm, varying scan to scan. The Resample class uses SimpleITK to rebuild each scan onto a uniform 0.5 mm grid: it computes how many voxels are needed per axis to preserve the physical size at the new spacing, then resamples the CT volume with linear interpolation (since intensities are continuous) and the mask with nearest-neighbour interpolation (since labels are discrete categories that can't be blended). The mask is resampled using the already-resampled volume as its reference image, guaranteeing the two stay perfectly aligned voxel-for-voxel rather than risking a mismatch from two independently computed resamples.

Use of inference: Only after all four are trained does the hard-vs-soft distinction come in — and it's purely about what happens to those four already-trained checkpoints at prediction time:

Hard vote: load all four trained checkpoints into one staged model, run one inference.py call, vote inside the forward pass.
Soft vote: run inference.py four separate times (once per already-trained checkpoint), save the raw probabilities, then average them afterward in ensemble_vote.py