#!/usr/bin/env python

import rospy

import serial

from std_msgs.msg import Header
from sensor_msgs.msg import Temperature, RelativeHumidity, FluidPressure
from agribot_msgs.msg import AgribotWind, AgribotPrecipitation

from hal_weather_station.srv import (
    ChangeCommunicationSettings,
    ChangeSupervisorSettings,
    ResetPrecipitationIntensity,
    ChangePrecipitationSettings,
    ChangeWindSettings,
    ChangePresTempHumSettings,
    ResetPrecipitationcounter
)

import weather_station_commands

SENSORS_PREFIX = "R"
SETTINGS_PREFIX = "X"


class AgribotWeatherStation():
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.com_port = None
        self.temperature_pub = None
        self.humidity_pub = None
        self.atmospheric_pressure_pub = None
        self.wind_speed_pub = None
        self.rain_level_pub = None
        self.hail_level_pub = None
        self.station_address = 0
        self.create_publishers()
        self.create_services()

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

    def create_services(self):
        rospy.Service(
            'change_communication_settings',
            ChangeCommunicationSettings,
            self.change_communication_settings)
        rospy.Service(
            'change_supervisor_settings',
            ChangeSupervisorSettings,
            self.change_supervisor_settings)
        rospy.Service(
            'change_wind_settings',
            ChangeWindSettings,
            self.change_wind_settings)
        rospy.Service(
            'change_pres_temp_hum_settings',
            ChangePresTempHumSettings,
            self.change_pres_temp_hum_settings)
        rospy.Service(
            'change_precipitation_settings',
            ChangePrecipitationSettings,
            self.change_precipitation_settings)
        rospy.Service(
            'reset_precipitation_counter',
            ResetPrecipitationcounter,
            self.reset_precipitation_counter)
        rospy.Service(
            'reset_precipitation_intensity',
            ResetPrecipitationIntensity,
            self.reset_precipitation_intensity)

    def open_com_port(self, port_name, baud_rate):
        rospy.loginfo("Opening serial port with baud rate %s", str(baud_rate))
        try:
            self.com_port = serial.Serial(port_name, baud_rate, timeout=0)
        except serial.SerialException as ex:
            rospy.logerr(str(ex))
            rospy.logerr("Couldn't open serial port %s", port_name)
            return False
        else:
            rospy.loginfo("Port %s opened succesfully", port_name)
            return True

    def run(self, rate, station_address):
        ros_rate = rospy.Rate(rate)
        self.station_address = station_address
        received = ""
        while not rospy.is_shutdown():
            self.send_requests()

            data_received = self.com_port.in_waiting
            if data_received > 0:
                received = self.com_port.read(data_received)

            try:
                self.publish_sensors_data(received)
                self.display_communication_settings(received)
            except IndexError:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            ros_rate.sleep()

    def send_requests(self):
        requests = (
            weather_station_commands.request_communication_settings(self.station_address),
            weather_station_commands.request_all_data(self.station_address)
        )
        for request in requests:
            self.com_port.write(request)

    def send_wind_message(self, data):
        wind_msg = AgribotWind()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        wind_msg.header = header
        wind_msg.direction_variance = 3.0 # +- degrees
        wind_msg.speed_variance = 3 # +- percent
        wind_msg.minimum_direction = data["minimum_direction"] # degrees
        wind_msg.average_direction = data["average_direction"] # degrees
        wind_msg.maximum_direction = data["maximum_direction"] # degrees
        wind_msg.minimum_speed = data["minimum_speed"] # m/s
        wind_msg.average_speed = data["average_speed"] # m/s
        wind_msg.maximum_speed = data["maximum_speed"] # m/s
        self.wind_speed_pub.publish(wind_msg)

    def send_rain_message(self, data):
        rain_msg = AgribotPrecipitation()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        rain_msg.header = header
        rain_msg.accumulation = data["accumulation"] # mm
        rain_msg.duration = data["duration"] # s
        rain_msg.intensity = data["intensity"] # mm/h
        rain_msg.peak_intensity = data["peak_intensity"] # mm/h
        self.rain_level_pub.publish(rain_msg)

    def send_hail_message(self, data):
        hail_msg = AgribotPrecipitation()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        hail_msg.header = header
        hail_msg.accumulation = data["accumulation"] # hits/cm^2
        hail_msg.duration = data["duration"] # s
        hail_msg.intensity = data["intensity"] # hits/cm^2/h
        hail_msg.peak_intensity = data["peak_intensity"] # hits/cm^2/h
        self.hail_level_pub.publish(hail_msg)

    def send_temperature_message(self, data):
        temperature_msg = Temperature()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        temperature_msg.header = header
        temperature_msg.variance = 0.3 # +- Celsius deg
        temperature_msg.temperature = data["temperature"] # Celsius deg
        self.temperature_pub.publish(temperature_msg)

    def send_humidity_message(self, data):
        humidity_msg = RelativeHumidity()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        humidity_msg.header = header
        humidity_msg.variance = 3.0 # +- percent point
        humidity_msg.relative_humidity = data["humidity"] # percent
        self.humidity_pub.publish(humidity_msg)

    def send_pressure_message(self, data):
        pressure_msg = FluidPressure()
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = "base_footprint"
        pressure_msg.header = header
        pressure_msg.variance = 0.5 # +- hPa
        pressure_msg.fluid_pressure = data["pressure"] # hPa
        self.atmospheric_pressure_pub.publish(pressure_msg)

    def display_communication_settings(self, received):
        # pylint: disable=no-self-use
        for data in received.split("\r\n")[:-1]:
            if data[1] == SETTINGS_PREFIX:
                output = weather_station_commands.parse_communication(data)
                output_to_print = "Address = " + output["A"] + "\n"
                output_to_print += "Protocol = " + output["M"] + "\n"
                output_to_print += "Interface = " + output["C"] + "\n"
                output_to_print += "Interval = " + output["I"] + "\n"
                output_to_print += "Baud rate = " + output["B"] + "\n"
                output_to_print += "Data bits = " + output["D"] + "\n"
                output_to_print += "Parity = " + output["P"] + "\n"
                output_to_print += "Stop bits = " + output["S"] + "\n"
                output_to_print += "Line delay = " + output["L"] + "\n"
                output_to_print += "Device name = " + output["N"] + "\n"
                output_to_print += "Software version = " + output["V"] + "\n"
                output_to_print += "Parameter lock = " + output["H"] + "\n"
                rospy.loginfo("Current communication settings:\n%s", output_to_print)

    def publish_sensors_data(self, received):
        for data in received.split("\r\n")[:-1]:
            if data[1] == SENSORS_PREFIX:
                output = weather_station_commands.parse_response(data)
                wind_data = get_wind_data_from_response(output)
                if wind_data is not None:
                    self.send_wind_message(wind_data)
                rain_data = get_rain_data_from_response(output)
                if rain_data is not None:
                    self.send_rain_message(rain_data)
                hail_data = get_hail_data_from_response(output)
                if hail_data is not None:
                    self.send_hail_message(hail_data)
                temperature_data = get_temperature_data_from_response(output)
                if temperature_data is not None:
                    self.send_temperature_message(temperature_data)
                humidity_data = get_humidity_data_from_response(output)
                if humidity_data is not None:
                    self.send_humidity_message(humidity_data)
                pressure_data = get_pressure_data_from_response(output)
                if pressure_data is not None:
                    self.send_pressure_message(pressure_data)

    def change_communication_settings(self, req):
        # pylint: disable=too-many-branches
        settings = dict()
        if req.address == "":
            settings["address"] = None
        else:
            settings["address"] = req.address
        if req.new_address == "":
            settings["new_address"] = None
        else:
            settings["new_address"] = req.new_address
        if req.protocol == "":
            settings["protocol"] = None
        else:
            settings["protocol"] = req.protocol
        if req.interface == "":
            settings["interface"] = None
        else:
            settings["interface"] = req.interface
        if req.update_interval == "":
            settings["update_interval"] = None
        else:
            settings["update_interval"] = req.update_interval
        if req.baud == "":
            settings["baud"] = None
        else:
            settings["baud"] = req.baud
        if req.data_bit == "":
            settings["data_bit"] = None
        else:
            settings["data_bit"] = req.data_bit
        if req.parity == "":
            settings["parity"] = None
        else:
            settings["parity"] = req.parity
        if req.stop_bits == "":
            settings["stop_bits"] = None
        else:
            settings["stop_bits"] = req.stop_bits
        if req.line_delay == "":
            settings["line_delay"] = None
        else:
            settings["line_delay"] = req.line_delay
        if req.param_lock == "":
            settings["param_lock"] = None
        else:
            settings["param_lock"] = req.param_lock

        request = weather_station_commands.change_communication_settings(
            address=self.station_address,
            new_address=settings.get("new_address"),
            protocol=settings.get("protocol"),
            interface=settings.get("interface"),
            update_interval=settings.get("update_interval"),
            baud=settings.get("baud"),
            data_bits=settings.get("data_bits"),
            parity=settings.get("parity"),
            stop_bits=settings.get("stop_bits"),
            line_delay=settings.get("line_delay"),
            param_lock=settings.get("param_lock")
        )
        self.com_port.write(request)

    def change_supervisor_settings(self, req):
        # pylint: disable=too-many-branches
        settings = dict()
        if req.parameter_selection == "":
            settings["parameter_selection"] = None
        else:
            settings["parameter_selection"] = req.parameter_selection
        if req.update_interval == "":
            settings["update_interval"] = None
        else:
            settings["update_interval"] = req.update_interval
        if req.error_messaging == "":
            settings["error_messaging"] = None
        else:
            settings["error_messaging"] = req.error_messaging
        if req.heating_control == "":
            settings["heating_control"] = None
        else:
            settings["heating_control"] = req.heating_control

        request = weather_station_commands.change_supervisor_settings(
            address=self.station_address,
            parameter_selection=settings.get("parameter_selection"),
            update_interval=settings.get("update_interval"),
            error_messaging=settings.get("error_messaging"),
            heating_control=settings.get("heating_control")
        )
        self.com_port.write(request)

    def change_wind_settings(self, req):
        # pylint: disable=too-many-branches
        settings = dict()
        if req.parameter_selection == "":
            settings["parameter_selection"] = None
        else:
            settings["parameter_selection"] = req.parameter_selection
        if req.update_interval == "":
            settings["update_interval"] = None
        else:
            settings["update_interval"] = req.update_interval
        if req.averaging_time == "":
            settings["averaging_time"] = None
        else:
            settings["averaging_time"] = req.averaging_time
        if req.suprema_mode == "":
            settings["suprema_mode"] = None
        else:
            settings["suprema_mode"] = req.suprema_mode
        if req.speed_unit == "":
            settings["speed_unit"] = None
        else:
            settings["speed_unit"] = req.speed_unit
        if req.direction_offset == "":
            settings["direction_offset"] = None
        else:
            settings["direction_offset"] = req.direction_offset
        if req.sampling_rate == "":
            settings["sampling_rate"] = None
        else:
            settings["sampling_rate"] = req.sampling_rate

        request = weather_station_commands.change_wind_settings(
            address=self.station_address,
            parameter_selection=settings.get("parameter_selection"),
            update_interval=settings.get("update_interval"),
            averaging_time=settings.get("averaging_time"),
            suprema_mode=settings.get(" suprema_mode"),
            speed_unit=settings.get("speed_unit"),
            direction_offset=settings.get("direction_offset"),
            sampling_rate=settings.get("sampling_rate")
        )
        self.com_port.write(request)

    def change_pres_temp_hum_settings(self, req):
        # pylint: disable=too-many-branches
        settings = dict()
        if req.parameter_selection == "":
            settings["parameter_selection"] = None
        else:
            settings["parameter_selection"] = req.parameter_selection
        if req.update_interval == "":
            settings["update_interval"] = None
        else:
            settings["update_interval"] = req.update_interval
        if req.pressure_unit == "":
            settings["pressure_unit"] = None
        else:
            settings["pressure_unit"] = req.pressure_unit
        if req.temperature_unit == "":
            settings["temperature_unit"] = None
        else:
            settings["temperature_unit"] = req.temperature_unit

        request = weather_station_commands.change_pres_temp_hum_settings(
            address=self.station_address,
            parameter_selection=settings.get("parameter_selection"),
            update_interval=settings.get("update_interval"),
            pressure_unit=settings.get("pressure_unit"),
            temperature_unit=settings.get("temperature_unit")
        )
        self.com_port.write(request)

    def change_precipitation_settings(self, req):
        # pylint: disable=too-many-branches
        settings = dict()
        if req.parameter_selection == "":
            settings["parameter_selection"] = None
        else:
            settings["parameter_selection"] = req.parameter_selection
        if req.update_interval == "":
            settings["update_interval"] = None
        else:
            settings["update_interval"] = req.update_interval
        if req.precipitation_unit == "":
            settings["precipitation_unit"] = None
        else:
            settings["precipitation_unit"] = req.precipitation_unit
        if req.hail_unit == "":
            settings["hail_unit"] = None
        else:
            settings["hail_unit"] = req.hail_unit
        if req.autosend_mode == "":
            settings["autosend_mode"] = None
        else:
            settings["autosend_mode"] = req.autosend_mode
        if req.reset_mode == "":
            settings["reset_mode"] = None
        else:
            settings["reset_mode"] = req.reset_mode
        if req.rain_limit == "":
            settings["rain_limit"] = None
        else:
            settings["rain_limit"] = req.rain_limit
        if req.hail_limit == "":
            settings["hail_limit"] = None
        else:
            settings["hail_limit"] = req.hail_limit

        request = weather_station_commands.change_precipitation_settings(
            address=self.station_address,
            parameter_selection=settings.get("parameter_selection"),
            update_interval=settings.get("update_interval"),
            precipitation_unit=settings.get("precipitation_unit"),
            hail_unit=settings.get(" hail_unit"),
            autosend_mode=settings.get("autosend_mode"),
            reset_mode=settings.get("reset_mode"),
            rain_limit=settings.get("rain_limit"),
            hail_limit=settings.get("hail_limit")
        )
        self.com_port.write(request)

    def reset_precipitation_counter(self):
        request = weather_station_commands.precipitation_counter_reset(self.station_address)
        self.com_port.write(request)

    def reset_precipitation_intensity(self):
        request = weather_station_commands.precipitation_intensity_reset(self.station_address)
        self.com_port.write(request)


