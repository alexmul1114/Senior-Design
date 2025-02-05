import argparse
import os

from ultralytics import YOLO


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=False, default="hrsid", help='Dataset to train on')
    parser.add_argument('--dataset_path', type=str, required=True, help='Dataset path')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs to train for')
    parser.add_argument('--gpu_util', type=float, default=0.7, help='Proportion of GPU memory to use (<=1.0) to set batch size')
    args = parser.parse_args()

    # Load pretrained model
    model = YOLO("yolo11n.pt")

    # Train model
    data_yaml_path = os.path.join(args.dataset_path, "yolo", args.dataset.lower() + '.yaml')
    results = model.train(data=data_yaml_path, epochs=args.epochs, imgsz=224, batch=args.gpu_util)


if __name__ == '__main__':
    main()
