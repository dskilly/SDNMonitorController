from .utils import logger

class SwitchHandler():
	def __init__(self):
		self.macs = {}
		core.openflow.addListeners(self)

	def _handle_ConnectionUp(self, event):
		logger("Switch {} has connected".format(event.dpid))

	def _handle_PacketIn(self, event):
		msg = of.ofp_packet_out()
		msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
		msg.buffer_id = event.ofp.buffer_id
		msg.in_port = event.port
		event.connection.send(msg)

	def _handle_PortStatsReceived(self, event):
		global received, transmitted
		for f in event.stats:
			received = received - f.rx_bytes
			transmitted = transmitted - f.tx_bytes
		logger("Switch {} has received {} bytes and transmitted {} bytes.".format(event.dpid, received, transmitted))