from os import path

db = 'dbname=sdnmonitorapp user=sdnmonitor host=localhost password=memeteam'

topo_name = 'SDNMonitorTopoTest'

class tables:
	ports = 'Appmonitor_port_stats'
	flows = 'Appmonitor_flow_stats'
	descs = 'Appmonitor_desc_stats'
	flowtables = 'Appmonitor_table_stats'
	queues = 'Appmonitor_queue_stats'
	netgraph_nodes = 'django_netjsongraph_node'
	netgraph_links = 'django_netjsongraph_link'
	links_table = 'SDNMonitorApp_links_table'
	nodes_table = 'SDNMonitorApp_nodes_table'