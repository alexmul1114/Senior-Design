import argparse
import os

from ultralytics import YOLO


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=False, default='pretrained_models/yolo11m.pt', help='Path to pre-trained model')
    parser.add_argument('--data_yaml', type=str, required=False, default='/home/tjriz/Documents/Senior-Design/datasets/SADD/hust-rslab-SAR-aircraft-data.v2i.yolov11.resize640/data.yaml',
                        help='Path to the updated data.yaml file')
    parser.add_argument('--results_dir', type=str, required=False, default='/home/tjriz/Documents/Senior-Design/YOLOv11_training_SADD/results', help='Directory to save results')
    args = parser.parse_args()

    # Initialize YOLO model with pre-trained weights
    model = YOLO(args.model_path)

    # Set training configurations and start training
    model.train(
        data=args.data_yaml,           # Path to the YAML configuration file
        epochs=200,                # Number of training epochs (adjust based on need)
        batch=12,                  # Batch size (adjust based on GPU memory)
        imgsz=200,                 # Input image size (matches the preprocessed size)
        save_dir=args.results_dir,      # Directory to save training logs and checkpoints
        name='hrsid_detection', # Custom name for the experiment
        device='cpu'                   # Specifies GPU (0) or CPU (-1)
    )


if __name__ == '__main__':
    main()
