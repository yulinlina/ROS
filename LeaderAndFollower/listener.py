#!/usr/bin/env python

import rospy

import math
import tf2_ros
from geometry_msgs.msg import *
from turtlesim.msg import *
from turtlesim.srv import *
import random

def setpen(i):
    rospy.wait_for_service("/turtle%s/set_pen"%i)
    setPen = rospy.ServiceProxy("/turtle%s/set_pen"%i, SetPen)
    setPen(255, 255, 255, 3, 0)#switch on white pen

def spawn_turtle(i):
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    turtle_name = rospy.get_param('turtle', 'turtle%s'%i)
    x = random.randint(0,10)
    y = random.randint(0,10)
    spawner(x, y, 0, turtle_name)
    return turtle_name


if __name__ == '__main__':
    rospy.init_node('turtle_tf2_listener')
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    turtle_name= []
    turtle_vel= []
    for i  in range(2,5):
        turtle_name.append(spawn_turtle(i))
        turtle_vel.append(rospy.Publisher('%s/cmd_vel' % turtle_name[i-2], Twist, queue_size=1))
        setpen(i)
    
   

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        for i in range(3):
            try: 
              # print("listener *****************:")
                trans = tfBuffer.lookup_transform(turtle_name[i], 'carrot', rospy.Time())
                rospy.loginfo(trans.transform.translation)
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rate.sleep()
                continue

            msg = geometry_msgs.msg.Twist()
            msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x)
            msg.linear.x = 0.5 * math.sqrt((trans.transform.translation.x) ** 2 + trans.transform.translation.y ** 2)
            if i==1:
                msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x-1)
                msg.linear.x = 0.5 * math.sqrt((trans.transform.translation.x-1) ** 2 + trans.transform.translation.y ** 2)
            if i==2: 
                 msg.angular.z = 4 * math.atan2(trans.transform.translation.y, trans.transform.translation.x+1)
                 msg.linear.x = 0.5 * math.sqrt((trans.transform.translation.x+1) ** 2 + trans.transform.translation.y ** 2)
            turtle_vel[i].publish(msg)

        rate.sleep()

    