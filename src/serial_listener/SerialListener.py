import serial
from src.logger.Logger import MyLogger
from src.config.settings import conf


class SerialListener:
    def __init__(self):
        self._logger = MyLogger()
        self._ser = serial.Serial()
        self._ser.baudrate = conf['boudrate']
        self._ser.port = conf['serial_port']
        self._logger.info('Init SerialListener\n')

    def open(self):
        """Open serial listener"""
        self._logger.info('Try open serial listener\n\n')
        self._ser.open()
        self._logger.info('Serial listener opened successfully!\n\n')

    def receive(self):
        """Returns gps events"""
        self._logger.info('Read line from receiver...\n\n')
        data = self._ser.readline().decode('ascii')
        self._logger.info('##################################################')
        self._logger.info(f'Received data: {data}')
        self._logger.info('##################################################\n\n')
        return data
