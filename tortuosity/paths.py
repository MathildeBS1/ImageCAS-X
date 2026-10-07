"""Every file the tortuosity code reads or writes. Edit the three roots after moving machines.

{case}, {side}, {split}, {vessel} and {name} are filled in by the code, so keep them.
"""

DATA = "/work3/s254124/ImageCAS-X_dataset"    # the ImageCAS-X dataset, read-only
RESULTS = "/work3/s254124/imagecasx_results"  # everything this code writes
FIGURES = "figures"                           # relative, so run from the repository root

# inputs
CENTERLINE = DATA + "/centerlines/{case}.coronary_{side}_centerline.vtk"  # side: left, right
FILELIST = DATA + "/filelist/{split}.txt"                                 # split: train, val, test

# Scan-level covariates, .xlsx or .csv, one row per scan, keyed by a column named "Scan ID".
# Add a file per source; they are merged left to right, so the first one defines the cohort.
DESCRIPTORS = [DATA + "/Descriptors.xlsx"]

# outputs
SCORES = RESULTS + "/tortuosity_scores"      # score.py: <split>_vessels.csv
DECILES = RESULTS + "/tortuosity_deciles"    # deciles.py: RCA here, LAD and LCX in subfolders
REGRESSION = RESULTS + "/tortuosity_{name}"  # regression_model.py: name is outcome[_covariates]
TRANSFORMER = RESULTS + "/tortuosity_transformer_{name}"  # transformer_model.py: name is outcome[_chord<l>][_covariates]

# figures, each written as .pdf and .png
DECILE_FIG = FIGURES + "/{vessel}_tortuosity_deciles"
EXAMPLE_FIG = FIGURES + "/{vessel}_tortuosity_examples"
TURNING_ANGLE_FIG = FIGURES + "/turning_angle_3d"
