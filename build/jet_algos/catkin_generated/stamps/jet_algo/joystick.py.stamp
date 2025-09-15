#!/usr/bin/env python3.8

import rospy
from geometry_msgs.msg import Twist
import serial

def joystick_to_cmd_vel():
    # Initialize ROS node
    rospy.init_node('joystick_cmd_vel_publisher', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(200)  # 10 Hz

    # Open serial port
    port = '/dev/ttyUSB0'  # Replace with your Arduino's port
    baud_rate = 115200  # Set baud rate to 9600
    ser = serial.Serial(port, baud_rate, timeout=1)
    rospy.loginfo(f"Connected to Arduino on port: {port}")

    try:
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:
                # Read joystick data from Arduino
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                
                try:
                    # Split the data into x and y axes
                    x, y,_,_ = map(float, data.split(','))

                    # Map joystick values to Twist message
                    cmd = Twist()
                    cmd.linear.x = (-x +(1023/2))/500 # Map y-axis to forward/backward speed
                    cmd.angular.z = (y-(1023/2))/500  # Map x-axis to angular velocity

                    rospy.loginfo(f"Publishing: linear.x={cmd.linear.x}, angular.z={cmd.angular.z}")
                    pub.publish(cmd)  # Publish the Twist message

                except ValueError:
                    rospy.logwarn(f"Invalid data received: {data}")

            rate.sleep()
    except rospy.ROSInterruptException:
        pass
    finally:
        ser.close()
        rospy.loginfo("Serial connection closed.")

if __name__ == '__main__':
    joystick_to_cmd_vel()
