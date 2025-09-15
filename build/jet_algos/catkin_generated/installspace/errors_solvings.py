#!/usr/bin/env python3

import subprocess
import time

teleop_process = None

def start_teleop():
    """Start the teleop_twist_keyboard node."""
    global teleop_process
    if teleop_process is None:
        print("Starting teleop...")
        # Start the subprocess
        teleop_process = subprocess.Popen(
            ["rosrun", "teleop_twist_keyboard", "teleop_twist_keyboard.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        print("Teleop is already running.")

def stop_teleop():
    """Stop the teleop_twist_keyboard node."""
    global teleop_process
    if teleop_process:
        print("Stopping teleop...")
        teleop_process.terminate()  # Sends termination signal
        teleop_process.wait()  # Wait for process to exit
        teleop_process = None
    else:
        print("Teleop is not running.")

def main():
    global teleop_process
    while True:
        print("\nEnter '1' to start teleop, '0' to stop teleop, or 'q' to quit:")
        user_input = input("> ").strip()

        if user_input == "1":
            start_teleop()
        elif user_input == "0":
            stop_teleop()
        elif user_input.lower() == "q":
            print("Exiting...")
            if teleop_process:
                stop_teleop()
            break
        else:
            print("Invalid input. Please enter '1', '0', or 'q'.")

if __name__ == "__main__":
    main()
