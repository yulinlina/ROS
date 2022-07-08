#! /usr/bin/env python

from turtle import st
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point
from nav_msgs.msg import Odometry
from tf import transformations

# A partially completed python class used to move a robot from any point to a desired point
import math
from std_srvs.srv import SetBool
class GoToPoint:

    def __init__(self):
       
        self.active = False
       
        # robot state variables
        self.position = Point()
        self.yaw = 0
        # A state machine: 0 - Fix heading; 1 - Go Straight; 2 - Reach the desitination
		#More information can be found at https://www.theconstructsim.com/ros-projects-exploring-ros-using-2-wheeled-robot-part-1/
        self.state = 0
        # Destination
        self.desired_position = Point()
        self.desired_position.x = rospy.get_param('des_pos_x')
        self.desired_position.y = rospy.get_param('des_pos_y')

        

        self.desired_position.z = 0
        # Threshold parameters
        self.yaw_threshold = rospy.get_param('th_yaw') # unit: degree
        self.yaw_threshold *= math.pi/90 # convert to radian

        self.dist_threshold = rospy.get_param('th_dist') # unit: meter

        #Need to change the topic used to command the robot to move based on what you defined in your urdf file.
        self.pub_vel = rospy.Publisher('week2bot/cmd_vel', Twist, queue_size=10)
		
		#Need to change the /odom topic based on what you defined in your urdf file.   
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.callback_odom)
        rospy.Service('GoToPoint_switch',SetBool,self.HandleGoToPoint)

        rate = rospy.Rate(20)
        while not rospy.is_shutdown():
            if not self.active:
                continue
            else:
                if self.state == 0:
                    self.fix_heading(self.desired_position)
                elif self.state == 1:
                    self.go_straight_ahead(self.desired_position)
                elif self.state == 2:
                    self.done()
                    break
                else:
                    rospy.logerr('Unknown state!')
        
                rate.sleep()
    
    def HandleGoToPoint(self,req):
        self.active =req.data
        return True,"Done!"


    def callback_odom(self,msg):
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


	# Please complete the rest of code.
	# The overall logic that governs its behavious can be found at 
	# https://www.theconstructsim.com/ros-projects-exploring-ros-using-2-wheeled-robot-part-1/
    def fix_heading(self,des_pos):
        desired_yaw =math.atan2(des_pos.y-self.position.y,des_pos.x-self.position.x)
        err_yaw =desired_yaw-self.yaw

        twist_msg =Twist()
        if math.fabs(err_yaw)>self.yaw_threshold:
            twist_msg.angular.z=0.7 if err_yaw>0 else -0.7
       # rospy.loginfo(twist_msg)
        self.pub_vel.publish(twist_msg)

        if math.fabs(err_yaw) <= self.yaw_threshold:
           # print('Yaw error: [%s]'%err_yaw)
            self.change_state(1)

    def go_straight_ahead(self,des_pos):
        #   rospy.loginfo(des_pos)
        #   rospy.loginfo(self.yaw_threshold)

          desired_yaw = math.atan2(des_pos.y - self.position.y, des_pos.x - self.position.x)
          err_yaw =desired_yaw-self.yaw
          err_pos =math.sqrt(pow(des_pos.y-self.position.y,2)+pow(des_pos.x-self.position.x,2))
          if err_pos>self.dist_threshold:
              twist_msg =Twist()
              twist_msg.linear.x=1
              self.pub_vel.publish(twist_msg)
          else:
            #print("Position error: [%s]"%err_pos)
            self.change_state(2)

          if math.fabs(err_yaw)>self.yaw_threshold:
            # print('Yaw error: [%s]'%err_yaw)
            self.change_state(0)
          
    def done(self):
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        self.pub_vel.publish(twist_msg)

    def change_state(self,state):
        self.state=state
       #  print("State changed to [%s]"%state)

       

if __name__ == '__main__':

    rospy.init_node('go_to_point')
    GoToPoint()
    rospy.spin()
    
    