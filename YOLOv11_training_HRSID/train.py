import argparse
import os

from ultralytics import YOLO


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=False, default='yolo11n.pt', help='Path to pre-trained model')
    parser.add_argument('--data_yaml', type=str, required=False, default='datasets/HRSID/yolo/hrsid.yaml',
                        help='Path to the updated data.yaml file')
    parser.add_argument('--results_dir', type=str, required=False, default='YOLOv11_training_HRSID/results', help='Directory to save results')
    parser.add_argument('--device', type=str, required=False, default=-1, help='Specific GPU num or CPU (-1) or mps')
    args = parser.parse_args()

    # Initialize YOLO model with pre-trained weights
    model = YOLO(args.model_path)

    # Set training configurations and start training
    model.train(
        data=args.data_yaml,           # Path to the YAML configuration file
        epochs=200,                # Number of training epochs (adjust based on need)
        batch=64,                  # Batch size (adjust based on GPU memory)
        imgsz=200,                 # Input image size (matches the preprocessed size)
        save_dir=args.results_dir,      # Directory to save training logs and checkpoints
        name='hrsid_detection', # Custom name for the experiment
        device=args.device            # Specifies GPU (0,1,...) or cpu or mps
    )


if __name__ == '__main__':
    main()
