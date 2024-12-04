import serial
import time

import os

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


# write_position(portHandler, packetHandler, 9000) # Increasing goal position lowers the screw
# ser = serial.Serial('/dev/ttyUSB0', 9600)  # Arduino connected to COM3


import os
# from detectionUtils import *

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_TORQUE_ENABLE      = 64
ADDR_GOAL_POSITION      = 116
ADDR_PRESENT_POSITION   = 132
ADDR_OPERATING_MODE     = 11




TORQUE_ENABLE           = 1                  # Value for enabling the torque
TORQUE_DISABLE          = 0                  # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 1000           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 2048 * 5       # 5 turns
DXL_MOVING_STATUS_THRESHOLD = 50             # Dynamixel moving status threshold
EXTENDED_POSITION_CONTROL_MODE = 4






def initialize_motor_with_initial_position(portHandler, packetHandler, target, DXL_ID=1):    
    # Disable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

    # Set operating mode to extended position control mode
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, EXTENDED_POSITION_CONTROL_MODE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Operating mode set to extended position control mode")

    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")


    # Write goal position to target to reset the position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, target)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print(f"Goal position set to {target}")

    # # Read present position until it reaches target
    while True:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%d  PresPos:%d" % (DXL_ID, target, dxl_present_position))

        if abs(target - dxl_present_position) <= DXL_MOVING_STATUS_THRESHOLD:
            break


def initialize_motor(portHandler, packetHandler, DXL_ID=1):
    # Disable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

    # Set operating mode to extended position control mode
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, EXTENDED_POSITION_CONTROL_MODE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Operating mode set to extended position control mode")

    # Enable Dynamixel Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")




def read_position(portHandler, packetHandler, DXL_ID=1):
    # Read present position
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print(f"Present position is {dxl_present_position/4096} rotations")
    
    return dxl_present_position

def write_position(portHandler, packetHandler, goal_position, DXL_ID=1):
    # Write goal position to 5 turns
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print(f"Goal position set to {goal_position/4096} rotations")

    # Read present position until it reaches the goal
    while True:
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # print("[ID:%03d] GoalPos:%d  PresPos:%d" % (DXL_ID, goal_position, dxl_present_position))

        if abs(goal_position - dxl_present_position) <= DXL_MOVING_STATUS_THRESHOLD:
            break


# # Disable Dynamixel Torque
# dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
# if dxl_comm_result != COMM_SUCCESS:
#     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
# elif dxl_error != 0:
#     print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
# portHandler.closePort()



def read_force(ser):
    force_reading = None
    count = 0
    while force_reading == None:
        try:
            line = ser.readline().decode('utf-8').strip()
            futek_reading = float(line)
            force_reading = futek_reading * 111 / 1024
            print(f"Force Reading: {force_reading}")
        except ValueError:
            count+=1
            futek_reading = 0
            force_reading = None
    print(f"No. of invalid values skipped: {count}")
    return force_reading
        

def give_force_with_initialization(target_force, rate, initial, portHandler, packetHandler, ser):

    # Initialize the motor
    initialize_motor_with_initial_position(portHandler, packetHandler, initial)
    
    # read futek sensor
    while True:

        ser.reset_input_buffer()
        force_reading = read_force()
                
        if(force_reading > target_force):
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos - rate)
        
        else:
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos + rate)




# give_force_with_initialization(0.02, 50, 9000)

# while True:
#     read_force()

def give_force(target_force, rate, portHandler, packetHandler, ser):
    while True:
        
        ser.reset_input_buffer()
        force_reading = read_force()

        if(force_reading > target_force):
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos - rate)

        else:
            curr_motor_pos = read_position(portHandler, packetHandler)
            write_position(portHandler, packetHandler, curr_motor_pos + rate)















# while True:
#     while ser.in_waiting < 32:
#         continue
#     if ser.in_waiting > 0:
#         try:
#             line = ser.readline().decode('utf-8').strip()
#             futek_reading = float(line)
#             force_reading = futek_reading * 111 / 1024
#             print(f"Force Reading: {force_reading}")
#         except ValueError:
#             print(f"Received invalid data: {line}")
#             futek_reading = 0