#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import SetBool


# A partially completed python class used to make the robot follow a wall
# A state machine: 0 - Find the wall; 1 - Turn left; 2 - Follow the wall
# More information can be found at https://www.theconstructsim.com/ros-projects-exploring-ros-using-2-wheeled-robot-part-1/





class FollowWall:
    def __init__(self,req=False):
        self.active=req
        self.state=0
        self.regions_ = {
            'right': 0,
            'fright': 0,
            'front': 0,
            'fleft': 0,
            'left': 0,
        }
        self.state_dict={
            0: 'find the wall',
            1: 'turn left',
            2: 'follow the wall',
        }
        self.state_description = ''
        
	# 	#Need to change the topic used to command the robot to move based on what you defined in your urdf file.
        self.pub_vel = rospy.Publisher('week2bot/cmd_vel', Twist, queue_size=1)
		
		#Need to change the topic used for publishing the laser data based on what you defined in your urdf file.
        self.sub_laser = rospy.Subscriber('/week2bot/laser/scan', LaserScan, self.callback_laser)

        rospy.Service('followWall_switch',SetBool,self.HandleFollowWall)
      
        rate = rospy.Rate(20)
        #print("*************follow the wall*************")
        #print(self.active)
        while not rospy.is_shutdown():
            if not self.active:
                rate.sleep()
                continue
            msg = Twist()
            if self.state == 0:
                msg = self.find_wall()
            elif self.state == 1:
                msg = self.turn_left()
            elif self.state == 2:
                msg = self.follow_the_wall()
            else:
                rospy.logerr('Unknown state!')
            
            self.pub_vel.publish(msg)
          #  rospy.loginfo(msg)
            
            rate.sleep()

	# Please complete the rest of code.
	# The overall logic that governs its behavious can be found at 
	# https://www.theconstructsim.com/ros-projects-exploring-ros-using-2-wheeled-robot-part-1/

    def callback_laser(self,msg):
        self.regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
        }   
        self.take_action()

    def take_action(self):
        regions = self.regions_
      
        
        d = 1.5
        
        if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
            self.state_description = 'case 1 - nothing'
            self.change_state(0)
        elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
            self.state_description = 'case 2 - front'
            self.change_state(1)
        elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
            self.state_description = 'case 3 - fright'
            self.change_state(2)
        elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
            self.state_description = 'case 4 - fleft'
            self.change_state(0)
        elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
            self.state_description = 'case 5 - front and fright'
            self.change_state(1)
        elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
            self.state_description = 'case 6 - front and fleft'
            self.change_state(1)
        elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
            self.state_description = 'case 7 - front and fleft and fright'
            self.change_state(1)
        elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
            self.state_description = 'case 8 - fleft and fright'
            self.change_state(0)
        else:
            self.state_description = 'unknown case'
           # rospy.loginfo(regions)
        # rospy.loginfo(self.state_description)

    def change_state(self,state):
       # print ('Wall follower - [%s] -> %s' % (state, self.state_dict[state]))
        if state is not self.state:
            #print ('Wall follower - [%s] - %s' % (state, self.state_dict[state]))
            self.state = state

    def find_wall(self):
        msg =Twist()
        msg.linear.x=0.2
        msg.angular.z=-0.3
        return msg

    def turn_left(self):
        msg =Twist()
        msg.angular.z=0.3
        return msg

    def turn_right(self):
        msg =Twist()
        msg.angular.z=-0.3
        return msg

    def follow_the_wall(self):
        msg=Twist()
        msg.linear.x=0.5
        return msg

    def HandleFollowWall(self,req):
        self.active=req.data
        return True,"Done!"

if __name__=='__main__':
    rospy.init_node('follow_wall')
    FollowWall()
    rospy.spin()