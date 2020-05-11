#!/usr/bin/env python

import rospy

import serial.tools.list_ports as list_ports

import weather_station_class

if __name__ == '__main__':
    try:
        rospy.init_node('agribot_weather_station')
    except rospy.ROSInterruptException:
        pass
    else:
        port = rospy.get_param("~com_port", "find")
        frequency = rospy.get_param("~frequency", 0.1)
        if port == "find":
            port = list_ports.comports()[0].device
        baud = rospy.get_param("~baud_rate", "19200")
        weather_station_address = rospy.get_param("~address", "0")
        weather_station = weather_station_class.AgribotWeatherStation()
        if weather_station.open_comport(port, baud):
            weather_station.run(frequency, weather_station_address)
        else:
            rospy.loginfo("Closing node")
