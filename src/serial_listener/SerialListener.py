
class SerialListener:
    def __init__(self):
        print(34)


# import serial
# from src.logger.Logger import MyLogger
#
#
# class SerialListener:
#     """This class handles serial gps receiver"""
#     def __init__(self):
#         self._logger = MyLogger()
#         self._ser = serial.Serial()
#         self._ser.baudrate = 115200
#         self._ser.port = 'COM7'
#         self._ser.open()
#         self._logger.info(f'Open serial port - {self._ser.name}')
#
#     def receive(self):
#         """Return gps event from device"""
#         data = self._ser.readline()
#         self._logger(data)
