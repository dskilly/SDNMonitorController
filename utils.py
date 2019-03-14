from pox.core import core

from os import path
from datetime import datetime

import sqlite3 as sql

db = path.expanduser('SDNMonitor_db.sqlite')
conn = sql.connect(db)
c = conn.cursor()

class db_handle:
	def __init__(self, interval):
		self.received = 0
		self.transmitted = 0
		self.interval = interval

	def requestStats(self):
		for con in core.openflow.connections:
			con.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))

	def handleStats(self):
		rx = self.received * 8 / self.interval
		tx = self.transmitted * 8 / self.interval
		c.execute("INSERT INTO total_traffic (total_rx_bytes, total_tx_bytes) VALUES (?, ?)", (rx, tx))
		conn.commit()

def logger(logmsg):
	log = core.getLogger()
	log.info(logmsg)
	c.execute("INSERT INTO Log_Message (device_id, date_time_col, Syslog) VALUEs (?, ?, ?)", ("", datetime.now(), logmsg))