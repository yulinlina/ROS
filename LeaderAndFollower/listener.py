#!/usr/bin/env python

import turtle
import rospy

import math
import tf2_ros
from geometry_msgs.msg import *
from turtlesim.msg import *
from turtlesim.srv import *
import random
from scu_tutorials.msg import HitBoundary

flag_hit0=0
flag_hit1=0
flag_hit2=0
turtle_to_flag={"turtle2":0,"turtle3":0,"turtle4":0}

def setpen(i):
    rospy.wait_for_service("/turtle%s/set_pen"%i)
    setPen = rospy.ServiceProxy("/turtle%s/set_pen"%i, SetPen)
    setPen(0, 0, 0, 3, 0)#switch on black pen

def setpen_white():
    for i in range(2,5):
        rospy.wait_for_service("/turtle%s/set_pen"%i)
        setPen = rospy.ServiceProxy("/turtle%s/set_pen"%i, SetPen)
        setPen(255, 255, 255, 3, 0)#switch on black pen

def spawn_turtle(i):
    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)
    turtle_name = rospy.get_param('turtle', 'turtle%s'%i)
    x = random.randint(0,10)
    y = random.randint(0,10)
    theta=random.random()*2*math.pi
    spawner(x, y, theta, turtle_name)
    return x,y,0,turtle_name

def teleport(msg,pose):
    turtle_to_flag[pose[3]]=1
    setpen_white()
    rospy.wait_for_service('%s/teleport_absolute'%pose[3])
    teleport=rospy.ServiceProxy('%s/teleport_absolute'%pose[3],TeleportAbsolute)
    teleport(pose[0],pose[1],pose[2])
        
def follow(i):
    pass
     # print("listener *****************:")
   

if __name__ == '__main__':
    rospy.init_node('turtle_tf2_listener')
    
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    turtle_name= []
    turtle_vel= []
    turtle_x=[]
    turtle_y=[]
    turtle_theta=[]
    for i  in range(2,5):
        x,y,theta,turtlename=spawn_turtle(i)
        turtle_x.append(x)
        turtle_y.append(y)
        turtle_theta.append(theta)
        turtle_name.append(turtlename)
        turtle_vel.append(rospy.Publisher('%s/cmd_vel' % turtle_name[i-2], Twist, queue_size=1))
        setpen(i)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():  
        for i in range(3):
            if not  turtle_to_flag['turtle%s'%(i+2)]: 
                try: 
                    # print("listener *****************:")
                    trans = tfBuffer.lookup_transform(turtle_name[i], 'carrot', rospy.Time())
                   
                except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                    rate.sleep()
                    continue

                pose=[turtle_x[i],turtle_y[i],turtle_theta[i],turtle_name[i]]

                rospy.Subscriber('hitboundary',HitBoundary,teleport,pose)
        
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
            else:
                break
