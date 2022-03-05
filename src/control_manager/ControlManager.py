import serial
import requests
from time import sleep, time
from src.logger.Logger import MyLogger

def current_milli_time():
    return round(time() * 1000)


class SerialListener:
    def __init__(self):
        self._logger = MyLogger()
        self._ser = serial.Serial()
        self._ser.baudrate = 115200  # TODO constant
        self._ser.port = 'COM7'  # TODO Constant
        self._logger.info('Init SerialListener')

    def open(self):
        """Open serial listener"""
        self._logger.info('Try open serial listener')
        self._ser.open()
        self._logger.info('Serial listener opened successfully')

    def receive(self):
        """Returns gps events"""
        self._logger.info('Read line from receiver')
        data = self._ser.readline().decode('ascii')
        self._logger.info(f'Received data: {data}')
        return data


class EventsSender:
    def __init__(self):
        self._logger = MyLogger()
        self._logger.info('Init Events Sender')

    def send(self, event: dict):
        """Sends post request to the server"""

        self._logger.info(f'Send post request with body: {event}')
        x = requests.post('http://localhost:3344/api/gps-events',
                          json=event,
                          headers={
                              'Content-Type': 'application/json'
                          })
        self._logger.info(f'Http response msg: {x.text}')


class ControlManager:
    """This class manages the program flow"""
    def __init__(self):
        self._logger = MyLogger()
        self._events_sender = EventsSender()
        self._ser_listener = None
        self.init_serial_listener()
        self._logger.info('Init ControlManager')

    def init_serial_listener(self):
        """Init the serial listener"""
        self._ser_listener = SerialListener()
        self._ser_listener.open()

    def run(self):
        is_failed = False
        while True:
            try:
                # TODO Implement more elegant way
                if is_failed:  # If failed open a new instance
                    self.init_serial_listener()
                    is_failed = False

                data = self._ser_listener.receive()

                if 'ID' not in data:  # If it is not gps event
                    self._logger.warn('Something wrong with the received data')
                    continue

                parsed_data = self._handle_receive_data(data)

                self._send_event_to_server(parsed_data)

            except serial.serialutil.SerialException as e:
                self._logger.error(str(e))
                is_failed = True
                sleep(0.5)

    def _send_event_to_server(self, event: dict):
        """Send the event to the server"""
        try:
            self._events_sender.send(event)
        except requests.exceptions.InvalidSchema as e:
            self._logger.error(f'During post request: {str(e)}')

    def _handle_receive_data(self, data: str):
        """Handles the receive data from the receiver"""
        self._logger.info('Parse the received data')

        # TODO Implement this func in more elegant way

        parsed_dict = {
            "timestamp": current_milli_time()
        }

        separated_params = data.split(';')

        for param in separated_params:

            if ':' in param:
                param = param.split(':')
            elif '=' in param:
                param = param.split('=')

            if param[0] == 'GPS':
                gps_value = param[1].split()
                gps_value = [float(n) for n in gps_value]
                parsed_dict['latLong'] = gps_value
            elif param[0] == 'ID':
                parsed_dict['cowId'] = param[1]
            elif param[0] == 'TW':
                parsed_dict['tw'] = param[1]
            elif param[0] == 'BAT':
                parsed_dict['battery'] = param[1]
            elif param[0] == 'C':
                parsed_dict['counter'] = int(param[1][:-2])  # -2 to cut the \r\n in the end of the event

        return parsed_dict


