#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
def talker():
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=1000)
    rospy.init_node('sendgoal', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(data)
        rate.sleep(0.1)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass