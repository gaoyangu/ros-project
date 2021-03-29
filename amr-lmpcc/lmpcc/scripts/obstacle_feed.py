#!/usr/bin/env python
"""
Converts /jackal*/predicted_trajectory  into /ellipse_objects_feed 
"""
import rospy
from lmpcc_msgs.msg import lmpcc_obstacle_array, lmpcc_obstacle

def callback(obstacle_array):
    for i in range(0, priority):
        ellipse_obstacle_array.lmpcc_obstacles.append( obstacle_array.lmpcc_obstacles[i])
    
    if len(ellipse_obstacle_array.lmpcc_obstacles) < 4:
        for obst_it in range(len(obstacle_array.lmpcc_obstacles), 4):
            obstacle = lmpcc_obstacle()
            obstacle.pose.position.x = -100
            obstacle.pose.position.y = 0
            obstacle.pose.position.z = 0
            ellipse_obstacle_array.lmpcc_obstacles.append(obstacle)

    for obs in ellipse_obstacle_array.lmpcc_obstacles:
        rospy.loginfo("%.2f"%(obs.pose.position.x))
    # rospy.loginfo("size: %.2f " % len(obstacle_array.lmpcc_obstacles) )

    pub.publish(ellipse_obstacle_array)

# Initialize node
rospy.init_node("obstacle_feed")
priority = rospy.get_param("/robot_priority", 0)
sub = rospy.Subscriber("/objects_feed", lmpcc_obstacle_array, callback)
pub = rospy.Publisher('/ellipse_objects_feed', lmpcc_obstacle_array, queue_size=5)

ellipse_obstacle_array = lmpcc_obstacle_array()

rospy.spin()
