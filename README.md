# 🪑 Smart Robotic Chair – BE Project

This repository contains the source code, ROS packages, and design files for our **Smart Robotic Chair**, developed as our **Bachelor's Final Year Project** (FYP).  
The project integrates **ROS Noetic**, **frontier-based exploration**, and **dynamic navigation** to create an intelligent, autonomous, and user-friendly robotic mobility solution.

---

## 🚀 Project Overview

The Smart Robotic Chair is designed to provide autonomous navigation for individuals with limited mobility.  
It features **real-time mapping, obstacle avoidance, and goal navigation** via a custom GUI.  

Key highlights:
- Autonomous mapping using **GMapping**.
- **Frontier Exploration** for auto-discovery of unknown areas.
- **TEB (Timed Elastic Band)** planner for dynamic path planning.
- Integrated **Kinect camera + 2D LiDAR** for robust sensor fusion.
- User-friendly **GUI to set navigation goals** in real time.

---

## 🛠️ System Architecture

**Hardware**
- Jetson Nano (ROS master)
- 2D LiDAR 
- Kinect Camera
- Differential drive / omnidrive wheelbase
- Motor drivers and encoders
- screen 

**Software**
- ROS Noetic
- `move_base` with TEB planner or with DWA
- `gmapping` for SLAM
- Custom GUI for goal setting
- Frontier exploration algorithm
- Sensor fusion for mapping 

---
## ▶️ How to Launch


**Clone the repository** into your ROS workspace:

```bash
cd ~/catkin_ws/src
git clone https://github.com/Bobghaddar99/BE.git

**## Build the workspace:**

cd ~/catkin_ws
catkin_make
source devel/setup.bash

**    Launch the full system:**

roslaunch launcher_of_launchers.launch
