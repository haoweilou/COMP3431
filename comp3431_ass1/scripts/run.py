#!/usr/bin/env python

import rospy
import roslaunch
import actionlib
import os
from geometry_msgs.msg import PoseStamped
import tf
import json
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def Run():
    print("CALLED THE INITIALISATION FUNCTION")
    publishers = rospy.Publisher('s', PoseStamped, queue_size=1000)
    rospy.init_node('turtle_tf_listener')
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    now = rospy.Time.now()
    listener.waitForTransform("/odom", "/map", now, rospy.Duration(3))
    position, orientation = listener.lookupTransform('/odom', '/map', rospy.Time(0))
    print(position, orientation)
    
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    print(1)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position[0]
    goal.target_pose.pose.position.y = position[1]
    goal.target_pose.pose.position.z = position[2]

    goal.target_pose.pose.orientation.w = 1.0
    

    client.send_goal(goal)        
    while not rospy.is_shutdown():
        #rospy.loginfo(initialposition)
        #publishers.publish(initialposition)
        #print(initialposition)
        rate.sleep()
        break
    print('run stop')
#
# rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped  '{header: {stamp: now, frame_id: "map"}, pose: {position: {x: -0.209999740124, y: 1.78999996185, z: 0.0}, orientation: {w: 1.0}}}'
if __name__ == '__main__':
    print("start")
    try:
        run = Run()
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("CAUGHT EXCEPTION")
            #turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
        #decalre all publishers and subscribers
