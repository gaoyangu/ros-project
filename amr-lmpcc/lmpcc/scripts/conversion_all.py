#!/usr/bin/env python
"""
Converts /jackal*/predicted_trajectory  into /ellipse_objects_feed 
"""
import rospy
import message_filters
from nav_msgs.msg import Path
from lmpcc_msgs.msg import lmpcc_obstacle_array, lmpcc_obstacle

def callback(path_01, path_02, path_03, path_04, path_05, path_06):
    # rospy.loginfo("new Message")
    path = [path_01, path_02, path_03, path_04, path_05, path_06]

    obstacle_array = lmpcc_obstacle_array()
    obstacle_array.header = path_01.header

    for i in [0,1,2,3,4,5]:
        obstacle = lmpcc_obstacle()
        obstacle.trajectory.poses = path[i].poses
        rospy.loginfo("%.2f" % (obstacle.trajectory.poses[0].pose.position.x))
        obstacle_array.lmpcc_obstacles.append(obstacle)
    
    pub.publish(obstacle_array)
    
# Initialize node
rospy.init_node("conversion_all")

# Create publisher and subscriber
inputTopic_01 = rospy.resolve_name("/jackal0/predicted_trajectory")
inputTopic_02 = rospy.resolve_name("/jackal1/predicted_trajectory")
inputTopic_03 = rospy.resolve_name("/jackal2/predicted_trajectory")
inputTopic_04 = rospy.resolve_name("/jackal3/predicted_trajectory")
inputTopic_05 = rospy.resolve_name("/jackal4/predicted_trajectory")
inputTopic_06 = rospy.resolve_name("/jackal5/predicted_trajectory")

outputTopic = rospy.resolve_name("/objects_feed")

sub_01 = message_filters.Subscriber(inputTopic_01, Path)
sub_02 = message_filters.Subscriber(inputTopic_02, Path)
sub_03 = message_filters.Subscriber(inputTopic_03, Path)
sub_04 = message_filters.Subscriber(inputTopic_04, Path)
sub_05 = message_filters.Subscriber(inputTopic_05, Path)
sub_06 = message_filters.Subscriber(inputTopic_06, Path)

ts = message_filters.TimeSynchronizer([sub_01, sub_02, sub_03, sub_04, sub_05, sub_06], 10)
ts.registerCallback(callback)

pub = rospy.Publisher(outputTopic, lmpcc_obstacle_array, queue_size=10)

rospy.loginfo("Re-publishing")
rospy.spin()