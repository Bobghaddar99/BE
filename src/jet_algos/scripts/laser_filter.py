#!/usr/bin/env python3.8

import rospy
import math
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
    rospy.loginfo("Received LIDAR scan data")
    
    # Create a new LaserScan message for publishing the filtered data
    filtered_scan = LaserScan()
    filtered_scan.header = msg.header
    filtered_scan.angle_min = msg.angle_min
    filtered_scan.angle_max = msg.angle_max
    filtered_scan.angle_increment = msg.angle_increment
    filtered_scan.time_increment = msg.time_increment
    filtered_scan.scan_time = msg.scan_time
    filtered_scan.range_min = msg.range_min
    filtered_scan.range_max = msg.range_max

    # Modify range readings: Set values < 80 meters to NaN
    filtered_scan.ranges = [
        r if r >= 0.8 else float('nan') for r in msg.ranges
    ]
    # Publish the filtered scan
    pub.publish(filtered_scan)

def main():
    global pub
    rospy.init_node('lidar_subscriber', anonymous=True)

    # Subscriber to raw LIDAR scan
    rospy.Subscriber("/scan_laser", LaserScan, scan_callback)

    # Publisher for filtered LIDAR scan
    pub = rospy.Publisher("/scan_filter", LaserScan, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    main()
