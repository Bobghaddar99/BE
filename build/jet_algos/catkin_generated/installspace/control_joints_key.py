#!/usr/bin/env python2

import rospy
from std_msgs.msg import Float64
import sys
import tty
import termios

def get_key():
    """ Reads a single key press from the terminal """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    rospy.init_node('control_joints_keyboard', anonymous=True)

    # Create publishers for each joint
    publishers = {
        'fl_joint': rospy.Publisher('/cl_robot/fl_joint_position_controller/command', Float64, queue_size=10),
        'fr_joint': rospy.Publisher('/cl_robot/fr_joint_position_controller/command', Float64, queue_size=10),
        'bl_joint': rospy.Publisher('/cl_robot/bl_joint_position_controller/command', Float64, queue_size=10),
        'br_joint': rospy.Publisher('/cl_robot/br_joint_position_controller/command', Float64, queue_size=10)
    }

    rospy.sleep(1)  # Wait for the publishers to be ready

    print("Use keys to control the joints:")
    print("w: Increase FL joint")
    print("s: Decrease FL joint")
    print("e: Increase FR joint")
    print("d: Decrease FR joint")
    print("r: Increase BL joint")
    print("f: Decrease BL joint")
    print("t: Increase BR joint")
    print("g: Decrease BR joint")
    print("a: Increase all joints together")
    print("d: Set all joints to default position")
    print("q: Quit")

    # Initialize joint commands and default positions
    joint_commands = {
        'fl_joint': 0.0,
        'fr_joint': 0.0,
        'bl_joint': 0.0,
        'br_joint': 0.0
    }

    default_positions = {
        'fl_joint': 0.0,
        'fr_joint': 0.0,
        'bl_joint': 0.0,
        'br_joint': 0.0
    }

    increase_step = 0.1

    while not rospy.is_shutdown():
        key = get_key()
        
        if key == 'w':
            joint_commands['fl_joint'] += increase_step
        elif key == 's':
            joint_commands['fl_joint'] -= increase_step
        elif key == 'e':
            joint_commands['fr_joint'] += increase_step
        elif key == 'd':
            joint_commands['fr_joint'] -= increase_step
        elif key == 'r':
            joint_commands['bl_joint'] += increase_step
        elif key == 'f':
            joint_commands['bl_joint'] -= increase_step
        elif key == 't':
            joint_commands['br_joint'] += increase_step
        elif key == 'g':
            joint_commands['br_joint'] -= increase_step
        elif key == 'a':
            # Increase all joints together
            for joint_name in joint_commands:
                joint_commands[joint_name] += increase_step
        elif key == 'd':
            # Reset all joints to default positions
            joint_commands = default_positions.copy()
        elif key == 'q':
            break

        # Publish commands to each joint
        for joint_name, position in joint_commands.items():
            publishers[joint_name].publish(Float64(position))

if __name__ == '__main__':
    main()

