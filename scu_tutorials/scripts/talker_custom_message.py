#! /usr/bin/env python

import rospy
from scu_tutorials.msg import CustomChat
from std_msgs.msg import Header

def talker():
    pub=rospy.Publisher('scu_chatter',CustomChat,queue_size=10)
    rospy.init_node('talker',anonymous=True)
    msg=CustomChat()

    msg.name="SCU user"
    count=0
    rate=rospy.Rate(10)

    while not rospy.is_shutdown():
        msg.header.stamp =rospy.Time.now()
        msg.data="Hello ROS%s"%count
        pub.publish(msg)
        count+=1
        rate.sleep()

if __name__=='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass