import requests
from src.logger.Logger import MyLogger
from src.config.settings import conf


def post_request(url: str, data: dict, logger: MyLogger):
    """Send post request"""

    try:
        logger.info(f'Send post to server...\n\n')
        x = requests.post(url,
                          json=data,
                          headers={
                              'Content-Type': 'application/json'
                          })
        logger.info(f'Server response: {x.text}\n\n')
    except (requests.exceptions.InvalidSchema, requests.exceptions.ConnectionError) as e:
        logger.error(f'During post request: {str(e)}\n\n')


class EventsSender:
    def __init__(self):
        self._logger = MyLogger()
        self._logger.info('Init Events Sender')

    def send_event(self, event: dict):
        """Sends post request to the server"""

        post_request(conf['server_url'], event, self._logger)

    def send_alert(self, cow_id: str):
        """Sends an alert to the server"""

        post_request(conf['server_url'] + "/theft-alert", {"cowId": cow_id}, self._logger)
