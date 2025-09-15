#!/usr/bin/env python2
import rospy

from std_msgs.msg import Float32
from geometry_msgs.msg import Pose, Twist, TransformStamped
from nav_msgs.msg import Odometry
import tf
import tf2_ros
import math

class OdometryPublisher:
    def __init__(self):
        rospy.init_node("odometry_publisher_node", anonymous=True)

        # Create a publisher for odometry
        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)

        # Create a transform broadcaster
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()

        # Variables for storing encoder data
        self.left_encoder_pos = 0
        self.right_encoder_pos = 0
        self.last_theta = 0
        # Wheel parameters
        self.wheel_radius = 0.08255  # meters
        self.wheel_sep = 0.65  # meters (distance between the wheels)

        # Initial encoder positions for reference
        self.initial_left_encoder_pos = 0
        self.initial_right_encoder_pos = 0

        # Previous encoder positions (for calculating velocity)
        self.prev_left_encoder_pos = 0
        self.prev_right_encoder_pos = 0

        self.x = 0
        self.y = 0
        self.theta = 0

        # Subscribe to encoder data
        rospy.Subscriber("/left_encoder", Float32, self.left_encoder_callback)
        rospy.Subscriber("/right_encoder", Float32, self.right_encoder_callback)

        # Set up the loop rate
        self.rate = rospy.Rate(200)  # 10 Hz

    def left_encoder_callback(self, msg):
        """Callback for the left encoder."""
        self.left_encoder_pos = msg.data

    def right_encoder_callback(self, msg):
        """Callback for the right encoder."""
        self.right_encoder_pos = msg.data

    def compute_odometry(self):
        """Compute odometry from encoder data."""
        # Initialize the initial positions if they haven't been set yet
        if self.initial_left_encoder_pos == 0 and self.initial_right_encoder_pos == 0:
            self.initial_left_encoder_pos = self.left_encoder_pos
            self.initial_right_encoder_pos = self.right_encoder_pos

        # Subtract the initial encoder positions to get the relative displacement
        delta_left = self.left_encoder_pos - self.initial_left_encoder_pos
        delta_right = self.right_encoder_pos - self.initial_right_encoder_pos
        # Compute the linear and angular velocities
        delta_distance = (delta_left + delta_right) / 2.0
        delta_theta = (delta_right - delta_left) / self.wheel_sep
        #print("distance" , delta_distance)
        #print("angle", delta_theta)
        # Update the robot's position (x, y, theta)
        self.x = delta_distance * math.cos(self.theta)
        self.y = delta_distance * math.sin(self.theta)

        self.theta = delta_theta
        

        # Update the previous encoder positions
        self.prev_left_encoder_pos = self.left_encoder_pos
        self.prev_right_encoder_pos = self.right_encoder_pos

    def publish_odometry(self):
        """Publish the odometry message."""
        # Create the odometry message
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"

        # Set the position
        odom.pose.pose = Pose()
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        quat = tf.transformations.quaternion_from_euler(0, 0, self.theta)
	odom.pose.pose.orientation.x = quat[0]
	odom.pose.pose.orientation.y = quat[1]
	odom.pose.pose.orientation.z = quat[2]
	odom.pose.pose.orientation.w = quat[3]
        # Set the velocity (not used, but you can fill it in if needed)
        odom.child_frame_id = "base_link"
        odom.twist.twist = Twist()

        # Publish the odometry message
        self.odom_pub.publish(odom)

        # Broadcast the transform
        t = TransformStamped()
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        # Correct way to assign quaternion values
        quaternion = tf.transformations.quaternion_from_euler(0, 0, self.theta)
        t.transform.rotation.x = quaternion[0]
        t.transform.rotation.y = quaternion[1]
        t.transform.rotation.z = quaternion[2]
        t.transform.rotation.w = quaternion[3]
        
        # Send the transform
        self.tf_broadcaster.sendTransform(t)

    def run(self):
        """Main loop to compute and publish odometry."""
        while not rospy.is_shutdown():
            # Compute the odometry
            self.compute_odometry()

            # Publish the odometry and the transform
            self.publish_odometry()

            # Sleep for a while to maintain the loop rate
            self.rate.sleep()

if __name__ == "__main__":
    # Create the OdometryPublisher object
    odom_publisher = OdometryPublisher()

    # Start publishing odometry
    odom_publisher.run()
