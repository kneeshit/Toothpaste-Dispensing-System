import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
from torch import where, round
from time import time

TOOTHPASTE_INDEX = 1
TOOTHBRUSH_INDEX = 0  

def find_target_length(model, camera_index=0, show_camera=False):
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        return Exception("Camera not found")
    
    
    while(True):
        ret, frame = capture.read()
        if not ret:
            return Exception("Error, frame could not be read!")
        
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = model(frame_RGB)
    
        if(show_camera):
            cv2.imshow('Video', cv2.cvtColor(processed_frame[0].plot(), cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        
        if(TOOTHBRUSH_INDEX in processed_frame[0].boxes.cls):
            idx = where(processed_frame[0].boxes.cls == TOOTHBRUSH_INDEX)[0][0]
            bounding_box = processed_frame[0].boxes.xyxy[idx]
            toothbrush_length = round(bounding_box[2] - bounding_box[0], decimals=2)
            print(f"Toothbrush detected!, Length is: {toothbrush_length} pixels!")
            break
        else:
            print("Toothbrush NOT detected!")
            continue
    
    return toothbrush_length
    

def find_state(model, camera_index=0, show_processed_video=False):
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        return Exception("Camera not found")
    
    
    fig, ax = plt.subplots()
    while(True):
        a=time()
        length_toothpaste, rate_toothpaste = find_length_and_rate(model, capture, show_processed_video=show_processed_video, verbose=True)
        b=time()
        print(f"FPS: {1/(b-a)}")
        print(f"Length of toothpaste is: {length_toothpaste} pixels!")
        print(f"Rate of toothpaste is: {rate_toothpaste} pixels/s!")
        if cv2.waitKey(10) & 0xFF == ord("q"):
            capture.release()
            break

    return length_toothpaste, rate_toothpaste


def find_length_and_rate(model, capture, show_processed_video=False, verbose=True):
    # Capturing first frame
    ret1, frame1 = capture.read()
    if not ret1:
        return Exception("Error, frame could not be read!")
    
    time1 = time()
    frame_RGB = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    processed_frame1 = model(frame_RGB)

    # Capturing second frame
    ret2, frame2 = capture.read()
    if not ret2:
        return Exception("Error, frame could not be read!")

    time2 = time()
    frame_RGB = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    processed_frame2 = model(frame_RGB)

    time_delta = time2 - time1
    

    # Finding the length and rate of toothpaste
    if(TOOTHPASTE_INDEX in processed_frame1[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
        idx = where(processed_frame1[0].boxes.cls == TOOTHPASTE_INDEX)[0][0]
        bounding_box = processed_frame1[0].boxes.xyxy[idx]
        toothpaste_length1 = round(bounding_box[2] - bounding_box[0], decimals=2)
        if(verbose):
            print(f"Toothpaste detected!, Length is: {toothpaste_length1} pixels!")
    else: # Object not found in the frame
        if(verbose):
            print("Toothpaste NOT detected!")
        toothpaste_length1 = 0

    if(TOOTHPASTE_INDEX in processed_frame2[0].boxes.cls): # If x  the object even exists in the frame, we will proceed to find id for where the box is and obtain the height for it
        idx = where(processed_frame2[0].boxes.cls == TOOTHPASTE_INDEX)[0][0]
        bounding_box = processed_frame2[0].boxes.xyxy[idx]
        toothpaste_length2 = round(bounding_box[2] - bounding_box[0], decimals=2)
        if(verbose):
            print(f"Toothpaste detected!, Length is: {toothpaste_length2} pixels!")
    else: # Object not found in the frame
        if(verbose):
            print("Toothpaste NOT detected!")
        toothpaste_length2 = 0


    if(toothpaste_length1 == 0 or toothpaste_length2 == 0):
        return 0, 0
    
    rate = (toothpaste_length2 - toothpaste_length1)/time_delta

    # Showing the processed video if required
    if(show_processed_video):
        cv2.imshow("Annotated Video", cv2.cvtColor(processed_frame2[0].plot(), cv2.COLOR_RGB2BGR))

    return toothpaste_length2, rate


def show_camera(camera_index):
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        return Exception("Camera not found")
    
    while(True):
        ret, frame = capture.read()
        if not ret:
            return Exception("Error, frame could not be read!")
        
        cv2.imshow("Camera", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()
    return None

