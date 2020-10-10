#!/usr/bin/env python

import tf
import json
import rospy
import roslaunch
import actionlib
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def callback(data):
    return data.data
    
def Run():
    print("CALLED THE INITIALISATION FUNCTION")
    publishers = rospy.Publisher('s', PoseStamped, queue_size=1000)
    #init node
    rospy.init_node('turtle_tf_listener')
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    now = rospy.Time.now()
    #get current position
    listener.waitForTransform("/odom", "/map", now, rospy.Duration(3))
    position, orientation = listener.lookupTransform('/odom', '/map', rospy.Time(0))
    #print(position, orientation)
    #check goal
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    print(1)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position[0]
    goal.target_pose.pose.position.y = 2
    goal.target_pose.pose.position.z = position[2]

    goal.target_pose.pose.orientation.w = 1.0
    command = rospy.Subscriber("/cmd", String, callback)
    print(command.callback())

    end = input()
    print("Finish")
    client.send_goal(goal)
    client.wait_for_result()
    print('run stop')
    
if __name__ == '__main__':
    print("start")
    try:
        run = Run()
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("CAUGHT EXCEPTION")
            #turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
        #decalre all publishers and subscribers
