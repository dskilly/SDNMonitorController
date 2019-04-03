from os import path

db = 'dbname=sdnmonitorapp user=sdnmonitor host=localhost password=memeteam'

topo_name = 'SDNMonitorTopoTest'

class tables:
	ports = 'Appmonitor_port_stats'
	flows = 'Appmonitor_flow_stats'
	descs = 'Appmonitor_desc_stats'
	flowtables = 'Appmonitor_table_stats'
	queues = 'Appmonitor_queue_stats'