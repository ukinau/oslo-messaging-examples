#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 
import time

URL = 'rabbit://guest:guest@localhost:5672/'

class TestEndpoint1(object):
  def hoge(self, ctx, arg):
    return arg * 2

class TestEndpoint2(object):
  target = oslo_messaging.Target(namespace='foo', version='1.2')
      
  def fuga(self, ctx, arg):
    return arg *3 

transport = oslo_messaging.get_transport(cfg.CONF, url = URL)

# NOTE: The argument of 'server' is mandatory
target = oslo_messaging.Target(topic='test01', server='server1')
endpoints = [
  TestEndpoint1(),
  TestEndpoint2(),
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
