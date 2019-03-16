from pox.core import core
import pox.openflow.libopenflow_01 as of

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