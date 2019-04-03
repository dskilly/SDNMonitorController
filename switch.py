from pox.core import core
import pox.openflow.libopenflow_01 as of

import psycopg2 as sql
from datetime import datetime

from .utils import logger
from .settings import *

class SwitchWrap:
	def __init__(self, passInTopo):
		self.topo = passInTopo
		
	class SwitchHandler():
		def __init__(self):
			self.macs = {}
			core.openflow.addListeners(self)
			self.received = 0
			self.transmitted = 0
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
			for f in event.stats:
				self.received = self.received - f.rx_bytes
				self.transmitted = self.transmitted - f.tx_bytes
			logger("Switch {} has received {} bytes and transmitted {} bytes.".format(event.dpid, self.received, self.transmitted))

		def _handle_FlowStatsReceived(self, event):
			for f in event.stats:
				pass

		def _handle_TableStatsReceived(self, event):
			sw = 's%s'%event.dpid
			self.max_entries[sw] = event.stats[0].max_entries
			self.tableActiveCount[sw] = event.stats[0].active_count
			print "TableStatsReceived"
			print self.tableActiveCount

			self.matched_count
			logger("Switch {} has received {} bytes and transmitted {} bytes.".format(event.dpid, self.max_entries, self.active_count, self.matched_count))

		def _handle_QueueStatsReceived(self, event):
			for f in event.stats:
				self.transmitted = f.tx_bytes
				self.packets = f.tx_packets
				self.errors = f.tx_errors
			logger("Switch {} has received {} bytes and transmitted {} bytes.".format(event.dpid, self.transmitted, self.packets, self.errors))
