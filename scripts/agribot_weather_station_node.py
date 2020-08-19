#!/usr/bin/env python

import rospy

import serial.tools.list_ports as list_ports
import socket

import weather_station_class

BUFF_SIZE = 100

if __name__ == '__main__':
    try:
        rospy.init_node('agribot_weather_station')
    except rospy.ROSInterruptException:
        pass
    else:
        interface = rospy.get_param("~selected_interface", "tcp")
        if interface == "usb":
            port = rospy.get_param("~com_port", "find")
            frequency = rospy.get_param("~frequency", 0.1)
            if port == "find":
                port = list_ports.comports()[0].device
            baud = rospy.get_param("~baud_rate", "19200")
            weather_station_address = rospy.get_param("~address", "0")
            weather_station = weather_station_class.AgribotWeatherStation()
            if weather_station.open_com_port(port, baud):
                weather_station.run(frequency, weather_station_address)
            else:
                rospy.loginfo("Closing node")
        if interface == "tcp":
            weather_station_ip = rospy.get_param("~ip_address", "192.168.1.1")
            weather_station_port = rospy.get_param("~port", "54321")
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            weather_station_address = (weather_station_ip,
                                       weather_station_port)
            socket.connect(weather_station_address)
            try:
                while True:
                    data = socket.recv(BUFF_SIZE)
                    rospy.loginfo("received %s", data)

            finally:
                rospy.loginfo('disconnected')
                socket.close()

