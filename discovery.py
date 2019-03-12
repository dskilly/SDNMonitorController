from pox.openflow.discovery import Discovery
from pox.lib.revent import EventMixin

from .utils import logger

class topology_discovery(EventMixin):
	def __init__(self):
		def startup():
			core.openflow.addListeners(self, priority = 0)
			core.openflow_dicovery.addListeners(self)
		core.call_when_ready(startup, ('openflow', 'openflow_discovery'))
		logger('Topology discovery init over')

	def _handle_LinkEvent(self, event):
		