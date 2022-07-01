#! /usr/bin/env python

import sys
import rospy
from wk1homework_2020141440041.srv import *

def draw_spiral_client(linears,angulars,step,color):
    rospy.wait_for_service("draw_spiral")
    try:
        draw_spiral=rospy.ServiceProxy("draw_spiral",DrawSpiral)
        resp1=draw_spiral(linears,step,angulars,color)
        return True
    except rospy.ServiceException as e:
        print("Service call failed : %s"%e)

def usage():
    return "%s [linear_speed,step,angular_step, color] "%sys.argv[0]

if __name__=="__main__":
    if len(sys.argv)==5:
         linear_speed =float(sys.argv[1])
         step=float(sys.argv[2])
         angular_speed= float(sys.argv[3])
         color=float(sys.argv[4])
    else:
        linear_speed =0.5
        step=0.01
        angular_speed= 1
        color=3
        if rospy.has_param("color_param"):
            color = rospy.get_param("color_param")
    print("color paramter is : %s"%color)
    print("Requesting %s %s %s %s"%(linear_speed,angular_speed,step,color))
    print("response state is %s"%draw_spiral_client(linear_speed,angular_speed,step,color))