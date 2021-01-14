// ros includes
#include <ros/ros.h>
#include <lmpcc_msgs/RobotStatus.h>

#include <string>

using namespace std;

unsigned int teamSize;

ros::Subscriber team_status_sub;
ros::Time timeBegin;
ros::Time timeEnd;
ros::Duration goal_time;

bool startPlan;
int flag;

void teamStatusCallback(const lmpcc_msgs::RobotStatus& status_msg)
{
    int robot_id = status_msg.robot_id;
    bool ready = status_msg.is_ready;
    if(ready && flag == 0){
        flag++;
        timeEnd = ros::Time::now();
        goal_time = timeEnd - timeBegin ;
        ROS_INFO("Robot %d id ready!", robot_id);
        ROS_INFO("using time: %f !", goal_time.toSec());
    }
}

int main(int argc, char** argv)
{
    if(argc < 2){
        ROS_ERROR("You must specify team size.");
        return -1;
    }

    char * teamSizeStr = argv[1];
    teamSize = atoi(teamSizeStr);

    flag = 0;

    ros::init(argc, argv, "team_monitor");
    ros::NodeHandle nh;

    team_status_sub = nh.subscribe("mbot_1/goal_status", 1, &teamStatusCallback);

    while(ros::ok()){

        nh.getParam("mbot_1/plan", startPlan);

        if(startPlan){
            timeBegin = ros::Time::now();
            ROS_INFO("startPlan == true");
        }
        else{
            ROS_INFO("startPlan == false");
        }
        
    }

    // ros::spin();
    return 0;
}