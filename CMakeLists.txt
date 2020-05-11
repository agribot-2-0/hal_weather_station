cmake_minimum_required(VERSION 2.8.3)
project(hal_weather_station)

find_package(catkin REQUIRED COMPONENTS
   rospy
   serial
   std_msgs
   agribot_msgs
   sensor_msgs
   message_generation
)

add_service_files(
   FILES
   ChangeCommunicationSettings.srv
   ChangeSupervisorSettings.srv
   ResetPrecipitationIntensity.srv
   ChangePrecipitationSettings.srv
   ChangeWindSettings.srv
   ChangePresTempHumSettings.srv
   ResetPrecipitationcounter.srv
)

generate_messages(
   DEPENDENCIES
   std_msgs
)

catkin_package(

)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
   
      ## Mark executable scripts (Python etc.) for installation
      ## in contrast to setup.py, you can choose the destination
catkin_install_python(PROGRAMS
   scripts/agribot_weather_station_node.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
