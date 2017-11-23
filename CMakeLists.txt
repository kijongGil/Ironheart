cmake_minimum_required(VERSION 2.8.3)
project(autorace)


find_package(catkin REQUIRED COMPONENTS roscpp std_msgs geometry_msgs message_generation rospy)

## Declare ROS messages and services
add_message_files(FILES forwardVision.msg)

## Generate added messages and services
generate_messages(DEPENDENCIES std_msgs geometry_msgs)

catkin_package(
  #INCLUDE_DIRS include
  LIBRARIES autorace
  CATKIN_DEPENDS roscpp std_msgs geometry_msgs message_runtime rospy
  DEPENDS system_lib
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(autorace_main src/autorace_main.cpp)
target_link_libraries(autorace_main ${catkin_LIBRARIES})
add_dependencies(autorace_main autorace_generate_messages_cpp)
