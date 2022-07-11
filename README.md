# ROS
the code about tos running on linux  
all the notes are available at https://www.yuque.com/yulinlin-rf5a0/qfbvb9
## Introdution
ROS (Robot Operating System) is rapidly becoming a de facto standard in robot programming. Using the turtlesim simulator, this course will provide a hands-on introduction to programming robots with ROS with an emphasis on middleware concepts and ROS architecture.     
It also will introduce students to programming autonomous mobile robots using ROS with a special emphasis on designing a robotic system that can locate and navigate independently in an unknown environment. A 3D dynamic simulator, i.e. Gazebo, will be used throughout this course. The assessment is based on the development and implementation of path planning algorithms which allows a robot to autonomously navigate in an unknown environment.  

***The topics to be covered include:***
1. basic ROS concepts  
2. controlling a robot with ROS  
3. communication and coordination between multiple robots  
4. ROS programming with Python. 
5. The assessment is based on a Python implementation of leader-follower formation control of multi robots
6. simulating robot models in ROS
7. making an autonomous robot in ROS  
8. path planning
9. obstacle detection and mapping  
10. SLAM and Calo

## Contents in RosⅠ
1. Introduction to ROS 
* a.An overview of ROS 
* b.Basic ROS concepts: ROS master, ROS nodes, topics, messages, packages, etc 
* c.ROS command line tools 
* d.Understanding ROS using the Turtlesim simulator 
3. ROS programming with Python 
* a.Catkin workspace and ROS package 
* b.How to write a ROS node in Python c.ROS launch file   
4. Custom ROS messages and services 
* a.Understand the message/service description and specification in ROS 
* b.Steps to create a custom ROS message/service 
* c.Writing a ROS node with a custom message 
* d.Implementing a ROS service in Python 
5. Multi-robot systems in ROS 
* a.An introduction to multi-robot systems in ROS 
* b.ROS namespaces 
* c.ROS tf system and tf command tools Writing a tf broadcaster/listener in Python
## Contents in RosⅡ
1. Gazebo robotics simulator with ROS 
* a.Gazebo architecture and user interface 
* b.Turtlebot simulator in Gazebo c.3D visualization tool for ROS (RViz)   
2. Simulating Robot models in ROS 
* a.Unified Robot Description Format (URDF)
* b.Visualizing the URDF model in RViz 
* c.Spawning URDF robots in Gazebo d.Using xacro to clean up a URDF file   
3. Obstacle avoidance and path planning 
* a.Introduction to obstacle detection in ROS using a laser scanner 
* b.Reading laser sensor data 
* c.Obstacle avoidance using laser readings 
* d.Bug algorithms: Bug 0, Bug 1 and Bug 2   
4. Mapping and navigation in ROS 
* a.An introduction to ROS navigation Stack 
* b.Building a map using SLAM c.Localization and navigation Using RViz with navigation stack
