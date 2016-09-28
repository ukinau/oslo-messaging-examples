#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

# This class is wrapper of Notifier class of oslo.messaging
class NotifyClient(object):
    def __init__(self, topic='test_topic', driver='messaging', pub_id='', url=''):
        transport =  oslo_messaging.get_notification_transport(cfg.CONF, url=url)
        self.notifier = oslo_messaging.Notifier(transport, driver=driver, publisher_id=pub_id, topic=topic)

    def functionClosure(self, name):
        def handlerFunction(*args, **kwargs):
            return getattr(self.notifier, name)(*args, **kwargs)

        return handlerFunction

    def __getattr__(self, name):
        return self.functionClosure(name)


if __name__ == '__main__':
    cfg.CONF()

    client = NotifyClient()
    client.info({'context': 'foo'}, 'event-hoge', {'hoge': 'abcd'})
    client.info({'context': 'bar'}, 'event-fuga', {'fuga': 'efgh'})
