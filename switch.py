from pox.core import core
from pox.lib.recoco import Timer
import pox.openflow.libopenflow_01 as of

import psycopg2 as sql
from datetime import datetime

from .utils import logger
from .settings import *

class SwitchHandler():
	def __init__(self):
		self.macs = {}
		core.openflow.addListeners(self)
		self.received = {}
		self.transmitted = {}
		self.interval = 0.5

	def _handle_ConnectionUp(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		nodes_table = 'SDNMonitorApp_nodes_table'
		switch = 'Switch{}'.format(event.dpid)
		c.execute("SELECT 1 FROM \"{}\" WHERE id = %s".format(nodes_table), (switch,))
		if c.fetchone() is None:
			c.execute("INSERT INTO \"{}\" (id, created, modified, label) VALUES (%s, %s, %s, %s)".format(nodes_table), (switch, datetime.now(), datetime.now(), switch,))
			conn.commit()
		logger("Switch {} has connected".format(event.dpid))

	def _handle_PacketIn(self, event):
		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
		msg.buffer_id = event.ofp.buffer_id
		msg.in_port = event.port
		event.connection.send(msg)

	def _handle_PortStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		sw = event.dpid
		for f in event.stats:
			self.received[sw] = self.receive[sw] - f.rx_bytes
			self.transmitted[sw] = self.transmitted[sw] - f.tx_bytes
			c.execute('INSERT INTO "{}" (device_id, port_id, rx_packets, tx_packets, rx_dropped, tx_dropped, rx_errors, tx_errors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'.format(tables.ports), (f.device_id, f.port_id, f.rx_packets, f.tx_packets, f.rx_dropped, f.tx_dropped, f.rx_errors, f.tx_errors))
			logger("Switch {} on port {} has received {} bytes and transmitted {} bytes.".format(sw, f.port_no, self.received, self.transmitted))
		conn.commit()

	def _handle_FlowStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		for f in event.stats:
			c.execute('INSERT INTO "{}" (length, table_id, duration_sec, priority, idle_timeout, hard_timeout, packet_count) VALUES (%s, %s, %s, %s, %s, %s, %s)'.format(tables.flows), (f.length, f.table_id, f.duration_sec, f.priority, f.idle_timeout, f.hard_timeout, f.packet_count))
			logger("Switch {} flow stats received.")
		conn.commit()

	def _handle_TableStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		sw = 's%s'%event.dpid
		for f in event.stats:
			self.max_entries[sw] = f.max_entries
			self.tableActiveCount[sw] = f.active_count
			logger("TableStatsReceived %s"%self.tableActiveCount)
			c.execute('INSERT INTO "{}" (table_id, name, wildcards, max_entries, active_count, lookup_count, matched_count) VALUEs (%s, %s, %s, %s, %s, %s, %s)'.format(tables.flowtables), (f.table_id, f.name, f.wildcards, f.max_entries, f.active_count, f.lookup_count, f.matched_count))
			logger("Switch {} flow table {} with max entries {}, {} active flows and {} matched.".format(sw, f.table_id if not f.name else f.name, f.max_entries, f.active_count, f.matched_count))
		conn.commit()

	def _handle_QueueStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		sw = 's%s'%event.dpid
		for f in event.stats:
			self.transmitted = f.tx_bytes
			self.packets = f.tx_packets
			self.errors = f.tx_errors
			c.execute('INSERT INTO "{}" (port_no, queue_id, tx_bytes, tx_packets, tx_errors) VALUES (%s, %s, %s, %s, %s)'format(tables.queues), (f.port_no, f.queue_id, f.tx_bytes, f.tx_packets, f.tx_errors))
			logger("Switch {} queue stats {} bytes transmitted, {} packets transmitted and {} errors.".format(sw, self.transmitted, self.packets, self.errors))
		conn.commit()

	def handleStats(self):
		rx = self.received * 8 / self.interval
		tx = self.transmitted * 8 / self.interval
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("INSERT INTO \"{}\" (total_rx_bytes, total_tx_bytes, ts) VALUES (%s, %s, %s)".format(traffic), (rx, tx, datetime.now()))
		conn.commit()
