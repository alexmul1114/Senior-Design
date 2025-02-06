# The necessary modifications were made for each of the training runs I did for all of the different versions of the dataset; i.e.
# the file paths, image size, batch size (changed from 16 to 8/12 for 640x640 resized images), and experiment name.

from ultralytics import YOLO
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=False, default='yolo11n.pt', help='Path to pre-trained model')
    parser.add_argument('--data_yaml', type=str, required=False, default='/home/tjriz/Documents/Senior-Design/datasets/SADD/hust-rslab-SAR-aircraft-data.v2i.yolov11.resize640/data.yaml',
                        help='Path to the updated data.yaml file')
    parser.add_argument('--results_dir', type=str, required=False, default='/home/tjriz/Documents/Senior-Design/YOLOv11_training_SADD/results', help='Directory to save results')
    parser.add_argument('--device', type=str, required=False, default=-1, help='Specific GPU num or CPU (-1) or mps')
    args = parser.parse_args()

    if args.device.isdecimal():
        args.device = int(args.device)

    # Initialize YOLO model with pre-trained weights
    model = YOLO(args.model_path)

    # Set training configurations and start training
    model.train(
        data=args.data_yaml,           # Path to the YAML configuration file
        epochs=200,                # Number of training epochs (adjust based on need)
        batch=64,                  # Batch size (adjust based on GPU memory)
        imgsz=200,                 # Input image size (matches the preprocessed size)
        save_dir=args.results_dir,      # Directory to save training logs and checkpoints
        name='airplane_detection_resize200', # Custom name for the experiment
        device=args.device            # Specifies GPU (0,1,...) or cpu or mps
    )

if __name__ == '__main__':
    main()