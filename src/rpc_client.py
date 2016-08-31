#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

URL = 'rabbit://guest:guest@localhost:5672/'

class TestClient(object):
  def __init__(self, transport, tgt_topic, tgt_server):
    target = oslo_messaging.Target(topic=tgt_topic, server=tgt_server)
    self.client = oslo_messaging.RPCClient(transport, target)

  def hoge(self, ctxt, arg):
    cctxt= self.client.prepare(namespace='foo', version='1.1')
    return cctxt.call(ctxt, 'hoge', arg = arg)

def send_request(ctx, arg, driver_url, topic, server=''):
    transport = oslo_messaging.get_transport(cfg.CONF, url = driver_url)
    client = TestClient(transport, topic, server)

    return client.hoge(ctx, arg)

if __name__ == '__main__':
    print(send_request({}, 10, URL, 'oslo01'))
