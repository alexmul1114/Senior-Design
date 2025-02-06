import os
from PIL import Image
import argparse
import random
from pathlib import Path
import shutil
import yaml


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, required=False, default=r"/Users/alexm/Senior-Design/datasets/SADD", help="Path to dataset")
    args = parser.parse_args()

    output_resized_data_dir = os.path.join(args.dataset_path, "hust-rslab-SAR-aircraft-data.v2i.yolov11.resize200")
    output_resized_data_640_dir = os.path.join(args.dataset_path, "hust-rslab-SAR-aircraft-data.v2i.yolov11.resize640")
    output_original_data_dir = os.path.join(args.dataset_path, "hust-rslab-SAR-aircraft-data.v2i.yolov11.newsplit")

    # Target image size for resizing
    target_size = (200,200)
    target_size_640 = (640,640)

    # Desired split ratios
    train_ratio = 0.7
    valid_ratio = 0.2
    test_ratio = 0.1

    # Setting a deterministic seed for reproducability
    random.seed(42)

    # Function to clear existing files in a directory
    def clear_directory(directory):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

    # Prepare output directories and clear any existing files for both resized and original datasets
    for output_dir in [output_resized_data_dir, output_resized_data_640_dir, output_original_data_dir]:
        for split in ['train', 'valid', 'test']:
            image_dir = os.path.join(output_dir, split, 'images')
            label_dir = os.path.join(output_dir, split, 'labels')
            os.makedirs(image_dir, exist_ok=True)
            os.makedirs(label_dir, exist_ok=True)
            clear_directory(image_dir)  # Clear existing images
            clear_directory(label_dir)  # Clear existing labels

    # Get all image files and corresponding label files, sorting to maintain reproducability across different systems,
    # as utilizing .glob() across different operating systems might produce different results
    image_files = sorted(list(Path(args.dataset_path, 'train/images').glob('*.jpg')) + \
                list(Path(args.dataset_path, 'valid/images').glob('*.jpg')))

    # Shuffle the dataset and split into train, valid, and test sets
    random.shuffle(image_files)
    train_end = int(len(image_files) * train_ratio)
    valid_end = train_end + int(len(image_files) * valid_ratio)

    train_files = image_files[:train_end]
    valid_files = image_files[train_end:valid_end]
    test_files = image_files[valid_end:]

    # Function to process files for both resized and original directories
    def process_files(files, split):
        for img_path in files:
            # Define paths
            label_path = img_path.with_suffix('.txt').as_posix().replace('images', 'labels')
            
            # Process for resized directory
            with Image.open(img_path) as img:
                resized_img = img.resize(target_size, Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
                resized_img.save(os.path.join(output_resized_data_dir, split, 'images', img_path.name))
                resized_img_640 = img.resize(target_size_640, Image.LANCZOS)  # Use LANCZOS for high-quality upsampling
                resized_img_640.save(os.path.join(output_resized_data_640_dir, split, 'images', img_path.name))
            
            # Process for original 224x224 directory (copy without resizing)
            shutil.copy(img_path, os.path.join(output_original_data_dir, split, 'images', img_path.name))

            # Copy the annotation file to both directories
            if os.path.exists(label_path):
                shutil.copy(label_path, os.path.join(output_resized_data_dir, split, 'labels', os.path.basename(label_path)))
                shutil.copy(label_path, os.path.join(output_resized_data_640_dir, split, 'labels', os.path.basename(label_path)))
                shutil.copy(label_path, os.path.join(output_original_data_dir, split, 'labels', os.path.basename(label_path)))

    # Process and save images and labels for each split
    process_files(train_files, 'train')
    process_files(valid_files, 'valid')
    process_files(test_files, 'test')

    # Function to create data.yaml file for YOLO training
    def create_data_yaml(directory, num_classes, list_classes):
        data_yaml = {
            'train': os.path.join(directory, 'train/images'),
            'val': os.path.join(directory, 'valid/images'),
            'test': os.path.join(directory, 'test/images'),
            'nc': num_classes,
        }
        
        yaml_path = Path(directory) / 'data.yaml'
        with open(yaml_path, 'w') as f:
            yaml.dump(data_yaml, f, default_flow_style=False, sort_keys=False)

        # Manually add class names in the desired format (comma-separated strings surrounded by brackets)
        # Trying to do this directly through the yaml.dump() function utilizing the list passed as an argument 
        # caused issues with the desired data.yaml formatting
        with open(yaml_path, 'a') as f:
            f.write(f"names: {list_classes}\n")

    # Create data.yaml for both resized and original directories
    create_data_yaml(output_resized_data_dir, 1, ['airplane'])
    create_data_yaml(output_resized_data_640_dir, 1, ['airplane'])
    create_data_yaml(output_original_data_dir, 1, ['airplane'])

    print("Dataset preparation complete. Both resized and original images are stored separately.")


if __name__ == '__main__':
    main()  