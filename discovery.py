from pox.core import core
from pox.openflow.discovery import Discovery
from pox.lib.revent import EventMixin

import sqlite3 as sql
from datetime import datetime

from .utils import logger
from .settings import *

class topology_discovery(EventMixin):
	def __init__(self):
		def startup():
			core.openflow.addListeners(self, priority = 0)
			core.openflow_dicovery.addListeners(self)
		core.call_when_ready(startup, ('openflow', 'openflow_discovery'))
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
		c.execute("SELECT 1 FROM {} WHERE id = ?".format(links_table), (id,))
		if c.fetchone is None and l.added:
			c.execute("INSERT INTO {} (id, created, modified, cost, status, source_id, target_id, status_changed) VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(links_table), (id, datetime.now(), datetime.now(), 1, True, sw1, sw2, datetime.now()))
		elif l.added:
			c.execute("UPDATE {} status_changed = ? WHERE id = ?".format(links_table), (datetime.now(), id))
		elif l.removed:
			c.execute("UPDATE {} status_changed = ?, status = ? WHERE id = ?".format(links_table), (datetime.now(), False, id))