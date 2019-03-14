from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from .utils import db_handle
from .switch import SwitchHandler

def launch(interval=0.5):
	dh = db_handle(interval)
	core.registerNew(SwitchHandler)
	Timer(interval, dh.requestStats, recurring=True)
	Timer(interval, dh.handleStats, recurring=True)