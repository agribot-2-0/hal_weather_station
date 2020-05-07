def request_communication_settings(address):
    return str(address) + "XU" + "\r\n"

def change_communication_settings(address,
                                  new_address=None,
                                  protocol=None,
                                  interface=None,
                                  update_interval=None,
                                  baud=None,
                                  data_bits=None,
                                  parity=None,
                                  stop_bits=None,
                                  line_delay=None,
                                  param_lock=None
                                  ):
    # pylint: disable=R0913,R0912,R0915
    request = str(address) + "XU"
    if new_address is not None:
        if isinstance(new_address, str):
            request = request + ",A=" + new_address
        else:
            print("Wrong new address")
    if protocol is not None:
        if protocol in ("A", "a", "P", "p", "Q", "S", "R"):
            request = request + ",M=" + protocol
        else:
            print("Wrong communication protocol")
    if interface is not None:
        if interface in ("1", "2", "3", "4"):
            request = request + ",C=" + interface
        elif interface in (1, 2, 3, 4):
            request = request + ",C=" + str(interface)
        else:
            print("Wrong serial interface")
    if update_interval is not None:
        if is_int_between(update_interval, 1, 3600):
            request = request + ",I=" + str(update_interval)
        else:
            print("Wrong repeat interval")
    if baud is not None:
        if baud in ("1200", "2400", "4800", "9600",
                    "19200", "38400", "57600", "115200"):
            request = request + ",B=" + baud
        elif baud in (1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200):
            request = request + ",B=" + str(baud)
        else:
            print("Wrong baud rate")
    if data_bits is not None:
        if data_bits in ("7", "8"):
            request = request + ",D=" + data_bits
        elif data_bits in (7, 8):
            request = request + ",D=" + str(data_bits)
        else:
            print("Wrong data bits")
    if parity is not None:
        if parity in ("O", "E", "N"):
            request = request + ",P=" + parity
        else:
            print("Wrong parity")
    if stop_bits is not None:
        if stop_bits in ("1", "2"):
            request = request + ",S=" + stop_bits
        elif stop_bits in (1, 2):
            request = request + ",S=" + str(stop_bits)
        else:
            print("Wrong stop bits")
    if line_delay is not None:
        if is_int_between(line_delay, 0, 10000):
            request = request + ",L=" + str(line_delay)
        else:
            print("Wrong line delay")
    if param_lock is not None:
        if param_lock in ("0", "1"):
            request = request + ",H=" + param_lock
        elif param_lock in (0, 1):
            request = request + ",H=" + str(param_lock)
        else:
            print("Wrong parameter locking")

    if request == (str(address) + "XU"):
        return None
    else:
        return request


def software_reset(address):
    return str(address) + "XZ" + "\r\n"


def precipitation_counter_reset(address):
    return str(address) + "XZRU" + "\r\n"


def precipitation_intensity_reset(address):
    return str(address) + "XZRI" + "\r\n"


def ongoing_measurements_stop(address):
    return str(address) + "XZM" + "\r\n"


def query_addresses():
    return "?" + "\r\n"


def check_respond(address):
    return str(address) + "\r\n"


def request_wind_data(address):
    return str(address) + "R1" + "\r\n"


def request_pres_temp_hum_data(address):
    return str(address) + "R2" + "\r\n"


def request_precipitation_data(address):
    return str(address) + "R3" + "\r\n"


def request_supervisor_data(address):
    return str(address) + "R5" + "\r\n"


def request_all_data(address):
    return str(address) + "R" + "\r\n"


def request_composite_data(address):
    return str(address) + "R0" + "\r\n"


def request_wind_settings(address):
    return str(address) + "WU" + "\r\n"


def request_pres_temp_hum_settings(address):
    return str(address) + "TU" + "\r\n"


def request_precipitation_settings(address):
    return str(address) + "RU" + "\r\n"


def request_supervisor_settings(address):
    return str(address) + "SU" + "\r\n"


def change_wind_settings(address,
                         parameter_selection=None,
                         update_interval=None,
                         averaging_time=None,
                         suprema_mode=None,
                         speed_unit=None,
                         direction_offset=None,
                         sampling_rate=None
                         ):
    # pylint: disable=R0913,R0912,R0915
    request = str(address) + "WU"
    if parameter_selection is not None:
        if isinstance(parameter_selection, str):
            request = request + ",R=" + parameter_selection
        else:
            print("Wrong parameter selection")
    if update_interval is not None:
        if is_int_between(update_interval, 1, 3600):
            request = request + ",I=" + str(update_interval)
        else:
            print("Wrong repeat interval")
    if averaging_time is not None:
        if is_int_between(averaging_time, 1, 3600):
            request = request + ",A=" + str(averaging_time)
        else:
            print("Wrong averaging time")
    if suprema_mode is not None:
        if suprema_mode in ("1", "3"):
            request = request + ",G=" + suprema_mode
        elif suprema_mode in (1, 3):
            request = request + ",G=" + str(suprema_mode)
        else:
            print("Wrong min/max calculation mode")
    if speed_unit is not None:
        if speed_unit in ("M", "K", "S", "N"):
            request = request + ",U=" + speed_unit
        else:
            print("Wrong speed unit")
    if direction_offset is not None:
        if is_int_between(direction_offset, -180, 180):
            request = request + ",D=" + str(direction_offset)
        else:
            print("Wrong averaging time")
    if sampling_rate is not None:
        if sampling_rate in ("1", "2", "4"):
            request = request + ",F=" + sampling_rate
        elif sampling_rate in (1, 2, 4):
            request = request + ",F=" + str(sampling_rate)
        else:
            print("Wrong sampling rate")

    if request == (str(address) + "WU"):
        return None
    else:
        return request


