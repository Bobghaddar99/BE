import subprocess
import os
import rospy
from PyQt5.QtWidgets import QPushButton, QLineEdit, QVBoxLayout, QWidget

class MapSaverWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout and input field
        layout = QVBoxLayout()

        input_field_map = QLineEdit(self)
        input_field_map.setPlaceholderText("Enter Map Name")

        # Set up the Confirm button
        confirm_button_map = QPushButton("Confirm")
        confirm_button_map.clicked.connect(lambda: self.process_map_name(input_field_map))

        # Add the input field and confirm button to the layout
        layout.addWidget(input_field_map)
        layout.addWidget(confirm_button_map)

        # Disable the "Add Button" to prevent multiple inputs
        self.setLayout(layout)

    def process_map_name(self, input_field_map):
        """Process the map name input and save the map."""
        # Get the map name from the input field
        map_name = input_field_map.text().strip()

        # If map name is empty, show a warning and return
        if not map_name:
            rospy.logwarn("Map name cannot be empty.")
            return

        # Define the output directory for saved maps
        output_dir = "/home/jetchair/Desktop/be/src/maps/map_saved"  # Change this to your preferred directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Full path for saving the map
        full_path = os.path.join(output_dir, map_name)

        # Run the map_saver command to save the map
        try:
            # Ensure the ROS environment is sourced
            ros_env = os.environ.copy()
            ros_env['ROS_PACKAGE_PATH'] = '/opt/ros/noetic/share'  # You may need to adjust the ROS version if not Noetic

            result = subprocess.run(
                ["rosrun", "map_server", "map_saver", "-f", full_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=ros_env  # Set environment for subprocess
            )

            # Check if the result is successful
            if result.returncode == 0:
                rospy.loginfo("Map saved successfully at {full_path}")
            else:
                rospy.logerr("Error saving map: {result.stderr}")

        except FileNotFoundError:
            rospy.logerr("map_saver is not available. Please ensure map_server is installed.")
        except Exception as e:
            rospy.logerr("An unexpected error occurred: {str(e)}")

