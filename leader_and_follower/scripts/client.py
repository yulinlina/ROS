#!/usr/bin/env python
import imp
import rospy
from leader_and_follower. msg import *
from leader_and_follower.srv import *
from turtlesim.msg import *




def callback_hit(data):
    if data.isHit == True:
        rospy.loginfo(data.message)
        rospy.wait_for_service('service_pid')
        try:
            service_pid = rospy.ServiceProxy('service_pid', ServicePID)
            service_pid(data.x,data.y,0,"leader")
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)




if __name__ == '__main__':
   

    rospy.init_node('client')
    rospy.Subscriber('hitboundary', HitBoundary, callback_hit)
   
    rospy.spin()
