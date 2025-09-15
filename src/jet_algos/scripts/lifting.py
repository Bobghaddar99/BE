#!/usr/bin/env python3.8
import rospy
from pyfirmata import Arduino, util
import time
from geometry_msgs.msg import Twist
import serial

board = Arduino('/dev/arduino1')  
# Define pin mappings
RPWM_Output = 10  # Connect to IBT-2 RPWM pin
LPWM_Output = 11  # Connect to IBT-2 LPWM pin
L_en = 9          # Connect to IBT-2 L_EN pin
R_en = 8          # Connect to IBT-2 R_EN pin
limit = 6
clutch  =0

# Set up pins
it = util.Iterator(board)
it.start()
board.digital[RPWM_Output].mode = 1  # Output
board.digital[LPWM_Output].mode = 1  # Output
board.digital[L_en].mode = 1         # Output
board.digital[R_en].mode = 1         # Output
board.digital[limit].mode = 0        # Input

# Open serial port
port = '/dev/arduino2'  # Replace with your Arduino's port
baud_rate = 115200  # Set baud rate to 9600
ser = serial.Serial(port, baud_rate)

def motor_control():
    rospy.init_node('motor_control_node', anonymous=True)
    rate = rospy.Rate(200)  # 200 Hz loop

    try:
        clutch = 0
        while not rospy.is_shutdown():           
            # Get the current value of the ROS parameter
            motor_param_up = rospy.get_param('/lift_up', 0)
            motor_param_down = rospy.get_param('/lift_down', 0)
            pressed = board.digital[limit].read()
            data = ser.readline().decode('utf-8', errors='ignore').strip()

            if True:  # Ensure exactly 4 values are present
                try:
                    x, y, up_b, off_b = map(float, data.split(','))
                except ValueError:
                    rospy.logwarn(f"Invalid data received: {data}")
                    x, y, up_b, off_b = 511.5, 511.5, 1, 1  # Default values in case of error
            else:
                rospy.logwarn(f"Incomplete or invalid serial data: {data}")
                x, y, up_b, off_b = 511.5, 511.5, 1, 1  # Default values

            rospy.loginfo(pressed)
            if  motor_param_up == 1 or up_b == 0:
                # Set RPWM to HIGH, LPWM to LOW
                board.digital[RPWM_Output].write(1)
                board.digital[LPWM_Output].write(0)
                board.digital[L_en].write(1)
                board.digital[R_en].write(1)
                rospy.loginfo("Motor running: RPWM = HIGH, LPWM = LOW")
            elif (motor_param_down == 1 and pressed == True and clutch == 1) or (off_b == 0 and pressed == True and clutch == 1):
                # Set LPWM to HIGH, RPWM to LOW
                board.digital[RPWM_Output].write(0)
                board.digital[LPWM_Output].write(1)
                board.digital[L_en].write(1)
       
                board.digital[R_en].write(1)
                rospy.loginfo("Motor running: LPWM = HIGH, RPWM = LOW")
            elif motor_param_down == 0 and up_b == 1 and off_b == 1 and motor_param_up == 0:
                # Disable both enables
                board.digital[RPWM_Output].write(0)
                board.digital[LPWM_Output].write(0)
                board.digital[L_en].write(0)
                board.digital[R_en].write(0)
                clutch = 1
                joystick_to_cmd_vel(x, y)  # Only publish valid joystick data
                rospy.loginfo("Motor disabled: Enables = LOW")
            
            if pressed == False:
                board.digital[RPWM_Output].write(0)
                board.digital[LPWM_Output].write(0)
                board.digital[L_en].write(0)
                board.digital[R_en].write(0)
                clutch = 0

            rate.sleep()

    except rospy.ROSInterruptException:
        rospy.loginfo("Exiting...")
        ser.close()
        board.exit()

def joystick_to_cmd_vel(x, y):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    if ser.in_waiting > 0:
        try:
            # Map joystick values to Twist message
            cmd = Twist()
            cmd.linear.x = (-x + (1023/2)) / 500  # Map y-axis to forward/backward speed
            cmd.angular.z = (y - (1023/2)) / 500  # Map x-axis to angular velocity

            rospy.loginfo(f"Publishing: linear.x={cmd.linear.x}, angular.z={cmd.angular.z}")
            pub.publish(cmd)  # Publish the Twist message
        except ValueError:
            rospy.logwarn("Invalid joystick data received.")

if __name__ == '__main__':
    motor_control()

