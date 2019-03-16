from pox.core import core
import pox.openflow.libopenflow_01 as of

from datetime import datetime

import sqlite3 as sql

traffic = 'SDNMonitorApp_total_traffic'
logs = 'SDNMonitorApp_log_message'

class db_handle:
	def __init__(self, interval, dbPath):
		self.received = 0
		self.transmitted = 0
		self.interval = interval
		self.db = dbPath

	def requestStats(self):
		for con in core.openflow.connections:
			con.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))

	def handleStats(self):
		rx = self.received * 8 / self.interval
		tx = self.transmitted * 8 / self.interval
		conn = sql.connect(self.db)
		c = conn.cursor()
		c.execute("INSERT INTO {} (total_rx_bytes, total_tx_bytes, ts) VALUES (?, ?, ?)".format(traffic), (rx, tx, datetime.now()))
		conn.commit()

def logger(logmsg):
	log = core.getLogger()
	log.info(logmsg)
	conn = sql.connect(self.db)
	c = conn.cursor()
	c.execute("INSERT INTO {} (device_id, syslog, ts) VALUES (?, ?, ?)".format(logs), ("", logmsg, datetime.now()))
	conn.commit()