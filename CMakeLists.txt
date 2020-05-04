cmake_minimum_required(VERSION 2.8.3)
project(hal_weatherstation)

find_package(catkin REQUIRED COMPONENTS
   rospy
   serial
   std_msgs
   agribot_msgs
)

catkin_package(

)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS
   scripts/agribot_weatherstation.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
