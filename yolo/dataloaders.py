import torch
from torch.utils.data import Dataset
from PIL import Image
import os


class HRSIDDataset(Dataset):
    def __init__(self, dataset_path):
        self.image_folder_path = os.path.join(dataset_path, "images")
        self.annotations_path = os.path.join(dataset_path, "annotations", "train_test2017.json")

        
    def __len__(self):
        

    def __getitem__(self, idx):
        