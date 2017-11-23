#include "ros/ros.h"                                 
#include "autorace/lineVision.h"            
#include "autorace/forwardVision.h"
#include "geometry_msgs/Twist.h"
#include "geometry_msgs/PoseStamped.h"
#include <stdio.h>

#define WHITE_CENTER 240
#define YELLOW_CENTER 80
#define WHITE_DISTANT 25
#define YELLOW_DISTANT 30
#define RATE 2
#define CENTER 160  
#define WHITE_MODE 0
#define YELLOW_MODE 1
#define SLOW 2
#define STOP 3
#define PARK_MODE 4
#define NO_SPACE 5
#define SPACE 6
#define TUNNEL_MODE 7

float vel, angle;
char stats, keep = 0;
int park, park_stats1,park_stats2, park_finish, cnt = 0, tunnel = 0;
void msgCallback1(const autorace::forwardVision::ConstPtr& msg)
{
    int stats;
	float white_1, white_2, yellow_1, yellow_2, white_weight, yellow_weight, front_1, back_1;
 	white_1 = msg->forward_white_1;
 	white_2 = msg->forward_white_2;
 	yellow_1 = msg->forward_yellow_1;
 	yellow_2 = msg->forward_yellow_2; 
	white_weight = white_1 - white_2;	
	yellow_weight = yellow_2 - yellow_1;
	
	stats = msg->forward_stats;
	
    if (stats == WHITE_MODE)
	{
		if(white_weight < 50){
		vel = 0.15;
		front_1 = -(white_2-WHITE_CENTER)/WHITE_CENTER;
        back_1 = ((-WHITE_DISTANT)/(WHITE_DISTANT*RATE*2))+vel*10;
        angle = front_1 * back_1;
		}

		else{
		vel = 0.1;
		front_1 = -(white_2-WHITE_CENTER)/WHITE_CENTER;
        back_1 = ((-WHITE_DISTANT)/(WHITE_DISTANT*RATE*2))+vel*10;
        angle = front_1 * back_1;
		}

	}
	
    else if (stats == YELLOW_MODE)
	{
		if(yellow_weight < 80){
        vel = 0.15;
		front_1 = -(yellow_2-YELLOW_CENTER)/YELLOW_CENTER;
        back_1 = ((-YELLOW_DISTANT)/(YELLOW_DISTANT*RATE*2))+vel*10;
        angle = front_1 * back_1;
		
		}

		else{
        vel = 0.1;
		front_1 = -(yellow_2-YELLOW_CENTER)/YELLOW_CENTER;
        back_1 = ((YELLOW_DISTANT)/(YELLOW_DISTANT*RATE*2))+vel*10;
        angle = front_1 * back_1;

		}

	}
	

    else if(stats == SLOW)
	{
        vel = 0.5;
		front_1 = -(white_2-WHITE_CENTER)/WHITE_CENTER;
        back_1 = ((-WHITE_DISTANT)/(WHITE_DISTANT*RATE*2))+vel*10;
		angle = front_1 * back_1;
	}
    else if(stats == PARK_MODE)
	{
		vel = 0;
		angle = 0;
	}
    else if(stats == PARK_MODE)
	{
		if (park_finish == 0)	park=1;
		else			park=0;
	}
    else if(stats == NO_SPACE)
	{
		park_stats1=1;
		park_stats2=0;
	}
    else if(stats == SPACE)
	{
		park_stats2=1;
		park_stats1=0;
	}
    else if(stats == TUNNEL_MODE)
	{
		tunnel = 1;
	}
}




int main(int argc, char **argv)                         
{
 
  

  ros::init(argc, argv, "autorace_main");                                 
  ros::NodeHandle nh1;
  ros::NodeHandle nh2;
  ros::NodeHandle nh3; 
  ros::Publisher cmd_pub = nh1.advertise<geometry_msgs::Twist>("/cmd_vel", 5);
  ros::Publisher tunnel_pub = nh2.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 5);
  ros::Subscriber forward_sub = nh3.subscribe("forwardVision", 5, msgCallback1);
  ros::Rate loop_rate(20);

   
  
 while (ros::ok())
  {
  
  geometry_msgs::PoseStamped goal;
  geometry_msgs::Twist msg;
  ros::spinOnce();

  if (park == 0){

	 msg.linear.x = vel;
	 msg.angular.z = angle;
	 ROS_INFO("angle %f", angle);
  }
  else {
	
        if(park_stats2==1 && cnt == 2) cnt = 5;
	else if (park_stats1==1 && cnt == 2) cnt =2;	

	switch(cnt){

		case 0:
			cnt++;
			msg.linear.x = 0;
            msg.angular.z = -0.8;
			cmd_pub.publish(msg); 
 			sleep(2);
			park=1;
			break;

		case 1:
			cnt++;
			msg.linear.x = 0;
            msg.angular.z = 0;
			cmd_pub.publish(msg); 
 			sleep(1);
			park=1;
			break;

		case 2:
			msg.linear.x = 0.0;
			msg.angular.z = 0.8;
			cmd_pub.publish(msg);
			sleep(2);
			park=1;
			cnt++;
            break;

		case 3:
			msg.linear.x = 0.2;
			msg.angular.z = 0.0;
			cmd_pub.publish(msg);
			sleep(2);
			cnt++;
			park=1;
			break;
		case 4:
			msg.linear.x = 0.0;
			msg.angular.z = -0.8;
			cmd_pub.publish(msg);
			sleep(2);
			cnt++;
			park=1;
			break;

		case 5:
			msg.linear.x = 0.18;
			msg.angular.z = 0.0;			
			cmd_pub.publish(msg); 
			sleep(2.5);
			cnt++;
			park=1;
			break;
		

		case 6:
			msg.linear.x = 0.0;
			msg.angular.z = 0.0;			
			cmd_pub.publish(msg); 
			sleep(1);
			cnt++;
			park=1;
			break;
		case 7:
			msg.linear.x = -0.18;
			msg.angular.z = 0.0;
			cmd_pub.publish(msg); 
			sleep(2.5);
			cnt++;
			park=1;
			break;

		case 8:
			msg.linear.x = 0.0;
			msg.angular.z = 0.8;			
			cmd_pub.publish(msg); 
			sleep(2);
			cnt++;
			park=0;
			park_finish = 1;
			break;


		}
  
  }
      cmd_pub.publish(msg);
	  loop_rate.sleep();   
  if(tunnel == 1){
	goal.pose.position.x = 0;
	goal.pose.position.y = 0;
	goal.pose.position.z = 0;
	goal.pose.orientation.w = 0;
	goal.header.stamp = ros::Time::now();
	goal.header.frame_id = "map";
	tunnel_pub.publish(goal); 
	while(1);
     }
  }
  return 0;
}
