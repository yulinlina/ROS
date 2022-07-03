#!/usr/bin/env python
import rospy
from scu_tutorials. msg import *
from scu_tutorials.srv import *

def callback(data):
    if data.isHit == True:
        rospy.loginfo(data.message)
        rospy.wait_for_service('service_pid')
        try:
            print("try*******************************************try in client:")
            service_pid = rospy.ServiceProxy('service_pid', ServicePID)
            service_pid(10,10,0.01,"leader")
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)



if __name__ == '__main__':
    rospy.init_node('client', anonymous=True)
    rospy.Subscriber('hitboundary', HitBoundary, callback)
    
    rospy.spin()
