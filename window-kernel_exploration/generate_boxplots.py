#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  4 14:25:49 2025

@author: tjriz
"""

# # Side‑by‑side box‑plots for normalized bounding‑box widths & heights
# import numpy as np
# import matplotlib.pyplot as plt
# from pathlib import Path

# confirmed_UMBRA_widths_npy   = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_widths_confirmed.npy"
# confirmed_UMBRA_heights_npy  = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_heights_confirmed.npy"
# fig_title    = "Dataset A — Normalized bbox sizes"
# save_png     = False
# out_png_path = "datasetA_boxplot.png"

# # load arrays and flatten to 1‑D
# widths  = np.asarray(np.load(confirmed_UMBRA_widths_npy)).ravel()
# heights = np.asarray(np.load(confirmed_UMBRA_heights_npy)).ravel()

# # make box‑and‑whisker plot
# fig, ax = plt.subplots(figsize=(6, 8))
# ax.boxplot([widths, heights],
#            labels=["Width", "Height"],
#            patch_artist=True,
#            boxprops=dict(facecolor="lightblue"))
# ax.set_ylabel("Normalized value (0–1)")
# ax.set_title(fig_title)

# # save or show
# if save_png:
#     Path(out_png_path).parent.mkdir(parents=True, exist_ok=True)
#     plt.savefig(out_png_path, dpi=300, bbox_inches="tight")
#     print(f"Plot saved → {out_png_path}")
# else:
#     plt.show()

# Overlayed swarm plots onto box plots, using seaborn package
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

confirmed_UMBRA_widths_npy   = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_widths_confirmed.npy"
confirmed_UMBRA_heights_npy  = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_heights_confirmed.npy"
questionable_UMBRA_widths_npy   = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_widths_questionable.npy"
questionable_UMBRA_heights_npy  = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/test-window-kernel/UMBRA_window_heights_questionable.npy"
HRSID_boxes_npy = "/home/tjriz/Documents/Senior-Design/window-kernel_exploration/HRSID_pixel-aspect-info/annotation_array.npy"

# fig_title = "UMBRA with Window/Kernel Method,\nNormalized Bounding Box Statistics\n(Confirmed Detections: i.e. 'Most Likely' Single Ship)"
# fig_title = "UMBRA with Window/Kernel Method,\nNormalized Bounding Box Statistics\n(Questionable Detections: i.e. 'Most Likely'\nPartials or Multiple Ships)"
fig_title = "HRSID Labeled Dataset\n(Preprocessed/Sliced to 200x200),\nNormalized Bounding Box Statistics"
save_png  = True
# out_png_path_boxswarm  = "UMBRA-confirmed_WindowKernelStatistics.png"
# out_png_path_boxswarm  = "UMBRA-questionable_WindowKernelStatistics.png"
out_png_path_boxswarm  = "HRSID_BoundingBoxStatistics.png"

# load and flatten arrays if necessary
# widths  = np.asarray(np.load(confirmed_UMBRA_widths_npy)).ravel()
# heights = np.asarray(np.load(confirmed_UMBRA_heights_npy)).ravel()
# widths  = np.asarray(np.load(questionable_UMBRA_widths_npy)).ravel()
# heights = np.asarray(np.load(questionable_UMBRA_heights_npy)).ravel()
widths  = np.asarray(np.load(HRSID_boxes_npy))[:,3]
heights = np.asarray(np.load(HRSID_boxes_npy))[:,4]

# put into DataFrame for seaborn box/swarm plot visualization
df = pd.DataFrame(dict(
    value = np.concatenate([widths, heights]),
    group = ["Width"]*len(widths) + ["Height"]*len(heights)
))


fig, ax = plt.subplots(figsize=(8, 10))

sns.boxplot(x="group", y="value", data=df,
            showfliers=False,
            palette=sns.color_palette("pastel",2), ax=ax)
# sns.swarmplot(x="group", y="value", data=df,
#               color="black", size=2, ax=ax)
sns.swarmplot(x="group", y="value", data=df,
              color="black", size=0.3, ax=ax)
ax.set_xlabel("Bounding Box Dimension", size=16, fontweight="bold")
ax.set_ylabel("Normalized Value (0–1)", size=16, fontweight="bold")
ax.set_title(fig_title, size=20, fontweight="bold")

if save_png:
    Path(out_png_path_boxswarm).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png_path_boxswarm, dpi=300, bbox_inches="tight")
    print(f"Swarm + box plot saved → {out_png_path_boxswarm}")
else:
    plt.show()
