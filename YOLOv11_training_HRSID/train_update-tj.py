from ultralytics import YOLO

# Define paths and configurations
model_path = 'yolo11m.pt'
data_yaml = '/home/tjriz/Documents/Senior-Design/datasets/HRSID/yolo_2/hrsid.yaml'  # Path to the updated data.yaml file
results_dir = '/home/tjriz/Documents/Senior-Design/YOLOv11_training_HRSID/results'  # Directory to save results

# Initialize YOLO model with pre-trained weights
model = YOLO(model_path)

# Set training configurations and start training
model.train(
    data=data_yaml,           # Path to the YAML configuration file
    epochs=100,                # Number of training epochs (adjust based on need)
    batch=96,                  # Batch size (adjust based on GPU memory)
    imgsz=200,                 # Input image size (matches the preprocessed size)
    save_dir=results_dir,      # Directory to save training logs and checkpoints
    name='HRSID_update-tj', # Custom name for the experiment
    device=0                   # Specifies GPU (0) or CPU (-1)
)
