#!/usr/bin/env python  
  
################################################
#Steven.Zhang
#2021.01.19
################################################

import rospy  
import actionlib  
from actionlib_msgs.msg import *  
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist, PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal  
from random import sample  
from math import pow, sqrt  

#time for nav:s
Time = 5.8
  
class PositionNav():  
    def __init__(self):  
        rospy.init_node('position_nav_node', anonymous=True)  
        self.pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
        rospy.on_shutdown(self.shutdown)  
          
        # How long in seconds should the robot pause at each location?  
        self.rest_time = rospy.get_param("~rest_time", 10)  
          
        # Are we running in the fake simulator?  
        self.fake_test = rospy.get_param("~fake_test", False)  
          
        # Goal state return values  
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED',   
                       'SUCCEEDED', 'ABORTED', 'REJECTED',  
                       'PREEMPTING', 'RECALLING', 'RECALLED',  
                       'LOST']  
          
        # Set up the goal locations. Poses are defined in the map frame.
        # An easy way to find the pose coordinates is to point-and-click  
        # Nav Goals in RViz when running in the simulator.  
        #  
        # Pose coordinates are then displayed in the terminal  
        # that was used to launch RViz.  
        locations = dict()  
        locations['one'] = Pose(Point(0,0,0), Quaternion(0.000,0.000,-0.0101048669294,0.999948944529)) 
        locations['two'] = Pose(Point(3.74477362633,-0.0526525974274,0.000), Quaternion(0.000,0.000,-0.359452623436,0.93316333592))
        locations['three'] = Pose(Point(3.28888034821,-3.51771521568, 0.000), Quaternion(0.000,0.000,0.999962532728,0.00865639304904))
        locations['four'] = Pose(Point(0.834230601788,-3.44316911697, 0.000), Quaternion(0.000,0.000,0.998966720319,0.0454476808452))
          

        # Publisher to manually control the robot (e.g. to stop it)  
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)  
          
        # Subscribe to the move_base action server  
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)  
        #rospy.loginfo("Waiting for move_base action server...")  
          
        # Wait 60 seconds for the action server to become available  
        #move_base.wait_for_server(rospy.Duration(60))  
          
        rospy.loginfo("Connected to move base server")  
          
        # A variable to hold the initial pose of the robot to be set by   
        # the user in RViz  
        #initial_pose = PoseStamped()  
          
        # Variables to keep track of success rate, running time,  
        # and distance traveled  
        n_locations = len(locations)  
        n_goals = 0  
        n_successes = 0  
        i = 0  
        distance_traveled = 0  
        start_time = rospy.Time.now()  
        running_time = 0  
        location = ""  
        sequeue=['one', 'two', 'three', 'four'] 
          
        # Get the initial pose from the user              
              
        rospy.loginfo("Starting position navigation ")  
        rospy.sleep(2)   
        # Begin the main loop and run through a sequence of locations  
        while not rospy.is_shutdown():  
            # If we've gone through the all sequence, then exit
            if i == n_locations:  
                i = 0
                rospy.logwarn("Now reach all destination, restart...")
                #rospy.signal_shutdown('Quit')  
                continue
              
            # Get the next location in the current sequence  
            location = sequeue[i]  
           
            # Store the last location for distance calculations  

            self.goalMsg = PoseStamped()
            self.goalMsg.header.frame_id = 'map'
            self.goalMsg.pose =locations[location] 
            self.goalMsg.header.stamp = rospy.Time.now() 

            # Let the user know where the robot is going next  
            rospy.loginfo("Going to: " + str(location))   
            # Start the robot toward the next location  
            #self.move_base.send_goal(self.goal) #move_base.send_goal() 
            self.pub.publish(self.goalMsg)  
            rospy.sleep(Time) 
            # Increment the counters  
            i += 1  
            n_goals += 1  
          
            
 
            #rospy.loginfo("Initial goal published! Goal ID is: %d", self.goalId)            
           
    def update_initial_pose(self, initial_pose):  
        self.initial_pose = initial_pose  
  
    def shutdown(self):  
        rospy.loginfo("Stopping the robot...")  
        self.move_base.cancel_goal()  
        rospy.sleep(2)  
        self.cmd_vel_pub.publish(Twist())  
        rospy.sleep(1)  
        
def trunc(f, n):  
    # Truncates/pads a float f to n decimal places without rounding  
    slen = len('%.*f' % (n, f))  
    return float(str(f)[:slen])  
  
if __name__ == '__main__':  
    try:  
        PositionNav()  
        rospy.spin()  
    except rospy.ROSInterruptException:  
        rospy.signal_shutdown('Quit')  
        rospy.loginfo("AMCL position navigation finished.")  

