import os
import sys
import threading
import unittest
sys.path.append(os.path.dirname(__file__) + "/../src")

import rpc_client as client
import rpc_server as server

class TestRPC(unittest.TestCase):
    TOPIC = 'oslo-example-test-for-rpc'
    SERVER = 'test'
    REQUEST_VALUE = 20

    def start_server(self):
        server.start_server(self.TOPIC, self.SERVER)

    def setUp(self):
        self.thread = threading.Thread(target = self.start_server)
        self.thread.start()

    def tearDown(self):
        if sys.version_info > (3,0):
            self.thread._stop()
        else:
            self.thread._Thread__stop()
        self.thread.join()

    def test_send_request(self):
        result = client.send_request({}, self.REQUEST_VALUE, self.TOPIC, self.SERVER)
        self.assertEqual(result, self.REQUEST_VALUE * 2)
