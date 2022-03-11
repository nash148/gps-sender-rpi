import serial
from time import time
import serial.tools.list_ports
from src.config.settings import conf


def current_milli_time():
    return round(time() * 1000)


def handle_received_data(data: str):
    """Handles the receive data from the receiver"""
    # TODO Implement this func in more elegant way

    parsed_dict = {
        "timestamp": current_milli_time()
    }

    separated_params = data.split(';')

    for param in separated_params:

        if ':' in param:
            separated_param = param.split(':')
        elif '=' in param:
            separated_param = param.split('=')
        else:
            continue

        if separated_param[0] == 'GPS':
            gps_value = separated_param[1].split()
            gps_value = [float(n) for n in gps_value]
            parsed_dict['latLong'] = gps_value
        elif separated_param[0] == 'ID':
            parsed_dict['cowId'] = separated_param[1]
        elif separated_param[0] == 'TW':
            parsed_dict['tw'] = separated_param[1]
        elif separated_param[0] == 'BAT':
            parsed_dict['battery'] = separated_param[1]
        elif separated_param[0] == 'C':
            parsed_dict['counter'] = int(separated_param[1][:-2])  # -2 to cut the \r\n in the end of the event

    return parsed_dict


def get_serial_port():
    """Returns the device path"""
    ports = serial.tools.list_ports.comports()

    for p in ports:
        if p.vid == conf['vendor_id']:
            return p.device
    raise serial.serialutil.SerialException('Cannot find device!!')


