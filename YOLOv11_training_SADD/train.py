# The necessary modifications were made for each of the training runs I did for all of the different versions of the dataset; i.e.
# the file paths, image size, batch size (changed from 16 to 8 for 640x640 resized images), and experiment name.

from ultralytics import YOLO

# Define paths and configurations
model_path = 'yolo11m.pt'
data_yaml = '/home/tjriz/Documents/Senior-Design/datasets/SADD/hust-rslab-SAR-aircraft-data.v1i.yolov11/data.yaml'  # Path to the updated data.yaml file
results_dir = '/home/tjriz/Documents/Senior-Design/YOLOv11_training_SADD/results'  # Directory to save results

# Initialize YOLO model with pre-trained weights
model = YOLO(model_path)

# Set training configurations and start training
model.train(
    data=data_yaml,           # Path to the YAML configuration file
    epochs=200,                # Number of training epochs (adjust based on need)
    batch=12,                  # Batch size (adjust based on GPU memory)
    imgsz=640,                 # Input image size (matches the preprocessed size)
    save_dir=results_dir,      # Directory to save training logs and checkpoints
    name='airplane_detection_resize640_2', # Custom name for the experiment
    device=0                   # Specifies GPU (0) or CPU (-1)
)

