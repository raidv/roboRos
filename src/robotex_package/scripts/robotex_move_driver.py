#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

import serial
import time

# Function that communicates with hardware via serial
def sendSerial(command):
    if ser.isOpen:
        ser.write(command + '\r\n')

# Function that sends the command to hardware
def sendCommand(m0, m1, m2):
    return sendSerial('a' + str(a) + 'b' + str(b) + 'c' + str(c)) 

def formatVelocity(data):
    maxV = 0.2
    steps = 255 
    unitV = steps/maxV # value for velocity 1 m/s
    motors = [0, 0, 0]

    motors[0] = data.linear.x * unitV + data.linear.y * unitV * 0.866 * (-1)
    motors[1] = data.linear.x * unitV * (-1) + data.linear.y * unitV * 0.866
    motors[2] = data.linear.x * unitV * 0 + data.linear.y * unitV * (-1)
    return motors

# Function to work with cmd_vel data
def callback(data):
    motors = [0, 0, 0]
    # TODO: work with data.data and output the correct thing
    motors = formatVelocity(data)
    rospy.loginfo(rospy.get_caller_id() + "I heard \n %s \n %s \n", data.linear, data.angular)
    print ("I calculated: \n m0 = " + str(motors[0]) + "\n m1 = "+ str(motors[1]) + " \n m2 = " + str( motors[2]))
    # Send correctly calculated command       
    #sendCommand(mootors[0],mootors[1], mootors[2])
    

# Function that subscribes to topics
def listener():

    # Initialize node
    rospy.init_node('robotex_move_driver', anonymous=True)

    # The topic to which the node subscribes
    rospy.Subscriber("turtlebot_teleop/cmd_vel", Twist, callback)

    # Keeps python from exiting
    rospy.spin()



# Open serial connection with Motor Controllers
"""port = "/dev/ttyACM0"
baud = 9600
ser = serial.Serial(port, baud, serial.EIGHTBITS, timeout=0)
"""
if __name__ == '__main__':
    listener()
