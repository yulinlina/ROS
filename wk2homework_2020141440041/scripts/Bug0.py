#! /usr/bin/env python

from std_srvs.srv import SetBool
from gazebo_msgs.srv import SetModelState
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from tf import transformations
from nav_msgs.msg import Odometry

import rospy
import math

class Bug:
    def __init__(self):
        self.state=0
        self.state_desc=[
            "Go to the point",
            "Follow the wall"
        ]
        self.yaw = 0
        self.raw_error_allowed = 5 * (math.pi / 180) # 5 degrees

        self.regions=None
        self.position=Point()

        self.desired_position = Point()
        self.desired_position.x = rospy.get_param('des_pos_x')
        self.desired_position.y = rospy.get_param('des_pos_y')
        print("*******************Bug is ready to go ****************************")

        self.sub_laser = rospy.Subscriber('/2020141440041Bot/laser/scan', LaserScan, self.clbk_laser)
        self.sub_odom = rospy.Subscriber('/Bot2020141440041/odom', Odometry, self.clbk_odom)
        
        rospy.wait_for_service('GoToPoint_switch')
        rospy.wait_for_service('followWall_switch')
        self.go_to_point=rospy.ServiceProxy('GoToPoint_switch',SetBool)
        self.follow_wall=rospy.ServiceProxy('followWall_switch',SetBool)
        #self.set_model_state=rospy.ServiceProxy()

        self.change_state(0)

              
    def take_action(self):
        rate=rospy.Rate(20)
        # print("********************************Bug is running************************")
        if self.state == 0:
            if self.regions['front'] < 1:
                self.change_state(1)

        elif self.state == 1:
            desired_yaw = math.atan2(self.desired_position.y - self.position.y, self.desired_position.x - self.position.x)
            err_yaw = self.normalize_angle(desired_yaw - self.yaw)

            # less than 30 degrees
            if math.fabs(err_yaw) < (math.pi / 6) and \
                    self.regions['front'] > 1.5 and self.regions['fright'] > 1 and self.regions['fleft'] > 1:
                self.change_state(0)

            # between 30 and 90
            if err_yaw > 0 and \
                    math.fabs(err_yaw) > (math.pi / 6) and \
                    math.fabs(err_yaw) < (math.pi / 2) and \
                    self.regions['left'] > 1.5 and  self.regions['fleft'] > 1:
                self.change_state(0)

            if err_yaw < 0 and \
                    math.fabs(err_yaw) > (math.pi / 6) and \
                    math.fabs(err_yaw) < (math.pi / 2) and \
                    self.regions['right'] > 1.5 and self.regions['fright'] > 1:
                self.change_state(0)

            rate.sleep() 

    def change_state(self,state):
        self.state=state
        # print("***************changed follow wall or go to point************************")
        log= "state changed: %s"%self.state_desc[state]
        rospy.loginfo(log)

        if state==0:
            self.go_to_point(True)
            self.follow_wall(False) 

        if state==1:
            self.follow_wall(True)
            self.go_to_point(False)
           
       # rospy.loginfo(resp)

    def clbk_odom(self,msg):
        # position
        self.position = msg.pose.pose.position

        # yaw
        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w)
        euler = transformations.euler_from_quaternion(quaternion)
        self.yaw = euler[2]
     

    def clbk_laser(self,msg):
        """ ok """
        self.regions = {
            'right':  min(min(msg.ranges[0:143]), 10),
            'fright': min(min(msg.ranges[144:287]), 10),
            'front':  min(min(msg.ranges[288:431]), 10),
            'fleft':  min(min(msg.ranges[432:575]), 10),
            'left':   min(min(msg.ranges[576:719]), 10),
        }
        self.take_action()
       

    def normalize_angle(self,angle):
        if(math.fabs(angle) > math.pi):
            angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
        return angle


if __name__=="__main__":
    rospy.init_node("bug0")
    Bug()