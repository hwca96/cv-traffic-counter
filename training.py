import cv2
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

if __name__ == '__main__':

    # # Load the YOLOv8 model
    model = YOLO('yolov8n.pt')

    # # Training
    results = model.train(data='VisDrone.yaml', epochs=100, imgsz=640)