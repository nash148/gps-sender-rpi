import logging
import os
import sys
import datetime


class MyLogger:
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:
            cls._logger = super().__new__(cls, *args, **kwargs)
            cls._logger = logging.getLogger("crumbs")
            cls._logger.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                '%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

            now = datetime.datetime.now()
            dirname = "./logs"

            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fileHandler = logging.FileHandler(
                dirname + "/log_" + now.strftime("%d-%m-%Y_%H-%M-%S")+".log")

            streamHandler = logging.StreamHandler(sys.stdout)

            fileHandler.setFormatter(formatter)
            streamHandler.setFormatter(formatter)

            cls._logger.addHandler(fileHandler)
            cls._logger.addHandler(streamHandler)

        return cls._logger
