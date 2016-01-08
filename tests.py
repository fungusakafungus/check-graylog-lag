from unittest import TestCase
from dateutil.tz import tzlocal
import datetime
import bottle
import threading
import os
import socket

response = None
sleep_seconds = 0


@bottle.route('/search/universal/relative')
def get():
    import time
    time.sleep(sleep_seconds)
    return response


t = threading.Thread(
    target=bottle.run,
    kwargs={'host': socket.gethostname(), 'port': 12900},
)
t.setDaemon(True)
t.start()


class Test(TestCase):
    def test_OK(self):
        global response
        now = datetime.datetime.now(tzlocal()).strftime("%Y-%m-%dT%T.000%Z")
        response = '{"messages":[{"message": {"timestamp": "%s"}}]}' % now
        assert os.system('./check_graylog_lag') >> 8 == 0

    def test_WARNING(self):
        global response
        earlier = (
            datetime.datetime.now(tzlocal()) - datetime.timedelta(minutes=6)
        ).strftime("%Y-%m-%dT%T.000%Z")
        response = '{"messages":[{"message": {"timestamp": "%s"}}]}' % earlier
        assert os.system('./check_graylog_lag') >> 8 == 1

    def test_CRITICAL(self):
        global response
        earlier = (
            datetime.datetime.now(tzlocal()) - datetime.timedelta(minutes=20)
        ).strftime("%Y-%m-%dT%T.000%Z")
        response = '{"messages":[{"message": {"timestamp": "%s"}}]}' % earlier
        assert os.system('./check_graylog_lag') >> 8 == 2

    def test_no_data_CRITICAL(self):
        global response
        response = '{"messages":[]}'
        assert os.system('./check_graylog_lag') >> 8 == 2

    def test_invalid_json_UNKNOWN(self):
        global response
        response = '%&!'
        assert os.system('./check_graylog_lag') >> 8 == 3

    def test_connection_refused_CRITICAL(self):
        exit_code = os.system('./check_graylog_lag -g example.com -t 1 --connection-errors-are-critical') >> 8
        assert exit_code == 2

    def test_connection_refused_UNKNOWN(self):
        exit_code = os.system('./check_graylog_lag -g example.com -t 1') >> 8
        assert exit_code == 3

    def test_timeout_CRITICAL(self):
        global sleep_seconds
        sleep_seconds = 2
        assert os.system('./check_graylog_lag -t 1 --connection-errors-are-critical') >> 8 == 2

    def test_timeout_UNKNOWN(self):
        global sleep_seconds
        sleep_seconds = 2
        assert os.system('./check_graylog_lag -t 1') >> 8 == 3
