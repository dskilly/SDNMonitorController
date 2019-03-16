from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from os import path
import sqlite3 as sql
from datetime import datetime

from .utils import db_handle
from .switch import SwitchWrap

def launch(interval=5):
	dbPath = path.expanduser('~/db.sqlite3')
	dh = db_handle(interval, dbPath)
	conn = sql.connect(dbPath)
	c = conn.cursor()
	topo = {}
	topo_name = 'SDNMonitorTopoTest'
	netjsongraph_topo_table = 'django_netjsongraph_topology'
	c.execute("SELECT 1 FROM {} WHERE label = ?".format(netjsongraph_topo_table), (topo_name,))
	if c.fetchone() is None:
		c.execute("INSERT INTO {} (id, label, created, modified, url, protocol, version, revision, metric, published, strategy, expiration_time, key, parser) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(netjsongraph_topo_table), (topo_name, topo_name, datetime.now(), datetime.now(), "", "", "", "", "", True, "Manual", -1, "", "NetJSON NetworkGraph"))
		conn.commit()
	switch = SwitchWrap(topo, dbPath)
	core.registerNew(SwitchWrap.SwitchHandler)
	Timer(interval, dh.requestStats, recurring=True)
	Timer(interval, dh.handleStats, recurring=True)