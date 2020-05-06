#!/usr/bin/env python

import rospy

import serial
import serial.tools.list_ports as list_ports

from std_msgs.msg import Header
from sensor_msgs.msg import Temperature, RelativeHumidity, FluidPressure
from agribot_msgs.msg import AgribotWind, AgribotPrecipitation

from weatherstation_commands import Commands


class AgribotWeatherstation():
    def __init__(self):
        self.port = rospy.get_param("~com_port", "find")
        self.rate = rospy.get_param("~frequency", 0.1)
        if self.port == "find":
            self.port = list_ports.comports()[0].device
        self.baud_rate = rospy.get_param("~baud_rate", "19200")
        self.com_port = None
        self.temperature_pub = None
        self.humidity_pub = None
        self.atmospheric_pressure_pub = None
        self.wind_speed_pub = None
        self.rain_level_pub = None
        self.hail_level_pub = None
        self.create_publishers()

    def create_publishers(self):
        self.temperature_pub = rospy.Publisher(
            "weather_station/temperature", Temperature, queue_size=1)
        self.humidity_pub = rospy.Publisher(
            "weather_station/humidity", RelativeHumidity, queue_size=1)
        self.atmospheric_pressure_pub = rospy.Publisher(
            "weather_station/atmospheric_pressure", FluidPressure, queue_size=1)
        self.wind_speed_pub = rospy.Publisher(
            "weather_station/wind_speed", AgribotWind, queue_size=1)
        self.rain_level_pub = rospy.Publisher(
            "weather_station/rain_level", AgribotPrecipitation, queue_size=1)
        self.hail_level_pub = rospy.Publisher(
            "weather_station/hail_level", AgribotPrecipitation, queue_size=1)

    def open_comport(self):
        print("Opening serial port with baud rate " + str(self.baud_rate))
        try:
            self.com_port = serial.Serial(self.port, self.baud_rate, timeout=0)
        except serial.SerialException as ex:
            print(ex)
            print("Couldn't open serial port " + self.port)
            return False
        else:
            print("Port " + self.port + " opened succesfully")
            return True



    def run(self):
        ros_rate = rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            request = Commands().request_all_data(0)
            self.com_port.write(request)
            data_received = self.com_port.in_waiting
            if data_received > 0:
                data = self.com_port.read(data_received)
                data_lines = data.replace("\r\n", ", ")
                output = Commands().parse_response(data_lines)

                wind_data = [output[k] for k in [
                    "Dn", "Dm", "Dx", "Sn", "Sm", "Sx"]]
                if not all(x is None for x in wind_data):
                    wind_msg = AgribotWind()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    wind_msg.header = header
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
                    self.wind_speed_pub.publish(wind_msg)

                rain_data = [output[k] for k in ["Rc", "Rd", "Ri", "Rp"]]
                if not all(x is None for x in rain_data):
                    rain_msg = AgribotPrecipitation()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    rain_msg.header = header
                    if output["Rc"] is not None:
                        rain_msg.accumulation = float(output["Rc"][0])
                    if output["Rd"] is not None:
                        rain_msg.duration = float(output["Rd"][0])
                    if output["Ri"] is not None:
                        rain_msg.intensity = float(output["Ri"][0])
                    if output["Rp"] is not None:
                        rain_msg.peak_intensity = float(output["Rp"][0])
                    self.rain_level_pub.publish(rain_msg)

                hail_data = [output[k] for k in ["Hc", "Hd", "Hi", "Hp"]]
                if not all(x is None for x in hail_data):
                    hail_msg = AgribotPrecipitation()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    hail_msg.header = header
                    if output["Hc"] is not None:
                        hail_msg.accumulation = float(output["Hc"][0])
                    if output["Hd"] is not None:
                        hail_msg.duration = float(output["Hd"][0])
                    if output["Hi"] is not None:
                        hail_msg.intensity = float(output["Hi"][0])
                    if output["Hp"] is not None:
                        hail_msg.peak_intensity = float(output["Hp"][0])
                    self.hail_level_pub.publish(hail_msg)

                if output["Ta"] is not None:
                    temperature_msg = Temperature()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    temperature_msg.header = header
                    temperature_msg.temperature = float(output["Ta"][0])
                    self.temperature_pub.publish(temperature_msg)

                if output["Ua"] is not None:
                    humidity_msg = RelativeHumidity()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    humidity_msg.header = header
                    humidity_msg.relative_humidity = float(output["Ua"][0])
                    self.humidity_pub.publish(humidity_msg)

                if output["Pa"] is not None:
                    pressure_msg = FluidPressure()
                    header = Header()
                    header.stamp = rospy.Time.now()
                    header.frame_id = "base_footprint"
                    pressure_msg.header = header
                    pressure_msg.fluid_pressure = float(output["Pa"][0])
                    self.atmospheric_pressure_pub.publish(pressure_msg)

            ros_rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('agribot_weatherstation')
    except rospy.ROSInterruptException:
        pass
    else:
        weatherstation = AgribotWeatherstation()
        if weatherstation.open_comport():
            weatherstation.run()
        else:
            print("Closing node")
