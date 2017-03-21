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
    maxV = 0.2 # maximum linear velocity
    radius = 0.15 
    maxRV = maxV/radius # angular velocity that cossesponds to the steps
    steps = 255 # maximum value to send to motors
    unitV = steps/maxV # value for velocity 1 m/s
    unitRV = steps/maxRV # value for angular velocity 1 rad/s
''' 
	Don't have to provide maximum values actually - it would be easier to check if
	sent value is too big or not.
	But it is important that the maxV and steps values correspond to each other
	eg. if you send motor dac value 255, it rotates at a velocity of 0.2 m/s
'''

    motors = [0, 0, 0]

    motors[0] += data.linear.x * unitV
    motors[1] += data.linear.x * unitV * (-1)
    motors[2] += data.linear.x * unitV * 0 

    motors[0] += data.linear.y * unitV * 0.866 * (-1)
    motors[1] += data.linear.y * unitV * 0.866
    motors[2] += data.linear.y * unitV * (-1)

    motors[0] += data.angular.z * unitRV
    motors[1] += data.angular.z * unitRV
    motors[2] += data.angular.z * unitRV

    return motors

# Function to work with cmd_vel data
def callback(data):
    motors = [0, 0, 0]
    motors = formatVelocity(data)
    rospy.loginfo(rospy.get_caller_id() + "I heard \n %s \n %s \n", data.linear, data.angular)

    print ("I calculated: \n m0 = " + str(motors[0]) + "\n m1 = "+ str(motors[1]) + " \n m2 = " + str( motors[2]))
    # Send correctly calculated command       
    #sendCommand(motors[0],motors[1], motors[2])
    

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
