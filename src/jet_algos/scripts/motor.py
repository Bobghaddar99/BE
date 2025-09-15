#!/usr/bin/env python3
import time
import rospy
import odrive
from odrive.enums import *
from std_msgs.msg import Float32
import math
import geometry_msgs.msg
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import Header
from nav_msgs.msg import Odometry

class ODriveROSNode:
    def __init__(self):
        rospy.init_node("odrive_node", anonymous=True)

        self.pub_left_ec = rospy.Publisher('/left_encoder', Float32, queue_size=10)
        self.pub_right_ec = rospy.Publisher("/right_encoder", Float32, queue_size=10)
        # Connect to ODrive
        rospy.loginfo("Searching for ODrive...")
        self.odrv0 = odrive.find_any()
        rospy.loginfo("ODrive found!")
        self.theta = 0
        
        # Ensure encoder is ready
        if not self.odrv0.axis0.encoder.is_ready:
            rospy.logwarn("Axis 0 encoder is not ready! Run encoder calibration first.")
        else:
            rospy.loginfo("Axis encoder is ready.")
        
        if not self.odrv0.axis1.encoder.is_ready:
            rospy.logwarn("Axis 1 encoder is not ready! Run encoder calibration first.")
        else:
            rospy.loginfo("Axis encoder is ready.")

        # Set motor to closed-loop control mode
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        while self.odrv0.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            rospy.loginfo("Waiting for Axis 0 to enter closed-loop control...")
            time.sleep(1)
        while self.odrv0.axis1.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
            rospy.loginfo("Waiting for Axis 1 to enter closed-loop control...")
            time.sleep(1)
        rospy.loginfo("Axis 1 is now in closed-loop control mode.")
        
        self.last_x = 0 
        self.last_y = 0
        self.last_theta = 0
        
        # Create a subscriber for velocity commands
        self.vel_subscriber = rospy.Subscriber("/cmd_vel", Twist, self.set_velocity)

    def set_velocity(self, msg):
        """Set motor velocities based on velocity commands."""
        wheel_radius = 3  # in inches
        wheel_sep = 65 * 0.01  # in meters
        x = msg.linear.x
        y = msg.angular.z
        v_left = -1 * (x - y * (wheel_sep / 2))
        v_right = (x + y * (wheel_sep / 2))
        wheel_circum = 2 * 3.14 * 2.54 * wheel_radius * 0.01  # in meters
        v_left = v_left / wheel_circum
        v_right = v_right / wheel_circum

        # Set the motor velocities
        self.odrv0.axis0.controller.input_vel = v_right  # Set the motor velocity
        self.odrv0.axis1.controller.input_vel = v_left   # Set the motor velocity

    def encoders(self):
        """Publish encoder positions to topics."""
        encoder_position_0 = self.odrv0.axis0.encoder.pos_estimate
        encoder_position_1 = -1*self.odrv0.axis1.encoder.pos_estimate
        self.pub_left_ec.publish(encoder_position_1)
        self.pub_right_ec.publish(encoder_position_0)

if __name__ == "__main__":
    node = ODriveROSNode()
    
    # Define a rate for publishing encoder data
    rate = rospy.Rate(200)  # 10 Hz
    
    while not rospy.is_shutdown():
        node.encoders()  # Continuously publish encoder data
        rate.sleep()  # Maintain the loop rate
        
    rospy.spin()  # Keeps the node running
