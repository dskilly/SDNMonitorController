from pox.core import core
from pox.lib.recoco import Timer
from pox.openflow.discovery import Discovery

from os import path
import sqlite3 as sql
from datetime import datetime

from .utils import db_handle
from .switch import SwitchWrap
from .settings import *

def launch(interval=5):
	dh = db_handle(interval)
	conn = sql.connect(db)
	c = conn.cursor()
	topo = {}
	netjsongraph_topo_table = 'django_netjsongraph_topology'
	c.execute("INSERT INTO {0} (id, label, created, modified, url, protocol, version, revision, metric, published, strategy, expiration_time, key, parser) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) WHERE NOT EXISTS(SELECT 1 FROM {0} WHERE id = ?)".format(netjsongraph_topo_table), (topo_name, topo_name, datetime.now(), datetime.now(), "", "", "", "", "", True, "Manual", -1, "", "NetJSON NetworkGraph", topo_name))
	conn.commit()
	switch = SwitchWrap(topo)
	core.registerNew(SwitchWrap.SwitchHandler)
	#Timer(interval, dh.requestStats, recurring=True)
	#Timer(interval, dh.handleStats, recurring=True)