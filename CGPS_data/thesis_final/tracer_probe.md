# Tracer file format (tracer_probe.py)

```
7188 BL files, 6120 FU files in /data/kimbr/centerlines_for_mathilde
BL file kinds: coronary_left_centerline.vtk, coronary_left_centerline_ostium_pruned.vtk, coronary_right_centerline.vtk, coronary_right_centerline_ostium_pruned.vtk
1797 BL participants with a tracer file

BL trees, Medis against the tracer (participants):
  Medis trees                          600
  tracer, any file                     1797
  tracer, pruned left and right        1797
  tracer, pruned left only / right only 0 / 0
  in both Medis and tracer             600
    with pruned left and right         600
  Medis only (no tracer file)          0
  tracer only (no Medis tree)          1197
  in both, with a BL NIfTI             600

=== participant 1
  coronary_left_centerline.vtk  (36 kB)
    first line: # vtk DataFile Version 5.1
    1117 points; bounds [    14.9,     68.5] [   -99.0,      3.5] [  1755.9,   1854.8]
    cells: LINES 18 (lengths 2-242)
    consecutive point spacing: median 0.473, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1117,), 7 distinct; first: 1, 2, 3, 4, 5, 6, 14
    cell_data:
    branch_id: dtype int64, shape (18,), 18 distinct; first: 3, 4, 5, 6, 7, 8, 9, 10
    parent: dtype int64, shape (18,), 9 distinct; first: -1, 3, 4, 5, 9, 10, 11, 12
    root_seed: dtype int64, shape (18,), 1 distinct; first: 0
    segment_label: dtype int64, shape (18,), 8 distinct; first: 1, 2, 3, 4, 5, 6, 7, 14
    termination: dtype object, shape (18,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (18,), 7 distinct; first: 1, 2, 3, 4, 5, 6, 14
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -55.852, -30.384, -9.07, 13.157, 1839.799, 1855.092
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_left_centerline_ostium_pruned.vtk  (34 kB)
    first line: # vtk DataFile Version 5.1
    1067 points; bounds [    14.9,     68.5] [   -99.0,      3.5] [  1755.9,   1854.8]
    cells: LINES 17 (lengths 2-242)
    consecutive point spacing: median 0.473, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1067,), 7 distinct; first: 1, 2, 3, 4, 5, 6, 14
    cell_data:
    branch_id: dtype int64, shape (17,), 17 distinct; first: 3, 4, 5, 6, 7, 8, 9, 10
    parent: dtype int64, shape (17,), 9 distinct; first: -1, 3, 4, 5, 9, 10, 11, 12
    root_seed: dtype int64, shape (17,), 1 distinct; first: 0
    segment_label: dtype int64, shape (17,), 8 distinct; first: 1, 2, 3, 4, 5, 6, 7, 14
    termination: dtype object, shape (17,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (17,), 7 distinct; first: 1, 2, 3, 4, 5, 6, 14
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -55.852, -30.384, -9.07, 13.157, 1839.799, 1855.092
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline.vtk  (14 kB)
    first line: # vtk DataFile Version 5.1
    417 points; bounds [   -43.0,     52.4] [   -96.1,    -25.7] [  1753.4,   1841.8]
    cells: LINES 4 (lengths 6-264)
    consecutive point spacing: median 0.477, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (417,), 4 distinct; first: 2, 9, 10, 11
    cell_data:
    branch_id: dtype int64, shape (4,), 4 distinct; first: 0, 1, 2, 21
    parent: dtype int64, shape (4,), 2 distinct; first: -1, 0
    root_seed: dtype int64, shape (4,), 1 distinct; first: 1
    segment_label: dtype int64, shape (4,), 4 distinct; first: 2, 9, 10, 11
    termination: dtype object, shape (4,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (4,), 4 distinct; first: 2, 9, 10, 11
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -55.852, -30.384, -9.07, 13.157, 1839.799, 1855.092
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline_ostium_pruned.vtk  (14 kB)
    first line: # vtk DataFile Version 5.1
    411 points; bounds [   -43.0,      8.9] [   -64.7,    -25.7] [  1767.0,   1841.8]
    cells: LINES 3 (lengths 59-264)
    consecutive point spacing: median 0.477, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (411,), 3 distinct; first: 9, 10, 11
    cell_data:
    branch_id: dtype int64, shape (3,), 3 distinct; first: 0, 1, 2
    parent: dtype int64, shape (3,), 2 distinct; first: -1, 0
    root_seed: dtype int64, shape (3,), 1 distinct; first: 1
    segment_label: dtype int64, shape (3,), 3 distinct; first: 9, 10, 11
    termination: dtype object, shape (3,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (3,), 3 distinct; first: 9, 10, 11
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -55.852, -30.384, -9.07, 13.157, 1839.799, 1855.092
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  Medis tree: 1603 points; bounds [   -42.6,     70.4] [   -98.9,      3.6] [  1754.4,   1854.8]
  volume: shape (512, 512, 560), zooms (np.float32(0.429), np.float32(0.429), np.float32(0.25)), axcodes LAS
    voxel bounds [     0.0,    511.0] [     0.0,    511.0] [     0.0,    559.0]
    RAS mm bounds [  -121.3,     97.9] [  -109.4,    109.8] [  1732.5,   1872.2]
    LPS mm bounds [   -97.9,    121.3] [  -109.8,    109.4] [  1732.5,   1872.2]

=== participant 2
  coronary_left_centerline.vtk  (43 kB)
    first line: # vtk DataFile Version 5.1
    1375 points; bounds [    16.5,     96.8] [   -42.9,     58.4] [  1791.8,   1885.0]
    cells: LINES 20 (lengths 2-304)
    consecutive point spacing: median 0.475, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1375,), 7 distinct; first: 1, 2, 3, 4, 6, 7, 8
    cell_data:
    branch_id: dtype int64, shape (20,), 20 distinct; first: 3, 4, 5, 6, 7, 8, 9, 10
    parent: dtype int64, shape (20,), 10 distinct; first: -1, 3, 4, 5, 6, 9, 10, 11
    root_seed: dtype int64, shape (20,), 1 distinct; first: 0
    segment_label: dtype int64, shape (20,), 6 distinct; first: 1, 2, 3, 4, 6, 7
    termination: dtype object, shape (20,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (20,), 7 distinct; first: 1, 2, 3, 4, 6, 7, 8
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -9.916, 1.707, 14.831, 22.661, 1855.545, 1880.6
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_left_centerline_ostium_pruned.vtk  (43 kB)
    first line: # vtk DataFile Version 5.1
    1365 points; bounds [    16.5,     96.8] [   -42.9,     58.4] [  1791.8,   1885.0]
    cells: LINES 19 (lengths 2-304)
    consecutive point spacing: median 0.476, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1365,), 7 distinct; first: 1, 2, 3, 4, 6, 7, 8
    cell_data:
    branch_id: dtype int64, shape (19,), 19 distinct; first: 3, 4, 5, 6, 7, 8, 9, 10
    parent: dtype int64, shape (19,), 10 distinct; first: -1, 3, 4, 5, 6, 9, 10, 11
    root_seed: dtype int64, shape (19,), 1 distinct; first: 0
    segment_label: dtype int64, shape (19,), 6 distinct; first: 1, 2, 3, 4, 6, 7
    termination: dtype object, shape (19,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (19,), 7 distinct; first: 1, 2, 3, 4, 6, 7, 8
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -9.916, 1.707, 14.831, 22.661, 1855.545, 1880.6
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline.vtk  (19 kB)
    first line: # vtk DataFile Version 5.1
    588 points; bounds [   -34.5,     51.1] [   -15.4,     37.8] [  1793.2,   1854.0]
    cells: LINES 4 (lengths 38-256)
    consecutive point spacing: median 0.482, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (588,), 3 distinct; first: 9, 10, 11
    cell_data:
    branch_id: dtype int64, shape (4,), 4 distinct; first: 0, 1, 2, 22
    parent: dtype int64, shape (4,), 2 distinct; first: -1, 0
    root_seed: dtype int64, shape (4,), 1 distinct; first: 1
    segment_label: dtype int64, shape (4,), 3 distinct; first: 9, 10, 11
    termination: dtype object, shape (4,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (4,), 3 distinct; first: 9, 10, 11
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -9.916, 1.707, 14.831, 22.661, 1855.545, 1880.6
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline_ostium_pruned.vtk  (18 kB)
    first line: # vtk DataFile Version 5.1
    550 points; bounds [   -34.5,     50.3] [   -15.4,     37.8] [  1793.2,   1854.0]
    cells: LINES 3 (lengths 145-256)
    consecutive point spacing: median 0.482, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (550,), 3 distinct; first: 9, 10, 11
    cell_data:
    branch_id: dtype int64, shape (3,), 3 distinct; first: 0, 1, 2
    parent: dtype int64, shape (3,), 2 distinct; first: -1, 0
    root_seed: dtype int64, shape (3,), 1 distinct; first: 1
    segment_label: dtype int64, shape (3,), 3 distinct; first: 9, 10, 11
    termination: dtype object, shape (3,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (3,), 3 distinct; first: 9, 10, 11
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -9.916, 1.707, 14.831, 22.661, 1855.545, 1880.6
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  Medis tree: 2292 points; bounds [   -34.1,     96.5] [   -42.3,     58.0] [  1789.9,   1886.8]
  volume: shape (512, 512, 512), zooms (np.float32(0.429), np.float32(0.429), np.float32(0.25)), axcodes LAS
    voxel bounds [     0.0,    511.0] [     0.0,    511.0] [     0.0,    511.0]
    RAS mm bounds [  -116.9,    102.3] [  -109.4,    109.8] [  1762.0,   1889.8]
    LPS mm bounds [  -102.3,    116.9] [  -109.8,    109.4] [  1762.0,   1889.8]

=== participant 3
  coronary_left_centerline.vtk  (50 kB)
    first line: # vtk DataFile Version 5.1
    1561 points; bounds [    26.5,    103.2] [   -81.8,     12.5] [  1877.2,   1962.8]
    cells: LINES 19 (lengths 2-245)
    consecutive point spacing: median 0.472, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1561,), 9 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    cell_data:
    branch_id: dtype int64, shape (19,), 19 distinct; first: 1, 2, 3, 4, 5, 6, 7, 8
    parent: dtype int64, shape (19,), 10 distinct; first: -1, 1, 2, 3, 5, 6, 8, 10
    root_seed: dtype int64, shape (19,), 1 distinct; first: 0
    segment_label: dtype int64, shape (19,), 8 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    termination: dtype object, shape (19,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (19,), 9 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -45.505, -22.244, 14.716, 26.052, 1941.002, 1960.513
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_left_centerline_ostium_pruned.vtk  (50 kB)
    first line: # vtk DataFile Version 5.1
    1561 points; bounds [    26.5,    103.2] [   -81.8,     12.5] [  1877.2,   1962.8]
    cells: LINES 19 (lengths 2-245)
    consecutive point spacing: median 0.472, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (1561,), 9 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    cell_data:
    branch_id: dtype int64, shape (19,), 19 distinct; first: 1, 2, 3, 4, 5, 6, 7, 8
    parent: dtype int64, shape (19,), 10 distinct; first: -1, 1, 2, 3, 5, 6, 8, 10
    root_seed: dtype int64, shape (19,), 1 distinct; first: 0
    segment_label: dtype int64, shape (19,), 8 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    termination: dtype object, shape (19,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (19,), 9 distinct; first: 1, 2, 3, 4, 5, 6, 7, 13
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -45.505, -22.244, 14.716, 26.052, 1941.002, 1960.513
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline.vtk  (12 kB)
    first line: # vtk DataFile Version 5.1
    352 points; bounds [    -9.2,     85.1] [   -75.4,    -22.2] [  1868.5,   1940.0]
    cells: LINES 2 (lengths 22-330)
    consecutive point spacing: median 0.481, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (352,), 2 distinct; first: 2, 9
    cell_data:
    branch_id: dtype int64, shape (2,), 2 distinct; first: 0, 20
    parent: dtype int64, shape (2,), 1 distinct; first: -1
    root_seed: dtype int64, shape (2,), 1 distinct; first: 1
    segment_label: dtype int64, shape (2,), 2 distinct; first: 2, 9
    termination: dtype object, shape (2,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (2,), 2 distinct; first: 2, 9
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -45.505, -22.244, 14.716, 26.052, 1941.002, 1960.513
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  coronary_right_centerline_ostium_pruned.vtk  (11 kB)
    first line: # vtk DataFile Version 5.1
    330 points; bounds [    -9.2,     48.7] [   -64.7,    -22.2] [  1877.3,   1940.0]
    cells: LINES 1 (lengths 330-330)
    consecutive point spacing: median 0.481, 95th pct 0.500
    point_data:
    segment_voted: dtype int64, shape (330,), 1 distinct; first: 9
    cell_data:
    branch_id: dtype int64, shape (1,), 1 distinct; first: 0
    parent: dtype int64, shape (1,), 1 distinct; first: -1
    root_seed: dtype int64, shape (1,), 1 distinct; first: 1
    segment_label: dtype int64, shape (1,), 1 distinct; first: 9
    termination: dtype object, shape (1,), 1 distinct; first: skeleton_end
    segment_voted: dtype int64, shape (1,), 1 distinct; first: 9
    field_data:
    step_mm: dtype float64, shape (1,), 1 distinct; first: 0.5
    seed_points: dtype float64, shape (6,), 6 distinct; first: -45.505, -22.244, 14.716, 26.052, 1941.002, 1960.513
    seed_sides: dtype int64, shape (2,), 2 distinct; first: 0, 1
    ostia_predicted: dtype int64, shape (1,), 1 distinct; first: 1
  Medis tree: 2055 points; bounds [   -12.1,    100.4] [   -87.0,     12.5] [  1870.7,   1961.8]
  volume: shape (512, 512, 512), zooms (np.float32(0.429), np.float32(0.429), np.float32(0.25)), axcodes LAS
    voxel bounds [     0.0,    511.0] [     0.0,    511.0] [     0.0,    511.0]
    RAS mm bounds [  -155.1,     64.2] [   -93.2,    126.0] [  1850.5,   1978.2]
    LPS mm bounds [   -64.2,    155.1] [  -126.0,     93.2] [  1850.5,   1978.2]

```