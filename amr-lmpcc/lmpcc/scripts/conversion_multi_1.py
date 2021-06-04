#!/usr/bin/env python
"""
Converts /mobt_1/predicted_trajectory and /mobt_2/predicted_trajectory into /mbot_3/ellipse_objects_feed 
"""
import rospy
import message_filters
from nav_msgs.msg import Path
from lmpcc_msgs.msg import lmpcc_obstacle_array, lmpcc_obstacle

def callback(path_01):
    # rospy.loginfo("new Message")
    path_list = [path_01]
    obstacle_array = lmpcc_obstacle_array()
    obstacle_array.header = path_01.header

    for path in path_list:
        obstacle = lmpcc_obstacle()
        obstacle.trajectory.poses = path.poses
        # rospy.loginfo("pose: %.2f " % obstacle.trajectory.poses[0].pose.position.x)
        for pose in path.poses:
            obstacle.major_semiaxis.append(0.2)
            obstacle.minor_semiaxis.append(0.2)
        obstacle_array.lmpcc_obstacles.append(obstacle)

    if len(obstacle_array.lmpcc_obstacles) < 4:
        for obst_it in range(len(obstacle_array.lmpcc_obstacles), 4):
            obstacle = lmpcc_obstacle()
            obstacle.pose.position.x = -100
            obstacle.pose.position.y = 0
            obstacle.pose.position.z = 0
            obstacle_array.lmpcc_obstacles.append(obstacle)
    # rospy.loginfo("size: %.2f " % len(obstacle_array.lmpcc_obstacles) )        
    pub.publish(obstacle_array)
    

# Initialize node
rospy.init_node("conversion_multi_1")

# Create publisher and subscriber
inputTopic_01 = rospy.resolve_name("/jackal0/predicted_trajectory")
outputTopic = rospy.resolve_name("/jackal1/ellipse_objects_feed")

sub_01 = message_filters.Subscriber(inputTopic_01, Path)

ts = message_filters.TimeSynchronizer([sub_01], 10)
ts.registerCallback(callback)

pub = rospy.Publisher(outputTopic, lmpcc_obstacle_array, queue_size=5)

rospy.loginfo("Re-publishing")
rospy.spin()