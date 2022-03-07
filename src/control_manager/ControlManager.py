import serial
import requests
from time import sleep
from src.logger.Logger import MyLogger
from src.utils.utils import handle_received_data
from src.serial_listener.SerialListener import SerialListener
from src.http_sender.HttpSender import EventsSender


class ControlManager:
    """This class manages the program flow"""
    def __init__(self):
        self._logger = MyLogger()
        self._events_sender = EventsSender()
        self._ser_listener = None
        self._logger.info('Init ControlManager')

    def init_serial_listener(self):
        """Init the serial listener"""
        self._ser_listener = SerialListener()
        self._ser_listener.open()

    def run(self):
        is_failed = True
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

                parsed_data = handle_received_data(data)

                self._send_event_to_server(parsed_data)

            except serial.serialutil.SerialException as e:
                self._logger.error(str(e))
                is_failed = True
                sleep(0.5)

    def _send_event_to_server(self, event: dict):
        """Send the event to the server"""
        try:
            self._events_sender.send(event)
        except (requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError) as e:
            self._logger.error(f'During post request: {str(e)}')


