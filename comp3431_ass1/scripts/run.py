#!/usr/bin/env python

import rospy
import roslaunch
import os
from geometry_msgs.msg import PoseStamped
import tf
import json


class Run():
    def __init__(self):
        print("CALLED THE INITIALISATION FUNCTION")
        listener = tf.TransformListener()
        rate = rospy.Rate(10.0)
        #print(11111111111111)
       
        try:
            now = rospy.Time.now()
            listener.waitForTransform("/odom", "/map", now, rospy.Duration(5))
            initialposition = listener.lookupTransform('/odom', '/map', rospy.Time(0))
            print(initialposition)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("CAUGHT EXCEPTION")
            #turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)
        #decalre all publishers and subscribers


if __name__ == '__main__':

    print("STARTING")
    rospy.init_node('turtle_tf_listener')
    run = Run()
    while not rospy.is_shutdown():
        rospy.sleep(0.1)

