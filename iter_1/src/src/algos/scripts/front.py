#!/usr/bin/env python3

import rospy
import numpy as np
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker

class FrontierGenerator:
    def __init__(self):
        rospy.init_node('frontier_generator', anonymous=True)

        # Subscriber to the map topic
        self.map_sub = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        
        # Publisher for frontier markers
        self.marker_pub = rospy.Publisher('/frontier_markers', Marker, queue_size=10)

        self.cost_map = None
        self.resolution = None
        self.origin_x = None
        self.origin_y = None

        # Marker ID for clearing old markers
        self.marker_id = 0

    def map_callback(self, msg):
        # Convert OccupancyGrid data to a 2D numpy array
        self.cost_map = np.array(msg.data).reshape((msg.info.height, msg.info.width))
        self.resolution = msg.info.resolution
        self.origin_x = msg.info.origin.position.x
        self.origin_y = msg.info.origin.position.y
        self.generate_frontiers()

    def generate_frontiers(self):
        if self.cost_map is None:
            return

        height, width = self.cost_map.shape
        frontiers = []

        for y in range(height):
            for x in range(width):
                # Check if the cell is free (cost 0) and has unknown neighbors
                if self.cost_map[y, x] == 0:  # Free cell
                    if self.has_unknown_neighbors(x, y):
                        frontiers.append((x, y))  # Mark this as a frontier

        # Publish markers for the identified frontiers
        self.publish_markers(frontiers)

    def has_unknown_neighbors(self, x, y):
        # Define neighbor offsets (adjacent cells)
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Up, Down
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.cost_map.shape[1] and 0 <= ny < self.cost_map.shape[0]:
                if self.cost_map[ny, nx] == -1:  # Check if unknown
                    return True
        return False

    def publish_markers(self, frontiers):
        # Clear previous markers by sending an empty marker with the same ID
        clear_marker = Marker()
        clear_marker.header.frame_id = "map"  # Ensure markers are published in the map frame
        clear_marker.header.stamp = rospy.Time.now()
        clear_marker.ns = "frontiers"
        clear_marker.id = self.marker_id
        clear_marker.action = Marker.DELETEALL

        # Publish the clear marker
        self.marker_pub.publish(clear_marker)

        # Create a Marker message for the new frontiers
        marker = Marker()
        marker.header.frame_id = "map"  # Set to the frame of the map
        marker.header.stamp = rospy.Time.now()
        marker.ns = "frontiers"
        marker.id = self.marker_id + 1  # Use a new ID for the green markers
        marker.type = Marker.SPHERE_LIST
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0

        # Set the scale of the markers
        marker.scale.x = 0.2  # Diameter of the sphere
        marker.scale.y = 0.2
        marker.scale.z = 0.2

        # Set the color for the markers (green)
        marker.color.a = 1.0  # Alpha (transparency)
        marker.color.r = 0.0  # Red
        marker.color.g = 1.0  # Green
        marker.color.b = 0.0  # Blue

        for fx, fy in frontiers:
            # Convert grid coordinates to world coordinates (map frame)
            x = (fx * self.resolution) + self.origin_x
            y = (fy * self.resolution) + self.origin_y

            # Create a new point for the marker
            point = Point()
            point.x = x
            point.y = y
            point.z = 0  # Assuming a flat surface
            marker.points.append(point)

        # Publish the marker only if there are frontiers
        if marker.points:
            self.marker_pub.publish(marker)
        else:
            rospy.loginfo("No frontiers to publish markers.")

if __name__ == '__main__':
    try:
        FrontierGenerator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
