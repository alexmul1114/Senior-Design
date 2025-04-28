#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 10:30:10 2025

@author: tjriz
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

# input/output paths

# CSV_PATH = Path("/home/tjriz/Documents/Senior-Design/YOLOv11_training_HRSID/"
#                 "runs/detect/HRSID_update-tj/results.csv")
# OUT_IMG  = Path("/home/tjriz/Documents/Senior-Design/YOLOv11_training_HRSID/"
#                 "HRSID_precision_recall.png")

CSV_PATH = Path("/home/tjriz/Documents/Senior-Design/YOLOv11_training_SADD/"
                "runs/detect/airplane_detection_resize200_2/results.csv")
OUT_IMG  = Path("/home/tjriz/Documents/Senior-Design/YOLOv11_training_SADD/"
                "SADD_precision_recall.png")

# reading with pandas
df = pd.read_csv(CSV_PATH)
PREC_COL = "metrics/precision(B)"
REC_COL  = "metrics/recall(B)"

# dataframes for parsing through .csv information
epochs = df["epoch"] if "epoch" in df.columns else np.arange(1, len(df) + 1)
precision = df[PREC_COL].to_numpy()
recall = df[REC_COL].to_numpy()

# version of smoothing used by YOLOv11 for the plots it generates?
sigma = 3
precision_s = gaussian_filter1d(precision, sigma=sigma, mode="nearest")
recall_s = gaussian_filter1d(recall, sigma=sigma, mode="nearest")

# plotting and labeling raw/smooth curves and figure
fig, axes = plt.subplots(1, 2, figsize=(12, 8), sharex=True)

for ax, raw, smooth, title, ylabel in zip(
        axes,
        [precision, recall],
        [precision_s, recall_s],
        # ["Precision (100 epochs)", "Recall (100 epochs)"],
        ["Precision (200 epochs)", "Recall (200 epochs)"],
        ["Precision","Recall"]):

    ax.plot(epochs, raw, "-", marker="o",markersize=4,
            linewidth=1.2, label="Raw Values")
    ax.plot(epochs, smooth, "--", linewidth=2.5,
            label="Smoothed Curve")
    ax.set_title(title)
    ax.set_xlabel("Epoch")
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle=":")
    ax.legend()

# fig.suptitle("YOLOv11 HRSID Training Results", y=0.97, fontsize=20)
fig.suptitle("YOLOv11 SADD Training Results", y=0.97, fontsize=20)
fig.tight_layout()
fig.savefig(OUT_IMG, dpi=300)
print(f"Saved → {OUT_IMG.resolve()}")
plt.show()