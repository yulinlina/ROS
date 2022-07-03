#! /usr/bin/env python
from itertools import count
import rospy
from geometry_msgs.msg import Twist
from leader_and_follower.srv import *
from turtlesim.srv import *
from turtlesim.msg import Pose
from math import sqrt,atan2


class PidControl():
    def __init__(self):
        self.pose=Pose()
        rospy.Subscriber('/leader/pose',Pose,self.pose_callback)
        print("Pid control****************************Pid control")
        self.pid_server()

    def pid_server(self):
        rospy.init_node("pid_server")
        s=rospy.Service('service_pid',ServicePID,self.handle_pid_server)
        print("Ready to pid control")
        rospy.spin()
        

    def pose_callback(self,msg):
        self.pose=msg


    def handle_pid_server(self,req):
       
        velocity_publisher=rospy.Publisher("leader/cmd_vel",Twist,queue_size=10)
        setpen=rospy.ServiceProxy('leader/set_pen',SetPen)
        setpen(255,255,255,2,0)
        goal_pose=Pose()
        goal_pose.x=req.goal_x
        goal_pose.y=req.goal_y
        distance_tolerance=req.tolerance


        vel_msg = Twist()

        rate= rospy.Rate(10)
        count_step=0
        while self.euclidean_distance(goal_pose)>=distance_tolerance:
            if count_step>=20:
               rospy.wait_for_service('leader/teleport_absolute')
               teleport=rospy.ServiceProxy('leader/teleport_absolute',TeleportAbsolute)
               teleport(req.goal_x,req.goal_y,0)
               break
            count_step+=1
       # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(goal_pose)

            # Publishing our vel_msg
            velocity_publisher.publish(vel_msg)
           

            # Publish at the desired rate.
            rate.sleep()

        while True:
            vel_msg.linear.x =0
            vel_msg.angular.z=0
            velocity_publisher.publish(vel_msg)
    
        

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                    pow((goal_pose.y - self.pose.y), 2))
                    
    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)
     
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=6):
  
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)

if __name__=="__main__":
    pid = PidControl()