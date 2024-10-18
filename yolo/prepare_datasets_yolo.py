# Script to convert images annotations to YOLO format, split images,...?

import argparse
import os
import json
from PIL import Image
from tqdm import tqdm
import numpy as np
import yaml
import shutil

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, help='Dataset to convert')
    parser.add_argument('--dataset_path', type=str, required=True, help='Dataset path')
    parser.add_argument('--make_patches', action='store_true')
    args = parser.parse_args()

    if args.dataset.lower() == 'hrsid':

        image_folder = os.path.join(args.dataset_path, 'images')
        annotations_file = os.path.join(args.dataset_path, 'annotations', 'train_test2017.json')

        # Collect list of image names and annotations
        with open(annotations_file) as json_data:
            data = json.load(json_data)
            image_infos = data['images']
            image_annotations = data['annotations']
            del data
            

        # Create directories for train, val, and test patches, and labels to match YOLO format
        train_patches_folder = os.path.join(args.dataset_path, 'yolo', 'train', 'images')
        val_patches_folder = os.path.join(args.dataset_path, 'yolo', 'val', 'images')
        test_patches_folder = os.path.join(args.dataset_path, 'yolo', 'test', 'images')
        train_labels_folder = os.path.join(args.dataset_path, 'yolo', 'train', 'labels')
        val_labels_folder = os.path.join(args.dataset_path, 'yolo', 'val', 'labels')
        test_labels_folder = os.path.join(args.dataset_path, 'yolo', 'test', 'labels')

        # Clear existing labels first so labels are not repeated if this script run multiple times
        try:
            shutil.rmtree(train_labels_folder)
            shutil.rmtree(val_labels_folder)
            shutil.rmtree(test_labels_folder)
        except:
            pass

        for folder in [train_patches_folder, val_patches_folder, test_patches_folder, 
                       train_labels_folder, val_labels_folder, test_labels_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Make 80/10/10 train/val/test split of patches, save idxs
        train_samples = int(0.8 * len(image_infos*16))
        val_test_samples = int(0.1 * len(image_infos*16))
        rng = np.random.default_rng(seed=0)
        patch_idxs_shuffled = rng.permutation(np.arange(len(image_infos*16)))
        train_idxs = patch_idxs_shuffled[:train_samples]
        val_idxs = patch_idxs_shuffled[train_samples:train_samples+val_test_samples]
        test_idxs = patch_idxs_shuffled[train_samples+val_test_samples:]
        np.save(os.path.join(args.dataset_path, "train_idxs.npy"), train_idxs)
        np.save(os.path.join(args.dataset_path, "val_idxs.npy"), val_idxs)
        np.save(os.path.join(args.dataset_path, "test_idxs.npy"), test_idxs)

        # Create mappings from overall patch idx to split for ease in saving patches to correct folder
        patch_idx_to_split_folder = {}
        patch_idx_to_split_folder_labels = {}
        for i in range(train_idxs.shape[0]):
            patch_idx_to_split_folder[str(train_idxs[i])] = train_patches_folder
            patch_idx_to_split_folder_labels[str(train_idxs[i])] = train_labels_folder
        for i in range(val_idxs.shape[0]):
            patch_idx_to_split_folder[str(val_idxs[i])] = val_patches_folder
            patch_idx_to_split_folder_labels[str(val_idxs[i])] = val_labels_folder
        for i in range(test_idxs.shape[0]):
            patch_idx_to_split_folder[str(test_idxs[i])] = test_patches_folder
            patch_idx_to_split_folder_labels[str(test_idxs[i])] = test_labels_folder


        # Split each image into 200x200 patches, save them in image_patches folder
        # Image naming convention: (original img name)_(patch id in image)_(patch id overall),
        # where patch id is 0 for top leftmost patch, then 1 for patch below, ... down to 15 for bottom rightmost patch
        if args.make_patches:
            print("Making image patches:")
            overall_patch_idx = 0  # Ranges from 0 to number of total patches for all images (about 90,000)
            for _, img_info in enumerate(tqdm(image_infos)):
                img_path = os.path.join(image_folder, img_info['file_name'])
                with Image.open(img_path) as img:
                    patch_idx = 0  # Ranges from 0 to 15 for image
                    for x_start in [0, 200, 400, 600]:
                        for y_start in [0, 200, 400, 600]:
                            patch = img.crop((x_start, y_start, x_start + 200, y_start + 200))
                            split_folder = patch_idx_to_split_folder[str(overall_patch_idx)]
                            if overall_patch_idx == 3915: 
                                print(split_folder)
                            patch_path = os.path.join(split_folder, 
                                                      img_info['file_name'][:-4] + '_' + str(patch_idx) + '_' + str(overall_patch_idx) + '.png')
                            patch.save(patch_path)
                            patch_idx += 1
                            overall_patch_idx += 1
        

        # Loop through all annotations
        for annot in image_annotations:

            img_id = annot['image_id']

            # Find what patch the image is in. 
            box_x_start, box_y_start, box_width, box_height = annot['bbox']
            box_x_end = box_x_start + box_width
            box_y_end = box_y_start + box_height
            
            # Handle overlapping patches:
            # 1. Decide which patch img should be in based on center of mass
            # 2. Truncate cooridinates of box to the patch
            # Get yolo formatted label (center, width, height, all normalized in 0-1)
            box_x_start_idx = box_x_start // 200
            box_x_end_idx = box_x_end // 200
            box_y_start_idx = box_y_start // 200
            box_y_end_idx = box_y_end // 200

            # For ships overlapping multiple patches, add all patches
            img_patch_idxs = []   
            center_xs = []
            center_ys = []
            widths = []
            heights = []
            
            if box_x_start_idx == box_x_end_idx and box_y_start_idx == box_y_end_idx:  # No overlapping
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, box_y_start % 200, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
                
            elif box_x_start_idx != box_x_end_idx and box_y_start_idx == box_y_end_idx: # overlapping in x but not y
                # Add left patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, box_y_start % 200, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
            
                # Add right patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_end, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, box_y_start % 200, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
                

            elif box_x_start_idx == box_x_end_idx and box_y_start_idx != box_y_end_idx: # overlapping in y but not x
                # Add top patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, box_y_start % 200, 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
                # Add bottom patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_end))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, 0, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)

            else: # overlapping in x and y
                # Top left patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, box_y_start % 200, 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
            
                # Bottom left patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_start, box_y_end))
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, 0, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
            
                # Top right patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_end, box_y_start))
                center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, box_y_start % 200, 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)
            
                # Bottom right patch
                img_patch_idxs.append(coords_to_patch_idx(box_x_end, box_y_end))
                center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, 0, box_y_end % 200)
                center_xs.append(center_x)
                center_ys.append(center_y)
                widths.append(width)
                heights.append(height)

            for img_patch_idx, center_x, center_y, width, height in zip(img_patch_idxs, center_xs, center_ys, widths, heights): 
                # Get overall patch idx
                overall_patch_idx = int(img_id * 16 + img_patch_idx)

                # Save labels in a .txt file (one per image, one row per object)
                img_info = image_infos[img_id]
                label_split_folder = patch_idx_to_split_folder_labels[str(overall_patch_idx)]
                save_path = os.path.join(label_split_folder, 
                                            img_info['file_name'][:-4] + '_' + str(int(img_patch_idx)) + '_' + str(overall_patch_idx) + ".txt")

                # Append to existing labels for patch or create new file if none exist
                with open(save_path, 'a') as file:
                    file.write("0 " + str(center_x) + " " + str(center_y) + " " + str(width) + " " + str(height) + "\n")


        # Create yaml file for yolo
        yaml_info = {"path":os.path.join(args.dataset_path, "yolo"), "train":"train/images", 
                     "val":"val/images", "test":"test/images", "names":{0:"ship"}}
        with open(os.path.join(args.dataset_path, 'yolo', args.dataset.lower() + '.yaml'), 'w') as yaml_file:
            yaml.dump(yaml_info, yaml_file, default_flow_style=False, sort_keys=False)
        #stream = file(os.path.join(args.dataset_path, 'yolo', args.dataset.lower() + '.yaml'), 'w')
        #yaml.dump(yaml_info, stream)


    else:
        print("Unrecognized dataset!")


def coords_to_patch_idx(x, y):
    row = y // 200
    col = x // 200
    return col * 4 + row

# Convert from box coordinates to yolo format (center of box + width + height, all normalized 0-1)
def format_yolo(total_x, total_y, x_start, x_end, y_start, y_end):

    center_x = 0.5*(x_end + x_start) / total_x
    center_y = 0.5*(y_end + y_start) / total_y

    width = (x_end - x_start) / total_x
    height = (y_end - y_start) / total_y

    return center_x, center_y, width, height


if __name__ == '__main__':
    main()