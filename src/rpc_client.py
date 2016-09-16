#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

DEFAULT_TOPIC = 'oslo-test1'
DEFAULT_SERVER = 'localhost'

class TestClient(object):
  def __init__(self, transport, tgt_topic, tgt_server):
    target = oslo_messaging.Target(topic=tgt_topic, server=tgt_server)
    self.client = oslo_messaging.RPCClient(transport, target)

  def hoge(self, ctxt, arg):
    cctxt= self.client.prepare(namespace='foo', version='1.1')
    return cctxt.call(ctxt, 'hoge', arg = arg)

def send_request(ctx, arg, topic=DEFAULT_TOPIC, server=DEFAULT_SERVER):
  # parse CLI parameter and load configuration file
  cfg.CONF()

  transport = oslo_messaging.get_transport(cfg.CONF)
  client = TestClient(transport, topic, server)

  return client.hoge(ctx, arg)

if __name__ == '__main__':
  print(send_request({}, 10))
