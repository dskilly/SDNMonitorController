from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from os import path
import sqlite3 as sql

from .utils import db_handle
from .switch import SwitchHandler

def launch(interval=0.5):
	db = path.expanduser('db.sqlite3')
	conn = sql.connect(db)
	dh = db_handle(interval, conn)
	core.registerNew(SwitchHandler)
	Timer(interval, dh.requestStats, recurring=True)
	Timer(interval, dh.handleStats, recurring=True)