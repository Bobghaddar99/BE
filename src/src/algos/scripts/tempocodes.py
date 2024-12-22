#!/usr/bin/env python3

import rospy
import numpy as np
from sklearn.cluster import DBSCAN
from geometry_msgs.msg import Point, PoseStamped
from visualization_msgs.msg import Marker
import tf
import time
from std_msgs.msg import Float32

from std_msgs.msg import Bool
from geometry_msgs.msg import PoseArray
from dynamic_reconfigure.client import Client
status=  None 
class FrontierWeightedCalculator:
    def __init__(self):
        rospy.init_node('frontier_weighted_calculator', anonymous=True)
        self.dyn_client = Client("/move_base/global_costmap")
        # Subscribe to the frontier marker topic
        self.frontier_sub = rospy.Subscriber('/frontier_markers', Marker, self.frontier_callback)


        # Publisher for mean frontier markers and text markers for numbering
        self.mean_marker_pub = rospy.Publisher('/mean_frontier_markers', Marker, queue_size=10)
        self.number_marker_pub = rospy.Publisher('/frontier_number_markers', Marker, queue_size=10)

        # Publisher for navigation goals
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

        # Timer for controlling the publishing frequency
        self.timer = rospy.Timer(rospy.Duration(0.5), self.timer_callback)

        # Transformation listener to get the robot's position
        self.tf_listener = tf.TransformListener()

        self.frontier_points = []
        self.last_published_goal = None
        self.epsilon = 0.5

        # Parameters from the launch file or parameter server
        self.size_weight = rospy.get_param('~size_weight', 1.0)
        self.distance_weight = rospy.get_param('~distance_weight', 0.3)
        self.min_size = rospy.get_param('~min_size', 3)  # Default minimum size

        # Robot Stuck Handling
        self.robot_stuck_timeout = rospy.get_param('~stuck_time', 40.0)  # 2 minutes time for stuck
        self.robot_size = rospy.get_param('~robot_size', 2.0)
        self.robot_positions = []
        self.stuck_start_time = None
        self.goal_pre_tempo = []
        # Save initial robot position
        self.initial_position = None
        self.save_initial_position()

        # Subscribe to global map points
        ###rospy.Subscriber('/global_map_points', PoseArray, self.listen_global_map)

    def status_callback(self, msg):
        global status  # Use the global variable
        status = msg.data  # Update the global status based on the incoming message

    def save_initial_position(self):
        """Save the initial position of the robot."""
        self.initial_position = self.get_robot_position()
        if self.initial_position is not None:
            rospy.loginfo(f"Initial position saved: {self.initial_position}")

    def frontier_callback(self, msg):
        """Callback to receive frontier marker points."""
        if not msg.points:
            rospy.loginfo("No frontier points received.")
            return
        rospy.loginfo("frontier detected.")
        # Convert the received frontier points into a NumPy array
        self.frontier_points = np.array([[p.x, p.y] for p in msg.points])

    def timer_callback(self, event):
        """Timer callback to process and publish mean markers."""
        if not len(self.frontier_points):
            rospy.loginfo("No points to process.")
            return

        # Perform clustering on the received frontier points
        frontier_groups = self.group_frontiers(self.frontier_points)

        # Get the robot's current position
        robot_position = self.get_robot_position()

        if robot_position is None:
            rospy.logwarn("Couldn't get robot position!")
            return

        # Publish mean positions for the grouped frontiers
        self.publish_mean_markers(frontier_groups)

        # Publish numbering markers for the groups
        self.publish_number_markers(frontier_groups)

        # Select and publish the navigation goal using weighted criteria
        if True:
            self.check_robot_stuck(robot_position)
        
            if self.robot_is_stuck():
                rospy.logwarn("Robot is stuck, navigating to initial position!")
                self.navigate_to_initial_position()
            else:
                self.publish_weighted_nav_goal(frontier_groups, robot_position)

    def group_frontiers(self, frontier_points, eps=0.3, min_samples=1):
        """Group frontier points using DBSCAN clustering."""
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(frontier_points)
        labels = clustering.labels_

        # Extract groups of points based on cluster labels
        grouped_points = []
        for label in set(labels):
            if label == -1:  # Ignore noise points
                continue
            group = frontier_points[labels == label]
            grouped_points.append(group)

        return grouped_points

    def get_robot_position(self):
        """Continuously try to get the robot's current position in the map frame until successful."""
        retry_count = 0
        max_retries = 10  # Define maximum retries to avoid endless loop
        delay_between_retries = 0.5  # Delay in seconds between retries

        while retry_count < max_retries:
            try:
                (trans, rot) = self.tf_listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
                rospy.loginfo("Robot position successfully retrieved.")
                return np.array([trans[0], trans[1]])  # Return the robot's x, y position
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                retry_count += 1
                rospy.logwarn("Attempting to get robot position... (Attempt %d/%d)", retry_count, max_retries)
                rospy.sleep(delay_between_retries)  # Wait before retrying

        rospy.logwarn("Robot position could not be determined after multiple attempts.")
        return None


    def publish_mean_markers(self, frontier_groups):
        """Publish mean position markers for each group of frontiers."""
        clear_marker = Marker()
        clear_marker.header.frame_id = "map"
        clear_marker.header.stamp = rospy.Time.now()
        clear_marker.action = Marker.DELETEALL
        self.mean_marker_pub.publish(clear_marker)

        mean_marker = Marker()
        mean_marker.header.frame_id = "map"
        mean_marker.header.stamp = rospy.Time.now()
        mean_marker.ns = "mean_frontier"
        mean_marker.type = Marker.SPHERE_LIST
        mean_marker.action = Marker.ADD
        mean_marker.pose.orientation.w = 1.0

        mean_marker.scale.x = 0.3
        mean_marker.scale.y = 0.3
        mean_marker.scale.z = 0.3
        mean_marker.color.a = 1.0
        mean_marker.color.r = 1.0  # Red
        mean_marker.color.g = 1.0  # Green
        mean_marker.color.b = 0.0  # Blue

        for group in frontier_groups:
            mean_x = np.mean(group[:, 0])
            mean_y = np.mean(group[:, 1])

            mean_point = Point()
            mean_point.x = mean_x
            mean_point.y = mean_y
            mean_point.z = 0  # Flat surface

            mean_marker.points.append(mean_point)

        if mean_marker.points:
            self.mean_marker_pub.publish(mean_marker)
        else:
            rospy.loginfo("No mean markers to publish.")

    def publish_number_markers(self, frontier_groups):
        """Publish numbered markers for each group based on size."""
        clear_number_marker = Marker()
        clear_number_marker.header.frame_id = "map"
        clear_number_marker.header.stamp = rospy.Time.now()
        clear_number_marker.action = Marker.DELETEALL
        self.number_marker_pub.publish(clear_number_marker)

        for idx, group in enumerate(frontier_groups):
            mean_x = np.mean(group[:, 0])
            mean_y = np.mean(group[:, 1])

            number_marker = Marker()
            number_marker.header.frame_id = "map"
            number_marker.header.stamp = rospy.Time.now()
            number_marker.ns = "frontier_numbers"
            number_marker.id = idx
            number_marker.type = Marker.TEXT_VIEW_FACING
            number_marker.action = Marker.ADD

            number_marker.pose.position.x = mean_x
            number_marker.pose.position.y = mean_y
            number_marker.pose.position.z = 0.2  # Slightly above ground level

            number_marker.scale.z = 0.5  # Height of the text
            number_marker.color.a = 1.0  # Alpha
            number_marker.color.r = 1.0  # Red
            number_marker.color.g = 1.0  # Green
            number_marker.color.b = 1.0  # White

            number_marker.text = str(idx)

            # Publish the number marker
            self.number_marker_pub.publish(number_marker)

    def check_robot_stuck(self, robot_position):
        print(self.initial_position)
        """Check if the robot is stuck based on its position history."""
        if self.initial_position is not None:
            self.robot_positions.append(robot_position)
            rospy.loginfo("appending position")
            if len(self.robot_positions) > 10:  # Keep only the last 10 positions
                self.robot_positions.pop(0)

    def robot_is_stuck(self):
        """Determine if the robot has been stuck for 2 minutes in a small square."""
        if len(self.robot_positions) < 2:
            return False

        # Calculate the bounding box of the robot's recent positions
        recent_positions = np.array(self.robot_positions)
        min_x, min_y = np.min(recent_positions, axis=0)
        max_x, max_y = np.max(recent_positions, axis=0)

        box_size = max(max_x - min_x, max_y - min_y)

        # Check if the robot has been within a square of size 2x robot_size
        if box_size <= 2 * self.robot_size:
            if self.stuck_start_time is None:
                self.stuck_start_time = time.time()  # Start the timer
            elif time.time() - self.stuck_start_time > self.robot_stuck_timeout:
                rospy.loginfo("time passed")
                self.stuck_start_time = None
                return True
        else:
            self.stuck_start_time = None  # Reset if moved
            rospy.loginfo("robot  oved apperntaly")

        return False

    def navigate_to_initial_position(self):
        """Navigate the robot back to its initial position and publish the distance."""
        global status
        if self.initial_position is not None:
            # Create the goal pose using the initial position
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = "map"
            goal_pose.header.stamp = rospy.Time.now()
            goal_pose.pose.position.x = self.initial_position[0]
            goal_pose.pose.position.y = self.initial_position[1]
            goal_pose.pose.position.z = 0.0  # Flat surface
            goal_pose.pose.orientation.w = 1.0  # No rotation

         # Update status
            status = False
            print(status)

            # Publish the goal pose
            self.goal_pub.publish(goal_pose)

            # Update the last published goal to the current goal pose
            self.last_published_goal = (goal_pose.pose.position.x, goal_pose.pose.position.y)

            # Calculate the distance to the initial position
            robot_position = self.get_robot_position()
            if robot_position is not None:
                # Calculate the difference in x and y coordinates
                dx = robot_position[0] - self.initial_position[0]
                dy = robot_position[1] - self.initial_position[1]

                # Assign distance based on which is greater
                if abs(dx) > abs(dy):
                    distance = abs(dx)
                else:
                    distance = abs(dy)
             # Create a message to publish the distance
                distance_msg = Float32()
                distance_msg.data = distance
                self.dyn_client.update_configuration({"width": distance + 10})
                self.dyn_client.update_configuration({"height": distance + 10})
                # Publish the distance to a topic
                



    def listen_global_map(self, msg):
        """Callback to process global map points."""
        global_map_points = msg.posess

    def publish_weighted_nav_goal(self, frontier_groups, robot_position):
        global status
        """Publish the navigation goal based on weighted criteria."""
        best_goal = None
        best_weight = float('-inf')

        for group in frontier_groups:
            mean_x = np.mean(group[:, 0])
            mean_y = np.mean(group[:, 1])
            dx = mean_x - robot_position[0]
            dy = mean_y - robot_position[1]
            if abs(dx) > abs(dy):
                 distance_to_robot = abs(dx)
            else:
                 distance_to_robot = abs(dy)

            # Calculate weight based on size and distance
            weight = len(group) * self.size_weight - distance_to_robot * self.distance_weight

            if weight > best_weight:
                best_weight = weight
                best_goal = (mean_x, mean_y)

        if best_goal is not None:
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = "map"
            goal_pose.header.stamp = rospy.Time.now()
            goal_pose.pose.position.x = best_goal[0]
            goal_pose.pose.position.y = best_goal[1]
            goal_pose.pose.position.z = 0.0  # Flat surface
            goal_pose.pose.orientation.w = 1.0  # No rotation
            distance_to_robot = int(distance_to_robot)
            self.dyn_client.update_configuration({"width": distance_to_robot + 50})
            self.dyn_client.update_configuration({"height": distance_to_robot + 50})
            if self.last_published_goal != best_goal:  # Avoid redundant publications
                self.goal_pub.publish(goal_pose)
                self.last_published_goal = best_goal
                status = None

if __name__ == '__main__':
    try:
        FrontierWeightedCalculator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
