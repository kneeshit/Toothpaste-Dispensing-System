#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# from detectionUtils import *

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_PRESENT_CURRENT    = 126
ADDR_PRO_GOAL_CURRENT       = 102
ADDR_PRO_OPERATING_MODE     = 11

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                 # Dynamixel ID : 1
# DXL2_ID                   = 2   
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM4'            # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

OPERATING_MODE              = 5
TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 10                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000              # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MINIMUM_CURRENT_VALUE   = 0                 # Ensure within current limits
DXL_MAXIMUM_CURRENT_VALUE   = 1000 
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Set Operating Mode to Current Based Position Control Mode
dxl_mode_result, dxl_mode_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, OPERATING_MODE)
if dxl_mode_result != COMM_SUCCESS:
    print("Operating mode set failed: %s" % packetHandler.getTxRxResult(dxl_mode_result))
elif dxl_mode_error != 0:
    print("Operating mode set error: %s" % packetHandler.getRxPacketError(dxl_mode_error))
else:
    print("Operating mode set to Current Based Position Control Mode")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

# Functions
def read_pos():
    present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return present_position

def write_pos(val):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, val)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def change_rate(val):
    present_current, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_CURRENT)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, present_current + val)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Initialize
goal_position=3500
write_pos(goal_position)

initial_current=200
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, initial_current)
if dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

goal_rate=5
step_size=1
goal_length=10
present_length=0

# Main loop
while present_length < goal_length:

    present_rate=0                  # get it from vision
    present_length=0                # get it from vision

    if present_rate < goal_rate:
        change_rate(+step_size)     # increase rate
    elif present_rate > goal_rate:
        change_rate(-step_size)     # decrease rate
