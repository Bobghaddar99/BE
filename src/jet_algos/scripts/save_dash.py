#!/usr/bin/env python3
import rospy
import serial

# Open serial port
port = '/dev/ttyUSB0'  # Replace with your Arduino's port
baud_rate = 115200  # Increased baud rate for faster communication
ser = serial.Serial(port, baud_rate, timeout=0.01)  # Lower timeout for faster response

def print_serial_data():
    rospy.init_node('serial_data_print_node', anonymous=True)
    rate = rospy.Rate(500)  # Increased loop rate

    try:
        while not rospy.is_shutdown():
            if ser.in_waiting > 0:  # Check if data is available
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                if data:
                    rospy.loginfo(f"Received Data: {data}")

            rate.sleep()  # Sleep less to improve responsiveness

    except rospy.ROSInterruptException:
        rospy.loginfo("Exiting...")
        ser.close()

if __name__ == '__main__':
    print_serial_data()

