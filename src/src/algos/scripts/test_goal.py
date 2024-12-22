#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from algos.srv import CheckGoal  # Replace `algos` with your actual package name

def check_goal_service_client(x, y):
    # Wait for the service to be available
    rospy.wait_for_service('check_goal')
    
    try:
        # Create a proxy for the 'check_goal' service
        check_goal = rospy.ServiceProxy('check_goal', CheckGoal)
        
        # Create a PoseStamped message for the goal
        goal_msg = PoseStamped()
        goal_msg.pose.position.x = x
        goal_msg.pose.position.y = y
        goal_msg.pose.position.z = 0  # Assuming 2D, z is 0
        goal_msg.pose.orientation.w = 1  # Assuming no rotation, set w=1

        # Send the request to the service
        response = check_goal(goal_msg)

        # Print the response
        if response.is_applicable:
            rospy.loginfo(f"Goal ({x}, {y}) is valid.")
        else:
            rospy.loginfo(f"Goal ({x}, {y}) is not valid.")
        
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")

if __name__ == "__main__":
    rospy.init_node('goal_checker_client')

    # Example goal position (x, y)
    goal_x = 2.0
    goal_y = 3.0

    # Call the service to check if the goal is valid
    check_goal_service_client(goal_x, goal_y)
