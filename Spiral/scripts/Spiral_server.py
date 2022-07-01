#! /usr/bin/env python

from __future__ import print_function

import rospy
from geometry_msgs.msg import Twist
from wk1homework_2020141440041.srv import *
from turtlesim.srv import SetPen
from turtlesim.msg import Pose

robot_x =0 

def set_color(color):
    rospy.wait_for_service('turtle1/set_pen')
    try:
        set_pen = rospy.ServiceProxy("turtle1/set_pen",SetPen)
        print("the track color has been changed")
        print("color choice is:  %s"%color)
        if color==0:
            set_pen(0,0,255,1,0)
        elif color==1:
            set_pen(0,255,0,1,0)
        elif color==2:
            set_pen(255,0,0,1,0)
        else:
            set_pen(255,255,255,1,0)
    except rospy.ServiceException as e:
        print("SetPen Service call failed : %s"%e)


def pose_callback(pose):
    global robot_x
    robot_x=pose.x

def handle_draw_spiral(req):
    global robot_x

    pub = rospy.Publisher("turtle1/cmd_vel",Twist,queue_size=10)
    rospy.Subscriber('/turtle1/pose',Pose,pose_callback)
    vel_msg =Twist()
    vel_msg.linear.x=req.linear_speed
    vel_msg.angular.z=req.angular_speed
    
    print("vel has been set linear speed :%s angular speed:%s"%( vel_msg.linear.x,vel_msg.angular.x) )

    rate = rospy.Rate(10)
    set_color(req.color)

    while not rospy.is_shutdown():
        if (abs(robot_x-11)<=0.2):
            rospy.loginfo("Robot Reached the wall")
            rospy.logwarn("Stop the turtlesim")
            break
        #rospy.loginfo(vel_msg)
        pub.publish(vel_msg)
        vel_msg.linear.x+=req.step
        rate.sleep()
    return True
    

  


def draw_spiral_server():
    rospy.init_node("draw_spiral_server")
    s=rospy.Service('draw_spiral',DrawSpiral,handle_draw_spiral)
    print("Ready to spiral the turtle")
    rospy.spin()

if __name__=="__main__":
   draw_spiral_server()