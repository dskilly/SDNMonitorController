#1. To run <mininet@mininet-vm:~$ sudo python net4901_topology.py>
#2. There are loops in the network therefore pings may fail until spanning tree is implemented
#3a. use net4901_topology_loopfree.py to use the same topology without loop causing links.
#3b. mininet> pingall    all pings should work h1,h2,h3,h4

#/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def FinalProject():

 net = Mininet( topo=None,
 build=False,
 ipBase='10.0.0.0/8')

 info( '*** Adding Controller\n' )
 c0=net.addController(name='c0',
 controller=RemoteController,
 ip='127.0.0.1',
 protocol='tcp',
 port=6633)

 info( '*** Adding Switches\n')
 s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
 s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
 s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
 s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
 s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
 s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
 s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
 s14 = net.addSwitch('s14', cls=OVSKernelSwitch)
 s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
 s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
 s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
 s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
 s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
 s7 = net.addSwitch('s7', cls=OVSKernelSwitch)

 info( '*** Adding Hosts\n')
 h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
 h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
 h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
 h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)

 info( '*** Adding links\n')
 net.addLink(h1, s13)
 net.addLink(s13, s10)
 net.addLink(s12, s11)
 net.addLink(s11, s10)
 net.addLink(s12, s14)
 net.addLink(s14, h2)
 net.addLink(s11, s1)
 net.addLink(s1, s2)
 net.addLink(s2, s4)
 net.addLink(s4, s3)
 net.addLink(s4, s7)
 net.addLink(s7, s5)
 net.addLink(s6, s7)
 net.addLink(s5, s8)
 net.addLink(s6, s9)
 net.addLink(s9, h4)
 net.addLink(s8, h3)

 info( '*** Building Network\n')
 net.build()
 info( '*** Starting Controller\n')
 for controller in net.controllers:
	controller.start()

 info( '*** Starting Switches\n')
 net.get('s6').start([c0])
 net.get('s1').start([c0])
 net.get('s13').start([c0])
 net.get('s4').start([c0])
 net.get('s12').start([c0])
 net.get('s10').start([c0])
 net.get('s3').start([c0])
 net.get('s14').start([c0])
 net.get('s8').start([c0])
 net.get('s11').start([c0])
 net.get('s9').start([c0])
 net.get('s5').start([c0])
 net.get('s2').start([c0])
 net.get('s7').start([c0])

 info( '*** Post configurtion of switches and hosts ***\n')
 info( '************************************************\n')
 info( '*********** NET4901 Official Topology **********\n')
 info( '* Created By: Carlos | Logan | Jiteng | Nissan *\n')
 info( '************************************************\n')

 CLI(net)
 net.stop()

if __name__ == '__main__':
 setLogLevel( 'info' )
 FinalProject()

