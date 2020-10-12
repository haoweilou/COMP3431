#!/usr/bin/env python
import tf
import json
import rospy
import roslaunch
import actionlib
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

#initialise launch file and get initial pose & position
def exploreStart():
    rospy.init_node('Lang', anonymous=True)
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    explore = ['comp3431_ass1', 'explore.launch']
    roslaunch_explore =roslaunch.rlutil.resolve_launch_arguments(explore)
    launch = roslaunch.parent.ROSLaunchParent(uuid,roslaunch_explore)
    launch.start()
    rospy.loginfo("Start Explore")
    #get initial postion
    listener = tf.TransformListener()
    rate = rospy.Rate(10.0)
    now = rospy.Time.now()
    #get current position
    listener.waitForTransform("/odom", "/map", rospy.Time(0), rospy.Duration(3))
    position, orientation = listener.lookupTransform('/odom', '/map', rospy.Time(0))
    return position

#send start message so robot can run
def startRun():
    rate = rospy.Rate(10)
    rospy.loginfo("Send start")
    for i in range(10):
        rate.sleep()
        pub = rospy.Publisher('cmd', String, queue_size=10)
        rospy.loginfo('start')
        pub.publish('start')

#start navigation
def navigation():
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    navigation = ['comp3431_ass1', 'navigation.launch']
    roslaunch_navigation =roslaunch.rlutil.resolve_launch_arguments(navigation)
    launch = roslaunch.parent.ROSLaunchParent(uuid,roslaunch_navigation)
    launch.start()
    rospy.loginfo("Start Explore")

def backToInitialGoal(position):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position[0]
    goal.target_pose.pose.position.y = position[1]
    goal.target_pose.pose.position.z = position[2]

    goal.target_pose.pose.orientation.w = 1.0
    client.send_goal(goal)
    client.wait_for_result()

endcondition = None
def callback(data):
    global endcondition
    endcondition = data.data
    #rospy.loginfo(endcondition.data)

if __name__ == "__main__":
    initial_pose = exploreStart()
    navigation()
    #startRun()
    string = ''
    while string != 'stop':
        command = rospy.Subscriber("/cmd", String, callback)
        global endcondition
        print(string)
        string = endcondition
    print('stop')
    backToInitialGoal(initial_pose)
    rospy.spin()
