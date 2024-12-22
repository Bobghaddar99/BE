#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Path, OccupancyGrid
from geometry_msgs.msg import PoseStamped
from algos.srv import CheckGoal, CheckGoalResponse  # Replace `algos` with your actual package name

class GoalAnalyzer:
    def __init__(self):
        # Parameters
        self.robot_radius = rospy.get_param("~robot_radius", 0.1)  # Robot's radius
        self.safety_factor = rospy.get_param("~safety_factor", 1.1)  # Factor for safety clearance
        self.clearance_radius = self.robot_radius * self.safety_factor  # Clearance radius

        # Map data
        self.costmap = None
        self.map_resolution = None
        self.map_origin = None

        # Subscribers
        rospy.Subscriber("/move_base/NavfnROS/plan", Path, self.path_callback)  # Subscribe to the planned path
        rospy.Subscriber("/move_base/global_costmap/costmap", OccupancyGrid, self.costmap_callback)  # Subscribe to the costmap

        # Service server
        self.service = rospy.Service("check_goal", CheckGoal, self.handle_check_goal)

    def costmap_callback(self, costmap_msg):
        """Callback function to store the costmap."""
        self.costmap = costmap_msg
        self.map_resolution = costmap_msg.info.resolution
        self.map_origin = costmap_msg.info.origin
        rospy.logwarn("Received costmap")

    def path_callback(self, path_msg):
        """Callback function to handle the received path."""
        self.path = path_msg.poses

    def handle_check_goal(self, req):
        """Service handler to check if a goal is valid."""
        if not self.costmap:
            rospy.logwarn("Costmap not received yet!")
            return CheckGoalResponse(is_applicable=False)

        if not hasattr(self, 'path') or len(self.path) == 0:
            rospy.logwarn("No path received yet!")
            return CheckGoalResponse(is_applicable=False)  # Return false if no path is available

        x = req.goal.pose.position.x
        y = req.goal.pose.position.y
        is_valid = self.is_path_clear(x, y)

        rospy.loginfo(f"Goal ({x}, {y}) is {'valid' if is_valid else 'not valid'}.")
        return CheckGoalResponse(is_applicable=is_valid)

    def is_path_clear(self, x, y):
        """Check if the area around the given goal is free for the robot."""
        # Convert the world coordinates to grid coordinates
        grid_x = int((x - self.map_origin.position.x) / self.map_resolution)
        grid_y = int((y - self.map_origin.position.y) / self.map_resolution)

        # Calculate the clearance area in grid cells
        clearance_cells = int(self.clearance_radius / self.map_resolution)

        # Check if the area around the goal is free (i.e., no obstacles within the clearance radius)
        for i in range(-clearance_cells, clearance_cells + 1):
            for j in range(-clearance_cells, clearance_cells + 1):
                # Calculate the index of the grid cell
                idx = (grid_y + i) * self.costmap.info.width + (grid_x + j)
                if idx < 0 or idx >= len(self.costmap.data):
                    return False  # Out of bounds
                if self.costmap.data[idx] != 0 and self.costmap.data[idx] != -1:  # Check for obstacles (0 = free, other values = occupied)
                    return False  # If there's an obstacle, return False
        return True  # If the space is free, return True


if __name__ == "__main__":
    rospy.init_node("goal_analyzer")
    GoalAnalyzer()
    rospy.spin()
