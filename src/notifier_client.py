#!/usr/bin/env python

from oslo_config import cfg
import oslo_messaging 

URL = 'rabbit://guest:guest@localhost:5672/'

transport =  oslo_messaging.get_notification_transport(cfg.CONF, url=URL)
notifier = oslo_messaging.Notifier(transport, driver='messaging', publisher_id='hoge', topic='test_topic')

notifier.info({'context': 'foo'}, 'event-type: hoge', {'payload': 'abcd'})
notifier.info({'context': 'bar'}, 'event-type: fuga', {'payload': 'efgh'})
