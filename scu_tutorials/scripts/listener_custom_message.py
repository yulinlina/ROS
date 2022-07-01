#! /usr/bin/env python


import rospy
from scu_tutorials.msg import CustomChat
from time import strftime
from time import gmtime

def callback(data):
    chatter =data.data
    header =data.header
    name = data.name
    timestamp = header.stamp.to_sec()
    rospy.loginfo("This message passed by %s is %s at %s"%(name,chatter,strftime("%H:%M:%S",gmtime(timestamp))))

def listener():
    rospy.Subscriber("scu_chatter",CustomChat,callback)
    rospy.init_node("Listner",anonymous=True)
    rospy.spin()

if __name__=='__main__':
    try:
        listener()
    except KeyboardInterrupt:
        pass

