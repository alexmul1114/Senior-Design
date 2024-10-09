# Script to convert images annotations to YOLO format, split images,...?

import argparse
import os
import json
from PIL import Image
from tqdm import tqdm
import numpy as np
import pickle

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True, help='Dataset to convert')
    parser.add_argument('--dataset_path', type=str, required=True, help='Dataset to convert')
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
        train_patches_folder = os.path.join(args.dataset_path, 'train_image_patches')
        val_patches_folder = os.path.join(args.dataset_path, 'val_image_patches')
        test_patches_folder = os.path.join(args.dataset_path, 'test_image_patches')
        train_labels_folder = os.path.join(args.dataset_path, 'train_image_labels')
        val_labels_folder = os.path.join(args.dataset_path, 'val_image_labels')
        test_labels_folder = os.path.join(args.dataset_path, 'test_image_labels')
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
            
            if box_x_start_idx == box_x_end_idx and box_y_start_idx == box_y_end_idx:  # No overlapping
                img_patch_idx = coords_to_patch_idx(box_x_start, box_y_start)
                center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, box_y_start % 200, box_y_end % 200)
                
            elif box_x_start_idx != box_x_end_idx and box_y_start_idx == box_y_end_idx: # overlapping in x but not y
                x_boundary = box_x_end // 200
                keep_start_x = np.abs(box_x_start - x_boundary*200) > np.abs(box_x_end - x_boundary*200)
                if keep_start_x:
                    img_patch_idx = coords_to_patch_idx(box_x_start, box_y_start)
                    center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, box_y_start % 200, box_y_end % 200)
                else:
                    img_patch_idx = coords_to_patch_idx(box_x_end, box_y_start)
                    center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, box_y_start % 200, box_y_end % 200)
                

            elif box_x_start_idx == box_x_end_idx and box_y_start_idx != box_y_end_idx: # overlapping in y but not x
                y_boundary = box_y_end // 200
                keep_start_y = np.abs(box_y_start - y_boundary*200) > np.abs(box_y_end - y_boundary*200)
                if keep_start_y:
                    img_patch_idx = coords_to_patch_idx(box_x_start, box_y_start)
                    center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, box_y_start % 200, 200)
                else:
                    img_patch_idx = coords_to_patch_idx(box_x_start, box_y_end)
                    center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, box_x_end % 200, 0, box_y_end % 200)

            else: # overlapping in x and y
                x_boundary = box_x_end // 200
                keep_start_x = np.abs(box_x_start - x_boundary*200) > np.abs(box_x_end - x_boundary*200)
                y_boundary = box_y_end // 200
                keep_start_y = np.abs(box_y_start - y_boundary*200) > np.abs(box_y_end - y_boundary*200)
                if keep_start_x and keep_start_y:
                    img_patch_idx = coords_to_patch_idx(box_x_start, box_y_start)
                    center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, box_y_start % 200, 200)
                elif keep_start_x and not keep_start_y:
                    img_patch_idx = coords_to_patch_idx(box_x_start, box_y_end)
                    center_x, center_y, width, height = format_yolo(200, 200, box_x_start % 200, 200, 0, box_y_end % 200)
                elif not keep_start_x and keep_start_y:
                    img_patch_idx = coords_to_patch_idx(box_x_end, box_y_start)
                    center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, box_y_start % 200, 200)
                else:
                    img_patch_idx = coords_to_patch_idx(box_x_end, box_y_end)
                    center_x, center_y, width, height = format_yolo(200, 200, 0, box_x_end % 200, 0, box_y_end % 200)


            # Get overall patch idx
            overall_patch_idx = int(img_id * 16 + img_patch_idx)

            # Save labels in a .txt file (one per image, one row per object)
            img_info = image_infos[img_id]
            label_split_folder = patch_idx_to_split_folder_labels[str(overall_patch_idx)]
            save_path = os.path.join(args.dataset_path, label_split_folder, 
                                     img_info['file_name'][:-4] + '_' + str(int(img_patch_idx)) + '_' + str(overall_patch_idx) + ".txt")

            with open(save_path, 'a') as file:
                file.write("0 " + str(center_x) + " " + str(center_y) + " " + str(width) + " " + str(height) + "\n")


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