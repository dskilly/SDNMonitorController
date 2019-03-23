from pox.core import core
from pox.openflow.discovery import Discovery
from pox.lib.revent import EventMixin

import psycopg2 as sql
from datetime import datetime

from .utils import logger
from .settings import *

class topology_discovery(EventMixin):
	def __init__(self):
		self.listenTo(core.openflow, priority=0)
		self.listenTo(core.openflow_discovery)
		core.openflow.addListeners(self)
		logger('Topology discovery init over')

	def _handle_LinkEvent(self, event):
		links_table = 'SDNMonitorApp_links_table'
		l = event.link
		sw1 = 'Switch{}'.format(l.dpid1)
		sw2 = 'Switch{}'.format(l.dpid2)
		po1 = l.port1
		po2 = l.port2
		id = '{}:{} to {}:{}'.format(sw1, po1, sw2, po2)
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("SELECT 1 FROM {} WHERE id = %s".format(links_table), (id,))
		if c.fetchone() is None and event.added:
			c.execute("INSERT INTO {} (id, created, modified, cost, status, source_id, target_id, status_changed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(links_table), (id, datetime.now(), datetime.now(), 1, True, sw1, sw2, datetime.now()))
		elif event.added:
			c.execute("UPDATE {} SET status_changed = %s WHERE id = %s".format(links_table), (datetime.now(), id))
		elif event.removed:
			c.execute("UPDATE {} SET status_changed = %s, status = %s WHERE id = %s".format(links_table), (datetime.now(), False, id))
		conn.commit()