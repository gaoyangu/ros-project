// ros includes
#include <ros/ros.h>
#include <lmpcc_msgs/RobotStatus.h>

#include <string>

using namespace std;

string robot_id;

ros::Subscriber goal_status_sub;
ros::Subscriber team_status_sub;

ros::Time timeBegin;
ros::Time timeEnd;
ros::Duration goal_time;

int flag;

void goalStatusCallback(const lmpcc_msgs::RobotStatus& status_msg){
    int robot_id = status_msg.robot_id;
    bool ready = status_msg.is_ready;
    if(ready && flag == 0){
        flag++;
        timeEnd = ros::Time::now();
        goal_time = timeEnd - timeBegin ;
        ROS_INFO("Robot %d id get to goal!", robot_id);
        ROS_INFO("using time: %f !", goal_time.toSec());
    }
}

void teamStatusCallback(const lmpcc_msgs::RobotStatus& status_msg){
    if(status_msg.header.frame_id == "monitor"){
        ROS_INFO("Team is ready !");
        //timeBegin = ros::Time::now();
        timeBegin = status_msg.header.stamp;
    }
    else{
        ROS_INFO("Team is NOT ready !!!");
    }   
}

int main(int argc, char** argv)
{
    if(argc < 2){
        ROS_ERROR("You must specify robot id.");
        return -1;
    }

    char *id = argv[1];
    robot_id = id;

    ROS_INFO("robot no. %s", robot_id.c_str());

    flag = 0;

    // string goal_topic_name = "/mbot_";
    // goal_topic_name += robot_id;
    // goal_topic_name += "/goal_status";

    ros::init(argc, argv, "goal_monitor");
    ros::NodeHandle nh;

    // goal_status_sub = nh.subscribe(goal_topic_name, 1, &goalStatusCallback);
    goal_status_sub = nh.subscribe("goal_status", 1, &goalStatusCallback);
    team_status_sub = nh.subscribe("/team_status", 1, &teamStatusCallback);

    ros::spin();
}