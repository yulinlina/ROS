#!/usr/bin/env python
import rospy

import tf

import tf2_ros
import tf2_msgs.msg
from geometry_msgs.msg import Twist
import geometry_msgs.msg
import turtlesim.msg
import tf_conversions
from turtlesim.msg import *
from turtlesim.srv import *
from scu_tutorials.msg import HitBoundary

import random

class tfBroadcaster:
    
    def __init__(self,turtle_name):
        
        self.spawn_leader(turtle_name)
        self.pose=Pose()
        rospy.Subscriber('%s/pose'%turtle_name,turtlesim.msg.Pose,self.handle_turtle_pose,turtle_name)
        
       

        #set pen color
        setpen = rospy.ServiceProxy("%s/set_pen"%turtle_name,SetPen)
        setpen(255,0,0,2,0)

        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=1)
        
        #publisher and velocity
        pub = rospy.Publisher('%s/cmd_vel'%turtle_name, Twist, queue_size = 10)
        vel_msg = Twist()
        #set linear speed
        vel_msg.linear.x = 1
      
        while not rospy.is_shutdown():
        #     #set angular speed random from -3 to 3
            vel_msg.angular.z = (random.random() - 0.5) * 10
            
            pub.publish(vel_msg)

            t = geometry_msgs.msg.TransformStamped()
            t.header.frame_id = "leader"
            t.header.stamp = rospy.Time.now()
            t.child_frame_id = "carrot"
            t.transform.translation.x = 0
            t.transform.translation.y = 1 #offset
            t.transform.translation.z = 0

            t.transform.rotation.x = 0
            t.transform.rotation.y = 0
            t.transform.rotation.z = 0
            t.transform.rotation.w = 1

            tfm = tf2_msgs.msg.TFMessage([t])
            self.pub_tf.publish(tfm)
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        pub.publish(vel_msg)

    def ishit_boundary(self):
         if self.pose.x>=10 or self.pose.y>=10:
            hb=HitBoundary()
            hb.isHit=True
            hb.message ="I hit the wall!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            pub=rospy.Publisher('hitboundary',HitBoundary,queue_size=10)
            pub.publish(hb)
            rospy.loginfo(hb)

    def spawn_leader(self,turtle_name):
        rospy.wait_for_service('spawn')
        spawner = rospy.ServiceProxy('spawn', Spawn)
        x = random.randint(0,10)
        y = random.randint(0,10)
        spawner(x, y, 0, turtle_name)
    
    def handle_turtle_pose(self,msg,turtlename):
        self.pose=msg
        self.ishit_boundary()
        br=tf2_ros.TransformBroadcaster()
        t = geometry_msgs.msg.TransformStamped()

        t.header.stamp=rospy.Time.now()
        t.header.frame_id="world"
        t.child_frame_id=turtlename
        t.transform.translation.x=msg.x
        t.transform.translation.y=msg.y
        t.transform.translation.z=0.0
        # rospy.loginfo(msg)
        q= tf_conversions.transformations.quaternion_from_euler(0,0,msg.theta)
        t.transform.rotation.x=q[0]
        t.transform.rotation.y=q[1]
        t.transform.rotation.z=q[2]
        t.transform.rotation.w=q[3]
        
        br.sendTransform(t)

if __name__ == '__main__':
    rospy.init_node('broadcaster')
    turtle_name = rospy.get_param('~turtle')
    tfb = tfBroadcaster(turtle_name)
    
    rospy.spin()
