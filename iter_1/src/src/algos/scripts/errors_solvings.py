#!/usr/bin/env python3

import rospy
from move_base_msgs.msg import MoveBaseActionResult
from std_msgs.msg import Bool  # Import Bool message type

status = None  # Define status globally to be accessible by multiple functions

def process_goal_status():
    """Function to subscribe to /move_base/result and handle status."""

    # Initialize the ROS node (needed for any ROS functionality)
    rospy.init_node('goal_status_listener', anonymous=True)

    # Define a publisher for the goal status
    status_pub = rospy.Publisher('/goal_status', Bool, queue_size=10)

    def status_callback(msg):
        """Callback function to handle received MoveBaseActionResult messages."""
        global status  # Indicate that we're using the global status variable

        if msg.status.status == 4:  # Goal was aborted
            rospy.loginfo("Goal was aborted, sending false.")
            handle_goal_status(False)  # Send false if the goal was aborted
        else:
            rospy.loginfo("Goal is active, sending true.")
            handle_goal_status(True)   # Send true otherwise

    def handle_goal_status(goal_status):
        """Process the boolean goal status and update global status."""
        global status  # Modify the global variable status
        status = goal_status
        # Publish the goal status as a Bool message
        status_pub.publish(Bool(status))  # Publish True or False as Bool
        if status:
            rospy.loginfo("Goal is active.")
        else:
            rospy.loginfo("Goal was aborted.")

    # Subscribe to the /move_base/result topic
    rospy.Subscriber('/move_base/result', MoveBaseActionResult, status_callback)

    # Keep the function running to listen for messages
    rospy.spin()

# Ensure this script is run directly
if __name__ == "__main__":
    process_goal_status()  # Call the main function
