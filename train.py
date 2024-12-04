from dynamixel_sdk import *
import serial
import cv2


DEVICENAME              = '/dev/ttyUSB0'             # Check which port is being used on your controller
                                             # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"
# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Protocol version
PROTOCOL_VERSION        = 2.0

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Default setting
DXL_ID                  = 1                  # Dynamixel ID: 1
BAUDRATE                = 57600              # Dynamixel default baudrate : 57600
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()
    
ADDR_HARDWARE_ERROR_STATUS = 70
# Check for hardware errors
dxl_hardware_error, dxl_comm_result, dxl_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_HARDWARE_ERROR_STATUS)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    if dxl_hardware_error != 0:
        print("Hardware Error Status: %d" % dxl_hardware_error)


import numpy as np
from detection import detection, detectionUtils
from ultralytics import YOLO
from motor.motor_control import *


def brush_ready(portHandler, packetHandler, camera_index=0):
    model = YOLO(r"runs/detect/train3/weights/best.pt")

    # detectionUtils.show_camera(2)
    target = detectionUtils.find_target_length(model, camera_index=camera_index, show_camera=True)
    # target = 100
    print(f"Target length is: {target} pixels!")
    initialize_motor(portHandler, packetHandler)
    # initialize_motor_with_initial_position(portHandler, packetHandler, -18000, DXL_ID)
    # write_position(portHandler, packetHandler, -10000)

    # initialize_motor(portHandler, packetHandler)

    # length, rate = detectionUtils.find_state(model, camera_index=0, show_processed_video=True)
    length, rate = 0, 0
    target_rate = 20
    print(f"length: {length}, rate: {rate}")
    curr_pos = read_position(portHandler, packetHandler)
    print(f"curr_position: {curr_pos}")

    capture = cv2.VideoCapture(0)


    while(length < 0.9 * target):
        length, rate = detectionUtils.find_length_and_rate(model, capture, show_processed_video=True, verbose=True)
        print(f"Current length is: {length} pixels!")
        print(f"Current rate is: {rate} pixels/s!")
        
        # Take action of increasing position
        if(rate < target_rate):
            curr_pos += 50
        
        # Take action of decreasing position
        elif(rate > target_rate):
            curr_pos -= 50
            
        write_position(portHandler, packetHandler, curr_pos, DXL_ID)    
        
    write_position(portHandler, packetHandler, 0, DXL_ID)
        
    

def reset_motor_position(portHandler, packetHandler):
    write_position(portHandler, packetHandler, 0, DXL_ID)
    print("Motor position reset to 0")
    
    

brush_ready(portHandler, packetHandler, camera_index=0, show_camera=True)
# reset_motor_position(portHandler, packetHandler)








# give_force_with_initialization(0.5, 50, 9000, portHandler, packetHandler)
    
    
