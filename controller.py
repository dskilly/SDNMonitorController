from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from os import path
import psycopg2 as sql
from datetime import datetime

from .utils import db_handle
from .switch import SwitchHandler
from .discovery import topology_discovery
from .settings import *

def launch(interval=5):
	dh = db_handle(interval)
	conn = sql.connect(db)
	c = conn.cursor()
	'''netjsongraph_topo_table = 'django_netjsongraph_topology'
	c.execute("SELECT 1 FROM {} WHERE id = ?".format(netjsongraph_topo_table), (topo_name,))
	if c.fetchone() is None:
		c.execute("INSERT INTO {} (id, label, created, modified, url, protocol, version, revision, metric, published, strategy, expiration_time, key, parser) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(netjsongraph_topo_table), (topo_name, topo_name, datetime.now(), datetime.now(), "", "", "", "", "", True, "Manual", -1, "", "NetJSON NetworkGraph"))
		conn.commit()'''
	core.registerNew(SwitchHandler)
	if 'openflow_discovery' not in core.components:
		core.registerNew(Discovery)
	core.registerNew(topology_discovery)
	#Timer(interval, dh.requestStats, recurring=True)
	#Timer(interval, dh.handleStats, recurring=True)