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
                self.max_entries = {}
                self.tableActiveCount = {}
		self.interval = 0.5
		self.mac = {}
		self.connection = None

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
		self.connection = event.connection

	def _handle_PacketIn(self, event):
		packet = event.parse()
		src = packet.src.toStr()
		dst = packet.dst.toStr()
		if dst in self.mac:
			self.forward(event, self.mac[dst])
		else:
			self.flood(event)
		if src not in self.mac:
			self.mac[src] = event.port

	def flood(self, pie):
		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
		msg.buffer_id = pie.ofp.buffer_id
		msg.in_port = pie.port
		self.connection.send(msg)

	def forward(self, pie, to_port):
		packet = pie.parse()
		msg = of.ofp_flow_mod()
		msg.match = of.ofp_match.from_packet(packet)
		msg.actions.append(of.ofp_action_output(port = to_port))
		msg.buffer_id = pie.ofp.buffer_id
		self.connection.send(msg)

	def _handle_PortStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		for f in event.stats:
			src = 'Switch{}'.format(event.dpid)
			port = f.port_no
                        sw = 's{}:{}'.format(event.dpid, port)
			self.received[sw] = f.rx_bytes - self.received[sw] if sw in self.received else f.rx_bytes
			self.transmitted[sw] = f.tx_bytes - self.transmitted[sw] if sw in self.transmitted else f.tx_bytes
			c.execute('INSERT INTO "{}" (device_id, port_id, rx_packets, tx_packets, rx_dropped, tx_dropped, rx_errors, tx_errors) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (port_id) DO UPDATE SET rx_packets = %s, tx_packets = %s, rx_dropped = %s, tx_dropped = %s, rx_errors = %s, tx_errors = %s'.format(tables.ports), (src, sw, f.rx_packets, f.tx_packets, f.rx_dropped, f.tx_dropped, f.rx_errors, f.tx_errors, f.rx_packets, f.tx_packets, f.rx_dropped, f.tx_dropped, f.rx_errors, f.tx_errors))
			logger("Switch {} on port {} has received {} bytes and transmitted {} bytes.".format(sw, port, self.received[sw], self.transmitted[sw]))
			
			status = 'up'
			if self.transmitted[sw] > 2000:
				status = 'congested'
			c.execute('SELECT source_id, target_id FROM "{}" WHERE (source_id = %s AND source_port = %s) OR (target_id = %s AND target_port = %s)'.format(tables.links_table), (src, port, src, port))
			res = c.fetchone()
			if res is not None:
				sw1 = res[0]
				sw2 = res[1]
				c.execute('SELECT id FROM "{}" WHERE label = %s'.format(tables.netgraph_nodes), (sw1,))
				x = c.fetchone()
				if x is None:
					break
				id1 = x[0]
				c.execute('SELECT id FROM "{}" WHERE label = %s'.format(tables.netgraph_nodes), (sw2,))
				x = c.fetchone()
				if x is None:
					break
				id2 = x[0]
				c.execute('UPDATE "{}" SET status = %s, status_changed = %s WHERE (source_id = %s AND target_id = %s) OR (source_id = %s AND target_id = %s)'.format(tables.netgraph_links), (status, datetime.now(), id1, id2, id2, id1))
		conn.commit()

	def _handle_FlowStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		for f in event.stats:
			c.execute('INSERT INTO "{}" (table_id, duration_sec, priority, idle_timeout, hard_timeout, packet_count) VALUES (%s, %s, %s, %s, %s, %s)'.format(tables.flows), (f.table_id, f.duration_sec, f.priority, f.idle_timeout, f.hard_timeout, f.packet_count))
			#logger("Switch {} flow stats received.")
		conn.commit()

	def _handle_TableStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		sw = 's%s'%event.dpid
		for f in event.stats:
			self.max_entries[sw] = f.max_entries
			self.tableActiveCount[sw] = f.active_count
			logger("TableStatsReceived %s"%self.tableActiveCount)
			c.execute('INSERT INTO "{}" (table_id, name, wildcards, max_entries, active_count, lookup_count, matched_count) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (table_id) DO UPDATE SET active_count = %s, lookup_count = %s, matched_count = %s'.format(tables.flowtables), (f.table_id, f.name, f.wildcards, f.max_entries, f.active_count, f.lookup_count, f.matched_count, f.active_count, f.lookup_count, f.matched_count))
			#logger("Switch {} flow table {} with max entries {}, {} active flows and {} matched.".format(sw, f.table_id if not f.name else f.name, f.max_entries, f.active_count, f.matched_count))
		conn.commit()

	def _handle_QueueStatsReceived(self, event):
		conn = sql.connect(db)
		c = conn.cursor()
		sw = 's%s'%event.dpid
		for f in event.stats:
			self.transmitted = f.tx_bytes
			self.packets = f.tx_packets
			self.errors = f.tx_errors
			c.execute('INSERT INTO "{}" (port_no, queue_id, tx_bytes, tx_packets, tx_errors) VALUES (%s, %s, %s, %s, %s)'.format(tables.queues), (f.port_no, f.queue_id, f.tx_bytes, f.tx_packets, f.tx_errors))
			#logger("Switch {} queue stats {} bytes transmitted, {} packets transmitted and {} errors.".format(sw, self.transmitted, self.packets, self.errors))
		conn.commit()

	def handleStats(self):
		rx = self.received * 8 / self.interval
		tx = self.transmitted * 8 / self.interval
		conn = sql.connect(db)
		c = conn.cursor()
		c.execute("INSERT INTO \"{}\" (total_rx_bytes, total_tx_bytes, ts) VALUES (%s, %s, %s)".format(traffic), (rx, tx, datetime.now()))
		conn.commit()
