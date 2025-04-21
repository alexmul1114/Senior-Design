# Senior-Design
ECE Senior Design Project

## Datasets:
1. HRSID - https://github.com/chaozhong2010/HRSID (we use PNG version here). Download to "datasets" folder within Senior-Design. To get YOLO-formatted images and labels, run the yolo/prepare_datasets_yolo.py script with args --dataset hrsid and --make_patches.
2. SADD - https://universe.roboflow.com/project-y2j81/hust-rslab-sar-aircraft-data/dataset/2 (this working link navigates to a page with various dataset formats)
            ---> This is the link for the GitHub page officially attached to the IEEE paper, but had issues downloading dataset directly through here:
                     https://github.com/hust-rslab/SAR-aircraft-data
3. XView3 - The xView3 SAR dataset is available through [here](https://iuu.xview.us/dataset), and requires a registration process and a unique method of downloading involving a batch script. 
4. UMBRA Ship Dataset - available via the UMBRA open data catalog on AWS, see umbra_ship_detection_images/download.sh for more info.

## Project Structure:
- dataset_exploration - contains python notebooks that view sample images from the datasets, compute statistics, etc.
- datasets - contains a python script to combine HRSID and SADD datasets into one dataset for YOLOv11 fine-tuning
- YOLOv11_training_HRSID - contains python scripts, yaml configuration files for fine-tuning YOLO models on HRSID
- YOLOv11_training_SADD - contains python scripts, yaml configuration files for fine-tuning YOLO models on SADD
- YOLOv11_training_combined - contains python scripts, yaml configuration files for fine-tuning YOLO models on the combined HRSID/SADD dataset
- umbra_ship_detection_images - contains a python script to conveniently download a specified number of images from the high-resolution UMBRA ship dataset
- super_resolution_testing - contains a python notebook, sample results for applying different super-resolution models
- swin_ir_finetuning - contains python notebook for preparing UMBRA images for fine-tuning a SwinIR model, a json configuration file for fine-tuning, and a fine-tuning script