def get_wind_data_from_response(response):
    wind_data = [response[k] for k in [
        "Dn", "Dm", "Dx", "Sn", "Sm", "Sx"]]
    if not all(x is None for x in wind_data):
        data = {
            "minimum_direction": 0.0,
            "average_direction": 0.0,
            "maximum_direction": 0.0,
            "minimum_speed": 0.0,
            "average_speed": 0.0,
            "maximum_speed": 0.0
        }
        if response["Dn"] is not None:
            data["minimum_direction"] = float(response["Dn"][0])
        if response["Dm"] is not None:
            data["average_direction"] = float(response["Dm"][0])
        if response["Dx"] is not None:
            data["maximum_direction"] = float(response["Dx"][0])
        if response["Sn"] is not None:
            data["minimum_speed"] = float(response["Sn"][0])
        if response["Sm"] is not None:
            data["average_speed"] = float(response["Sm"][0])
        if response["Sx"] is not None:
            data["maximum_speed"] = float(response["Sx"][0])
    else:
        data = None
    return data


def get_rain_data_from_response(response):
    rain_data = [response[k] for k in ["Rc", "Rd", "Ri", "Rp"]]
    if not all(x is None for x in rain_data):
        data = {
            "accumulation": 0.0,
            "duration": 0.0,
            "intensity": 0.0,
            "peak_intensity": 0.0
        }
        if response["Rc"] is not None:
            data["accumulation"] = float(response["Rc"][0])
        if response["Rd"] is not None:
            data["duration"] = float(response["Rd"][0])
        if response["Ri"] is not None:
            data["intensity"] = float(response["Ri"][0])
        if response["Rp"] is not None:
            data["peak_intensity"] = float(response["Rp"][0])
    else:
        data = None
    return data

def get_hail_data_from_response(response):
    hail_data = [response[k] for k in ["Hc", "Hd", "Hi", "Hp"]]
    if not all(x is None for x in hail_data):
        data = {
            "accumulation": 0.0,
            "duration": 0.0,
            "intensity": 0.0,
            "peak_intensity": 0.0
        }
        if response["Hc"] is not None:
            data["accumulation"] = float(response["Hc"][0])
        if response["Hd"] is not None:
            data["duration"] = float(response["Hd"][0])
        if response["Hi"] is not None:
            data["intensity"] = float(response["Hi"][0])
        if response["Hp"] is not None:
            data["peak_intensity"] = float(response["Hp"][0])
    else:
        data = None
    return data


def get_temperature_data_from_response(response):
    if response["Ta"] is not None:
        data = {
            "temperature": float(response["Ta"][0])
        }
    else:
        data = None
    return data


def get_humidity_data_from_response(response):
    if response["Ua"] is not None:
        data = {
            "humidity": float(response["Ua"][0])
        }
    else:
        data = None
    return data


def get_pressure_data_from_response(response):
    if response["Pa"] is not None:
        data = {
            "pressure": float(response["Pa"][0])
        }
    else:
        data = None
    return data
