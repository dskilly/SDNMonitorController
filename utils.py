from pox.core import core
import pox.openflow.libopenflow_01 as of

from datetime import datetime
import psycopg2 as sql

from .settings import *

traffic = 'SDNMonitorApp_total_traffic'
logs = 'SDNMonitorApp_log_message'

class db_handle:
	def __init__(self, interval):
		self.received = 0
		self.transmitted = 0
		self.interval = interval

	def requestStats(self):
		for con in core.openflow.connections:
			con.send(of.ofp_stats_request(body=of.ofp_port_stats_request()))
			con.send(of.ofp_stats_request(body=of.ofp_flow_stats_request()))
			#con.send(of.ofp_stats_request(body=of.ofp_desc_stats_request()))
			#con.send(of.ofp_stats_request(body=of.ofp_table_stats_request()))
			#con.send(of.ofp_stats_request(body=of.ofp_queue_stats_request()))

def logger(logmsg):
	log = core.getLogger()
	log.info(logmsg)
	conn = sql.connect(db)
	c = conn.cursor()
	#c.execute("INSERT INTO {} (device_id, syslog, ts) VALUES (?, ?, ?)".format(logs), ("", logmsg, datetime.now()))
	#conn.commit()
