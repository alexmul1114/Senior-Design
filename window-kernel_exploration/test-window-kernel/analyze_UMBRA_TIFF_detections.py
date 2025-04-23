#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:54:27 2025

@author: tjriz
"""

import argparse
from pathlib import Path
import numpy as np
import csv

# for parsing command line arguments, wanted to learn how to do this using Python script
ap = argparse.ArgumentParser(description="Compute bbox stats from log files")
ap.add_argument("files", nargs="+",
                help="Paths to confirmed_detections.txt, questionable_detections.txt, …")
args = ap.parse_args()

# for collecting widths and heihts of bounding boxes from every specified file
widths  = []
heights = []

for fpath in args.files:
    fpath = Path(fpath)
    if not fpath.exists():
        print(f"[warning] {fpath} not found — skipping")
        continue

    with fpath.open() as fh:
        reader = csv.reader(fh)
        for row in reader:
            # If incorrectly formatted detection line
            if len(row) < 5:
                continue
            x1, y1, x2, y2 = map(float, row[1:5])
            widths.append(x2 - x1)
            heights.append(y2 - y1)

# if there were boxes, print statistics
if widths:
    w = np.array(widths)
    h = np.array(heights)

    def stats(arr):
        return (arr.mean(), arr.min(), arr.max(), arr.std(), arr.var())

    w_mean, w_min, w_max, w_std, w_var = stats(w)
    h_mean, h_min, h_max, h_std,  h_var = stats(h)

    print("Bounding‑box width (pixels)")
    print(f"  mean: {w_mean:.2f}   min: {w_min:.2f}   max: {w_max:.2f}   std deviation: {w_std:.2f} var: {w_var:.2f}")
    print("Bounding‑box height (pixels)")
    print(f"  mean: {h_mean:.2f}   min: {h_min:.2f}  max: {h_max:.2f}   std deviation: {h_std:.2f} var: {h_var:.2f}")
    print(f"Total boxes analysed: {len(w)}")
else:
    print("No bounding boxes found in the provided file(s).")
