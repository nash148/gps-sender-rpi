import requests
from src.logger.Logger import MyLogger
from src.config.settings import conf


class EventsSender:
    def __init__(self):
        self._logger = MyLogger()
        self._logger.info('Init Events Sender')

    def send(self, event: dict):
        """Sends post request to the server"""

        self._logger.info(f'Send post event to server...\n\n')
        x = requests.post(conf['server_url'],
                          json=event,
                          headers={
                              'Content-Type': 'application/json'
                          })
        self._logger.info(f'Server response: {x.text}\n\n')
