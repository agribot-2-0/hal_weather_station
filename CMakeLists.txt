cmake_minimum_required(VERSION 2.8.3)
project(hal_weather_station)

find_package(catkin REQUIRED COMPONENTS
   rospy
   std_msgs
   agribot_msgs
   sensor_msgs
   message_generation
)

catkin_package(

)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
   
catkin_install_python(PROGRAMS
   scripts/agribot_weather_station_node.py
   scripts/weather_station_class.py
   scripts/weather_station_commands.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ".svn" EXCLUDE
)
