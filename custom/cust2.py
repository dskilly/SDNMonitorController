from mininet.topo import Topo
from math import log

class custom2(Topo):
	def __init__(self):
		Topo.__init__(self)
		n = 16
		sn = [self.addSwitch('s{}'.format(x)) for x in range(1, n + 2)]
		'''for i in range(int(log(n, 2))):
			self.addLink(sn[i], sn[i * 2 + 1])
			self.addLink(sn[i], sn[i * 2 + 2])
		for i in range(n - 1):
			for j in range(i + 1, n):
				self.addLink(sn[i], sn[j])'''
		for i in range(1, n + 1):
			self.addLink(sn[0], sn[i])

topos = {
	'topo': (lambda: custom2())
}