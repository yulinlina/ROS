#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

def move_circle():
    pub = rospy.Publisher('turtle1/cmd_vel',Twist,queue_size=10)
    rospy.init_node('turtle_mover')

    vel_msg=Twist()
    vel_msg.linear.x=1.0
    vel_msg.angular.z=1.0

    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.loginfo(vel_msg)
        pub.publish(vel_msg)
        rate.sleep()

if __name__=="__main__":
    try:
        move_circle()
    except rospy.ROSInterruptException:
        pass