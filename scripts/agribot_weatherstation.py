#!/usr/bin/env python

import rospy

import serial
import serial.tools.list_ports as list_ports

from std_msgs.msg import Float32
from agribot_msgs.msg import AgribotWind, AgribotPrecipitation

import weatherstation_commands

TEMPERATURE_PUB = rospy.Publisher(
    "weather_station/temperature", Float32, queue_size=1)
HUMIDITY_PUB = rospy.Publisher(
    "weather_station/humidity", Float32, queue_size=1)
ATMOSPHERIC_PRESSURE_PUB = rospy.Publisher(
    "weather_station/atmospheric_pressure", Float32, queue_size=1)
WIND_SPEED_PUB = rospy.Publisher(
    "weather_station/wind_speed", AgribotWind, queue_size=1)
RAIN_LEVEL_PUB = rospy.Publisher(
    "weather_station/rain_level", AgribotPrecipitation, queue_size=1)
HAIL_LEVEL_PUB = rospy.Publisher(
    "weather_station/hail_level", AgribotPrecipitation, queue_size=1)


def agribot_weatherstation(com_port, rate):
    ros_rate = rospy.Rate(rate)
    while not rospy.is_shutdown():
        com_port.write(weatherstation_commands.request_all_data(0))
        data_received = com_port.in_waiting
        if data_received > 0:
            data = com_port.read(data_received)
            data_lines = data.replace("\r\n", ", ")
            output = weatherstation_commands.parse_response(data_lines)
            wind_data = [output[k] for k in [
                "Dn", "Dm", "Dx", "Sn", "Sm", "Sx"]]
            if not all(x is None for x in wind_data):
                wind_msg = AgribotWind()
                if output["Dn"] is not None:
                    wind_msg.minimum_direction = float(output["Dn"][0])
                if output["Dm"] is not None:
                    wind_msg.average_direction = float(output["Dm"][0])
                if output["Dx"] is not None:
                    wind_msg.maximum_direction = float(output["Dx"][0])
                if output["Sn"] is not None:
                    wind_msg.minimum_speed = float(output["Sn"][0])
                if output["Sm"] is not None:
                    wind_msg.average_speed = float(output["Sm"][0])
                if output["Sx"] is not None:
                    wind_msg.maximum_speed = float(output["Sx"][0])
                WIND_SPEED_PUB.publish(wind_msg)

            rain_data = [output[k] for k in ["Rc", "Rd", "Ri", "Rp"]]
            if not all(x is None for x in rain_data):
                rain_msg = AgribotPrecipitation()
                if output["Rc"] is not None:
                    rain_msg.accumulation = float(output["Rc"][0])
                if output["Rd"] is not None:
                    rain_msg.duration = float(output["Rd"][0])
                if output["Ri"] is not None:
                    rain_msg.intensity = float(output["Ri"][0])
                if output["Rp"] is not None:
                    rain_msg.peak_intensity = float(output["Rp"][0])
                RAIN_LEVEL_PUB.publish(rain_msg)

            hail_data = [output[k] for k in ["Hc", "Hd", "Hi", "Hp"]]
            if not all(x is None for x in hail_data):
                hail_msg = AgribotPrecipitation()
                if output["Hc"] is not None:
                    hail_msg.accumulation = float(output["Hc"][0])
                if output["Hd"] is not None:
                    hail_msg.duration = float(output["Hd"][0])
                if output["Hi"] is not None:
                    hail_msg.intensity = float(output["Hi"][0])
                if output["Hp"] is not None:
                    hail_msg.peak_intensity = float(output["Hp"][0])
                HAIL_LEVEL_PUB.publish(hail_msg)

            if output["Ta"] is not None:
                temperature_msg = Float32()
                temperature_msg.data = float(output["Ta"][0])
                TEMPERATURE_PUB.publish(temperature_msg)

            if output["Ua"] is not None:
                humidity_msg = Float32()
                humidity_msg.data = float(output["Ua"][0])
                HUMIDITY_PUB.publish(humidity_msg)

            if output["Pa"] is not None:
                pressure_msg = Float32()
                pressure_msg.data = float(output["Pa"][0])
                ATMOSPHERIC_PRESSURE_PUB.publish(pressure_msg)

        ros_rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('agribot_weatherstation')
        PORT = rospy.get_param("~com_port", "find")
        FREQUENCY = rospy.get_param("~frequency", 0.1)
        if PORT == "find":
            PORT = list_ports.comports()[0].device
        BAUD_RATE = rospy.get_param("~baud_rate", "19200")

        try:
            print("Opening serial port with baud rate " + str(BAUD_RATE))
            COM = serial.Serial(PORT, BAUD_RATE, timeout=0)
        except serial.SerialException as ex:
            print(ex)
            print("Couldn't open serial port " + PORT)
        else:
            print("Port " + PORT + " opened succesfully")
            agribot_weatherstation(COM, FREQUENCY)
    except rospy.ROSInterruptException:
        pass
