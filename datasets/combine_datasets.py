# Script to combine HRSID and SADD datasets into one directory
# It is assumed that the HRSID and SADD (hust-rslab-SAR-aircraft-data.v2i.yolov11.resize200) dataseta have been
# created and formatted for YOLO training.

import argparse
import os
import yaml
import shutil

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_dir', type=str, required=False, default='/Users/alexm/Senior-Design', help='Path to root project directory')

    args = parser.parse_args()

    # 1. Create directory structure
    datasets_dir = os.path.join(args.root_dir, "datasets")
    combined_datasets_dir = os.path.join(datasets_dir, "HRSID_SADD_Combined")

    if not os.path.exists(combined_datasets_dir):
        os.makedirs(combined_datasets_dir)
    for split in ["train", "valid", "test"]:
        split_dir = os.path.join(combined_datasets_dir, split)
        for obj in ["images", "labels"]:
            obj_dir = os.path.join(split_dir, obj)
            if not os.path.exists(obj_dir):
                os.makedirs(obj_dir, exist_ok=True)

    # 2. Create yaml file
    yaml_path = os.path.join(combined_datasets_dir, "hrsid_sadd_combined.yaml")
    yaml_data = {
        "path": combined_datasets_dir,
        "train": os.path.join("train", "images"),
        "val": os.path.join("valid", "images"),
        "test": os.path.join("test", "images"),
        "names": {0: "ship", 1: "airplane"}
    }

    if not os.path.exists(yaml_path):
        with open(yaml_path, "w") as file:
            yaml.dump(yaml_data, file, default_flow_style=False)

    # 3. Copy images and labels from separate dataset directories into the combined one
    # Need to do train, valid, test from each dataset
    hrsid_dataset_path = os.path.join(datasets_dir, "HRSID", "yolo")
    sadd_dataset_path = os.path.join(datasets_dir, "SADD", "hust-rslab-SAR-aircraft-data.v2i.yolov11.resize200")
    for dataset_path in [hrsid_dataset_path, sadd_dataset_path]:
        for split in ["train", "valid",  "test"]:
            src_images_path = os.path.join(dataset_path, split, "images")
            src_labels_path = os.path.join(dataset_path, split, "labels")
            dst_images_path = os.path.join(combined_datasets_dir, split, "images")
            dst_labels_path = os.path.join(combined_datasets_dir, split, "labels")
            for file in os.listdir(src_images_path):
                shutil.copy2(os.path.join(src_images_path, file), os.path.join(dst_images_path, file))
            for file in os.listdir(src_labels_path):
                shutil.copy2(os.path.join(src_labels_path, file), os.path.join(dst_labels_path, file))

    print("Combined HRSID/SADD Dataset Successfully Created!")

if __name__ == "__main__":
    main()