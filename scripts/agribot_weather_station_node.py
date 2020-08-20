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
        interface = rospy.get_param("~selected_interface", "tcp")
        weather_station = weather_station_class.AgribotWeatherStation()
        frequency = rospy.get_param("~frequency", 0.1)
        if interface == "usb":
            port = rospy.get_param("~com_port", "find")
            if port == "find":
                port = list_ports.comports()[0].device
            baud = rospy.get_param("~baud_rate", "19200")
            weather_station_address = rospy.get_param("~address", "0")
            if weather_station.open_com_port(port, baud):
                weather_station.run(frequency, weather_station_address)
            else:
                rospy.loginfo("Closing node. Com port was not created.")
        if interface == "tcp":
            weather_station_ip = rospy.get_param("~ip_address", "192.168.1.1")
            weather_station_port = rospy.get_param("~port", "54321")
            weather_station_address = (weather_station_ip,
                                       weather_station_port)
            if weather_station.open_tcp_connection(weather_station_address):
                weather_station.run(frequency)
