#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 
import time

URL = 'rabbit://guest:guest@localhost:5672/'

class TestEndpoint(object):
  target = oslo_messaging.Target(namespace='foo', version='1.2')

  def hoge(self, ctx, arg):
    print("[TestEndpoint] hoge(%s, %d) is called" % (ctx, arg))
    return arg * 2

def start_server(driver_url, tgt_topic, tgt_server):
  transport = oslo_messaging.get_transport(cfg.CONF, url = driver_url)
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
    start_server(URL, 'oslo01', 'hoge')
