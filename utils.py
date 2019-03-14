from pox.core import core

from os import path
from datetime import datetime

import sqlite3 as sql

class db_handle:
	def __init__(self, interval, connection):
		self.received = 0
		self.transmitted = 0
		self.interval = interval
		self.conn = connection
		self.c = conn.cursor()

	def requestStats(self):
		for con in core.openflow.connections:
			con.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))

	def handleStats(self):
		rx = self.received * 8 / self.interval
		tx = self.transmitted * 8 / self.interval
		self.c.execute("INSERT INTO total_traffic (total_rx_bytes, total_tx_bytes) VALUES (?, ?)", (rx, tx))
		self.conn.commit()

def logger(logmsg):
	log = core.getLogger()
	log.info(logmsg)
	self.c.execute("INSERT INTO Log_Message (device_id, date_time_col, Syslog) VALUEs (?, ?, ?)", ("", datetime.now(), logmsg))