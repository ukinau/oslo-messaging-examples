#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

URL = 'rabbit://guest:guest@localhost:5672/'

class HogeEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(event_type='.*: hoge$')

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        print("[HogeEndpoint] ctxt: %s" % (ctxt))
        print("[HogeEndpoint] publisher_id: %s" % (publisher_id))
        print("[HogeEndpoint] event_type: %s" % (event_type))
        print("[HogeEndpoint] payload: %s" % (payload))
        print("[HogeEndpoint] metadata: %s" % (metadata))


class FugaEndpoint(object):

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        print("[FugaEndpoint] ctxt: %s" % (ctxt))
        print("[FugaEndpoint] publisher_id: %s" % (publisher_id))
        print("[FugaEndpoint] event_type: %s" % (event_type))
        print("[FugaEndpoint] payload: %s" % (payload))
        print("[FugaEndpoint] metadata: %s" % (metadata))


transport = oslo_messaging.get_notification_transport(cfg.CONF, url=URL)
targets   = [oslo_messaging.Target(topic='test_topic')]
endpoints = [
    HogeEndpoint(),
    FugaEndpoint(),
]

server = oslo_messaging.get_notification_listener(transport, targets, endpoints)

try:
    server.start()
    server.wait()
except KeyboardInterrupt:
    print("stop server")
    server.stop()
except Exception as e:
    print("[ERROR] faield to start server '%s'" % (e.message))
    server.stop()
