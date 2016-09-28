#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

class HogeEndpoint(object):
    filter_rule = oslo_messaging.NotificationFilter(event_type='event-hoge')

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


def start_server(endpoints=[], topic='test_topic', url=''):
    transport = oslo_messaging.get_notification_transport(cfg.CONF, url=url)
    targets   = [oslo_messaging.Target(topic=topic)]
    server    = oslo_messaging.get_notification_listener(transport, targets, endpoints)

    try:
        server.start()
        server.wait()
    except KeyboardInterrupt:
        print("stop server")
        server.stop()
    except Exception as e:
        print("[ERROR] faield to start server '%s'" % (e.message))
        server.stop()

if __name__ == '__main__':
    # parse CLI parameter and load configuration file
    cfg.CONF()

    start_server([HogeEndpoint(), FugaEndpoint()])
