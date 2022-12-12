import serial
import requests
from time import sleep
from src.logger.Logger import MyLogger
from src.utils.utils import handle_received_data, get_cow_id_from_alert
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
        # self._ser_listener.open()

    def run(self):
        is_failed = True
        while True:
            try:
                # TODO Implement more elegant way
                if is_failed:  # If failed open a new instance
                    self.init_serial_listener()
                    is_failed = False

                data = self._ser_listener.receive()

                if 'alert' in data:
                    cow_id = get_cow_id_from_alert(data)
                    self._events_sender.send_alert(cow_id)
                    sleep(30)
                    continue

                if 'ID' not in data:  # If it is not gps event
                    self._logger.warn('The received data is not a GPS message!\n\n')
                    continue

                parsed_data = handle_received_data(data)

                self._events_sender.send_event(parsed_data)

            except serial.serialutil.SerialException as e:
                self._logger.error(f'{str(e)} \n\n')
                is_failed = True
                sleep(30)


