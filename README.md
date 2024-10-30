# Senior-Design
ECE Senior Design Project

## Datasets:
1. HRSID - https://github.com/chaozhong2010/HRSID (we use PNG version here). Download to "datasets" folder within Senior-Design. To get YOLO-formatted images and labels, run the yolo/prepare_datasets_yolo.py script with args --dataset hrsid and --make_patches.

## Training:
To train a YOLO model on HRSID:
1. Install torch: conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
2. Install ultralytics: pip install ultralytics