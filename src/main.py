from src.control_manager.ControlManager import ControlManager
from src.logger.Logger import MyLogger

logger = MyLogger()


def main():
    logger.info('#################################')
    logger.info('##   GPS Sender Starting...    ##')
    logger.info('#################################')

    manager = ControlManager()

    manager.run()


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        logger.error(str(e))
        raise e
