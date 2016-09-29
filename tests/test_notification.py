import os
import sys
import threading
import timeout_decorator
import unittest
sys.path.append(os.path.dirname(__file__) + "/../src")

import notifier_client as client
import notifier_server as server

g_check = False

class EndpointForTest(object):
    def info(self, _ctxt, _pid, _etype, _payload, _metadata):
        global g_check
        g_check = True


class TestNotifier(unittest.TestCase):
    TOPIC = 'oslo-example-test-for-notifier'

    def start_server(self):
        server.start_server([EndpointForTest()], self.TOPIC)

    def setUp(self):
        self.thread = threading.Thread(target = self.start_server)
        self.thread.start()

    def tearDown(self):
        if sys.version_info > (3,0):
            self.thread._stop()
        else:
            self.thread._Thread__stop()
        self.thread.join()

    @timeout_decorator.timeout(2)
    def test_send_notification(self):
        global g_check

        obj = client.NotifyClient(self.TOPIC)
        obj.info({}, 'hoge', {})

        while not g_check:
            pass

        self.assertTrue(g_check)
