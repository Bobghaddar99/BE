#!/usr/bin/python3
import rospy
import subprocess
import csv
import os
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSize, QTimer, QProcess, QPoint
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QMovie, QFont, QGuiApplication, QPolygon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFrame, QStackedWidget, QLabel, QGridLayout, QLineEdit, QFormLayout, QComboBox, QDialog, QDialogButtonBox
import subprocess
import tf
import numpy as np
#import pygame
#current_dir = os.path.dirname(os.path.abspath('/home/wassim/GUI'))


rospy
ROOMS_CSV_FILE = "rooms.csv" 
# Custom Styled Button Class
class StyledButton(QPushButton):

    def __init__(self, text, icon_path=None, parent=None):
        super(StyledButton,self).__init__(text, parent)
        rospy.init_node("gui")

        self._widget = QWidget()
        if icon_path:
            self.setIcon(QIcon(icon_path))
            
            self.setIconSize(QSize(125, 125))  # Adjust the icon size
            self.input_layout = QHBoxLayout()
        self.setStyleSheet("""
            StyledButton {
                background-color: #323232;
                color: #ecf0f1;
                border: 1px solid #323232;
                padding: 24px;
                border-radius: 12px;
                font-size: 20px;
                font-family: 'Roboto', sans-serif;
                text-align: left;
                margin: 3px;
                transition: all 0.3s ease;
            }
            StyledButton:hover {
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
            }
            StyledButton:pressed {
                background-color: #16a085;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
            }
        """)

    def set_active(self, active):
        if active:
            self.setStyleSheet("""
                StyledButton {
                    background-color: #323232;
                    color: white;
                    border: 1px solid #323232;
                    padding: 12px;
                    border-radius: 12px;
                    font-size: 16px;
                    font-family: 'Roboto', sans-serif;
                    text-align: left;
                    margin: 5px;
                }
                StyledButton:hover {
                    background-color: #16a085;
                }
            """)
        else:
            self.setStyleSheet("""
                StyledButton {
                    background-color: #212121;
                    color: #ecf0f1;
                    border: 1px solid #323232;
                    padding: 12px;self._widget = QWidget()-serif;
                    text-align: left;
                    margin: 5px;
                }
                StyledButton:hover {
                    background-color: #323232;
                    color: white;
                }
            """)

########### GLOBAL STYLE SHEETS ##############
########### GLOBAL STYLE SHEETS ##############
light_theme = """
    QWidget {
        background-color: white;
        color: black;
    }
    QPushButton {
        background-color: #f7f7f8;
        color: #007AFF;
        border: 1px solid #d1d1d6;
        border-radius: 24px;
    }
    QPushButton:hover {
        background-color: #e1e1e6;
    }
    QPushButton:pressed {
        background-color: #c0c0c7;
    }
    QLabel, QLineEdit, QComboBox, QSpinBox {
        background-color: #f7f7f8;
        color: black;
        border: 1px solid #d1d1d6;
    }
    QWidget#side_menu {
        background-color: #34495e;
        color: white;
    }
    QLabel {
        font-size: 18px;
    }
"""

dark_theme = """
    QWidget {
        background-color: #2e2e2e;
        color: white;
    }
    QPushButton {
        background-color: #1e1e1e;
        color: lightgreen;
        border: 1px solid #3c3c3c;
        border-radius: 24px;
    }
    QPushButton:hover {
        background-color: #2c2c2c;
    }
    QPushButton:pressed {
        background-color: #444444;
    }
    QLabel, QLineEdit, QComboBox, QSpinBox {
        background-color: #3c3c3c;
        color: white;
        border: 1px solid #555;
    }
    QWidget#side_menu {
        background-color: #313131;
        color: 313131;
    }
    QLabel {
        font-size: 18px;
    }

"""



class CustomizationPage(QWidget):
    def __init__(self, app):
        super(CustomizationPage,self).__init__()
        self.app = app  # We will use the main app to apply the theme globally

        layout = QVBoxLayout(self)
        
        # Add a title to your customization page
        self.title = QLabel("Customization Page", self)
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Add the "Change Theme" button
        self.theme_button = QPushButton("Change Theme", self)
        self.theme_button.clicked.connect(self.toggle_theme)  # Connect button click to toggle theme
        layout.addWidget(self.theme_button)

        self.setLayout(layout)
        self.dark_theme = False  # Track if the current theme is dark or light
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.dark_theme:
            self.app.set_light_theme()  # Apply light theme to entire app
        else:
            self.app.set_dark_theme()  # Apply dark theme to entire app

        self.dark_theme = not self.dark_theme  # Toggle theme state


