#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

import time

DEFAULT_TOPIC = 'oslo-test1'
DEFAULT_SERVER = 'localhost'

class TestEndpoint(object):
    target = oslo_messaging.Target(namespace='foo', version='1.2')

    def hoge(self, ctxt, arg):
        print("[TestEndpoint] hoge(%s, %d) is called" % (ctxt, arg))
        return arg * 2

def start_server(tgt_topic = DEFAULT_TOPIC, tgt_server = DEFAULT_SERVER, url=''):
    transport = oslo_messaging.get_transport(cfg.CONF, url=url)
    target = oslo_messaging.Target(topic=tgt_topic, server=tgt_server)
    endpoints = [
        TestEndpoint(),
    ]

    server = oslo_messaging.get_rpc_server(transport, target, endpoints)
    try:
        server.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("will stop server")
        server.stop()
    except Exception as e:
        print("[ERROR] faield to start server '%s'" % (e.message))

if __name__ == '__main__':
    # parse CLI parameter and load configuration file
    cfg.CONF()

    start_server()
