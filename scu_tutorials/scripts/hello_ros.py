#! /usr/bin/env python
import rospy

rospy.init_node('hello_node')
rate =rospy.Rate(2)
while not rospy.is_shutdown():
    print("\n Hello ROS , this is my first ROS program\n")
    rate.sleep()