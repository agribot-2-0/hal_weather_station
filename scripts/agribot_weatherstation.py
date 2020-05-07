#!/usr/bin/env python

from std_msgs.msg import Header
from sensor_msgs.msg import Temperature, RelativeHumidity, FluidPressure

import rospy

import serial
import serial.tools.list_ports as list_ports

from agribot_msgs.msg import AgribotWind, AgribotPrecipitation

import weatherstation_commands


class AgribotWeatherstation():
    def __init__(self):
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

    def open_comport(self, port_name, baud_rate):
        print("Opening serial port with baud rate " + str(baud_rate))
        try:
            self.com_port = serial.Serial(port_name, baud_rate, timeout=0)
        except serial.SerialException as ex:
            print(ex)
            print("Couldn't open serial port " + port_name)
            return False
        else:
            print("Port " + port_name + " opened succesfully")
            return True

    def run(self, rate):
        ros_rate = rospy.Rate(rate)
        while not rospy.is_shutdown():
            request = weatherstation_commands.request_all_data(0)
            self.com_port.write(request)
            data_received = self.com_port.in_waiting
            if data_received > 0:
                data = self.com_port.read(data_received)
                data_lines = data.replace("\r\n", ", ")
                output = weatherstation_commands.parse_response(data_lines)

                wind_data = [output[k] for k in [
                    "Dn", "Dm", "Dx", "Sn", "Sm", "Sx"]]
                if not all(x is None for x in wind_data):
                    self.send_wind_message(output)

                rain_data = [output[k] for k in ["Rc", "Rd", "Ri", "Rp"]]
                if not all(x is None for x in rain_data):
                    self.send_rain_message(output)

                hail_data = [output[k] for k in ["Hc", "Hd", "Hi", "Hp"]]
                if not all(x is None for x in hail_data):
                    self.send_hail_message(output)

                if output["Ta"] is not None:
                    self.send_temperature_message(output)

                if output["Ua"] is not None:
                    self.send_humidity_message(output)

                if output["Pa"] is not None:
                    self.send_pressure_message(output)

            ros_rate.sleep()

    def send_wind_message(self, output):
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

    def send_rain_message(self, output):
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

    def send_hail_message(self, output):
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

    def send_temperature_message(self, output):
        temperature_msg = Temperature()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        temperature_msg.header = header
        temperature_msg.temperature = float(output["Ta"][0])
        self.temperature_pub.publish(temperature_msg)

    def send_humidity_message(self, output):
        humidity_msg = RelativeHumidity()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        humidity_msg.header = header
        humidity_msg.relative_humidity = float(output["Ua"][0])
        self.humidity_pub.publish(humidity_msg)

    def send_pressure_message(self, output):
        pressure_msg = FluidPressure()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        pressure_msg.header = header
        pressure_msg.fluid_pressure = float(output["Pa"][0])
        self.atmospheric_pressure_pub.publish(pressure_msg)


if __name__ == '__main__':
    try:
        rospy.init_node('agribot_weatherstation')
    except rospy.ROSInterruptException:
        pass
    else:
        port = rospy.get_param("~com_port", "find")
        frequency = rospy.get_param("~frequency", 0.1)
        if port == "find":
            port = list_ports.comports()[0].device
        baud = rospy.get_param("~baud_rate", "19200")
        weatherstation = AgribotWeatherstation()
        if weatherstation.open_comport(port, baud):
            weatherstation.run(frequency)
        else:
            print("Closing node")