class SettingsPage(QWidget):
    def __init__(self,dashboard_gui):
        super(SettingsPage,self).__init__()
        self.dashboard_gui = dashboard_gui
        # Layout for the Settings Page
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)  # Align everything to the top
        # Title or heading for the settings page
        self.title = QLabel("Settings Page", self)
        self.title.setAlignment(Qt.AlignCenter)     
        layout.addWidget(self.title)

        self.rooms = self.load_rooms_from_csv()  # Load rooms from CSV file initially        # Adding buttons dynamically (you can add as many as needed)
        self.button1 = QPushButton("Input Rooms Database", self)
        self.button2 = QPushButton("Edit Existing Rooms", self)
        self.button3 = QPushButton("Clear all Data", self)

        # Example of button actions (you can customize these as needed)
        self.button1.clicked.connect(self.input_rooms_database)
        self.button2.clicked.connect(self.edit_existing_rooms)
        self.button3.clicked.connect(self.clear_all_data)

        # Add buttons to the layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        self.setLayout(layout)
        self.style_buttons()

    def style_buttons(self):
        """Apply modern, iPhone-like style to buttons."""
        button_style = """
            QPushButton {
                background-color: #323232;
                color: #007AFF;
                border: 1px solid #303030;
                border-radius: 24px;
                padding: 12px;
                font-size: 24px Roboto;
                text-align: left;
                margin-bottom: 12px;
            }
            QPushButton:hover {
                background-color: #e1e1e6;
            }
            QPushButton:pressed {
                background-color: #c0c0c7;
            }
            QPushButton:focus {
                outline: none;
            }
        """
        # Apply the style to all buttons
        self.button1.setStyleSheet(button_style)
        self.button2.setStyleSheet(button_style)
        self.button3.setStyleSheet(button_style)


    # Example actions for the buttons (you can replace with actual logic)
    def input_rooms_database(self):
        """Handle the action when 'Input Rooms Database' button is clicked."""
        dialog = InputRoomDialog(self)
        if dialog.exec_():
            room_data = dialog.get_room_data()
            if room_data:
                self.rooms.append(room_data)
                #print(f"Room Added: {room_data}")
                self.save_rooms_to_csv()  # Save to CSV after adding room
                self.dashboard_gui.update_choosing_rooms_page(self.rooms)  # Notify the main dashboard to refresh the ChoosingRoomsPage
            else:
                print("Room data input canceled")

    def save_rooms_to_csv(self):
     with open(ROOMS_CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(["Room Name", "Position X", "Position Y", "Orientation X", "Orientation Y", "Orientation Z", "Orientation W"])

        # Write room data
        for room in self.rooms:
            room_name = room[0]  # Room name
            pose = room[1]  # PoseStamped object containing position and orientation

            # Extract position and orientation from Pose
            position_x = pose.pose.position.x
            position_y = pose.pose.position.y
            orientation_x = pose.pose.orientation.x
            orientation_y = pose.pose.orientation.y
            orientation_z = pose.pose.orientation.z
            orientation_w = pose.pose.orientation.w

            # Write data to CSV (room name and pose data)
            writer.writerow([room_name, position_x, position_y, orientation_x, orientation_y, orientation_z, orientation_w])


    def edit_existing_rooms(self):
        """Handle the action when 'Edit Existing Rooms' button is clicked."""
        if not self.rooms:
            print("No rooms to edit!")
            return

        dialog = EditRoomDialog(self.rooms, self)
        if dialog.exec_():
            updated_room = dialog.get_edited_room_data()
            if updated_room:
                index = dialog.get_selected_room_index()
                self.rooms[index] = updated_room  # Update the selected room
                #print(f"Room Updated: {updated_room}")
                self.save_rooms_to_csv()  # Save to CSV after editing
                self.dashboard_gui.update_choosing_rooms_page(self.rooms)  # Notify the main dashboard to refresh the ChoosingRoomsPage
            else:
                print("Editing canceled")

    def clear_all_data(self):
        """Show confirmation dialog before clearing data."""
        # Create the confirmation dialog
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Confirm Clear Data")
        self.dialog.setModal(True)  # Make it modal to block interaction with other windows
        self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint)  # Frameless window

        # Set custom size and style
        self.dialog.setFixedSize(400, 200)
        self.dialog.setStyleSheet("background-color: #313131;")

        # Layout setup
        layout = QVBoxLayout(self.dialog)

        # Title and description
        description_label = QLabel("Are you sure you want to clear all room data?", self.dialog)
        description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_label)

        # Buttons layout
        button_layout = QHBoxLayout()
        
        yes_button = QPushButton("Yes, Clear All Data", self.dialog)
        cancel_button = QPushButton("Cancel", self.dialog)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Connect button actions
        yes_button.clicked.connect(self.confirm_clear_all_data)  # Connect to the method that clears the data
        cancel_button.clicked.connect(self.dialog.reject)  # Close the dialog without doing anything

        # Show the dialog and wait for the user input
        self.dialog.exec_()

    def confirm_clear_all_data(self):
        """Clear all rooms data if user confirms."""
        self.rooms = []  # Clear the room list
        if os.path.exists(ROOMS_CSV_FILE):
            os.remove(ROOMS_CSV_FILE)
        print("All data cleared.")
        
        # Close the dialog after confirming
        self.dialog.accept()

        # Optionally refresh the page or update something after data is cleared
        self.dashboard_gui.update_choosing_rooms_page(self.rooms)  # This will refresh the rooms on the ChoosingRoomsPage


    def load_rooms_from_csv(self):
        """Load rooms from a CSV file."""
        if not os.path.exists(ROOMS_CSV_FILE):
            return []

        rooms = []
        with open(ROOMS_CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            #next(reader)  # Skip header
            for row in reader:
                rooms.append(tuple(row))  # Add room to the list
        return rooms


class InputRoomDialog(QDialog):
    def __init__(self, parent=None):
        self.tf_listener = tf.TransformListener()
        super(InputRoomDialog,self).__init__(parent)
        self.setWindowTitle("Input Room Data")

        self.layout = QVBoxLayout(self)

        # Create form layout
        self.form_layout = QFormLayout()
        self.room_name_input = QLineEdit(self)
        self.room_location_input = QLineEdit(self)

        self.form_layout.addRow("Room Name", self.room_name_input)        # Add form layout to main layout
        self.layout.addLayout(self.form_layout)

        # Buttons for submitting or canceling
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def accept(self):
        room_name = self.room_name_input.text()
        #print(f"Room Name: {room_name}, Room Location: {room_location}")
        super(InputRoomDialog,self).accept()
    def reject(self):
        """Handle the cancel action"""
        print("Room data input canceled")
        super(InputRoomDialog,self).reject()

    def get_room_data(self):
        """Return the entered room data."""
        room_name = self.room_name_input.text()
        try:
            self.tf_listener.waitForTransform('map', 'base_footprint', rospy.Time(0), rospy.Duration(5.0))  # wait for up to 5 seconds
            (trans, rot) = self.tf_listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
            room_location = PoseStamped()
            room_location.header.stamp = rospy.Time.now()
            room_location.header.frame_id = "map"
            room_location.pose.position.x = trans[0]
            room_location.pose.position.y = trans[1]
            room_location.pose.orientation.x = rot[0]
            room_location.pose.orientation.y = rot[1]
            room_location.pose.orientation.z = rot[2]
            room_location.pose.orientation.w = rot[3]
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.logwarn("Could not get transform from 'map' to 'base_footprint'")
        if room_name and room_location:
            return (room_name, room_location)
        return None
    

class EditRoomDialog(QDialog):
    def __init__(self, rooms, parent=None):
        super(EditRoomDialog,self).__init__(parent)
        self.setWindowTitle("Edit Existing Rooms")

        self.rooms = rooms
        self.selected_room_index = 0

        # Layout for the dialog
        self.layout = QVBoxLayout(self)

        # ComboBox to select a room
        self.room_selector = QComboBox(self)
        self.room_selector.addItems([room[0] for room in rooms])  # Display room names
        self.room_selector.currentIndexChanged.connect(self.on_room_selected)
        self.layout.addWidget(self.room_selector)

        # Form for room name and location
        self.form_layout = QFormLayout()
        self.room_name_input = QLineEdit(self)
        self.room_location_input = QLineEdit(self)

        self.form_layout.addRow("Room Name", self.room_name_input)
        self.form_layout.addRow("Room Location", self.room_location_input)

        self.layout.addLayout(self.form_layout)

        # Buttons for submitting or canceling
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

        # Set the initial room data
        self.update_room_data()

    def on_room_selected(self, index):
        """Update the room details based on selected room."""
        self.selected_room_index = index
        self.update_room_data()

    def update_room_data(self):
        """Update the QLineEdit fields with the selected room's details."""
        selected_room = self.rooms[self.selected_room_index]
        self.room_name_input.setText(selected_room[0])
        pose = selected_room[1]  # PoseStamped object
        #pose_text = f"X: {pose.pose.position.x}, Y: {pose.pose.position.y}"
        self.room_location_input.setText(pose_text)

    def get_edited_room_data(self):
        """Return the edited room data."""
        room_name = self.room_name_input.text()
        room_location = self.room_location_input.text()
        if room_name and room_location:
            return (room_name, room_location)
        return None

    def get_selected_room_index(self):
        """Return the index of the selected room."""
        return self.selected_room_index


class AutomappingPage(QWidget):
    def __init__(self, dashboard_gui):
        super(AutomappingPage,self).__init__()
        self.dashboard_gui = dashboard_gui
        layout = QVBoxLayout(self)

        rospy.set_param('ATMP', False)  

        
        self.back_button = StyledButton("Back", None, self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        self.automapping_button = StyledButton("Toggle Automapping")
        layout.addWidget(self.automapping_button, alignment=Qt.AlignCenter)
        self.automapping_button.clicked.connect(self.show_automapping_confirmation)
        layout.addWidget(self.automapping_button)
        parent_widget = QWidget()
        input_field_map = QLineEdit(parent_widget)
        input_field_map.setPlaceholderText("Enter map name")

        confirm_button_map = QPushButton("Confirm")
        confirm_button_map.clicked.connect(lambda: self.process_map_name(input_field_map))

        # Add the input field and confirm button to the layout
        layout.addWidget(input_field_map)
        layout.addWidget(confirm_button_map)

        # Disable the "Add Button" to prevent multiple inputs
        self.setLayout(layout)
    def process_map_name(self,input_field_map):
        """Process the map name input and save the map."""
        # Get the map name from the input field
        map_name = input_field_map.text().strip()

        # If map name is empty, show a warning and return
        if not map_name:
            rospy.logwarn("Map name cannot be empty.")
            #self.reset_input_field()
            return

        # Define the output directory for saved maps
        output_dir = r"/home/bob/Desktop/be/src/stair_cl_maps/map_saved" # Change this to your preferred directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Full path for saving the map
        full_path = os.path.join(output_dir, map_name)

    # Run the map_saver command to save the map
        try:
            result = subprocess.run(
             ["rosrun", "map_server", "map_saver", "-f", full_path],
             stdout=subprocess.PIPE,
             stderr=subprocess.PIPE,
             text=True,
            )

            # Check the result and log appropriate message
            #if result.returncode == 0:
             #rospy.loginfo(f"Map saved successfully at {full_path}")
            #else:
             #rospy.logerr(f"Failed to save the map: {result.stderr}")

        except FileNotFoundError:
         rospy.logerr("map_saver is not available. Please ensure map_server is installed.")

        # Reset the input field and enable the add button again
        #self.reset_input_field()
    def go_back(self):
        self.dashboard_gui.show_main_page()

        
    def show_automapping_confirmation(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Confirm Automapping")
        self.dialog.setModal(True)  # Make it modal to block interaction with other windows
        self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint)  # Frameless window

        # Set custom size and style
        self.dialog.setFixedSize(400, 200)
        self.dialog.setStyleSheet("background-color: white;")

        # Layout setup
        layout = QVBoxLayout(self.dialog)

        # Title and description
        description_label = QLabel("Are you sure you want to start automapping?", self.dialog)
        description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_label)

        # Buttons layout
        button_layout = QHBoxLayout()

        yes_button = QPushButton("Yes, Start Automapping", self.dialog)
        cancel_button = QPushButton("Stop Automapping", self.dialog)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Connect button actions
        yes_button.clicked.connect(self.start_automapping)  # Start automapping if confirmed
        cancel_button.clicked.connect(self.cancel_automapping)  # Close the dialog if canceled

        # Show the dialog
        self.dialog.exec_()

    def start_automapping(self):
        """Start automapping."""
        rospy.set_param('ATMP', True)  # Set automapping parameter to True
        print("Automapping started!")

        # Close the dialog after starting automapping
        self.dialog.accept()  # Close the dialog after confirmation

    def cancel_automapping(self):
        """Cancel automapping."""
        rospy.set_param('ATMP', False)  # Set automapping parameter to False
        print("Automapping canceled.")  # Handle cancellation logic here

        # Close the dialog after cancellation
        self.dialog.reject()  # Close the dialog after cancellation


class DockingStationPage(QWidget):
    def __init__(self, dashboard_gui):
        super(DockingStationPage,self).__init__()
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.dashboard_gui = dashboard_gui
        rospy.set_param('HOMING', False)  
        layout = QVBoxLayout(self)
        self.Homebutton = StyledButton("GO Home", None, self)
        self.Homebutton.clicked.connect(self.go_home)
        layout.addWidget(self.Homebutton, alignment=Qt.AlignCenter)
        self.back_button = StyledButton("Back", None, self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.Homebutton.setFixedSize(150, 100)  # Width: 150, Height: 50
        self.setLayout(layout)
    def go_home(self):
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = rospy.Time.now()  # Ensure correct timestamp
            pose.pose.position.x = 0
            pose.pose.position.y = 0
            pose.pose.orientation.x = 0
            pose.pose.orientation.y = 0
            pose.pose.orientation.z = 0
            pose.pose.orientation.w = 1
            self.goal_pub.publish(pose)
    def go_back(self):
        self.dashboard_gui.show_main_page()


class ChoosingRoomsPage(QWidget):
    def __init__(self, dashboard_gui,rooms):
        super(ChoosingRoomsPage,self).__init__()
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.dashboard_gui = dashboard_gui
        self.rooms = rooms  # Initialize with a list of rooms

        layout = QVBoxLayout(self)
        self.label = QLabel("Select a Room", self)
        layout.addWidget(self.label)
        
        # Combo box to display existing rooms
        self.room_selector = QComboBox(self)
        self.room_selector.addItems(["{} - {}".format(room[0],room[1]) for room in self.rooms])
        layout.addWidget(self.room_selector)

        # Confirm Button
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_room_selection)
        layout.addWidget(self.confirm_button)

        # Back Button
        self.back_button = StyledButton("Back", None, self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        self.setLayout(layout)


    def load_rooms(self):
        """Load rooms from the settings page."""
        self.rooms = self.dashboard_gui.settings_page.rooms  # Use the updated rooms list
        self.update_room_selector()

    def update_room_selector(self):
        """Update the room selector combo box."""
        self.room_selector.clear()
        self.room_selector.addItems(["{} - {}".format(room[0],room[1]) for room in self.rooms])


    def confirm_room_selection(self):
        """Show confirmation dialog before confirming room selection."""
        selected_index = self.room_selector.currentIndex()
        if selected_index != -1:  # Ensure a room is selected
            selected_room = self.rooms[selected_index]
            print("Room '{}' selected!".format(selected_room[0]))

            # Show confirmation dialog
            self.dialog = QDialog(self)
            self.dialog.setWindowTitle("Confirm Room Selection")
            self.dialog.setModal(True)  # Make it modal to block interaction with other windows
            self.dialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowCloseButtonHint)  # Frameless window

            # Set custom size and style
            self.dialog.setFixedSize(400, 200)
            self.dialog.setStyleSheet("background-color: #313131;")

            # Layout setup
            layout = QVBoxLayout(self.dialog)

            # Title and description
            description_label = QLabel("Are you sure you want to select the room '?", self.dialog)
            description_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(description_label)

            # Buttons layout
            button_layout = QHBoxLayout()

            yes_button = QPushButton("Yes, Confirm", self.dialog)
            cancel_button = QPushButton("Cancel", self.dialog)

            button_layout.addWidget(yes_button)
            button_layout.addWidget(cancel_button)

            layout.addLayout(button_layout)

            # Connect button actions
            yes_button.clicked.connect(lambda: self.finalize_room_selection(selected_room))  # Finalize if confirmed
            cancel_button.clicked.connect(self.dialog.reject)  # Close the dialog if canceled

            # Show the dialog
            self.dialog.exec_()  # This will block interaction until a decision is made

        else:
            print("No room selected!")

    def finalize_room_selection(self, selected_room):
     with open(ROOMS_CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
         print(selected_room[1])
         position_x = float(row[1])  # Convert string to float for position
         position_y = float(row[2])  # Convert string to float for position
         orientation_x = float(row[3])  # Convert string to float for orientation
         orientation_y = float(row[4])  # Convert string to float for orientation
         orientation_z = float(row[5])  # Convert string to float for orientation
         orientation_w = float(row[6])  # Convert string to float for orientation
         room_location = PoseStamped()
         room_location.header.stamp = rospy.Time.now()
         room_location.header.frame_id = "map"
         room_location.pose.position.x = position_x
         room_location.pose.position.y = position_y
         room_location.pose.orientation.x = orientation_x
         room_location.pose.orientation.y = orientation_y
         room_location.pose.orientation.z = orientation_z
         room_location.pose.orientation.w = orientation_w
         self.goal_pub.publish(room_location)

     self.dialog.accept()


    def go_back(self):
        """Navigate back to the main page."""
        self.dashboard_gui.show_main_page()



class LiftingPage(QWidget):
    def __init__(self, dashboard_gui):
        super(LiftingPage,self).__init__()
        self.dashboard_gui = dashboard_gui
        
        # Create main layout
        main_layout = QHBoxLayout(self)
        
        # Create a container for arrow buttons with vertical layout
        arrow_container = QWidget()
        arrow_layout = QVBoxLayout(arrow_container)
        
        # Create arrow buttons with Unicode arrow symbols
        self.up_arrow = QPushButton("LIft UP", self)
        self.down_arrow = QPushButton("LIFT DOWN", self)

        rospy.set_param('lift_up', False)  # Initially lift up is not pressed
        rospy.set_param('lift_down', False)  # Initially lift down is not pressed
        
        # Style the arrow buttons
        arrow_style = """
            QPushButton {
                background-color: #1abc9c;
                color: white;
                border: 2px solid #16a085;
                border-radius: 10px;
                font-size: 24px;
                min-width: 60px;
                min-height: 60px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
            QPushButton:pressed {
                background-color: #148f77;
                border: 2px solid #0e6655;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                border: 2px solid #95a5a6;
            }
        """
        self.up_arrow.setStyleSheet(arrow_style)
        self.down_arrow.setStyleSheet(arrow_style)
        
        # Connect button press and release events
        self.up_arrow.pressed.connect(self.up_arrow_pressed)
        self.up_arrow.released.connect(self.up_arrow_released)
        self.down_arrow.pressed.connect(self.down_arrow_pressed)
        self.down_arrow.released.connect(self.down_arrow_released)
        
        # Add spacer at the top to push buttons to vertical center
        arrow_layout.addStretch()
        
        # Add buttons to the arrow layout with some spacing
        arrow_layout.addWidget(self.up_arrow, alignment=Qt.AlignCenter)
        arrow_layout.addSpacing(10)  # Add 10 pixels spacing between arrows
        arrow_layout.addWidget(self.down_arrow, alignment=Qt.AlignCenter)
        
        # Add spacer at the bottom to maintain vertical centering
        arrow_layout.addStretch()
        
        # Create content area (right side)
        
        # Add the original label and back button to content area
        
        self.back_button = StyledButton("Back", None, self)
        self.back_button.clicked.connect(self.go_back)
        arrow_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        
        # Add the arrow container and content area to main layout
        main_layout.addWidget(arrow_container)
        
        # Set the stretch factors to position arrows on the left
        main_layout.setStretchFactor(arrow_container, 1)        
        self.setLayout(main_layout)
        
    def up_arrow_pressed(self):
        """Handle up arrow press event"""
        print("Up arrow pressed - Start lifting up")
        rospy.set_param('lift_up', True)        
        
    def up_arrow_released(self):
        """Handle up arrow release event"""
        print("Up arrow released - Stop lifting up")
        rospy.set_param('lift_up', False)        

    def down_arrow_pressed(self):
        """Handle down arrow press event"""
        print("Down arrow pressed - Start lifting down")
        rospy.set_param('lift_down', True)   

    def down_arrow_released(self):
        """Handle down arrow release event"""
        print("Down arrow released - Stop lifting down")
        rospy.set_param('lift_down', False)

    def go_back(self):
        """Return to main page"""
        self.dashboard_gui.show_main_page()
        
class NLPage(QWidget):
    def __init__(self, dashboard_gui):
        super(NLPage,self).__init__()
        self.dashboard_gui = dashboard_gui  # Store reference to DashboardGUI
        layout = QVBoxLayout(self)

        # Create a label for the "Listening..." message
        self.listening_label = QLabel("Listening...", self)
        self.listening_label.setAlignment(Qt.AlignCenter)
        self.listening_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        layout.addWidget(self.listening_label)

        # Create an icon in the center
        self.gif_label = QLabel(self)
        self.movie = QMovie("/home/wassim/icons_gui/Listening.gif")
        self.gif_label.setMovie(self.movie)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.movie.start()
        layout.addWidget(self.gif_label)
        self.setLayout(layout)
        
        # Create the timer for 5 seconds
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # The timer will only trigger once
        self.timer.timeout.connect(self.switch_to_main_page)

    def start_listening(self):
        """Start the listening process, which will last 5 seconds."""
        self.timer.start(5000)  # Start a timer for 5 seconds (5000 milliseconds)
    
    def switch_to_main_page(self):
        """Switch back to the main page after 5 seconds."""
        dashboard_gui = self.dashboard_gui  # Get the parent DashboardGUI
        dashboard_gui.stacked_widget.setCurrentWidget(dashboard_gui.main_page)  # Switch to the main page

class VisualizationPage(QWidget):
    def __init__(self, dashboard_gui):
        super(VisualizationPage,self).__init__()
        self.dashboard_gui = dashboard_gui
        
        layout = QVBoxLayout(self)

        # Label for Visualization Page
        self.label = QLabel("Visualization Control Panel", self)
        self.label.setStyleSheet("font-size: 24px; color: #323232; font-family: 'Roboto', sans-serif;")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # Launch RViz Button
        self.launch_rviz_button = StyledButton("Launch Visualizer", None, self)
        self.launch_rviz_button.clicked.connect(self.launch_rviz)
        layout.addWidget(self.launch_rviz_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.rviz_process = QProcess(self)

    def launch_rviz(self):
        rviz_config_path = "/home/bob/Desktop/gui_test/src/gui_ros/src/config_gui_rviz.rviz"  # Update this path
        rviz_command = ['rosrun', 'rviz', 'rviz', '-d', rviz_config_path] 
        self.rviz_process.start(rviz_command[0], rviz_command[1:])
        print("Launching RViz...")
        #subprocess.Popen(['rviz'])


# SlottedSideMenu class remains unchanged
class SlottedSideMenu(QFrame):
    def __init__(self, parent=None):
        super(SlottedSideMenu,self).__init__(parent)
        self.setStyleSheet("background-color: #323232;")
        self.setFixedWidth(250)
        self.setGeometry(-250, 0, 250, parent.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.end()
        


# Modified DashboardGUI class with smooth transitions
class DashboardGUI(QMainWindow):
    def __init__(self):
        super(DashboardGUI,self).__init__()
        self.setWindowTitle("Smooth Side Menu Dashboard")
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.setGeometry(screen_geometry)
        #self.setWindowState(Qt.WindowFullScreen)

        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.main_layout = QVBoxLayout(self.main_widget)

        self.title_label = QLabel("Willow Control Interface", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Roboto", 36, QFont.Bold))
        self.title_label.setStyleSheet("color: black;")
        
        # Add title to the main layout (Top center)


        self.top_margin = QFrame(self)
        self.top_margin.setStyleSheet("background-color: #313131;")
        self.top_margin.setFixedHeight(25)

        self.main_layout.addWidget(self.top_margin)
        self.main_layout.addWidget(self.title_label)

        self.top_layout = QHBoxLayout()
        self.main_layout.addLayout(self.top_layout)

        self.side_menu = SlottedSideMenu(self)

        
        self.toggle_button = QPushButton("=", self)
        self.toggle_button.setStyleSheet("font-size: 20px; background-color: #313131; color: white; border: none;")
        self.toggle_button.clicked.connect(self.toggle_menu)

        self.top_layout.addWidget(self.toggle_button, alignment=Qt.AlignLeft)

        # Create buttons for the side menu
        self.main_button = StyledButton("Main Interface", None, self)
        self.customization_button = StyledButton("Customization", None, self)
        self.settings_button = StyledButton("Settings", None, self)
        self.visualization_button = StyledButton("Visualization", None, self)
        #self.emergent_button.move(775, 850)  # Set button position (X, Y)

        #self.emergent_button.setMinimumSize(300, 150)  # Set minimum button size
        # Connect buttons to the relevant methods
        self.main_button.clicked.connect(self.show_main_page)
        self.customization_button.clicked.connect(self.show_customization_page)
        self.settings_button.clicked.connect(self.show_settings_page)
        self.visualization_button.clicked.connect(self.show_visualization_page)

        side_menu_layout = QVBoxLayout(self.side_menu)
        side_menu_layout.addWidget(self.main_button)
        side_menu_layout.addWidget(self.customization_button)
        side_menu_layout.addWidget(self.settings_button)
        side_menu_layout.addWidget(self.visualization_button)
    
        self.stacked_widget = QStackedWidget(self)
        self.main_layout.addWidget(self.stacked_widget)





        self.main_page = QWidget()
        self.customization_page = QWidget()
        self.customization_page = CustomizationPage(self)  # Use our new CustomizationPage here
        self.settings_page = SettingsPage(self)        
        self.visualization_page = VisualizationPage(self)
        self.automapping_page = AutomappingPage(self)
        self.docking_station_page = DockingStationPage(self)
        self.lifting_page = LiftingPage(self)
        self.nl_page = NLPage(self)  # Initialize NLPage here
        self.choosing_rooms_page = ChoosingRoomsPage(self, self.settings_page.rooms)


        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.customization_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.visualization_page)
        self.stacked_widget.addWidget(self.visualization_page)
        self.stacked_widget.addWidget(self.automapping_page)
        self.stacked_widget.addWidget(self.docking_station_page)
        self.stacked_widget.addWidget(self.lifting_page)
        self.stacked_widget.addWidget(self.nl_page)
        self.stacked_widget.addWidget(self.choosing_rooms_page)

        # Create buttons for the main page (Auto Mapping, Lift, etc.)
        self.main_page_layout = QGridLayout(self.main_page)

        # Add the buttons with icons
        self.auto_mapping_button = StyledButton("Auto Mapping", "/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/robot.png", self)
        self.docking_button = StyledButton("Docking", "/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/home.png", self)
        self.lift_button = StyledButton("Lift", "/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/lifting.png", self)
        self.choose_rooms_button = StyledButton("Choose Rooms", "/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/press-button.png", self)
        self.emergent_button = StyledButton("Emergencay","/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/emerg.jpg",self)
        self.joystick = StyledButton("joystick","/home/bob/Desktop/gui_test/src/gui_ros/src/icons_gui/emerg.jpg",self)
        self.auto_mapping_button.clicked.connect(lambda: self.show_bottom_menu("automapping"))
        self.docking_button.clicked.connect(lambda: self.show_bottom_menu("docking"))
        self.lift_button.clicked.connect(lambda: self.show_bottom_menu("lifting"))
        self.choose_rooms_button.clicked.connect(lambda: self.show_bottom_menu("choosing_rooms"))
        self.emergent_button.clicked.connect(lambda:self.siren_sound())
        self.joystick.clicked.connect(lambda:self.siren_sound())
        # Add buttons to the main page layout (grid)
        # Arrange the first 4 buttons in two rows (2 buttons per row)
        self.main_page_layout.addWidget(self.auto_mapping_button, 0, 0)
        self.main_page_layout.addWidget(self.docking_button, 0, 1)
        self.main_page_layout.addWidget(self.lift_button, 1, 0)
        self.main_page_layout.addWidget(self.choose_rooms_button, 1, 1)
        self.main_page_layout.addWidget(self.emergent_button, 2, 0, 1, 2)  # Span 2 columns to center it
        self.main_page_layout.addWidget(self.joystick,2,0,2,2)
        self.main_page.setLayout(self.main_page_layout)
        # Set the layout for the overlay and add the loader to it
        
        self.set_dark_theme()


        # Set up a timer to simulate loading for 3 seconds

        # Animation for the side menu toggle
        self.animation = QPropertyAnimation(self.side_menu, b"geometry")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.main_widget_animation = QPropertyAnimation(self.main_widget, b"geometry")
        self.main_widget_animation.setDuration(500)
        self.main_widget_animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.menu_open = False

        self.side_menu.move(-250, 0)

        self.toggle_button.raise_()

        self.bottom_menu = QWidget(self)
        self.bottom_menu.setStyleSheet("background-color: #212121;")
        self.bottom_menu.setFixedHeight(1200)  # Height of bottom menu
        self.bottom_menu.move(0, self.height())  # Start off-screen at the bottom
        self.bottom_menu_layout = QVBoxLayout(self.bottom_menu)
        self.bottom_menu_label = QLabel("", self)
        self.bottom_menu_label.setStyleSheet("font-size: 18px; color: white;")
        self.bottom_menu_layout.addWidget(self.bottom_menu_label)
        self.bottom_menu.setLayout(self.bottom_menu_layout)

        # Bottom menu animation
        self.bottom_menu_animation = QPropertyAnimation(self.bottom_menu, b"geometry")
        self.bottom_menu_animation.setDuration(800)
        self.bottom_menu_animation.setEasingCurve(QEasingCurve.InOutQuad)
    def siren_sound(self):
     #pygame.mixer.init()
     print("here")
    

# Load the sound file (supports MP3, WAV, OGG, etc.)

    def update_choosing_rooms_page(self, rooms):
        """Update the ChoosingRoomsPage with new rooms."""
        self.choosing_rooms_page.load_rooms()

    def show_settings_page(self):
        """Show the settings page."""
        self.layout.addWidget(self.settings_page)

    def show_choosing_rooms_page(self):
        """Show the choosing rooms page."""
        self.choosing_rooms_page.load_rooms()  # Reload rooms when visiting the ChoosingRoomsPage
        self.layout.addWidget(self.choosing_rooms_page)

    def set_light_theme(self):
        """Set the light theme for the entire app."""
        self.setStyleSheet(light_theme)
      

    def set_dark_theme(self):
        """Set the dark theme for the entire app."""
        self.setStyleSheet(dark_theme)
       

    def toggle_menu(self):
        """Toggle the visibility of the side menu with animation."""
        if not self.menu_open:
            self.animation.setStartValue(QRect(-250, 0, 250, self.height()))
            self.animation.setEndValue(QRect(0, 0, 250, self.height()))
            self.main_widget_animation.setStartValue(QRect(0, 0, self.width(), self.height()))
            self.main_widget_animation.setEndValue(QRect(250, 0, self.width() - 250, self.height()))
            self.menu_open = True
        else:
            self.animation.setStartValue(QRect(0, 0, 250, self.height()))
            self.animation.setEndValue(QRect(-250, 0, 250, self.height()))
            self.main_widget_animation.setStartValue(QRect(250, 0, self.width() - 250, self.height()))
            self.main_widget_animation.setEndValue(QRect(0, 0, self.width(), self.height()))
            self.menu_open = False

        self.animation.start()
        self.main_widget_animation.start()

    def show_bottom_menu(self, page_name):
        menu_height = 1000  # Get the full height of the main window
        """Show the bottom sliding menu before switching to the page."""
        self.bottom_menu_animation.setStartValue(QRect(0, self.height(), self.width(), self.height()))  # Off-screen at the bottom
        self.bottom_menu_animation.setEndValue(QRect(0, self.height() - self.height(), self.width(), self.height()))  # Slide up
        self.bottom_menu_animation.start()

        QTimer.singleShot(300, lambda: self.switch_page(page_name))

    def switch_page(self, page_name):
        """Switch to the respective page after the bottom menu slides up."""
        if page_name == "automapping":
            self.stacked_widget.setCurrentWidget(self.automapping_page)
        elif page_name == "docking":
            self.stacked_widget.setCurrentWidget(self.docking_station_page)
        elif page_name == "lifting":
            self.stacked_widget.setCurrentWidget(self.lifting_page)
        elif page_name == "choosing_rooms":
            self.stacked_widget.setCurrentWidget(self.choosing_rooms_page)

        QTimer.singleShot(300, self.switch_off_loading)  # After 3 seconds, call switch_off_loading



    def switch_off_loading(self):
        self.hide_bottom_menu()


    def hide_bottom_menu(self):
        """Hide the bottom menu after the page is shown."""
        self.bottom_menu_animation.setStartValue(QRect(0, self.height() , self.width(), 0))
        self.bottom_menu_animation.setEndValue(QRect(0, self.height(), self.width(), 0))  # Slide down
        self.bottom_menu_animation.start()


    def switch_to_button(self):


        # Show the button
        self.button.setVisible(True)


    def show_main_page(self):
        """Switch to the main page and reset layout if the side menu is toggled."""
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.main_button.set_active(True)
        self.customization_button.set_active(False)
        self.settings_button.set_active(False)
        self.visualization_button.set_active(False)
        self.hide_menu()

    def show_customization_page(self):
        """Switch to the customization page."""
        self.stacked_widget.setCurrentWidget(self.customization_page)
        self.hide_menu()

    def show_settings_page(self):
        """Switch to the settings page."""
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.hide_menu()

    def show_visualization_page(self):
        """Switch to the visualization page."""
        self.stacked_widget.setCurrentWidget(self.visualization_page)
        self.hide_menu()

    def show_automapping_page(self):
        """Switch to the Automapping page."""
        self.show_bottom_menu("automapping")

    def show_docking_station_page(self):
        """Switch to the Docking Station page."""
        self.stacked_widget.setCurrentWidget(self.docking_station_page)
        self.show_bottom_menu("docking")

    def show_lifting_page(self):
        """Switch to the Lifting page."""
        self.stacked_widget.setCurrentWidget(self.lifting_page)
        self.show_bottom_menu("lifting")

    def show_choose_rooms(self):
        """Switch to the Choosing page."""
        self.stacked_widget.setCurrentWidget(self.choosing_rooms_page)
        self.show_bottom_menu("choosing_rooms")


    def hide_menu(self):
        """Hide the side menu if it's visible."""
        if self.menu_open:
            self.toggle_menu()

    def resizeEvent(self, event):
        """Adjust layout when the window is resized."""
        if self.menu_open:
            self.main_widget.setGeometry(250, 0, self.width() - 250, self.height())
        else:
            self.main_widget.setGeometry(0, 0, self.width(), self.height())

    def mousePressEvent(self, event):
        """Close the menu if clicked outside the side menu area."""
        if event.button() == Qt.LeftButton:
            if self.menu_open and not self.side_menu.geometry().contains(event.pos()):
                self.hide_menu()


if __name__ == '__main__':
    rospy.init_node("gui")

    app = QApplication(sys.argv)
    window = DashboardGUI()
    window.show()
    sys.exit(app.exec_())
