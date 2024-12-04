# This module takes the image from the camera and processes it using the YOLOv8n model and then shows the detection in live video

import cv2
import sys
import matplotlib.pyplot as plt
import numpy as np
# from detectionUtils import *
from ultralytics import YOLO
import pathlib

# cwd = pathlib.Path()
# print(cwd)

# model = YOLO(r"runs/detect/train3/weights/best.pt")

# height = display_state_from_camera(model, camera_index=0, flip=True, verbose=True)
# t = find_state(model, camera_index=0)
# print(length_toothbrush, length_toothpaste, rate_toothpaste)