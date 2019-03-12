from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from .utils import db_handle
from .switch import SwitchHandler

interval = 0.5

def launch(intervals=interval):
	global interval
	interval = intervals
	dh = newd db_handle()
	core.registerNew(SwitchHandler)
	Timer(interval, dh.requestStats, recurring=True)
	Timer(interval, dh.handleStats, recurring=True)