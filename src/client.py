#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

URL = 'rabbit://guest:guest@localhost:5672/'

class TestClient(object):
  def __init__(self, transport):
    target = oslo_messaging.Target(topic='test01')
    self.client = oslo_messaging.RPCClient(transport, target)

  def hoge(self, ctxt, arg):
    cctxt= self.client.prepare(namespace='foo', version='1.1')
    return cctxt.call(ctxt, 'hoge', arg = arg)

transport = oslo_messaging.get_transport(cfg.CONF, url = URL)
client = TestClient(transport)

print(client.hoge({}, 10))
