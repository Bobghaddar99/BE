import rospy
from std_msgs.msg import Float64

def set_joint_positions(joint_commands):
    rospy.init_node('batata', anonymous=True)
    
    # Create publishers for each joint
    publishers = {
        'fl_joint': rospy.Publisher('/cl_robot/fl_joint_position_controller/command', Float64, queue_size=10),
        'fr_joint': rospy.Publisher('/cl_robot/fr_joint_position_controller/command', Float64, queue_size=10),
        'bl_joint': rospy.Publisher('/cl_robot/bl_joint_position_controller/command', Float64, queue_size=10),
        'br_joint': rospy.Publisher('/cl_robot/br_joint_position_controller/command', Float64, queue_size=10)
    }
    
    rospy.sleep(1)  # Wait for the publishers to be ready
    
    # Publish commands to each joint
    for joint_name, position in joint_commands.items():
        publishers[joint_name].publish(position)
        rospy.loginfo(f"Publishing {position} to {joint_name}")

if __name__ == '__main__':
    try:
        rospy.init_node('batata', anonymous=True)
        
        while not rospy.is_shutdown():
            user_input = input("Enter direction (up/down/stairu/staird): ").strip().lower()
            
            if user_input == "up":
                commands = {
                    'fl_joint': 2.5,
                    'fr_joint': 2.5,
                    'bl_joint': -2.5,
                    'br_joint': -2.5
                }
            elif user_input == "down":
                commands = {
                    'fl_joint': 0,
                    'fr_joint': 0,
                    'bl_joint': -0,
                    'br_joint': -0
                }
            elif user_input == "stairu":
                commands = {
                    'fl_joint': -0.5,
                    'fr_joint': -0.5,
                    'bl_joint': 1,
                    'br_joint': 1
                }
            elif user_input == "staird":
                commands = {
                    'fl_joint': 1,
                    'fr_joint': 1,
                    'bl_joint': 0.5,
                    'br_joint': 0.5
                }

            else:
                print("Invalid input. Please enter 'up' or 'down'.")
                continue
            
            set_joint_positions(commands)
    
    except rospy.ROSInterruptException:
        pass