def change_pres_temp_hum_settings(address,
                                  parameter_selection=None,
                                  update_interval=None,
                                  pressure_unit=None,
                                  temperature_unit=None
                                  ):
    # pylint: disable=R0913,R0912,R0915
    request = str(address) + "TU"
    if parameter_selection is not None:
        if isinstance(parameter_selection, str):
            request = request + ",R=" + parameter_selection
        else:
            print("Wrong parameter selection")
    if update_interval is not None:
        if is_int_between(update_interval, 1, 3600):
            request = request + ",I=" + str(update_interval)
        else:
            print("Wrong repeat interval")
    if pressure_unit is not None:
        if pressure_unit in ("H", "P", "B", "M", "I"):
            request = request + ",P=" + pressure_unit
        else:
            print("Wrong pressure unit")
    if temperature_unit is not None:
        if temperature_unit in ("C", "F"):
            request = request + ",T=" + temperature_unit
        else:
            print("Wrong temperature unit")

    if request == (str(address) + "TU"):
        return None
    else:
        return request


def change_precipitation_settings(address,
                                  parameter_selection=None,
                                  update_interval=None,
                                  precipitation_unit=None,
                                  hail_unit=None,
                                  autosend_mode=None,
                                  reset_mode=None,
                                  rain_limit=None,
                                  hail_limit=None
                                  ):
    # pylint: disable=R0913,R0912,R0915
    request = str(address) + "RU"
    if parameter_selection is not None:
        if isinstance(parameter_selection, str):
            request = request + ",R=" + parameter_selection
        else:
            print("Wrong parameter selection")
    if update_interval is not None:
        if is_int_between(update_interval, 1, 3600):
            request = request + ",I=" + str(update_interval)
        else:
            print("Wrong repeat interval")
    if precipitation_unit is not None:
        if precipitation_unit in ("M", "I"):
            request = request + ",U=" + precipitation_unit
        else:
            print("Wrong precipitation unit")
    if hail_unit is not None:
        if hail_unit in ("M", "I"):
            request = request + ",S=" + hail_unit
        else:
            print("Wrong hail unit")
    if autosend_mode is not None:
        if autosend_mode in ("R", "C", "T"):
            request = request + ",M=" + autosend_mode
        else:
            print("Wrong auto send mode")
    if reset_mode is not None:
        if reset_mode in ("M", "A", "L", "Y"):
            request = request + ",Z=" + reset_mode
        else:
            print("Wrong counter reset mode")
    if rain_limit is not None:
        if is_int_between(rain_limit, 100, 65535):
            request = request + ",X=" + str(rain_limit)
        else:
            print("Wrong rain accumulation limit")
    if hail_limit is not None:
        if isinstance(hail_limit, 100, 65535):
            request = request + ",Y=" + str(hail_limit)
        else:
            print("Wrong hail accumulation limit")

    if request == (str(address) + "RU"):
        return None
    else:
        return request


def change_supervisor_settings(address,
                               parameter_selection=None,
                               update_interval=None,
                               error_messaging=None,
                               heating_control=None
                               ):
    # pylint: disable=R0913,R0912,R0915
    request = str(address) + "SU"
    if parameter_selection is not None:
        if isinstance(parameter_selection, str):
            request = request + ",R=" + parameter_selection
        else:
            print("Wrong parameter selection")
    if update_interval is not None:
        if  is_int_between(update_interval, 1, 3600):
            request = request + ",I=" + str(update_interval)
        else:
            print("Wrong repeat interval")
    if error_messaging is not None:
        if error_messaging in ("Y", "N"):
            request = request + ",S=" + error_messaging
        else:
            print("Wrong pressure unit")
    if heating_control is not None:
        if heating_control in ("Y", "N"):
            request = request + ",H=" + heating_control
        else:
            print("Wrong temperature unit")

    if request == (str(address) + "SU"):
        return None
    else:
        return request


def parse_response(response):
    parsed = {
        "Sn": None,
        "Sm": None,
        "Sx": None,
        "Dn": None,
        "Dm": None,
        "Dx": None,
        "Pa": None,
        "Ta": None,
        "Tp": None,
        "Ua": None,
        "Rc": None,
        "Rd": None,
        "Ri": None,
        "Rp": None,
        "Hc": None,
        "Hd": None,
        "Hi": None,
        "Hp": None,
        "Th": None,
        "Vh": None,
        "Vs": None,
        "Vr": None,
        "Id": None
    }
    response = response.replace("\r\n", "")
    response = response.replace(" ", "")
    for info in response.split(","):
        if "=" in info:
            identifier = info.split("=")[0]
            if identifier == "Id":
                data = info.split("=")[1]
                unit = None
            else:
                data = info.split("=")[1][:-1]
                unit = info.split("=")[1][-1]
            parsed[identifier] = (data, unit)
    return parsed

def is_int_between(value, low_limit, high_limit):
    if isinstance(value, int):
        if value >= low_limit:
            if value <= high_limit:
                return True
    return False
