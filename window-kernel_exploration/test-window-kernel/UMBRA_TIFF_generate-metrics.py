#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:19:34 2025

@author: tjriz
"""

import os
import cv2
import numpy as np
import torch
import rasterio
from rasterio.windows import Window
from rasterio.enums import Resampling
from ultralytics import YOLO
from tqdm import tqdm       # for progress bars
from pathlib import Path

# configuration parameters
ROOT_DIR = "/home/tjriz/Documents/Senior-Design/datasets/tif-images/sar-data/tasks/ship_detection_testdata"
WEIGHTS_PT = "/home/tjriz/Documents/Senior-Design/YOLOv11_training_HRSID/runs/detect/HRSID_update-tj/weights/best.pt"
LOG_TXT = "confirmed_detections.txt"
QUESTIONABLE_TXT = "questionable_detections.txt"

WIN_FULL = 2500
RESIZE_TO = 224
STRIDE = 1250
CONF_TH = 0.3
NMS_TH = 0.5
HALF_WIN_ZOOM = 400

# returning a list of image directories for two levels down from each directory within a given root directory
def gather_tifs(root_dir):
    tif_paths = []
    top = Path(root_dir)
    for uuid_dir in top.iterdir():
        if not uuid_dir.is_dir():
            continue
        for ts_dir in uuid_dir.iterdir():
            if ts_dir.is_dir():
                for tifp in ts_dir.glob("*.tif"):
                    tif_paths.append(str(tifp))
    return tif_paths

# for computing Intersection-over-Union (IoU) between two axis-aligned bounding boxes
# Important computation for the process of the global NMS
def iou(boxA, boxB):
    # coords of the overlap rectangle
    x1 = max(boxA[0], boxB[0])
    y1 = max(boxA[1], boxB[1])
    x2 = min(boxA[2], boxB[2])
    y2 = min(boxA[3], boxB[3])
    # multiplying the width and height of the overlap to get the area of intersection
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    # Areas of the individual boxes involved in the overlapping
    areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    # returning the IoU, which is intersection is inter and union = (sum of individual areas) - inter + (epsilon to avoid possible division by zero) 
    return inter / (areaA + areaB - inter + 1e-6)

# for performing class-agnostic Non-Maximum Suppression (NMS) on a list of full-resolution detections
# Important for combining overlapping bounding boxes as we use sliding window/kernel method
def global_nms(boxes, thresh=0.4):
    # if no boxes, return empty list
    if not boxes:
        return []
    # quick NumPy conversion so things are easier
    arr = np.array(boxes)
    #sorting from highest to lowest confidence
    order = arr[:, 4].argsort()[::-1]
    # indices we will keep
    keep = []
    while order.size:
        # Current best box
        i = order[0]
        keep.append(i)
        # if the last one, we stop
        if order.size == 1:
            break
        # compare IoU of the best box with every remaining box
        rest = order[1:]
        ious = [iou(arr[i], arr[j]) for j in rest]
        # keep boxes whose IoU is below the threshold
        mask = np.array(ious) < thresh
        # drop overlapping boxes
        order = rest[mask]
    # return the surviving boxes as nested Python list
    return arr[keep].tolist()

def detect_ships(tif_path, model):
    # scale factors to move between full resolution tiles and the 224×224 network input (aligning with dataset trained on)
    scale_down = RESIZE_TO / WIN_FULL
    # inverse for mapping back
    scale_up   = 1.0 / scale_down
    # will hold every detection with respect to full resolution coordinates
    all_boxes  = []
    
    # open the TIFF in "streaming" mode, which means no full image loaded in RAM, presumably less computationally intensive way of reading image
    with rasterio.open(tif_path) as src:
        H, W = src.height, src.width
        # vertical sliding window, with tqdm providing a progress bar for these rows
        for top in tqdm(range(0, H, STRIDE), desc="rows"):
            # "clamping" last row window to bottom edge to prevent error and account for fringes of image
            if top + WIN_FULL > H:
                top = H - WIN_FULL
            # horizontal sliding window across the current row
            for left in range(0, W, STRIDE):
                # "clamping" last column window to right edge to prevent error and account for fringes of image
                if left + WIN_FULL > W:
                    left = W - WIN_FULL
                
                #reading one 2500×2500 tile (single SAR band)
                tile = src.read(1, window=Window(left, top, WIN_FULL, WIN_FULL))
                # replicate single band to "fake" RGB format so YOLOv11 architecture accepts it
                tile_rgb = np.stack([tile]*3, axis=-1)
                
                # downsampling to 224×224, to match resolution of dataset trained on
                tile_rs = cv2.resize(tile_rgb, (RESIZE_TO, RESIZE_TO), interpolation=cv2.INTER_AREA)
                # running inferencing using trained weights, while suppressing console output with verbose=False
                results = model.predict(tile_rs, conf=CONF_TH, verbose=False)
                
                # if detections exist, map each box coordinates back to full image pixels
                if results and len(results[0].boxes):
                    for b in results[0].boxes:
                        # coords in 224×224
                        x1, y1, x2, y2 = b.xyxy[0].tolist()
                        conf = b.conf[0].item()
                        cls  = int(b.cls[0].item())
                        
                        # shift by the tile origin and scale back up to the space of 2500 pixels
                        X1 = left + x1 * scale_up
                        Y1 = top  + y1 * scale_up
                        X2 = left + x2 * scale_up
                        Y2 = top  + y2 * scale_up
                        all_boxes.append([X1, Y1, X2, Y2, conf, cls])
                # exit loop early once we hit the window furthest to the right
                if left + WIN_FULL >= W:
                    break
            # exit loop early once we hit the window furthest towards the bottom
            if top + WIN_FULL >= H:
                break
    # merge the overlapping detections that came from different tiles using a global version of NMS
    final = global_nms(all_boxes, NMS_TH)
    return final

def confirm_detections(full_image, boxes, class_names, image_label, log_file, questionable_file):
    # global counters updated for precision metrics calculated at the end
    global detection_count, yes_count, questionable_count
    # original image size
    H, W = full_image.shape[:2]
    
    # loop over every box, previously filtered with global NMS
    for i, (x1, y1, x2, y2, conf, cls) in enumerate(boxes):
        # total boxes shown so far
        detection_count += 1
        
        # building a cropped/zoomed box view of the detection so the reviewer can see detail without loading the whole giant image
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        left   = max(cx - HALF_WIN_ZOOM, 0)
        right  = min(cx + HALF_WIN_ZOOM, W)
        top    = max(cy - HALF_WIN_ZOOM, 0)
        bottom = min(cy + HALF_WIN_ZOOM, H)
        crop   = full_image[top:bottom, left:right].copy()
        
        # local box coordinates inside the crop/zoom box
        bx1 = int(x1 - left)
        by1 = int(y1 - top)
        bx2 = int(x2 - left)
        by2 = int(y2 - top)
        
        # drawing a rectangle and confidence label on the crop
        cv2.rectangle(crop, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
        label_str = f"{class_names[int(cls)]}: {conf:.2f}"
        cv2.putText(crop, label_str, (bx1, max(by1 - 5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # showing the crop in an OpenCV window while waiting for a key press
        disp_name = "Confirm"
        cv2.namedWindow(disp_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(disp_name, 800, 800)
        cv2.imshow(disp_name, crop)

        print(f"[{i+1}/{len(boxes)}] detection on {image_label}, conf={conf:.2f}")
        print("Press 'y' to confirm, 'n' to skip, 'u' for questionable, 'q' to quit all...")
        
        # blocks further execution until key is pressed
        key = cv2.waitKey(0) & 0xFF
        
        # ------------------------------------------------------------
        # Handling the valid key presses
        #   q: abort entire script
        #   y: log to confirmed file
        #   u: log to questionable file
        #   n: ignore
        # ------------------------------------------------------------
        
        # break outer loop and stop entire logging process
        if key == ord('q'):
            return False
        elif key == ord('y'):
            yes_count += 1
            line = f"{image_label},{x1:.2f},{y1:.2f},{x2:.2f},{y2:.2f},{conf:.3f},{int(cls)}\n"
            log_file.write(line)
            log_file.flush()
        elif key == ord('u'):
            questionable_count += 1
            line = f"{image_label},{x1:.2f},{y1:.2f},{x2:.2f},{y2:.2f},{conf:.3f},{int(cls)}\n"
            questionable_file.write(line)
            questionable_file.flush()
        # any other key, whether 'n' or other unspecified key, simply skips the and logs nothing
    
    # all boxes processed and logged accordingly and we simply continue with the rest of the script
    return True

# MAIN for script execution
if __name__ == "__main__":
    # discover every GeoTIFF we downloaded
    tifs = gather_tifs(ROOT_DIR)
    print(f"Found {len(tifs)} GeoTIFFs in: {ROOT_DIR}")
    
    # load YOLO once on GPU if available, otherwise do so on CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model  = YOLO(WEIGHTS_PT).to(device)
    
    # counters used for rudimentary precision metrics
    detection_count     = 0
    yes_count           = 0
    questionable_count  = 0
    
    # open the two output log files in append mode so we keep earlier work if the script is rerun
    with open(LOG_TXT, "a") as f, open(QUESTIONABLE_TXT, "a") as fq:
        # loop over every .tif path
        for tifp in tifs:
            # “image_label” is immediate parent folder (timestamp folder?)
            image_label = os.path.basename(os.path.dirname(tifp))
            
            # run sliding window/kernel detection, returns NMS-filtered boxes
            boxes = detect_ships(tifp, model)
            if len(boxes) == 0:
                continue
            
            # read entire TIFF once so we can extract crops/zoom boxes for GUI routine of inspection
            with rasterio.open(tifp) as src:
                # single SAR image band
                band = src.read(1)
            # RGB conversion for OpenCV
            full_rgb = np.stack([band]*3, axis=-1)
            
            # interactive confirmation routine initiated and returns False if ‘q’ was pressed
            cont = confirm_detections(full_rgb, boxes, model.names, image_label, f, fq)
            # user chose to exit early
            if not cont:
                break
    
    # tidy up the UI windows and print summary statistics
    cv2.destroyAllWindows()

    if detection_count > 0:
        precision_confirmed = yes_count / detection_count
        precision_plus_q = (yes_count + questionable_count) / detection_count
    else:
        precision_confirmed = 0.0
        precision_plus_q    = 0.0

    print(f"\nStopped. Logged {yes_count} confirmed out of {detection_count}")
    print(f"Questionable detections: {questionable_count}")
    print(f"Precision (confirmed only): {precision_confirmed:.3f}")
    print(f"Precision (confirmed + questionable): {precision_plus_q:.3f}")
    print(f"See {LOG_TXT} for confirmed ships and {QUESTIONABLE_TXT} for questionable ships.")
