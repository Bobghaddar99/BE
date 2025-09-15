#!/usr/bin/env python3

import rospy
import numpy as np
from sklearn.cluster import DBSCAN
from geometry_msgs.msg import Point, PoseStamped, Twist
from visualization_msgs.msg import Marker
import tf
from algos.srv import CheckGoal, CheckGoalResponse # Replace `algos` with your actual package name
import time
from std_msgs.msg import Float32
from dynamic_reconfigure.client import Client

class FrontierWeightedCalculator:
    def __init__(self):
        # Initialize ROS node
        rospy.init_node('frontier_weighted_calculator', anonymous=True)
        rospy.wait_for_service('check_goal')
    
        try:
            # Create a proxy for the 'check_goal' service
            self.check_goal_service = rospy.ServiceProxy('check_goal', CheckGoal)
        except rospy.ServiceException as e:
            rospy.logerr(f"Failed to connect to service: {e}")
            rospy.signal_shutdown("Service connection failed")
        
        # Dynamic reconfiguration client for costmap
        self.dyn_client = Client("/move_base/global_costmap")
        
        # ROS Communication Setup
        self._setup_communication()
        
        # Exploration Parameters
        self._load_parameters()
        
        # Save initial robot position for stuck recovery
        self.save_initial_position()

    def _setup_communication(self):
        """Setup ROS publishers and subscribers"""
        # Frontier detection subscriber
        self.frontier_sub = rospy.Subscriber(
            '/frontier_markers', 
            Marker, 
            self.frontier_callback
        )

        # Visualization publishers
        self.mean_marker_pub = rospy.Publisher(
            '/mean_frontier_markers', 
            Marker, 
            queue_size=10
        )
        self.number_marker_pub = rospy.Publisher(
            '/frontier_number_markers', 
            Marker, 
            queue_size=10
        )

        # Navigation goal publisher
        self.goal_pub = rospy.Publisher(
            '/move_base_simple/goal', 
            PoseStamped, 
            queue_size=10
        )

        # cmd_vel publisher for stuck recovery
        self.cmd_vel_pub = rospy.Publisher(
            '/cmd_vel', 
            Twist, 
            queue_size=10
        )

        # Processing timer
        self.timer = rospy.Timer(rospy.Duration(0.5), self.timer_callback)

        # Transform listener for robot positioning
        self.tf_listener = tf.TransformListener()

    def _load_parameters(self):
        """Load configurable parameters"""
        # Exploration strategy weights
        self.size_weight = rospy.get_param('~size_weight', 2.0)
        self.distance_weight = rospy.get_param('~distance_weight', 0)
        
        # Minimum cluster size
        self.min_size = rospy.get_param('~min_size', 3)
        
        # Stuck detection parameters
        self.robot_stuck_timeout = rospy.get_param('~stuck_time', 100.0)
        self.robot_size = rospy.get_param('~robot_size', 1.5)

        # Initialization of state variables
        self.frontier_points = []
        self.last_published_goal = None
        self.epsilon = 0.5
        self.robot_positions = []
        self.stuck_start_time = None
        self.initial_position = None

    def save_initial_position(self):
        """Save the initial position of the robot"""
        self.initial_position = self.get_robot_position()
        if self.initial_position is not None:
            rospy.loginfo(f"Initial position saved: {self.initial_position}")

    def frontier_callback(self, msg):
        """Process incoming frontier marker points"""
        if not msg.points:
            rospy.loginfo("No frontier points received.")
            return
        rospy.loginfo("frontier points received.")
        # Convert frontier points to numpy array
        self.frontier_points = np.array([[p.x, p.y] for p in msg.points])

    def timer_callback(self, event):
        """Main processing callback for frontier exploration"""
        if not len(self.frontier_points):
            rospy.loginfo("No points to process.")
            return

        # Cluster frontier points
        frontier_groups = self.group_frontiers(self.frontier_points)

        # Get current robot position
        robot_position = self.get_robot_position()
        if robot_position is None:
            rospy.logwarn("Couldn't get robot position!")
            return

        # Publish visualization markers
        self.publish_mean_markers(frontier_groups)
        self.publish_number_markers(frontier_groups)

        # Check if robot is stuck
        self.check_robot_stuck(robot_position)
        
        if self.robot_is_stuck():
            rospy.logwarn("Robot is stuck, attempting recovery!")
        else:
            # Select and publish navigation goal
            self.publish_weighted_nav_goal(frontier_groups, robot_position)

    def group_frontiers(self, frontier_points, eps=0.1, min_samples=4):
        """Cluster frontier points using DBSCAN"""
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(frontier_points)
        labels = clustering.labels_

        # Extract groups of points based on cluster labels
        grouped_points = [
            frontier_points[labels == label] 
            for label in set(labels) if label != -1
        ]

        return grouped_points

    def get_robot_position(self):
        """Retrieve robot's current position with multiple retry attempts"""
        max_retries = 10
        retry_count = 0
        delay_between_retries = 0.5

        while retry_count < max_retries:
            try:
                (trans, rot) = self.tf_listener.lookupTransform(
                    'map', 'base_footprint', rospy.Time(0)
                )
                return np.array([trans[0], trans[1]])
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                retry_count += 1
                rospy.logwarn(f"Position retrieval attempt {retry_count}/{max_retries}")
                rospy.sleep(delay_between_retries)

        rospy.logwarn("Robot position could not be determined")
        return None

    def publish_mean_markers(self, frontier_groups):
        """Publish mean position markers for frontier groups"""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.type = Marker.POINTS
        marker.action = Marker.ADD
        marker.scale.x = 0.3
        marker.scale.y = 0.3
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 0.0

        for group in frontier_groups:
            mean_point = Point()
            mean_point.x = np.mean(group[:, 0])
            mean_point.y = np.mean(group[:, 1])
            marker.points.append(mean_point)

        self.mean_marker_pub.publish(marker)

    def publish_number_markers(self, frontier_groups):
        """Publish numbered markers for frontier groups"""
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rospy.Time.now()
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD
        marker.scale.z = 0.4
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0

        for i, group in enumerate(frontier_groups):
            marker_text = Marker()
            marker_text.header = marker.header
            marker_text.type = Marker.TEXT_VIEW_FACING
            marker_text.action = Marker.ADD
            marker_text.scale.z = 0.4
            marker_text.color = marker.color
            marker_text.text = str(i)
            marker_text.pose.position.x = np.mean(group[:, 0])
            marker_text.pose.position.y = np.mean(group[:, 1])
            marker_text.pose.position.z = 0.5
            self.number_marker_pub.publish(marker_text)

    def check_robot_stuck(self, robot_position):
        """Track robot positions for stuck detection"""
        self.robot_positions.append(robot_position)
        
        # Limit position history
        if len(self.robot_positions) > 10:
            self.robot_positions.pop(0)

    def robot_is_stuck(self):
        """
        Advanced stuck detection and recovery method
        1. First attempt standard stuck recovery (navigate to initial position)
        2. If not resolved after 20 seconds, attempt forced movement
        """
        if len(self.robot_positions) < 2:
            return False

        # Calculate bounding box of recent positions
        recent_positions = np.array(self.robot_positions)
        min_x, min_y = np.min(recent_positions, axis=0)
        max_x, max_y = np.max(recent_positions, axis=0)

        # Check movement range
        box_size = max(max_x - min_x, max_y - min_y)

        # Stuck detection logic
        if box_size <= 2 * self.robot_size:
            if self.stuck_start_time is None:
                self.stuck_start_time = time.time()
            elif time.time() - self.stuck_start_time > self.robot_stuck_timeout:
                # First, attempt standard stuck recovery
                self.navigate_to_initial_position()
                
                # Wait and check if robot moves after standard recovery
                start_wait_time = time.time()
                while time.time() - start_wait_time < 20:
                    # Check if robot has moved
                    current_position = self.get_robot_position()
                    if current_position is not None:
                        movement_distance = np.linalg.norm(current_position - recent_positions[0])
                        if movement_distance > 0.5 * self.robot_size:
                            # Robot successfully moved
                            self.stuck_start_time = None
                            return False
                    
                    rospy.sleep(1)  # Check every second
                
                # If robot still stuck after 20 seconds, force movement
                # Movement sequences: back, forward, left, right
                movements = [
                    ((-1 * self.robot_size, 0),   # Backward
                     "Moving robot backward"),
                    ((1 * self.robot_size, 0),    # Forward
                     "Moving robot forward"),
                    ((0, 1 * self.robot_size),    # Left rotation
                     "Rotating robot left"),
                    ((0, -1 * self.robot_size),   # Right rotation
                     "Rotating robot right")
                ]
                
                for (linear, angular), description in movements:
                    rospy.logwarn(description)
                    twist = Twist()
                    twist.linear.x = linear
                    twist.angular.z = angular
                    
                    # Send movement for 2 seconds
                    start_movement_time = time.time()
                    while time.time() - start_movement_time < 2:
                        self.cmd_vel_pub.publish(twist)
                        rospy.sleep(0.1)
                    
                    # Check if robot moved
                    current_position = self.get_robot_position()
                    if current_position is not None:
                        movement_distance = np.linalg.norm(current_position - recent_positions[0])
                        if movement_distance > 0.5 * self.robot_size:
                            rospy.loginfo(f"Successfully unstuck robot with {description}")
                            self.stuck_start_time = None
                            return False
                
                # If all movement attempts fail
                rospy.logerr("Failed to unstick robot after multiple attempts")
                self.stuck_start_time = None
        else:
            self.stuck_start_time = None

        return False

    def navigate_to_initial_position(self):
        """Navigate robot back to its initial position"""
        if self.initial_position is not None:
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = "map"
            goal_pose.header.stamp = rospy.Time.now()
            goal_pose.pose.position.x = self.initial_position[0]
            goal_pose.pose.position.y = self.initial_position[1]
            goal_pose.pose.orientation.w = 1.0

            # Publish goal and update costmap
            self.goal_pub.publish(goal_pose)
            
            # Dynamic costmap adjustment
            robot_position = self.get_robot_position()
            if robot_position is not None:
                distance = np.linalg.norm(robot_position - self.initial_position)
                self.dyn_client.update_configuration({
                    "width": max(int(distance) + 10, 20),
                    "height": max(int(distance) + 10, 20)
                })

    def publish_weighted_nav_goal(self, frontier_groups, robot_position):
        """Select and publish navigation goal based on weighted criteria"""
        best_goal = None
        best_weight = float('-inf')

        # Select best frontier group
        for group in frontier_groups:
            mean_x = np.mean(group[:, 0])
            mean_y = np.mean(group[:, 1])
            
            # Calculate distance 
            dx = mean_x - robot_position[0]
            dy = mean_y - robot_position[1]
            distance_to_robot = max(abs(dx), abs(dy))

            # Calculate weighted score
            weight = len(group) * self.size_weight - distance_to_robot * self.distance_weight

            # Update best goal
            if weight > best_weight:
                best_weight = weight
                best_goal = (mean_x, mean_y)

        # Publish selected goal
        if best_goal is not None:
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = "map"
            goal_pose.header.stamp = rospy.Time.now()
            goal_pose.pose.position.x = best_goal[0]
            goal_pose.pose.position.y = best_goal[1]
            goal_pose.pose.orientation.w = 1.0

            # Dynamic costmap adjustment
            self.dyn_client.update_configuration({
                "width": max(int(distance_to_robot) + 50, 20),
                "height": max(int(distance_to_robot) + 50, 20)
            })
            
            # Publish goal if different from last
            if self.last_published_goal != best_goal : 
                self.goal_pub.publish(goal_pose)
                self.last_published_goal = best_goal
                response = self.check_goal_service(goal_pose)
                # if(response  == False ) :
                #  pos = get_robot_position(self)
                #  goal_pose.pose.position.x = trans[0]
                #  goal_pose.pose.position.y = trans[1]
                #  goal_pose.pose.orientation.w = 1.0


                
def main():
    try:
        FrontierWeightedCalculator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()
