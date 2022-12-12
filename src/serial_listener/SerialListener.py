import serial
from src.logger.Logger import MyLogger
from src.config.settings import conf
from src.utils.utils import get_serial_port


class SerialListener:
    def __init__(self):
        self._logger = MyLogger()
        self._ser = serial.Serial()
        self._ser.baudrate = conf['boudrate']
        self._logger.info('Init SerialListener\n')

    def open(self):
        """Open serial listener"""
        self._logger.info('Try open serial listener\n\n')
        self._ser.port = get_serial_port()
        self._ser.open()
        self._logger.info('Serial listener opened successfully!\n\n')

    def receive(self):
        """Returns gps events"""
        self._logger.info('Read line from receiver...\n\n')
        # data = self._ser.readline().decode('ascii')
        data = '004 alert'
        self._logger.info('##################################################')
        self._logger.info(f'Received data: {data}')
        self._logger.info('##################################################\n\n')
        return data
