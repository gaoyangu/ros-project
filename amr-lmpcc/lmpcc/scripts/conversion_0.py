#!/usr/bin/env python
"""
Converts /mobt_1/predicted_trajectory into /mbot_2/ellipse_objects_feed 
"""
import rospy
from nav_msgs.msg import Path
from lmpcc_msgs.msg import lmpcc_obstacle_array, lmpcc_obstacle

def newMessageReceived(path):
    # rospy.loginfo("new Message")

    obstacle_array = lmpcc_obstacle_array()
    obstacle_array.header = path.header

    obstacle = lmpcc_obstacle()
    obstacle.trajectory.poses = path.poses

    for pose in path.poses:
        # rospy.loginfo("%.2f" % (pose.pose.position.x))
        obstacle.major_semiaxis.append(0.2)
        obstacle.minor_semiaxis.append(0.2)

    obstacle_array.lmpcc_obstacles.append(obstacle)

    # rospy.loginfo("size: %.2f " % len(obstacle_array.lmpcc_obstacles) )
    if len(obstacle_array.lmpcc_obstacles) < 4:
        for obst_it in range(len(obstacle_array.lmpcc_obstacles), 4):
            obstacle.pose.position.x = -100
            obstacle.pose.position.y = 0
            obstacle.pose.position.z = 0
            obstacle_array.lmpcc_obstacles.append(obstacle)
    # rospy.loginfo("size: %.2f " % len(obstacle_array.lmpcc_obstacles) )

    pub.publish(obstacle_array)
    

# Initialize node
rospy.init_node("conversion")

# Create publisher and subscriber
inputTopic = rospy.resolve_name("/jackal0/predicted_trajectory")
outputTopic = rospy.resolve_name("/jackal5/ellipse_objects_feed")
sub = rospy.Subscriber(inputTopic, Path, newMessageReceived, queue_size=5)
pub = rospy.Publisher(outputTopic, lmpcc_obstacle_array, queue_size=5)

rospy.loginfo("Re-publishing")
rospy.spin()